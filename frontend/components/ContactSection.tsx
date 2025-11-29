'use client';

import { Phone, MapPin, Mail, Clock, AlertTriangle, MessageCircle, Navigation } from 'lucide-react';
import { useEffect } from 'react';

export default function ContactSection() {
  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  return (
    <section id="contato" className="contact-section">
      <div className="container">
        <div className="section-header" data-aos="fade-up">
          <div className="section-badge">
            <Phone width={16} height={16} />
            <span>Entre em Contato</span>
          </div>
          <h2 className="section-title">
            Vamos Cuidar do Seu Pet <em className="destaque">juntos?</em>
          </h2>
          <p className="section-description">
            Estamos aqui para oferecer o melhor cuidado veterinário com carinho e dedicação
          </p>
        </div>

        <div className="contact-content">
          <div className="contact-info" data-aos="fade-right">
            <h3>Como Chegar Até Nós</h3>
            <div className="contact-item">
              <span className="icon">
                <MapPin width={24} height={24} />
              </span>
              <span>R. Santo Antônio, 891 - Rebouças, Curitiba - PR, 80230-120</span>
            </div>
            <div className="contact-item">
              <span className="icon">
                <Phone width={24} height={24} />
              </span>
              <span>(41) 98860-4202</span>
            </div>
            <div className="contact-item">
              <span className="icon">
                <Mail width={24} height={24} />
              </span>
              <span>aumivet.clinica@gmail.com</span>
            </div>
            <div className="contact-item">
              <span className="icon">
                <Clock width={24} height={24} />
              </span>
              <span>Atendimento com agendamento - mais agilidade para você</span>
            </div>
            <div className="contact-item emergency">
              <span className="icon">
                <AlertTriangle width={24} height={24} />
              </span>
              <span>Emergências: WhatsApp para orientação imediata</span>
            </div>

            <div className="contact-cta">
              <a
                href="https://wa.me/5541988604202?text=Olá! Gostaria de agendar uma consulta."
                className="contact-btn primary"
                target="_blank"
                rel="noopener"
              >
                <MessageCircle width={20} height={20} />
                Agendar pelo WhatsApp
              </a>
              <a href="tel:+5541988604202" className="contact-btn secondary">
                <Phone width={20} height={20} />
                Ligar Agora
              </a>
            </div>
          </div>

          <div className="contact-map" data-aos="fade-left">
            <h3>Nossa Clínica no Mapa</h3>
            <div className="map-container">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3603.0837123047447!2d-49.2847143!3d-25.4461097!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94dce53b6b8b3b31%3A0x5a8b5b4a3b2b1b2b!2sR.%20Santo%20Ant%C3%B4nio%2C%20891%20-%20Rebou%C3%A7as%2C%20Curitiba%20-%20PR%2C%2080230-120!5e0!3m2!1spt-BR!2sbr!4v1699999999999!5m2!1spt-BR!2sbr"
                width="100%"
                height="300"
                style={{ border: 0, borderRadius: '12px' }}
                allowFullScreen
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
                title="Aumivet - R. Santo Antônio, 891 - Rebouças, Curitiba"
              />
            </div>
            <p className="map-description">
              <Navigation width={16} height={16} />
              Fácil acesso e estacionamento disponível
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
