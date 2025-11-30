# ✅ Status do Deploy - Strapi na VPS

## 🎉 SUCESSO!

### Containers Rodando:
- ✅ **aumivet-strapi-db-prod** (PostgreSQL) - Porta 5433
- ✅ **aumivet-strapi-prod** (Strapi) - Porta 1337

### Acesso:
- **Strapi Admin:** http://46.202.147.75:1337/admin
- **Strapi API:** http://46.202.147.75:1337/api

### Próximos Passos:

1. **Configurar DNS:**
   - `strapi.digitaldog.pet` → `46.202.147.75`
   - `aumivet.com.br` → `46.202.147.75`

2. **Após DNS propagar, gerar SSL:**
   ```bash
   ssh root@46.202.147.75
   certbot --nginx -d strapi.digitaldog.pet
   certbot --nginx -d aumivet.com.br -d www.aumivet.com.br
   ```

3. **Atualizar Nginx para HTTPS:**
   - Substituir configs HTTP pelas versões HTTPS
   - Reiniciar Nginx

4. **Configurar Coolify (opcional):**
   - Como o Coolify já está usando porta 80, você pode:
     - Parar temporariamente o Coolify
     - Ou configurar o Coolify para fazer proxy para o Strapi

### Comandos Úteis:

```bash
# Ver logs
ssh root@46.202.147.75 "cd /opt/aumivet-strapi && docker compose logs -f strapi"

# Reiniciar
ssh root@46.202.147.75 "cd /opt/aumivet-strapi && docker compose restart"

# Status
ssh root@46.202.147.75 "cd /opt/aumivet-strapi && docker compose ps"
```

### Arquivos na VPS:
- `/opt/aumivet-strapi/docker-compose.yml`
- `/opt/aumivet-strapi/.env` (com secrets gerados)
- `/opt/aumivet-strapi/strapi-app/` (config, src, uploads)
- `/etc/nginx/sites-available/strapi.digitaldog.pet`
- `/etc/nginx/sites-available/aumivet.com.br`

### ⚠️ Nota sobre Coolify:
O Coolify está usando a porta 80. Você tem duas opções:
1. Parar o Coolify temporariamente para testar o Nginx
2. Configurar o Coolify para fazer proxy reverso para o Strapi



