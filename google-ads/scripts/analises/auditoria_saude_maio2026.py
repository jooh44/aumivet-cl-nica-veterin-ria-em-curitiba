#!/usr/bin/env python3
"""
Auditoria de Saúde Completa — RZ VET — Maio 2026
Levanta: limitações de política, assets faltando, ad strength, aprovações.
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.client import get_client, CUSTOMER_ID

client = get_client()
service = client.get_service("GoogleAdsService")


def query(gaql):
    try:
        return list(service.search(customer_id=CUSTOMER_ID, query=gaql))
    except Exception as e:
        print(f"   [ERRO] Query falhou: {e}")
        return []


def money(micros):
    return round(micros / 1_000_000, 2)


# ══════════════════════════════════════════════════════════════
# 1. CAMPANHAS — status, saúde, razões de limitação
# ══════════════════════════════════════════════════════════════
print("\n>>> 1. Campanhas + Saúde + Razões...")
rows = query("""
    SELECT
        campaign.id,
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
    WHERE campaign.status != 'REMOVED'
    ORDER BY campaign.name
""")
campaigns = []
for r in rows:
    cost = money(r.metrics.cost_micros)
    val = round(r.metrics.conversions_value, 2)
    reasons = [x.name for x in r.campaign.primary_status_reasons]
    campaigns.append({
        "id": r.campaign.id,
        "name": r.campaign.name,
        "status": r.campaign.status.name,
        "primary_status": r.campaign.primary_status.name,
        "reasons": reasons,
        "channel": r.campaign.advertising_channel_type.name,
        "budget_brl": money(r.campaign_budget.amount_micros),
        "impressions": r.metrics.impressions,
        "clicks": r.metrics.clicks,
        "cost_brl": cost,
        "conversions": round(r.metrics.conversions, 2),
        "conv_value_brl": val,
        "roas": round(val / cost, 2) if cost > 0 else 0,
    })
print(f"   {len(campaigns)} campanhas")


# ══════════════════════════════════════════════════════════════
# 2. ADS REPROVADOS — política, termos médicos/vet
# ══════════════════════════════════════════════════════════════
print("\n>>> 2. Ads Reprovados por Política...")
rows = query("""
    SELECT
        campaign.name,
        ad_group.name,
        ad_group_ad.ad.id,
        ad_group_ad.ad.type,
        ad_group_ad.status,
        ad_group_ad.policy_summary.approval_status,
        ad_group_ad.policy_summary.policy_topic_entries
    FROM ad_group_ad
    WHERE ad_group_ad.status != 'REMOVED'
      AND ad_group_ad.policy_summary.approval_status != 'APPROVED'
    ORDER BY campaign.name
""")
disapproved_ads = []
for r in rows:
    topics = []
    for entry in r.ad_group_ad.policy_summary.policy_topic_entries:
        topic = {
            "topic": entry.topic,
            "type": entry.type_.name if hasattr(entry.type_, 'name') else str(entry.type_),
        }
        evidences = []
        for ev in entry.evidences:
            ev_data = {}
            if ev.text_list and ev.text_list.texts:
                ev_data["texts"] = list(ev.text_list.texts)
            if ev_data:
                evidences.append(ev_data)
        if evidences:
            topic["evidences"] = evidences
        topics.append(topic)

    disapproved_ads.append({
        "campaign": r.campaign.name,
        "ad_group": r.ad_group.name,
        "ad_id": r.ad_group_ad.ad.id,
        "ad_type": r.ad_group_ad.ad.type_.name,
        "ad_status": r.ad_group_ad.status.name,
        "approval_status": r.ad_group_ad.policy_summary.approval_status.name,
        "policy_topics": topics,
    })
print(f"   {len(disapproved_ads)} ads com restrição de política")


# ══════════════════════════════════════════════════════════════
# 3. TODOS OS ADS APROVADOS — ad strength (RSA Search)
# ══════════════════════════════════════════════════════════════
print("\n>>> 3. Todos os Ads Ativos + Ad Strength...")
rows = query("""
    SELECT
        campaign.name,
        campaign.advertising_channel_type,
        ad_group.name,
        ad_group_ad.ad.id,
        ad_group_ad.ad.type,
        ad_group_ad.status,
        ad_group_ad.policy_summary.approval_status,
        ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions,
        ad_group_ad.ad_strength,
        ad_group_ad.action_items
    FROM ad_group_ad
    WHERE ad_group_ad.status != 'REMOVED'
    ORDER BY campaign.name, ad_group.name
