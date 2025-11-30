# 📝 PROJETO BLOG INSTITUCIONAL AUMIVET - DOCUMENTO MESTRE
## Next.js + Strapi + Docker Swarm + Traefik

> **Versão:** 2.0  
> **Data:** Novembro 2025  
> **Status:** Planejamento Completo  
> **Objetivo:** Plataforma escalável, SEO-first, template comercializável

---

## 🎯 DECISÕES ESTRATÉGICAS APROVADAS

### **Filosofia do Projeto**
- ✅ **Perfeição técnica** sobre velocidade de entrega
- ✅ **Escalabilidade** para agendamento e novas funcionalidades
- ✅ **Template comercializável** desde a concepção
- ✅ **SEO líder** em Curitiba como meta principal
- ✅ **Desenvolvimento local** com arquitetura production-ready

### **Arquitetura Aprovada**
- ✅ **Frontend**: 100% Next.js 15 (App Router) - site completo migrado do HTML
- ✅ **Roteamento**: Subpath `/blog` para posts, raiz para institucional
- ✅ **Conteúdo**: Lorem Ipsum e placeholders para validação de layout
- ✅ **Páginas dinâmicas**: Todas institucionais gerenciadas via Strapi
- ✅ **Deploy**: Desenvolvimento local → Staging → Produção (Ubuntu + Docker Swarm)

### **Escopo Completo**
```
✅ Blog (posts, categorias, autores)
✅ Páginas institucionais dinâmicas (home, sobre, serviços, contato)
✅ Sistema de navegação gerenciável
✅ Preparação para agendamento (estrutura + placeholder)
✅ CMS completo (Strapi 5)
✅ SEO avançado (Schema.org, OG, sitemaps, breadcrumbs)
✅ Performance otimizada (ISR, image optimization, Core Web Vitals)
```

---

## 📋 VISÃO GERAL TÉCNICA

**Plataforma headless CMS** movida por **Next.js 15** (frontend) e **Strapi 5** (backend), rodando via **Docker Swarm** em **Ubuntu 24.04 LTS**, com **Traefik** como reverse proxy (SSL automático), **PostgreSQL 16**, **Node 20**, gerenciada via **Portainer**.

**Diferenciais:**
- SEO técnico e moderno (structured data, rich snippets, AI-optimized)
- Conteúdo escalável e gerenciável sem código
- Template white-label para revenda
- Arquitetura preparada para microserviços futuros (agendamento, pagamentos)

---

## 🛠 Stack

- **Frontend**: Next.js 15, React 18+, TypeScript, Tailwind CSS, next/image, next-sitemap
- **Backend**: Strapi 5, PostgreSQL (Docker), Node 20 (Docker)
- **Infra**: Traefik (reverse proxy, SSL confiante via labels), Docker Swarm, Portainer, Ubuntu 24.04 LTS

---

## 📁 Estrutura de Diretórios

```

aumivet-blog/
├── frontend/        \# Next.js App
│   ├── app/         \# Pages
│   ├── components/  \# UI
│   ├── lib/         \# API Strapi
│   ├── types/       \# TS types
│   └── .env
├── backend/         \# Strapi App
│   ├── config/
│   ├── src/         \# Models
│   └── .env
├── docker-compose.yml
└── docs/            \# Documentação

```

---

## 🗃 Modelos de Conteúdo Strapi

### Blog Post
- title, slug, content (rich), excerpt, cover_image
- meta_title, meta_description, keywords
- published_date, updated_at, author (relation)
- categories (relation), featured, seo (componente)

### Author
- name, slug, bio, avatar, email, social_links, blog_posts (relation)

### Category
- name, slug, description, color, icon

### Page
- title, slug, content, meta_title, meta_description, seo, published

### Site Config (single)
- site_name, logo, favicon, contact_email/phone, social_media, google_analytics_id, google_site_verification

---

## 🐳 Docker Compose (Traefik Ready)

