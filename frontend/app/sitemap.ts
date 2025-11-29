import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://aumivet.com.br';

  // Páginas estáticas
  const routes = ['', '/sobre', '/servicos', '/contato', '/blog'].map(
    (route) => ({
      url: `${baseUrl}${route}`,
      lastModified: new Date().toISOString(),
      changeFrequency: 'weekly' as const,
      priority: route === '' ? 1 : 0.8,
    })
  );

  // TODO: Adicionar posts dinâmicos do Strapi quando integrado
  const blogPosts = [
    '/blog/saude-bucal-caes',
    '/blog/vacinas-pets',
    '/blog/alimentacao-gatos',
  ].map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date().toISOString(),
    changeFrequency: 'monthly' as const,
    priority: 0.6,
  }));

  return [...routes, ...blogPosts];
}