""")
all_ads = []
for r in rows:
    ad_type = r.ad_group_ad.ad.type_.name
    headlines = []
    descriptions = []
    if ad_type == "RESPONSIVE_SEARCH_AD":
        for h in r.ad_group_ad.ad.responsive_search_ad.headlines:
            headlines.append({
                "text": h.text,
                "pinned": h.pinned_field.name if h.pinned_field else None,
            })
        for d in r.ad_group_ad.ad.responsive_search_ad.descriptions:
            descriptions.append({
                "text": d.text,
                "pinned": d.pinned_field.name if d.pinned_field else None,
            })

    action_items = list(r.ad_group_ad.action_items) if r.ad_group_ad.action_items else []

    all_ads.append({
        "campaign": r.campaign.name,
        "channel": r.campaign.advertising_channel_type.name,
        "ad_group": r.ad_group.name,
        "ad_id": r.ad_group_ad.ad.id,
        "ad_type": ad_type,
        "status": r.ad_group_ad.status.name,
        "approval_status": r.ad_group_ad.policy_summary.approval_status.name,
        "ad_strength": r.ad_group_ad.ad_strength.name if r.ad_group_ad.ad_strength else None,
        "action_items": action_items,
        "headline_count": len(headlines),
        "description_count": len(descriptions),
        "headlines": headlines,
        "descriptions": descriptions,
    })
print(f"   {len(all_ads)} ads ativos")


# ══════════════════════════════════════════════════════════════
# 4. KEYWORDS COM PROBLEMAS DE POLÍTICA
# ══════════════════════════════════════════════════════════════
print("\n>>> 4. Keywords com Restrição de Política...")
rows = query("""
    SELECT
        campaign.name,
        ad_group.name,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.status,
        ad_group_criterion.approval_status,
        ad_group_criterion.policy_summary.policy_topic_entries
    FROM ad_group_criterion
    WHERE ad_group_criterion.type = 'KEYWORD'
      AND ad_group_criterion.status != 'REMOVED'
      AND ad_group_criterion.approval_status != 'APPROVED'
    ORDER BY campaign.name
""")
policy_keywords = []
for r in rows:
    topics = []
    for entry in r.ad_group_criterion.policy_summary.policy_topic_entries:
        topics.append({
            "topic": entry.topic,
            "type": entry.type_.name if hasattr(entry.type_, 'name') else str(entry.type_),
        })
    policy_keywords.append({
        "campaign": r.campaign.name,
        "ad_group": r.ad_group.name,
        "keyword": r.ad_group_criterion.keyword.text,
        "match_type": r.ad_group_criterion.keyword.match_type.name,
        "status": r.ad_group_criterion.status.name,
        "approval_status": r.ad_group_criterion.approval_status.name,
        "policy_topics": topics,
    })
print(f"   {len(policy_keywords)} keywords com restrição")


# ══════════════════════════════════════════════════════════════
# 5. PMAX ASSET GROUPS — inventário completo de assets
# ══════════════════════════════════════════════════════════════
print("\n>>> 5. PMax Asset Groups + Inventário de Assets...")
rows = query("""
    SELECT
        campaign.name,
        asset_group.id,
        asset_group.name,
        asset_group.status,
        asset_group.primary_status,
        asset_group.primary_status_reasons,
        asset_group.ad_strength
    FROM asset_group
    WHERE campaign.status != 'REMOVED'
    ORDER BY campaign.name, asset_group.name
""")
asset_groups = []
for r in rows:
    reasons = [x.name for x in r.asset_group.primary_status_reasons]
    asset_groups.append({
        "campaign": r.campaign.name,
        "id": r.asset_group.id,
        "name": r.asset_group.name,
        "status": r.asset_group.status.name,
        "primary_status": r.asset_group.primary_status.name,
        "reasons": reasons,
        "ad_strength": r.asset_group.ad_strength.name if r.asset_group.ad_strength else None,
        "assets": {},  # preenchido abaixo
    })
print(f"   {len(asset_groups)} asset groups")

# Assets por grupo
print("   Carregando assets de cada grupo...")
rows = query("""
    SELECT
        campaign.name,
        asset_group.id,
        asset_group.name,
        asset_group_asset.field_type,
        asset_group_asset.status,
        asset.id,
        asset.name,
        asset.type,
        asset.text_asset.text,
        asset.image_asset.full_size.url,
        asset.image_asset.full_size.width_pixels,
        asset.image_asset.full_size.height_pixels,
        asset.youtube_video_asset.youtube_video_id,
        asset.youtube_video_asset.youtube_video_title
    FROM asset_group_asset
    WHERE campaign.status != 'REMOVED'
    ORDER BY campaign.name, asset_group.name, asset_group_asset.field_type
