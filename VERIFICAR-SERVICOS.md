# 🔍 Verificar Status dos Serviços Docker

## 📋 Comandos para Verificar

Execute estes comandos **diretamente na VPS** (via SSH manual ou painel da Hostinger):

### 1. Verificar Containers em Execução

```bash
cd /opt/aumivet
docker compose ps
```

**Resultado esperado:**
- `aumivet-frontend-prod` - Status: Up
- `aumivet-strapi-prod` - Status: Up  
- `aumivet-strapi-db-prod` - Status: Up

### 2. Verificar Todos os Containers Docker

```bash
docker ps | grep aumivet
```

### 3. Testar Conectividade Local

```bash
# Testar Frontend
curl -I http://127.0.0.1:3000

# Testar Strapi
curl -I http://127.0.0.1:1337
```

### 4. Ver Logs dos Serviços

```bash
cd /opt/aumivet

# Logs do Frontend
docker compose logs --tail=20 frontend

# Logs do Strapi
docker compose logs --tail=20 strapi

# Logs do Banco de Dados
docker compose logs --tail=20 strapiDB
```

### 5. Reiniciar Serviços (se necessário)

```bash
cd /opt/aumivet

# Parar todos
docker compose down

# Iniciar novamente
docker compose up -d

# Ver status
docker compose ps
```

## 🐛 Troubleshooting

### Container não está rodando

```bash
# Ver o que aconteceu
docker compose logs [nome-do-container]

# Reiniciar container específico
docker compose restart [nome-do-container]
```

### Porta já em uso

```bash
# Verificar o que está usando a porta
netstat -tlnp | grep :3000
netstat -tlnp | grep :1337
```

### Verificar se os serviços estão respondendo

```bash
# Frontend
curl http://127.0.0.1:3000

# Strapi
curl http://127.0.0.1:1337
```

## 📝 Status Esperado

Após executar `docker compose ps`, você deve ver:

```
NAME                     STATUS          PORTS
aumivet-frontend-prod    Up X minutes    127.0.0.1:3000->3000/tcp
aumivet-strapi-prod      Up X minutes    127.0.0.1:1337->1337/tcp
aumivet-strapi-db-prod   Up X minutes    127.0.0.1:5433->5432/tcp
```

## 🔧 Script Automatizado

Criei um script `verificar_servicos.sh` que você pode executar na VPS:

```bash
chmod +x verificar_servicos.sh
./verificar_servicos.sh
```

Ou copie o conteúdo e execute diretamente na VPS.

