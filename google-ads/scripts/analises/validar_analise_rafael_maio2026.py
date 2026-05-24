#!/usr/bin/env python3
"""Validação da análise do Rafael (RZVET_Analise_GoogleAds_Pos_Dia8_Maio2026.html)
contra a API real do Google Ads. SOMENTE LEITURA — nenhuma mutação.

Hoje: 2026-05-12. Conta: 2419898793 (RZVET).
"""
import sys, os, traceback, logging
logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
logging.disable(logging.INFO)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.client import get_client, CUSTOMER_ID

client = get_client()
svc = client.get_service("GoogleAdsService")


def q(gaql):
    return list(svc.search(customer_id=CUSTOMER_ID, query=gaql))


def brl(micros):
    return round((micros or 0) / 1_000_000, 2)


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def safe(fn, label):
    try:
        fn()
    except Exception as e:
        print(f"\n[!] FALHOU bloco '{label}': {type(e).__name__}: {e}")
        traceback.print_exc(limit=2)


# Descobrir campanhas ATIVAS (as que o Rafael analisou estão entre elas)
ENABLED_CAMP_IDS = []
ENABLED_CAMP_NAMES = {}
def _load_enabled_campaigns():
    for r in q("SELECT campaign.id, campaign.name, campaign.advertising_channel_type FROM campaign WHERE campaign.status = 'ENABLED'"):
        ENABLED_CAMP_IDS.append(r.campaign.id)
        ENABLED_CAMP_NAMES[r.campaign.id] = r.campaign.name
_load_enabled_campaigns()
ENABLED_IN = "(" + ",".join(str(i) for i in ENABLED_CAMP_IDS) + ")" if ENABLED_CAMP_IDS else "(0)"


# ─────────────────────────────────────────────────────────────────────────────
# 1. CHANGE EVENTS — últimos 14 dias (cobre desde ~28/04)
# ─────────────────────────────────────────────────────────────────────────────
def bloco_change_events():
    section("1. CHANGE EVENTS — últimos 14 dias (quem mexeu no quê)")
    rows = q("""
        SELECT
            change_event.change_date_time,
            change_event.user_email,
            change_event.client_type,
            change_event.change_resource_type,
            change_event.resource_change_operation,
            change_event.changed_fields,
            change_event.campaign,
            change_event.ad_group
        FROM change_event
        WHERE change_event.change_date_time DURING LAST_14_DAYS
        ORDER BY change_event.change_date_time DESC
        LIMIT 1000
    """)
    print(f"Total de eventos: {len(rows)}\n")
    print(f"{'Data/Hora':<22} {'Usuário':<26} {'Origem':<14} {'Recurso':<22} {'Op':<8} Campos")
    print("-" * 130)
    for r in rows:
        ce = r.change_event
        try:
            fields = ", ".join(ce.changed_fields.paths)
        except Exception:
            fields = ""
        camp = ENABLED_CAMP_NAMES.get(int(ce.campaign.split("/")[-1]), ce.campaign.split("/")[-1]) if ce.campaign else ""
        print(f"{ce.change_date_time:<22} {(ce.user_email or '')[:25]:<26} "
              f"{ce.client_type.name[:13]:<14} {ce.change_resource_type.name[:21]:<22} "
              f"{ce.resource_change_operation.name[:7]:<8} {fields[:50]}"
              + (f"  | camp={camp[:30]}" if camp else ""))
    print("\n>>> NOTA: a API change_event NÃO captura mudanças em metas de conversão / "
          "conversion_action / conversion_goal — isso só aparece no change history da UI. "
          "Estado ATUAL dessas metas: blocos 2 e 3.")


# ─────────────────────────────────────────────────────────────────────────────
# 2. METAS DE CONVERSÃO DA CONTA (customer_conversion_goal) — estado atual
# ─────────────────────────────────────────────────────────────────────────────
def bloco_conversion_goals():
    section("2. METAS DE CONVERSÃO DA CONTA — biddable? (customer_conversion_goal)")
    rows = q("SELECT customer_conversion_goal.category, customer_conversion_goal.origin, customer_conversion_goal.biddable FROM customer_conversion_goal")
    print(f"{'Categoria':<26} {'Origem':<16} {'Biddable (= meta padrão da conta?)'}")
    print("-" * 72)
    for r in sorted(rows, key=lambda x: (not x.customer_conversion_goal.biddable, x.customer_conversion_goal.category.name)):
        g = r.customer_conversion_goal
        print(f"{g.category.name:<26} {g.origin.name:<16} {g.biddable}")
    print("\n>>> Rafael alega que 'Submit lead forms' e 'Add to cart' foram REMOVIDAS das metas padrão "
          "em 08/05. Se ADD_TO_CART/SUBMIT_LEAD_FORM aparecem biddable=False, de fato não são metas "
          "padrão hoje — mas pode ser a config correta de 23/03 (MEMORY), não a causa da queda.")


