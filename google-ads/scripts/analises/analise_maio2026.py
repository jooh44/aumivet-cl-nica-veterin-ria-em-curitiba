#!/usr/bin/env python3
"""Performance Google Ads — Maio 2026 (01-09)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.client import get_client, CUSTOMER_ID

client = get_client()
svc = client.get_service("GoogleAdsService")

START, END = "2026-05-01", "2026-05-09"

def q(gaql):
    return list(svc.search(customer_id=CUSTOMER_ID, query=gaql))

def brl(micros):
    return round(micros / 1_000_000, 2)


# ── Campanhas ──────────────────────────────────────────────────
rows = q(f"""
    SELECT
        campaign.id, campaign.name, campaign.status,
        campaign.advertising_channel_type,
        campaign.primary_status,
        campaign_budget.amount_micros,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value,
        metrics.ctr, metrics.average_cpc,
        metrics.search_impression_share
    FROM campaign
    WHERE segments.date BETWEEN '{START}' AND '{END}'
    ORDER BY metrics.cost_micros DESC
""")

campaigns = []
total_cost = total_conv = total_val = 0
for r in rows:
    cost = brl(r.metrics.cost_micros)
    val  = round(r.metrics.conversions_value, 2)
    conv = round(r.metrics.conversions, 2)
    total_cost += cost; total_conv += conv; total_val += val
    campaigns.append({
        "name": r.campaign.name,
        "status": r.campaign.status.name,
        "primary": r.campaign.primary_status.name,
        "channel": r.campaign.advertising_channel_type.name,
        "budget": brl(r.campaign_budget.amount_micros),
        "impressions": r.metrics.impressions,
        "clicks": r.metrics.clicks,
        "cost": cost,
        "conv": conv,
        "val": val,
        "roas": round(val / cost, 2) if cost > 0 else 0,
        "ctr": round(r.metrics.ctr * 100, 2),
        "cpc": brl(r.metrics.average_cpc),
        "is": round(r.metrics.search_impression_share * 100, 1) if r.metrics.search_impression_share else None,
    })

print("\n" + "="*70)
print(f"CAMPANHAS — {START} a {END}")
print("="*70)
print(f"{'Campanha':<42} {'Status':<10} {'Custo':>8} {'Conv':>6} {'Val':>9} {'ROAS':>6} {'IS%':>5}")
print("-"*85)
for c in campaigns:
    is_str = f"{c['is']:.0f}%" if c['is'] is not None else "  N/A"
    print(f"{c['name'][:41]:<42} {c['primary']:<10} R${c['cost']:>7.2f} {c['conv']:>6.1f} R${c['val']:>8.2f} {c['roas']:>5.2f}x {is_str:>5}")

print("-"*85)
roas_total = round(total_val / total_cost, 2) if total_cost > 0 else 0
print(f"{'TOTAL':<42} {'':>10} R${total_cost:>7.2f} {total_conv:>6.1f} R${total_val:>8.2f} {roas_total:>5.2f}x")


# ── Tendência diária ───────────────────────────────────────────
rows = q(f"""
    SELECT
        segments.date,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value
    FROM campaign
    WHERE segments.date BETWEEN '{START}' AND '{END}'
        AND campaign.status = 'ENABLED'
    ORDER BY segments.date
