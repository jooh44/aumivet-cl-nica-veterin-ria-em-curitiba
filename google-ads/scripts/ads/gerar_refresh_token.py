import os
from pathlib import Path

import google_auth_oauthlib.flow


def load_env_ads():
    env_path = Path(__file__).resolve().parents[2] / ".env.ads"
    values = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.split(" #", 1)[0].strip()
    return values


def main():
    env = {**load_env_ads(), **os.environ}
    client_id = env.get("CLIENT_ID")
    client_secret = env.get("CLIENT_SECRET")
    if not client_id or not client_secret:
        raise SystemExit("Defina CLIENT_ID e CLIENT_SECRET no .env.ads ou no ambiente.")

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    # O Escopo permissivo da API do Google Ads
    scopes = ["https://www.googleapis.com/auth/adwords"]

    print("Iniciando o fluxo de autorização OAuth 2.0...")
    print("O seu navegador deve abrir automaticamente.")
    print("Se não abrir, clique no link que aparecerá abaixo!\n")

    # Inicia o servidor local para capturar a resposta do Google
    # Usando a porta 8080 para facilitar
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
        client_config, scopes=scopes
    )
    
    # Executa a autorização
    flow.run_local_server(port=8080, prompt="consent")

    print("\nAUTORIZACAO CONCLUIDA COM SUCESSO!\n")
    print("Por favor, copie as informações abaixo e salve no arquivo '.env.ads':")
    print("-" * 50)
    print(f"REFRESH_TOKEN={flow.credentials.refresh_token}")
    print("-" * 50)

if __name__ == "__main__":
    main()
