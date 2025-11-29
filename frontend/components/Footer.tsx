import Image from 'next/image';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <Image
              src="/images/logo-aumivet.png"
              alt="Logo Aumivet"
              className="footer-logo"
              width={180}
              height={60}
              loading="lazy"
            />
            <p>
              Cuidado veterinário com <em className="destaque-rosa">amor</em> e <em className="destaque">excelência</em>
            </p>
          </div>
          <div className="footer-info">
            <p>
              <strong>Dra. Thaise</strong> - CRMV-PR
            </p>
            <p>R. Santo Antônio, 891 - Rebouças, Curitiba</p>
            <p>(41) 98860-4202 • aumivet.clinica@gmail.com</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2025 Aumivet. Feito com 💚 para quem ama pets em Curitiba.</p>
        </div>
      </div>
    </footer>
  );
}
