# Project Context - Aumivet

Ultima atualizacao: 2026-05-24

Este arquivo e a fonte rapida para agentes continuarem a retomada da Aumivet sem reconstruir contexto.

## Objetivo atual

A Aumivet era cliente, pausou e esta sendo reativada. O trabalho imediato e preparar a retomada comercial para gestao de Google Ads e evolucao do site, com proposta em HTML pronta para envio e contexto suficiente para planejar o proximo ciclo.

O foco da retomada nao e vender um projeto do zero. E reposicionar a presenca digital da clinica, reforcar a parceria com a Petlove e organizar a aquisicao local com anuncios, Google Meu Negocio, site, SEO/AIO e branding.

## Arquivos principais

- `docs/proposta-comercial-aumivet.html`: proposta comercial cliente-facing mais atual.
- `docs/00-contexto-retomada.md`: contexto tecnico/comercial da retomada.
- `docs/01-proposta-google-ads-upsell.md`: base interna inicial da oferta.
- `docs/02-checklist-retomada.md`: checklist tecnico e comercial.
- `CLAUDE.md`: briefing curto para agentes.
- `frontend/`: site Astro estatico atual, usado para o deploy.
- `index.html` e `styles.css`: landing estatica publica original.

## Proposta comercial atual

A proposta principal esta em `docs/proposta-comercial-aumivet.html` e deve ser tratada como o artefato de venda mais atualizado.

Planos:

1. **Google Ads essencial - R$ 500/mes**
   - Gestao de Google Ads.
   - Foco em campanhas de busca.
   - Pode explorar termos ligados a Petlove quando fizer sentido.
   - Nao inclui atualizacao estrutural do site.

2. **Retomada local completa - R$ 750/mes por 3 meses**
   - Opcao recomendada e escolha obvia da proposta.
   - Google Ads + Google Meu Negocio + edicoes livres no site durante o periodo.
   - Atualizacao do site para melhorar ranqueamento e preparar presenca em buscas com IA.
   - Reforco da parceria Petlove no site.
   - Medicao simples dos contatos por WhatsApp, telefone, formulario e mapa.
   - Deve mostrar que anuncio e site vao provar a mesma mensagem.

3. **Expansao visual e branding - R$ 1.000/mes por 3 meses**
   - Tudo do plano recomendado.
   - Expansao da identidade visual da marca.
   - Reforco de branding.
   - Posts semanais no Instagram para aplicar a identidade e divulgar a parceria Petlove.
   - Cartao de visita com design, impressao grafica e entrega na porta da clinica por nossa conta.

Midia paga ao Google e investimento separado da gestao.

## Diretrizes de linguagem comercial

- Nao explicitar o problema antigo de SEO ou a grafia errada que ainda aparece em buscas.
- Tratar SEO/AIO como evolucao natural do site diante das mudancas dos buscadores e das IAs.
- Evitar termos tecnicos que a cliente nao reconhece, como GA4, GTM, UTM e Search Console, em materiais comerciais.
- Em proposta cliente-facing, usar linguagem como:
  - medicao dos contatos;
  - WhatsApp, telefone, formulario e mapa monitorados;
  - organizacao dos links e rotas de contato;
  - melhoria de ranqueamento;
  - busca com IA;
  - presenca local no Google.
- A Petlove deve aparecer como oportunidade positiva: a parceria ja traz resultado e o site precisa evidenciar isso melhor.
- O plano de R$ 750 deve ser claramente o melhor custo-beneficio; o de R$ 1.000 e a expansao de marca.

## Diretrizes visuais

### Paleta atual — design system expandido (2026-05-22)

Fonte autoritativa: `design.md` (raiz do repo). Figma: node `7:8995`.

Famílias:

- **Aumi Pink** (acao primaria, links, destaques). `aumi-500 #F24E88` e a cor original do logo.
  - `aumi-50 #FDEEF4`, `aumi-100 #FBD3E1`, `aumi-200 #F7A8C2`, `aumi-300 #F575A3`, `aumi-500 #F24E88` ★, `aumi-600 #D43670`, `aumi-700 #A8295A`, `aumi-900 #6E1A3B`.
- **Vet Green** (acao secundaria, sucesso, saude). `vet-400 #81BD65` e a cor original do logo.
  - `vet-50 #EEF6E8`, `vet-100 #D3E8C4`, `vet-200 #AFD698`, `vet-400 #81BD65` ★, `vet-500 #67A24B`, `vet-600 #4E8235`, `vet-700 #3A6326`, `vet-900 #234016`.
- **Neutros quentes** (~70% da interface, fundos, texto, bordas).
  - `neutral-50 #FAF8F5`, `neutral-100 #F0ECE6`, `neutral-200 #DDD6CC`, `neutral-300 #B5ADA0`, `neutral-500 #8A8175`, `neutral-700 #5C544A`, `neutral-900 #382F26`.
