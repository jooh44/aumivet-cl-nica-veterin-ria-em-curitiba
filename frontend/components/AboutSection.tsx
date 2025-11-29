'use client';

import { Building2, CalendarPlus } from 'lucide-react';
import { useEffect } from 'react';

export default function AboutSection() {
  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  return (
    <section id="about" className="about-section">
      <div className="container">
        <div className="section-header" data-aos="fade-up">
          <div className="container">
            <div className="section-badge">
              <Building2 width={16} height={16} />
              <span>Sobre a Aumivet</span>
            </div>
            <h2 className="section-title">
              Sobre a <em className="destaque">Aumivet</em>
            </h2>
            <p className="section-description">
              Mais que uma clínica veterinária, somos um centro de cuidado completo para seu pet Fundada com o
              propósito de oferecer atendimento veterinário de excelência em Curitiba, nossa missão é proporcionar
              saúde, bem-estar e qualidade de vida para cães e gatos, em um ambiente moderno e acolhedor.
            </p>
            <a href="#contato" className="about-cta-button">
              <CalendarPlus width={20} height={20} />
              Agendar Consulta
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
