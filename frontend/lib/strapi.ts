/**
 * Strapi CMS Integration
 * Funções para comunicação com o Strapi headless CMS
 */

const STRAPI_URL = process.env.NEXT_PUBLIC_STRAPI_URL || "http://localhost:1337";
const STRAPI_TOKEN = process.env.STRAPI_API_TOKEN;

/**
 * Fetch genérico para Strapi API
 */
async function fetchStrapi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${STRAPI_URL}${endpoint}`;
  
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (STRAPI_TOKEN) {
    headers["Authorization"] = `Bearer ${STRAPI_TOKEN}`;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`Strapi API error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    throw error;
  }
}

/**
 * Buscar todos os posts do blog
 */
export async function getBlogPosts() {
  return fetchStrapi<any[]>("/blog-posts", {
    next: { revalidate: 3600 }, // Revalidar a cada 1 hora
  });
}

/**
 * Buscar post por slug
 */
export async function getBlogPostBySlug(slug: string) {
  const posts = await fetchStrapi<any[]>(`/blog-posts`, {
    next: { revalidate: 3600 },
  });

  return posts.find((post) => post.Slug === slug) || null;
}

/**
 * Gera URL completa para imagem do Strapi
 */
export function getStrapiImageUrl(url: string | undefined): string {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `${STRAPI_URL}${url}`;
}
