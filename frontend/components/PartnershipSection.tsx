'use client';

import { Handshake, ArrowRight } from 'lucide-react';
import Image from 'next/image';
import { useState, useEffect } from 'react';

const photos = [
  {
    id: 1,
    src: '/images/aumivet-clinica-veterinaria-em-curitiba (1).jpg',
    alt: 'Infraestrutura da Aumivet - ambiente de atendimento',
  },
  {
    id: 2,
    src: '/images/aumivet-clinica-veterinaria-em-curitiba (2).jpg',
    alt: 'Infraestrutura da Aumivet - sala de procedimentos',
  },
  {
    id: 3,
    src: '/images/aumivet-clinica-veterinaria-em-curitiba (3).jpg',
    alt: 'Infraestrutura da Aumivet - equipamentos veterinários',
  },
  {
    id: 4,
    src: '/images/aumivet-clinica-veterinaria-em-curitiba (4).jpg',
    alt: 'Infraestrutura da Aumivet - área de recepção',
  },
];

export default function PartnershipSection() {
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  useEffect(() => {
    const slider = document.querySelector('.partnership-slider') as HTMLElement;
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
    const slider = document.querySelector('.partnership-slider') as HTMLElement;
    if (!slider) return;
    
    const item = slider.children[index] as HTMLElement;
    if (item) {
      item.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
  };

  return (
    <section id="parcerias" className="partnership-section">
      <div className="container">
        <div className="partnership-container">
          {/* Left: Content */}
          <div className="partnership-content" data-aos="fade-right">
            <div className="section-badge">
              <Handshake width={16} height={16} />
              <span>Parcerias</span>
            </div>
            <h2 className="section-title">
              Parceria para <em className="destaque">Médicos Veterinários</em>
            </h2>
            <h3 className="partnership-subtitle">Espaço Colaborativo para Veterinários</h3>
            <p className="partnership-description">
              Oferecemos infraestrutura completa para médicos veterinários que precisam de cirurgias e internamento,
              utilizando equipamentos modernos e suporte técnico para colegas da área.
            </p>

            <div className="partnership-target">
              <strong>Para quem:</strong>
              <ul>
                <li>Veterinários autônomos</li>
                <li>Especialistas</li>
                <li>Profissionais em transição</li>
              </ul>
            </div>

            <a
              href="https://wa.me/5541988604202?text=Olá! Tenho interesse na parceria para médicos veterinários."
              className="service-button secondary"
              target="_blank"
              rel="noopener"
            >
              Saber Mais
              <ArrowRight width={20} height={20} />
            </a>
          </div>

          {/* Right: Photo Grid (Desktop) / Slider (Mobile) */}
          <div className="partnership-photos" data-aos="fade-left">
            <div className="partnership-slider">
              {photos.map((photo) => (
                <div key={photo.id} className="partnership-photo-item">
                  <Image
                    src={photo.src}
                    alt={photo.alt}
                    width={600}
                    height={450}
                    loading="lazy"
                  />
                </div>
              ))}
            </div>

            {/* Mobile Slider Dots */}
            <div className="partnership-slider-dots">
              {photos.map((_, index) => (
                <button
                  key={index}
                  className={`partnership-slider-dot ${currentSlide === index ? 'active' : ''}`}
                  onClick={() => scrollToSlide(index)}
                  aria-label={`Ir para foto ${index + 1}`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