- **Apoio** (graficos, categorias, ilustracoes remanescentes).
  - `peach-100 #FBE8DD`, `peach-400 #F2A878`, `terra-600 #C9603A`.
  - `teal-100 #DDEBEA`, `teal-400 #5FA8A3`, `teal-700 #2C6B68`.

Aplicacao:

| Papel | Token |
|---|---|
| Fundo da pagina | `neutral-50` |
| Superficie (cards) | `#FFFFFF` |
| Linha / borda | `neutral-200` |
| Texto principal | `neutral-900` |
| Texto suave | `neutral-700` |
| Acao primaria | `aumi-500` (hover `aumi-600`) |
| Acao secundaria | `vet-600` (hover `vet-700`) |

Notas WCAG:
- Cores medias (300-500) de Aumi e Vet **nao passam contraste** para texto sobre branco. Para "cor de marca em texto", usar sempre 700 ou 900.
- Sobre `vet-400` (verde original), usar texto escuro (`vet-900`). Branco falha.
- `aumi-500` com texto branco passa em AA (botao primario).
- Neutros sao quentes de proposito; cinza azulado fica doentio sobre fotografia de pele/pelagem.

Fontes ja usadas na proposta: Inter, Poppins e Playfair Display.

### Layout bentô — 2026-05-22 (IMPORTANTE)

**Hero e Servicos usam "bento": grande card unico com cantos arredondados (~32-48px) sobre o fundo neutro da pagina.**

- O hero NAO e uma secao full-bleed com pets isolados em colunas. E **um unico modulo gigante arredondado** (bento) sentado sobre o `bg` da pagina.
- A imagem do hero e **uma unica composicao de fundo** com os pets ja compostos no proprio asset. Nao use `<Image>` separados para cada pet.
- Mobile e desktop podem ter composicoes de bg diferentes (pets afastados no desktop, juntos no mobile), mas sempre como bg unico do bento.
- A secao de Servicos segue a mesma pegada de bento, com o card "Cirurgias Especializadas" como bento maior.
- E uma tendencia moderna; e o que da ao site a sensacao de "modulos premium".
- Approach rejeitado: pets como `<Image>` isolados em colunas (3-col grid dog | texto | cat). Isso e full-bleed, nao bento.

### Decisao de direcao visual — 2026-05-19

**A direcao do site muda de ilustracao para fotografia real, com posicionamento ligeiramente mais premium.**

Razao: o novo posicionamento (cirurgia especializada, unica credenciada Petlove para catarata no Parana) exige um visual que transmita confianca tecnica e qualidade clinica. Ilustracoes genericas contradizem esse nível de posicionamento.

O que muda:
- **Hero**: substituir por fotografia real da clinica ou equipe (sem ilustracao).
- **Imagens de servico**: fotografias reais dos procedimentos, centro cirurgico, instrumentos, ambiente. Sem icones ilustrativos como substitutos.
- **Paleta**: expandida em 2026-05-22 (ver `design.md` e secao "Paleta atual" acima). Aumi Pink + Vet Green como ancoras, neutros quentes como base, peach/terra/teal como apoio.
- **Tom**: menos playful, mais seguro/clinico mas ainda acolhedor. Equiibrio entre premium e proximidade.

O que nao muda:
- Identidade de marca Aumivet (nome, tipografia base, rosa e verde como acentos).
- Tom de voz comercial (acolhedor, sem jargao tecnico cliente-facing).

Impacto em outros arquivos:
- A proposta `docs/06-resumo-cliente-aumivet.html` deve refletir a nova direcao quando imagens forem incluidas.
- As paginas de servico do Next.js (cirurgias, catarata, odontologia) devem usar fotos reais no hero, nao placeholder ou ilustracao.
- O `index.html` (landing atual) sera atualizado na hero e nas imagens de servico.
- Paleta expandida ja definida em `design.md` (2026-05-22): aplicar tokens novos ao implementar secoes a partir de agora.

Evitar misturar outro design system. Todo material deve parecer Aumivet.

## Estado atual do site e deploy — 2026-05-23

O site esta pronto para deploy/pos-deploy no app Astro em `frontend/`. O usuario fez os ultimos ajustes com Claude e realizou deploy em 2026-05-23. Para continuidade, tratar o estado de `frontend/src/`, `frontend/public/images/` e `frontend/dist/` como a base visual mais recente, nao a landing estatica legada da raiz.

Stack atual:

