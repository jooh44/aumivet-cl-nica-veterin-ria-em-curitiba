"""
Análise de Campanhas — Março 2026
Objetivo: Detectar impacto da queda de pagamento no início do mês,
verificar recuperação dos produtos caros e status de reaprendizado do algoritmo.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from core.reports import _query
from core.client import CUSTOMER_ID
from datetime import date, timedelta

today = date.today()  # 2026-03-30

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def fmt_brl(v): return f"R${v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def fmt_pct(v): return f"{v:.1f}%"


# ─────────────────────────────────────────────
# 1. PERFORMANCE DIÁRIA — Março completo (detectar queda e recuperação)
# ─────────────────────────────────────────────

def performance_diaria_marco():
    gaql = """
        SELECT
            segments.date,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '2026-03-01' AND '2026-03-30'
        ORDER BY segments.date
    """
    rows = _query(gaql)

    por_dia = {}
    for row in rows:
        d = row.segments.date
        if d not in por_dia:
            por_dia[d] = {"impressions": 0, "clicks": 0, "cost": 0, "conv": 0, "value": 0}
        por_dia[d]["impressions"] += row.metrics.impressions
        por_dia[d]["clicks"] += row.metrics.clicks
        por_dia[d]["cost"] += row.metrics.cost_micros / 1_000_000
        por_dia[d]["conv"] += row.metrics.conversions
        por_dia[d]["value"] += row.metrics.conversions_value

    print("\n" + "="*70)
    print("📅 PERFORMANCE DIÁRIA — MARÇO 2026")
    print("="*70)
    print(f"{'Data':<12} {'Impress':>8} {'Cliques':>8} {'Custo':>10} {'Conv':>6} {'Faturamento':>12} {'ROAS':>6}")
    print("-"*70)

    for d in sorted(por_dia.keys()):
        m = por_dia[d]
        roas = m["value"] / m["cost"] if m["cost"] > 0 else 0
        flag = ""
        if m["cost"] < 50:
            flag = " ⚠️ BAIXO"
        elif roas > 5:
            flag = " ✅"
        print(f"{d:<12} {m['impressions']:>8,} {m['clicks']:>8,} {fmt_brl(m['cost']):>10} {m['conv']:>6.1f} {fmt_brl(m['value']):>12} {roas:>6.2f}{flag}")

    return por_dia


# ─────────────────────────────────────────────
# 2. COMPARATIVO: SEMANA DA QUEDA vs SEMANA ATUAL
# ─────────────────────────────────────────────

def comparativo_semanas():
    # Semana 1 (queda): 01-07/03
    # Semana atual (recuperação): 24-30/03
    queries = {
        "Semana 01-07/03 (queda)": ("2026-03-01", "2026-03-07"),
        "Semana 10-16/03": ("2026-03-10", "2026-03-16"),
        "Semana 17-23/03": ("2026-03-17", "2026-03-23"),
        "Semana 24-30/03 (atual)": ("2026-03-24", "2026-03-30"),
    }

    print("\n" + "="*70)
    print("📊 COMPARATIVO POR SEMANA — MARÇO 2026")
    print("="*70)

    resultados = {}
    for label, (start, end) in queries.items():
        gaql = f"""
            SELECT
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value
            FROM campaign
            WHERE segments.date BETWEEN '{start}' AND '{end}'
        """
        rows = _query(gaql)
        tot = {"impressions": 0, "clicks": 0, "cost": 0, "conv": 0, "value": 0}
        for row in rows:
            tot["impressions"] += row.metrics.impressions
            tot["clicks"] += row.metrics.clicks
            tot["cost"] += row.metrics.cost_micros / 1_000_000
            tot["conv"] += row.metrics.conversions
            tot["value"] += row.metrics.conversions_value
        resultados[label] = tot

        roas = tot["value"] / tot["cost"] if tot["cost"] > 0 else 0
        print(f"\n  {label}")
        print(f"    Custo: {fmt_brl(tot['cost'])}  |  Faturamento: {fmt_brl(tot['value'])}  |  ROAS: {roas:.2f}")
        print(f"    Impressões: {tot['impressions']:,}  |  Cliques: {tot['clicks']:,}  |  Conv: {tot['conv']:.1f}")

    return resultados


# ─────────────────────────────────────────────
# 3. PERFORMANCE POR CAMPANHA — Março completo
# ─────────────────────────────────────────────

def campanhas_marco():
    gaql = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.search_impression_share,
            metrics.search_budget_lost_impression_share,
            metrics.search_rank_lost_impression_share
        FROM campaign
        WHERE segments.date BETWEEN '2026-03-01' AND '2026-03-30'
            AND campaign.status = 'ENABLED'
        ORDER BY metrics.cost_micros DESC
    """
    rows = _query(gaql)

    campanhas = {}
    for row in rows:
        cid = row.campaign.id
        if cid not in campanhas:
            campanhas[cid] = {
                "name": row.campaign.name,
                "channel": row.campaign.advertising_channel_type.name,
                "impressions": 0, "clicks": 0, "cost": 0, "conv": 0, "value": 0,
                "imp_share": row.metrics.search_impression_share,
                "lost_budget": row.metrics.search_budget_lost_impression_share,
                "lost_rank": row.metrics.search_rank_lost_impression_share,
            }
        campanhas[cid]["impressions"] += row.metrics.impressions
        campanhas[cid]["clicks"] += row.metrics.clicks
        campanhas[cid]["cost"] += row.metrics.cost_micros / 1_000_000
        campanhas[cid]["conv"] += row.metrics.conversions
        campanhas[cid]["value"] += row.metrics.conversions_value

    print("\n" + "="*70)
    print("🎯 CAMPANHAS ATIVAS — MARÇO 2026 (01 a 30)")
    print("="*70)
    print(f"{'Campanha':<35} {'Custo':>10} {'ROAS':>6} {'Conv':>6} {'Faturamento':>12} {'IS%':>6}")
    print("-"*70)

    total_cost = 0
    total_value = 0
    total_conv = 0

    for cid, c in sorted(campanhas.items(), key=lambda x: -x[1]["cost"]):
        roas = c["value"] / c["cost"] if c["cost"] > 0 else 0
        is_pct = c["imp_share"] * 100 if c["imp_share"] else 0
        nome = c["name"][:34]
        print(f"{nome:<35} {fmt_brl(c['cost']):>10} {roas:>6.2f} {c['conv']:>6.1f} {fmt_brl(c['value']):>12} {is_pct:>5.0f}%")
        total_cost += c["cost"]
        total_value += c["value"]
        total_conv += c["conv"]

    print("-"*70)
    total_roas = total_value / total_cost if total_cost > 0 else 0
    print(f"{'TOTAL':<35} {fmt_brl(total_cost):>10} {total_roas:>6.2f} {total_conv:>6.1f} {fmt_brl(total_value):>12}")

    return campanhas


