import os
from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Read .env.ads manually
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env.ads"

credentials = {}
with open(ENV_PATH, "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            key, val = line.split("=", 1)
            # Remove inline comments
            if "#" in val:
                val = val.split("#")[0]
            credentials[key.strip()] = val.strip().strip('"').strip("'")


def clean_customer_id(value: str) -> str:
    return value.replace("-", "").strip()

def main():
    googleads_config = {
        "developer_token": credentials["DEVELOPER_TOKEN"],
        "client_id": credentials["CLIENT_ID"],
        "client_secret": credentials["CLIENT_SECRET"],
        "refresh_token": credentials["REFRESH_TOKEN"],
        "use_proto_plus": True,
    }
    login_customer_id = clean_customer_id(credentials.get("LOGIN_CUSTOMER_ID", ""))
    if login_customer_id:
        googleads_config["login_customer_id"] = login_customer_id

    try:
        client = GoogleAdsClient.load_from_dict(googleads_config)
        googleads_service = client.get_service("GoogleAdsService")
        # In Google Ads API, customer IDs should be just numbers, no hyphens.
        customer_id = clean_customer_id(credentials["CUSTOMER_ID"])

        print(f"Buscando Campanhas para o Customer ID: {customer_id}...\n")

        query = """
            SELECT
              campaign.id,
              campaign.name,
              campaign.status
            FROM campaign
            ORDER BY campaign.id
        """

        stream = googleads_service.search_stream(
            customer_id=customer_id, query=query
        )

        for batch in stream:
            for row in batch.results:
                status_name = row.campaign.status.name
                print(f"Campanha: '{row.campaign.name}' (ID: {row.campaign.id}) | Status: {status_name}")

        print("\n✅ Conexão bem-sucedida!")

    except GoogleAdsException as ex:
        print(f"Request Error: {ex}")
        for error in ex.failure.errors:
            print(f"\tError with message: {error.message}.")

if __name__ == "__main__":
    main()
