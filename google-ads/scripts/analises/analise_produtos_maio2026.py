#!/usr/bin/env python3
"""
Análise de produtos caros — PMAX/Shopping Maio 2026
- Performance por produto
- Ticket médio implícito das conversões
- Tracking check
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.client import get_client, CUSTOMER_ID

client = get_client()
svc = client.get_service("GoogleAdsService")

START, END = "2026-05-01", "2026-05-09"

def q(gaql):
    return list(svc.search(customer_id=CUSTOMER_ID, query=gaql))

def brl(micros):
    return round(micros / 1_000_000, 2)


# ── 1. Shopping Products Performance ──────────────────────────
print("\n" + "="*80)
print(f"PRODUTOS SHOPPING/PMAX — {START} a {END}")
print("="*80)

rows = q(f"""
    SELECT
        campaign.name,
        segments.product_title,
        segments.product_item_id,
        segments.product_brand,
        segments.product_type_l1,
        segments.product_type_l2,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value,
        metrics.all_conversions,
        metrics.all_conversions_value,
        metrics.ctr,
        metrics.average_cpc
    FROM shopping_performance_view
    WHERE segments.date BETWEEN '{START}' AND '{END}'
    ORDER BY metrics.clicks DESC
    LIMIT 50
""")

products = []
for r in rows:
    cost = brl(r.metrics.cost_micros)
    val  = round(r.metrics.conversions_value, 2)
    conv = round(r.metrics.conversions, 2)
    all_conv = round(r.metrics.all_conversions, 2)
    all_val  = round(r.metrics.all_conversions_value, 2)
    products.append({
        "title":    r.segments.product_title[:50],
        "item_id":  r.segments.product_item_id,
        "campaign": r.campaign.name[:30],
        "clicks":   r.metrics.clicks,
        "impressions": r.metrics.impressions,
        "cost":     cost,
        "ctr":      round(r.metrics.ctr * 100, 2),
        "cpc":      brl(r.metrics.average_cpc),
        "conv":     conv,
        "val":      val,
        "all_conv": all_conv,
        "all_val":  all_val,
        "roas":     round(val / cost, 2) if cost > 0 else 0,
        "ticket":   round(val / conv, 2) if conv > 0 else None,
    })

# Mostrar tudo com cliques
print(f"\n{'Produto':<52} {'ID':>8} {'Clicks':>7} {'Custo':>9} {'CPC':>7} {'Conv':>5} {'Val':>9} {'ROAS':>6} {'Ticket':>9}")
print("-"*115)

total_clicks = total_cost = total_conv = total_val = 0
for p in products:
    if p["clicks"] == 0:
        continue
    ticket_str = f"R${p['ticket']:>8.0f}" if p["ticket"] else "       ---"
    conv_flag = "⚠️" if p["clicks"] >= 5 and p["conv"] == 0 else ""
    print(f"{p['title']:<52} {p['item_id']:>8} {p['clicks']:>7} R${p['cost']:>8.2f} R${p['cpc']:>6.2f} {p['conv']:>5.1f} R${p['val']:>8.2f} {p['roas']:>5.2f}x {ticket_str} {conv_flag}")
    total_clicks += p["clicks"]
    total_cost   += p["cost"]
    total_conv   += p["conv"]
    total_val    += p["val"]

print("-"*115)
print(f"{'TOTAL':<52} {'':>8} {total_clicks:>7} R${total_cost:>8.2f} {'':>7} {total_conv:>5.1f} R${total_val:>8.2f}")


# ── 2. Ticket médio das conversões registradas ────────────────
print("\n" + "="*80)
print("ANÁLISE DO TICKET MÉDIO — O QUE ESTÁ CONVERTENDO?")
print("="*80)

# Conversões por campanha com valor
rows = q(f"""
    SELECT
        campaign.name,
        campaign.advertising_channel_type,
        metrics.conversions,
        metrics.conversions_value,
        metrics.all_conversions,
        metrics.all_conversions_value
    FROM campaign
    WHERE segments.date BETWEEN '{START}' AND '{END}'
        AND campaign.status = 'ENABLED'
        AND metrics.conversions > 0
    ORDER BY metrics.conversions_value DESC
