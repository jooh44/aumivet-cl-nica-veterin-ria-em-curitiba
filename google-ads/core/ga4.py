import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy,
    FilterExpression,
    Filter
)

# Caminho para o arquivo JSON de credenciais
GA4_CREDENTIALS_PATH = "scrapper-470321-5c88062238a6.json"
# ID da Propriedade GA4 (será preenchido pelo usuário ou extraído do .env.ads se existir)
PROPERTY_ID = "294320922" 

def get_ga4_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GA4_CREDENTIALS_PATH
    return BetaAnalyticsDataClient()

def run_ga4_report(property_id, dimensions, metrics, start_date, end_date, dimension_filter=None):
    client = get_ga4_client()
    
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter=dimension_filter
    )
    
    return client.run_report(request)

if __name__ == "__main__":
    # Teste rápido de conexão
    try:
        response = run_ga4_report(PROPERTY_ID, ["sessionSourceMedium"], ["sessions"], "7daysAgo", "today")
        print("✅ Conexão GA4 API estabelecida com sucesso!")
        for row in response.rows:
            print(f"Origem/Mídia: {row.dimension_values[0].value} | Sessões: {row.metric_values[0].value}")
    except Exception as e:
        print(f"❌ Erro ao conectar GA4: {e}")
