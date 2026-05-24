#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import textwrap
import webbrowser
from datetime import datetime
from pathlib import Path

import google_auth_oauthlib.flow
from google.ads.googleads.errors import GoogleAdsException


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env.ads"
SCOPES = ["https://www.googleapis.com/auth/adwords"]
USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}


def load_env(path: Path = ENV_PATH) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if "#" in value:
            value = value.split("#", 1)[0]
        env[key.strip()] = value.strip()
    return env


def update_env_value(path: Path, key: str, value: str) -> None:
    lines = path.read_text().splitlines()
    updated = False
    new_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f"{key}="):
            new_lines.append(f"{key}={value}")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        if new_lines and new_lines[-1].strip():
            new_lines.append("")
        new_lines.append(f"{key}={value}")

    path.write_text("\n".join(new_lines) + "\n")


def build_client_config(env: dict[str, str]) -> dict:
    return {
        "installed": {
            "client_id": env["CLIENT_ID"],
            "client_secret": env["CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def run_oauth(env: dict[str, str]) -> str:
    client_config = build_client_config(env)
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
        client_config, scopes=SCOPES
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true",
    )

    print("Abrindo autorização OAuth do Google Ads no navegador...")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    print("Se a janela não abrir, use este link:\n")
    print(auth_url)
    print("\nAguardando autorização no navegador...")

    flow.run_local_server(
        host="127.0.0.1",
        port=8080,
        authorization_prompt_message="",
        success_message="Autorização concluída. Pode voltar ao terminal.",
        open_browser=False,
    )

    refresh_token = flow.credentials.refresh_token
    if not refresh_token:
        raise RuntimeError("OAuth concluído sem refresh token.")
    return refresh_token


def ensure_refresh_token(env: dict[str, str], force: bool = False) -> dict[str, str]:
    refresh_token = env.get("REFRESH_TOKEN", "").strip()
    if refresh_token and not force:
        return env

    print("REFRESH_TOKEN ausente ou renovação solicitada.")
    refresh_token = run_oauth(env)
    update_env_value(ENV_PATH, "REFRESH_TOKEN", refresh_token)
    env["REFRESH_TOKEN"] = refresh_token
    print("\nRefresh token salvo em .env.ads.")
    print("Rode o comando novamente.\n")
    sys.exit(0)


def get_client():
    from core.client import get_client as _get_client

    return _get_client()


def gaql(query: str):
    env = load_env()
    ensure_refresh_token(env)

    client = get_client()
    service = client.get_service("GoogleAdsService")
    customer_id = env["CUSTOMER_ID"].replace("-", "")

    try:
        return list(service.search(customer_id=customer_id, query=query))
    except GoogleAdsException as exc:
        error_text = str(exc).lower()
        invalid_refresh = "invalid_grant" in error_text or "authentication" in error_text
        if invalid_refresh:
            print("Refresh token inválido ou expirado. Reabrindo OAuth...")
            ensure_refresh_token(env, force=True)
            client = get_client()
            service = client.get_service("GoogleAdsService")
            return list(service.search(customer_id=customer_id, query=query))
        raise


def money(micros: int | float) -> str:
    return f"R${micros / 1_000_000:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def brl(value: int | float) -> str:
    return f"R${value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def color(text: str, *styles: str) -> str:
    if not USE_COLOR or not styles:
        return text
    prefix = "".join(ANSI[style] for style in styles)
    return f"{prefix}{text}{ANSI['reset']}"


def campaign_color(channel: str) -> str:
    mapping = {
        "SEARCH": "blue",
        "PERFORMANCE_MAX": "magenta",
        "SHOPPING": "cyan",
    }
    return mapping.get(channel, "white")


def status_badge(status: str) -> str:
    palette = {
        "ENABLED": ("green", "bold"),
        "PAUSED": ("yellow", "bold"),
        "REMOVED": ("red", "bold"),
    }
    return color(status, *(palette.get(status, ("white",))))


def health_badge(status: str) -> str:
    palette = {
        "ELIGIBLE": ("green", "bold"),
        "LIMITED": ("yellow", "bold"),
        "NOT_ELIGIBLE": ("red", "bold"),
        "PAUSED": ("yellow", "bold"),
        "PENDING": ("cyan", "bold"),
    }
    return color(status, *(palette.get(status, ("white", "bold"))))


def bool_badge(value: bool) -> str:
    return color("yes" if value else "no", "green" if value else "red", "bold")


def metric(text: str, tone: str = "cyan") -> str:
    return color(text, tone, "bold")


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def pad(text: str, width: int, align: str = "left") -> str:
    visible = len(strip_ansi(text))
    if visible >= width:
        return text
    fill = " " * (width - visible)
    if align == "right":
        return fill + text
    return text + fill


def print_section(title: str) -> None:
    rule = color("=" * 96, "dim")
    print(f"\n{rule}")
    print(color(title, "cyan", "bold"))
    print(rule)


def safe_float(value) -> float:
    return float(value) if value is not None else 0.0


def shorten_reason(reasons: list[str]) -> str:
    if not reasons:
        return "-"
    text = ", ".join(reasons)
    return text if len(text) <= 38 else text[:35] + "..."


def get_campaign_rows(days: int) -> list[dict]:
    query = f"""
        SELECT
          campaign.name,
          campaign.status,
          campaign.primary_status,
          campaign.primary_status_reasons,
          campaign.advertising_channel_type,
          campaign_budget.amount_micros,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros,
          metrics.conversions,
          metrics.conversions_value
        FROM campaign
        WHERE campaign.status = ENABLED
          AND segments.date DURING LAST_{days}_DAYS
        ORDER BY campaign.name
    """
    rows = []
    for row in gaql(query):
        cost = row.metrics.cost_micros / 1_000_000
        value = safe_float(row.metrics.conversions_value)
        reasons = [reason.name for reason in row.campaign.primary_status_reasons]
        rows.append(
            {
                "name": row.campaign.name,
                "channel": row.campaign.advertising_channel_type.name,
                "status": row.campaign.status.name,
                "primary_status": row.campaign.primary_status.name,
                "reasons": reasons,
                "budget_brl": row.campaign_budget.amount_micros / 1_000_000,
                "impressions": int(row.metrics.impressions),
                "clicks": int(row.metrics.clicks),
                "cost_brl": round(cost, 2),
                "conversions": round(safe_float(row.metrics.conversions), 1),
                "value_brl": round(value, 2),
                "roas": round(value / cost, 2) if cost > 0 else 0.0,
            }
        )
    return rows


def get_conversion_rows() -> list[dict]:
    query = """
        SELECT
          conversion_action.name,
          conversion_action.status,
          conversion_action.include_in_conversions_metric,
          conversion_action.primary_for_goal,
          conversion_action.type,
          conversion_action.category
        FROM conversion_action
        WHERE conversion_action.category = PURCHASE
          AND conversion_action.status = ENABLED
        ORDER BY conversion_action.name
    """
    rows = []
    for row in gaql(query):
        rows.append(
            {
                "name": row.conversion_action.name,
                "status": row.conversion_action.status.name,
                "include": bool(row.conversion_action.include_in_conversions_metric),
                "primary": bool(row.conversion_action.primary_for_goal),
                "type": row.conversion_action.type_.name,
            }
        )
    return rows


def get_pmax_asset_group_rows(days: int) -> list[dict]:
    query = f"""
        SELECT
          asset_group.name,
          asset_group.status,
          asset_group.primary_status,
          asset_group.primary_status_reasons,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros
        FROM asset_group
        WHERE campaign.name = '[PMAX] - TODOS OS PRODUTOS I FORMAÇÃO'
          AND segments.date DURING LAST_{days}_DAYS
    """
    rows = []
    for row in gaql(query):
        rows.append(
            {
                "name": row.asset_group.name,
                "status": row.asset_group.status.name,
                "primary_status": row.asset_group.primary_status.name,
                "reasons": [reason.name for reason in row.asset_group.primary_status_reasons],
                "impressions": int(row.metrics.impressions),
                "clicks": int(row.metrics.clicks),
                "cost_brl": round(row.metrics.cost_micros / 1_000_000, 2),
            }
        )
    return rows


def get_change_rows() -> list[dict]:
    query = """
        SELECT
          change_event.change_date_time,
          change_event.change_resource_type,
          change_event.user_email,
          change_event.client_type
        FROM change_event
        WHERE change_event.change_date_time DURING LAST_7_DAYS
        ORDER BY change_event.change_date_time DESC
        LIMIT 10
    """
    rows = []
    for row in gaql(query):
        rows.append(
            {
                "at": str(row.change_event.change_date_time),
                "user_email": row.change_event.user_email,
                "client_type": row.change_event.client_type.name,
                "resource_type": row.change_event.change_resource_type.name,
            }
        )
    return rows


def build_snapshot(days: int, show_changes: bool) -> dict:
    campaigns = get_campaign_rows(days)
    conversions = get_conversion_rows()
    pmax_assets = get_pmax_asset_group_rows(days)
    changes = get_change_rows() if show_changes else []

    total_budget = sum(c["budget_brl"] for c in campaigns)
    total_cost = sum(c["cost_brl"] for c in campaigns)
    total_clicks = sum(c["clicks"] for c in campaigns)
    total_impressions = sum(c["impressions"] for c in campaigns)
    total_conversions = round(sum(c["conversions"] for c in campaigns), 1)
    total_value = round(sum(c["value_brl"] for c in campaigns), 2)
    total_roas = round(total_value / total_cost, 2) if total_cost > 0 else 0.0

    healthy = [c for c in campaigns if c["primary_status"] == "ELIGIBLE"]
    limited = [c for c in campaigns if c["primary_status"] == "LIMITED"]
    primary_purchase = [c for c in conversions if c["primary"]]

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "days": days,
        "campaign_count": len(campaigns),
        "healthy_count": len(healthy),
        "limited_count": len(limited),
        "total_daily_budget_brl": round(total_budget, 2),
        "total_cost_brl": round(total_cost, 2),
        "total_clicks": total_clicks,
        "total_impressions": total_impressions,
        "total_conversions": total_conversions,
        "total_value_brl": total_value,
        "total_roas": total_roas,
        "primary_purchase_names": [c["name"] for c in primary_purchase],
    }

    return {
        "summary": summary,
        "campaigns": campaigns,
        "conversions": conversions,
        "pmax_asset_groups": pmax_assets,
        "changes": changes,
    }


def print_summary(snapshot: dict) -> None:
    summary = snapshot["summary"]
    print_section("Resumo Executivo")
    items = [
        ("Campanhas", str(summary["campaign_count"])),
        ("Saudaveis", str(summary["healthy_count"])),
        ("Limitadas", str(summary["limited_count"])),
        ("Budget/dia", brl(summary["total_daily_budget_brl"])),
        ("Custo", brl(summary["total_cost_brl"])),
        ("Cliques", str(summary["total_clicks"])),
        ("Conversoes", str(summary["total_conversions"])),
        ("Valor", brl(summary["total_value_brl"])),
        ("ROAS", f"{summary['total_roas']:.2f}"),
    ]
    print("  " + "  ".join(f"{color(k + ':', 'dim')} {metric(v, 'white')}" for k, v in items))
    primary_names = ", ".join(summary["primary_purchase_names"]) or "-"
    print(f"  {color('Compra principal:', 'dim')} {metric(primary_names, 'green')}")


def print_campaign_table(snapshot: dict) -> None:
    print_section(f"Campanhas Ativas | Ultimos {snapshot['summary']['days']} dias")
    headers = ["Campanha", "Canal", "Budget", "Saude", "Custo", "Cliques", "Conv", "Valor", "ROAS", "Motivos"]
    widths = [34, 11, 10, 11, 10, 8, 7, 12, 7, 38]

    header_line = "  ".join(pad(color(h, "cyan", "bold"), w) for h, w in zip(headers, widths))
    print(header_line)
    print("  ".join("-" * w for w in widths))

    for row in snapshot["campaigns"]:
        values = [
            color(row["name"], campaign_color(row["channel"]), "bold"),
            color(row["channel"], campaign_color(row["channel"])),
            metric(brl(row["budget_brl"]), "cyan"),
            health_badge(row["primary_status"]),
            metric(brl(row["cost_brl"]), "yellow"),
            metric(str(row["clicks"]), "white"),
            metric(f"{row['conversions']:.1f}", "green"),
            metric(brl(row["value_brl"]), "green"),
            metric(f"{row['roas']:.2f}", "white"),
            color(shorten_reason(row["reasons"]), "dim"),
        ]
        aligned = [
            pad(value, width, "right" if idx in {2, 4, 5, 6, 7, 8} else "left")
            for idx, (value, width) in enumerate(zip(values, widths))
        ]
        print("  ".join(aligned))


def print_conversion_table(snapshot: dict) -> None:
    print_section("Conversoes de Compra")
    headers = ["Conversao", "Status", "Primary", "Include", "Tipo"]
    widths = [52, 10, 8, 8, 28]
    print("  ".join(pad(color(h, "cyan", "bold"), w) for h, w in zip(headers, widths)))
    print("  ".join("-" * w for w in widths))
    for row in snapshot["conversions"]:
        values = [
            color(row["name"], "blue", "bold"),
            status_badge(row["status"]),
            bool_badge(row["primary"]),
            bool_badge(row["include"]),
            color(row["type"], "dim"),
        ]
        print("  ".join(pad(value, width) for value, width in zip(values, widths)))


def print_pmax_section(snapshot: dict) -> None:
    if not snapshot["pmax_asset_groups"]:
        return
    print_section("PMAX | Asset Groups")
    headers = ["Asset Group", "Status", "Saude", "Custo", "Cliques", "Motivos"]
    widths = [28, 10, 11, 10, 8, 42]
    print("  ".join(pad(color(h, "cyan", "bold"), w) for h, w in zip(headers, widths)))
    print("  ".join("-" * w for w in widths))
    for row in snapshot["pmax_asset_groups"]:
        values = [
            color(row["name"], "magenta", "bold"),
            status_badge(row["status"]),
            health_badge(row["primary_status"]),
            metric(brl(row["cost_brl"]), "yellow"),
            metric(str(row["clicks"]), "white"),
            color(shorten_reason(row["reasons"]), "dim"),
        ]
        aligned = [
            pad(value, width, "right" if idx in {3, 4} else "left")
            for idx, (value, width) in enumerate(zip(values, widths))
        ]
        print("  ".join(aligned))


def print_changes(snapshot: dict) -> None:
    if not snapshot["changes"]:
        return
    print_section("Mudancas Recentes")
    headers = ["Quando", "Usuario", "Cliente", "Recurso"]
    widths = [21, 28, 18, 18]
    print("  ".join(pad(color(h, "cyan", "bold"), w) for h, w in zip(headers, widths)))
    print("  ".join("-" * w for w in widths))
    for row in snapshot["changes"]:
        values = [
            color(row["at"], "dim"),
            color(row["user_email"], "white", "bold"),
            color(row["client_type"], "yellow"),
            color(row["resource_type"], "cyan"),
        ]
        print("  ".join(pad(value, width) for value, width in zip(values, widths)))


def print_footer(snapshot: dict) -> None:
    print(
        textwrap.dedent(
            f"""
            Leitura rapida:
              - {health_badge('ELIGIBLE')} = saudavel
              - {health_badge('LIMITED')} = rodando, mas com restricao de budget/aprendizado/politica
              - {bool_badge(True)} na compra certa = Smart Bidding limpo
              - janela atual = ultimos {snapshot['summary']['days']} dias
            """
        ).strip()
    )


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def build_markdown(snapshot: dict) -> str:
    summary = snapshot["summary"]
    campaign_rows = [
        [
            row["name"],
            row["channel"],
            brl(row["budget_brl"]),
            row["primary_status"],
            brl(row["cost_brl"]),
            str(row["clicks"]),
            f"{row['conversions']:.1f}",
            brl(row["value_brl"]),
            f"{row['roas']:.2f}",
            shorten_reason(row["reasons"]),
        ]
        for row in snapshot["campaigns"]
    ]
    conversion_rows = [
        [row["name"], row["status"], str(row["primary"]), str(row["include"]), row["type"]]
        for row in snapshot["conversions"]
    ]
    pmax_rows = [
        [
            row["name"],
            row["status"],
            row["primary_status"],
            brl(row["cost_brl"]),
            str(row["clicks"]),
            shorten_reason(row["reasons"]),
        ]
        for row in snapshot["pmax_asset_groups"]
    ]

    sections = [
        "# RZ Ads Status",
        "",
        f"- Gerado em: `{summary['generated_at']}`",
        f"- Janela: `{summary['days']} dias`",
        f"- Budget/dia: `{brl(summary['total_daily_budget_brl'])}`",
        f"- Custo: `{brl(summary['total_cost_brl'])}`",
        f"- Conversoes: `{summary['total_conversions']}`",
        f"- Valor: `{brl(summary['total_value_brl'])}`",
        f"- ROAS: `{summary['total_roas']:.2f}`",
        f"- Compra principal: `{', '.join(summary['primary_purchase_names']) or '-'}`",
        "",
        "## Campanhas",
        markdown_table(
            ["Campanha", "Canal", "Budget", "Saude", "Custo", "Cliques", "Conv", "Valor", "ROAS", "Motivos"],
            campaign_rows,
        ),
        "",
        "## Conversoes de Compra",
        markdown_table(["Conversao", "Status", "Primary", "Include", "Tipo"], conversion_rows),
    ]

    if pmax_rows:
        sections.extend(
            [
                "",
                "## PMAX Asset Groups",
                markdown_table(["Asset Group", "Status", "Saude", "Custo", "Cliques", "Motivos"], pmax_rows),
            ]
        )

    if snapshot["changes"]:
        change_rows = [
            [row["at"], row["user_email"], row["client_type"], row["resource_type"]]
            for row in snapshot["changes"]
        ]
        sections.extend(
            [
                "",
                "## Mudancas Recentes",
                markdown_table(["Quando", "Usuario", "Cliente", "Recurso"], change_rows),
            ]
        )

    return "\n".join(sections) + "\n"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_outputs(snapshot: dict, json_out: str | None, md_out: str | None) -> None:
    if json_out:
        path = Path(json_out).expanduser()
        ensure_parent(path)
        path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        print(f"\nJSON salvo em {path}")
    if md_out:
        path = Path(md_out).expanduser()
        ensure_parent(path)
        path.write_text(build_markdown(snapshot))
        print(f"Markdown salvo em {path}")


def cmd_auth(_: argparse.Namespace) -> int:
    env = load_env()
    ensure_refresh_token(env, force=True)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    snapshot = build_snapshot(days=args.days, show_changes=args.show_changes)
    print_summary(snapshot)
    print_campaign_table(snapshot)
    print_conversion_table(snapshot)
    print_pmax_section(snapshot)
    print_changes(snapshot)
    print_footer(snapshot)
    write_outputs(snapshot, args.json_out, args.md_out)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    snapshot = build_snapshot(days=args.days, show_changes=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    default_json = BASE_DIR / "memory" / "reports" / f"rzads-report-{timestamp}.json"
    default_md = Path.home() / "Documentos" / f"rzads-report-{timestamp}.md"
    json_out = args.json_out or str(default_json)
    md_out = args.md_out or str(default_md)

    print_summary(snapshot)
    print_campaign_table(snapshot)
    print_conversion_table(snapshot)
    print_pmax_section(snapshot)
    print_changes(snapshot)
    print_footer(snapshot)
    write_outputs(snapshot, json_out, md_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resumo operacional da conta Google Ads da RZVET.")
    sub = parser.add_subparsers(dest="command")

    auth = sub.add_parser("auth", help="Renova o refresh token do Google Ads.")
    auth.set_defaults(func=cmd_auth)

    status = sub.add_parser("status", help="Mostra saude e metricas principais.")
    status.add_argument("--days", type=int, default=7, choices=[7, 14, 30], help="Janela de analise.")
    status.add_argument("--show-changes", action="store_true", help="Mostra historico recente de alteracoes.")
    status.add_argument("--json-out", help="Salva snapshot em JSON.")
    status.add_argument("--md-out", help="Salva snapshot em Markdown.")
    status.set_defaults(func=cmd_status)

    report = sub.add_parser("report", help="Gera relatorio com export JSON e Markdown.")
    report.add_argument("--days", type=int, default=14, choices=[7, 14, 30], help="Janela de analise.")
    report.add_argument("--json-out", help="Caminho customizado para JSON.")
    report.add_argument("--md-out", help="Caminho customizado para Markdown.")
    report.set_defaults(func=cmd_report)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        args = parser.parse_args(["status"])
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