""")

# Indexar por asset_group.id
ag_index = {ag["id"]: ag for ag in asset_groups}
for r in rows:
    ag_id = r.asset_group.id
    if ag_id not in ag_index:
        continue
    ag = ag_index[ag_id]
    field_type = r.asset_group_asset.field_type.name
    if field_type not in ag["assets"]:
        ag["assets"][field_type] = []

    asset_entry = {
        "id": r.asset.id,
        "name": r.asset.name,
        "type": r.asset.type_.name,
        "status": r.asset_group_asset.status.name,
    }
    if r.asset.text_asset.text:
        asset_entry["text"] = r.asset.text_asset.text
    if r.asset.image_asset.full_size.url:
        asset_entry["url"] = r.asset.image_asset.full_size.url
        asset_entry["width"] = r.asset.image_asset.full_size.width_pixels
        asset_entry["height"] = r.asset.image_asset.full_size.height_pixels
    if r.asset.youtube_video_asset.youtube_video_id:
        asset_entry["video_id"] = r.asset.youtube_video_asset.youtube_video_id
        asset_entry["video_title"] = r.asset.youtube_video_asset.youtube_video_title

    ag["assets"][field_type].append(asset_entry)

# Recontar por tipo
for ag in asset_groups:
    ag["asset_counts"] = {k: len(v) for k, v in ag["assets"].items()}

total_assets = sum(sum(ag["asset_counts"].values()) for ag in asset_groups)
print(f"   {total_assets} assets mapeados nos grupos")


# ══════════════════════════════════════════════════════════════
# 6. DISPLAY / DEMAND GEN — Responsive Display Assets
# ══════════════════════════════════════════════════════════════
print("\n>>> 6. Display / Demand Gen Ads — Assets...")
rows = query("""
    SELECT
        campaign.name,
        campaign.advertising_channel_type,
        ad_group.name,
        ad_group_ad.ad.id,
        ad_group_ad.ad.type,
        ad_group_ad.status,
        ad_group_ad.policy_summary.approval_status,
        ad_group_ad.ad_strength,
        ad_group_ad.ad.responsive_display_ad.headlines,
        ad_group_ad.ad.responsive_display_ad.long_headline,
        ad_group_ad.ad.responsive_display_ad.descriptions,
        ad_group_ad.ad.responsive_display_ad.business_name,
        ad_group_ad.ad.responsive_display_ad.marketing_images,
        ad_group_ad.ad.responsive_display_ad.square_marketing_images,
        ad_group_ad.ad.responsive_display_ad.logo_images,
        ad_group_ad.ad.responsive_display_ad.youtube_videos
    FROM ad_group_ad
    WHERE ad_group_ad.status != 'REMOVED'
      AND campaign.advertising_channel_type IN ('DISPLAY', 'DEMAND_GEN')
    ORDER BY campaign.name
