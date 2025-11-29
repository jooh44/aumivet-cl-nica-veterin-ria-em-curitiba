'use client';

import { Stethoscope, Calendar, Phone, MessageCircle } from 'lucide-react';
import Image from 'next/image';
import { useEffect } from 'react';

const services = [
  {
    id: 1,
    title: 'Consulta com Especialistas',
    subtitle: 'Atendimento com Veterinários Especializados',
    description: 'Oferecemos consultas com médicos veterinários especialistas para diagnósticos e tratamentos mais complexos. Seu pet recebe o cuidado especializado que merece.',
    targetTitle: 'Especialidades:',
    targetList: ['Oncologia', 'Ortopedia', 'Cardiologia', 'Oftalmologia', 'Odontologia', 'Dermatologia'],
    linkText: 'Agendar Consulta',
    linkUrl: 'https://wa.me/5541988604202?text=Olá! Preciso de consulta com especialista.',
    icon: Calendar,
  },
  {
    id: 2,
    title: 'Anestesista Volante',
    subtitle: 'Segurança Anestésica Onde Você Precisar',
    description: 'Dr. Gustavo Trevisan disponível como anestesista especializado para procedimentos em outras clínicas. Experiência em anestesia inalatória e monitoramento avançado.',
    targetTitle: 'Inclui:',
    targetList: ['Avaliação pré-anestésica', 'Monitoramento trans-operatório', 'Protocolos personalizados'],
    linkText: 'Solicitar',
    linkUrl: 'https://wa.me/5541988604202?text=Olá! Preciso de anestesista para procedimento.',
    icon: Phone,
  },
  {
    id: 3,
    title: 'Cirurgiã Volante',
    subtitle: 'Expertise Cirúrgica em Sua Clínica',
    description: 'Serviço de cirurgia especializada para procedimentos complexos. Levamos nossa experiência até você, com técnica apurada e cuidado excepcional.',
    targetTitle: 'Especialidades:',
    targetList: ['Cirurgias de tecidos moles', 'Procedimentos ortopédicos', 'Emergências cirúrgicas'],
    linkText: 'Consultar',
    linkUrl: 'https://wa.me/5541988604202?text=Olá! Preciso de cirurgia para procedimento.',
    icon: MessageCircle,
  },
];

export default function SpecializedSection() {
  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  return (
    <section id="servicos-especializados" className="specialized-section" style={{ background: 'var(--branco)' }}>
      <div className="container">
        <div className="section-header" data-aos="fade-up">
          <div className="section-badge">
            <Stethoscope width={16} height={16} />
            <span>Serviços Especializados</span>
          </div>
          <h2 className="section-title">
            Serviços <em className="destaque">Especializados</em>
          </h2>
          <p className="section-description">
            Consultas com especialistas e serviços volantes para cuidados avançados.
          </p>
        </div>

        <div className="specialized-grid">
          {services.map((service) => (
            <div key={service.id} className="specialized-card" data-aos="fade-up">
              <div className="specialized-icon">
                <Image
                  src="/images/aumivet-clinica-veterinaria-em-curitiba-cruz.png"
                  alt={`Aumivet - ${service.title}`}
                  className="specialized-image"
                  width={80}
                  height={80}
                  loading="lazy"
                />
              </div>
              <div className="specialized-content">
                <h3>{service.title}</h3>
                <h4>{service.subtitle}</h4>
                <p>{service.description}</p>
                <div className="specialized-target">
                  <strong>{service.targetTitle}</strong>
                  <ul>
                    {service.targetList.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
                <a href={service.linkUrl} className="specialized-link" target="_blank" rel="noopener">
                  <span>{service.linkText}</span>
                  <service.icon width={16} height={16} />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
