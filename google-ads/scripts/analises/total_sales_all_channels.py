import csv
from collections import defaultdict
from datetime import datetime

def main():
    csv_path = "/home/johny/Downloads/pedidos_752744_17768769999659_c4ac93c0.csv"
    
    # Pedidos que sabemos que vieram do Ads mas perderam a UTM
    ads_hidden_orders = ['16329', '16281', '16277']
    
    channel_totals = defaultdict(lambda: {'orders': 0, 'revenue': 0.0})
    
    with open(csv_path, newline='', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            status = row['Status pedido'].strip().upper()
            if status == 'CANCELADO' or status == 'CANCELADO AUT':
                continue
                
            total_str = row['Total'].replace('.', '').replace(',', '.')
            total = float(total_str) if total_str else 0.0
            
            canal = row['Canal de venda'].strip().upper()
            utm = row.get('UTM Source', '').strip()
            pedido_id = row['Pedido'].strip()
            
            if canal == 'LOJA VIRTUAL':
                if 'Google Ads' in utm or pedido_id in ads_hidden_orders:
                    derived_channel = 'Loja Virtual (Google Ads)'
                else:
                    derived_channel = 'Loja Virtual (Orgânico / Direto)'
            elif canal == 'MERCADO LIVRE':
                derived_channel = 'Mercado Livre'
            elif canal == 'SHOPEE':
                derived_channel = 'Shopee'
            else:
                derived_channel = canal
                
            channel_totals[derived_channel]['orders'] += 1
            channel_totals[derived_channel]['revenue'] += total

    print(f"{'Canal de Venda':<45} | {'Qtd Pedidos':<12} | {'Faturamento (R$)'}")
    print("-" * 80)
    
    total_orders = 0
    total_revenue = 0.0
    
    # Sort by revenue descending
    sorted_channels = sorted(channel_totals.items(), key=lambda x: x[1]['revenue'], reverse=True)
    
    for channel, data in sorted_channels:
        orders = data['orders']
        revenue = data['revenue']
        total_orders += orders
        total_revenue += revenue
        print(f"{channel:<45} | {orders:<12} | R$ {revenue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
    print("-" * 80)
    print(f"{'TOTAL GERAL':<45} | {total_orders:<12} | R$ {total_revenue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

if __name__ == "__main__":
    main()
