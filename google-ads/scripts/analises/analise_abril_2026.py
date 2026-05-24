#!/usr/bin/env python3
"""Extração completa de dados de Abril 2026 — Google Ads + GA4"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.client import get_client, CUSTOMER_ID
from core.ga4 import run_ga4_report, PROPERTY_ID

client = get_client()
service = client.get_service("GoogleAdsService")

def query(gaql):
    return list(service.search(customer_id=CUSTOMER_ID, query=gaql))

def money(micros):
    return round(micros / 1_000_000, 2)

# ── 1. Campanhas Abril ──
print(">>> Campanhas...")
rows = query("""
    SELECT
        campaign.id, campaign.name, campaign.status,
        campaign.advertising_channel_type,
        campaign_budget.amount_micros,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value,
        metrics.all_conversions, metrics.all_conversions_value,
        metrics.ctr, metrics.average_cpc,
        metrics.search_impression_share,
        metrics.interactions
    FROM campaign
    WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
    ORDER BY metrics.cost_micros DESC
""")
campaigns = []
for r in rows:
    cost = money(r.metrics.cost_micros)
    val = round(r.metrics.conversions_value, 2)
    campaigns.append({
        "id": r.campaign.id,
        "name": r.campaign.name,
        "status": r.campaign.status.name,
        "channel": r.campaign.advertising_channel_type.name,
        "budget_brl": money(r.campaign_budget.amount_micros),
        "impressions": r.metrics.impressions,
        "clicks": r.metrics.clicks,
        "cost_brl": cost,
        "conversions": round(r.metrics.conversions, 2),
        "conv_value_brl": val,
        "all_conversions": round(r.metrics.all_conversions, 2),
        "all_conv_value_brl": round(r.metrics.all_conversions_value, 2),
        "roas": round(val / cost, 2) if cost > 0 else 0,
        "ctr": round(r.metrics.ctr * 100, 2),
        "avg_cpc_brl": money(r.metrics.average_cpc),
        "search_impression_share": round(r.metrics.search_impression_share, 4) if r.metrics.search_impression_share else None,
        "interactions": r.metrics.interactions,
    })
print(f"   {len(campaigns)} campanhas")

# ── 2. Campanhas por semana ──
print(">>> Campanhas por semana...")
rows = query("""
    SELECT
        campaign.name, segments.week,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value
    FROM campaign
    WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
        AND campaign.status = 'ENABLED'
    ORDER BY segments.week, campaign.name
""")
weekly = []
for r in rows:
    cost = money(r.metrics.cost_micros)
    val = round(r.metrics.conversions_value, 2)
    weekly.append({
        "campaign": r.campaign.name,
        "week": str(r.segments.week),
        "impressions": r.metrics.impressions,
        "clicks": r.metrics.clicks,
        "cost_brl": cost,
        "conversions": round(r.metrics.conversions, 2),
        "conv_value_brl": val,
        "roas": round(val / cost, 2) if cost > 0 else 0,
    })
print(f"   {len(weekly)} linhas semanais")

# ── 3. Ad Groups ──
print(">>> Ad Groups...")
rows = query("""
    SELECT
        campaign.name, ad_group.id, ad_group.name, ad_group.status,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value,
        metrics.ctr, metrics.average_cpc
    FROM ad_group
    WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
    ORDER BY metrics.cost_micros DESC
""")
ad_groups = []
for r in rows:
    cost = money(r.metrics.cost_micros)
    val = round(r.metrics.conversions_value, 2)
    ad_groups.append({
        "campaign": r.campaign.name,
        "id": r.ad_group.id,
        "name": r.ad_group.name,
        "status": r.ad_group.status.name,
        "impressions": r.metrics.impressions,
        "clicks": r.metrics.clicks,
        "cost_brl": cost,
        "conversions": round(r.metrics.conversions, 2),
        "conv_value_brl": val,
        "roas": round(val / cost, 2) if cost > 0 else 0,
        "ctr": round(r.metrics.ctr * 100, 2),
        "avg_cpc_brl": money(r.metrics.average_cpc),
    })
print(f"   {len(ad_groups)} ad groups")

# ── 4. Keywords ──
print(">>> Keywords...")
rows = query("""
    SELECT
        campaign.name, ad_group.name,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.status,
        ad_group_criterion.quality_info.quality_score,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value,
        metrics.ctr, metrics.average_cpc
    FROM keyword_view
    WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
        AND ad_group_criterion.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
    LIMIT 200