```

version: "3.8"

services:

db:
image: postgres:16
container_name: aumivet-db
environment:
POSTGRES_DB: aumivet_strapi
POSTGRES_USER: strapi_user
POSTGRES_PASSWORD: senha_segura_aqui
volumes:
- db_data:/var/lib/postgresql/data
restart: unless-stopped

strapi:
image: strapi/strapi:latest
container_name: aumivet-cms
env_file: ./backend/.env
volumes:
- ./backend:/srv/app
depends_on:
- db
labels:
- "traefik.enable=true"
- "traefik.http.routers.strapi.rule=Host(`cms.aumivet.com.br`)"
- "traefik.http.routers.strapi.entrypoints=websecure"
- "traefik.http.routers.strapi.tls.certresolver=letsencrypt"
restart: unless-stopped

nextjs:
image: node:20
container_name: aumivet-frontend
working_dir: /app
command: "bash -c 'npm install \&\& npm run build \&\& npm run start'"
env_file: ./frontend/.env
volumes:
- ./frontend:/app
labels:
- "traefik.enable=true"
- "traefik.http.routers.nextjs.rule=Host(`aumivet.com.br`,`www.aumivet.com.br`)"
- "traefik.http.routers.nextjs.entrypoints=websecure"
- "traefik.http.routers.nextjs.tls.certresolver=letsencrypt"
restart: unless-stopped

volumes:
db_data:

```

---

## 🌱 Variáveis .env

### backend/.env (Strapi)
```

HOST=0.0.0.0
PORT=1337
APP_KEYS=key1,key2,key3,key4
API_TOKEN_SALT=token_salt
ADMIN_JWT_SECRET=admin_jwt_secret
TRANSFER_TOKEN_SALT=transfer_token_salt
JWT_SECRET=jwt_secret

DATABASE_CLIENT=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=aumivet_strapi
DATABASE_USERNAME=strapi_user
DATABASE_PASSWORD=senha_segura_aqui
DATABASE_SSL=false

URL=https://cms.aumivet.com.br
FRONTEND_URL=https://aumivet.com.br
NODE_ENV=production

```

### frontend/.env (Next.js)
```

NEXT_PUBLIC_STRAPI_URL=https://cms.aumivet.com.br
STRAPI_API_TOKEN=token_readonly
REVALIDATE_SECRET=secret_revalidate
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NODE_ENV=production

```

---

## ⚙️ Setup & Deploy Docker Swarm

1. **Não remova nenhum serviço! Adicione este stack separadamente.**
2. Crie diretórios `frontend` e `backend` conforme acima (copie projetos Next.js e Strapi).
3. Adicione e configure `docker-compose.yml` com rotas/labels do Traefik.

**Deploy pelo Portainer:**  
- Suba o stack novo: _aumivet-blog_ ou nome similar
- Verifique logs/saúde dos containers
- Gerencie tudo via Portainer Orion Design

---

## 🚀 Workflow do Conteúdo

1. Insira posts, pages, autores e categorias via painel do Strapi em `https://cms.aumivet.com.br/admin`
2. Next.js consome dados via API (`/api/blog-posts`, etc) usando token
3. Utiliza ISR com revalidação automática via webhook Strapi → Next.js (`/api/revalidate?secret=SECRET_TOKEN`)
4. SEO: Plugin Strapi SEO, next-sitemap, metadados dinâmicos
5. Conteúdo e layout atualizáveis sem rebuild no frontend

---

## 🎯 Checklist SEO + Performance

- [x] Meta tags e dados estruturados automáticos
- [x] Sitemap.xml/robots.txt
- [x] Open Graph/Twitter Card
- [x] SSL via Traefik/Let's Encrypt
- [x] Imagens otimizadas
- [x] Core Web Vitals
- [x] Canonical URLs e breadcrumbs
- [x] FAQ com Schema.org
- [x] Featured snippets otimizados para IA

---

## 🔧 Comandos Docker Úteis

```

docker stack deploy -c docker-compose.yml aumivet-blog
docker service ls
docker logs aumivet-cms
docker logs aumivet-frontend
docker exec -it aumivet-db psql -U strapi_user aumivet_strapi

```

---

## 📝 Observações Finais

- NÃO remova nem altere Traefik, Portainer, stacks existentes.
- Todos os serviços novos com rede, volumes e rotas dedicados.
- Backup de banco com `pg_dump` via exec no container.
- Todos os comandos e configurações podem ser automatizados via IA CLI ou pelo Portainer.

---

