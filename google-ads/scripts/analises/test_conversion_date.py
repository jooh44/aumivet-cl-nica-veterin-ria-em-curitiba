import os
from collections import defaultdict
from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env.ads"

credentials = {}
with open(ENV_PATH, "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            key, val = line.split("=", 1)
            if "#" in val:
                val = val.split("#")[0]
            credentials[key.strip()] = val.strip()

def main():
    googleads_config = {
        "developer_token": credentials["DEVELOPER_TOKEN"],
        "client_id": credentials["CLIENT_ID"],
        "client_secret": credentials["CLIENT_SECRET"],
        "refresh_token": credentials["REFRESH_TOKEN"],
        "use_proto_plus": True,
        "login_customer_id": credentials["MANAGER_CUSTOMER_ID"],
    }

    try:
        client = GoogleAdsClient.load_from_dict(googleads_config)
        googleads_service = client.get_service("GoogleAdsService")
        customer_id = credentials["CUSTOMER_ID"].replace("-", "")

        query = """
            SELECT
              segments.date,
              metrics.conversions_by_conversion_date,
              metrics.conversions_value_by_conversion_date
            FROM customer
            WHERE segments.date >= '2026-04-01' AND segments.date <= '2026-04-22'
        """

        stream = googleads_service.search_stream(
            customer_id=customer_id, query=query
        )

        ads_data_by_date = defaultdict(lambda: {'conversions': 0.0, 'value': 0.0})

        for batch in stream:
            for row in batch.results:
                date = row.segments.date
                ads_data_by_date[date]['conversions'] += row.metrics.conversions_by_conversion_date
                ads_data_by_date[date]['value'] += row.metrics.conversions_value_by_conversion_date

        for date in sorted(ads_data_by_date.keys()):
            print(f"{date}: {ads_data_by_date[date]['conversions']:.2f} conv, R$ {ads_data_by_date[date]['value']:.2f}")

    except GoogleAdsException as ex:
        print(f"Request Error: {ex}")
        for error in ex.failure.errors:
            print(f"\tError with message: {error.message}.")

if __name__ == "__main__":
    main()
