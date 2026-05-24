from core.client import get_client, CUSTOMER_ID


def _query(gaql: str, customer_id: str = CUSTOMER_ID) -> list[dict]:
    client = get_client()
    service = client.get_service("GoogleAdsService")
    rows = service.search(customer_id=customer_id, query=gaql)
    results = []
    for row in rows:
        results.append(row)
    return results


def get_campaigns(status_filter: str = None) -> list[dict]:
    where = ""
    if status_filter:
        where = f"WHERE campaign.status = '{status_filter}'"
    gaql = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign_budget.amount_micros
        FROM campaign
        {where}
        ORDER BY campaign.name
    """
    out = []
    for row in _query(gaql):
        out.append({
            "id": row.campaign.id,
            "name": row.campaign.name,
            "status": row.campaign.status.name,
            "channel": row.campaign.advertising_channel_type.name,
            "budget_brl": row.campaign_budget.amount_micros / 1_000_000,
        })
    return out


def get_campaign_performance(days: int = 30, status_filter: str = None) -> list[dict]:
    where = f"segments.date DURING LAST_{days}_DAYS"
    if status_filter:
        where += f" AND campaign.status = '{status_filter}'"
    gaql = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.ctr,
            metrics.average_cpc
        FROM campaign
        WHERE {where}
        ORDER BY metrics.cost_micros DESC
    """
    out = []
    for row in _query(gaql):
        cost = row.metrics.cost_micros / 1_000_000
        conversions = row.metrics.conversions
        conv_value = row.metrics.conversions_value
        out.append({
            "id": row.campaign.id,
            "name": row.campaign.name,
            "status": row.campaign.status.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost_brl": round(cost, 2),
            "conversions": round(conversions, 1),
            "conv_value_brl": round(conv_value, 2),
            "roas": round(conv_value / cost, 2) if cost > 0 else 0,
            "ctr": round(row.metrics.ctr * 100, 2),
            "avg_cpc_brl": round(row.metrics.average_cpc / 1_000_000, 2),
        })
    return out


def get_ad_groups(campaign_id: int) -> list[dict]:
    gaql = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.status,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM ad_group
        WHERE campaign.id = {campaign_id}
            AND segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC
    """
    out = []
    for row in _query(gaql):
        cost = row.metrics.cost_micros / 1_000_000
        conv_value = row.metrics.conversions_value
        out.append({
            "id": row.ad_group.id,
            "name": row.ad_group.name,
            "status": row.ad_group.status.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost_brl": round(cost, 2),
            "conversions": round(row.metrics.conversions, 1),
            "conv_value_brl": round(conv_value, 2),
            "roas": round(conv_value / cost, 2) if cost > 0 else 0,
        })
    return out


def get_keywords_performance(campaign_id: int = None, days: int = 30) -> list[dict]:
    where = f"segments.date DURING LAST_{days}_DAYS AND ad_group_criterion.status != 'REMOVED'"
    if campaign_id:
        where += f" AND campaign.id = {campaign_id}"
    gaql = f"""
        SELECT
            campaign.name,
            ad_group.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.average_cpc,
            metrics.ctr
        FROM keyword_view
        WHERE {where}
        ORDER BY metrics.cost_micros DESC
    """
    out = []
    for row in _query(gaql):
        cost = row.metrics.cost_micros / 1_000_000
        conv_value = row.metrics.conversions_value
        out.append({
            "campaign": row.campaign.name,
            "ad_group": row.ad_group.name,
            "keyword": row.ad_group_criterion.keyword.text,
            "match_type": row.ad_group_criterion.keyword.match_type.name,
            "status": row.ad_group_criterion.status.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost_brl": round(cost, 2),
            "conversions": round(row.metrics.conversions, 1),
            "conv_value_brl": round(conv_value, 2),
            "roas": round(conv_value / cost, 2) if cost > 0 else 0,
            "avg_cpc_brl": round(row.metrics.average_cpc / 1_000_000, 2),
            "ctr": round(row.metrics.ctr * 100, 2),
        })
    return out


def get_search_terms(campaign_id: int = None, days: int = 30) -> list[dict]:
    where = f"segments.date DURING LAST_{days}_DAYS"
    if campaign_id:
        where += f" AND campaign.id = {campaign_id}"
    gaql = f"""
        SELECT
            campaign.name,
            search_term_view.search_term,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM search_term_view
        WHERE {where}
        ORDER BY metrics.cost_micros DESC
        LIMIT 100
    """
    out = []
    for row in _query(gaql):
        cost = row.metrics.cost_micros / 1_000_000
        conv_value = row.metrics.conversions_value
        out.append({
            "campaign": row.campaign.name,
            "search_term": row.search_term_view.search_term,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost_brl": round(cost, 2),
            "conversions": round(row.metrics.conversions, 1),
            "conv_value_brl": round(conv_value, 2),
            "roas": round(conv_value / cost, 2) if cost > 0 else 0,
        })
    return out
