from core.client import get_client, CUSTOMER_ID
from google.protobuf import field_mask_pb2


def update_campaign_budget(budget_resource_name: str, new_amount_brl: float, dry_run: bool = True) -> dict:
    """Update a campaign budget amount."""
    if new_amount_brl < 1.0:
        return {"status": "error", "reason": "Budget mínimo R$1,00"}

    if dry_run:
        return {
            "status": "dry_run",
            "budget_rn": budget_resource_name,
            "new_amount_brl": new_amount_brl,
            "action": "would_update_budget",
        }

    client = get_client()
    budget_service = client.get_service("CampaignBudgetService")

    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = budget_resource_name
    op.update.amount_micros = int(new_amount_brl * 1_000_000)
    client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["amount_micros"]))

    response = budget_service.mutate_campaign_budgets(
        customer_id=CUSTOMER_ID,
        operations=[op],
    )
    return {
        "status": "updated",
        "budget_rn": response.results[0].resource_name,
        "new_amount_brl": new_amount_brl,
    }


def set_campaign_status(campaign_id: int, status: str, dry_run: bool = True) -> dict:
    """Enable or pause a campaign. status: 'ENABLED' or 'PAUSED'."""
    if status not in ("ENABLED", "PAUSED"):
        return {"status": "error", "reason": "status deve ser ENABLED ou PAUSED"}

    resource_name = f"customers/{CUSTOMER_ID}/campaigns/{campaign_id}"

    if dry_run:
        return {
            "status": "dry_run",
            "campaign_id": campaign_id,
            "new_status": status,
            "action": f"would_set_{status.lower()}",
        }

    client = get_client()
    campaign_service = client.get_service("CampaignService")

    op = client.get_type("CampaignOperation")
    op.update.resource_name = resource_name
    op.update.status = client.enums.CampaignStatusEnum[status]
    client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["status"]))

    response = campaign_service.mutate_campaigns(
        customer_id=CUSTOMER_ID,
        operations=[op],
    )
    return {
        "status": "done",
        "campaign_id": campaign_id,
        "new_status": status,
        "resource_name": response.results[0].resource_name,
    }


_DONE_VERB = {"PAUSED": "paused", "ENABLED": "enabled"}


def _set_keyword_status(keyword_text: str, campaign_id: int, target_status: str, dry_run: bool = True):
    """Set status (ENABLED/PAUSED) for all criteria matching keyword_text in a campaign.
    Matches every match type of that exact text in the campaign. Returns a dict (single match)
    or list of dicts (multiple matches)."""
    if target_status not in ("ENABLED", "PAUSED"):
        return {"status": "error", "reason": "target_status deve ser ENABLED ou PAUSED"}

    client = get_client()
    service = client.get_service("GoogleAdsService")
    gaql = f"""
        SELECT
            ad_group_criterion.resource_name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            ad_group.name
        FROM keyword_view
        WHERE campaign.id = {campaign_id}
            AND ad_group_criterion.keyword.text = '{keyword_text}'
            AND ad_group_criterion.status != 'REMOVED'
    """
    rows = list(service.search(customer_id=CUSTOMER_ID, query=gaql))
    if not rows:
        return {"status": "not_found", "keyword": keyword_text}

    ag_criterion_service = client.get_service("AdGroupCriterionService")
    results = []
    for row in rows:
        resource_name = row.ad_group_criterion.resource_name
        current_status = row.ad_group_criterion.status.name
        ad_group = row.ad_group.name
        match_type = row.ad_group_criterion.keyword.match_type.name

        if current_status == target_status:
            results.append({
                "status": f"already_{target_status.lower()}",
                "keyword": keyword_text, "match_type": match_type, "ad_group": ad_group,
            })
            continue

        if dry_run:
            results.append({
                "status": "dry_run", "keyword": keyword_text, "match_type": match_type,
                "ad_group": ad_group, "from": current_status,
                "action": f"would_set_{target_status.lower()}",
            })
            continue

        criterion = client.get_type("AdGroupCriterion")
        criterion.resource_name = resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum[target_status]
        op = client.get_type("AdGroupCriterionOperation")
        client.copy_from(op.update, criterion)
        client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["status"]))
        response = ag_criterion_service.mutate_ad_group_criteria(
            customer_id=CUSTOMER_ID, operations=[op],
        )
        results.append({
            "status": _DONE_VERB[target_status],
            "keyword": keyword_text, "match_type": match_type, "ad_group": ad_group,
            "from": current_status, "resource_name": response.results[0].resource_name,
        })

    return results[0] if len(results) == 1 else results


def pause_keyword(keyword_text: str, campaign_id: int, dry_run: bool = True):
    """Pause all criteria matching keyword_text in a campaign."""
    return _set_keyword_status(keyword_text, campaign_id, "PAUSED", dry_run=dry_run)


def enable_keyword(keyword_text: str, campaign_id: int, dry_run: bool = True):
    """Enable all criteria matching keyword_text in a campaign."""
    return _set_keyword_status(keyword_text, campaign_id, "ENABLED", dry_run=dry_run)


