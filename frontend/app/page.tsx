import Header from '@/components/Header';
import HeroSection from '@/components/HeroSection';
import ServicesSection from '@/components/ServicesSection';
import HealthPlansStrip from '@/components/HealthPlansStrip';
import PartnershipSection from '@/components/PartnershipSection';
import SpecializedSection from '@/components/SpecializedSection';
import TaxiPetSection from '@/components/TaxiPetSection';
import AboutSection from '@/components/AboutSection';
import TeamSection from '@/components/TeamSection';
import TestimonialsSection from '@/components/TestimonialsSection';
import BlogPreviewSection from '@/components/BlogPreviewSection';
import FAQSection from '@/components/FAQSection';
import ContactSection from '@/components/ContactSection';
import Footer from '@/components/Footer';
import { MessageCircle } from 'lucide-react';

export const metadata = {
  title: 'Aumivet - Clínica Veterinária Curitiba | Dra. Thaise PUCPR | Rebouças',
  description: 'Aumivet: clínica veterinária moderna em Curitiba. Consultas, cirurgias, banho e tosa, coworking veterinário. Dra. Thaise PUCPR. R. Santo Antônio 891, Rebouças. (41) 98860-4202',
  keywords: 'aumivet, clinica veterinaria curitiba, veterinario curitiba, dra thaise, banho e tosa curitiba, coworking veterinario, anestesista veterinaria, cirurgia veterinaria curitiba',
};

export default function HomePage() {
  return (
    <>
      <Header />
      <main>
        <HeroSection />
        <ServicesSection />
        <HealthPlansStrip />
        <PartnershipSection />
        <SpecializedSection />
        <TaxiPetSection />
        <AboutSection />
        <TeamSection />
        <TestimonialsSection />
        <BlogPreviewSection />
        <FAQSection />
        <ContactSection />

        {/* WhatsApp Float Button */}
        <a 
          href="https://wa.me/5541988604202?text=Olá! Gostaria de mais informações" 
          className="whatsapp-float"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Falar no WhatsApp"
        >
          <MessageCircle size={28} />
        </a>
      </main>
      <Footer />
    </>
  );
}
