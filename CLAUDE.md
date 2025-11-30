# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Aumivet Veterinary Clinic** website - a modern Next.js application for a veterinary clinic in Curitiba, Brazil. The site features a blog system and is designed to integrate with Strapi CMS for content management.

## Architecture & Structure

- **Framework**: Next.js 15.5.6 (App Router)
- **Language**: TypeScript
- **Styling**: CSS Modules + Global CSS (aumivet-original.css)
- **Deployment**: Static export ready for VPS
- **CMS**: Strapi integration (headless CMS)

### File Structure
```
/
├── frontend/                 # Next.js application
│   ├── app/                 # App Router pages
│   │   ├── page.tsx        # Homepage
│   │   ├── layout.tsx      # Root layout
│   │   ├── globals.css     # Global styles
│   │   ├── aumivet-original.css  # Main stylesheet
│   │   ├── blog/           # Blog archive page
│   │   │   ├── page.tsx
│   │   │   └── [slug]/     # Individual blog posts
│   │   ├── servicos/       # Services page
│   │   ├── sobre/          # About page
│   │   ├── contato/        # Contact page
│   │   └── api/            # API routes
│   ├── components/         # React components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── HeroSection.tsx
│   │   ├── ServicesSection.tsx
│   │   ├── TestimonialsSection.tsx
│   │   ├── BlogPreviewSection.tsx
│   │   └── ... (other sections)
│   ├── lib/                # Utilities
│   │   └── strapi.ts       # Strapi API integration
│   ├── types/              # TypeScript types
│   │   └── strapi.ts
│   └── public/             # Static assets
│       └── images/
├── docker-compose.yml       # Strapi + PostgreSQL containers
├── .env                     # Strapi configuration (not committed)
├── .gitignore              # Git ignore rules
├── STRAPI-SETUP.md         # Strapi setup guide
├── QUICK-START.md          # Quick start guide
├── images/                  # Legacy image assets
├── instruções.md           # Content guidelines (Portuguese)
├── design-principles.md    # Design system
└── CLAUDE.md              # This file
```

## 📋 Strapi Content Types

### Blog Post (blog-posts)
- **Title** (Text) - Título do post
- **Slug** (UID) - URL amigável (gerado automaticamente)
- **Category** (Enumeration) - saude, prevencao, nutricao, comportamento, dicas
- **Author** (Text) - Nome do autor
- **Readtime** (Number) - Tempo de leitura estimado
- **Publishedat** (Date) - Data de publicação
- **Featuredimage** (Media) - Imagem de destaque
- **Content** (Rich Text) - Conteúdo completo do post
- **Excerpt** (Text Long) - Resumo/preview

### Service (services)
- **Title** (Text)
- **Slug** (UID)
- **Description** (Text Long)
- **Icon** (Text) - Nome do ícone
- **Order** (Number) - Ordem de exibição
- **Featuredimage** (Media)

### Testimonial (testimonials)
- **Authorname** (Text)
- **Petname** (Text)
- **Content** (Text Long)
- **Rating** (Number)
- **Order** (Number)

### ⚠️ Importante - Strapi v3 Specifics
- **Version**: Strapi 3.6.8 Community Edition
- **Field Names**: Usa PascalCase (`Title`, `Slug`, `Category`)
- **API Endpoint**: `/blog-posts` (sem prefixo `/api` do Strapi v4)
- **Categories**: Armazenadas sem acentos no banco (`saude`, `prevencao`, `nutricao`, `comportamento`, `dicas`)
- **Frontend Mapping**: Converte para exibição com acentos (Saúde, Prevenção, etc.)
- **Permissions**: Public role precisa ter `find` e `findone` habilitados para cada content type
- **API Token**: Opcional na v3 (diferente da v4 que exige token)
- **React Keys**: Usar `slug` como key em listas (não `id`) para evitar conflitos entre posts do Strapi e estáticos

## Design System

