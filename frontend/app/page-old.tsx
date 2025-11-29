import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-aumivet-white">
      {/* Header temporário */}
      <header className="bg-aumivet-green py-6">
        <div className="container mx-auto px-4">
          <nav className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-sans font-bold text-aumivet-white">
              🐾 Aumivet
            </Link>
            <div className="flex gap-6">
              <Link href="/" className="text-aumivet-white hover:text-aumivet-green-light transition">
                Home
              </Link>
              <Link href="/sobre" className="text-aumivet-white hover:text-aumivet-green-light transition">
                Sobre
              </Link>
              <Link href="/servicos" className="text-aumivet-white hover:text-aumivet-green-light transition">
                Serviços
              </Link>
              <Link href="/blog" className="text-aumivet-white hover:text-aumivet-green-light transition">
                Blog
              </Link>
              <Link href="/contato" className="text-aumivet-white hover:text-aumivet-green-light transition">
                Contato
              </Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <h1 className="text-5xl md:text-6xl font-sans font-bold text-aumivet-black mb-6">
            Cuidar com Amor, Tratar com Excelência
          </h1>
          <p className="text-2xl font-display text-aumivet-pink mb-8">
            Sua Clínica Veterinária de Confiança no Coração de Curitiba
          </p>
          <p className="text-lg text-aumivet-gray max-w-3xl mb-8 leading-relaxed">
            Somos uma clínica veterinária moderna no bairro Rebouças, especializada em cães e gatos, 
            com foco no bem-estar, prevenção e qualidade de vida. Fundada pela Dra. Thaise, 
            oferecemos cuidado personalizado em um ambiente acolhedor.
          </p>
          <div className="flex gap-4">
            <Link
              href="/contato"
              className="bg-aumivet-green hover:bg-aumivet-green-light text-white px-8 py-3 rounded-lg font-sans font-semibold transition"
            >
              Agendar Consulta
            </Link>
            <Link
              href="/sobre"
              className="border-2 border-aumivet-green text-aumivet-green hover:bg-aumivet-green hover:text-white px-8 py-3 rounded-lg font-sans font-semibold transition"
            >
              Conheça a Aumivet
            </Link>
          </div>
        </div>
      </section>

      {/* Serviços em Destaque */}
      <section className="py-16 bg-aumivet-white/50">
        <div className="container mx-auto px-4 max-w-6xl">
          <h2 className="text-4xl font-sans font-bold text-aumivet-black mb-12 text-center">
            Nossos Serviços
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: "Consultas Veterinárias",
                description: "Atendimento personalizado com Dra. Thaise formada pela PUCPR",
                icon: "🩺",
              },
              {
                title: "Cirurgias",
                description: "Procedimentos cirúrgicos com anestesia segura e equipamentos modernos",
                icon: "⚕️",
              },
              {
                title: "Banho e Tosa",
                description: "Cuidados estéticos e higiênicos para seu pet",
                icon: "🛁",
              },
              {
                title: "Odontologia Veterinária",
                description: "Saúde bucal completa para cães e gatos",
                icon: "🦷",
              },
              {
                title: "Coworking Veterinário",
                description: "Espaço para médicos veterinários parceiros",
                icon: "🏥",
              },
              {
                title: "Serviços Volantes",
                description: "Anestesista e cirurgiã disponível para atendimento externo",
                icon: "🚑",
              },
            ].map((service, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition">
                <div className="text-4xl mb-4">{service.icon}</div>
                <h3 className="text-xl font-sans font-semibold text-aumivet-black mb-2">
                  {service.title}
                </h3>
                <p className="text-aumivet-gray">{service.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-aumivet-pink text-white">
        <div className="container mx-auto px-4 text-center max-w-4xl">
          <h2 className="text-3xl md:text-4xl font-sans font-bold mb-4">
            Seu pet merece o melhor cuidado
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Agende uma consulta e venha conhecer nossa clínica no Rebouças
          </p>
          <div className="flex flex-col md:flex-row gap-4 justify-center items-center">
            <a
              href="tel:+554198604202"
              className="bg-white text-aumivet-pink hover:bg-aumivet-green-light hover:text-white px-8 py-3 rounded-lg font-sans font-semibold transition"
            >
              📞 (41) 98860-4202
            </a>
            <a
              href="https://wa.me/554198604202"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-aumivet-green hover:bg-aumivet-green-light text-white px-8 py-3 rounded-lg font-sans font-semibold transition"
            >
              💬 WhatsApp
            </a>
          </div>
        </div>
      </section>

      {/* Footer temporário */}
      <footer className="bg-aumivet-black text-white py-12">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-xl font-sans font-bold mb-4">Aumivet</h3>
              <p className="text-gray-400">
                Clínica Veterinária moderna em Curitiba, Rebouças.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-sans font-bold mb-4">Contato</h3>
              <p className="text-gray-400">R. Santo Antônio, 891</p>
              <p className="text-gray-400">Rebouças, Curitiba - PR</p>
              <p className="text-gray-400">CEP: 80230-120</p>
              <p className="text-gray-400 mt-2">(41) 98860-4202</p>
            </div>
            <div>
              <h3 className="text-xl font-sans font-bold mb-4">Horário</h3>
              <p className="text-gray-400">Segunda a Sexta: 9h - 18h</p>
              <p className="text-gray-400">Sábado: 9h - 13h</p>
              <p className="text-gray-400">Domingo: Fechado</p>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 Aumivet. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>

      {/* Schema.org JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "VeterinaryCare",
            name: "Aumivet Clínica Veterinária",
            description:
              "Clínica veterinária moderna em Curitiba com serviços completos: consultas, cirurgias, banho e tosa, coworking veterinário",
            url: "https://aumivet.com.br",
            telephone: "+55-41-98860-4202",
            email: "aumivet.clinica@gmail.com",
            address: {
              "@type": "PostalAddress",
              streetAddress: "R. Santo Antônio, 891",
              addressLocality: "Curitiba",
              addressRegion: "PR",
              postalCode: "80230-120",
              addressCountry: "BR",
            },
            founder: {
              "@type": "Person",
              name: "Dra. Thaise",
              jobTitle: "Médica Veterinária",
              alumniOf: "PUCPR",
            },
            serviceType: [
              "Consultas veterinárias",
              "Cirurgias veterinárias",
              "Banho e tosa",
              "Odontologia veterinária",
              "Coworking veterinário",
              "Anestesista volante",
              "Cirurgiã volante",
            ],
          }),
        }}
      />
    </div>
  );
}
