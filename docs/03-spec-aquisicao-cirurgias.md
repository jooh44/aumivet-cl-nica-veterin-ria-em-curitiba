# Spec: Aquisicao de Cirurgias - Aumivet

Ultima atualizacao: 2026-05-19
Status: aprovado (Phase 1 concluida)

## Objetivo

Preparar a presenca digital da Aumivet para gerar **demanda qualificada de cirurgias**, otimizando para o universo amplo de **cirurgia veterinaria**, com foco em **cirurgia geral** (Dra. Thaise), **odontologia** e **cirurgia de catarata** como USP premium, antes de ativar Google Ads.

USP confirmada em 2026-05-19: a Aumivet e a **unica clinica do Parana credenciada para cirurgia de catarata pelo Petlove Saude**. Esse e o maior diferencial competitivo da casa hoje e deve ocupar lugar de destaque na home, na pagina de cirurgia e em uma pagina dedicada.

Cirurgia ortopedica esta fora do foco: e atendimento terceirizado, nao e coberto pelo Petlove e nao representa vantagem competitiva. Sem pagina dedicada, sem investimento de midia, e negativada na campanha.

Sucesso significa:

- Quando um tutor em Curitiba busca "cirurgia veterinaria curitiba", "cirurgia cachorro", "castracao", "remocao tumor", "limpeza dental" ou "cirurgia catarata cachorro", a Aumivet aparece no mapa local e/ou no organico com pagina especifica.
- O tutor entende, em menos de 30 segundos na pagina, que a Aumivet faz aquela cirurgia, com qual equipe, com qual estrutura anestesica e como falar com a clinica.
- Todo clique vindo do Ads cai numa pagina que prova o servico, nao na home generica.
- Os contatos por WhatsApp, telefone e rota estao sendo medidos individualmente.
- A parceria Petlove esta visivel no site e funciona como argumento direto de conversao em cirurgia geral, odontologia e catarata (todas cobertas pelo plano). A unicidade Petlove-catarata-PR e o reforco central da proposta.

Publico:

- B2C primario: tutores em Curitiba e regiao metropolitana, com cachorro/gato, considerando cirurgia eletiva (castracao, odonto, tecidos moles, catarata) ou indicada por outro veterinario.
- B2C premium: beneficiarios Petlove Saude do Parana com indicacao de cirurgia de catarata, que hoje nao tem outra opcao credenciada no estado.
- Secundario: beneficiarios Petlove Saude buscando credenciada para consultas e rotina.

## Tech Stack

- Landing publica atual: `index.html` + `styles.css` estaticos servidos via Vercel em `https://www.aumivet.com.br`.
- App principal alvo: Next.js 15 (App Router) em `frontend/`, TypeScript, Tailwind, blog estatico.
- Sem CMS. Conteudo de servicos como arquivos do proprio Next.
- Deploy: Vercel.
- Tag manager: GTM (a instalar). GA4 (a confirmar ou criar). Tag de conversao Google Ads.
- Sem Search Console acessivel agora; verificacao sera adicionada quando o acesso for liberado.

## Comandos

```bash
cd frontend
npm ci
npm run dev          # dev local em http://localhost:3000
npm run build        # build de producao
npm run start        # roda o build local
npm run lint         # lint
npm audit --omit=dev # checagem de vulnerabilidades em prod
```

Deploy:

- Push para `master` dispara deploy automatico no Vercel (validar configuracao do projeto Vercel).

## Project Structure

```
/                                  -> landing estatica legada (sera substituida pelo Next.js)
index.html, styles.css, images/    -> landing antiga
docs/                              -> contexto, propostas, specs internos
docs/03-spec-aquisicao-cirurgias.md-> este spec
frontend/                          -> app Next.js 15 (alvo do deploy)
frontend/app/                      -> rotas App Router
frontend/app/servicos/             -> ja existe; expandir com paginas por servico
frontend/app/servicos/cirurgias/page.tsx            -> nova (guarda-chuva)
frontend/app/servicos/cirurgia-catarata/page.tsx    -> nova (USP)
frontend/app/servicos/odontologia/page.tsx          -> nova
frontend/app/blog/                 -> blog estatico
frontend/components/               -> componentes UI reutilizaveis
frontend/lib/                      -> helpers (tracking, formatadores)
frontend/public/images/            -> assets
frontend/public/sitemap.xml        -> gerado por next-sitemap
```

## Code Style

Componentes funcionais, server components por padrao, marca `"use client"` so quando necessario para interatividade (botoes com tracking, modais).

