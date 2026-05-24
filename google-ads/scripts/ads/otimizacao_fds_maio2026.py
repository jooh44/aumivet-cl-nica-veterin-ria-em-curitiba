#!/usr/bin/env python3
"""
Otimização FDS Maio 2026 — RZVet
Executa com dry_run=True por padrão. Passe --apply para efetivar.

Mudanças:
  1. Conversões primárias incorretas → secundárias (5 ações)
  2. Pausar esfigmomanômetro (3 keywords, IQ 0-1)
  3. Reativar equipamentos veterinários (2 keywords, IQ 8)
  4. Negativos de concorrentes na campanha Produtos
"""
import sys
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..'))

from core.client import get_client, CUSTOMER_ID
from google.protobuf import field_mask_pb2

DRY_RUN = "--apply" not in sys.argv
client = get_client()

if DRY_RUN:
    print("\n🔍 DRY-RUN — nenhuma mudança será aplicada. Use --apply para efetivar.\n")
else:
    print("\n🚀 APLICANDO MUDANÇAS...\n")

results = []


# ═══════════════════════════════════════════════════════════════
# 1. CONVERSÕES PRIMÁRIAS INCORRETAS → SECUNDÁRIAS
# ═══════════════════════════════════════════════════════════════
print("=" * 60)
print("1. CONVERSÕES — demovendo primárias incorretas")
print("=" * 60)

CONVERSOES_PARA_SECUNDARIA = [
    (481539521, "Local actions - Directions"),
    (501347432, "Local actions - Website visits"),
    (512639890, "Local actions - Other engagements"),
    (949442292, "Store visits"),
    (791021910, "Android installs (all other apps)"),
]

if not DRY_RUN:
    conv_service = client.get_service("ConversionActionService")

for conv_id, conv_name in CONVERSOES_PARA_SECUNDARIA:
    rn = f"customers/{CUSTOMER_ID}/conversionActions/{conv_id}"
    if DRY_RUN:
        print(f"  [DRY] {conv_name} → secundária")
        results.append({"acao": "conv_secundaria", "nome": conv_name, "status": "dry_run"})
    else:
        op = client.get_type("ConversionActionOperation")
        op.update.resource_name = rn
        op.update.primary_for_goal = False
        client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["primary_for_goal"]))
        try:
            conv_service.mutate_conversion_actions(customer_id=CUSTOMER_ID, operations=[op])
            print(f"  ✅ {conv_name} → secundária")
            results.append({"acao": "conv_secundaria", "nome": conv_name, "status": "ok"})
        except Exception as e:
            print(f"  ❌ {conv_name}: {e}")
            results.append({"acao": "conv_secundaria", "nome": conv_name, "status": "erro", "detalhe": str(e)})


# ═══════════════════════════════════════════════════════════════
# 2. PAUSAR KEYWORDS RUINS — esfigmomanômetro
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("2. PAUSAR — esfigmomanômetro (IQ 0-1, sem relevância vet)")
print("=" * 60)

PAUSAR_KEYWORDS = [
    # (resource_name, descricao)
    ("customers/2419898793/adGroupCriteria/189770626483~668047433",       "esfigmomanômetro BROAD IQ1"),
    ("customers/2419898793/adGroupCriteria/189770626483~10989586969",     "esfigmomanômetro PHRASE IQ1"),
    ("customers/2419898793/adGroupCriteria/189770626483~2456494665978",   "esfigmomanômetro 1 via PHRASE IQ0"),
]

if not DRY_RUN:
    kw_service = client.get_service("AdGroupCriterionService")

for rn, desc in PAUSAR_KEYWORDS:
    if DRY_RUN:
        print(f"  [DRY] PAUSAR: {desc}")
        results.append({"acao": "pausar_kw", "keyword": desc, "status": "dry_run"})
    else:
        op = client.get_type("AdGroupCriterionOperation")
        op.update.resource_name = rn
        op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
        client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["status"]))
        try:
            kw_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=[op])
            print(f"  ✅ PAUSADO: {desc}")
            results.append({"acao": "pausar_kw", "keyword": desc, "status": "ok"})
        except Exception as e:
            print(f"  ❌ {desc}: {e}")
            results.append({"acao": "pausar_kw", "keyword": desc, "status": "erro", "detalhe": str(e)})


# ═══════════════════════════════════════════════════════════════
# 3. REATIVAR KEYWORDS BOAS — equipamentos veterinários IQ 8
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("3. REATIVAR — equipamentos veterinários (IQ 8, pausada sem motivo)")
print("=" * 60)

