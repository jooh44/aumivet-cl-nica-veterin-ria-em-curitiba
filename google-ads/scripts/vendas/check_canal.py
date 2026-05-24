import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_FILE = PROJECT_ROOT / "data" / "imports" / "pedidos-mar-abr.csv"

def main():
    canal_counts = Counter()
    canal_revenue = Counter()
    
    with open(CSV_FILE, mode='r', encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if not row:
                continue
            
            canal = row.get('Canal de venda', '').strip()
            total_str = row.get('Total', '0').strip().replace('R$', '').strip().replace('.', '').replace(',', '.')
            if not total_str:
                total_str = '0'
            
            canal_counts[canal] += 1
            canal_revenue[canal] += float(total_str)
                
    print("Canal de venda:")
    for c, count in canal_counts.items():
        print(f"  {c}: {count} pedidos, R$ {canal_revenue[c]:,.2f}")

if __name__ == '__main__':
    main()
