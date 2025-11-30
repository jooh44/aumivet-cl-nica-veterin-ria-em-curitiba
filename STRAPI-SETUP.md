# Aumivet Strapi CMS - Docker Setup

Este diretório contém a configuração do Strapi CMS para o projeto Aumivet.

## 🚀 Quick Start

### 1. Iniciar o Strapi (primeira vez)

```bash
# Na raiz do projeto
docker-compose up -d
```

Aguarde alguns minutos para o Strapi inicializar pela primeira vez.

### 2. Acessar o Strapi Admin

Abra o navegador em: **http://localhost:1337/admin**

Na primeira vez, você será solicitado a criar uma conta de administrador:
- Email: seu-email@exemplo.com
- Password: senha-segura
- Nome: Seu Nome

### 3. Parar o Strapi

```bash
docker-compose down
```

### 4. Ver logs

```bash
docker-compose logs -f strapi
```

---

## 📁 Estrutura de Pastas

```
/
├── docker-compose.yml          # Configuração Docker
├── .env                        # Variáveis de ambiente (NÃO commitar)
├── .env.example               # Template de variáveis
└── strapi-app/                # Dados do Strapi (criado automaticamente)
    ├── config/                # Configurações
    ├── src/                   # Content types, controllers, etc
    ├── public/uploads/        # Uploads de mídia
    └── package.json
```

---

## 🎯 Content Types a Criar no Strapi

Após acessar o admin, crie estes content types:

### 1. **Blog Post** (Collection Type)
- title (Text, Required)
- slug (UID, Required, from title)
- content (Rich Text, Required)
- excerpt (Text)
- category (Enumeration: Saúde, Prevenção, Nutrição, Comportamento, Dicas)
- author (Text, default: "Dra. Thaise")
- featuredImage (Media, Single)
- readTime (Text, ex: "5 min")
- publishedAt (DateTime)
- SEO Component:
  - metaTitle (Text)
  - metaDescription (Text)
  - keywords (Text)

### 2. **Service** (Collection Type)
- name (Text, Required)
- slug (UID, Required, from name)
- description (Rich Text)
- icon (Text) - nome do ícone Lucide
- order (Number)
- featured (Boolean)

### 3. **Testimonial** (Collection Type)
- name (Text, Required)
- source (Text, default: "Google")
- text (Text, Required)
- rating (Number, 1-5)
- date (Date)

### 4. **Team Member** (Collection Type)
- name (Text, Required)
- role (Text)
- bio (Rich Text)
- photo (Media, Single)
- credentials (Text)
- order (Number)

---

## 🔌 Conectar Frontend ao Strapi

### 1. Atualizar .env.local do Frontend

```bash
cd frontend
```

Criar/editar `.env.local`:
```env
NEXT_PUBLIC_STRAPI_API_URL=http://localhost:1337
NEXT_PUBLIC_STRAPI_API_TOKEN=seu-token-aqui
```

### 2. Gerar API Token no Strapi

1. Acesse: http://localhost:1337/admin/settings/api-tokens
2. Clique em "Create new API Token"
3. Nome: "Frontend Token"
4. Token type: "Read-only"
5. Duration: "Unlimited"
6. Copie o token gerado e cole no `.env.local`

### 3. Configurar Permissões

1. Acesse: Settings → Users & Permissions Plugin → Roles → Public
2. Habilite as permissões de leitura (find, findOne) para:
   - Blog Post
   - Service
   - Testimonial
   - Team Member

---

## 🔒 Segurança

### Arquivos no .gitignore

Certifique-se de que estes estão no `.gitignore`:
```
.env
strapi-app/
.tmp/
.cache/
```

### Produção (VPS)

Quando for para produção:
1. Mude `NODE_ENV=production` no `.env`
2. Gere novos secrets aleatórios para:
   - APP_KEYS
   - API_TOKEN_SALT
   - ADMIN_JWT_SECRET
   - JWT_SECRET
3. Use senha forte no DATABASE_PASSWORD
4. Configure HTTPS no Nginx
5. Configure backup automático do banco

---

## 🛠️ Comandos Úteis

```bash
# Reiniciar serviços
docker-compose restart

# Ver todos os containers
docker ps

# Entrar no container do Strapi
docker exec -it aumivet-strapi sh

# Ver logs do banco de dados
docker-compose logs -f strapiDB

# Limpar tudo e recomeçar (CUIDADO: apaga dados!)
docker-compose down -v
docker-compose up -d
```

---

## 📝 Próximos Passos

1. ✅ Subir o Docker
2. ✅ Criar conta admin
3. ⬜ Criar content types
4. ⬜ Adicionar conteúdo de exemplo
5. ⬜ Conectar frontend
6. ⬜ Testar API
7. ⬜ Deploy na VPS
