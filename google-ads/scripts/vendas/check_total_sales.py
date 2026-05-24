import csv
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_FILE = PROJECT_ROOT / "data" / "imports" / "pedidos-mar-abr.csv"

def main():
    total_sales = 0.0
    total_orders = 0
    
    with open(CSV_FILE, mode='r', encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if not row:
                continue
            
            total_str = row.get('Total', '0').strip().replace('R$', '').strip().replace('.', '').replace(',', '.')
            if not total_str:
                total_str = '0'
            
            # exclude cancelled?
            status = row.get('Status pedido', '').strip()
            # if 'CANCELADO' in status:
            #     continue
            
            total_sales += float(total_str)
            total_orders += 1
                
    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: R$ {total_sales:,.2f}")

if __name__ == '__main__':
    main()