""")
display_ads = []
for r in rows:
    ad = r.ad_group_ad.ad.responsive_display_ad
    display_ads.append({
        "campaign": r.campaign.name,
        "channel": r.campaign.advertising_channel_type.name,
        "ad_group": r.ad_group.name,
        "ad_id": r.ad_group_ad.ad.id,
        "ad_type": r.ad_group_ad.ad.type_.name,
        "status": r.ad_group_ad.status.name,
        "approval_status": r.ad_group_ad.policy_summary.approval_status.name,
        "ad_strength": r.ad_group_ad.ad_strength.name if r.ad_group_ad.ad_strength else None,
        "headline_count": len(ad.headlines),
        "headlines": [h.text for h in ad.headlines],
        "long_headline": ad.long_headline.text if ad.long_headline else None,
        "description_count": len(ad.descriptions),
        "descriptions": [d.text for d in ad.descriptions],
        "business_name": ad.business_name,
        "landscape_image_count": len(ad.marketing_images),
        "square_image_count": len(ad.square_marketing_images),
        "logo_count": len(ad.logo_images),
        "video_count": len(ad.youtube_videos),
    })
print(f"   {len(display_ads)} display/demand gen ads")


# ══════════════════════════════════════════════════════════════
# 7. SHOPPING — status do feed
# ══════════════════════════════════════════════════════════════
print("\n>>> 7. Shopping — Status de Produtos...")
try:
    rows = query("""
        SELECT
            campaign.name,
            segments.product_title,
            segments.product_item_id,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM shopping_performance_view
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """)
    shopping_products = []
    for r in rows:
        cost = money(r.metrics.cost_micros)
        val = round(r.metrics.conversions_value, 2)
        shopping_products.append({
            "campaign": r.campaign.name,
            "title": r.segments.product_title,
            "item_id": r.segments.product_item_id,
            "impressions": r.metrics.impressions,
            "clicks": r.metrics.clicks,
            "cost_brl": cost,
            "conversions": round(r.metrics.conversions, 2),
            "conv_value_brl": val,
            "roas": round(val / cost, 2) if cost > 0 else 0,
        })
    print(f"   {len(shopping_products)} produtos Shopping (top 50)")
except Exception as e:
    print(f"   Shopping não disponível: {e}")
    shopping_products = []


# ══════════════════════════════════════════════════════════════
# 8. RECOMENDAÇÕES DO GOOGLE ADS (Recommendations API)
# ══════════════════════════════════════════════════════════════
print("\n>>> 8. Recomendações do Google Ads...")
try:
    rows = query("""
        SELECT
            recommendation.type,
            recommendation.impact.base_metrics.cost_micros,
            recommendation.impact.potential_metrics.cost_micros,
            recommendation.campaign,
            recommendation.dismissed
        FROM recommendation
        WHERE recommendation.dismissed = FALSE
        ORDER BY recommendation.type
    """)
    recommendations = []
    for r in rows:
        recommendations.append({
            "type": r.recommendation.type_.name,
            "campaign": r.recommendation.campaign,
            "dismissed": r.recommendation.dismissed,
        })
    print(f"   {len(recommendations)} recomendações pendentes")
except Exception as e:
    print(f"   Recomendações: {e}")
    recommendations = []


# ══════════════════════════════════════════════════════════════
# ANÁLISE E DIAGNÓSTICO
# ══════════════════════════════════════════════════════════════
print("\n\n" + "="*70)
print("DIAGNÓSTICO — AUDITORIA DE SAÚDE RZVET")
print("="*70)

# --- Campanhas LIMITED ---
print("\n🔴 CAMPANHAS LIMITADAS (PRIMARY_STATUS = LIMITED):")
limited = [c for c in campaigns if c["primary_status"] == "LIMITED"]
if limited:
    for c in limited:
        print(f"   • {c['name']}")
        print(f"     Canal: {c['channel']} | Budget: R${c['budget_brl']:.2f}/dia")
        print(f"     Razões: {', '.join(c['reasons']) if c['reasons'] else 'não especificada'}")
else:
    print("   Nenhuma campanha LIMITED ✅")

# --- Campanhas ELIGIBLE ---
print("\n✅ CAMPANHAS SAUDÁVEIS (ELIGIBLE):")
eligible = [c for c in campaigns if c["primary_status"] == "ELIGIBLE"]
for c in eligible:
    print(f"   • {c['name']} ({c['channel']})")

# --- Campanhas PAUSED/OTHER ---
other = [c for c in campaigns if c["primary_status"] not in ("LIMITED", "ELIGIBLE")]
if other:
    print("\n⚪ OUTRAS CAMPANHAS:")
    for c in other:
        print(f"   • {c['name']} — {c['primary_status']} ({c['status']})")

# --- Ads reprovados ---
print(f"\n🚫 ADS COM RESTRIÇÃO DE POLÍTICA: {len(disapproved_ads)}")
if disapproved_ads:
    for ad in disapproved_ads:
        print(f"   • [{ad['campaign']}] {ad['ad_group']}")
        print(f"     Tipo: {ad['ad_type']} | Aprovação: {ad['approval_status']}")
        for t in ad["policy_topics"]:
            ev_str = ""
            if "evidences" in t:
                texts = []
                for ev in t["evidences"]:
                    texts.extend(ev.get("texts", []))
                if texts:
                    ev_str = f" → evidências: {', '.join(texts[:3])}"
            print(f"     Política: {t['topic']} ({t['type']}){ev_str}")

# --- Keywords com política ---
print(f"\n🔑 KEYWORDS COM RESTRIÇÃO: {len(policy_keywords)}")
if policy_keywords:
    for kw in policy_keywords:
        topics_str = ", ".join(t["topic"] for t in kw["policy_topics"])
        print(f"   • [{kw['campaign']}] \"{kw['keyword']}\" ({kw['match_type']})")
        print(f"     Status: {kw['approval_status']} | Políticas: {topics_str}")

# --- Ad Strength RSA ---
print("\n📊 AD STRENGTH — RSA (Search):")
rsa_ads = [a for a in all_ads if a["ad_type"] == "RESPONSIVE_SEARCH_AD"]
strength_counts = {}
for a in rsa_ads:
    s = a["ad_strength"] or "UNKNOWN"
    strength_counts[s] = strength_counts.get(s, 0) + 1

for s, c in sorted(strength_counts.items()):
    icon = {"EXCELLENT": "✅", "GOOD": "🟡", "AVERAGE": "🟠", "POOR": "🔴"}.get(s, "⚪")
    print(f"   {icon} {s}: {c} ad(s)")

# Detalhar ads não EXCELLENT
non_excellent = [a for a in rsa_ads if a["ad_strength"] not in ("EXCELLENT",)]
if non_excellent:
    print("\n   Ads que precisam de melhoria:")
    for a in non_excellent:
        print(f"   • [{a['campaign']}] {a['ad_group']}")
        print(f"     Ad Strength: {a['ad_strength']} | Headlines: {a['headline_count']}/15 | Desc: {a['description_count']}/4")
        if a["action_items"]:
            for item in a["action_items"]:
                print(f"     → Ação: {item}")

# --- PMax Asset Groups ---
print("\n🖼️  PMAX — ASSETS POR GRUPO:")
PMAX_REQUIREMENTS = {
    "HEADLINE": {"min": 3, "max": 5, "label": "Headlines (15-30 chars)"},
    "LONG_HEADLINE": {"min": 1, "max": 5, "label": "Long Headlines (≤90 chars)"},
    "DESCRIPTION": {"min": 2, "max": 5, "label": "Descriptions (≤90 chars)"},
    "MARKETING_IMAGE": {"min": 1, "max": 20, "label": "Imagens paisagem (1.91:1)"},
    "SQUARE_MARKETING_IMAGE": {"min": 1, "max": 20, "label": "Imagens quadradas (1:1)"},
    "PORTRAIT_MARKETING_IMAGE": {"min": 0, "max": 20, "label": "Imagens retrato (4:5) — recomendado"},
    "LOGO": {"min": 1, "max": 5, "label": "Logos (1:1)"},
    "LANDSCAPE_LOGO": {"min": 0, "max": 5, "label": "Logos paisagem (4:1) — recomendado"},
    "YOUTUBE_VIDEO": {"min": 0, "max": 5, "label": "Vídeos YouTube — recomendado"},
    "CALL_TO_ACTION_SELECTION": {"min": 0, "max": 1, "label": "Call to Action"},
    "BUSINESS_NAME": {"min": 1, "max": 1, "label": "Nome da empresa"},
}

for ag in asset_groups:
    counts = ag["asset_counts"]
    missing = []
    ok = []
    recommended = []

    for field, req in PMAX_REQUIREMENTS.items():
        n = counts.get(field, 0)
        label = req["label"]
        if req["min"] > 0 and n < req["min"]:
            missing.append(f"{label}: {n}/{req['min']} mínimo ❌")
        elif req["min"] == 0 and n == 0:
            recommended.append(f"{label}: 0 (recomendado adicionar) ⚠️")
        else:
            ok.append(f"{label}: {n} ✅")

    status_icon = "✅" if not missing else "❌"
    strength = ag.get("ad_strength", "?")
    strength_icon = {"EXCELLENT": "✅", "GOOD": "🟡", "AVERAGE": "🟠", "POOR": "🔴"}.get(strength, "⚪")

    print(f"\n   {status_icon} {ag['campaign']} → {ag['name']}")
    print(f"      Status: {ag['status']} | Saúde: {ag['primary_status']} | Ad Strength: {strength_icon} {strength}")

    if missing:
        print("      FALTANDO (obrigatório):")
        for m in missing:
            print(f"        🔴 {m}")
    if recommended:
        print("      RECOMENDADO (aumenta cobertura):")
        for rec in recommended:
            print(f"        🟡 {rec}")
    if ok:
        print("      OK:")
        for o in ok:
            print(f"        {o}")

# --- Display Ads ---
if display_ads:
    print("\n🖼️  DISPLAY / DEMAND GEN — ASSETS:")
    for ad in display_ads:
        issues = []
        if ad["headline_count"] < 5:
            issues.append(f"headlines: {ad['headline_count']}/5 (mínimo recomendado)")
        if ad["description_count"] < 5:
            issues.append(f"descrições: {ad['description_count']}/5")
        if ad["landscape_image_count"] < 1:
            issues.append("sem imagem paisagem (1.91:1) ❌")
        if ad["square_image_count"] < 1:
            issues.append("sem imagem quadrada (1:1) ❌")
        if ad["logo_count"] < 1:
            issues.append("sem logo ❌")
        if ad["video_count"] == 0:
            issues.append("sem vídeo (recomendado)")

        icon = "✅" if not issues else "⚠️"
        print(f"   {icon} [{ad['campaign']}] {ad['ad_group']} — {ad['ad_type']}")
        print(f"      Ad Strength: {ad['ad_strength']} | Aprovação: {ad['approval_status']}")
        if issues:
            for iss in issues:
                print(f"      🟡 {iss}")

# --- Recomendações ---
if recommendations:
    print("\n💡 RECOMENDAÇÕES DO GOOGLE ADS:")
    from collections import Counter
    rec_counts = Counter(r["type"] for r in recommendations)
    for rtype, count in rec_counts.most_common():
        print(f"   • {rtype}: {count}x")

# ══════════════════════════════════════════════════════════════
# PLANO DE AÇÃO — RESUMO
# ══════════════════════════════════════════════════════════════
print("\n\n" + "="*70)
print("PLANO DE AÇÃO — O QUE FAZER PARA FICAR REDONDO")
print("="*70)

action_plan = []

if limited:
    for c in limited:
        for reason in c["reasons"]:
            if "BUDGET" in reason:
                action_plan.append(f"[BUDGET] '{c['name']}': aumentar budget diário (LIMITED por orçamento)")
            elif "POLICY" in reason or "RESTRICTED" in reason:
                action_plan.append(f"[POLÍTICA] '{c['name']}': revisar termos médicos/vet nos anúncios")
            elif "LEARNING" in reason:
                action_plan.append(f"[APRENDIZADO] '{c['name']}': aguardar período de aprendizado (não alterar bids agora)")
            else:
                action_plan.append(f"[LIMITED] '{c['name']}': razão '{reason}' — investigar")

if disapproved_ads:
    action_plan.append(f"[ADS] {len(disapproved_ads)} anúncio(s) reprovado(s) — reescrever sem termos políticados")

if policy_keywords:
    action_plan.append(f"[KEYWORDS] {len(policy_keywords)} keyword(s) com restrição — pausar ou substituir")

for a in non_excellent:
    if a["ad_strength"] in ("POOR", "AVERAGE"):
        action_plan.append(
            f"[RSA] '{a['campaign']}' / '{a['ad_group']}': Ad Strength {a['ad_strength']} — "
            f"adicionar mais headlines ({a['headline_count']}/15) e descrições ({a['description_count']}/4)"
        )

for ag in asset_groups:
    counts = ag["asset_counts"]
    for field, req in PMAX_REQUIREMENTS.items():
        n = counts.get(field, 0)
        if req["min"] > 0 and n < req["min"]:
            action_plan.append(
                f"[PMAX] '{ag['name']}': adicionar {req['label']} (tem {n}, mínimo {req['min']})"
            )
    if counts.get("YOUTUBE_VIDEO", 0) == 0:
        action_plan.append(f"[PMAX] '{ag['name']}': adicionar ao menos 1 vídeo YouTube (melhora cobertura)")
    if counts.get("PORTRAIT_MARKETING_IMAGE", 0) == 0:
        action_plan.append(f"[PMAX] '{ag['name']}': adicionar imagem retrato 4:5 (Stories/Reels)")

if not action_plan:
    print("\n   Nenhuma ação crítica encontrada ✅")
else:
    for i, item in enumerate(action_plan, 1):
        print(f"\n   {i}. {item}")


# ══════════════════════════════════════════════════════════════
# SALVAR JSON
# ══════════════════════════════════════════════════════════════
output = {
    "period": "LAST_30_DAYS",
    "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
    "campaigns": campaigns,
    "disapproved_ads": disapproved_ads,
    "all_ads": all_ads,
    "policy_keywords": policy_keywords,
    "asset_groups": asset_groups,
    "display_ads": display_ads,
    "shopping_products": shopping_products,
    "recommendations": recommendations,
    "action_plan": action_plan,
}

out_path = os.path.join(
    os.path.dirname(__file__), '..', '..', 'memory', 'reports', 'auditoria_saude_maio2026.json'
)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n\n✅ JSON completo salvo em: {os.path.abspath(out_path)}")
print("="*70)
