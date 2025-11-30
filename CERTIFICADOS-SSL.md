# 🔒 Certificados SSL Configurados

## ✅ Status

### Certificados Gerados

1. **aumivet.com.br** ✅
   - Domínios: `aumivet.com.br`, `www.aumivet.com.br`
   - Válido até: 2026-02-27 (89 dias)
   - Localização: `/etc/letsencrypt/live/aumivet.com.br/`
   - Status: **FUNCIONANDO** ✅

2. **strapi.digitaldog.pet** ⏳
   - Status: **Aguardando propagação DNS**
   - Erro: DNS problem: NXDOMAIN
   - Ação: Aguardar propagação DNS e tentar novamente

## 🌐 Acesso HTTPS

### Site Principal
- ✅ **https://aumivet.com.br** - Funcionando
- ✅ **https://www.aumivet.com.br** - Funcionando
- ✅ Redirecionamento HTTP → HTTPS configurado

### Strapi
- ⏳ **https://strapi.digitaldog.pet** - Aguardando DNS

## 🔄 Renovação Automática

O Certbot configurou renovação automática. Os certificados serão renovados automaticamente antes de expirar.

## 📝 Gerar Certificado para Strapi (quando DNS propagar)

Quando o DNS de `strapi.digitaldog.pet` estiver propagado:

```bash
# Parar Traefik temporariamente
docker stop coolify-proxy

# Gerar certificado
certbot certonly --standalone --non-interactive --agree-tos \
  --email aumivet.clinica@gmail.com -d strapi.digitaldog.pet

# Reiniciar Traefik
docker start coolify-proxy

# Atualizar configuração Nginx
# (já temos o arquivo nginx-strapi.conf pronto)
```

## 🛠️ Comandos Úteis

### Ver certificados
```bash
certbot certificates
```

### Renovar manualmente
```bash
certbot renew
```

### Testar renovação (dry-run)
```bash
certbot renew --dry-run
```

## ✅ Tudo Configurado!

Seu site está acessível via HTTPS:
- 🔒 **https://aumivet.com.br** - Seguro e funcionando!

