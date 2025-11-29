'use client';

import { Users, UserCheck, Stethoscope, Sparkles, Eye, Heart, Award, Star, Calendar, BookOpen } from 'lucide-react';
import Image from 'next/image';
import { useState, useEffect } from 'react';

const teamMembers = [
  {
    id: 0,
    name: 'Dra. Thaise',
    title: 'Médica Veterinária - CRMV-PR 16704',
    description:
      'Fundadora da Aumivet, graduada pela PUCPR e pós-graduanda em Clínica Médica e Cirúrgica de Pequenos Animais. Atua em cirurgia de tecidos moles, procedimentos ortopédicos e emergências cirúrgicas, oferecendo acompanhamento completo para cada paciente.',
    photo: '/images/dra-thaise.jpg',
    icon: UserCheck,
    attributes: [
      { icon: Heart, label: 'ESPECIALIZAÇÃO' },
      { icon: Award, label: 'EXPERIÊNCIA' },
      { icon: Star, label: 'CERTIFICAÇÃO' },
    ],
  },
  {
    id: 1,
    name: 'Dr. Gustavo Trevisan',
    title: 'Médico Veterinário Anestesista',
    description:
      'Médico veterinário graduado pela UFPR em 2015. Especialização no programa de Residência Médico Veterinária na área de Anestesiologia Veterinária na PUCPR em 2018. Especialista em procedimentos anestésicos seguros e monitoramento avançado.',
    photo: '/images/dr-gustavo-trevisan.jpg',
    icon: Stethoscope,
    attributes: [
      { icon: Heart, label: 'CUIDADOS' },
      { icon: Award, label: 'MANEJO' },
      { icon: Star, label: 'ATENÇÃO' },
    ],
  },
  {
    id: 2,
    name: 'Dra. Renata',
    title: 'Médica Veterinária Especialista em Odontologia',
    description:
      'Formada em Medicina Veterinária pela PUC Paraná (2009), após 12 anos atuando exclusivamente na clínica médica, especializou-se em odontologia veterinária. Curso teórico-prático em Doença Periodontal pelo CTEOV-SP (2019) e especialização pela Anclivepa-SP (2021-2023). Dedicada a oferecer atendimento especializado e humanizado, garantindo a saúde bucal e o bem-estar dos pets.',
    photo: '/images/Dra Renata.jpg',
    icon: Sparkles,
    attributes: [
      { icon: Heart, label: 'ODONTOLOGIA' },
      { icon: Award, label: 'ESPECIALIZAÇÃO' },
      { icon: Star, label: 'HUMANIZAÇÃO' },
    ],
  },
  {
    id: 3,
    name: 'Dr. Franz',
    title: 'Médico Veterinário - Oftalmologia',
    description:
      'Médico veterinário formado pela UFPR. Realizou externship na Michigan State University, residência em Oftalmologia Veterinária pela UFPR e hoje é mestrando em Ciências Veterinárias. Atua como preceptor do programa de residência em oftalmologia veterinária da UFPR, unindo pesquisa, docência e atendimento clínico especializado para oferecer visão saudável aos pets.',
    photo: '/images/franz.jpg',
    icon: Eye,
    attributes: [
      { icon: Eye, label: 'OFTALMOLOGIA' },
      { icon: BookOpen, label: 'PESQUISA' },
      { icon: Users, label: 'PRECEPTORIA' },
    ],
  },
];

export default function TeamSection() {
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).AOS) {
      (window as any).AOS.refresh();
    }
  }, []);

  return (
    <section id="team" className="team-section">
      <div className="container">
        <div className="section-header" data-aos="fade-up">
          <div className="section-badge">
            <Users width={16} height={16} />
            <span>Nossa Equipe</span>
          </div>
          <h2 className="section-title">
            Conheça Nossa <em className="destaque">Equipe</em>
          </h2>
          <p className="section-description">Profissionais qualificados e apaixonados pelo bem-estar animal</p>
        </div>

        {/* Team Tabs System */}
        <div className="team-tabs-container" data-aos="fade-up">
          {/* Tab Navigation */}
          <div className="team-tabs-nav">
            {teamMembers.map((member, index) => (
              <button
                key={member.id}
                className={`team-tab ${activeTab === index ? 'active' : ''}`}
                onClick={() => setActiveTab(index)}
                data-tab={index}
              >
                <member.icon width={18} height={18} />
                <span>{member.name}</span>
              </button>
            ))}
          </div>

          {/* Tab Content (Folder Style) */}
          <div className="team-folder-container">
            {teamMembers.map((member, index) => (
              <div
                key={member.id}
                className={`team-folder-content ${activeTab === index ? '' : 'hidden'}`}
                id={`team-content-${index}`}
              >
                <div className="team-content-grid">
                  {/* Photo Section */}
                  <div className="team-photo-section">
                    <div className="team-photo-container">
                      <Image
                        src={member.photo}
                        alt={`Foto ${member.name}`}
                        className="team-photo"
                        width={400}
                        height={400}
                        loading="lazy"
                      />
                    </div>
                  </div>

                  {/* Info Section */}
                  <div className="team-info-section">
                    <div className="team-info-content">
                      <h3>{member.name}</h3>
                      <h4>{member.title}</h4>
                      <p>{member.description}</p>

                      <button className="team-cta-button">
                        Agendar Horário
                        <Calendar width={16} height={16} />
                      </button>

                      <div className="team-attributes">
                        {member.attributes.map((attr, idx) => (
                          <div key={idx} className="attribute-item">
                            <attr.icon width={20} height={20} />
                            <span>{attr.label}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
