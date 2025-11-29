'use client';

import { 
  Award, CalendarPlus, MessageCircle,
  Stethoscope, Scissors, Droplets, Microscope,
  Sparkles, Users, Briefcase, Activity, GraduationCap, Car
} from 'lucide-react';
import Image from 'next/image';
import { useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';

export default function HeroSection() {
  useEffect(() => {
    AOS.init({
      duration: 800,
      once: true,
    });
  }, []);

  return (
    <section className="hero-section">
      <div className="container">
        <div className="hero-content">
          <div className="hero-text">
            <div className="hero-badge" data-aos="fade-right">
              <Award width={16} height={16} />
              <span>Clínica Veterinária em Curitiba</span>
            </div>
            <h1 className="hero-title" data-aos="fade-right">
              Na Aumivet, nós Cuidamos com <em className="destaque">Amor</em> e Tratamos com <em className="destaque">Excelência</em>
            </h1>
            <p className="hero-description" data-aos="fade-right">
              Sua Clínica Veterinária de Confiança no <em className="destaque-rosa">Coração de Curitiba</em>
              <span className="hero-description-desktop">
                {' '}Somos uma clínica veterinária moderna no bairro Rebouças, especializada em cães e gatos, com foco no bem-estar, prevenção e qualidade de vida.
              </span>
            </p>

            <div className="hero-cta-group" data-aos="fade-up" data-aos-delay="300">
              <a 
                href="https://wa.me/5541988604202?text=Olá! Gostaria de agendar uma consulta." 
                className="hero-cta-primary" 
                target="_blank" 
                rel="noopener noreferrer"
              >
                <CalendarPlus width={20} height={20} />
                Agendar Consulta
              </a>
              <a 
                href="https://wa.me/5541988604202?text=Olá! Tenho dúvidas sobre os serviços." 
                className="hero-cta-secondary" 
                target="_blank" 
                rel="noopener noreferrer"
              >
                <MessageCircle width={20} height={20} />
                Tire suas Dúvidas
              </a>
            </div>
          </div>
          <div className="hero-visual">
            <div className="hero-image-container">
              <Image 
                src="/images/aumivet_clinica_veterinaria_em_curitiba.jpg" 
                alt="Aumivet - Clínica Veterinária em Curitiba" 
                width={600} 
                height={400}
                className="hero-image"
                priority
              />
            </div>
          </div>
        </div>

        {/* Services Ticker */}
        <HeroTicker />
      </div>
    </section>
  );
}

function HeroTicker() {
  const services = [
    { Icon: Stethoscope, label: 'Consultas Veterinárias' },
    { Icon: Scissors, label: 'Cirurgias Especializadas' },
    { Icon: Droplets, label: 'Banho e Tosa' },
    { Icon: Microscope, label: 'Exames e Diagnósticos' },
    { Icon: Sparkles, label: 'Odontologia Veterinária' },
    { Icon: Users, label: 'Parceria para Veterinários' },
    { Icon: Briefcase, label: 'Anestesista Volante' },
    { Icon: Activity, label: 'Cirurgiã Volante' },
    { Icon: GraduationCap, label: 'Adestramento Pet' },
    { Icon: Car, label: 'Leva e Traz' },
  ];

  return (
    <div className="hero-ticker">
      <div className="ticker-wrapper">
        <div className="ticker-content">
          {/* Render services twice for seamless loop */}
          {[...services, ...services].map((service, index) => {
            const IconComponent = service.Icon;
            return (
              <div key={index} className="ticker-badge">
                <IconComponent width={16} height={16} />
                <span>{service.label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
