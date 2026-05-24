import csv
from datetime import datetime
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from core.reports import _query

CSV_FILE = PROJECT_ROOT / "data" / "imports" / "pedidos-mar-abr.csv"

def parse_csv(filepath):
    total_revenue_google = 0.0
    total_orders_google = 0
    min_date = None
    max_date = None
    
    with open(filepath, mode='r', encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if not row:
                continue
            
            date_str = row.get('Data', '').strip()
            utm_source = row.get('UTM Source', '').strip()
            total_str = row.get('Total', '0').strip()
            # Handle R$ or other currency formats if any, then float
            total_str = total_str.replace('R$', '').strip().replace('.', '').replace(',', '.')
            if not total_str:
                total_str = '0'
            
            if not date_str:
                continue
                
            dt = datetime.strptime(date_str, '%d/%m/%Y').date()
            if min_date is None or dt < min_date:
                min_date = dt
            if max_date is None or dt > max_date:
                max_date = dt
                
            if 'Google' in utm_source:
                total_revenue_google += float(total_str)
                total_orders_google += 1
                
    return min_date, max_date, total_orders_google, total_revenue_google

def main():
    min_date, max_date, csv_orders, csv_revenue = parse_csv(CSV_FILE)
    print(f"--- CSV DATA ({min_date} to {max_date}) ---")
    print(f"Pedidos Google Ads: {csv_orders}")
    print(f"Receita Google Ads: R$ {csv_revenue:,.2f}")
    
    print(f"\n--- GOOGLE ADS API DATA ({min_date} to {max_date}) ---")
    gaql = f"""
        SELECT
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{min_date}' AND '{max_date}'
    """
    rows = _query(gaql)
    api_orders = 0
    api_revenue = 0.0
    for row in rows:
        api_orders += row.metrics.conversions
        api_revenue += row.metrics.conversions_value
        
    print(f"Conversões API: {api_orders}")
    print(f"Valor Conversões API: R$ {api_revenue:,.2f}")
    
    print("\n--- COMPARAÇÃO ---")
    print(f"Diferença Pedidos (API - CSV): {api_orders - csv_orders}")
    print(f"Diferença Receita (API - CSV): R$ {api_revenue - csv_revenue:,.2f}")

if __name__ == '__main__':
    main()
