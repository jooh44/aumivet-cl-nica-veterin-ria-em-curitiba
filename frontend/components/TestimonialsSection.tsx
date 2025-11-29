'use client';

import { Heart } from 'lucide-react';
import { useState, useEffect } from 'react';

const testimonials = [
  {
    id: 1,
    name: 'Luiza Folda',
    source: 'Google',
    text: 'A Dra Thaise já acompanha a nossa família há anos! Sempre pronta para me auxiliar em qualquer dúvida, vacinando tanto meus cães como meus gatos. Escolho ela de olhos fechados! Me ajudou também com transporte internacional dos meus dois cães para os Estados Unidos e de volta ao Brasil! Se você quer o melhor atendimento para os seus filhos de quatro patas ela é a escolha ideal! Agora nessa nova clínica espetacular: conta com tudo de melhor e mais moderno para os seus bichinhos!',
  },
  {
    id: 2,
    name: 'Thays Kempa',
    source: 'Google',
    text: 'Super indico a Aumivet! Atendimento acolhedor, minha filha (minha gatinha) precisou fazer extração de alguns dentes e foi muito bem cuidada, com todo amor e carinho. A Dra explica tudo certinho, profissional que realmente ama o que faz e faz com amor! Sempre nos mantendo informados sobre cada procedimento, me senti segura e sabia que ela estava em boas mãos. Profissionais excelentes!',
  },
  {
    id: 3,
    name: 'Suélen Ribeiro',
    source: 'Google',
    text: 'Eu agradeço grandemente por toda equipe da Aumivet. Foram muito atenciosos e carinhosos. Chegamos angustiados com o estado do meu cachorro e eles, com toda paciência e carinho, nos acalmaram. Tiveram um cuidado gigante antes e depois da cirurgia. Foram anjos nas nossas vidas! Agradeço demais por tudo! Deus abençoe cada um de vocês!',
  },
  {
    id: 4,
    name: 'Elisangela Zembik',
    source: 'Google',
    text: 'Thaise trabalha por amor, é uma profissional diferenciada. Todo conhecimento dela foi essencial para o tratamento de diabetes do meu cão e ela mostrou uma prestatividade difícil de encontrar. Indico de olhos fechados, somos eternamente gratos! 🙏❤',
  },
  {
    id: 5,
    name: 'Marina Santos',
    source: 'Google',
    text: 'Tenho muito que agradecer à Doutora Thaise! Ela acompanha nossa família há alguns anos e já salvou várias vidas dos animais que resgatamos, sempre auxiliando com muito amor. A gratidão é enorme: nesta semana minha cachorra foi atacada e ela estava ali, pronta para ajudar. Agradeço pelo profissionalismo e pelo carinho com que cuida!',
  },
];

const GoogleIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path
      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
      fill="#4285F4"
    />
    <path
      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
      fill="#34A853"
    />
    <path
      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
      fill="#FBBC05"
    />
    <path
      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
      fill="#EA4335"
    />
  </svg>
);

export default function TestimonialsSection() {
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  useEffect(() => {
    const slider = document.querySelector('.testimonials-ticker') as HTMLElement;
    if (!slider) return;

    const handleScroll = () => {
      const scrollLeft = slider.scrollLeft;
      const itemWidth = slider.children[0]?.clientWidth || 0;
      const currentIndex = Math.round(scrollLeft / itemWidth);
      setCurrentSlide(currentIndex);
    };

    slider.addEventListener('scroll', handleScroll);
    return () => slider.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSlide = (index: number) => {
    const slider = document.querySelector('.testimonials-ticker') as HTMLElement;
    if (!slider) return;
    
    const item = slider.children[index] as HTMLElement;
    if (item) {
      item.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
  };

  return (
    <section id="testimonials" className="testimonials-section">
      <div className="container">
        <div className="section-header" data-aos="fade-up">
          <div className="section-badge">
            <Heart width={16} height={16} />
            <span>Depoimentos</span>
          </div>
          <h2 className="section-title">
            Depoimentos dos <em className="destaque">Tutores</em>
          </h2>
          <p className="section-description">O que nossos clientes dizem sobre o cuidado que oferecemos</p>
        </div>

        {/* Testimonials Ticker */}
        <div className="testimonials-ticker-container" data-aos="fade-up">
          <div className="testimonials-ticker">
            {testimonials.map((testimonial) => (
              <div key={testimonial.id} className="testimonial-item">
                <div className="testimonial-google-icon">
                  <GoogleIcon />
                </div>
                <div className="testimonial-content">
                  <h4>{testimonial.name}</h4>
                  <span className="testimonial-source">{testimonial.source}</span>
                  <p>{testimonial.text}</p>
                </div>
              </div>
            ))}
            {/* Duplicate for seamless loop */}
            {testimonials.map((testimonial) => (
              <div key={`dup-${testimonial.id}`} className="testimonial-item">
                <div className="testimonial-google-icon">
                  <GoogleIcon />
                </div>
                <div className="testimonial-content">
                  <h4>{testimonial.name}</h4>
                  <span className="testimonial-source">{testimonial.source}</span>
                  <p>{testimonial.text}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Mobile Slider Dots */}
        <div className="testimonials-slider-dots">
          {testimonials.map((_, index) => (
            <button
              key={index}
              className={`testimonials-slider-dot ${currentSlide === index ? 'active' : ''}`}
              onClick={() => scrollToSlide(index)}
              aria-label={`Ir para depoimento ${index + 1}`}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
