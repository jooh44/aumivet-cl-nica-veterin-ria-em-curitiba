/**
 * Strapi v3 Type Definitions
 * 
 * Note: Currently not imported anywhere, but kept for future reference.
 * The blog/page.tsx uses its own local BlogPost interface.
 */

// Strapi v3 API Response
export interface StrapiResponse<T> {
  data: T;
}

// Blog Post (matches Strapi content type)
export interface BlogPost {
  id: number;
  Title: string;
  Slug: string;
  Content: string;
  Excerpt: string;
  Category: 'saude' | 'prevencao' | 'nutricao' | 'comportamento' | 'dicas';
  Author: string;
  Readtime: number;
  Publishedat: string;
  Featuredimage?: {
    id: number;
    url: string;
    name: string;
    alternativeText?: string;
  };
  created_at: string;
  updated_at: string;
  published_at: string;
}

// Service (matches Strapi content type)
export interface Service {
  id: number;
  Title: string;
  Slug: string;
  Description: string;
  Icon?: string;
  Order: number;
  Featuredimage?: {
    id: number;
    url: string;
    name: string;
    alternativeText?: string;
  };
}

// Testimonial (matches Strapi content type)
export interface Testimonial {
  id: number;
  Authorname: string;
  Petname: string;
  Content: string;
  Rating: number;
  Order: number;
}