def pause_keywords_bulk(keyword_list: list[dict], dry_run: bool = True) -> list[dict]:
    """Pause multiple keywords. keyword_list: [{'text': ..., 'campaign_id': ...}]"""
    return [pause_keyword(kw["text"], kw["campaign_id"], dry_run=dry_run) for kw in keyword_list]


def enable_keywords_bulk(keyword_list: list[dict], dry_run: bool = True) -> list[dict]:
    """Enable multiple keywords. keyword_list: [{'text': ..., 'campaign_id': ...}]"""
    return [enable_keyword(kw["text"], kw["campaign_id"], dry_run=dry_run) for kw in keyword_list]


def set_ad_group_status(ad_group_id: int, status: str, dry_run: bool = True) -> dict:
    """Enable or pause an ad group. status: 'ENABLED' or 'PAUSED'."""
    if status not in ("ENABLED", "PAUSED"):
        return {"status": "error", "reason": "status deve ser ENABLED ou PAUSED"}

    resource_name = f"customers/{CUSTOMER_ID}/adGroups/{ad_group_id}"

    if dry_run:
        return {
            "status": "dry_run",
            "ad_group_id": ad_group_id,
            "new_status": status,
            "action": f"would_set_{status.lower()}",
        }

    client = get_client()
    ad_group_service = client.get_service("AdGroupService")

    op = client.get_type("AdGroupOperation")
    op.update.resource_name = resource_name
    op.update.status = client.enums.AdGroupStatusEnum[status]
    client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["status"]))

    response = ad_group_service.mutate_ad_groups(
        customer_id=CUSTOMER_ID,
        operations=[op],
    )
    return {
        "status": "done",
        "ad_group_id": ad_group_id,
        "new_status": status,
        "resource_name": response.results[0].resource_name,
    }


def add_negative_keywords(campaign_id: int, keywords: list[str], dry_run: bool = True) -> list[dict]:
    """Add negative keywords (PHRASE match) at campaign level."""
    if dry_run:
        return [{"status": "dry_run", "keyword": kw, "action": "would_add_negative"} for kw in keywords]

    client = get_client()
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    operations = []

    for kw in keywords:
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = f"customers/{CUSTOMER_ID}/campaigns/{campaign_id}"
        criterion.negative = True
        criterion.keyword.text = kw
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        operations.append(op)

    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=CUSTOMER_ID,
        operations=operations,
    )
    return [
        {"status": "added", "keyword": kw, "resource_name": r.resource_name}
        for kw, r in zip(keywords, response.results)
    ]


def upload_image_asset(image_path: str, asset_name: str, dry_run: bool = True) -> dict:
    """Upload an image file as an asset. Returns asset resource name."""
    import os
    if not os.path.exists(image_path):
        return {"status": "error", "reason": f"File not found: {image_path}"}

    if dry_run:
        return {"status": "dry_run", "image_path": image_path, "asset_name": asset_name, "action": "would_upload"}

    client = get_client()
    asset_service = client.get_service("AssetService")

    with open(image_path, "rb") as f:
        image_data = f.read()

    op = client.get_type("AssetOperation")
    asset = op.create
    asset.name = asset_name
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    asset.image_asset.data = image_data

    response = asset_service.mutate_assets(
        customer_id=CUSTOMER_ID,
        operations=[op],
    )
    return {
        "status": "uploaded",
        "asset_name": asset_name,
        "resource_name": response.results[0].resource_name,
    }


def link_asset_to_pmax_group(
    asset_resource_name: str,
    asset_group_id: int,
    field_type: str,
    dry_run: bool = True,
) -> dict:
    """Link an uploaded asset to a PMAX asset group.
    field_type: LOGO, LANDSCAPE_LOGO, MARKETING_IMAGE, SQUARE_MARKETING_IMAGE, PORTRAIT_MARKETING_IMAGE
    """
    asset_group_rn = f"customers/{CUSTOMER_ID}/assetGroups/{asset_group_id}"

    if dry_run:
        return {
            "status": "dry_run",
            "asset": asset_resource_name,
            "asset_group_id": asset_group_id,
            "field_type": field_type,
            "action": "would_link",
        }

    client = get_client()
    asset_group_asset_service = client.get_service("AssetGroupAssetService")

    op = client.get_type("AssetGroupAssetOperation")
    aga = op.create
    aga.asset = asset_resource_name
    aga.asset_group = asset_group_rn
    aga.field_type = client.enums.AssetFieldTypeEnum[field_type]

    response = asset_group_asset_service.mutate_asset_group_assets(
        customer_id=CUSTOMER_ID,
        operations=[op],
    )
    return {
        "status": "linked",
        "field_type": field_type,
        "resource_name": response.results[0].resource_name,
    }


def remove_asset_group_assets(resource_names: list[str], dry_run: bool = True) -> list[dict]:
    """Remove asset-group-asset links by resource name."""
    if dry_run:
        return [{"status": "dry_run", "rn": rn, "action": "would_remove"} for rn in resource_names]

    client = get_client()
    service = client.get_service("AssetGroupAssetService")
    ops = []
    for rn in resource_names:
        op = client.get_type("AssetGroupAssetOperation")
        op.remove = rn
        ops.append(op)

    response = service.mutate_asset_group_assets(customer_id=CUSTOMER_ID, operations=ops)
    return [{"status": "removed", "rn": r.resource_name} for r in response.results]


