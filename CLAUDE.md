# Aumivet - contexto para agentes

Leia primeiro `project-context.md`. Ele e a fonte atual da retomada, proposta comercial, estado tecnico e limites de linguagem.

## Estado rapido

- Aumivet e uma clinica veterinaria em Curitiba, cliente antigo em retomada.
- O repo tem landing estatica na raiz (`index.html`, `styles.css`, `images/`) e app Next em `frontend/`.
- O projeto nao usa CMS no estado atual.
- Strapi/CMS legado foi removido nesta retomada; nao reintroduzir sem decisao explicita.
- A proposta comercial mais atual esta em `docs/proposta-comercial-aumivet.html`.

## Comandos do frontend

```bash
cd frontend
npm ci
npm run build
npm run dev
```

## Cuidados comerciais

- Nao mencionar o problema antigo de SEO/grafia nas propostas.
- Nao usar jargao tecnico cliente-facing como GA4, GTM, UTM ou Search Console.
- Falar em medicao de contatos, presenca local no Google, melhoria de ranqueamento, busca com IA e reforco da parceria Petlove.
- O plano recomendado da proposta e `R$ 750/mes por 3 meses`.
- O plano premium e `R$ 1.000/mes por 3 meses`, com posts semanais, branding e cartao de visita impresso entregue na clinica.
