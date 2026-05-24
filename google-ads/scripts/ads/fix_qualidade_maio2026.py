#!/usr/bin/env python3
"""
Fix de Qualidade — Maio 2026
Corrige:
  1. PMax "TODOS OS PRODUTOS" — adiciona business_name + headlines/desc sem termos clínicos
  2. Search RSAs — completa headlines/descriptions para reduzir "Ad Quality baixa"
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.client import get_client, CUSTOMER_ID
from google.protobuf import field_mask_pb2

DRY_RUN = "--apply" not in sys.argv
client = get_client()
CUSTOMER_ID_STR = CUSTOMER_ID

if DRY_RUN:
    print(">>> MODO DRY RUN — use --apply para aplicar de verdade\n")
else:
    print(">>> MODO APPLY — changes serão enviadas ao Google Ads\n")


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def create_text_asset(text: str, name: str) -> str:
    """Cria asset de texto e retorna resource_name."""
    service = client.get_service("AssetService")
    op = client.get_type("AssetOperation")
    asset = op.create
    asset.name = name
    asset.text_asset.text = text
    if DRY_RUN:
        return f"[dry-run] customers/{CUSTOMER_ID_STR}/assets/NEW"
    resp = service.mutate_assets(customer_id=CUSTOMER_ID_STR, operations=[op])
    return resp.results[0].resource_name


def link_text_to_pmax(asset_rn: str, asset_group_id: int, field_type: str):
    """Linka texto ao asset group PMax."""
    asset_group_rn = f"customers/{CUSTOMER_ID_STR}/assetGroups/{asset_group_id}"
    service = client.get_service("AssetGroupAssetService")
    op = client.get_type("AssetGroupAssetOperation")
    aga = op.create
    aga.asset = asset_rn
    aga.asset_group = asset_group_rn
    aga.field_type = client.enums.AssetFieldTypeEnum[field_type]
    if DRY_RUN:
        return "[dry-run] linked"
    resp = service.mutate_asset_group_assets(customer_id=CUSTOMER_ID_STR, operations=[op])
    return resp.results[0].resource_name


def add_pmax_text(asset_group_id: int, field_type: str, text: str):
    """Cria asset de texto e linka no PMax de uma vez. Ignora RESOURCE_LIMIT."""
    safe_name = text[:25].replace(" ", "_").replace("ã", "a").replace("ç", "c")
    name = f"rzvet_pmax_{field_type[:3].lower()}_{safe_name}"
    if DRY_RUN:
        print(f"   [DRY] ADD {field_type}: \"{text}\"")
        return
    try:
        rn = create_text_asset(text, name)
        link_text_to_pmax(rn, asset_group_id, field_type)
        print(f"   ✅ ADD {field_type}: \"{text}\"")
    except Exception as e:
        msg = str(e)
        if "RESOURCE_LIMIT" in msg or "limit" in msg.lower():
            print(f"   [LIMITE] {field_type} no limite — pulando: \"{text}\"")
        elif "DUPLICATE_ASSET_LINK" in msg or "duplicate" in msg.lower():
            print(f"   [DUPLICADO] Já existe — pulando: \"{text}\"")
        else:
            print(f"   [ERRO] {field_type} \"{text}\": {msg[:120]}")


def create_rsa(ad_group_id: int, final_url: str, headlines: list[dict], descriptions: list[dict], label: str):
    """Cria novo RSA em um ad group. RSA existentes são mantidos (Google faz AB test)."""
    service = client.get_service("AdGroupAdService")
    op = client.get_type("AdGroupAdOperation")
    ada = op.create
    ada.ad_group = f"customers/{CUSTOMER_ID_STR}/adGroups/{ad_group_id}"
    ada.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ada.ad.final_urls.append(final_url)

    for hl in headlines:
        h = client.get_type("AdTextAsset")
        h.text = hl["text"]
        # Não pinar nos novos RSAs — deixar Google testar combinações
        ada.ad.responsive_search_ad.headlines.append(h)

    for desc in descriptions:
        d = client.get_type("AdTextAsset")
        d.text = desc["text"]
        ada.ad.responsive_search_ad.descriptions.append(d)

    if DRY_RUN:
        print(f"   [DRY] CREATE RSA: {label} | ag={ad_group_id} | {len(headlines)} headlines | {len(descriptions)} descs")
        return

    try:
        resp = service.mutate_ad_group_ads(customer_id=CUSTOMER_ID_STR, operations=[op])
        print(f"   ✅ CREATE RSA: {label} | {len(headlines)} headlines | {len(descriptions)} descs")
    except Exception as e:
        msg = str(e)
        if "TOO_MANY_ADS" in msg or "limit" in msg.lower():
            print(f"   [LIMITE] Já tem 3 RSAs neste grupo — pulando: {label}")
        else:
            print(f"   [ERRO] {label}: {msg[:200]}")


# ══════════════════════════════════════════════════════════════
# 1. PMAX — "TODOS OS PRODUTOS" — fix policy + business name
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("1. PMAX — TODOS OS PRODUTOS — textos limpos")
print("=" * 60)

PMAX_AG_ID = 6517406311
PMAX_CAMPAIGN_ID = 21710109809

# Business name "RZvet Brasil" já está ENABLED no nível de campanha (Brand Guidelines).
# Logo e landscape logo também já estão configurados.
# Foco: adicionar textos limpos ao asset GROUP (headlines, long headlines, descriptions).
print("  [OK] Business name, logos já configurados no nível de campanha — skipping")

# Headlines novas (sem termos clínicos — "anestesia", "cirúrgico", "UTI", "material cirúrgico")
# Já existem habilitados: RZ Equipamentos Veterinários, RZ Equipamentos Vet, Doppler Veterinário,
# Plug Adaptador Veterinário, RZVET Equipamentos, Kit Manguito Vet, Equipamentos Com Manutenção,
# 11 Anos Entregando Qualidade, Produtos Com Garantia, Equipamentos Veterinários Rz, Monitores Vet Promo
print("\n  Headlines (substituem removidos):")
PMAX_NEW_HEADLINES = [
    "Compre Direto da Fábrica",     # 24 chars — comercial puro
    "Envio para Todo o Brasil",      # 24 chars
    "Parcelamento em 12x",           # 19 chars
    "Bomba de Infusão Vet",          # 20 chars
    "Monitor Multiparamétrico",      # 24 chars
    "Oxímetro Veterinário",          # 21 chars
    "Manguito Veterinário",          # 20 chars
    "Cateter Periférico Vet",        # 22 chars
    "Garantia de 12 Meses",          # 21 chars
]
for h in PMAX_NEW_HEADLINES:
    assert len(h) <= 30, f"Headline muito longa: {h} ({len(h)} chars)"
    add_pmax_text(PMAX_AG_ID, "HEADLINE", h)

# Long headlines novas
print("\n  Long Headlines (substituem removidos 'Anestesia'):")
PMAX_NEW_LONG_HEADLINES = [
    "Equipamentos Veterinários com Garantia e Suporte Técnico Especializado",   # 71 chars
    "Tudo para Sua Clínica Veterinária. Compre com a Confiança de Quem Fabrica", # 74 chars
    "Monitores, Manguitos, Cateteres e Bombas. A Linha Completa da RZVet",      # 68 chars
]
for lh in PMAX_NEW_LONG_HEADLINES:
    assert len(lh) <= 90, f"Long headline muito longa: {lh} ({len(lh)} chars)"
    add_pmax_text(PMAX_AG_ID, "LONG_HEADLINE", lh)

# Descriptions novas (substituem as removidas com "Cirúrgico", "UTI", "Dissecação")
print("\n  Descriptions (substituem removidas):")
PMAX_NEW_DESCRIPTIONS = [
    "Linha completa de equipamentos veterinários. Compre direto da fábrica com garantia e suporte.",   # 92 — ops too long
    "Monitores, manguitos, cateteres e bombas. Frete para todo o Brasil e parcele em até 12x.",       # 89 chars ✅
    "Peças originais e assistência técnica própria. Tecnologia RZVet com 11 anos de experiência.",     # 90 chars ✅
    "Estoque disponível e envio imediato. Qualidade de fabricante com o melhor custo-benefício.",      # 89 chars ✅
]
# Verificar tamanhos
for desc in PMAX_NEW_DESCRIPTIONS:
    if len(desc) <= 90:
        add_pmax_text(PMAX_AG_ID, "DESCRIPTION", desc)
    else:
        print(f"   [SKIP] Desc muito longa ({len(desc)} chars): {desc[:40]}...")


# ══════════════════════════════════════════════════════════════
# 2. SEARCH RSAs — buscar resource names e atualizar
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("2. SEARCH — RSA Ads — completando headlines/descriptions")
print("=" * 60)

gaql_rsa = """
    SELECT
        campaign.name,
        campaign.id,
        ad_group.name,
        ad_group.id,
        ad_group_ad.resource_name,
        ad_group_ad.ad.id,
        ad_group_ad.ad.type,
        ad_group_ad.ad.final_urls,
        ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions,
        ad_group_ad.ad_strength
    FROM ad_group_ad
    WHERE ad_group_ad.status != 'REMOVED'
      AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
      AND campaign.id IN (23366014954, 23362032632, 23361821714)
    ORDER BY campaign.name, ad_group.name
