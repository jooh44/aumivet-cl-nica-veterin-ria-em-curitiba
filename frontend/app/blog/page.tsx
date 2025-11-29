'use client';

import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { BookOpen, Calendar, Tag, ArrowRight, MessageCircle } from 'lucide-react';
import Image from 'next/image';
import { useState, useEffect } from 'react';

// Mapeamento de categorias sem acento para exibição
const categoryLabels: Record<string, string> = {
  saude: 'Saúde',
  prevencao: 'Prevenção',
  nutricao: 'Nutrição',
  comportamento: 'Comportamento',
  dicas: 'Dicas',
};

const staticBlogPosts = [
  {
    id: 1,
    title: 'Como Cuidar da Saúde Bucal do seu Cão',
    excerpt:
      'A saúde bucal é fundamental para o bem-estar geral do seu pet. Descubra dicas essenciais para manter os dentes do seu cão limpos e saudáveis.',
    slug: 'saude-bucal-caes',
    category: 'Saúde',
    date: '2025-01-15',
    author: 'Dra. Thaise',
    image: 'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&q=80',
    readTime: '5 min',
  },
  {
    id: 2,
    title: 'Vacinação: Tudo que Você Precisa Saber',
    excerpt:
      'Manter o calendário de vacinação em dia é essencial para proteger seu pet de doenças graves. Entenda a importância de cada vacina.',
    slug: 'vacinas-pets',
    category: 'Prevenção',
    date: '2025-01-10',
    author: 'Dra. Thaise',
    image: 'https://images.unsplash.com/photo-1628009368231-7bb7cfcb0def?w=800&q=80',
    readTime: '4 min',
  },
  {
    id: 3,
    title: 'Alimentação Saudável para Gatos',
    excerpt:
      'Uma dieta balanceada é a base para a saúde do seu gato. Conheça os nutrientes essenciais e como escolher a melhor ração.',
    slug: 'alimentacao-gatos',
    category: 'Nutrição',
    date: '2025-01-05',
    author: 'Dr. Gustavo',
    image: 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800&q=80',
    readTime: '6 min',
  },
  {
    id: 4,
    title: 'Cirurgias Veterinárias: O que Esperar',
    excerpt:
      'Entenda como funcionam os procedimentos cirúrgicos na Aumivet e como preparar seu pet para uma cirurgia segura.',
    slug: 'cirurgias-veterinarias',
    category: 'Saúde',
    date: '2024-12-28',
    author: 'Dra. Thaise',
    image: 'https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=800&q=80',
    readTime: '7 min',
  },
  {
    id: 5,
    title: 'Adestramento: Técnicas Positivas',
    excerpt:
      'Aprenda técnicas de adestramento positivo para melhorar o comportamento do seu pet e fortalecer o vínculo com ele.',
    slug: 'adestramento-tecnicas',
    category: 'Comportamento',
    date: '2024-12-20',
    author: 'Equipe Aumivet',
    image: 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800&q=80',
    readTime: '5 min',
  },
  {
    id: 6,
    title: 'Banho e Tosa: Cuidados Essenciais',
    excerpt:
      'Saiba quando e como dar banho no seu pet, escolher produtos adequados e manter a higiene em dia.',
    slug: 'banho-tosa-cuidados',
    category: 'Dicas',
    date: '2024-12-15',
    author: 'Equipe Aumivet',
    image: 'https://images.unsplash.com/photo-1544568104-5b7eb8189dd4?w=800&q=80',
    readTime: '4 min',
  },
];

const categories = ['Todos', 'Saúde', 'Prevenção', 'Nutrição', 'Comportamento', 'Dicas'];

interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  category: string;
  author: string;
  readTime: string;
  date: string;
  image: string;
  publishedat?: string;
  featuredimage?: any;
}

