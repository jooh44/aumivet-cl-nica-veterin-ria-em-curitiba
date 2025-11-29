'use client';

import { Car, ShieldCheck, Heart, Clock, MapPin } from 'lucide-react';
import Image from 'next/image';
import { useEffect } from 'react';

export default function TaxiPetSection() {
  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  return (
    <section id="taxi-pet" className="taxi-pet-section">
      <div className="container">
        <div className="section-header" data-aos="fade-up">
          <div className="section-badge">
            <Car width={16} height={16} />
            <span>Leva e Traz</span>
          </div>
          <h2 className="section-title">
            Leva e Traz - Transporte <em className="destaque">Seguro</em> e Confortável
          </h2>
          <p className="section-description">Buscamos e levamos seu pet em segurança e muito cuidado!</p>
        </div>

        {/* Carro com badges dos benefícios */}
        <div className="taxi-pet-showcase" data-aos="fade-up">
          <div className="taxi-pet-image-container">
            <Image
              src="/images/carro-aumivet.jpg"
              alt="Carro da Aumivet - Leva e Traz Transporte Seguro para Pets"
              className="taxi-pet-image"
              width={1200}
              height={600}
              loading="lazy"
            />

            {/* Badges lado esquerdo */}
            <div className="benefit-badge left-1" data-aos="fade-right">
              <ShieldCheck width={16} height={16} />
              <span>Segurança Garantida</span>
            </div>
            <div className="benefit-badge left-2" data-aos="fade-right" data-aos-delay="100">
              <Heart width={16} height={16} />
              <span>Cuidado Especializado</span>
            </div>

            {/* Badges lado direito */}
            <div className="benefit-badge right-1" data-aos="fade-left">
              <Clock width={16} height={16} />
              <span>Pontualidade</span>
            </div>
            <div className="benefit-badge right-2" data-aos="fade-left" data-aos-delay="100">
              <MapPin width={16} height={16} />
              <span>Cobertura Ampla</span>
            </div>
          </div>
        </div>

        {/* CTA centralizado */}
        <div style={{ textAlign: 'center', marginTop: '3rem' }} data-aos="fade-up">
          <a
            href="https://wa.me/5541988604202?text=Olá! Preciso do serviço de Leva e Traz."
            className="service-button secondary taxi-pet-button"
            target="_blank"
            rel="noopener"
          >
            Solicitar Leva e Traz
            <Car width={20} height={20} />
          </a>
        </div>
      </div>
    </section>
  );
}
