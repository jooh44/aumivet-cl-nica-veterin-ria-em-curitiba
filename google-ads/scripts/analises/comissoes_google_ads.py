import csv
import glob
from collections import defaultdict
from datetime import datetime

def main():
    files = glob.glob('/home/johny/Downloads/pedidos_752744_17768769999659_c4ac93c0.csv')
    
    ads_hidden_orders = ['16329', '16281', '16277']
    
    total_ads_revenue = 0.0
    total_ads_a_vista = 0.0
    
    for file in files:
        with open(file, newline='', encoding='utf-8-sig', errors='replace') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                status = row['Status pedido'].strip().upper()
                if status in ('CANCELADO', 'CANCELADO AUT'):
                    continue
                    
                total_str = row['Total'].replace('.', '').replace(',', '.')
                total = float(total_str) if total_str else 0.0
                
                canal = row['Canal de venda'].strip().upper()
                utm = row.get('UTM Source', '').strip()
                pedido_id = row['Pedido'].strip()
                pagamento = row['Pagamento tipo'].strip().upper()
                
                is_ads = False
                if canal == 'LOJA VIRTUAL':
                    if 'GOOGLE ADS' in utm.upper() or pedido_id in ads_hidden_orders:
                        is_ads = True
                        
                if is_ads:
                    total_ads_revenue += total
                    if 'PIX' in pagamento or 'BOLETO' in pagamento or 'DEPSITO' in pagamento or 'DEPÓSITO' in pagamento:
                        total_ads_a_vista += total

    print(f"Faturamento Total Google Ads: R$ {total_ads_revenue:,.2f}")
    print(f"Faturamento Google Ads (À Vista): R$ {total_ads_a_vista:,.2f}")
    
    print("\nComissões sobre o Faturamento Total:")
    print(f"- Se tudo fosse equipamento (7%): R$ {total_ads_revenue * 0.07:,.2f}")
    print(f"- Se tudo fosse consumo (3%): R$ {total_ads_revenue * 0.03:,.2f}")
    
    print("\nComissões sobre o Faturamento À Vista (PIX/Boleto):")
    print(f"- Se tudo fosse equipamento (7%): R$ {total_ads_a_vista * 0.07:,.2f}")
    print(f"- Se tudo fosse consumo (3%): R$ {total_ads_a_vista * 0.03:,.2f}")

if __name__ == "__main__":
    main()
