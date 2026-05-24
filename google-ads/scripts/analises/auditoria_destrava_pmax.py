"""Auditoria para validar plano de destravar PMAX e otimizar conta.

Coleta:
1. Performance 7d e 30d por campanha (com status, budget, bidding)
2. Bidding strategy detalhada da PMAX (tROAS atual, status de restrição)
3. Geo performance 30d (quais locais foram cortados / onde performa)
4. Search terms da Search Produtos 30d (cost>0 conv=0)
5. Recomendações ativas (BIDDING_STRATEGY_CONSTRAINED, etc.)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.client import get_client, CUSTOMER_ID
from core.reports import _query, get_campaign_performance


def perf_window(days: int):
    print(f"\n=== PERFORMANCE {days}D (campanhas com gasto > 0) ===")
    rows = get_campaign_performance(days=days)
    rows = [r for r in rows if r["cost_brl"] > 0]
    for r in rows:
        print(
            f"  [{r['status']:8}] {r['name']:55} "
            f"cost R${r['cost_brl']:7.2f}  conv {r['conversions']:5.1f}  "
            f"val R${r['conv_value_brl']:8.2f}  ROAS {r['roas']:6.2f}  "
            f"clicks {r['clicks']}"
        )
    return rows


def campaign_settings():
    print("\n=== BIDDING STRATEGY / ORÇAMENTO POR CAMPANHA ATIVA ===")
    gaql = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign.bidding_strategy_type,
            campaign.maximize_conversion_value.target_roas,
            campaign.target_roas.target_roas,
            campaign.target_cpa.target_cpa_micros,
            campaign_budget.amount_micros,
            campaign.primary_status,
            campaign.primary_status_reasons
        FROM campaign
        WHERE campaign.status = 'ENABLED'
        ORDER BY campaign_budget.amount_micros DESC
    """
    out = []
    for row in _query(gaql):
        c = row.campaign
        b = row.campaign_budget
        troas_mcv = c.maximize_conversion_value.target_roas
        troas_t = c.target_roas.target_roas
        troas = troas_mcv or troas_t
        reasons = [r.name for r in c.primary_status_reasons]
        info = {
            "id": c.id,
            "name": c.name,
            "channel": c.advertising_channel_type.name,
            "bid_strategy": c.bidding_strategy_type.name,
            "target_roas": round(troas, 2) if troas else None,
            "tcpa_brl": round(c.target_cpa.target_cpa_micros / 1_000_000, 2) if c.target_cpa.target_cpa_micros else None,
            "budget_brl": round(b.amount_micros / 1_000_000, 2),
            "primary_status": c.primary_status.name,
            "primary_status_reasons": reasons,
        }
        out.append(info)
        print(
            f"  {info['name']:55} {info['channel']:12} "
            f"{info['bid_strategy']:25} tROAS={info['target_roas']} "
            f"budget R${info['budget_brl']}/dia  status={info['primary_status']}"
        )
        if reasons:
            print(f"      ⚠ reasons: {reasons}")
    return out


def geo_performance(days: int = 30):
    print(f"\n=== GEO PERFORMANCE {days}D (top 30 por gasto) ===")
    gaql = f"""
        SELECT
            campaign.name,
            geographic_view.country_criterion_id,
            geographic_view.location_type,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.clicks,
            segments.geo_target_city,
            segments.geo_target_region,
            segments.geo_target_state
        FROM geographic_view
        WHERE segments.date DURING LAST_{days}_DAYS
            AND metrics.cost_micros > 0
        ORDER BY metrics.cost_micros DESC
        LIMIT 30
    """
    out = []
    for row in _query(gaql):
        cost = row.metrics.cost_micros / 1_000_000
        cv = row.metrics.conversions_value
        info = {
            "campaign": row.campaign.name,
            "city_resource": row.segments.geo_target_city,
            "region_resource": row.segments.geo_target_region,
            "state_resource": row.segments.geo_target_state,
            "cost_brl": round(cost, 2),
            "conversions": round(row.metrics.conversions, 1),
            "conv_value_brl": round(cv, 2),
            "roas": round(cv / cost, 2) if cost > 0 else 0,
            "clicks": row.metrics.clicks,
        }
        out.append(info)
        print(
            f"  {info['campaign']:40} city={info['city_resource'] or '-':35} "
            f"cost R${info['cost_brl']:6.2f}  conv {info['conversions']:4.1f}  ROAS {info['roas']:5.2f}"
        )
    return out


