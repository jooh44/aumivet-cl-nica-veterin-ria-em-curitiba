'use client';

import { HelpCircle, ChevronDown, Syringe, Scissors, Droplets, Stethoscope, Cat, Smile, ShieldCheck, Siren, CalendarPlus } from 'lucide-react';
import { useState, useEffect } from 'react';

const faqs = [
  {
    id: 1,
    icon: Syringe,
    question: 'Posso levar meu pet sem agendar?',
    answer: 'Trabalhamos com agendamento para oferecer um atendimento mais rápido e sem esperas desnecessárias. Entre em contato pelo WhatsApp e reserve seu horário.',
  },
  {
    id: 2,
    icon: Scissors,
    question: 'Cirurgias são realizadas com anestesia?',
    answer: 'Utilizamos protocolos de anestesia inalatória para máxima segurança e conforto. Seu pet é monitorado durante todo o procedimento e recebe medicação para controle da dor pós-operatória.',
  },
  {
    id: 3,
    icon: Droplets,
    question: 'Meu pet pode tomar banho toda semana?',
    answer: 'Depende da raça e tipo de pele. Durante a consulta, orientamos sobre a frequência ideal para seu pet, considerando suas necessidades específicas.',
  },
  {
    id: 4,
    icon: Stethoscope,
    question: 'Como sei se meu pet precisa de uma consulta dermatológica?',
    answer: 'Sinais como coceira excessiva, perda de pelo, vermelhidão ou odor forte na pele indicam necessidade de avaliação especializada.',
  },
  {
    id: 5,
    icon: Cat,
    question: 'Vocês fazem banho e tosa em gatos?',
    answer: 'Sim! Temos técnicas específicas para felinos, sempre priorizando o bem-estar e reduzindo o estresse do animal.',
  },
  {
    id: 6,
    icon: Smile,
    question: 'O que acontece se eu não escovar os dentes do meu pet?',
    answer: 'A falta de higiene oral pode levar ao acúmulo de tártaro, gengivite e até problemas cardíacos. Orientamos sobre cuidados domiciliares e oferecemos tratamentos odontológicos.',
  },
  {
    id: 7,
    icon: ShieldCheck,
    question: 'Quais vacinas meu pet precisa tomar?',
    answer: 'O protocolo varia conforme idade, estilo de vida e região. Durante a consulta, elaboramos um calendário personalizado de vacinação.',
  },
  {
    id: 8,
    icon: Siren,
    question: 'Como funciona o atendimento veterinário de emergência?',
    answer: 'Para emergências, entre em contato via WhatsApp (41) 98860-4202. Avaliamos a situação e orientamos sobre o melhor procedimento.',
  },
  {
    id: 9,
    icon: CalendarPlus,
    question: 'Como agendar um atendimento na Aumivet?',
    answer: 'Pelo telefone (41) 98860-4202, WhatsApp ou através do formulário em nosso site. Respeitamos horários e raramente há espera.',
  },
];

export default function FAQSection() {
  const [openItems, setOpenItems] = useState<number[]>([]);

  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  const toggleItem = (id: number) => {
    setOpenItems((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  return (
    <section id="faq" className="faq-section">
      <div className="container">
        <div className="section-header" data-aos="fade-up">
          <div className="section-badge">
            <HelpCircle width={16} height={16} />
            <span>Perguntas Frequentes</span>
          </div>
          <h2 className="section-title">
            Dúvidas <em className="destaque">Frequentes</em>
          </h2>
          <p className="section-description">Respostas rápidas para as perguntas mais comuns</p>
        </div>

        <div className="faq-list" data-aos="fade-up">
          {faqs.map((faq) => (
            <div key={faq.id} className={`faq-item ${openItems.includes(faq.id) ? 'active' : ''}`}>
              <button className="faq-question" onClick={() => toggleItem(faq.id)}>
                <faq.icon width={20} height={20} />
                <span>{faq.question}</span>
                <ChevronDown width={20} height={20} className="faq-chevron" />
              </button>
              <div className="faq-answer">{faq.answer}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