### Color Palette (CSS Variables)
- `--branco: #FFFFF2` - Main background color
- `--rosa: #E66884` - Accent color for highlights and vectors
- `--verde: #9CA876` - Primary button color
- `--verde-claro: #B6D455` - Button hover state
- `--preto: #1f1f1f` - Main text color
- `--cinza: rgb(29, 29, 29)` - Body text color
- `--border-color: #e5e5e5` - Border color for cards

### Typography Hierarchy
- **Destaque/Special phrases**: `'Playfair Display', serif` (italic, weight 400)
- **Títulos/Headers**: `'Poppins', sans-serif`
- **Corpo/Body text**: `'Inter', sans-serif`

### Key Components
- **Hero section** with smooth ticker animation
- **Responsive navigation** with mobile menu
- **Service cards** with Lucide icons
- **Blog system** with category filters and clean card design
- **Team section** featuring Dra. Thaise
- **Testimonials** with infinite scroll ticker (Google Reviews)
- **Contact section** with WhatsApp integration
- **Footer** with sitemap and social links

### Blog System Features
- Category filtering (Saúde, Prevenção, Nutrição, Comportamento, Dicas)
- Clean card design without hover effects (only category tag highlights on hover)
- Responsive grid layout
- Individual blog post pages with SEO optimization
- No active/focus outlines on links (cleaner UX)

## Important Implementation Notes

### Recent Updates (November 2025)
- **Blog page fixed**: Removed spacing issues between cards, fixed rendering bugs
- **Testimonials ticker**: Implemented infinite seamless loop without jumps
- **Blog card interactions**: Removed hover effects from cards, only category tag animates
- **Link styling**: Removed focus/active outlines for cleaner UX (hover effects preserved)
- **Responsive optimization**: All sections working properly on mobile and desktop

### Hero Section Specifics
- Clean hero with smooth ticker animation
- Logo properly sized in navigation
- Solid green buttons (`--verde`) with light green hover (`--verde-claro`)
- Use `.destaque` class for italic Playfair Display highlights in titles

### Blog System Implementation
- **Archive page** (`/blog`): Grid layout with category filters
- **Individual posts** (`/blog/[slug]`): Full post pages
- **Card design**: Clean, minimal hover effects
- **Category tags**: Animate on card hover (scale + opacity + shadow)
- **No CSS artifacts**: Fixed margin-bottom issues causing phantom spacing

### SEO Requirements
- Next.js metadata API for dynamic SEO
- Sitemap generation (`sitemap.ts`)
- Robots.txt configuration
- Schema.org markup for VeterinaryCare
- Optimized meta tags for local Curitiba veterinary searches
- Semantic HTML structure with proper heading hierarchy

### Performance Guidelines
- Next.js Image component for automatic optimization
- App Router for optimal routing performance
- Static generation where possible
- Mobile-first responsive approach
- Core Web Vitals optimization

## Content Guidelines

All content is in **Portuguese (Brazilian)** and focuses on:
- Local SEO for Curitiba veterinary services
- Dra. Thaise's credentials (PUCPR graduate)
- Clinic address: R. Santo Antônio, 891 - Rebouças, Curitiba - PR
- Contact: (41) 98860-4202 / aumivet.clinica@gmail.com

### Service Categories
1. Consultas e Vacinas
2. Cirurgias Especializadas
3. Exames e Diagnósticos
4. Odontologia Veterinária
5. Banho, Tosa e Estética Pet
6. Adestramento Pet
7. Coworking Veterinário (specialty service)
8. Anestesista/Cirurgiã Volante (specialty services)

## Development Workflow

### Local Development
```bash
cd frontend
npm install
npm run dev
```
- Development server runs on `http://localhost:3000`
- Hot reload enabled for rapid development
- TypeScript type checking on save

### Build & Deploy
```bash
cd frontend
npm run build    # Production build
npm run start    # Test production build locally
```

### Testing Checklist
1. Test across breakpoints: 320px, 768px, 1024px, 1200px
2. Verify blog pagination and filtering
3. Check all internal links and navigation
4. Test mobile menu functionality
5. Verify WhatsApp button integration
6. Check testimonials infinite scroll
7. Validate all forms (contact)

## Common Tasks