```tsx
// frontend/app/servicos/cirurgia-geral/page.tsx
import type { Metadata } from "next";
import { ServiceHero } from "@/components/ServiceHero";
import { TeamCard } from "@/components/TeamCard";
import { WhatsappCTA } from "@/components/WhatsappCTA";

export const metadata: Metadata = {
  title: "Cirurgia Geral Veterinaria em Curitiba | Aumivet",
  description:
    "Cirurgia geral veterinaria em Curitiba: castracao, remocao de tumores, tecidos moles, emergencias cirurgicas. Equipe propria, anestesista dedicado. R. Santo Antonio, 891 - Reboucas.",
};

export default function CirurgiaOrtopedicaPage() {
  return (
    <main>
      <ServiceHero
        title="Cirurgia geral veterinaria em Curitiba"
        subtitle="Equipe especializada, anestesista dedicado e acompanhamento pos-operatorio."
        ctaLabel="Falar no WhatsApp"
        ctaEvent="cta_whatsapp_cirurgia_geral"
      />
      <TeamCard />
      <WhatsappCTA event="cta_whatsapp_cirurgia_geral_bottom" />
    </main>
  );
}
```

Convencoes:

- Nomes de arquivos kebab-case em rotas (`cirurgias`, `cirurgia-catarata`).
- Componentes PascalCase.
- Eventos de tracking em snake_case com prefixo `cta_` ou `view_`.
- Sem cores hardcoded fora dos tokens do design system. **Paleta expandida** definida em `design.md` (2026-05-22): familias `aumi-*` (rosa, primaria), `vet-*` (verde, secundaria), `neutral-*` (quentes, base ~70% da UI) e apoio `peach-*`, `terra-*`, `teal-*`. Aplicacao base: fundo `neutral-50`, superficie `#FFFFFF`, borda `neutral-200`, texto `neutral-900`/`neutral-700`, acao primaria `aumi-500` (hover `aumi-600`), acao secundaria `vet-600` (hover `vet-700`). Para marca em texto sobre branco usar sempre 700 ou 900 — medias nao passam AA.
- **Direcao visual: fotografia real, nao ilustracao.** Hero e imagens de servico devem usar fotos reais da clinica, equipe e procedimentos. Ver decisao em `project-context.md > Diretrizes visuais`.
- Imagens com `next/image` e `alt` descritivo contendo a palavra "Aumivet" quando fizer sentido para a marca.
- Schema markup `VeterinaryCare` no layout raiz; `MedicalProcedure` ou `Service` em cada pagina de servico.

## Testing Strategy

Este projeto nao precisa de suite ampla de testes unitarios. Verificacao real e por:

- `npm run build` deve passar sem erros nem warnings novos.
- `npm run lint` sem erros.
- Lighthouse mobile em paginas de servico: Performance >= 85, SEO = 100, Acessibilidade >= 90.
- Validacao manual:
  - Schema markup valido em https://validator.schema.org/.
  - Sitemap.xml acessivel.
  - Cliques de CTA disparam evento no GA4 (DebugView).
- Checklist NAP: nome "Aumivet Clinica Veterinaria", endereco e telefone identicos em site, GBP e Petlove.

Sem testes E2E nesta fase.

## Boundaries

Always do:

- Atualizar `docs/03-spec-aquisicao-cirurgias.md` quando decisoes mudarem.
- Rodar `npm run build` antes de commit que mexa em `frontend/`.
- Manter nome exato "Aumivet Clinica Veterinaria" em todas as citacoes.
- Usar tokens do design system existente.
- Preservar a parceria Petlove em destaque no site.
- Disparar evento de tracking em todo CTA novo.

Ask first:

- Reescrever copy comercial em paginas existentes que ja convertem.
- Adicionar dependencia nova em `frontend/package.json`.
- Mudar dominio canonico (hoje `www.aumivet.com.br`).
- Criar campanha Google Ads de fato (ativacao).
- Trocar fotos da equipe ou da clinica.
- Mexer em GBP (acoes irreversiveis como mudanca de categoria principal).

Never do:

- Reintroduzir Strapi/CMS sem decisao explicita.
- Migrar para outro framework (Astro etc.) nesta fase.
- Mencionar publicamente o problema antigo de SEO/grafia.
- Usar jargao tecnico (GA4, GTM, UTM, Search Console, CTR) em material cliente-facing.
- Subir Ads antes de paginas de servico e tracking estarem prontos.
- Commitar segredos (`.env`, tokens GBP, tokens Vercel).
- Alterar fotos sem confirmar uso de imagem.

## Success Criteria

Antes de ligar Google Ads, todos os itens abaixo devem estar verdadeiros:

1. **Paginas de servico publicadas e indexaveis**
   - `https://www.aumivet.com.br/servicos/cirurgias` (guarda-chuva) retorna 200, schema valido, peso < 1.5 MB.
   - `https://www.aumivet.com.br/servicos/cirurgia-catarata` (USP) retorna 200, schema valido.
   - `https://www.aumivet.com.br/servicos/odontologia` retorna 200, schema valido.
   - Todas listam: o que e feito, quem faz (equipe), seguranca anestesica, ambiente, cobertura Petlove, CTA WhatsApp, telefone, mapa.
   - Pagina de catarata destaca "unica do Parana credenciada Petlove Saude".
2. **Tracking ativo**
   - GA4 instalado via GTM, eventos `cta_whatsapp`, `cta_telefone`, `cta_rota` disparando.
   - Conversao Google Ads importando ao menos `cta_whatsapp` e `cta_telefone`.
