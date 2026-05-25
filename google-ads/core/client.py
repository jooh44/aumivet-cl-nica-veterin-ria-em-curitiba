import os

from google.ads.googleads.client import GoogleAdsClient

_client = None
_env = {}


def _clean_env_value(value: str) -> str:
    """Remove inline comments and formatting from .env.ads values."""
    if "#" in value:
        value = value.split("#", 1)[0]
    return value.strip().strip('"').strip("'")


def _clean_customer_id(value: str) -> str:
    return _clean_env_value(value).replace("-", "")


# Carrega as variáveis do .env.ads ao importar o módulo
env_path = os.path.join(os.path.dirname(__file__), "..", ".env.ads")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                _env[k.strip()] = _clean_env_value(v)

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

    login_customer = _clean_customer_id(_env.get("LOGIN_CUSTOMER_ID", ""))
    if login_customer:
        client_config["login_customer_id"] = login_customer

    _client = GoogleAdsClient.load_from_dict(client_config)
    return _client

CUSTOMER_ID = _clean_customer_id(_env.get("CUSTOMER_ID", "9838845707"))