- **Local development**: `npm run dev` in `/frontend` directory
- **Add new blog post**: Create new page in `/frontend/app/blog/[slug]/page.tsx`
- **Edit components**: All components in `/frontend/components/`
- **Update styles**: Main stylesheet at `/frontend/app/aumivet-original.css`
- **Content updates**: Refer to `instruções.md` for copy and SEO guidelines
- **Design changes**: Follow CSS variables in aumivet-original.css

## Strapi CMS Integration ✅

### Current Setup (Docker)
- **Container**: aumivet-strapi (Strapi 3.6.8)
- **Database**: aumivet-strapi-db (PostgreSQL 15)
- **Admin Panel**: http://localhost:1337/admin
- **API Endpoint**: http://localhost:1337/blog-posts

### Environment Variables
```env
# Local Development
NEXT_PUBLIC_STRAPI_URL=http://localhost:1337

# Production (VPS)
NEXT_PUBLIC_STRAPI_URL=https://cms.aumivet.com.br
NEXT_PUBLIC_SITE_URL=https://aumivet.com.br
```

### Content Types Created
- ✅ **Blog Posts** (9 fields: Title, Slug, Content, Category, Author, Readtime, Publishedat, Featuredimage, Excerpt)
- ✅ **Services** (6 fields: Title, Slug, Description, Icon, Order, Featuredimage)
- ✅ **Testimonials** (5 fields: Authorname, Petname, Content, Rating, Order)

### Integration Details
- **Blog Archive** (`/blog`): Fetches from Strapi via `useEffect`, combines with static posts
- **Blog Post** (`/blog/[slug]`): Fetches from Strapi via `getBlogPostBySlug()`, falls back to static
- **Fallback Strategy**: Static posts always available if Strapi is down
- **ISR**: Configured with `revalidate: 3600` (1 hour cache)
- **Category Mapping**: Converts database format (`saude`) to display format (`Saúde`)
- **Image URLs**: Automatically prefixed with Strapi URL via `getStrapiImageUrl()`
- **Date Handling**: Uses `published_at` as fallback if `Publishedat` is null
- **Readtime Field**: Handles both string ("5 min") and number (5) formats
- **React Keys**: Uses `slug` instead of `id` to prevent duplicate key warnings
- **Public Permissions**: No API token required for v3 (enabled in Strapi admin)

## ✅ Completed & Working

### Frontend
- ✅ Blog system with category filtering
- ✅ Clean card design (category tag animates on hover)
- ✅ Testimonials infinite scroll ticker
- ✅ All sections responsive and optimized
- ✅ No focus/active outlines on links

### Strapi CMS (Integrated)
- ✅ Docker setup with PostgreSQL
- ✅ Content Types: Blog Post, Service, Testimonial
- ✅ Public permissions configured
- ✅ Frontend consuming Strapi API
- ✅ Fallback to static posts if API fails

### Infrastructure
- ✅ Docker Compose for local development
- ✅ Environment variables configured
- ✅ Strapi API endpoint: `/blog-posts`
- ✅ ISR (Incremental Static Regeneration) configured

## 🚀 Ready for Deploy

### Local Development
```bash
# Start Strapi CMS
docker compose up -d

# Start Next.js Frontend
cd frontend
npm run dev
```

### Production Deployment Checklist
- [ ] Update environment variables for production
- [ ] Configure production database (PostgreSQL)
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure Nginx reverse proxy
- [ ] Set up automatic backups
- [ ] Generate new Strapi secrets
- [ ] Deploy Docker containers on VPS
- [ ] Configure domain DNS
- [ ] Test all integrations

### Environment Variables for Production
```env
# Strapi (.env)
NODE_ENV=production
DATABASE_PASSWORD=[strong-password]
APP_KEYS=[generate-new-keys]
API_TOKEN_SALT=[generate-new-salt]
ADMIN_JWT_SECRET=[generate-new-secret]
JWT_SECRET=[generate-new-secret]

# Frontend (.env.local)
NEXT_PUBLIC_STRAPI_URL=https://cms.aumivet.com.br
NEXT_PUBLIC_SITE_URL=https://aumivet.com.br
```