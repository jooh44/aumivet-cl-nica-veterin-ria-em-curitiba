# Aumivet Frontend

Redesign local em Astro para reconstruir a home a partir do Figma, mantendo por enquanto apenas:

- hero;
- serviços.

## Stack

- Astro estático;
- CSS próprio em `src/styles/global.css`;
- `lucide-astro` para ícones;
- GSAP para entrada refinada;
- Lenis para scroll suave.

## Desenvolvimento

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Fonte visual

Figma: `https://www.figma.com/design/eIGmItv6LdatT0BOoMfKvj/Aumivet?node-id=19-9034`

O bloco `carinho` usa texto real em HTML com `Style Script`, reforço ótico por CSS e sublinhado SVG vetorial para se aproximar do manuscrito do mockup sem sacrificar acessibilidade/SEO.
