# 🚀 Guia Completo de Deploy - Aumivet Blog + Strapi

Este guia explica como fazer o deploy completo do blog Next.js e do Strapi CMS para a VPS.

## 📋 Pré-requisitos

1. Python 3 instalado
2. Paramiko instalado: `pip install paramiko`
3. Acesso SSH à VPS (46.202.147.75)
4. DNS configurado para:
   - `aumivet.com.br` → IP da VPS
   - `strapi.digitaldog.pet` → IP da VPS

## 🎯 Processo de Deploy

### Passo 1: Executar Script de Deploy

Execute o script Python que transfere todos os arquivos para a VPS:

```bash
python deploy_full.py
```

Este script irá:
- ✅ Transferir o código do Strapi
- ✅ Transferir o código do frontend Next.js
- ✅ Transferir arquivos de configuração (docker-compose, nginx, etc.)
- ✅ Criar estrutura de diretórios na VPS

### Passo 2: Configurar Variáveis de Ambiente na VPS

Conecte-se na VPS e crie os arquivos `.env` necessários:

```bash
python ssh_run.py "cd /opt/aumivet && cat > .env << 'EOF'
DATABASE_CLIENT=postgres
DATABASE_HOST=strapiDB
DATABASE_PORT=5432
DATABASE_NAME=aumivet_strapi
DATABASE_USERNAME=strapi_user
DATABASE_PASSWORD=SUA_SENHA_SEGURA_AQUI
JWT_SECRET=SEU_JWT_SECRET_AQUI
ADMIN_JWT_SECRET=SEU_ADMIN_JWT_SECRET_AQUI
APP_KEYS=key1,key2,key3,key4
API_TOKEN_SALT=SEU_API_TOKEN_SALT_AQUI
NODE_ENV=production
HOST=0.0.0.0
PORT=1337
URL=https://strapi.digitaldog.pet
EOF"
```

**⚠️ IMPORTANTE:** Gere novos secrets para produção! Use um gerador de senhas seguras.

Para o frontend:

```bash
python ssh_run.py "cd /opt/aumivet/frontend && cat > .env.production << 'EOF'
NEXT_PUBLIC_STRAPI_URL=https://strapi.digitaldog.pet
NEXT_PUBLIC_SITE_URL=https://aumivet.com.br
NODE_ENV=production
EOF"
```

### Passo 3: Configurar Ambiente na VPS

Execute o script de setup:

```bash
python ssh_run.py "cd /opt/aumivet && bash deploy/setup-vps.sh"
```

Este script irá:
- ✅ Verificar/instalar Docker
- ✅ Verificar/instalar Nginx
- ✅ Configurar arquivos Nginx
- ✅ Criar diretórios necessários

### Passo 4: Configurar SSL com Certbot

Configure os certificados SSL:

```bash
# Para o Strapi
python ssh_run.py "certbot --nginx -d strapi.digitaldog.pet --non-interactive --agree-tos --email seu-email@exemplo.com"

# Para o site principal
python ssh_run.py "certbot --nginx -d aumivet.com.br -d www.aumivet.com.br --non-interactive --agree-tos --email seu-email@exemplo.com"
```

### Passo 5: Iniciar Containers

Inicie os containers Docker:

```bash
python ssh_run.py "cd /opt/aumivet && docker compose up -d --build"
```

**⏱️ Nota:** O build do frontend pode levar alguns minutos na primeira vez.

### Passo 6: Verificar Status

Verifique se tudo está rodando:

```bash
# Ver status dos containers
python ssh_run.py "cd /opt/aumivet && docker compose ps"

# Ver logs
python ssh_run.py "cd /opt/aumivet && docker compose logs -f"
```

## 🔍 Verificação e Testes

### Testar Strapi
- Acesse: `https://strapi.digitaldog.pet/admin`
- Faça login no painel administrativo
- Verifique se os content types estão configurados

### Testar Frontend
- Acesse: `https://aumivet.com.br`
- Verifique se o site carrega corretamente
- Teste a página do blog: `https://aumivet.com.br/blog`
- Verifique se os posts do Strapi aparecem

## 🛠️ Comandos Úteis

### Na VPS (via ssh_run.py)

```bash
# Ver logs do Strapi
python ssh_run.py "cd /opt/aumivet && docker compose logs -f strapi"

# Ver logs do Frontend
python ssh_run.py "cd /opt/aumivet && docker compose logs -f frontend"

# Reiniciar serviços
python ssh_run.py "cd /opt/aumivet && docker compose restart"

# Parar serviços
python ssh_run.py "cd /opt/aumivet && docker compose down"

# Atualizar e reconstruir
python ssh_run.py "cd /opt/aumivet && docker compose up -d --build"

# Ver status
python ssh_run.py "cd /opt/aumivet && docker compose ps"
```

## 🔄 Atualizações Futuras

Para atualizar o código após mudanças:

1. Execute novamente o script de deploy:
   ```bash
   python deploy_full.py
   ```

2. Reconstrua os containers:
   ```bash
   python ssh_run.py "cd /opt/aumivet && docker compose up -d --build"
   ```

## 🐛 Troubleshooting

### Container não inicia
```bash
python ssh_run.py "cd /opt/aumivet && docker compose logs [nome-do-container]"
```

### Nginx não funciona
```bash
python ssh_run.py "nginx -t"
python ssh_run.py "systemctl status nginx"
python ssh_run.py "systemctl restart nginx"
```

### Certificado SSL não funciona
```bash
python ssh_run.py "certbot certificates"
python ssh_run.py "certbot renew --dry-run"
```

### Frontend não conecta ao Strapi
- Verifique se `NEXT_PUBLIC_STRAPI_URL` está correto no `.env.production`
- Verifique se o Strapi está rodando: `docker compose ps`
- Verifique os logs: `docker compose logs strapi`

## 📝 Estrutura na VPS

```
/opt/aumivet/
├── .env                          # Variáveis do Strapi
├── docker-compose.yml            # Docker Compose
├── strapi-app/                   # Código do Strapi
│   ├── config/
│   ├── src/
│   └── public/uploads/
├── frontend/                     # Código do Next.js
│   ├── .env.production           # Variáveis do Frontend
│   └── ...
└── deploy/                       # Scripts de deploy
    ├── nginx-strapi.conf
    ├── nginx-aumivet.conf
    └── setup-vps.sh
```

## ✅ Checklist de Deploy

- [ ] DNS configurado e propagado
- [ ] Script de deploy executado (`deploy_full.py`)
- [ ] Arquivo `.env` criado na VPS com secrets seguros
- [ ] Arquivo `frontend/.env.production` criado
- [ ] Script de setup executado (`setup-vps.sh`)
- [ ] Certificados SSL configurados
- [ ] Containers iniciados e rodando
- [ ] Strapi acessível em `https://strapi.digitaldog.pet`
- [ ] Site acessível em `https://aumivet.com.br`
- [ ] Blog funcionando e mostrando posts do Strapi

## 🎉 Pronto!

Seu blog e Strapi estão em produção! 🚀

