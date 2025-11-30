# 🚀 Deploy Rápido - Aumivet Blog + Strapi

## ⚡ Instalação em 3 Passos

### 1. Transferir Arquivos

```bash
python deploy_full.py
```

### 2. Configurar Variáveis de Ambiente

Na VPS (`/opt/aumivet/`):

**Criar `.env`:**
```env
DATABASE_CLIENT=postgres
DATABASE_HOST=strapiDB
DATABASE_PORT=5432
DATABASE_NAME=aumivet_strapi
DATABASE_USERNAME=strapi_user
DATABASE_PASSWORD=senha_segura_aqui
JWT_SECRET=seu_jwt_secret_aqui
ADMIN_JWT_SECRET=seu_admin_jwt_secret_aqui
APP_KEYS=key1,key2,key3,key4
API_TOKEN_SALT=seu_api_token_salt_aqui
NODE_ENV=production
HOST=0.0.0.0
PORT=1337
URL=https://strapi.digitaldog.pet
```

**Criar `frontend/.env.production`:**
```env
NEXT_PUBLIC_STRAPI_URL=https://strapi.digitaldog.pet
NEXT_PUBLIC_SITE_URL=https://aumivet.com.br
NODE_ENV=production
```

### 3. Iniciar Serviços

```bash
cd /opt/aumivet
docker compose up -d --build
```

## ✅ Verificar Status

```bash
docker compose ps
```

Deve mostrar 3 containers:
- ✅ `aumivet-strapi-db` (PostgreSQL)
- ✅ `aumivet-strapi` (Strapi CMS)
- ✅ `aumivet-frontend` (Next.js)

## 🔧 Comandos Úteis

```bash
# Ver logs
docker compose logs -f

# Reiniciar
docker compose restart

# Parar
docker compose down

# Atualizar
docker compose up -d --build
```

## 📁 Estrutura

```
/opt/aumivet/
├── docker-compose.yml      # ← TUDO EM UM ARQUIVO!
├── .env                    # Variáveis do Strapi
├── frontend/
│   ├── .env.production     # Variáveis do Frontend
│   └── ...
└── strapi-app/
    └── ...
```

**Simples, rápido e fácil de manter!** 🎉

