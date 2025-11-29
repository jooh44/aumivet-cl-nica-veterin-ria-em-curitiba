'use client';

import { ChevronRight } from 'lucide-react';
import Image from 'next/image';
import { useEffect } from 'react';

const services = [
  {
    id: 1,
    tagline: 'Prevenção',
    title: 'Consultas e',
    destaque: 'Vacinas',
    description: 'Cuidar da saúde do seu pet começa com prevenção. Realizamos consultas clínicas completas e aplicamos vacinas essenciais com toda a segurança, carinho e atenção que eles merecem. Também oferecemos <strong>atendimento domiciliar</strong> para maior comodidade.',
    image: '/images/aumivet-consultas-e-vacinas-em-curitiba.png',
    alt: 'Consultas e Vacinas',
    whatsapp: 'https://wa.me/5541988604202?text=Olá! Gostaria de agendar uma consulta.',
    whatsappInfo: 'https://wa.me/5541988604202?text=Olá! Tenho dúvidas sobre consultas.',
    buttonText: 'Agendar',
    reverse: false,
  },
  {
    id: 2,
    tagline: 'Cirurgia',
    title: 'Cirurgias',
    destaque: 'Especializadas',
    description: 'Aqui, seu pet está em boas mãos. Nossa equipe realiza procedimentos cirúrgicos com técnica, segurança e todo o cuidado que ele merece — desde os mais simples até os mais delicados. Todas as nossas cirurgias são realizadas com anestesia inalatória por médico veterinário especialista.',
    image: '/images/aumivet-cirurgias-especializadas-veterinaria-em-curitiba.png',
    alt: 'Cirurgias Especializadas',
    whatsapp: 'https://wa.me/5541988604202?text=Olá! Preciso de informações sobre cirurgias.',
    whatsappInfo: 'https://wa.me/5541988604202?text=Olá! Tenho dúvidas sobre procedimentos cirúrgicos.',
    buttonText: 'Consultar',
    reverse: true,
  },
  {
    id: 3,
    tagline: 'Diagnóstico',
    title: 'Exames e',
    destaque: 'Diagnósticos',
    description: 'Com tecnologia de ponta e agilidade nos resultados, oferecemos exames precisos que auxiliam no diagnóstico rápido e eficaz. Porque cada detalhe importa na saúde do seu pet.',
    image: '/images/aumivet-exames-e-diagnostico-em-curitiba.png',
    alt: 'Exames e Diagnósticos',
    whatsapp: 'https://wa.me/5541988604202?text=Olá! Preciso de exames para meu pet.',
    whatsappInfo: 'https://wa.me/5541988604202?text=Olá! Tenho dúvidas sobre exames.',
    buttonText: 'Solicitar',
    reverse: false,
  },
  {
    id: 4,
    tagline: 'Saúde Bucal',
    title: 'Odontologia',
    destaque: 'Veterinária',
    description: 'Saúde bucal também é qualidade de vida. Cuidamos do sorriso do seu pet com tratamentos odontológicos especializados e sem estresse.',
    image: '/images/aumivet-odotonlogia-veterinaria-em-curitiba.png',
    alt: 'Odontologia Veterinária',
    whatsapp: 'https://wa.me/5541988604202?text=Olá! Meu pet precisa de cuidados dentários.',
    whatsappInfo: 'https://wa.me/5541988604202?text=Olá! Tenho dúvidas sobre odontologia veterinária.',
    buttonText: 'Agendar',
    reverse: true,
  },
  {
    id: 5,
    tagline: 'Comportamento',
    title: 'Adestramento',
    destaque: 'Pet',
    description: 'Transforme o dia a dia com seu pet com mais harmonia e obediência. Técnicas positivas para comportamento e socialização.',
    image: '/images/aumivet-adrestramento-em-curitiba.png',
    alt: 'Adestramento Pet',
    whatsapp: 'https://wa.me/5541988604202?text=Olá! Tenho interesse no adestramento.',
    whatsappInfo: 'https://wa.me/5541988604202?text=Olá! Tenho dúvidas sobre adestramento.',
    buttonText: 'Consultar',
    reverse: false,
  },
  {
    id: 6,
    tagline: 'Estética',
    title: 'Banho, Tosa e',
    destaque: 'Estética Pet',
    description: 'Mais que higiene: momentos de cuidado e bem-estar. Seu pet sai limpo, cheiroso e ainda mais bonito com nossos serviços de banho e tosa pensados para o conforto dele.',
    image: '/images/aumivet-banho-tosa-e-estetica-pet-em-curitiba.png',
    alt: 'Banho, Tosa e Estética Pet',
    whatsapp: 'https://wa.me/5541985332493?text=Olá! Quero agendar banho e tosa.',
    whatsappInfo: 'https://wa.me/5541985332493?text=Olá! Tenho dúvidas sobre banho e tosa.',
    buttonText: 'Agendar',
    reverse: true,
  },
];

export default function ServicesSection() {
  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  return (
    <section id="servicos" className="services-section">
      <div className="container">
        <div className="services-container">
          {services.map((service) => (
            <div
              key={service.id}
              className={`service-card-figma ${service.reverse ? 'reverse' : ''}`}
              data-aos="fade-up"
            >
              {!service.reverse && (
                <div className="service-image">
                  <Image
                    src={service.image}
                    alt={service.alt}
                    width={600}
                    height={400}
                    loading="lazy"
                  />
                </div>
              )}
              
              <div className="service-content">
                <div className="service-content-top">
                  <div className="service-tagline">
                    <span>{service.tagline}</span>
                  </div>
                  <h3>
                    {service.title} <em className="destaque">{service.destaque}</em>
                  </h3>
                  <p dangerouslySetInnerHTML={{ __html: service.description }} />
                </div>
                <div className="service-actions">
                  <a
                    href={service.whatsapp}
                    className="service-button secondary"
                    target="_blank"
                    rel="noopener"
                  >
                    {service.buttonText}
                  </a>
                  <a
                    href={service.whatsappInfo}
                    className="service-button link"
                    target="_blank"
                    rel="noopener"
                  >
                    Saber Mais
                    <ChevronRight width={16} height={16} />
                  </a>
                </div>
              </div>

              {service.reverse && (
                <div className="service-image">
                  <Image
                    src={service.image}
                    alt={service.alt}
                    width={600}
                    height={400}
                    loading="lazy"
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