3. **GBP coerente**
   - Nome exato "Aumivet Clinica Veterinaria".
   - Categoria principal "Veterinario" + secundarias relevantes.
   - Servicos cadastrados incluem "Cirurgia geral", "Castracao", "Cirurgia de catarata", "Oftalmologia veterinaria", "Odontologia veterinaria" e "Atendimento de emergencia".
   - Fotos atuais carregadas.
   - Horario e telefone batendo com o site.
4. **Citacao Petlove ativa**
   - Confirmado que existe pagina Aumivet em `saude.petlove.com.br/rede-credenciada/pr/curitiba/<slug>`.
   - Se nao existir, abrir solicitacao via canal de credenciamento Petlove.
   - Pagina mostra NAP correto.
5. **Site canonico**
   - Decidido se o publico vai migrar de `index.html` para Next.js ou se ambos coexistem.
   - Redirects sem loop, canonico estavel.
6. **Estrategia de Ads desenhada (nao ativa)**
   - 1 campanha Search com 3 grupos: cirurgia geral (umbrella), catarata (USP, ticket alto) e odontologia.
   - Catarata recebe atencao especial: keyword exact, copy com "unica do PR pela Petlove".
   - Lista inicial de palavras-chave em correspondencia frase/exata.
   - Lista de negativas iniciais (cursos, gratis, faculdade, concurso).
   - Lances manuais ou Maximizar conversoes apenas apos 30 conversoes registradas.
   - Verba teto R$ 500/mes.

## Indicadores pos-lancamento (para acompanhar nos primeiros 60 dias)

- Cliques no WhatsApp por origem (organico, Ads, GBP).
- Numero de chamadas telefonicas registradas.
- Numero de rotas geradas no Maps.
- Custo por contato qualificado (clique em WhatsApp pos-pagina de servico).
- Aparicao da marca "Aumivet" no autocomplete do Google sem sugerir variantes erradas.

## Decisoes confirmadas em 2026-05-19

- **GBP categorias atuais**: Veterinario (principal), Banho e tosa, Servico veterinario de emergencia.
  - Acao: **descontinuar "Banho e tosa"** (cliente vai fechar essa frente). Adicionar categorias secundarias relevantes para cirurgia/odonto se disponiveis.
- **Petlove**: Aumivet ja consta em `https://saude.petlove.com.br/rede-credenciada/pr/curitiba/aumivet-clinica-veterinaria`. Pagina existe, e indexavel, fornece NAP. Usar como citacao no site e validar consistencia NAP.
- **Site canonico**: a decisao sera baseada em performance medida. Estrategia: portar a landing estatica para a home do Next.js (preservando o design atual), deployar Next.js como dominio canonico unico. Antes da migracao, capturar baseline de performance e indexacao da landing atual.
- **Fotos**: clinica/ambiente ja temos. Precisamos solicitar fotos do anestesista e demais medicos da rotina. Cirurgia geral e assinada pela Dra. Thaise, entao o foco fotografico e nela + centro cirurgico.
- **Foco cirurgico revisado em 2026-05-19 (WhatsApp da cliente)**: cirurgia ortopedica esta fora (terceirizada e nao coberta pelo Petlove). Foco passa a ser cirurgias no geral, com cirurgia geral (Dra. Thaise) e odontologia como volume e cirurgia de catarata como diferencial premium.
- **USP de catarata confirmada em 2026-05-19**: Aumivet e a unica clinica do Parana credenciada para cirurgia de catarata pelo Petlove Saude (confirmado por escrito pela cliente). Posicionar como destaque na home, em `/servicos/cirurgias` e em pagina dedicada `/servicos/cirurgia-catarata`.
- **Cobertura Petlove**: cobre cirurgia geral, odontologia e catarata. Nao cobre ortopedica. Selo Petlove pode aparecer em cirurgia, catarata e odontologia.

## Open Questions ainda pendentes

1. **Preco de cirurgia**: exibir faixa de preco ou apenas "solicite orcamento"?
2. **Tipos de cirurgia geral a destacar na pagina umbrella**: castracao, tumor/nodulo, piometra, cesariana, abdominal — quais devem aparecer com mais peso?
7. **Cirurgia de catarata**: temos foto pos-cirurgia, depoimento de tutor, dados de quantos procedimentos ja foram feitos pela Petlove? Tudo isso reforca a pagina dedicada.
8. **Volume de catarata pela Petlove**: aproximadamente quantos beneficiarios sao encaminhados por mes? Ajuda a calibrar a expectativa de Ads.
3. **Anestesista volante**: ela cobre todas as cirurgias? Pode virar diferencial nominado?
4. **Casos clinicos**: podemos publicar antes/depois com autorizacao do tutor?
5. **Search Console**: quando teremos acesso?
6. **Telefone (41) 98860-4202**: WhatsApp puro ou recebe chamada tambem? Se for so WhatsApp, esconder click-to-call do mobile.
