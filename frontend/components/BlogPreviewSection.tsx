'use client';

import Link from 'next/link';
import Image from 'next/image';
import { BookOpen, Calendar, ArrowRight, Tag } from 'lucide-react';
import { useEffect } from 'react';

const featuredPosts = [
  {
    id: 1,
    title: 'Como Cuidar da Saúde Bucal do seu Cão',
    excerpt:
      'A saúde bucal é fundamental para o bem-estar geral do seu pet. Descubra dicas essenciais para manter os dentes do seu cão limpos.',
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
];

export default function BlogPreviewSection() {
  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  return (
    <section id="blog" className="blog-preview-section">
      <div className="container">
        <div className="section-header" data-aos="fade-up">
          <div className="section-badge">
            <BookOpen width={16} height={16} />
            <span>Blog Aumivet</span>
          </div>
          <h2 className="section-title">
            Dicas e Cuidados para <em className="destaque">Seu Pet</em>
          </h2>
          <p className="section-description">
            Conteúdos exclusivos sobre saúde, comportamento e bem-estar animal
          </p>
        </div>

        <div className="blog-preview-grid">
          {featuredPosts.map((post) => (
            <article key={post.id} className="blog-preview-card" data-aos="fade-up">
              <Link href={`/blog/${post.slug}`} className="blog-preview-image-link">
                <div className="blog-preview-image">
                  <Image
                    src={post.image}
                    alt={post.title}
                    fill
                    sizes="(max-width: 768px) 100vw, 33vw"
                  />
                  <div className="blog-preview-category">
                    <Tag width={14} height={14} />
                    {post.category}
                  </div>
                </div>
              </Link>

              <div className="blog-preview-content">
                <div className="blog-preview-meta">
                  <span className="blog-preview-date">
                    <Calendar width={14} height={14} />
                    {new Date(post.date).toLocaleDateString('pt-BR')}
                  </span>
                  <span className="blog-preview-read-time">{post.readTime}</span>
                </div>

                <h3 className="blog-preview-title">
                  <Link href={`/blog/${post.slug}`}>{post.title}</Link>
                </h3>

                <p className="blog-preview-excerpt">{post.excerpt}</p>

                <div className="blog-preview-footer">
                  <span className="blog-preview-author">Por {post.author}</span>
                  <Link href={`/blog/${post.slug}`} className="blog-preview-read-more">
                    Ler mais
                    <ArrowRight width={16} height={16} />
                  </Link>
                </div>
              </div>
            </article>
          ))}
        </div>

        <div className="blog-preview-cta" data-aos="fade-up">
          <Link href="/blog" className="service-button secondary">
            Ver Todos os Posts
            <ArrowRight width={20} height={20} />
          </Link>
        </div>
      </div>
    </section>
  );
}
