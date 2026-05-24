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

    csv_data_by_date = defaultdict(lambda: {'orders': 0, 'revenue': 0.0, 'cancelled_revenue': 0.0})
    
    for o in all_orders:
        if 'Google Ads' in o['utm']:
            if o['status'] == 'CANCELADO':
                csv_data_by_date[o['date']]['cancelled_revenue'] += o['total']
            else:
                csv_data_by_date[o['date']]['orders'] += 1
                csv_data_by_date[o['date']]['revenue'] += o['total']

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
              segments.conversion_action_name,
              metrics.conversions_by_conversion_date,
              metrics.conversions_value_by_conversion_date
            FROM customer
            WHERE segments.date >= '2026-04-01' AND segments.date <= '2026-04-22'
              AND segments.conversion_action_name = 'Compra Rzvet Tray'
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
        
        print(f"{'Data':<12} | {'Tray Pixel Ord':<14} | {'Tray Pixel (R$)':<15} | {'CSV Valid Ord':<13} | {'CSV Valid (R$)':<14} | {'CSV Cancelled (R$)'}")
        print("-" * 100)
        
        total_ads_conv = 0
        total_ads_val = 0
        total_csv_orders = 0
        total_csv_rev = 0
        total_csv_canc = 0
        
        for date in all_dates:
            ads_conv = ads_data_by_date[date]['conversions']
            ads_val = ads_data_by_date[date]['value']
            csv_g_ord = csv_data_by_date[date]['orders']
            csv_g_rev = csv_data_by_date[date]['revenue']
            csv_canc_rev = csv_data_by_date[date]['cancelled_revenue']
            
            total_ads_conv += ads_conv
            total_ads_val += ads_val
            total_csv_orders += csv_g_ord
            total_csv_rev += csv_g_rev
            total_csv_canc += csv_canc_rev
            
            print(f"{date:<12} | {ads_conv:<14.2f} | {ads_val:<15.2f} | {csv_g_ord:<13} | {csv_g_rev:<14.2f} | {csv_canc_rev:<14.2f}")

        print("-" * 100)
        print(f"{'TOTAL':<12} | {total_ads_conv:<14.2f} | {total_ads_val:<15.2f} | {total_csv_orders:<13} | {total_csv_rev:<14.2f} | {total_csv_canc:<14.2f}")

    except GoogleAdsException as ex:
        print(f"Request Error: {ex}")
        for error in ex.failure.errors:
            print(f"\tError with message: {error.message}.")

if __name__ == "__main__":
    main()
