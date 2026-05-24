"""
manager.py — Orquestrador de otimizações para RZ VET Google Ads.

Uso:
    python manager.py --dry-run        # simula, não executa
    python manager.py --execute        # executa de verdade (cuidado)
    python manager.py --snapshot       # só salva snapshot de campanhas

Fluxo:
    1. Puxa dados via core/reports.py
    2. Avalia regras de rules_config.json
    3. Loga decisões em memory/decisions_log.md
    4. Aplica mudanças via core/mutates.py (se não dry-run)
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

from core.reports import get_campaign_performance, get_keywords_performance
from core.mutates import pause_keyword, update_keyword_bid

BASE = Path(__file__).parent
MEMORY = BASE / "memory"
CONFIG_PATH = MEMORY / "rules_config.json"
SNAPSHOT_PATH = MEMORY / "campaigns_snapshot.json"
LOG_PATH = MEMORY / "decisions_log.md"


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_snapshot(data: dict):
    data["_meta"] = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    with open(SNAPSHOT_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Snapshot salvo em {SNAPSHOT_PATH}")


def log_decision(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_PATH, "a") as f:
        f.write(f"\n## {timestamp}\n{message}\n")


def run_snapshot():
    """Salva snapshot atual de campanhas e keywords."""
    print("Puxando dados de campanhas...")
    campaigns = get_campaign_performance(days=30, status_filter="ENABLED")
    keywords = get_keywords_performance(days=30)
    save_snapshot({"campaigns": campaigns, "keywords": keywords})


def run_pause_bleeding(config: dict, dry_run: bool):
    """Pausa keywords que gastam muito sem converter."""
    rule = config["rules"]["pause_bleeding_keyword"]
    if not rule["enabled"]:
        print("[pause_bleeding_keyword] desabilitado — pulando")
        return

    conds = rule["conditions"]
    keywords = get_keywords_performance(days=conds["min_days"])

    candidates = [
        kw for kw in keywords
        if kw["cost_brl"] >= conds["min_cost_brl"]
        and kw["conversions"] <= conds["max_conversions"]
    ]

    if not candidates:
        print("[pause_bleeding_keyword] Nenhuma keyword candidata encontrada")
        return

    print(f"[pause_bleeding_keyword] {len(candidates)} candidatas:")
    for kw in candidates:
        print(f"  {kw['keyword']} | R${kw['cost_brl']} | {kw['conversions']} conv | {kw['campaign']}")

    if dry_run:
        print("[DRY RUN] Nenhuma alteração feita")
        return

    for kw in candidates:
        result = pause_keyword(kw["keyword"], kw["campaign_id"], dry_run=False)
        log_decision(f"- Pausada keyword '{kw['keyword']}' (R${kw['cost_brl']}, {kw['conversions']} conv) — {result}")
        print(f"  Pausada: {kw['keyword']}")


def main():
    parser = argparse.ArgumentParser(description="Manager de otimizações RZ VET Ads")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--snapshot", action="store_true")
    args = parser.parse_args()

    dry_run = not args.execute

    if args.snapshot:
        run_snapshot()
        return

    config = load_config()
    print(f"Modo: {'DRY RUN' if dry_run else 'EXECUTE'}")
    print(f"Regras ativas: {[k for k, v in config['rules'].items() if v['enabled']]}")

    run_pause_bleeding(config, dry_run)


if __name__ == "__main__":
    main()
