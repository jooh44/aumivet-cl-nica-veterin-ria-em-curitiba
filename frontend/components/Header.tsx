'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';

export default function Header() {
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Scroll suave para âncoras quando a página carrega com hash
    const hash = window.location.hash;
    if (hash && pathname === '/') {
      const element = document.querySelector(hash);
      if (element) {
        setTimeout(() => {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
      }
    }
  }, [pathname]);

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, sectionId: string) => {
    e.preventDefault();
    
    // Se já estiver na homepage
    if (pathname === '/') {
      const element = document.querySelector(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Atualiza a URL com o hash
        window.history.pushState(null, '', sectionId);
      }
    } else {
      // Se estiver em outra página, navega para home com hash
      router.push('/' + sectionId);
    }
  };

  return (
    <header className="header">
      <div className="container">
        <nav className="nav">
          <div className="logo">
            <Link href="/">
              <Image 
                src="/images/logo-aumivet.png" 
                alt="Aumivet - Clínica Veterinária" 
                width={180} 
                height={60} 
                className="logo-img"
                priority
              />
            </Link>
          </div>
          <ul className="nav-links">
            <li><Link href="/">Início</Link></li>
            <li><Link href="/#servicos" onClick={(e) => handleNavClick(e, '#servicos')}>Serviços</Link></li>
            <li><Link href="/blog">Blog</Link></li>
            <li><Link href="/#about" onClick={(e) => handleNavClick(e, '#about')}>Sobre</Link></li>
            <li><Link href="/#team" onClick={(e) => handleNavClick(e, '#team')}>Equipe</Link></li>
            <li><Link href="/#faq" onClick={(e) => handleNavClick(e, '#faq')}>FAQ</Link></li>
            <li><Link href="/#contato" onClick={(e) => handleNavClick(e, '#contato')}>Contato</Link></li>
          </ul>
          <a 
            href="https://wa.me/5541988604202?text=Olá! Gostaria de agendar uma consulta." 
            className="nav-cta" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            Agendar Consulta
          </a>
        </nav>
      </div>
    </header>
  );
}