"""
gaql_service = client.get_service("GoogleAdsService")
rsa_rows = list(gaql_service.search(customer_id=CUSTOMER_ID_STR, query=gaql_rsa))

def extract_rsa(row):
    hs = [{"text": h.text, "pinned": h.pinned_field.name if h.pinned_field else None}
          for h in row.ad_group_ad.ad.responsive_search_ad.headlines]
    ds = [{"text": d.text, "pinned": d.pinned_field.name if d.pinned_field else None}
          for d in row.ad_group_ad.ad.responsive_search_ad.descriptions]
    return {
        "campaign": row.campaign.name,
        "campaign_id": row.campaign.id,
        "ad_group": row.ad_group.name,
        "ad_group_id": row.ad_group.id,
        "ad_id": row.ad_group_ad.ad.id,
        "rn": row.ad_group_ad.resource_name,
        "strength": row.ad_group_ad.ad_strength.name,
        "final_url": list(row.ad_group_ad.ad.final_urls)[0] if row.ad_group_ad.ad.final_urls else "https://rzvet.com.br",
        "headlines": hs,
        "descriptions": ds,
    }

rsa_ads = [extract_rsa(r) for r in rsa_rows]
print(f"\n  Encontrados {len(rsa_ads)} RSA ads nas campanhas ativas")

# Agrupar por (campaign, ad_group) para saber quantos RSAs existem em cada grupo
from collections import defaultdict
rsa_by_group = defaultdict(list)
for ad in rsa_ads:
    rsa_by_group[(ad["campaign"], ad["ad_group"])].append(ad)


# ── Helper: merge headlines (sem duplicar, respeita limite 15 + 4) ─────────
def merge_headlines(existing: list[dict], new_texts: list[str], max_count: int = 15) -> list[dict]:
    existing_texts = {h["text"].lower() for h in existing}
    result = list(existing)
    for t in new_texts:
        if len(result) >= max_count:
            break
        if t.lower() not in existing_texts:
            result.append({"text": t, "pinned": None})
            existing_texts.add(t.lower())
    return result


def merge_descriptions(existing: list[dict], new_texts: list[str], max_count: int = 4) -> list[dict]:
    existing_texts = {d["text"].lower() for d in existing}
    result = list(existing[:max_count])  # garante que não passa do limite mesmo com muitos existentes
    for t in new_texts:
        if len(result) >= max_count:
            break
        if t.lower() not in existing_texts:
            result.append({"text": t, "pinned": None})
            existing_texts.add(t.lower())
    return result


# ══════════════════════════════════════════════════════════════
# NOVOS CONTEÚDOS POR CAMPANHA / AD GROUP
# ══════════════════════════════════════════════════════════════

# Conteúdo genérico RZVet (reutilizável)
COMMON_HL = [
    "Compre Direto da Fábrica",
    "Frete para Todo o Brasil",
    "Parcelamento em 12x",
    "Garantia de Fábrica",
    "Suporte Técnico Incluso",
    "11 Anos de Experiência",
    "Envio Imediato",
    "Peças Originais RZVet",
    "Qualidade de Fabricante",
]
COMMON_DESC = [
    "Compre com garantia de fábrica e suporte técnico especializado. Entrega para todo o Brasil.",
    "11 anos entregando qualidade. Parcele em até 12x sem juros e receba com rapidez.",
]

# Por ad group — novos headlines específicos
NEW_CONTENT = {
    # ── [Search] RZVet - Concorrentes ──────────────────────────
    ("[Search] RZVet - Concorrentes", "Grupo de anúncios 1"): {
        "hl": [
            "Monitor Multiparamétrico",
            "Bomba de Infusão Veterinária",
            "Doppler Veterinário",
            "Oxímetro Veterinário",
            "Frete para Todo o Brasil",
            "Parcelamento em 12x",
            "Suporte Técnico Incluso",
            "11 Anos de Experiência",
        ],
        "desc": [
            "Compare e descubra por que veterinários de todo o Brasil escolhem a RZVet.",
            "Garantia de fábrica, suporte técnico e as melhores condições de pagamento.",
        ],
    },
    # ── [Search] RZVet - Institucional ─────────────────────────
    ("[Search] RZVet - Institucional", "Grupo de anúncios 1"): {
        "hl": [
            "Frete para Todo o Brasil",
            "Parcelamento em 12x",
            "Equipamentos Certificados",
            "Monitores Veterinários",
            "Manguitos Veterinários",
            "Cateteres e Insumos",
            "Produtos para Clínica",
            "11 Anos no Mercado",
            "Qualidade de Fabricante",
        ],
        "desc": [
            "Tudo para sua clínica em um só lugar. Frete para todo o Brasil e parcele em 12x.",
            "Assistência técnica própria e peças originais. 11 anos de tradição no mercado vet.",
        ],
    },
    # ── [Search] RZVet - Produtos — Ad Groups ──────────────────
    ("[Search] RZVet - Produtos", "Anestesia e Respiratório"): {
        "hl": [
            "Tubo T de Bain Veterinário",
            "Circuito Mapleson Vet",
            "Filtro HME Veterinário",
            "Cal Sodada Veterinária",
            "Capnógrafo Veterinário",
            "Ressuscitador Ambu Vet",
            "Compre Direto da Fábrica",
            "Frete para Todo o Brasil",
        ],
        "desc": [
            "Frete para todo o Brasil e parcelamento em 12x. Estoque disponível com envio imediato.",
        ],
    },
    ("[Search] RZVet - Produtos", "Cateteres e Acesso"): {
        "hl": [
            "Cateter 22g Veterinário",
            "Cateter 18g Veterinário",
            "Cateter 24g Neonatal",
            "Acesso Venoso Seguro",
            "Cateter Umbilical Vet",
            "Equipo de Soro Vet",
            "Compre Direto da Fábrica",
            "Frete para Todo o Brasil",
        ],
        "desc": [
            "Frete para todo o Brasil e parcelamento em 12x. Estoque disponível com envio imediato.",
        ],
    },
    ("[Search] RZVet - Produtos", "Colar Elizabetano"): {
        "hl": [
            "Colar Elizabetano Cão",
            "Colar Elizabetano Gato",
            "Colar Protetor Pet",
            "Colar Elizabetano Inflável",
            "Proteção Pós-Operatória",
            "Tamanhos PP ao GG",
            "Compre Direto da Fábrica",
            "Frete para Todo o Brasil",
            "Garantia de Qualidade RZ",
            "Entrega Rápida",
        ],
        "desc": [
            "Colares em vários tamanhos para cães, gatos e aves. Envio rápido para todo o Brasil.",
            "Compre direto da fábrica RZVet com garantia de qualidade e as melhores condições.",
        ],
    },
    ("[Search] RZVet - Produtos", "Insumos Diversos"): {
        "hl": [
            "Agulha Espinhal Vet",
            "Extensor Pediátrico",
            "Seringa de Insulina Vet",
            "Kit Insumos Veterinário",
            "Insumos para Clínica",
            "Compre Direto da Fábrica",
            "Frete para Todo o Brasil",
            "Garantia de Fábrica",
        ],
        "desc": [
            "Frete para todo o Brasil e parcelamento em 12x. Estoque disponível com envio imediato.",
            "Compre direto da fábrica RZVet com garantia e suporte técnico especializado.",
        ],
    },
    ("[Search] RZVet - Produtos", "Manguitos"): {
        "hl": [
            "Manguito Neonatal Vet",
            "Manguito 1 Via Silicone",
            "Manguito 3 Vias Silicone",
            "Manguito 5 Vias Silicone",
            "Kit Manguito Completo",
            "Pressão Arterial Vet",
            "NIBP Veterinário",
            "Aferição de Alta Precisão",
            "Compre Direto da Fábrica",
            "Frete para Todo o Brasil",
            "Garantia de Fábrica",
        ],
        "desc": [
            "Kits de 1 a 5 vias em silicone de alta durabilidade. Neonatal ao gigante. Compre na RZ.",
            "Compatível com monitores RZ e outras marcas. Garantia direta de fabricante.",
        ],
    },
    ("[Search] RZVet - Produtos", "Monitoramento"): {
        # Já tem 15 headlines — só trocar os genéricos por keywords melhores
        # Mantemos todos os 15 existentes, Google vai rodar A/B
        "hl": [],
        "desc": [
            "Frete para todo o Brasil e parcelamento em 12x. Estoque disponível com envio imediato.",
        ],
    },
    ("[Search] RZVet - Produtos", "Produtos Gerais"): {
        "hl": [
            "Cal Sodada Veterinária",
            "Vetrap Bandagem Coesa",
            "Kits de Dissecção Vet",
            "Caixas Cirúrgicas Completas",
            "Compre Direto da Fábrica",
            "Frete para Todo o Brasil",
            "Aluguel de Equipamentos",
        ],
        "desc": [
            "Frete para todo o Brasil e parcelamento em 12x. Estoque disponível com envio imediato.",
        ],
    },
}


# ══════════════════════════════════════════════════════════════
# APLICAR UPDATES NOS RSAs
# ══════════════════════════════════════════════════════════════
print()
# Processar um CREATE por ad group (pegar o melhor ad group ref para URL/path)
processed_groups = set()

for ad in rsa_ads:
    key = (ad["campaign"], ad["ad_group"])
    if key in processed_groups:
        continue  # já criamos RSA para este grupo

    content = NEW_CONTENT.get(key)
    if content is None:
        print(f"  [SKIP] Sem conteúdo para: {ad['campaign']} / {ad['ad_group']}")
        continue

    # Pegar todos os ads do grupo para consolidar headlines únicas existentes
    group_ads = rsa_by_group[key]
    all_existing_hl: list[dict] = []
    all_existing_desc: list[dict] = []
    seen_hl_texts: set = set()
    seen_desc_texts: set = set()
    for g_ad in group_ads:
        for h in g_ad["headlines"]:
            if h["text"].lower() not in seen_hl_texts:
                all_existing_hl.append({"text": h["text"], "pinned": None})
                seen_hl_texts.add(h["text"].lower())
        for d in g_ad["descriptions"]:
            if d["text"].lower() not in seen_desc_texts:
                all_existing_desc.append({"text": d["text"], "pinned": None})
                seen_desc_texts.add(d["text"].lower())

    new_hl = merge_headlines(all_existing_hl, content["hl"], max_count=15)
    new_desc = merge_descriptions(all_existing_desc, content["desc"], max_count=4)

    n_existing = len(group_ads)
    print(f"\n  Campanha: {ad['campaign']}")
    print(f"  Ad Group: {ad['ad_group']} | RSAs existentes: {n_existing} | URL: {ad['final_url']}")
    print(f"  Headlines: {len(all_existing_hl)} únicos → novo RSA com {len(new_hl)}")
    print(f"  Descriptions: {len(all_existing_desc)} únicos → novo RSA com {len(new_desc)}")

    create_rsa(ad["ad_group_id"], ad["final_url"], new_hl, new_desc,
               f"{ad['ad_group']} (novo RSA)")

    processed_groups.add(key)

print("\n" + "=" * 60)
if DRY_RUN:
    print("DRY RUN concluído. Rode com --apply para aplicar.")
else:
    print("✅ Todas as correções aplicadas.")
print("=" * 60)