- Astro `^5.16.0` em `frontend/`.
- Scripts principais: `pnpm build`, `pnpm preview`, `pnpm check`.
- `frontend/package.json` inclui `astro`, `@astrojs/check`, `@lucide/astro`, `gsap`, `lenis`, `sharp` e `typescript`.
- Build validado com `pnpm build`; passa com 0 erros. Permanecem apenas 2 hints conhecidos em `src/components/About.astro` sobre o script inline da galeria (`photos` via `define:vars`).

Estado visual recente:

- Hero usa bento premium: um unico card grande arredondado, com imagem unica de fundo para desktop/mobile.
- O bento da hero agora segue a logica dos cards de servicos: moldura externa branca real, com imagem recuada internamente em vez de apenas stroke/sombra interna.
- Imagens finais da hero foram exportadas do Figma node `71:2` do arquivo `eIGmItv6LdatT0BOoMfKvj`:
  - `image 7` -> `frontend/public/images/redesign/hero-bento-desktop.webp` (`1716x917`).
  - `image 8` -> `frontend/public/images/redesign/hero-bento-mobile.webp` (`941x1672`).
- `Hero.astro` foi ajustado para declarar `width="1716"` e `height="917"` no asset desktop.
- A navegacao/active state foi estabilizada: cliques entre secoes usam Lenis quando disponivel, calculam offset real da header sticky e evitam disputa entre clique e observacao de scroll.

Cuidados de continuidade:

- Nao substituir a hero por pets separados em colunas; a decisao continua sendo asset unico dentro de bento.
- Se trocar fotos da galeria, manter os paths e composicao visual do site atual; validar com `pnpm build`.
- Se mexer na nav, preservar a fonte unica de active state em `frontend/src/components/Header.astro`.
- Se mexer na hero, preservar a moldura externa branca em `.hero-bento` e o recuo interno de `.hero-picture`.

## Estado tecnico historico do repo

Repositorio clonado em:

`/home/johny/Documentos/projetos/aumivet`

Origem:

`https://github.com/jooh44/aumivet-cl-nica-veterin-ria-em-curitiba`

Estado historico relevante da retomada:

- Branch atual: `master`.
- O projeto nao usa CMS no estado atual.
- Codigo e documentacao legada de Strapi/CMS foram removidos.
- Busca por termos de Strapi ficou limpa fora de `node_modules`, `.next` e `.git`.
- O frontend ja foi Next durante a limpeza inicial, mas o app ativo em 2026-05-23 e Astro. Nao tratar `frontend/app/` ou componentes React antigos como fonte atual.
- Na etapa antiga, `npm audit --omit=dev` retornou `found 0 vulnerabilities` e `npm run build` passou no Next.
- No estado atual Astro, usar `pnpm build` dentro de `frontend/`.

Comandos principais:

```bash
cd frontend
pnpm install
pnpm build
pnpm preview
```

## Limpeza ja feita

Foram removidos ou ajustados os pontos ligados a Strapi:

- docs antigos de Strapi/deploy na raiz;
- scripts legados em `deploy/`;
- `frontend/app/api/revalidate/route.ts`;
- `frontend/lib/strapi.ts`;
- `frontend/types/strapi.ts`;
- referencias de env `STRAPI`, `NEXT_PUBLIC_STRAPI`, `REVALIDATE_SECRET` e dominios antigos;
- `frontend/next.config.js`;
- `docker-compose.yaml` e `docker-compose-frontend.yaml`;
- `.env.example`, `frontend/.env.example`, `frontend/README.md` e `CLAUDE.md`.

Nao reintroduzir CMS, Strapi ou revalidate webhook sem decisao explicita.

## Integração Google Ads (Tracking e API) — 2026-05-24

O rastreamento do Google Ads foi configurado dinamicamente no site Astro (`frontend/src/layouts/BaseLayout.astro`) e as ferramentas locais de gerenciamento de campanhas via API foram estruturadas em `google-ads/`.

- **Google Tag (gtag.js)**: Configurada no cabeçalho do `BaseLayout.astro`. Carrega e inicializa a tag se a variável de ambiente `PUBLIC_GOOGLE_TAG_ID` estiver definida no ambiente.
- **Rastreamento de Conversões**: Cliques em links do WhatsApp (`wa.me` ou `api.whatsapp.com`) e Telefone (`tel:`) são capturados de forma automática e enviam eventos de conversão de leads usando as labels configuradas no ambiente (`PUBLIC_WA_CONVERSION_LABEL` e `PUBLIC_PHONE_CONVERSION_LABEL`).
- **Gerenciador de Campanhas Local**: Pasta `google-ads/` configurada. Contém `rzads.py` e scripts herdados. As credenciais em `google-ads/.env.ads` estão configuradas para interagir diretamente com a conta da Aumivet (Customer ID: `9838845707`). O arquivo de credenciais está ignorado no Git para segurança.
- **Launch Readiness**: O site está pronto para lançamento e deploy de produção na Vercel (as variáveis de ambiente reais do Ads já foram configuradas no arquivo local `.env` e as conversões criadas via API). A galeria da seção "Conheça a Aumivet" foi atualizada com novas fotos em WebP em 2026-05-25.

