import type { Metadata } from "next";
import { Inter, Poppins, Playfair_Display } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-poppins",
  display: "swap",
});

const playfair = Playfair_Display({
  subsets: ["latin"],
  weight: ["400"],
  style: ["italic"],
  variable: "--font-playfair",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://aumivet.com.br"),
  title: {
    default: "Aumivet - Clínica Veterinária em Curitiba | Dra. Thaise PUCPR",
    template: "%s | Aumivet",
  },
  description:
    "Aumivet: clínica veterinária moderna em Curitiba. Consultas, cirurgias, banho e tosa, coworking veterinário. Dra. Thaise PUCPR. R. Santo Antônio 891, Rebouças.",
  keywords: [
    "aumivet",
    "clinica veterinaria curitiba",
    "veterinario curitiba",
    "dra thaise",
    "banho e tosa curitiba",
    "coworking veterinario",
    "anestesista veterinaria",
    "cirurgia veterinaria curitiba",
  ],
  authors: [{ name: "Aumivet" }],
  creator: "Aumivet",
  publisher: "Aumivet",
  openGraph: {
    type: "website",
    locale: "pt_BR",
    url: "https://aumivet.com.br",
    siteName: "Aumivet",
    title: "Aumivet - Clínica Veterinária em Curitiba",
    description:
      "Clínica veterinária moderna em Curitiba com serviços completos: consultas, cirurgias, banho e tosa, coworking veterinário",
  },
  twitter: {
    card: "summary_large_image",
    title: "Aumivet - Clínica Veterinária em Curitiba",
    description:
      "Clínica veterinária moderna em Curitiba com serviços completos",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "google-site-verification-code",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${poppins.variable} ${playfair.variable}`}>
      <body className="font-body antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