""")
keywords = []
for r in rows:
    cost = money(r.metrics.cost_micros)
    val = round(r.metrics.conversions_value, 2)
    qs = r.ad_group_criterion.quality_info.quality_score
    keywords.append({
        "campaign": r.campaign.name,
        "ad_group": r.ad_group.name,
        "keyword": r.ad_group_criterion.keyword.text,
        "match_type": r.ad_group_criterion.keyword.match_type.name,
        "status": r.ad_group_criterion.status.name,
        "quality_score": qs if qs > 0 else None,
        "impressions": r.metrics.impressions,
        "clicks": r.metrics.clicks,
        "cost_brl": cost,
        "conversions": round(r.metrics.conversions, 2),
        "conv_value_brl": val,
        "roas": round(val / cost, 2) if cost > 0 else 0,
        "ctr": round(r.metrics.ctr * 100, 2),
        "avg_cpc_brl": money(r.metrics.average_cpc),
    })
print(f"   {len(keywords)} keywords")

# ── 5. Search Terms (top 200) ──
print(">>> Search Terms...")
rows = query("""
    SELECT
        campaign.name, ad_group.name,
        search_term_view.search_term,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value
    FROM search_term_view
    WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
    ORDER BY metrics.cost_micros DESC
    LIMIT 200
""")
search_terms = []
for r in rows:
    cost = money(r.metrics.cost_micros)
    val = round(r.metrics.conversions_value, 2)
    search_terms.append({
        "campaign": r.campaign.name,
        "ad_group": r.ad_group.name,
        "term": r.search_term_view.search_term,
        "impressions": r.metrics.impressions,
        "clicks": r.metrics.clicks,
        "cost_brl": cost,
        "conversions": round(r.metrics.conversions, 2),
        "conv_value_brl": val,
        "roas": round(val / cost, 2) if cost > 0 else 0,
    })
print(f"   {len(search_terms)} search terms")

# ── 6. PMAX Asset Groups ──
print(">>> Asset Groups PMAX...")
rows = query("""
    SELECT
        campaign.name, asset_group.id, asset_group.name,
        asset_group.status, asset_group.primary_status,
        asset_group.primary_status_reasons,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value
    FROM asset_group
    WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
    ORDER BY metrics.cost_micros DESC
""")
asset_groups = []
for r in rows:
    cost = money(r.metrics.cost_micros)
    val = round(r.metrics.conversions_value, 2)
    asset_groups.append({
        "campaign": r.campaign.name,
        "id": r.asset_group.id,
        "name": r.asset_group.name,
        "status": r.asset_group.status.name,
        "primary_status": r.asset_group.primary_status.name,
        "reasons": [x.name for x in r.asset_group.primary_status_reasons],
        "impressions": r.metrics.impressions,
        "clicks": r.metrics.clicks,
        "cost_brl": cost,
        "conversions": round(r.metrics.conversions, 2),
        "conv_value_brl": val,
        "roas": round(val / cost, 2) if cost > 0 else 0,
    })
print(f"   {len(asset_groups)} asset groups")

# ── 7. Shopping Product Performance ──
print(">>> Shopping Products...")
try:
    rows = query("""
        SELECT
            campaign.name,
            segments.product_title,
            segments.product_item_id,
            segments.product_brand,
            segments.product_type_l1,
            metrics.impressions, metrics.clicks, metrics.cost_micros,
            metrics.conversions, metrics.conversions_value
        FROM shopping_performance_view
        WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
        ORDER BY metrics.cost_micros DESC
        LIMIT 100
    """)
    products = []
    for r in rows:
        cost = money(r.metrics.cost_micros)
        val = round(r.metrics.conversions_value, 2)
        products.append({
            "campaign": r.campaign.name,
            "title": r.segments.product_title,
            "item_id": r.segments.product_item_id,
            "brand": r.segments.product_brand,
            "type_l1": r.segments.product_type_l1,
            "impressions": r.metrics.impressions,
            "clicks": r.metrics.clicks,
            "cost_brl": cost,
            "conversions": round(r.metrics.conversions, 2),
            "conv_value_brl": val,
            "roas": round(val / cost, 2) if cost > 0 else 0,
        })
    print(f"   {len(products)} products")
except Exception as e:
    print(f"   Shopping query error: {e}")
    products = []

# ── 8. PMAX Asset Performance (para identificar imagens) ──
print(">>> Asset Performance PMAX...")
try:
    rows = query("""
        SELECT
            campaign.name,
            asset_group.name,
            asset_group_asset.field_type,
            asset_group_asset.status,
            asset.name,
            asset.type,
            asset.image_asset.full_size.url,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels
        FROM asset_group_asset
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
            AND asset.type = 'IMAGE'
    """)
    pmax_assets = []
    for r in rows:
        pmax_assets.append({
            "campaign": r.campaign.name,
            "asset_group": r.asset_group.name,
            "field_type": r.asset_group_asset.field_type.name,
            "status": r.asset_group_asset.status.name,
            "asset_name": r.asset.name,
            "url": r.asset.image_asset.full_size.url if r.asset.image_asset.full_size.url else None,
            "width": r.asset.image_asset.full_size.width_pixels,
            "height": r.asset.image_asset.full_size.height_pixels,
        })
    print(f"   {len(pmax_assets)} image assets")
except Exception as e:
    print(f"   Asset query error: {e}")
    pmax_assets = []

# ── 9. Conversion Actions Detail ──
print(">>> Conversion Actions...")
rows = query("""
    SELECT
        conversion_action.name,
        conversion_action.status,
        conversion_action.include_in_conversions_metric,
        conversion_action.primary_for_goal,
        conversion_action.type,
        conversion_action.category,
        metrics.all_conversions,
        metrics.all_conversions_value
    FROM conversion_action
    WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
    ORDER BY metrics.all_conversions DESC