## Galeria do site — 2026-05-25

A galeria atual do Astro usa 8 fotos novas baixadas do Drive do usuário, otimizadas para WebP em `frontend/public/images/gallery/`.

- Arquivo fonte do componente: `frontend/src/components/About.astro`.
- Layout: foto principal 4:3 com thumbnails em grade 2 colunas no desktop e scroll horizontal no mobile.
- Rótulos e legendas visíveis da galeria foram removidos em 2026-05-25 porque alguns nomes de ambientes ainda precisam de validação manual. Os textos `alt` permanecem para acessibilidade.
- Fotos antigas de baixa resolução removidas do `frontend/public/images/`: `aumivet-clinica-veterinaria-em-curitiba (1).jpg` a `(4).jpg`.
- O schema da home em `frontend/src/pages/index.astro` foi atualizado para apontar a nova imagem de recepção.
- Validado com `cd frontend && pnpm build`.

## Operação Google Ads — 2026-05-25

Foi criada a skill local `.agents/skills/aumivet-google-ads/SKILL.md` para orientar futuras sessões de Ads sem reaproveitar premissas da RZ Vet por engano.

Estado verificado via API:

- Conta Aumivet: `CUSTOMER_ID=9838845707`.
- A conta é acessível diretamente pelo OAuth atual; não usar `MANAGER_CUSTOMER_ID` como `login_customer_id` para Aumivet, salvo se `LOGIN_CUSTOMER_ID` for explicitamente configurado.
- Existe uma campanha antiga pausada: `SEARCH v0.5` (`22634313741`), budget `R$10/dia`. Não ativar como está: ela mistura adestramento, banho e tosa, atendimento domiciliar, termos genéricos amplos e copy antiga.
- Campanha nova criada via API em 2026-05-25: `Search | Cirurgias Curitiba | Aumivet | 2026-05` (`23882431819`), budget `R$16,50/dia`, CPC manual `R$2,50`, Curitiba + português, 38 negativas de campanha.
- Campanha ativada em 2026-05-25 após aprovação explícita do usuário, com agenda somente em dias úteis: segunda a sexta, 00:00-24:00, no fuso `America/Sao_Paulo`.
- Grupos criados: `Cirurgia Geral` (8 keywords, 1 RSA), `Catarata Petlove` (6 keywords, 1 RSA) e `Odontologia Veterinaria` (5 keywords, 1 RSA).
- Anúncios e keywords ficaram habilitados e em revisão (`REVIEW_IN_PROGRESS` / `UNDER_REVIEW`) após a criação/ativação. A campanha pode começar a servir quando a revisão do Google liberar os anúncios.
- O script `google-ads/scripts/ads/create_aumivet_search_cirurgias.py` foi atualizado para usar a URL canônica `https://aumivet.com.br/` e reaplicar isenções de política marcadas pela API como `is_exemptible`.
- Conversões encontradas: `WhatsApp Click (Aumivet)` label `vfMFCJLy7rIcENLey94_`; `Phone Click (Aumivet)` label `FIwuCI_-17IcENLey94_`; também há `Clique de saída whatsapp` codeless, que deve ser revisada para evitar duplicidade/otimização no sinal errado.
- Site ao vivo em `https://www.aumivet.com.br/` retorna 200 e contém `AW-17109806930`.
- A tentativa inicial com `https://www.aumivet.com.br/` foi rejeitada pela API como `DESTINATION_NOT_WORKING`; a URL canônica `https://aumivet.com.br/` foi aceita para os RSAs.
- Em 2026-05-25, as rotas `/servicos/cirurgias`, `/servicos/cirurgia-catarata` e `/servicos/odontologia` retornavam 404 no site ao vivo. Não ativar tráfego para essas URLs até existirem; a campanha criada usa a home como destino provisório.

## Cuidados para o proximo agente

- Antes de editar, verificar `git status --short`.
- Nao reverter delecoes de Strapi/CMS.
- Se for alterar proposta, editar diretamente `docs/proposta-comercial-aumivet.html`.
- Se for criar planejamento para Claude, usar este arquivo como fonte e manter a proposta final sem jargao tecnico.
- Se for mexer no site, preservar a direcao comercial: Petlove em evidencia, presenca local, contato facil, ranqueamento e busca com IA.
- O deploy mais recente foi feito a partir do site Astro em `frontend/`; nao retomar a landing estatica da raiz sem decisao explicita.
