# 🚀 Instalação Rápida - Aumivet Blog + Strapi

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Acesso SSH à VPS
- Domínio configurado (DNS apontando para o IP da VPS)

## ⚡ Instalação em 5 Passos

### 1. Transferir Arquivos para VPS

```bash
# Execute o script de deploy
python deploy_full.py
```

Ou transfira manualmente:
- `docker-compose.yml`
- Pasta `frontend/`
- Pasta `strapi-app/`

### 2. Criar Arquivo .env

Na VPS, em `/opt/aumivet/`, crie o arquivo `.env`:

```bash
cd /opt/aumivet
nano .env
```

Cole o conteúdo (substitua os valores):

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

### 3. Criar Arquivo frontend/.env.production

```bash
cd /opt/aumivet/frontend
nano .env.production
```

Cole:

```env
NEXT_PUBLIC_STRAPI_URL=https://strapi.digitaldog.pet
NEXT_PUBLIC_SITE_URL=https://aumivet.com.br
NODE_ENV=production
```

### 4. Iniciar os Serviços

```bash
cd /opt/aumivet
docker compose up -d --build
```

### 5. Verificar Status

```bash
docker compose ps
```

Você deve ver 3 containers rodando:
- `aumivet-strapi-db` (PostgreSQL)
- `aumivet-strapi` (Strapi CMS)
- `aumivet-frontend` (Next.js)

## 🔍 Verificar Logs

```bash
# Todos os serviços
docker compose logs -f

# Serviço específico
docker compose logs -f frontend
docker compose logs -f strapi
docker compose logs -f strapiDB
```

## 🛠️ Comandos Úteis

### Reiniciar Serviços
```bash
docker compose restart
```

### Parar Serviços
```bash
docker compose down
```

### Parar e Remover Volumes (CUIDADO: apaga dados!)
```bash
docker compose down -v
```

### Atualizar e Reconstruir
```bash
docker compose up -d --build
```

### Ver Status
```bash
docker compose ps
```

## 🌐 Acessar Serviços

- **Frontend**: http://localhost:3000 (ou via domínio após configurar Nginx)
- **Strapi Admin**: http://localhost:1337/admin
- **Banco de Dados**: localhost:5432

## 🔧 Configurar Nginx (Opcional)

Se quiser usar Nginx como reverse proxy, configure:

```nginx
# /etc/nginx/sites-available/aumivet.com.br
server {
    listen 80;
    server_name aumivet.com.br www.aumivet.com.br;
    
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔒 Configurar SSL (Após DNS propagado)

```bash
certbot --nginx -d aumivet.com.br -d www.aumivet.com.br
certbot --nginx -d strapi.digitaldog.pet
```

## ✅ Tudo em Um Arquivo!

Agora você tem tudo em um único `docker-compose.yml`:
- ✅ Banco de Dados PostgreSQL
- ✅ Strapi CMS
- ✅ Frontend Next.js
- ✅ Rede isolada
- ✅ Volumes persistentes

Fácil de instalar, fácil de manter! 🎉