export default function BlogPage() {
  const [selectedCategory, setSelectedCategory] = useState('Todos');
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Buscar posts do Strapi
    const STRAPI_URL = process.env.NEXT_PUBLIC_STRAPI_URL || 'https://strapi.digitaldog.pet';
    fetch(`${STRAPI_URL}/blog-posts`)
      .then((res) => res.json())
      .then((data) => {
        const posts = data.map((post: any) => ({
          id: post.id,
          title: post.Title,
          slug: post.Slug,
          excerpt: post.Excerpt || '',
          category: categoryLabels[post.Category] || post.Category,
          author: post.Author || 'Dra. Thaise',
          readTime: post.Readtime || '5 min',
          date: post.Publishedat || post.published_at || new Date().toISOString(),
          image: post.Featuredimage?.url
            ? `${STRAPI_URL}${post.Featuredimage.url}`
            : 'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&q=80',
        }));
        
        console.log('Posts do Strapi:', posts); // Debug
        
        // Combinar posts do Strapi com estáticos
        setBlogPosts([...posts, ...staticBlogPosts]);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Erro ao buscar posts:', error);
        // Em caso de erro, usar posts estáticos
        setBlogPosts(staticBlogPosts);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, [selectedCategory]);

  const filteredPosts =
    selectedCategory === 'Todos'
      ? blogPosts
      : blogPosts.filter((post) => post.category === selectedCategory);

  return (
    <>
      <Header />
      <main>
        {/* Hero Section */}
        <section className="blog-hero-section">
          <div className="container">
            <div className="blog-hero-content">
              <div className="section-badge">
                <BookOpen width={16} height={16} />
                <span>Blog Aumivet</span>
              </div>
              <h1 className="section-title">
                Dicas e Cuidados para <em className="destaque">Seu Pet</em>
              </h1>
              <p className="section-description">
                Conteúdos exclusivos sobre saúde, comportamento e bem-estar animal
              </p>
            </div>
          </div>
        </section>

        {/* Categories Filter */}
        <section className="blog-categories-section">
          <div className="container">
            <div className="blog-categories">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`category-button ${selectedCategory === category ? 'active' : ''}`}
                >
                  <Tag width={16} height={16} />
                  {category}
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Blog Posts Grid */}
        <section className="blog-posts-section">
          <div className="container">
            <div className="blog-posts-grid">
              {filteredPosts.map((post) => (
                <article key={post.slug} className="blog-post-card">
                  <Link href={`/blog/${post.slug}`} className="blog-post-image-link">
                    <div className="blog-post-image">
                      <Image src={post.image} alt={post.title} fill sizes="(max-width: 768px) 100vw, 33vw" />
                      <div className="blog-post-category">
                        <Tag width={14} height={14} />
                        {post.category}
                      </div>
                    </div>
                  </Link>

                  <div className="blog-post-content">
                    <div className="blog-post-meta">
                      <span className="blog-post-date">
                        <Calendar width={14} height={14} />
                        {new Date(post.date).toLocaleDateString('pt-BR')}
                      </span>
                      <span className="blog-post-read-time">{post.readTime} de leitura</span>
                    </div>

                    <h3 className="blog-post-title">
                      <Link href={`/blog/${post.slug}`}>{post.title}</Link>
                    </h3>

                    <p className="blog-post-excerpt">{post.excerpt}</p>

                    <div className="blog-post-footer">
                      <span className="blog-post-author">Por {post.author}</span>
                      <Link href={`/blog/${post.slug}`} className="blog-post-read-more">
                        Ler mais
                        <ArrowRight width={16} height={16} />
                      </Link>
                    </div>
                  </div>
                </article>
              ))}
            </div>

            {filteredPosts.length === 0 && (
              <div className="blog-empty-state">
                <BookOpen width={48} height={48} />
                <h3>Nenhum post encontrado</h3>
                <p>Não há posts nesta categoria ainda. Volte em breve para novos conteúdos!</p>
              </div>
            )}
          </div>
        </section>

        {/* CTA Section */}
        <section className="blog-cta-section">
          <div className="container">
            <div className="blog-cta-content">
              <h2>Ficou com alguma dúvida?</h2>
              <p>Nossa equipe está pronta para ajudar você e seu pet</p>
              <a
                href="https://wa.me/5541988604202?text=Olá! Vi o blog e tenho algumas dúvidas."
                className="service-button secondary"
                target="_blank"
                rel="noopener"
              >
                <MessageCircle width={20} height={20} />
                Falar com a Aumivet
              </a>
            </div>
          </div>
        </section>

        {/* WhatsApp Float Button */}
        <a
          href="https://wa.me/5541988604202?text=Olá! Gostaria de mais informações"
          className="whatsapp-float"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Falar no WhatsApp"
        >
          <MessageCircle size={28} />
        </a>
      </main>
      <Footer />
    </>
  );
}