# ─────────────────────────────────────────────
# 4. SHOPPING — Produtos caros (ticket alto)
#    Detectar se estão voltando com impressões
# ─────────────────────────────────────────────

def shopping_produtos_caros():
    gaql = """
        SELECT
            segments.product_title,
            segments.product_item_id,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM shopping_performance_view
        WHERE segments.date BETWEEN '2026-03-01' AND '2026-03-30'
        ORDER BY metrics.conversions_value DESC
        LIMIT 50
    """
    try:
        rows = _query(gaql)
    except Exception as e:
        print(f"\n  [Shopping] Erro: {e}")
        return []

    print("\n" + "="*70)
    print("🛒 SHOPPING — TOP 50 PRODUTOS POR FATURAMENTO (Março 2026)")
    print("="*70)
    print(f"{'Produto':<45} {'Impress':>8} {'Cliq':>6} {'Custo':>10} {'Faturamento':>12}")
    print("-"*70)

    produtos = []
    for row in rows:
        cost = row.metrics.cost_micros / 1_000_000
        value = row.metrics.conversions_value
        titulo = (row.segments.product_title or "—")[:44]
        print(f"{titulo:<45} {row.metrics.impressions:>8,} {row.metrics.clicks:>6,} {fmt_brl(cost):>10} {fmt_brl(value):>12}")
        produtos.append({
            "titulo": row.segments.product_title,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": cost,
            "value": value,
        })

    return produtos


# ─────────────────────────────────────────────
# 5. SHOPPING — Semana queda vs semana atual (produtos ticket alto)
# ─────────────────────────────────────────────

def shopping_comparativo():
    periodos = {
        "01-07/03 (queda)": ("2026-03-01", "2026-03-07"),
        "24-30/03 (atual)": ("2026-03-24", "2026-03-30"),
    }

    print("\n" + "="*70)
    print("🛒 SHOPPING — COMPARATIVO SEMANA QUEDA vs SEMANA ATUAL")
    print("="*70)

    for label, (start, end) in periodos.items():
        gaql = f"""
            SELECT
                segments.product_title,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions_value
            FROM shopping_performance_view
            WHERE segments.date BETWEEN '{start}' AND '{end}'
            ORDER BY metrics.conversions_value DESC
            LIMIT 20
        """
        try:
            rows = _query(gaql)
        except Exception as e:
            print(f"\n  [{label}] Erro: {e}")
            continue

        print(f"\n  📅 {label} — Top 10 produtos por faturamento:")
        print(f"  {'Produto':<45} {'Impress':>8} {'Faturamento':>12}")
        print("  " + "-"*67)

        for i, row in enumerate(rows):
            if i >= 10:
                break
            titulo = (row.segments.product_title or "—")[:44]
            value = row.metrics.conversions_value
            impr = row.metrics.impressions
            print(f"  {titulo:<45} {impr:>8,} {fmt_brl(value):>12}")


