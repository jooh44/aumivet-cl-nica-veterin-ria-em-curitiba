#!/usr/bin/env python3
"""
Aplica as 3 ações aprovadas após a validação da análise do Rafael (12/mai/2026).
Plano: ~/.claude/plans/atomic-brewing-marshmallow.md
Relatório: RZVET_Validacao_Analise_Rafael_2026-05-12.md

Dry-run por padrão. Passe --apply para efetivar.

Blocos:
  1. Pausar keywords QI 1/10 que afundam o Ad Rank da [Search] RZVet - Produtos
     (grupo "Produtos Gerais" + limpeza do grupo "Monitoramento").
  2. Reativar o grupo Monitoramento — as 4 keywords que o Rafael pediu.
  3. Corrigir os 2 sitelinks reprovados (apontavam pra 404 / homepage cru).
"""
import sys, os, json, logging
logging.disable(logging.INFO)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.client import get_client, CUSTOMER_ID
from core.mutates import pause_keywords_bulk, enable_keywords_bulk, update_asset_final_urls

DRY_RUN = "--apply" not in sys.argv
client = get_client()
svc = client.get_service("GoogleAdsService")

print("\n" + ("🔍 DRY-RUN — nada será aplicado. Use --apply para efetivar." if DRY_RUN
              else "🚀 APLICANDO MUDANÇAS...") + "\n")

CAMP_PRODUTOS = 23361821714  # [Search] RZVet - Produtos (Maximize Conversion Value)
AG_PRODUTOS_GERAIS = 189770626483
AG_MONITORAMENTO = 190352009499


def show(results):
    for r in results:
        if isinstance(r, list):
            for x in r:
                print(f"    - {json.dumps(x, ensure_ascii=False)}")
        else:
            print(f"    - {json.dumps(r, ensure_ascii=False)}")


# ═══════════════════════════════════════════════════════════════
# BLOCO 1 — Pausar keywords QI 1/10
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("BLOCO 1 — Pausar keywords QI 1/10 na [Search] RZVet - Produtos")
print("=" * 70)

# Cada texto pausa BROAD+PHRASE daquele texto na campanha.
PAUSAR_PRODUTOS_GERAIS = ["ambu infantil", "atadura elastica", "cufômetro",
                          "luer lock", "prn", "vetrap pet"]          # QI 1, grupo Produtos Gerais
PAUSAR_MONITORAMENTO = ["cufometro", "doppler parks"]                # QI 1, grupo Monitoramento

pausar = PAUSAR_PRODUTOS_GERAIS + PAUSAR_MONITORAMENTO
print(f"  Pausando {len(pausar)} textos (BROAD+PHRASE de cada): {pausar}")
res_pause = pause_keywords_bulk(
    [{"text": t, "campaign_id": CAMP_PRODUTOS} for t in pausar], dry_run=DRY_RUN
)
show(res_pause)


# ═══════════════════════════════════════════════════════════════
# BLOCO 2 — Reativar grupo Monitoramento (as 4 do Rafael)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("BLOCO 2 — Reativar grupo Monitoramento")
print("=" * 70)

REATIVAR_MONITORAMENTO = ["monitores veterinários", "monitor veterinário portátil",
                          "doppler veterinario", "oximetro veterinario"]
print(f"  Reativando {len(REATIVAR_MONITORAMENTO)} textos (BROAD+PHRASE de cada): {REATIVAR_MONITORAMENTO}")
print("  (campanha é Maximize Conversion Value — sem ajuste de CPC, Smart Bidding decide o lance)")
res_enable = enable_keywords_bulk(
    [{"text": t, "campaign_id": CAMP_PRODUTOS} for t in REATIVAR_MONITORAMENTO], dry_run=DRY_RUN
)
show(res_enable)


# ═══════════════════════════════════════════════════════════════
# BLOCO 3 — Corrigir sitelinks reprovados
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("BLOCO 3 — Corrigir sitelinks reprovados")
print("=" * 70)

SITELINK_FIXES = [
    (352365187764, "Manguitos", ["https://www.rzvet.com.br/acessorios/manguitos-01-e-02-vias"]),
    (358199478954, "Monitores Veterinários", ["https://www.rzvet.com.br/monitores"]),
]
res_sitelinks = []
for asset_id, label, urls in SITELINK_FIXES:
    print(f"  {label} (asset {asset_id}) → {urls[0]}")
    r = update_asset_final_urls(asset_id, urls, dry_run=DRY_RUN)
    res_sitelinks.append(r)
    print(f"    - {json.dumps(r, ensure_ascii=False)}")


# ═══════════════════════════════════════════════════════════════
# VERIFICAÇÃO (só faz sentido depois do --apply)
# ═══════════════════════════════════════════════════════════════
if not DRY_RUN:
    print("\n" + "=" * 70)
    print("VERIFICAÇÃO")
    print("=" * 70)

    alvo_pause = {t.lower() for t in pausar}
    alvo_enable = {t.lower() for t in REATIVAR_MONITORAMENTO}
    rows = svc.search(customer_id=CUSTOMER_ID, query=f"""
        SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
               ad_group_criterion.status, ad_group_criterion.quality_info.quality_score
        FROM ad_group_criterion
        WHERE campaign.id = {CAMP_PRODUTOS} AND ad_group_criterion.type = 'KEYWORD'
          AND ad_group_criterion.negative = FALSE
        ORDER BY ad_group.name, ad_group_criterion.keyword.text
    """)
    print("\n  Keywords-alvo (esperado: PAUSADO no bloco 1, HABILITADO no bloco 2):")
    for r in rows:
        c = r.ad_group_criterion
        low = c.keyword.text.lower()
        if low in alvo_pause:
            tag = "BLOCO1→deveria PAUSED"
        elif low in alvo_enable:
            tag = "BLOCO2→deveria ENABLED"
        else:
            continue
        print(f"    {c.keyword.text:<32} [{c.keyword.match_type.name:<7}] status={c.status.name:<8} QI={c.quality_info.quality_score or '-'}  ({tag})")

    print("\n  Sitelinks corrigidos (esperado: final_urls novos, approval em UNDER_REVIEW → APPROVED em ~24h):")
    for asset_id, label, _ in SITELINK_FIXES:
        for r in svc.search(customer_id=CUSTOMER_ID, query=f"""
            SELECT asset.id, asset.sitelink_asset.link_text, asset.final_urls,
                   asset.policy_summary.approval_status, asset.policy_summary.review_status
            FROM asset WHERE asset.id = {asset_id}
        """):
            a = r.asset
            print(f"    {a.sitelink_asset.link_text:<26} final_urls={list(a.final_urls)} approval={a.policy_summary.approval_status.name} review={a.policy_summary.review_status.name}")

print("\n✅ Concluído." + ("" if DRY_RUN else " Verifique a saída acima."))
