import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.client import get_client, CUSTOMER_ID

client = get_client()
service = client.get_service("GoogleAdsService")

# Sitelinks nas Search ativas
rows = list(service.search(customer_id=CUSTOMER_ID, query="""
    SELECT
        campaign.id,
        campaign.name,
        campaign_asset.field_type,
        campaign_asset.status,
        asset.id,
        asset.sitelink_asset.link_text,
        asset.sitelink_asset.description1,
        asset.sitelink_asset.description2
    FROM campaign_asset
    WHERE campaign.id IN (23366014954, 23362032632, 23361821714)
      AND campaign_asset.field_type = 'SITELINK'
    ORDER BY campaign.name
"""))

print(f"Sitelinks em Search: {len(rows)}")
for r in rows:
    sl = r.asset.sitelink_asset
    print(f"  [{r.campaign.name}] id={r.asset.id} | {sl.link_text} | {sl.description1}")

# Sitelinks na PMax (para ver quais temos prontos e reaproveitar)
print()
rows3 = list(service.search(customer_id=CUSTOMER_ID, query="""
    SELECT
        campaign.name,
        campaign_asset.status,
        asset.id,
        asset.sitelink_asset.link_text,
        asset.sitelink_asset.description1,
        asset.sitelink_asset.description2
    FROM campaign_asset
    WHERE campaign.id = 21710109809
      AND campaign_asset.field_type = 'SITELINK'
"""))
print(f"Sitelinks PMax: {len(rows3)}")
for r in rows3:
    sl = r.asset.sitelink_asset
    print(f"  [{r.campaign_asset.status.name}] id={r.asset.id} | {sl.link_text} | {sl.description1} | {sl.description2}")