# ─────────────────────────────────────────────
# 6. SEARCH TERMS RECENTES — Termos de ticket alto
# ─────────────────────────────────────────────

def search_terms_recentes():
    gaql = """
        SELECT
            campaign.name,
            search_term_view.search_term,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM search_term_view
        WHERE segments.date BETWEEN '2026-03-24' AND '2026-03-30'
        ORDER BY metrics.cost_micros DESC
        LIMIT 40
    """
    rows = _query(gaql)

    print("\n" + "="*70)
    print("🔍 TERMOS DE PESQUISA — ÚLTIMOS 7 DIAS (24-30/03)")
    print("="*70)
    print(f"{'Termo':<40} {'Custo':>10} {'Conv':>6} {'Faturamento':>12} {'Campanha':<25}")
    print("-"*70)

    for row in rows:
        cost = row.metrics.cost_micros / 1_000_000
        value = row.metrics.conversions_value
        termo = row.search_term_view.search_term[:39]
        camp = row.campaign.name[:24]
        print(f"{termo:<40} {fmt_brl(cost):>10} {row.metrics.conversions:>6.1f} {fmt_brl(value):>12} {camp:<25}")


# ─────────────────────────────────────────────
# 7. STATUS DE APRENDIZADO DAS CAMPANHAS
# ─────────────────────────────────────────────

def status_aprendizado():
    gaql = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.bidding_strategy_type,
            campaign_budget.amount_micros,
            metrics.cost_micros,
            metrics.conversions,
            metrics.impressions
        FROM campaign
        WHERE segments.date BETWEEN '2026-03-01' AND '2026-03-30'
            AND campaign.status = 'ENABLED'
        ORDER BY metrics.cost_micros DESC
    """
    rows = _query(gaql)

    campanhas = {}
    for row in rows:
        cid = row.campaign.id
        if cid not in campanhas:
            campanhas[cid] = {
                "name": row.campaign.name,
                "strategy": row.campaign.bidding_strategy_type.name,
                "budget_dia": row.campaign_budget.amount_micros / 1_000_000,
                "cost": 0, "conv": 0, "impressions": 0,
            }
        campanhas[cid]["cost"] += row.metrics.cost_micros / 1_000_000
        campanhas[cid]["conv"] += row.metrics.conversions
        campanhas[cid]["impressions"] += row.metrics.impressions

    print("\n" + "="*70)
    print("🧠 STATUS DE APRENDIZADO — CAMPANHAS SMART BIDDING")
    print("   (Smart Bidding precisa de ~30-50 conv/mês para estabilizar)")
    print("="*70)
    print(f"{'Campanha':<35} {'Estratégia':<22} {'Conv/mês':>9} {'Status'}")
    print("-"*70)

    for cid, c in sorted(campanhas.items(), key=lambda x: -x[1]["conv"]):
        conv = c["conv"]
        estrategia = c["strategy"].replace("TARGET_", "T_").replace("MAXIMIZE_", "MAX_")

        # Avaliação de aprendizado
        if "MANUAL" in c["strategy"]:
            status = "Manual — sem aprendizado"
        elif conv >= 50:
            status = "✅ Estabilizado"
        elif conv >= 30:
            status = "🟡 Aprendendo (quase lá)"
        elif conv >= 10:
            status = "🟠 Reaprendendo"
        else:
            status = "🔴 Aprendizado inicial / incerto"

        nome = c["name"][:34]
        print(f"{nome:<35} {estrategia:<22} {conv:>9.1f} {status}")

    print("\n  Ref: Google leva ~2 semanas + 30-50 conv para restabilizar após interrupção.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "█"*70)
    print("  ANÁLISE COMPLETA — CAMPANHAS RZVET — MARÇO 2026")
    print("  Gerado em: " + str(today))
    print("█"*70)

    try:
        performance_diaria_marco()
    except Exception as e:
        print(f"\n[ERRO] Performance diária: {e}")

    try:
        comparativo_semanas()
    except Exception as e:
        print(f"\n[ERRO] Comparativo semanas: {e}")

    try:
        campanhas_marco()
    except Exception as e:
        print(f"\n[ERRO] Campanhas: {e}")

    try:
        shopping_produtos_caros()
    except Exception as e:
        print(f"\n[ERRO] Shopping produtos: {e}")

    try:
        shopping_comparativo()
    except Exception as e:
        print(f"\n[ERRO] Shopping comparativo: {e}")

    try:
        search_terms_recentes()
    except Exception as e:
        print(f"\n[ERRO] Search terms: {e}")

    try:
        status_aprendizado()
    except Exception as e:
        print(f"\n[ERRO] Status aprendizado: {e}")

    print("\n" + "█"*70)
    print("  FIM DA ANÁLISE")
    print("█"*70 + "\n")
