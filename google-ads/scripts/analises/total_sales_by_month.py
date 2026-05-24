import csv
from collections import defaultdict
from datetime import datetime

def main():
    csv_path = "/home/johny/Downloads/pedidos_752744_17768769999659_c4ac93c0.csv"
    
    # Pedidos que sabemos que vieram do Ads mas perderam a UTM
    ads_hidden_orders = ['16329', '16281', '16277']
    
    # Estrutura: data_by_month[mes_ano][canal] = {'orders': 0, 'revenue': 0.0}
    data_by_month = defaultdict(lambda: defaultdict(lambda: {'orders': 0, 'revenue': 0.0}))
    
    with open(csv_path, newline='', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            status = row['Status pedido'].strip().upper()
            if status == 'CANCELADO' or status == 'CANCELADO AUT':
                continue
                
            date_str = row['Data'].strip()
            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y")
                month_year = dt.strftime("%Y-%m")
            except ValueError:
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
                
            data_by_month[month_year][derived_channel]['orders'] += 1
            data_by_month[month_year][derived_channel]['revenue'] += total

    # Meses em pt-br para exibicao
    meses_pt = {
        '2026-01': 'Janeiro 2026',
        '2026-02': 'Fevereiro 2026',
        '2026-03': 'Março 2026',
        '2026-04': 'Abril 2026'
    }

    for month_key in sorted(data_by_month.keys()):
        month_name = meses_pt.get(month_key, month_key)
        print(f"### 📅 {month_name}")
        print(f"{'Canal de Venda':<40} | {'Qtd Pedidos':<12} | {'Faturamento (R$)'}")
        print("-" * 80)
        
        month_total_orders = 0
        month_total_revenue = 0.0
        
        # Sort by revenue descending within the month
        sorted_channels = sorted(data_by_month[month_key].items(), key=lambda x: x[1]['revenue'], reverse=True)
        
        for channel, data in sorted_channels:
            orders = data['orders']
            revenue = data['revenue']
            month_total_orders += orders
            month_total_revenue += revenue
            print(f"{channel:<40} | {orders:<12} | R$ {revenue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
        print("-" * 80)
        print(f"{'TOTAL DO MÊS':<40} | {month_total_orders:<12} | R$ {month_total_revenue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print("\n")

if __name__ == "__main__":
    main()
