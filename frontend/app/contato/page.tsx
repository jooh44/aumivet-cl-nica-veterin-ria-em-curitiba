export default function ContatoPage() {
  return (
    <div className="min-h-screen bg-aumivet-white py-20 px-4">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-5xl font-sans font-bold text-aumivet-black mb-6 text-center">
          Entre em Contato
        </h1>
        <p className="text-xl font-display text-aumivet-pink mb-12 text-center">
          Estamos prontos para cuidar do seu pet
        </p>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Informações de Contato */}
          <div className="space-y-8">
            <div>
              <h2 className="text-2xl font-sans font-bold text-aumivet-black mb-4">
                📍 Endereço
              </h2>
              <p className="text-aumivet-gray leading-relaxed">
                R. Santo Antônio, 891<br />
                Rebouças, Curitiba - PR<br />
                CEP: 80230-120
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-sans font-bold text-aumivet-black mb-4">
                📞 Telefone
              </h2>
              <a
                href="tel:+554198604202"
                className="text-aumivet-green hover:text-aumivet-green-light text-xl font-semibold transition"
              >
                (41) 98860-4202
              </a>
            </div>

            <div>
              <h2 className="text-2xl font-sans font-bold text-aumivet-black mb-4">
                📧 Email
              </h2>
              <a
                href="mailto:aumivet.clinica@gmail.com"
                className="text-aumivet-green hover:text-aumivet-green-light text-xl font-semibold transition"
              >
                aumivet.clinica@gmail.com
              </a>
            </div>

            <div>
              <h2 className="text-2xl font-sans font-bold text-aumivet-black mb-4">
                ⏰ Horário de Atendimento
              </h2>
              <div className="text-aumivet-gray space-y-2">
                <p>Segunda a Sexta: 9h - 18h</p>
                <p>Sábado: 9h - 13h</p>
                <p>Domingo: Fechado</p>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-sans font-bold text-aumivet-black mb-4">
                💬 Redes Sociais
              </h2>
              <div className="flex gap-4">
                <a
                  href="https://wa.me/554198604202"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-aumivet-green hover:bg-aumivet-green-light text-white px-6 py-2 rounded-lg font-sans font-semibold transition"
                >
                  WhatsApp
                </a>
                <a
                  href="https://instagram.com/aumivet"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-aumivet-pink hover:opacity-90 text-white px-6 py-2 rounded-lg font-sans font-semibold transition"
                >
                  Instagram
                </a>
              </div>
            </div>
          </div>

          {/* Mapa (placeholder) */}
          <div className="bg-aumivet-gray/10 rounded-lg p-8 flex items-center justify-center">
            <div className="text-center">
              <p className="text-aumivet-gray mb-4">
                📍 Mapa interativo será adicionado em breve
              </p>
              <a
                href="https://maps.google.com/?q=R.+Santo+Antônio+891+Curitiba"
                target="_blank"
                rel="noopener noreferrer"
                className="text-aumivet-green hover:text-aumivet-green-light font-semibold transition"
              >
                Abrir no Google Maps →
              </a>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 bg-aumivet-green text-white rounded-lg p-8 text-center">
          <h2 className="text-3xl font-sans font-bold mb-4">
            Emergência Veterinária?
          </h2>
          <p className="text-xl mb-6 opacity-90">
            Entre em contato imediatamente pelo WhatsApp
          </p>
          <a
            href="https://wa.me/554198604202"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-white text-aumivet-green hover:bg-aumivet-green-light hover:text-white px-8 py-3 rounded-lg font-sans font-semibold transition"
          >
            💬 Chamar no WhatsApp
          </a>
        </div>
      </div>
    </div>
  );
}