# ─────────────────────────────────────────────────────────────────────────────
# 3. CONVERSION ACTIONS — estado + métricas 30d
# ─────────────────────────────────────────────────────────────────────────────
def bloco_conversion_actions():
    section("3. CONVERSION ACTIONS — status, categoria, primary_for_goal, atribuição")
    rows = q("""
        SELECT conversion_action.id, conversion_action.name, conversion_action.status,
               conversion_action.type, conversion_action.category, conversion_action.origin,
               conversion_action.primary_for_goal, conversion_action.counting_type,
               conversion_action.include_in_conversions_metric,
               conversion_action.click_through_lookback_window_days,
               conversion_action.attribution_model_settings.attribution_model
        FROM conversion_action ORDER BY conversion_action.name
    """)
    print(f"{'Nome':<42} {'Status':<10} {'Categoria':<20} {'primary':<8} {'incl.conv':<10} {'janela':<7} Atribuição")
    print("-" * 130)
    for r in rows:
        ca = r.conversion_action
        print(f"{ca.name[:41]:<42} {ca.status.name:<10} {ca.category.name[:19]:<20} "
              f"{str(ca.primary_for_goal):<8} {str(ca.include_in_conversions_metric):<10} "
              f"{ca.click_through_lookback_window_days:<7} {ca.attribution_model_settings.attribution_model.name}")

    section("3b. CONVERSÕES POR AÇÃO — últimos 30 dias (conta inteira, all_conversions)")
    try:
        rows = q("""
            SELECT segments.conversion_action_name, segments.conversion_action_category,
                   metrics.all_conversions, metrics.all_conversions_value
            FROM customer WHERE segments.date DURING LAST_30_DAYS
        """)
        agg = {}
        for r in rows:
            k = (r.segments.conversion_action_name, r.segments.conversion_action_category.name)
            d = agg.setdefault(k, {"c": 0.0, "v": 0.0})
            d["c"] += r.metrics.all_conversions
            d["v"] += r.metrics.all_conversions_value
        print(f"{'Ação de conversão':<44} {'Categoria':<20} {'Conv (all)':>12} {'Valor (all)':>14}")
        print("-" * 95)
        for (name, cat), d in sorted(agg.items(), key=lambda x: -x[1]["v"]):
            print(f"{(name or '(sem nome)')[:43]:<44} {cat[:19]:<20} {d['c']:>12.2f} {d['v']:>14.2f}")
    except Exception as e:
        print(f"[!] conversões por ação falhou: {e}")
    print("\n>>> Confere o '78 compras / R$43 mil' que o Rafael marcou como possivelmente distorcido.")


# ─────────────────────────────────────────────────────────────────────────────
# 4. CAMPANHAS — 30 dias + split antes/depois de 08/05
# ─────────────────────────────────────────────────────────────────────────────
CAMP_FIELDS = """
    campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
    campaign.primary_status, campaign_budget.amount_micros,
    metrics.impressions, metrics.clicks, metrics.cost_micros,
    metrics.conversions, metrics.conversions_value,
    metrics.all_conversions, metrics.all_conversions_value, metrics.average_cpc,
    metrics.search_impression_share, metrics.search_budget_lost_impression_share,
    metrics.search_rank_lost_impression_share
"""

