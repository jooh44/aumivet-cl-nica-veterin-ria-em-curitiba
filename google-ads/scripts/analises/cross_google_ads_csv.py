import os
import csv
from collections import defaultdict
from datetime import datetime
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
    csv_path = "/home/johny/Downloads/pedidos_752744_17768748407109_91d27680.csv"
    
    # Store all orders
    all_orders = []
    
    with open(csv_path, newline='', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            date_str = row['Data'].strip()
            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y")
                iso_date = dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
            
            total_str = row['Total'].replace('.', '').replace(',', '.')
            total = float(total_str) if total_str else 0.0
            
            all_orders.append({
                'id': row['Pedido'],
                'date': iso_date,
                'total': total,
                'utm': row.get('UTM Source', '').strip(),
                'status': row['Status pedido'].strip().upper()
            })

    # Group by date for "Google Ads" tagged orders
    csv_data_by_date = defaultdict(lambda: {'orders': 0, 'revenue': 0.0, 'all_revenue': 0.0, 'all_orders': 0})
    
    for o in all_orders:
        if o['status'] != 'CANCELADO':
            csv_data_by_date[o['date']]['all_orders'] += 1
            csv_data_by_date[o['date']]['all_revenue'] += o['total']
            if 'Google Ads' in o['utm']:
                csv_data_by_date[o['date']]['orders'] += 1
                csv_data_by_date[o['date']]['revenue'] += o['total']

    # Google Ads Data
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

        all_dates = sorted(list(set(csv_data_by_date.keys()) | set(ads_data_by_date.keys())))
        
        print(f"{'Data':<12} | {'GAds Conv':<10} | {'GAds Val (R$)':<14} | {'CSV GAds Ord':<12} | {'CSV GAds (R$)':<14} | {'CSV All Ord':<12} | {'CSV All (R$)':<14}")
        print("-" * 100)
        
        for date in all_dates:
            ads_conv = ads_data_by_date[date]['conversions']
            ads_val = ads_data_by_date[date]['value']
            csv_g_ord = csv_data_by_date[date]['orders']
            csv_g_rev = csv_data_by_date[date]['revenue']
            csv_a_ord = csv_data_by_date[date]['all_orders']
            csv_a_rev = csv_data_by_date[date]['all_revenue']
            
            print(f"{date:<12} | {ads_conv:<10.2f} | {ads_val:<14.2f} | {csv_g_ord:<12} | {csv_g_rev:<14.2f} | {csv_a_ord:<12} | {csv_a_rev:<14.2f}")

    except GoogleAdsException as ex:
        print(f"Request Error: {ex}")
        for error in ex.failure.errors:
            print(f"\tError with message: {error.message}.")

if __name__ == "__main__":
    main()