""")
conv_actions = []
for r in rows:
    conv_actions.append({
        "name": r.conversion_action.name,
        "status": r.conversion_action.status.name,
        "include": bool(r.conversion_action.include_in_conversions_metric),
        "primary": bool(r.conversion_action.primary_for_goal),
        "type": r.conversion_action.type_.name,
        "category": r.conversion_action.category.name,
        "all_conversions": round(r.metrics.all_conversions, 2),
        "all_conv_value": round(r.metrics.all_conversions_value, 2),
    })
print(f"   {len(conv_actions)} conversion actions")

# ── 10. Campanhas diárias (para ver tendência) ──
print(">>> Tendência diária...")
rows = query("""
    SELECT
        segments.date,
        metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.conversions, metrics.conversions_value
    FROM campaign
    WHERE segments.date BETWEEN '2026-04-01' AND '2026-04-30'
        AND campaign.status = 'ENABLED'
    ORDER BY segments.date
""")
# Agregar por dia
daily_agg = {}
for r in rows:
    d = str(r.segments.date)
    if d not in daily_agg:
        daily_agg[d] = {"date": d, "impressions": 0, "clicks": 0, "cost_brl": 0, "conversions": 0, "conv_value_brl": 0}
    daily_agg[d]["impressions"] += r.metrics.impressions
    daily_agg[d]["clicks"] += r.metrics.clicks
    daily_agg[d]["cost_brl"] += money(r.metrics.cost_micros)
    daily_agg[d]["conversions"] += round(r.metrics.conversions, 2)
    daily_agg[d]["conv_value_brl"] += round(r.metrics.conversions_value, 2)
daily = sorted(daily_agg.values(), key=lambda x: x["date"])
for d in daily:
    d["cost_brl"] = round(d["cost_brl"], 2)
    d["conversions"] = round(d["conversions"], 2)
    d["conv_value_brl"] = round(d["conv_value_brl"], 2)
    d["roas"] = round(d["conv_value_brl"] / d["cost_brl"], 2) if d["cost_brl"] > 0 else 0
print(f"   {len(daily)} dias")

# ── 11. GA4 — Funil e-commerce ──
print(">>> GA4 Funil...")
try:
    from google.analytics.data_v1beta.types import FilterExpression, Filter

    # Sessões por canal
    ga4_channels = run_ga4_report(
        PROPERTY_ID,
        ["sessionDefaultChannelGroup"],
        ["sessions", "totalUsers", "ecommercePurchases", "purchaseRevenue", "addToCarts", "checkouts"],
        "2026-04-01", "2026-04-30"
    )
    ga4_channel_data = []
    for row in ga4_channels.rows:
        ga4_channel_data.append({
            "channel": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "users": int(row.metric_values[1].value),
            "purchases": int(row.metric_values[2].value),
            "revenue": float(row.metric_values[3].value),
            "add_to_carts": int(row.metric_values[4].value),
            "checkouts": int(row.metric_values[5].value),
        })
    print(f"   {len(ga4_channel_data)} canais GA4")

    # Sessões por source/medium com filtro google/cpc
    ga4_gads = run_ga4_report(
        PROPERTY_ID,
        ["sessionSourceMedium", "sessionCampaignName"],
        ["sessions", "totalUsers", "ecommercePurchases", "purchaseRevenue", "addToCarts", "checkouts",
         "engagedSessions", "bounceRate", "averageSessionDuration"],
        "2026-04-01", "2026-04-30",
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="sessionSourceMedium",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.CONTAINS,
                    value="google / cpc"
                )
            )
        )
    )
    ga4_gads_data = []
    for row in ga4_gads.rows:
        ga4_gads_data.append({
            "source_medium": row.dimension_values[0].value,
            "campaign": row.dimension_values[1].value,
            "sessions": int(row.metric_values[0].value),
            "users": int(row.metric_values[1].value),
            "purchases": int(row.metric_values[2].value),
            "revenue": float(row.metric_values[3].value),
            "add_to_carts": int(row.metric_values[4].value),
            "checkouts": int(row.metric_values[5].value),
            "engaged_sessions": int(row.metric_values[6].value),
            "bounce_rate": round(float(row.metric_values[7].value), 4),
            "avg_session_duration": round(float(row.metric_values[8].value), 1),
        })
    print(f"   {len(ga4_gads_data)} campanhas Google Ads no GA4")

    # GA4 diário — tráfego pago
    ga4_daily = run_ga4_report(
        PROPERTY_ID,
        ["date"],
        ["sessions", "ecommercePurchases", "purchaseRevenue", "addToCarts"],
        "2026-04-01", "2026-04-30",
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="sessionSourceMedium",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.CONTAINS,
                    value="google / cpc"
                )
            )
        )
    )
    ga4_daily_data = []
    for row in ga4_daily.rows:
        ga4_daily_data.append({
            "date": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "purchases": int(row.metric_values[1].value),
            "revenue": float(row.metric_values[2].value),
            "add_to_carts": int(row.metric_values[3].value),
        })
    ga4_daily_data.sort(key=lambda x: x["date"])
    print(f"   {len(ga4_daily_data)} dias GA4")

    # Landing pages do tráfego pago
    ga4_landing = run_ga4_report(
        PROPERTY_ID,
        ["landingPagePlusQueryString"],
        ["sessions", "ecommercePurchases", "purchaseRevenue", "bounceRate", "addToCarts"],
        "2026-04-01", "2026-04-30",
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="sessionSourceMedium",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.CONTAINS,
                    value="google / cpc"
                )
            )
        )
    )
    ga4_landing_data = []
    for row in ga4_landing.rows:
        ga4_landing_data.append({
            "landing_page": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "purchases": int(row.metric_values[1].value),
            "revenue": float(row.metric_values[2].value),
            "bounce_rate": round(float(row.metric_values[3].value), 4),
            "add_to_carts": int(row.metric_values[4].value),
        })
    ga4_landing_data.sort(key=lambda x: x["sessions"], reverse=True)
    print(f"   {len(ga4_landing_data)} landing pages")

    # Dispositivos
    ga4_devices = run_ga4_report(
        PROPERTY_ID,
        ["deviceCategory"],
        ["sessions", "ecommercePurchases", "purchaseRevenue", "bounceRate", "addToCarts"],
        "2026-04-01", "2026-04-30",
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="sessionSourceMedium",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.CONTAINS,
                    value="google / cpc"
                )
            )
        )
    )
    ga4_device_data = []
    for row in ga4_devices.rows:
        ga4_device_data.append({
            "device": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "purchases": int(row.metric_values[1].value),
            "revenue": float(row.metric_values[2].value),
            "bounce_rate": round(float(row.metric_values[3].value), 4),
            "add_to_carts": int(row.metric_values[4].value),
        })
    print(f"   {len(ga4_device_data)} dispositivos")

except Exception as e:
    print(f"   GA4 error: {e}")
    import traceback; traceback.print_exc()
    ga4_channel_data = []
    ga4_gads_data = []
    ga4_daily_data = []
    ga4_landing_data = []
    ga4_device_data = []

# ── SALVAR ──
output = {
    "period": "2026-04-01 to 2026-04-30",
    "campaigns": campaigns,
    "weekly": weekly,
    "daily": daily,
    "ad_groups": ad_groups,
    "keywords": keywords,
    "search_terms": search_terms,
    "asset_groups": asset_groups,
    "pmax_image_assets": pmax_assets,
    "products": products,
    "conversion_actions": conv_actions,
    "ga4": {
        "channels": ga4_channel_data,
        "google_ads_campaigns": ga4_gads_data,
        "daily_paid": ga4_daily_data,
        "landing_pages": ga4_landing_data,
        "devices": ga4_device_data,
    }
}

out_path = os.path.join(os.path.dirname(__file__), '..', '..', 'memory', 'reports', 'analise_abril_2026.json')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\n✅ Salvo em {out_path}")
