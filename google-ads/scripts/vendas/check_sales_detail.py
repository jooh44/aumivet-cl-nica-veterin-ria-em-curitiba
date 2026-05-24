import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_FILE = PROJECT_ROOT / "data" / "imports" / "pedidos-mar-abr.csv"

def main():
    status_counts = Counter()
    canal_counts = Counter()
    total_google = 0.0
    
    with open(CSV_FILE, mode='r', encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if not row:
                continue
            
            utm_source = row.get('UTM Source', '').strip()
            status = row.get('Status pedido', '').strip()
            canal = row.get('Canal de venda', '').strip()
            total_str = row.get('Total', '0').strip().replace('R$', '').strip().replace('.', '').replace(',', '.')
            if not total_str:
                total_str = '0'
            
            if 'Google' in utm_source:
                status_counts[status] += 1
                canal_counts[canal] += 1
                total_google += float(total_str)
                
    print("Status para Google Ads:")
    for s, c in status_counts.items():
        print(f"  {s}: {c}")
        
    print("\nCanal de venda para Google Ads:")
    for c, count in canal_counts.items():
        print(f"  {c}: {count}")

if __name__ == '__main__':
    main()