def link_asset_to_campaign(
    asset_resource_name: str,
    campaign_id: int,
    field_type: str,
    dry_run: bool = True,
) -> dict:
    """Link an asset at campaign level (required for LOGO/LANDSCAPE_LOGO when Brand Guidelines is enabled).
    field_type: LOGO, LANDSCAPE_LOGO, BUSINESS_NAME
    """
    campaign_rn = f"customers/{CUSTOMER_ID}/campaigns/{campaign_id}"

    if dry_run:
        return {
            "status": "dry_run",
            "asset": asset_resource_name,
            "campaign_id": campaign_id,
            "field_type": field_type,
            "action": "would_link_at_campaign",
        }

    client = get_client()
    campaign_asset_service = client.get_service("CampaignAssetService")

    op = client.get_type("CampaignAssetOperation")
    ca = op.create
    ca.asset = asset_resource_name
    ca.campaign = campaign_rn
    ca.field_type = client.enums.AssetFieldTypeEnum[field_type]

    response = campaign_asset_service.mutate_campaign_assets(
        customer_id=CUSTOMER_ID,
        operations=[op],
    )
    return {
        "status": "linked_at_campaign",
        "field_type": field_type,
        "resource_name": response.results[0].resource_name,
    }


def update_keyword_bid(keyword_text: str, campaign_id: int, new_bid_brl: float, dry_run: bool = True) -> dict:
    """Update CPC bid for a keyword. Safety: min R$0.30, max change ±50%."""
    MIN_BID = 0.30
    new_bid_brl = max(new_bid_brl, MIN_BID)

    client = get_client()
    service = client.get_service("GoogleAdsService")

    gaql = f"""
        SELECT
            ad_group_criterion.resource_name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.status,
            ad_group_criterion.cpc_bid_micros,
            ad_group.name
        FROM keyword_view
        WHERE campaign.id = {campaign_id}
            AND ad_group_criterion.keyword.text = '{keyword_text}'
            AND ad_group_criterion.status = 'ENABLED'
    """
    rows = list(service.search(customer_id=CUSTOMER_ID, query=gaql))

    if not rows:
        return {"status": "not_found", "keyword": keyword_text}

    row = rows[0]
    resource_name = row.ad_group_criterion.resource_name
    current_bid = row.ad_group_criterion.cpc_bid_micros / 1_000_000
    ad_group = row.ad_group.name

    # Safety cap: max ±50% change per execution
    max_bid = current_bid * 1.50
    min_bid = max(current_bid * 0.50, MIN_BID)
    new_bid_brl = max(min(new_bid_brl, max_bid), min_bid)

    if dry_run:
        return {
            "status": "dry_run",
            "keyword": keyword_text,
            "ad_group": ad_group,
            "current_bid_brl": round(current_bid, 2),
            "new_bid_brl": round(new_bid_brl, 2),
            "change_pct": round((new_bid_brl / current_bid - 1) * 100, 1),
        }

    ag_criterion_service = client.get_service("AdGroupCriterionService")
    criterion = client.get_type("AdGroupCriterion")
    criterion.resource_name = resource_name
    criterion.cpc_bid_micros = int(new_bid_brl * 1_000_000)

    from google.protobuf import field_mask_pb2
    op = client.get_type("AdGroupCriterionOperation")
    client.copy_from(op.update, criterion)
    client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["cpc_bid_micros"]))

    ag_criterion_service.mutate_ad_group_criteria(
        customer_id=CUSTOMER_ID,
        operations=[op],
    )
    return {
        "status": "updated",
        "keyword": keyword_text,
        "ad_group": ad_group,
        "old_bid_brl": round(current_bid, 2),
        "new_bid_brl": round(new_bid_brl, 2),
        "change_pct": round((new_bid_brl / current_bid - 1) * 100, 1),
    }


def update_asset_final_urls(asset_id: int, final_urls: list[str], dry_run: bool = True) -> dict:
    """Update the final_urls of an asset (e.g. a disapproved sitelink pointing to a 404).
    Replaces the URL list and triggers a re-review by Google. The asset stays linked to
    whatever campaigns/ad groups already reference it."""
    if not final_urls:
        return {"status": "error", "reason": "final_urls vazio"}

    resource_name = f"customers/{CUSTOMER_ID}/assets/{asset_id}"
    if dry_run:
        return {
            "status": "dry_run", "asset_id": asset_id,
            "new_final_urls": final_urls, "action": "would_update_final_urls",
        }

    client = get_client()
    asset_service = client.get_service("AssetService")

    op = client.get_type("AssetOperation")
    op.update.resource_name = resource_name
    op.update.final_urls.extend(final_urls)
    client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["final_urls"]))

    response = asset_service.mutate_assets(
        customer_id=CUSTOMER_ID,
        operations=[op],
    )
    return {
        "status": "updated", "asset_id": asset_id, "new_final_urls": final_urls,
        "resource_name": response.results[0].resource_name,
    }
