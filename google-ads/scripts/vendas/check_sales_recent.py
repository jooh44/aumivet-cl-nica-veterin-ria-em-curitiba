import csv
from datetime import datetime, date, timedelta
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from core.reports import _query

CSV_FILE = PROJECT_ROOT / "data" / "imports" / "pedidos-mar-abr.csv"

def parse_csv(filepath, start_date, end_date):
    total_revenue_google = 0.0
    total_orders_google = 0
    total_revenue_all = 0.0
    total_orders_all = 0
    
    with open(filepath, mode='r', encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if not row:
                continue
            
            date_str = row.get('Data', '').strip()
            utm_source = row.get('UTM Source', '').strip()
            total_str = row.get('Total', '0').strip()
            total_str = total_str.replace('R$', '').strip().replace('.', '').replace(',', '.')
            if not total_str:
                total_str = '0'
            
            if not date_str:
                continue
                
            dt = datetime.strptime(date_str, '%d/%m/%Y').date()
            if start_date <= dt <= end_date:
                total_revenue_all += float(total_str)
                total_orders_all += 1
                
                if 'Google' in utm_source:
                    total_revenue_google += float(total_str)
                    total_orders_google += 1
                
    return total_orders_all, total_revenue_all, total_orders_google, total_revenue_google

def main():
    # Date range: Last 3 days (18, 19, 20 of April 2026)
    end_date = date(2026, 4, 20)
    start_date = end_date - timedelta(days=2)
    
    print(f"Analisando período recente: {start_date} até {end_date}")
    
    orders_all, rev_all, orders_google, rev_google = parse_csv(CSV_FILE, start_date, end_date)
    print(f"\n--- CSV DATA (Loja Virtual) ---")
    print(f"Total Vendas (Todos Canais/Origens): {orders_all} pedidos | R$ {rev_all:,.2f}")
    print(f"Vendas Atribuídas ao Google (UTM): {orders_google} pedidos | R$ {rev_google:,.2f}")
    
    print(f"\n--- GOOGLE ADS API DATA ---")
    gaql = f"""
        SELECT
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    """
    rows = _query(gaql)
    api_orders = 0
    api_revenue = 0.0
    for row in rows:
        api_orders += row.metrics.conversions
        api_revenue += row.metrics.conversions_value
        
    print(f"Conversões API: {api_orders:.2f}")
    print(f"Valor Conversões API: R$ {api_revenue:,.2f}")
    
    print("\n--- COMPARAÇÃO GOOGLE ADS (API vs CSV UTM) ---")
    print(f"Diferença Pedidos (API - CSV): {api_orders - orders_google:.2f}")
    print(f"Diferença Receita (API - CSV): R$ {api_revenue - rev_google:,.2f}")

if __name__ == '__main__':
    main()
