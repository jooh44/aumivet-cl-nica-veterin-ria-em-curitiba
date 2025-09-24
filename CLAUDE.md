# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Aumivet Veterinary Clinic** website - a static HTML/CSS landing page for a veterinary clinic in Curitiba, Brazil. The site is a single-page application showcasing the clinic's services, team, and contact information.

## Architecture & Structure

- **Static HTML/CSS Site**: No build process or package dependencies
- **Single Page Application**: Everything contained in `index.html`
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox
- **No Framework**: Pure HTML, CSS, and minimal JavaScript for animations

### File Structure
```
/
├── index.html          # Main HTML file with all page content
├── styles.css          # Complete stylesheet with design system
├── images/             # Image assets
│   ├── logo-aumivet.png
│   ├── aumivet_clinica_veterinaria_em_curitiba.jpg
│   └── aumivet-*.png   # Service-specific images for each category
├── instruções.md       # Detailed content and SEO instructions (Portuguese)
├── design-principles.md # Design system guidelines
├── ajustes-hero.md     # Specific hero section adjustments
├── design-review-agent.md # Design review documentation
├── design-review-slash-command.md # Design review commands
└── .claude/            # Claude Code configuration
```

## Design System

### Color Palette (CSS Variables)
- `--branco: #FFFFF2` - Main background color
- `--rosa: #E66884` - Accent color for highlights and vectors
- `--verde: #9CA876` - Primary button color
- `--verde-claro: #B6D455` - Button hover state
- `--preto: #1f1f1f` - Main text color
- `--cinza: rgb(29, 29, 29)` - Body text color

### Typography Hierarchy
- **Destaque/Special phrases**: `'Playfair Display', serif` (italic, weight 400)
- **Títulos/Headers**: `'Poppins', sans-serif`
- **Corpo/Body text**: `'Inter', sans-serif`

### Key Components
- **Hero section** with ticker animation
- **Responsive navigation** with logo
- **Service cards** with icons
- **Team section** featuring Dra. Thaise
- **Testimonials** with Google Reviews
- **Contact section** with Schema markup

## Important Implementation Notes

### Hero Section Specifics
- Remove hero-features, move ticker to hero viewport for optimization
- Increase logo size in nav without stretching navigation height
- Button should be solid green (`--verde`) with light green hover (`--verde-claro`)
- Ticker services should be in badges with more spacing
- Use `.destaque` class for italic Playfair Display highlights in titles

### SEO Requirements
- Comprehensive Schema.org markup for VeterinaryCare
- Optimized meta tags for local Curitiba veterinary searches
- Semantic HTML structure with proper heading hierarchy
- Internal linking structure defined in instruções.md

### Performance Guidelines
- Lazy loading for images
- Critical CSS inline for first 14KB
- Preload fonts and hero images
- Mobile-first responsive approach
- Core Web Vitals optimization (LCP < 2.5s target)

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

Since this is a static site with no build process:
1. Edit HTML/CSS files directly
2. Test in browser with live server
3. Check responsiveness across breakpoints: 320px, 768px, 1024px, 1200px
4. Validate HTML and run accessibility checks
5. No linting/testing commands - manual browser testing required

## Common Tasks

- **Local development**: Use any live server (VS Code Live Server extension recommended)
- **Image optimization**: Compress images in `/images/` directory
- **Content updates**: Refer to `instruções.md` for copy and SEO guidelines
- **Design changes**: Follow color system and typography rules in CSS variables