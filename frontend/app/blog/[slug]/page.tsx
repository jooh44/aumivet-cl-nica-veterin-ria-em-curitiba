import Link from 'next/link';
import { notFound } from 'next/navigation';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { Calendar, User, Tag, ArrowLeft, MessageCircle, Share2, Clock } from 'lucide-react';
import Image from 'next/image';
import { getBlogPostBySlug, getStrapiImageUrl } from '@/lib/strapi';

// Placeholder data (fallback)
const placeholderPosts: Record<string, any> = {
  'saude-bucal-caes': {
    title: 'Como Cuidar da Saúde Bucal do seu Cão',
    content: `
      <p>A saúde bucal é um aspecto fundamental do bem-estar geral do seu cão. Problemas dentários não tratados podem levar a doenças graves e afetar outros órgãos.</p>
      
      <h2>Por que a Saúde Bucal é Importante?</h2>
      <p>Aproximadamente 80% dos cães acima de 3 anos apresentam algum tipo de doença periodontal. Quando não tratada, pode causar:</p>
      <ul>
        <li>Dor e desconforto ao comer</li>
        <li>Perda de dentes</li>
        <li>Infecções que podem atingir coração, fígado e rins</li>
        <li>Mau hálito persistente</li>
      </ul>

      <h2>Dicas de Cuidados Diários</h2>
      <p>Prevenir é sempre melhor que remediar. Siga estas orientações:</p>
      <ol>
        <li><strong>Escovação regular:</strong> Idealmente diária, usando pasta dental específica para cães</li>
        <li><strong>Brinquedos dentais:</strong> Auxiliam na limpeza mecânica dos dentes</li>
        <li><strong>Alimentação adequada:</strong> Ração de qualidade contribui para a saúde bucal</li>
        <li><strong>Check-ups regulares:</strong> Consultas periódicas com veterinário</li>
      </ol>

      <h2>Sinais de Problemas</h2>
      <p>Fique atento aos seguintes sintomas:</p>
      <ul>
        <li>Mau hálito intenso</li>
        <li>Gengivas vermelhas ou sangrando</li>
        <li>Dificuldade para comer</li>
        <li>Acúmulo de tártaro (placa amarelada)</li>
        <li>Perda de apetite</li>
      </ul>

      <h2>Quando Procurar o Veterinário</h2>
      <p>Se notar qualquer dos sinais acima, agende uma consulta. Na Aumivet, oferecemos serviços completos de odontologia veterinária, incluindo limpeza dentária (profilaxia), extrações e tratamento de doenças periodontais.</p>
    `,
    excerpt: 'A saúde bucal é fundamental para o bem-estar geral do seu pet.',
    category: 'Saúde',
    date: '2025-01-15',
    author: 'Dra. Thaise',
    image: 'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&q=80',
    readTime: '5 min',
  },
  'vacinas-pets': {
    title: 'Vacinação: Tudo que Você Precisa Saber',
    content: `
      <p>A vacinação é uma das medidas mais importantes para proteger seu pet contra doenças graves e potencialmente fatais.</p>
      
      <h2>Vacinas Essenciais para Cães</h2>
      <ul>
        <li><strong>V10 ou V8:</strong> Protege contra cinomose, parvovirose, coronavirose, hepatite, entre outras</li>
        <li><strong>Antirrábica:</strong> Obrigatória por lei, previne a raiva</li>
        <li><strong>Tosse dos Canis:</strong> Importante para cães que frequentam ambientes com outros animais</li>
        <li><strong>Leishmaniose:</strong> Recomendada em áreas endêmicas</li>
      </ul>

      <h2>Calendario de Vacinação</h2>
      <p>O protocolo varia conforme idade, estilo de vida e região. Durante a consulta na Aumivet, elaboramos um calendário personalizado de vacinação.</p>
    `,
    excerpt: 'Manter o calendário de vacinação em dia é essencial.',
    category: 'Prevenção',
    date: '2025-01-10',
    author: 'Dra. Thaise',
    image: 'https://images.unsplash.com/photo-1628009368231-7bb7cfcb0def?w=800&q=80',
    readTime: '4 min',
  },
  'alimentacao-gatos': {
    title: 'Alimentação Saudável para Gatos',
    content: `
      <p>Uma dieta balanceada é a base para a saúde do seu gato. Conheça os nutrientes essenciais e como escolher a melhor ração.</p>
      
      <h2>Necessidades Nutricionais dos Gatos</h2>
      <p>Gatos são carnívoros obrigatórios e precisam de proteína animal de alta qualidade em sua dieta.</p>
    `,
    excerpt: 'Uma dieta balanceada é a base para a saúde do seu gato.',
    category: 'Nutrição',
    date: '2025-01-05',
    author: 'Dr. Gustavo',
    image: 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800&q=80',
    readTime: '6 min',
  },
  'cirurgias-veterinarias': {
    title: 'Cirurgias Veterinárias: O que Esperar',
    content: `
      <p>Entenda como funcionam os procedimentos cirúrgicos na Aumivet e como preparar seu pet para uma cirurgia segura.</p>
      
      <h2>Segurança em Primeiro Lugar</h2>
      <p>Na Aumivet, seguimos rigorosos protocolos de segurança para garantir o bem-estar do seu pet durante qualquer procedimento cirúrgico.</p>
      
      <h2>Pré-operatório</h2>
      <ul>
        <li>Exames de sangue completos</li>
        <li>Avaliação cardiológica (quando necessário)</li>
        <li>Jejum adequado (conforme orientação veterinária)</li>
      </ul>

      <h2>Pós-operatório</h2>
      <p>O cuidado após a cirurgia é tão importante quanto o procedimento em si. Fornecemos todas as orientações para uma recuperação tranquila em casa.</p>
    `,
    excerpt: 'Entenda como funcionam os procedimentos cirúrgicos na Aumivet e como preparar seu pet para uma cirurgia segura.',
    category: 'Saúde',
    date: '2024-12-28',
    author: 'Dra. Thaise',
    image: 'https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=800&q=80',
    readTime: '7 min',
  },
  'adestramento-tecnicas': {
    title: 'Adestramento: Técnicas Positivas',
    content: `
      <p>Aprenda técnicas de adestramento positivo para melhorar o comportamento do seu pet e fortalecer o vínculo com ele.</p>
      
      <h2>O que é Reforço Positivo?</h2>
      <p>O reforço positivo consiste em recompensar os comportamentos desejados, incentivando o animal a repeti-los. É uma forma ética e eficaz de educar.</p>
      
      <h2>Dicas Básicas</h2>
      <ul>
        <li>Use petiscos ou brinquedos como recompensa</li>
        <li>Mantenha as sessões de treino curtas e divertidas</li>
        <li>Seja consistente nos comandos</li>
        <li>Tenha paciência e respeite o tempo do seu pet</li>
      </ul>
    `,
    excerpt: 'Aprenda técnicas de adestramento positivo para melhorar o comportamento do seu pet e fortalecer o vínculo com ele.',
    category: 'Comportamento',
    date: '2024-12-20',
    author: 'Equipe Aumivet',
    image: 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800&q=80',
    readTime: '5 min',
  },
  'banho-tosa-cuidados': {
    title: 'Banho e Tosa: Cuidados Essenciais',
    content: `
      <p>Saiba quando e como dar banho no seu pet, escolher produtos adequados e manter a higiene em dia.</p>
      
      <h2>Frequência dos Banhos</h2>
      <p>A frequência ideal depende da raça, tipo de pelagem e estilo de vida do animal. Em geral, cães podem tomar banho a cada 15 dias ou mensalmente.</p>
      
      <h2>Escolha dos Produtos</h2>
      <p>Utilize sempre shampoos e condicionadores específicos para uso veterinário. O pH da pele dos animais é diferente do nosso, e produtos humanos podem causar alergias.</p>
      
      <h2>A Importância da Tosa</h2>
      <p>Além da estética, a tosa ajuda a manter a higiene, evita nós que podem machucar a pele e facilita a visualização de ectoparasitas (pulgas e carrapatos).</p>
    `,
    excerpt: 'Saiba quando e como dar banho no seu pet, escolher produtos adequados e manter a higiene em dia.',
    category: 'Dicas',
    date: '2024-12-15',
    author: 'Equipe Aumivet',
    image: 'https://images.unsplash.com/photo-1544568104-5b7eb8189dd4?w=800&q=80',
    readTime: '4 min',
  },
};

