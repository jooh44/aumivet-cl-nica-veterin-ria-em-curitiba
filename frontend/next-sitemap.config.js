/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: process.env.SITE_URL || 'https://aumivet.com.br',
  generateRobotsTxt: false, // Já temos robots.ts
  generateIndexSitemap: false,
  exclude: ['/api/*', '/admin/*'],
  changefreq: 'weekly',
  priority: 0.7,
  sitemapSize: 5000,
  transform: async (config, path) => {
    // Personalizar prioridade por tipo de página
    let priority = config.priority;
    let changefreq = config.changefreq;

    if (path === '/') {
      priority = 1.0;
      changefreq = 'daily';
    } else if (path.startsWith('/blog/') && !path.endsWith('/blog')) {
      priority = 0.6;
      changefreq = 'monthly';
    } else if (['/sobre', '/servicos', '/contato'].includes(path)) {
      priority = 0.8;
      changefreq = 'weekly';
    }

    return {
      loc: path,
      changefreq,
      priority,
      lastmod: new Date().toISOString(),
    };
  },
};
