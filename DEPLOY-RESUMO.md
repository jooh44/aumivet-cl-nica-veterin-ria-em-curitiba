# 🚀 Resumo do Deploy - Execute Manualmente

## ✅ O que já foi criado:

1. ✅ Scripts de deploy em `deploy/`
2. ✅ Docker-compose para produção
3. ✅ Configurações Nginx
4. ✅ Frontend atualizado com novo domínio

## ⚡ EXECUTE AGORA (copie e cole no terminal):

### 1. Copiar arquivos essenciais para VPS:

```bash
# Copiar docker-compose
scp deploy/docker-compose.prod.yml root@46.202.147.75:/opt/aumivet-strapi/docker-compose.yml

# Copiar configs Nginx
scp deploy/nginx-strapi.conf root@46.202.147.75:/opt/aumivet-strapi/deploy/
scp deploy/nginx-aumivet.conf root@46.202.147.75:/opt/aumivet-strapi/deploy/

# Copiar script de setup
scp deploy/setup-vps.sh root@46.202.147.75:/opt/aumivet-strapi/deploy/
```

### 2. Conectar na VPS e executar:

```bash
ssh root@46.202.147.75
```

### 3. Na VPS, executar:

```bash
cd /opt/aumivet-strapi

# Criar diretórios
mkdir -p strapi-app/{config,src,public/uploads} deploy

# Criar arquivo .env (COPIE SEU .env LOCAL AQUI)
nano .env
# Cole o conteúdo do seu .env local, mas mude:
# URL=https://strapi.digitaldog.pet
# NODE_ENV=production

# Dar permissão ao script
chmod +x deploy/setup-vps.sh

# Executar setup
bash deploy/setup-vps.sh
```

### 4. Iniciar containers:

```bash
cd /opt/aumivet-strapi
docker compose up -d
```

### 5. Verificar se está rodando:

```bash
docker compose ps
docker compose logs -f strapi
```

### 6. Configurar SSL (DEPOIS de configurar DNS):

```bash
certbot --nginx -d strapi.digitaldog.pet
certbot --nginx -d aumivet.com.br -d www.aumivet.com.br
```

## 📝 Arquivos importantes:

- `deploy/docker-compose.prod.yml` - Docker compose produção
- `deploy/nginx-strapi.conf` - Nginx para strapi.digitaldog.pet
- `deploy/nginx-aumivet.conf` - Nginx para aumivet.com.br
- `deploy/setup-vps.sh` - Script de configuração

## ⚠️ IMPORTANTE:

1. Configure DNS primeiro antes de gerar SSL
2. Use secrets diferentes em produção
3. Teste com: `curl http://46.202.147.75:1337/_health`