**Desenvolvedor:** UI/UX & Web Developer  
**Cliente:** AumiVet  
**Ambiente:** Ubuntu 24.04 LTS + Docker Swarm + Traefik + Portainer  
**Data:** Novembro 2025  
**Versão:** 1.0
```

Se quiser incluir mais detalhes como setup multi-stage para build do Next.js, exemplos de rotas, ou configurações extras de Traefik, peça que complemento!

---

## Recomendações Adicionais para Manutenção e Estabilidade

- Versione explicitamente as imagens e dependências críticas para evitar que updates automáticos do `node:20` ou `strapi/strapi:latest` introduzam regressões; sugerido fixar tags (ex.: `node:20.11-alpine`, `strapi/strapi:5.2.1`) e atualizar conscientemente.
- Implemente builds multi-stage no frontend para compilar o Next.js em imagem própria (`builder` + `runner`) reduzindo tempo de deploy e superfície de falhas; publique a imagem em registry privado para reproduzir releases facilmente.
- Padronize arquivos `.env.example` na pasta `frontend` e `backend` com explicação de cada variável; adote `doppler` ou `sops` se quiser criptografar segredos e manter sincronizados entre ambientes.
- Crie workflow de CI (GitHub Actions ou GitLab CI) para rodar lint, testes, `next build` e `strapi build` antes de gerar as imagens; isso captura bugs de schema ou TypeScript cedo e garante imagens sempre consistentes.
- Automatize migrações e backups do PostgreSQL com job recorrente (`docker service` ou cron no host) salvando dumps versionados e testando restauração periódica em ambiente de staging.
- No Swarm, defina `deploy.update_config` e `deploy.rollback_config` nos serviços críticos para habilitar atualizações coordenadas, healthchecks (`CMD-SHELL curl -f http://localhost:3000/health`) e reversão automática em caso de falha.
- Configure observabilidade mínima: métricas (Prometheus + cAdvisor) e alertas de logs (Loki/ELK) para acompanhar consumo, erros de Strapi e status dos webhooks de revalidação.
- Documente no diretório `docs/` um playbook curto de incidentes (como reiniciar serviços, restaurar backup, renovar certificado) e mantenha changelog a cada release para rastreabilidade.


---

## Planejamento de Paginas Institucionais e Escalabilidade

- **Conteudo estruturado**: amplie o schema `Page` no Strapi com um campo `page_type` (ex.: landing, service, about, team, contact) e blocos reutilizaveis (hero, rich_text, feature_grid, cta). Crie colecoes `Service`, `TeamMember`, `Partner`, `Timeline` com slugs unicos e campos SEO herdando o componente padrao.
- **Rotas Next.js**: mantenha as paginas institucionais dentro de `app/(site)/[pageSlug]/page.tsx`, e crie segmentos dedicados `app/(site)/servicos/[serviceSlug]/page.tsx`, `app/(site)/equipe/page.tsx`, etc. Use `generateStaticParams` + `revalidate` para SSG incremental e trate `notFound` para slugs inexistentes.
- **Layouts e navegacao**: centralize o layout publico em `app/(site)/layout.tsx`, com cabecalho/rodape dinamicos vindos de uma collection `Navigation`. Implemente breadcrumbs e sidebars quando houver hierarquia de servicos para reforcar SEO e UX.
- **Componentizacao**: extraia componentes UI em `frontend/components/site/` (ex.: `HeroSection.tsx`, `ServiceCard.tsx`, `TeamGrid.tsx`). Cada componente recebe dados tipados (`zod`/`io-ts`) vindos do Strapi, garantindo compatibilidade quando o template for revendido.
- **Seeds e fixtures**: mantenha scripts `backend/scripts/seed.ts` e `frontend/scripts/generate-mock.ts` para popular o Strapi com servicos/equipe de exemplo. Documente esse fluxo em `docs/SEEDING.md` para quem comprar o template reproduzir rapido.
- **Automacao de sitemap/OG**: ajuste `next-sitemap` para incluir rotas raiz (`/servicos`, `/sobre`, `/equipe`) e detalhes de servico. Implemente `generateMetadata` por tipo de pagina, disparando schemas apropriados (`Service`, `Organization`, `Person`).
- **Planejamento de agendamento**: reserve rota `/agendamento` com pagina estagio beta consumindo dados do Strapi (texto, faq, links externos). Documente opcao futura de integrar provedores externos ou microservico proprio via API em `/api/scheduling`.
- **Template comercial**: crie guia `docs/TEMPLATE-Handoff.md` descrevendo como duplicar o projeto, ajustar dominios/Traefik e importar conteudo base. Inclua checklist de substituicao (logos, cores, textos default) para acelerar entregas pagas.
- **Testes e QA**: adicione testes Playwright para smoke das principais rotas (`servicos`, `sobre`, `blog`, `contato`) e contrato de API validando que blocos obrigatorios estao presentes. Configure workflow para rodar esses testes antes de publicar novas imagens no registry.
