#!/usr/bin/env python3
"""Create the paused Aumivet Search campaign for surgery acquisition.

Default is dry-run. Use --apply only after the landing URLs and conversion
goal setup have been checked in the live account.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.client import CUSTOMER_ID, get_client


CURITIBA_GEO_TARGET = "geoTargetConstants/1001634"
PORTUGUESE_LANGUAGE = "languageConstants/1014"


@dataclass(frozen=True)
class AdGroupPlan:
    name: str
    final_url: str
    headlines: list[str]
    descriptions: list[str]
    keywords: list[tuple[str, str]]


AD_GROUPS = [
    AdGroupPlan(
        name="Cirurgia Geral",
        final_url="https://www.aumivet.com.br/",
        headlines=[
            "Cirurgia Vet em Curitiba",
            "Aumivet Reboucas",
            "Clinica Veterinaria",
            "Agende Pelo WhatsApp",
            "Castracao e Cirurgias",
            "Centro Cirurgico Seguro",
            "Equipe Veterinaria",
            "Petlove Saude Aceito",
            "Fale Com a Aumivet",
            "Cuidado Para Caes e Gatos",
        ],
        descriptions=[
            "Cirurgias veterinarias com equipe experiente no Reboucas. Agende pelo WhatsApp.",
            "Castracao, tumores, piometra e procedimentos com cuidado anestesico.",
            "Aumivet em Curitiba: atendimento acolhedor, estrutura clinica e contato rapido.",
        ],
        keywords=[
            ("cirurgia veterinaria curitiba", "PHRASE"),
            ("cirurgia veterinaria em curitiba", "EXACT"),
            ("castracao cachorro curitiba", "PHRASE"),
            ("castracao gato curitiba", "PHRASE"),
            ("remocao tumor cachorro curitiba", "PHRASE"),
            ("piometra cachorro curitiba", "PHRASE"),
            ("cesariana cadela curitiba", "PHRASE"),
            ("clinica veterinaria cirurgia curitiba", "PHRASE"),
        ],
    ),
    AdGroupPlan(
        name="Catarata Petlove",
        final_url="https://www.aumivet.com.br/",
        headlines=[
            "Catarata Petlove PR",
            "Cirurgia de Catarata",
            "Aumivet em Curitiba",
            "Clinica Credenciada",
            "Petlove Saude",
            "Olhos do Seu Pet",
            "Avaliacao Veterinaria",
            "Agende Pelo WhatsApp",
            "Especialistas Aumivet",
            "Reboucas Curitiba",
        ],
        descriptions=[
            "Aumivet e credenciada Petlove Saude para cirurgia de catarata no Parana.",
            "Avaliacao, orientacao e encaminhamento para tutores Petlove em Curitiba.",
            "Converse com a equipe da Aumivet e veja os proximos passos pelo WhatsApp.",
        ],
        keywords=[
            ("cirurgia catarata cachorro", "PHRASE"),
            ("cirurgia catarata cachorro curitiba", "EXACT"),
            ("catarata em cachorro", "PHRASE"),
            ("oftalmologista veterinario curitiba", "PHRASE"),
            ("cirurgia catarata petlove", "PHRASE"),
            ("catarata cachorro plano de saude", "PHRASE"),
        ],
    ),
    AdGroupPlan(
        name="Odontologia Veterinaria",
        final_url="https://www.aumivet.com.br/",
        headlines=[
            "Odontologia Veterinaria",
            "Limpeza Dental Pet",
            "Extracao Dentaria",
            "Aumivet Curitiba",
            "Clinica no Reboucas",
            "Agende Pelo WhatsApp",
            "Saude Bucal Pet",
            "Petlove Saude Aceito",
            "Cuidado Para Caes e Gatos",
            "Equipe Veterinaria",
        ],
        descriptions=[
            "Odontologia veterinaria em Curitiba com avaliacao, limpeza e orientacao.",
            "Cuide da saude bucal do seu pet na Aumivet. Agende pelo WhatsApp.",
            "Atendimento no Reboucas para caes e gatos, com estrutura clinica completa.",
        ],
        keywords=[
            ("limpeza dental cachorro curitiba", "PHRASE"),
            ("odontologia veterinaria curitiba", "PHRASE"),
            ("extracao dente cachorro curitiba", "PHRASE"),
            ("tartaro cachorro curitiba", "PHRASE"),
            ("dentista veterinario curitiba", "PHRASE"),
        ],
    ),
]

NEGATIVE_KEYWORDS = [
    "gratis",
    "gratuito",
    "curso",
    "faculdade",
    "concurso",
    "ufpr",
    "puc",
    "publico",
    "municipal",
    "hospital publico",
    "ong",
    "estagio",
    "emprego",
    "trabalhe conosco",
    "baixo custo",
    "barato",
    "voluntario",
    "adocao",
    "adoção",
    "banho e tosa",
    "tosa",
    "pet shop",
    "racao",
    "ração",
    "hotel",
    "creche",
    "domicilio",
    "24 horas",
    "ortopedia",
    "ortopedico",
    "fratura",
    "joelho",
    "tplo",
    "ruptura ligamento",
    "colombo",
    "pinhais",
    "campo largo",
    "fazenda rio grande",
]


def validate_text_lengths() -> None:
    for ad_group in AD_GROUPS:
        for headline in ad_group.headlines:
            if len(headline) > 30:
                raise ValueError(f"Headline too long ({len(headline)}): {headline}")
        for description in ad_group.descriptions:
            if len(description) > 90:
                raise ValueError(f"Description too long ({len(description)}): {description}")


def print_plan(args: argparse.Namespace) -> None:
    print("Aumivet Search campaign plan")
    print(f"customer_id={CUSTOMER_ID}")
    print(f"campaign_name={args.name}")
    print(f"status=PAUSED")
    print(f"budget=R${args.budget:.2f}/day")
    print(f"default_cpc=R${args.cpc:.2f}")
    print(f"location={CURITIBA_GEO_TARGET} (Curitiba)")
    print(f"language={PORTUGUESE_LANGUAGE} (Portuguese)")
    for ad_group in AD_GROUPS:
        print(f"\n- {ad_group.name}")
        print(f"  final_url={ad_group.final_url}")
        print(f"  headlines={len(ad_group.headlines)} descriptions={len(ad_group.descriptions)} keywords={len(ad_group.keywords)}")
    print(f"\nnegative_keywords={len(NEGATIVE_KEYWORDS)}")


def create_campaign(args: argparse.Namespace) -> None:
    validate_text_lengths()
    print_plan(args)

    if not args.apply:
        print("\nDRY RUN only. Re-run with --apply to create the paused campaign.")
        return

    client = get_client()
    budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")
    criterion_service = client.get_service("CampaignCriterionService")
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_ad_service = client.get_service("AdGroupAdService")

    budget_op = client.get_type("CampaignBudgetOperation")
    budget = budget_op.create
    budget.name = f"{args.name} budget"
    budget.amount_micros = int(args.budget * 1_000_000)
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    budget.period = client.enums.BudgetPeriodEnum.DAILY
    budget.explicitly_shared = False
    budget_response = budget_service.mutate_campaign_budgets(
        customer_id=CUSTOMER_ID,
        operations=[budget_op],
    )
    budget_resource = budget_response.results[0].resource_name
    print(f"\nCreated budget: {budget_resource}")

    campaign_op = client.get_type("CampaignOperation")
    campaign = campaign_op.create
    campaign.name = args.name
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    campaign.campaign_budget = budget_resource
    campaign.manual_cpc.enhanced_cpc_enabled = False
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = False
    campaign.network_settings.target_content_network = False
    campaign.network_settings.target_partner_search_network = False
    campaign.geo_target_type_setting.positive_geo_target_type = client.enums.PositiveGeoTargetTypeEnum.PRESENCE
    campaign.geo_target_type_setting.negative_geo_target_type = client.enums.NegativeGeoTargetTypeEnum.PRESENCE
    campaign.contains_eu_political_advertising = (
        client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    )
    campaign_response = campaign_service.mutate_campaigns(
        customer_id=CUSTOMER_ID,
        operations=[campaign_op],
    )
    campaign_resource = campaign_response.results[0].resource_name
    campaign_id = campaign_resource.rsplit("/", 1)[-1]
    print(f"Created paused campaign: {campaign_resource}")

    criterion_ops = []
    for resource in (CURITIBA_GEO_TARGET, PORTUGUESE_LANGUAGE):
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = campaign_resource
        if resource.startswith("geoTargetConstants"):
            criterion.location.geo_target_constant = resource
        else:
            criterion.language.language_constant = resource
        criterion_ops.append(op)
    for keyword in NEGATIVE_KEYWORDS:
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = campaign_resource
        criterion.negative = True
        criterion.keyword.text = keyword
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        criterion_ops.append(op)
    criterion_service.mutate_campaign_criteria(
        customer_id=CUSTOMER_ID,
        operations=criterion_ops,
    )
    print(f"Added targeting and negatives: {len(criterion_ops)} criteria")

    for plan in AD_GROUPS:
        ag_op = client.get_type("AdGroupOperation")
        ad_group = ag_op.create
        ad_group.name = plan.name
        ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
        ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ad_group.campaign = campaign_resource
        ad_group.cpc_bid_micros = int(args.cpc * 1_000_000)
        ag_response = ad_group_service.mutate_ad_groups(
            customer_id=CUSTOMER_ID,
            operations=[ag_op],
        )
        ad_group_resource = ag_response.results[0].resource_name
        print(f"Created ad group: {ad_group_resource} ({plan.name})")

        keyword_ops = []
        for text, match_type in plan.keywords:
            op = client.get_type("AdGroupCriterionOperation")
            criterion = op.create
            criterion.ad_group = ad_group_resource
            criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            criterion.keyword.text = text
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum[match_type]
            keyword_ops.append(op)
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=CUSTOMER_ID,
            operations=keyword_ops,
        )
        print(f"  Added keywords: {len(keyword_ops)}")

        ad_op = client.get_type("AdGroupAdOperation")
        ad_group_ad = ad_op.create
        ad_group_ad.ad_group = ad_group_resource
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        ad_group_ad.ad.final_urls.append(plan.final_url)
        for headline in plan.headlines:
            text_asset = client.get_type("AdTextAsset")
            text_asset.text = headline
            ad_group_ad.ad.responsive_search_ad.headlines.append(text_asset)
        for description in plan.descriptions:
            text_asset = client.get_type("AdTextAsset")
            text_asset.text = description
            ad_group_ad.ad.responsive_search_ad.descriptions.append(text_asset)
        ad_group_ad_service.mutate_ad_group_ads(
            customer_id=CUSTOMER_ID,
            operations=[ad_op],
        )
        print("  Added RSA: 1")

    print(f"\nDone. Campaign remains PAUSED: {campaign_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Create the campaign in Google Ads. It remains PAUSED.")
    parser.add_argument("--name", default="Search | Cirurgias Curitiba | Aumivet | 2026-05")
    parser.add_argument("--budget", type=float, default=16.50)
    parser.add_argument("--cpc", type=float, default=2.50)
    args = parser.parse_args()
    create_campaign(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