export function generateStaticParams() {
  return Object.keys(placeholderPosts).map((slug) => ({
    slug,
  }));
}

const categoryLabels: Record<string, string> = {
  'saude': 'Saúde',
  'prevencao': 'Prevenção',
  'nutricao': 'Nutrição',
  'comportamento': 'Comportamento',
  'dicas': 'Dicas'
};

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;

  // Try to fetch from Strapi first
  try {
    const strapiPost = await getBlogPostBySlug(slug);
    if (strapiPost) {
      return {
        title: strapiPost.Title,
        description: strapiPost.Excerpt || strapiPost.Content.substring(0, 160),
        openGraph: {
          title: strapiPost.Title,
          description: strapiPost.Excerpt || strapiPost.Content.substring(0, 160),
          type: "article",
          publishedTime: strapiPost.Publishedat,
          authors: [strapiPost.Author],
        },
      };
    }
  } catch (error) {
    console.error('Error fetching post from Strapi:', error);
  }

  // Fallback to placeholder
  const post = placeholderPosts[slug];

  if (!post) {
    return {
      title: "Post não encontrado",
    };
  }

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: "article",
      publishedTime: post.date,
      authors: [post.author],
    },
  };
}

export default async function BlogPostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;

  // Try to fetch from Strapi first
  let postData = null;
  try {
    const strapiPost = await getBlogPostBySlug(slug);
    if (strapiPost) {
      // Handle readTime - can be number or string
      const readTimeValue = typeof strapiPost.Readtime === 'string'
        ? strapiPost.Readtime
        : `${strapiPost.Readtime} min`;

      postData = {
        title: strapiPost.Title,
        content: strapiPost.Content,
        excerpt: strapiPost.Excerpt,
        category: categoryLabels[strapiPost.Category] || strapiPost.Category,
        date: strapiPost.Publishedat || strapiPost.published_at,
        author: strapiPost.Author,
        image: strapiPost.Featuredimage
          ? getStrapiImageUrl(strapiPost.Featuredimage.url)
          : 'https://images.unsplash.com/photo-1548681528-6a5c45b66b42?w=800&q=80',
        readTime: readTimeValue,
      };
    }
  } catch (error) {
    console.error('Error fetching post from Strapi:', error);
  }

  // Fallback to placeholder posts
  const post = postData || placeholderPosts[slug];

  if (!post) {
    notFound();
  }

  return (
    <>
      <Header />
      <main>
        <article className="blog-post-page">
          <div className="container">
            {/* Breadcrumb */}
            <nav className="blog-breadcrumb" data-aos="fade-down">
              <Link href="/" className="breadcrumb-link">
                <ArrowLeft width={16} height={16} />
                Home
              </Link>
              <span>/</span>
              <Link href="/blog" className="breadcrumb-link">
                Blog
              </Link>
              <span>/</span>
              <span className="breadcrumb-current">{post.category}</span>
            </nav>

            {/* Post Header */}
            <header className="blog-post-header" data-aos="fade-up">
              <div className="blog-post-category-badge">
                <Tag width={14} height={14} />
                {post.category}
              </div>

              <h1 className="blog-post-title-single">{post.title}</h1>

              <div className="blog-post-meta-single">
                <div className="blog-post-author-info">
                  <User width={18} height={18} />
                  <span>{post.author}</span>
                </div>
                <div className="blog-post-date-info">
                  <Calendar width={18} height={18} />
                  <time>
                    {new Date(post.date).toLocaleDateString('pt-BR', {
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric',
                    })}
                  </time>
                </div>
                <div className="blog-post-read-info">
                  <Clock width={18} height={18} />
                  <span>{post.readTime} de leitura</span>
                </div>
              </div>
            </header>

            {/* Featured Image */}
            <div className="blog-post-featured-image" data-aos="fade-up">
              <Image src={post.image} alt={post.title} fill sizes="(max-width: 1200px) 100vw, 1200px" priority />
            </div>

            {/* Post Content */}
            <div className="blog-post-content-wrapper">
              <div
                className="blog-post-content"
                data-aos="fade-up"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Author Bio */}
              <div className="blog-post-author-bio" data-aos="fade-up">
                <div className="author-bio-avatar">
                  <User width={32} height={32} />
                </div>
                <div className="author-bio-content">
                  <h3>Sobre {post.author}</h3>
                  <p>
                    Médica Veterinária formada pela PUCPR, com especialização em anestesiologia e cirurgia
                    veterinária. Fundadora da Aumivet Clínica Veterinária.
                  </p>
                </div>
              </div>

              {/* Share Section */}
              <div className="blog-post-share" data-aos="fade-up">
                <span className="share-label">
                  <Share2 width={18} height={18} />
                  Compartilhar este post:
                </span>
                <div className="share-buttons">
                  <a
                    href={`https://wa.me/?text=${encodeURIComponent(post.title + ' - https://aumivet.com.br/blog/' + slug)}`}
                    target="_blank"
                    rel="noopener"
                    className="share-button whatsapp"
                  >
                    <MessageCircle width={18} height={18} />
                    WhatsApp
                  </a>
                  <a
                    href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent('https://aumivet.com.br/blog/' + slug)}`}
                    target="_blank"
                    rel="noopener"
                    className="share-button facebook"
                  >
                    Facebook
                  </a>
                </div>
              </div>

              {/* CTA */}
              <div className="blog-post-cta" data-aos="fade-up">
                <h2>Precisa de Atendimento Veterinário?</h2>
                <p>Agende uma consulta com nossa equipe especializada</p>
                <a
                  href="https://wa.me/5541988604202?text=Olá! Vi o blog e gostaria de agendar uma consulta."
                  className="service-button secondary"
                  target="_blank"
                  rel="noopener"
                >
                  <MessageCircle width={20} height={20} />
                  Agendar Consulta
                </a>
              </div>
            </div>
          </div>
        </article>

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

      {/* Schema.org BlogPosting */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'BlogPosting',
            headline: post.title,
            description: post.excerpt,
            datePublished: post.date,
            author: {
              '@type': 'Person',
              name: post.author,
              jobTitle: 'Médica Veterinária',
            },
            publisher: {
              '@type': 'Organization',
              name: 'Aumivet',
              logo: {
                '@type': 'ImageObject',
                url: 'https://aumivet.com.br/logo.png',
              },
            },
          }),
        }}
      />
    </>
  );
}