""")

print(f"\n{'Campanha':<45} {'Conv':>5} {'Valor':>9} {'Ticket Médio':>13} {'all_conv':>9} {'all_val':>9}")
print("-"*95)
for r in rows:
    conv = round(r.metrics.conversions, 2)
    val  = round(r.metrics.conversions_value, 2)
    ticket = round(val / conv, 2) if conv > 0 else 0
    all_c = round(r.metrics.all_conversions, 2)
    all_v = round(r.metrics.all_conversions_value, 2)
    print(f"{r.campaign.name:<45} {conv:>5.1f} R${val:>8.2f} R${ticket:>11.2f} {all_c:>9.1f} R${all_v:>8.2f}")


# ── 3. Conversões por ação de conversão (o que está trackando) ─
print("\n" + "="*80)
print("TRACKING CHECK — CONVERSÕES POR AÇÃO")
print("="*80)

rows = q(f"""
    SELECT
        conversion_action.name,
        conversion_action.status,
        conversion_action.include_in_conversions_metric,
        conversion_action.primary_for_goal,
        conversion_action.type,
        conversion_action.category,
        metrics.conversions,
        metrics.conversions_value,
        metrics.all_conversions,
        metrics.all_conversions_value,
        metrics.cost_per_conversion
    FROM conversion_action
    WHERE segments.date BETWEEN '{START}' AND '{END}'
        AND metrics.all_conversions > 0
    ORDER BY metrics.all_conversions DESC
""")

print(f"\n{'Ação de Conversão':<45} {'Primária':>8} {'Status':>8} {'conv':>6} {'val':>9} {'all_c':>7} {'all_v':>9}")
print("-"*100)
for r in rows:
    primary = "✅ SIM" if r.conversion_action.primary_for_goal else "   NÃO"
    include = "INC" if r.conversion_action.include_in_conversions_metric else "EXC"
    conv = round(r.metrics.conversions, 2)
    val  = round(r.metrics.conversions_value, 2)
    all_c = round(r.metrics.all_conversions, 2)
    all_v = round(r.metrics.all_conversions_value, 2)
    status = r.conversion_action.status.name[:8]
    print(f"{r.conversion_action.name[:44]:<45} {primary:>8} {status:>8} {conv:>6.1f} R${val:>8.2f} {all_c:>7.1f} R${all_v:>8.2f}")


# ── 4. Search terms da campanha de Produtos (o que ativa) ─────
print("\n" + "="*80)
print("SEARCH TERMS — [Search] RZVet - Produtos (maio)")
print("="*80)

rows = q(f"""
    SELECT
        search_term_view.search_term,
        ad_group.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value
    FROM search_term_view
    WHERE segments.date BETWEEN '{START}' AND '{END}'
        AND campaign.name LIKE '%Produtos%'
    ORDER BY metrics.cost_micros DESC
    LIMIT 30
""")

print(f"\n{'Termo de Pesquisa':<50} {'Ad Group':<25} {'Clicks':>7} {'Custo':>9} {'Conv':>5}")
print("-"*100)
for r in rows:
    cost = brl(r.metrics.cost_micros)
    conv = round(r.metrics.conversions, 2)
    flag = " ⚠️" if r.metrics.clicks >= 3 and conv == 0 else ""
    print(f"{r.search_term_view.search_term[:49]:<50} {r.ad_group.name[:24]:<25} {r.metrics.clicks:>7} R${cost:>8.2f} {conv:>5.1f}{flag}")


# ── 5. Diagnóstico econômico ──────────────────────────────────
print("\n" + "="*80)
print("DIAGNÓSTICO ECONÔMICO — VIABILIDADE DOS PRODUTOS CAROS")
print("="*80)

# Estimar CPL aceitável
COMISSAO_MEDIA = 700  # R$ informado pelo usuário
TAXA_FECHAMENTO = 0.05  # conservador: 5% dos cliques viram venda (lead quente)

print(f"""
Premissas:
  • Comissão média por venda de produto caro: R${COMISSAO_MEDIA:.0f}
  • CPA break-even (se 1 em cada clique fosse conversão): R${COMISSAO_MEDIA:.0f}

Raciocínio de funil (estimativa conservadora):
  • 1 em 20 cliques gera uma venda → CPC break-even = R${COMISSAO_MEDIA/20:.0f}
  • 1 em 50 cliques gera uma venda → CPC break-even = R${COMISSAO_MEDIA/50:.0f}
  • 1 em 100 cliques gera uma venda → CPC break-even = R${COMISSAO_MEDIA/100:.0f}

Os CPCs observados nos produtos caros (monitor, ultrassom):
  • CPC médio ~ R$2-3 → se 1 em 100 cliques converter: ROAS positivo ✅
  • Problema: sem rastreamento de conversão de produto caro = cego

Questão central de tracking:
  - Se GA4/Tray registra "purchase" com valor do produto → PMAX aprende a vender caro ✅
  - Se o ticket médio reportado é muito baixo (< R$300) → pode estar convertendo
    só acessórios baratos, não os produtos grandes
""")

print("✅ Script concluído.")
