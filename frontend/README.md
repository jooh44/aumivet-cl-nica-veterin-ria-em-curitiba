# Aumivet Frontend - Next.js

Frontend do projeto Aumivet construído com Next.js 15, TypeScript e Tailwind CSS.

## 🚀 Início Rápido

### Desenvolvimento Local

```bash
# Instalar dependências
npm install

# Rodar em modo desenvolvimento
npm run dev

# Abrir http://localhost:3000
```

### Build de Produção

```bash
# Criar build otimizado
npm run build

# Rodar em produção
npm start
```

## 📁 Estrutura do Projeto

```
frontend/
├── app/                    # App Router (Next.js 15)
│   ├── layout.tsx         # Layout root
│   ├── page.tsx           # Homepage
│   ├── globals.css        # Estilos globais
│   ├── blog/              # Rotas do blog
│   │   ├── page.tsx       # Listagem de posts
│   │   └── [slug]/        # Post individual
│   ├── sobre/             # Página sobre
│   ├── servicos/          # Página de serviços
│   ├── contato/           # Página de contato
│   ├── sitemap.ts         # Sitemap dinâmico
│   ├── robots.ts          # Robots.txt
│   └── api/               # API Routes
│       └── revalidate/    # Webhook ISR
├── components/            # Componentes React (futuro)
├── lib/                   # Bibliotecas e utilidades
│   └── strapi.ts         # Client Strapi API
├── types/                 # TypeScript types
│   └── strapi.ts         # Tipos Strapi
├── public/               # Assets estáticos
├── .env.local           # Variáveis de ambiente (local)
├── .env.example         # Template de variáveis
├── next.config.js       # Configuração Next.js
├── tailwind.config.ts   # Configuração Tailwind
└── tsconfig.json        # Configuração TypeScript
```

## 🎨 Design System

### Cores

```css
--color-white: #FFFFF2      /* Background principal */
--color-pink: #E66884       /* Destaques */
--color-green: #9CA876      /* Botões */
--color-green-light: #B6D455 /* Hover */
--color-black: #111111      /* Textos principais */
--color-gray: #1D1D1D       /* Textos secundários */
```

### Tipografia

- **Display/Frases especiais**: Playfair Display (italic)
- **Títulos**: Poppins
- **Corpo**: Inter

## 🔧 Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env.local` e configure:

```env
NEXT_PUBLIC_STRAPI_URL=http://localhost:1337
STRAPI_API_TOKEN=your_api_token_here
REVALIDATE_SECRET=your_secret_here
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

## 📡 Integração Strapi

### Funções Disponíveis

```typescript
import { getBlogPosts, getBlogPostBySlug } from '@/lib/strapi';

// Listar posts
const posts = await getBlogPosts({ limit: 10, page: 1 });

// Post por slug
const post = await getBlogPostBySlug('exemplo-post');
```

### ISR (Incremental Static Regeneration)

- Posts do blog: revalidação a cada 1h
- Páginas estáticas: revalidação a cada 24h
- Revalidação sob demanda via webhook `/api/revalidate`

## 🎯 SEO

### Implementado

- ✅ Metadata dinâmica por página
- ✅ Open Graph e Twitter Cards
- ✅ Schema.org (VeterinaryCare, BlogPosting)
- ✅ Sitemap.xml automático
- ✅ Robots.txt
- ✅ Canonical URLs
- ✅ Imagens otimizadas (next/image)

### Webhooks Strapi

Configure no Strapi Admin:

**URL**: `https://aumivet.com.br/api/revalidate`  
**Method**: POST  
**Body**:
```json
{
  "secret": "seu_secret_aqui",
  "path": "/blog/{{slug}}"
}
```

## 🐳 Docker

```bash
# Build
docker build -t aumivet-frontend .

# Run
docker run -p 3000:3000 aumivet-frontend
```

## 📝 Próximos Passos

- [ ] Conectar com Strapi backend real
- [ ] Criar componentes reutilizáveis (Header, Footer, Button, Card)
- [ ] Implementar busca de posts
- [ ] Adicionar paginação
- [ ] Sistema de comentários (opcional)
- [ ] Newsletter (integração futura)
- [ ] Página de agendamento

## 🚨 Troubleshooting

### Erro: "Cannot find module"
```bash
npm install
```

### Imagens não carregam do Strapi
Verifique `next.config.js` > `remotePatterns`

### Revalidação não funciona
Confirme `REVALIDATE_SECRET` em `.env.local` e no webhook Strapi

## 📄 Licença

MIT - Aumivet 2025
