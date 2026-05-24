import os
from google.ads.googleads.client import GoogleAdsClient

_client = None
_env = {}

# Carrega as variáveis do .env.ads ao importar o módulo
env_path = os.path.join(os.path.dirname(__file__), '..', '.env.ads')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                _env[k.strip()] = v.strip()

def get_client() -> GoogleAdsClient:
    global _client
    if _client is not None:
        return _client

    client_config = {
        "developer_token": _env.get("DEVELOPER_TOKEN", ""),
        "client_id": _env.get("CLIENT_ID", ""),
        "client_secret": _env.get("CLIENT_SECRET", ""),
        "refresh_token": _env.get("REFRESH_TOKEN", ""),
        "use_proto_plus": True,
    }

    # Só envia o login_customer_id se estivermos gerenciando a conta sob a MCC da RZ Vet
    # e o CUSTOMER_ID selecionado for o da RZ Vet (2419898793).
    # Caso contrário, omitimos para permitir acesso direto a outras contas (como Aumivet e Avipec).
    selected_customer = _env.get("CUSTOMER_ID", "").replace("-", "")
    if selected_customer == "2419898793" and _env.get("MANAGER_CUSTOMER_ID"):
        client_config["login_customer_id"] = _env.get("MANAGER_CUSTOMER_ID")

    _client = GoogleAdsClient.load_from_dict(client_config)
    return _client

CUSTOMER_ID = _env.get("CUSTOMER_ID", "9838845707").replace("-", "")

