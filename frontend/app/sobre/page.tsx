export default function SobrePage() {
  return (
    <div className="min-h-screen bg-aumivet-white py-20 px-4">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-5xl font-sans font-bold text-aumivet-black mb-6">
          Sobre a Aumivet
        </h1>
        <p className="text-xl font-display text-aumivet-pink mb-8">
          Cuidado veterinário com amor e excelência desde [ANO]
        </p>
        
        <div className="prose prose-lg max-w-none">
          <p className="text-aumivet-gray mb-6 leading-relaxed">
            A Aumivet nasceu do sonho da Dra. Thaise de criar um espaço acolhedor e moderno 
            para cuidar do bem-estar de cães e gatos em Curitiba. Localizada no coração do 
            bairro Rebouças, nossa clínica oferece atendimento personalizado e humanizado.
          </p>

          <h2 className="text-3xl font-sans font-bold text-aumivet-black mt-12 mb-4">
            Nossa Missão
          </h2>
          <p className="text-aumivet-gray mb-6 leading-relaxed">
            Proporcionar cuidados veterinários de excelência, promovendo a saúde, bem-estar 
            e qualidade de vida dos animais, com atendimento humanizado e tecnologia moderna.
          </p>

          <h2 className="text-3xl font-sans font-bold text-aumivet-black mt-12 mb-4">
            Dra. Thaise
          </h2>
          <p className="text-aumivet-gray mb-6 leading-relaxed">
            Médica Veterinária formada pela PUCPR, com especialização em anestesiologia e 
            cirurgia veterinária. Com anos de experiência e dedicação, a Dra. Thaise fundou 
            a Aumivet para oferecer um atendimento diferenciado e personalizado.
          </p>

          <h2 className="text-3xl font-sans font-bold text-aumivet-black mt-12 mb-4">
            Nossos Valores
          </h2>
          <ul className="list-disc list-inside text-aumivet-gray space-y-2 mb-6">
            <li>Amor e respeito pelos animais</li>
            <li>Excelência técnica e científica</li>
            <li>Atendimento humanizado</li>
            <li>Transparência e ética profissional</li>
            <li>Educação e prevenção</li>
            <li>Inovação e tecnologia</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
