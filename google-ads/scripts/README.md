# Scripts auxiliares

Scripts operacionais e análises ad hoc foram agrupados aqui para manter a raiz do projeto mais limpa.

## Estrutura

- `ads/`: utilitários ligados ao Google Ads e OAuth
- `analises/`: análises pontuais e investigações históricas
- `ga4/`: automações e testes ligados ao GA4/Playwright
- `tray/`: validacao OAuth/API da Tray em loja teste
- `vendas/`: conferências e cruzamentos com exports de pedidos

## Exemplos

- `./.venv_ads/bin/python scripts/ads/listar_campanhas.py`
- `./.venv_ads/bin/python scripts/ads/gerar_refresh_token.py`
- `python3 scripts/tray/tray_auth_check.py --env .env.tray auth`
- `python3 scripts/tray/tray_auth_check.py --env .env.tray refresh`
- `python3 scripts/tray/tray_auth_check.py --env .env.tray smoke`