def campaign_targeted_locations():
    print("\n=== LOCALIZAÇÕES SEGMENTADAS POR CAMPANHA ATIVA ===")
    gaql = """
        SELECT
            campaign.id,
            campaign.name,
            campaign_criterion.location.geo_target_constant,
            campaign_criterion.negative,
            campaign_criterion.status
        FROM campaign_criterion
        WHERE campaign.status = 'ENABLED'
          AND campaign_criterion.type = 'LOCATION'
          AND campaign_criterion.status != 'REMOVED'
    """
    by_campaign = {}
    for row in _query(gaql):
        name = row.campaign.name
        by_campaign.setdefault(name, {"positive": [], "negative": []})
        loc = row.campaign_criterion.location.geo_target_constant
        if row.campaign_criterion.negative:
            by_campaign[name]["negative"].append(loc)
        else:
            by_campaign[name]["positive"].append(loc)
    for cname, locs in by_campaign.items():
        print(f"  {cname}: {len(locs['positive'])} positivos, {len(locs['negative'])} negativos")
    return by_campaign


def search_produtos_bad_terms(days: int = 30):
    print(f"\n=== SEARCH TERMS — gasto>0 e conv=0 (todas as Search) últimos {days}d ===")
    gaql = f"""
        SELECT
            campaign.name,
            campaign.advertising_channel_type,
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.clicks,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_{days}_DAYS
          AND campaign.advertising_channel_type = 'SEARCH'
          AND metrics.cost_micros > 0
          AND metrics.conversions = 0
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """
    out = []
    for row in _query(gaql):
        cost = row.metrics.cost_micros / 1_000_000
        info = {
            "campaign": row.campaign.name,
            "term": row.search_term_view.search_term,
            "cost_brl": round(cost, 2),
            "clicks": row.metrics.clicks,
        }
        out.append(info)
        print(f"  {info['campaign']:40} '{info['term'][:50]:50}' R${info['cost_brl']:5.2f} clicks={info['clicks']}")
    total = sum(r["cost_brl"] for r in out)
    print(f"  TOTAL desperdiçado (top 50): R${total:.2f}")
    return out


def recommendations():
    print("\n=== RECOMENDAÇÕES ATIVAS ===")
    gaql = """
        SELECT
            recommendation.type,
            recommendation.campaign,
            recommendation.impact.base_metrics.cost_micros,
            recommendation.impact.potential_metrics.cost_micros,
            recommendation.target_roas_recommendation.recommended_target_roas,
            recommendation.target_roas_recommendation.current_average_target_roas
        FROM recommendation
    """
    out = []
    try:
        for row in _query(gaql):
            info = {
                "type": row.recommendation.type.name,
                "campaign": row.recommendation.campaign,
                "current_troas": row.recommendation.target_roas_recommendation.current_average_target_roas or None,
                "recommended_troas": row.recommendation.target_roas_recommendation.recommended_target_roas or None,
            }
            out.append(info)
            extra = ""
            if info["recommended_troas"]:
                extra = f"  current={info['current_troas']} → recommended={info['recommended_troas']}"
            print(f"  {info['type']:40} {info['campaign']}{extra}")
    except Exception as e:
        print(f"  erro lendo recommendations: {e}")
    return out


def main():
    print(f"Cliente: {CUSTOMER_ID}")
    data = {}
    data["perf_7d"] = perf_window(7)
    data["perf_30d"] = perf_window(30)
    data["settings"] = campaign_settings()
    data["locations_targeted"] = campaign_targeted_locations()
    data["geo_30d"] = geo_performance(30)
    data["bad_search_terms_30d"] = search_produtos_bad_terms(30)
    data["recommendations"] = recommendations()

    out_path = Path(__file__).resolve().parents[2] / "data" / "auditoria_destrava_pmax.json"
    out_path.parent.mkdir(exist_ok=True)
    with out_path.open("w") as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)
    print(f"\n✓ Snapshot salvo em {out_path}")


if __name__ == "__main__":
    main()