def _print_campaigns(rows, titulo):
    print(f"\n--- {titulo} ---")
    print(f"{'Campanha':<40} {'PrimaryStatus':<22} {'Orç/d':>8} {'Custo':>9} {'Conv':>7} {'CPA':>9} "
          f"{'AllConv':>8} {'Val':>10} {'IS%':>6} {'LostBudg%':>10} {'LostRank%':>10}")
    print("-" * 150)
    tc = tcv = tco = 0.0
    for r in rows:
        if r.metrics.impressions == 0 and r.metrics.cost_micros == 0:
            continue
        m = r.metrics
        cost = brl(m.cost_micros); conv = m.conversions; val = m.conversions_value
        tc += cost; tco += conv; tcv += val
        cpa = cost / conv if conv else 0
        is_ = m.search_impression_share * 100 if m.search_impression_share else None
        lb = m.search_budget_lost_impression_share * 100 if m.search_budget_lost_impression_share else None
        lr = m.search_rank_lost_impression_share * 100 if m.search_rank_lost_impression_share else None
        print(f"{r.campaign.name[:39]:<40} {r.campaign.primary_status.name[:21]:<22} "
              f"{brl(r.campaign_budget.amount_micros):>8.2f} {cost:>9.2f} {conv:>7.2f} {cpa:>9.2f} "
              f"{m.all_conversions:>8.2f} {val:>10.2f} {(f'{is_:.1f}' if is_ is not None else 'N/A'):>6} "
              f"{(f'{lb:.1f}' if lb is not None else 'N/A'):>10} {(f'{lr:.1f}' if lr is not None else 'N/A'):>10}")
    cpa_t = tc / tco if tco else 0
    print("-" * 150)
    print(f"{'TOTAL (campanhas com tráfego)':<40} {'':<22} {'':>8} {tc:>9.2f} {tco:>7.2f} {cpa_t:>9.2f} {'':>8} {tcv:>10.2f}")

def bloco_campanhas():
    section("4. CAMPANHAS — performance (conversions = métrica de bidding)")
    _print_campaigns(q(f"SELECT {CAMP_FIELDS} FROM campaign WHERE segments.date BETWEEN '2026-04-12' AND '2026-05-11' ORDER BY metrics.cost_micros DESC"),
                     "Últimos 30 dias (12/abr → 11/mai) — comparar com a tabela do Rafael")
    _print_campaigns(q(f"SELECT {CAMP_FIELDS} FROM campaign WHERE segments.date BETWEEN '2026-05-01' AND '2026-05-07' ORDER BY metrics.cost_micros DESC"),
                     "ANTES: 01→07/mai (7 dias)")
    _print_campaigns(q(f"SELECT {CAMP_FIELDS} FROM campaign WHERE segments.date BETWEEN '2026-05-08' AND '2026-05-11' ORDER BY metrics.cost_micros DESC"),
                     "DEPOIS: 08→11/mai (4 dias) — Rafael alega CPA Produtos R$94,93 → R$139,90")
    _print_campaigns(q(f"SELECT {CAMP_FIELDS} FROM campaign WHERE segments.date BETWEEN '2026-04-08' AND '2026-05-07' ORDER BY metrics.cost_micros DESC"),
                     "Janela de 30d ANTES do dia 8: 08/abr → 07/mai (base do 'CPA anterior R$94,93')")