""")

daily = {}
for r in rows:
    d = str(r.segments.date)
    if d not in daily:
        daily[d] = {"imp": 0, "clicks": 0, "cost": 0, "conv": 0, "val": 0}
    daily[d]["imp"]    += r.metrics.impressions
    daily[d]["clicks"] += r.metrics.clicks
    daily[d]["cost"]   += brl(r.metrics.cost_micros)
    daily[d]["conv"]   += r.metrics.conversions
    daily[d]["val"]    += r.metrics.conversions_value

print("\n" + "="*70)
print("TENDÊNCIA DIÁRIA")
print("="*70)
print(f"{'Data':<12} {'Impr':>7} {'Cliques':>8} {'Custo':>9} {'Conv':>6} {'Valor':>9} {'ROAS':>6}")
print("-"*65)
for d in sorted(daily):
    x = daily[d]
    x["cost"] = round(x["cost"], 2)
    x["conv"] = round(x["conv"], 2)
    x["val"]  = round(x["val"], 2)
    roas = round(x["val"] / x["cost"], 2) if x["cost"] > 0 else 0
    print(f"{d:<12} {x['imp']:>7,} {x['clicks']:>8,} R${x['cost']:>8.2f} {x['conv']:>6.1f} R${x['val']:>8.2f} {roas:>5.2f}x")


# ── Ad Groups (top 15) ─────────────────────────────────────────
rows = q(f"""
    SELECT
        campaign.name, ad_group.name, ad_group.status,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value,
        metrics.ctr, metrics.average_cpc
    FROM ad_group
    WHERE segments.date BETWEEN '{START}' AND '{END}'
    ORDER BY metrics.cost_micros DESC
    LIMIT 15
""")

print("\n" + "="*70)
print("AD GROUPS — TOP 15 POR CUSTO")
print("="*70)
print(f"{'Campanha / Ad Group':<60} {'Custo':>9} {'Conv':>6} {'ROAS':>6}")
print("-"*80)
for r in rows:
    cost = brl(r.metrics.cost_micros)
    val  = round(r.metrics.conversions_value, 2)
    conv = round(r.metrics.conversions, 2)
    roas = round(val / cost, 2) if cost > 0 else 0
    label = f"{r.campaign.name[:25]} / {r.ad_group.name}"[:59]
    print(f"{label:<60} R${cost:>8.2f} {conv:>6.1f} {roas:>5.2f}x")


# ── Keywords top ──────────────────────────────────────────────
rows = q(f"""
    SELECT
        campaign.name, ad_group.name,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.status,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value,
        metrics.ctr, metrics.average_cpc
    FROM keyword_view
    WHERE segments.date BETWEEN '{START}' AND '{END}'
        AND ad_group_criterion.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
    LIMIT 20
""")

print("\n" + "="*70)
print("KEYWORDS — TOP 20 POR CUSTO")
print("="*70)
print(f"{'Keyword':<40} {'Match':<8} {'Custo':>9} {'CPC':>7} {'Conv':>6} {'ROAS':>6}")
print("-"*80)
for r in rows:
    cost = brl(r.metrics.cost_micros)
    val  = round(r.metrics.conversions_value, 2)
    conv = round(r.metrics.conversions, 2)
    roas = round(val / cost, 2) if cost > 0 else 0
    cpc  = brl(r.metrics.average_cpc)
    kw   = r.ad_group_criterion.keyword.text[:39]
    mt   = r.ad_group_criterion.keyword.match_type.name[:7]
    print(f"{kw:<40} {mt:<8} R${cost:>8.2f} R${cpc:>6.2f} {conv:>6.1f} {roas:>5.2f}x")


# ── Search Terms (top 15 por custo) ───────────────────────────
rows = q(f"""
    SELECT
        campaign.name,
        search_term_view.search_term,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value
    FROM search_term_view
    WHERE segments.date BETWEEN '{START}' AND '{END}'
    ORDER BY metrics.cost_micros DESC
    LIMIT 15
""")

print("\n" + "="*70)
print("SEARCH TERMS — TOP 15 POR CUSTO")
print("="*70)
print(f"{'Termo':<45} {'Campanha':<22} {'Custo':>9} {'Conv':>6}")
print("-"*85)
for r in rows:
    cost = brl(r.metrics.cost_micros)
    conv = round(r.metrics.conversions, 2)
    print(f"{r.search_term_view.search_term[:44]:<45} {r.campaign.name[:21]:<22} R${cost:>8.2f} {conv:>6.1f}")

print("\n✅ Análise concluída.")
