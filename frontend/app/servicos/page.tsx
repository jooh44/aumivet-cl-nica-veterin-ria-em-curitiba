export default function ServicosPage() {
  const services = [
    {
      title: "Consultas Veterinárias",
      description:
        "Atendimento clínico completo com anamnese detalhada, exame físico e orientações personalizadas para a saúde do seu pet.",
      features: [
        "Consultas de rotina e check-up",
        "Diagnóstico e tratamento de doenças",
        "Orientações nutricionais",
        "Planos de vacinação",
        "Controle de parasitas",
      ],
    },
    {
      title: "Cirurgias Veterinárias",
      description:
        "Procedimentos cirúrgicos realizados com equipamentos modernos, anestesia segura e acompanhamento pós-operatório completo.",
      features: [
        "Castração de cães e gatos",
        "Cirurgias de tecidos moles",
        "Cirurgias ortopédicas",
        "Procedimentos odontológicos",
        "Anestesia inalatória segura",
      ],
    },
    {
      title: "Banho e Tosa",
      description:
        "Serviços de estética e higiene para manter seu pet limpo, saudável e bonito.",
      features: [
        "Banho terapêutico",
        "Tosa higiênica",
        "Tosa completa",
        "Corte de unhas",
        "Limpeza de ouvidos",
      ],
    },
    {
      title: "Odontologia Veterinária",
      description:
        "Cuidados com a saúde bucal do seu pet, prevenindo doenças e melhorando a qualidade de vida.",
      features: [
        "Limpeza dentária (profilaxia)",
        "Extração dentária",
        "Tratamento de gengivite",
        "Orientações de higiene bucal",
        "Radiografia dentária",
      ],
    },
    {
      title: "Coworking Veterinário",
      description:
        "Espaço completo para médicos veterinários parceiros realizarem atendimentos e procedimentos.",
      features: [
        "Consultório equipado",
        "Sala cirúrgica",
        "Internação",
        "Suporte técnico",
        "Agendamento flexível",
      ],
    },
    {
      title: "Serviços Volantes",
      description:
        "Anestesista e cirurgiã disponível para atendimento em outras clínicas e hospitais veterinários.",
      features: [
        "Anestesia volante",
        "Cirurgias em outras clínicas",
        "Procedimentos especializados",
        "Consultoria técnica",
        "Atendimento personalizado",
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-aumivet-white py-20 px-4">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-5xl font-sans font-bold text-aumivet-black mb-6 text-center">
          Nossos Serviços
        </h1>
        <p className="text-xl font-display text-aumivet-pink mb-12 text-center">
          Cuidado completo para a saúde e bem-estar do seu pet
        </p>

        <div className="grid gap-12">
          {services.map((service, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-sm p-8 hover:shadow-md transition"
            >
              <h2 className="text-3xl font-sans font-bold text-aumivet-black mb-4">
                {service.title}
              </h2>
              <p className="text-aumivet-gray mb-6 leading-relaxed">
                {service.description}
              </p>
              <ul className="grid md:grid-cols-2 gap-3">
                {service.features.map((feature, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-aumivet-pink mr-2">✓</span>
                    <span className="text-aumivet-gray">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-16 bg-aumivet-green text-white rounded-lg p-8 text-center">
          <h2 className="text-3xl font-sans font-bold mb-4">
            Agende uma Consulta
          </h2>
          <p className="text-xl mb-6 opacity-90">
            Entre em contato e garanta o melhor cuidado para seu pet
          </p>
          <a
            href="tel:+554198604202"
            className="inline-block bg-white text-aumivet-green hover:bg-aumivet-green-light hover:text-white px-8 py-3 rounded-lg font-sans font-semibold transition"
          >
            📞 (41) 98860-4202
          </a>
        </div>
      </div>
    </div>
  );
}