# ─────────────────────────────────────────────────────────────────────────────
# 5. TENDÊNCIA DIÁRIA — 24/abr → 11/mai (conta inteira)
# ─────────────────────────────────────────────────────────────────────────────
def bloco_diario():
    section("5. TENDÊNCIA DIÁRIA — conta inteira, 24/abr → 11/mai (dia 8 = corte do Rafael)")
    rows = q("""
        SELECT segments.date, segments.day_of_week,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.conversions_value, metrics.all_conversions
        FROM customer WHERE segments.date BETWEEN '2026-04-24' AND '2026-05-11' ORDER BY segments.date
    """)
    print(f"{'Data':<12} {'Dia':<10} {'Impr':>8} {'Cliques':>8} {'Custo':>10} {'Conv':>8} {'AllConv':>9} {'Valor':>11} {'CPA':>9}")
    print("-" * 100)
    for r in rows:
        m = r.metrics
        cost = brl(m.cost_micros); conv = m.conversions
        cpa = cost / conv if conv else 0
        marker = "  <== DIA 8 (corte do Rafael)" if str(r.segments.date) == "2026-05-08" else ""
        print(f"{str(r.segments.date):<12} {r.segments.day_of_week.name[:9]:<10} {m.impressions:>8} {m.clicks:>8} "
              f"{cost:>10.2f} {conv:>8.2f} {m.all_conversions:>9.2f} {m.conversions_value:>11.2f} {cpa:>9.2f}{marker}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. KEYWORDS
# ─────────────────────────────────────────────────────────────────────────────
ALVO_KW = ["equipamentos veterinários", "esfigmomanômetro", "manguito veterinario",
           "monitores veterinários", "monitor veterinário portátil", "doppler veterinario",
           "oximetro veterinario", "ventpet"]
ALVO_LOW = [k.lower() for k in ALVO_KW]

def bloco_keywords():
    section("6. KEYWORDS — estado atual nas campanhas ATIVAS (e qualquer alvo do Rafael)")
    rows = q(f"""
        SELECT campaign.name, campaign.status, ad_group.name, ad_group.status,
               ad_group_criterion.criterion_id, ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type, ad_group_criterion.status,
               ad_group_criterion.quality_info.quality_score
        FROM ad_group_criterion
        WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
          AND campaign.id IN {ENABLED_IN}
        ORDER BY campaign.name, ad_group.name, ad_group_criterion.keyword.text
    """)
    print(f"{'Keyword':<40} {'Match':<8} {'KW':<9} {'AG':<9} {'Camp':<9} {'QS':>3} {'Campanha / AdGroup'}")
    print("-" * 135)
    alvo_found = set()
    for r in rows:
        c = r.ad_group_criterion
        txt = c.keyword.text
        is_alvo = txt.lower() in ALVO_LOW
        if is_alvo:
            alvo_found.add(txt.lower())
        qs = c.quality_info.quality_score if c.quality_info.quality_score else "-"
        mark = " ***ALVO RAFAEL" if is_alvo else ""
        print(f"{txt[:39]:<40} {c.keyword.match_type.name[:7]:<8} {c.status.name[:8]:<9} "
              f"{r.ad_group.status.name[:8]:<9} {r.campaign.status.name[:8]:<9} {str(qs):>3} "
              f"{r.campaign.name[:24]} / {r.ad_group.name[:22]}{mark}")
    faltando = [k for k in ALVO_KW if k.lower() not in alvo_found]
    if faltando:
        print(f"\n>>> Keywords da tabela do Rafael NÃO encontradas nas campanhas ativas: {faltando}")

    section("6b. KEYWORDS — métricas últimos 30 dias (top 50 por custo, qualquer campanha)")
    rows = q("""
        SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type, ad_group_criterion.status,
               ad_group_criterion.quality_info.quality_score,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.conversions_value, metrics.average_cpc
        FROM keyword_view WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC LIMIT 50
    """)
    print(f"{'Keyword':<38} {'Match':<8} {'Status':<9} {'QS':>3} {'Impr':>7} {'Cliq':>6} {'Custo':>9} {'CPC':>7} {'Conv':>6} {'Valor':>10} {'Campanha'}")
    print("-" * 145)
    for r in rows:
        c = r.ad_group_criterion; m = r.metrics
        qs = c.quality_info.quality_score if c.quality_info.quality_score else "-"
        mark = " *ALVO" if c.keyword.text.lower() in ALVO_LOW else ""
        print(f"{c.keyword.text[:37]:<38} {c.keyword.match_type.name[:7]:<8} {c.status.name[:8]:<9} {str(qs):>3} "
              f"{m.impressions:>7} {m.clicks:>6} {brl(m.cost_micros):>9.2f} {brl(m.average_cpc):>7.2f} "
              f"{m.conversions:>6.2f} {m.conversions_value:>10.2f} {r.campaign.name[:20]}{mark}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. NEGATIVAS — campanhas ativas (Rafael: 22 adicionadas na [Search] Produtos)
# ─────────────────────────────────────────────────────────────────────────────
def bloco_negativas():
    section("7. NEGATIVAS de campanha — campanhas ativas")
    rows = q(f"""
        SELECT campaign.id, campaign.name, campaign_criterion.criterion_id,
               campaign_criterion.negative, campaign_criterion.keyword.text,
               campaign_criterion.keyword.match_type
        FROM campaign_criterion
        WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'
          AND campaign.id IN {ENABLED_IN}
        ORDER BY campaign.name
    """)
    by_camp = {}
    for r in rows:
        by_camp.setdefault(r.campaign.name, []).append(
            (r.campaign_criterion.keyword.text, r.campaign_criterion.keyword.match_type.name))
    SUSPEITAS = ["como usar", "conserto", "manual", "como funciona", "o que é", "significado",
                 "curso", "concerto", "reparo", "defeito"]
    for camp, kws in by_camp.items():
        print(f"\n{camp}  —  {len(kws)} negativas de campanha. Sinalizadas para revisão:")
        flagged = [(txt, mt) for txt, mt in sorted(kws) if any(s in txt.lower() for s in SUSPEITAS)]
        if not flagged:
            print("   (nenhuma negativa obviamente nociva)")
        for txt, mt in flagged:
            print(f"   [{mt:<7}] {txt}   <-- revisar (pode bloquear busca legítima)")

    section("7b. LISTAS DE NEGATIVAS COMPARTILHADAS (shared sets)")
    try:
        for r in q("SELECT shared_set.id, shared_set.name, shared_set.type, shared_set.status, shared_set.member_count FROM shared_set"):
            s = r.shared_set
            print(f"  set: {s.name} (tipo={s.type_.name}, membros={s.member_count}, status={s.status.name})")
        for r in q("SELECT campaign.name, shared_set.name, shared_set.type FROM campaign_shared_set"):
            print(f"  vínculo: {r.campaign.name} <- {r.shared_set.name} ({r.shared_set.type_.name})")
    except Exception as e:
        print(f"  [!] shared sets: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. ANÚNCIOS — ad strength (Rafael: 5 de 14 'Ruim')
# ─────────────────────────────────────────────────────────────────────────────
def bloco_anuncios():
    section("8. ANÚNCIOS — ad_strength + status de aprovação (campanhas ativas)")
    rows = q(f"""
        SELECT campaign.name, ad_group.name, ad_group.status, ad_group_ad.ad.id, ad_group_ad.ad.type,
               ad_group_ad.status, ad_group_ad.ad_strength,
               ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status
        FROM ad_group_ad
        WHERE ad_group_ad.status != 'REMOVED' AND campaign.id IN {ENABLED_IN}
        ORDER BY campaign.name, ad_group.name
    """)
    print(f"{'Campanha':<32} {'AdGroup':<24} {'Tipo':<22} {'AdStatus':<9} {'AG':<8} {'Força':<10} {'Aprovação':<14} {'Review'}")
    print("-" * 140)
    cont = {}
    for r in rows:
        a = r.ad_group_ad
        cont[a.ad_strength.name] = cont.get(a.ad_strength.name, 0) + 1
        print(f"{r.campaign.name[:31]:<32} {r.ad_group.name[:23]:<24} {a.ad.type_.name[:21]:<22} "
              f"{a.status.name:<9} {r.ad_group.status.name[:7]:<8} {a.ad_strength.name:<10} "
              f"{a.policy_summary.approval_status.name:<14} {a.policy_summary.review_status.name}")
    print(f"\nContagem por força do anúncio (campanhas ativas): {cont}  (Rafael alega 5 'POOR'/Ruim de 14)")


# ─────────────────────────────────────────────────────────────────────────────
# 9. SITELINKS / ASSETS — status de aprovação (Rafael: sitelinks reprovados)
# ─────────────────────────────────────────────────────────────────────────────
def bloco_sitelinks():
    section("9. SITELINKS — status de aprovação (Rafael: sitelinks reprovados em 3 campanhas)")
    rows = q("""
        SELECT asset.id, asset.type, asset.name, asset.sitelink_asset.link_text,
               asset.policy_summary.approval_status, asset.policy_summary.review_status
        FROM asset WHERE asset.type = 'SITELINK' ORDER BY asset.id
    """)
    print(f"{'AssetID':<14} {'Texto do sitelink':<42} {'Aprovação':<18} {'Review'}")
    print("-" * 95)
    for r in rows:
        a = r.asset
        print(f"{a.id:<14} {(a.sitelink_asset.link_text or a.name or '')[:41]:<42} "
              f"{a.policy_summary.approval_status.name:<18} {a.policy_summary.review_status.name}")

    section("9b. SITELINKS vinculados a campanhas ativas")
    try:
        rows = q(f"""
            SELECT campaign.id, campaign.name, asset.sitelink_asset.link_text,
                   campaign_asset.status, campaign_asset.field_type, asset.policy_summary.approval_status
            FROM campaign_asset
            WHERE campaign_asset.field_type = 'SITELINK' AND campaign.id IN {ENABLED_IN}
            ORDER BY campaign.name
        """)
        for r in rows:
            ca = r.campaign_asset
            print(f"  {r.campaign.name[:34]:<35} | {(r.asset.sitelink_asset.link_text or '')[:30]:<31} | "
                  f"link={ca.status.name:<10} aprov={r.asset.policy_summary.approval_status.name}")
    except Exception as e:
        print(f"  [!] campaign_asset sitelinks: {e}")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"VALIDAÇÃO — análise do Rafael x API Google Ads | conta {CUSTOMER_ID} | hoje 2026-05-12")
    print(f"Campanhas ATIVAS ({len(ENABLED_CAMP_IDS)}): " + " | ".join(ENABLED_CAMP_NAMES.values()))
    safe(bloco_change_events, "change_events")
    safe(bloco_conversion_goals, "conversion_goals")
    safe(bloco_conversion_actions, "conversion_actions")
    safe(bloco_campanhas, "campanhas")
    safe(bloco_diario, "diario")
    safe(bloco_keywords, "keywords")
    safe(bloco_negativas, "negativas")
    safe(bloco_anuncios, "anuncios")
    safe(bloco_sitelinks, "sitelinks")
    print("\n\n✅ Coleta concluída.")
