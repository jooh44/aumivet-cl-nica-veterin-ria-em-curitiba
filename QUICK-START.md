# 🚀 Guia Rápido - Iniciar Strapi

## Passo 1: Subir o Strapi

Abra o PowerShell na raiz do projeto e execute:

```powershell
docker-compose up -d
```

**Aguarde 2-3 minutos** para o Strapi inicializar pela primeira vez.

---

## Passo 2: Verificar se está rodando

```powershell
docker-compose logs -f strapi
```

Quando ver algo como: `Server started on port 1337` - está pronto! ✅

Pressione `Ctrl+C` para sair dos logs.

---

## Passo 3: Criar conta Admin

1. Abra: **http://localhost:1337/admin**
2. Preencha o formulário:
   - **First name:** Aumivet
   - **Last name:** Admin
   - **Email:** admin@aumivet.com.br
   - **Password:** [senha forte, guarde bem!]
3. Clique em "Let's start"

---

## Passo 4: Criar Content Types

No painel admin, vá em: **Content-Type Builder** (ícone de quebra-cabeça)

### 📝 Blog Post

1. Clique em **"Create new collection type"**
2. **Display name:** `Blog Post`
3. Adicione os campos:

| Campo | Tipo | Configurações |
|-------|------|--------------|
| title | Text | Required, Short text |
| slug | UID | Required, Attached to: title |
| content | Rich Text (Markdown) | Required |
| excerpt | Text | Long text |
| category | Enumeration | Values: Saúde, Prevenção, Nutrição, Comportamento, Dicas |
| author | Text | Default: "Dra. Thaise" |
| featuredImage | Media | Single media |
| readTime | Text | ex: "5 min" |
| publishedAt | Date | Type: datetime |

4. Clique em **"Save"** (canto superior direito)
5. Clique em **"Finish"**

### 🎨 Service

1. **"Create new collection type"**
2. **Display name:** `Service`
3. Campos:

| Campo | Tipo | Configurações |
|-------|------|--------------|
| name | Text | Required |
| slug | UID | Required, Attached to: name |
| description | Rich Text (Markdown) | |
| icon | Text | Short text (nome do ícone Lucide) |
| order | Number | Integer, default: 0 |
| featured | Boolean | default: false |

4. **Save** → **Finish**

### ⭐ Testimonial

1. **"Create new collection type"**
2. **Display name:** `Testimonial`
3. Campos:

| Campo | Tipo | Configurações |
|-------|------|--------------|
| name | Text | Required |
| source | Text | Default: "Google" |
| text | Text | Long text, Required |
| rating | Number | Integer format, Min: 1, Max: 5 |
| date | Date | Type: date |

4. **Save** → **Finish**

---

## Passo 5: Configurar Permissões (IMPORTANTE!)

1. Vá em: **Settings** → **Users & Permissions Plugin** → **Roles**
2. Clique em **"Public"**
3. Expanda cada Content Type e marque:
   - ✅ `find`
   - ✅ `findOne`
4. Clique em **"Save"** no topo

---

## Passo 6: Criar API Token

1. Vá em: **Settings** → **API Tokens**
2. Clique em **"Create new API Token"**
3. Preencha:
   - **Name:** Frontend Token
   - **Token type:** Read-only
   - **Token duration:** Unlimited
4. Clique em **"Save"**
5. **COPIE O TOKEN** (aparece uma vez só!)

---

## Passo 7: Adicionar Token no Frontend

Edite: `frontend/.env.local`

Cole o token nas duas variáveis:
```env
NEXT_PUBLIC_STRAPI_API_TOKEN=seu-token-aqui
STRAPI_API_TOKEN=seu-token-aqui
```

---

## Passo 8: Testar

1. Adicione um post de teste no Strapi:
   - Content Manager → Blog Post → Create new entry
   - Preencha os campos
   - Clique em **"Publish"**

2. Reinicie o Next.js:
```powershell
cd frontend
npm run dev
```

3. Acesse: **http://localhost:3000/blog**

---

## 🛑 Parar tudo

```powershell
# Parar Strapi
docker-compose down

# Parar Next.js
Ctrl+C no terminal do npm run dev
```

---

## ✅ Checklist

- [ ] Docker rodando
- [ ] Strapi acessível em localhost:1337
- [ ] Conta admin criada
- [ ] Content Types criados
- [ ] Permissões configuradas
- [ ] API Token gerado
- [ ] Token adicionado no .env.local
- [ ] Post de teste criado
- [ ] Frontend conectado ao Strapi

---

## 🆘 Problemas?

### Strapi não inicia
```powershell
docker-compose down -v
docker-compose up -d
```

### Erro de permissão
- No Strapi Admin: Settings → Roles → Public
- Marque find e findOne nos Content Types

### Frontend não conecta
- Verifique se o token está no .env.local
- Reinicie o `npm run dev`