ATIVAR_KEYWORDS = [
    ("customers/2419898793/adGroupCriteria/189770626483~1713085609",   "equipamentos veterinários BROAD IQ8"),
    ("customers/2419898793/adGroupCriteria/189770626483~308595288708", "equipamentos veterinários PHRASE IQ8"),
]

for rn, desc in ATIVAR_KEYWORDS:
    if DRY_RUN:
        print(f"  [DRY] ATIVAR: {desc}")
        results.append({"acao": "ativar_kw", "keyword": desc, "status": "dry_run"})
    else:
        op = client.get_type("AdGroupCriterionOperation")
        op.update.resource_name = rn
        op.update.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["status"]))
        try:
            kw_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=[op])
            print(f"  ✅ ATIVADO: {desc}")
            results.append({"acao": "ativar_kw", "keyword": desc, "status": "ok"})
        except Exception as e:
            print(f"  ❌ {desc}: {e}")
            results.append({"acao": "ativar_kw", "keyword": desc, "status": "erro", "detalhe": str(e)})


# ═══════════════════════════════════════════════════════════════
# 4. NEGATIVOS DE CONCORRENTES — campanha Produtos (Search)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("4. NEGATIVOS — concorrentes na campanha [Search] RZVet - Produtos")
print("=" * 60)

CAMP_PRODUTOS_ID = 23361821714

# Termos de concorrentes vistos nos search terms + marcas que não queremos pagar
NEGATIVOS_CONCORRENTES = [
    "delta life",
    "doppler delta life",
    "tradevet",
    "brasmed",
    "doppler parks",
    "parks medical",
    "medmega",
    "doppler medmega",
    "ecco vet",
    "vet acess",
]

# Termos sem intenção de compra
NEGATIVOS_INTENT = [
    "aluguel",
    "emprestimo",
    "conserto",
    "reparo",
    "manutenção",
    "segunda mão",
    "usado",
    "semi novo",
    "curso",
    "apostila",
    "como usar",
    "humano",               # esfigmomanômetro humano etc
]

TODOS_NEGATIVOS = NEGATIVOS_CONCORRENTES + NEGATIVOS_INTENT

if DRY_RUN:
    for neg in TODOS_NEGATIVOS:
        print(f"  [DRY] NEGATIVO PHRASE: \"{neg}\"")
    results.append({"acao": "negativos", "count": len(TODOS_NEGATIVOS), "status": "dry_run"})
else:
    camp_criterion_service = client.get_service("CampaignCriterionService")
    operations = []
    for neg in TODOS_NEGATIVOS:
        op = client.get_type("CampaignCriterionOperation")
        c = op.create
        c.campaign = f"customers/{CUSTOMER_ID}/campaigns/{CAMP_PRODUTOS_ID}"
        c.negative = True
        c.keyword.text = neg
        c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        operations.append(op)
    try:
        resp = camp_criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=operations)
        for neg, r in zip(TODOS_NEGATIVOS, resp.results):
            print(f"  ✅ NEGATIVO: \"{neg}\"")
        results.append({"acao": "negativos", "count": len(TODOS_NEGATIVOS), "status": "ok"})
    except Exception as e:
        print(f"  ❌ Erro ao adicionar negativos: {e}")
        results.append({"acao": "negativos", "status": "erro", "detalhe": str(e)})


# ═══════════════════════════════════════════════════════════════
# RESUMO
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
if DRY_RUN:
    print("DRY-RUN CONCLUÍDO — rode com --apply para efetivar")
    print(f"\nTotal de operações planejadas: {len([r for r in results if r['status'] == 'dry_run'])}")
    print("\nContexto FDS + Pagamento:")
    print("  • Fds = volume levemente menor, mas intenção de compra mantida")
    print("  • Pagamento recente = poder de compra alto, especialmente para")
    print("    clínicas que receberam e estão pensando em equipar")
    print("  • Manter budgets como estão, não cortar")
    print("  • As reativações de 'equipamentos veterinários' IQ8 chegam")
    print("    num momento de demanda real — boa timing")
else:
    ok = sum(1 for r in results if r["status"] == "ok")
    erros = sum(1 for r in results if r["status"] == "erro")
    print(f"CONCLUÍDO — ✅ {ok} OK | ❌ {erros} erros")
print("=" * 60)
