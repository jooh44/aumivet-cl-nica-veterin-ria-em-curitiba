#!/usr/bin/env python3
"""
Adiciona sitelinks com URLs de categoria e descrições nas campanhas Search ativas.
Campanhas: [Search] RZVet - Produtos, Concorrentes, Institucional
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.client import get_client, CUSTOMER_ID

DRY_RUN = "--apply" not in sys.argv
client = get_client()

if DRY_RUN:
    print(">>> DRY RUN — use --apply para aplicar\n")
else:
    print(">>> APPLY MODE\n")

CAMPAIGN_IDS = {
    "[Search] RZVet - Produtos":      23361821714,
    "[Search] RZVet - Concorrentes":  23366014954,
    "[Search] RZVet - Institucional": 23362032632,
}

# Sitelinks a criar: (link_text, desc1, desc2, url)
# link_text ≤ 25 | desc1 ≤ 35 | desc2 ≤ 35
NEW_SITELINKS = [
    (
        "Monitores Veterinários",
        "RM700 e RM1200 com capnografia",
        "Suporte técnico incluso",
    ),
    (
        "Bombas de Infusão",
        "Equipo, seringa e TCI",
        "Tecnologia nacional RZVet",
    ),
    (
        "Manguitos Silicone",
        "1 a 5 vias, neonatal a gigante",
        "Compatível com vários monitores",
    ),
    (
        "Doppler Veterinário",
        "Pressão arterial de alta precisão",
        "Direto da fábrica RZVet",
    ),
    (
        "Cateter Venoso",
        "Central, peridural e periférico",
        "Estoque disponível para envio",
    ),
    (
        "Peças de Reposição",
        "Originais para monitores RZ",
        "Entrega para todo o Brasil",
    ),
]

# Validar tamanhos
for lt, d1, d2 in NEW_SITELINKS:
    assert len(lt) <= 25, f"link_text muito longo: {lt!r} ({len(lt)})"
    assert len(d1) <= 35, f"desc1 muito longa: {d1!r} ({len(d1)})"
    assert len(d2) <= 35, f"desc2 muito longa: {d2!r} ({len(d2)})"

print(f"Sitelinks planejados: {len(NEW_SITELINKS)}")
for lt, d1, d2 in NEW_SITELINKS:
    print(f"  [{len(lt):2}] {lt!r:25} | {d1}")

if DRY_RUN:
    print("\n[DRY] Nenhuma chamada de API feita.")
    print("Rode com --apply para criar e vincular.")
    sys.exit(0)

# ── Criar assets + linkar em cada campanha ───────────────────────────────────
asset_service = client.get_service("AssetService")
campaign_asset_service = client.get_service("CampaignAssetService")

print()
for link_text, desc1, desc2 in NEW_SITELINKS:
    # 1. Criar o asset de sitelink
    op = client.get_type("AssetOperation")
    safe = link_text.lower().replace(" ", "_")[:20]
    op.create.name = f"rzvet_sl_{safe}"
    op.create.final_urls.append("https://rzvet.com.br")
    op.create.sitelink_asset.link_text = link_text
    op.create.sitelink_asset.description1 = desc1
    op.create.sitelink_asset.description2 = desc2

    try:
        resp = asset_service.mutate_assets(customer_id=CUSTOMER_ID, operations=[op])
        asset_rn = resp.results[0].resource_name
        print(f"  ✅ Asset criado: {link_text!r} → {asset_rn}")
    except Exception as e:
        print(f"  [ERRO] criando asset {link_text!r}: {str(e)[:150]}")
        continue

    # 2. Linkar em cada campanha
    ca_ops = []
    for camp_name, camp_id in CAMPAIGN_IDS.items():
        ca_op = client.get_type("CampaignAssetOperation")
        ca_op.create.asset = asset_rn
        ca_op.create.campaign = f"customers/{CUSTOMER_ID}/campaigns/{camp_id}"
        ca_op.create.field_type = client.enums.AssetFieldTypeEnum.SITELINK
        ca_ops.append(ca_op)

    try:
        campaign_asset_service.mutate_campaign_assets(
            customer_id=CUSTOMER_ID, operations=ca_ops
        )
        print(f"       Vinculado em {len(CAMPAIGN_IDS)} campanhas ✅")
    except Exception as e:
        print(f"  [ERRO] vinculando {link_text!r}: {str(e)[:150]}")

print("\n" + "=" * 50)
print("Sitelinks criados e vinculados." if not DRY_RUN else "DRY RUN.")
print("=" * 50)
