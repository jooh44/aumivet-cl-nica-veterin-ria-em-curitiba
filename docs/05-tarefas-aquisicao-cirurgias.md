# Tarefas - Aquisicao de Cirurgias

Base: `docs/04-plano-aquisicao-cirurgias.md`
Ultima atualizacao: 2026-05-19
Status: backlog inicial

Cada tarefa tem critério de aceite e forma de verificar.
Numero entre colchetes indica dependencia (T-XX).

---

## Stream A - Off-site (sem codigo)

### T-01 - Sessao guiada de auditoria do Perfil da Empresa no Google

- Acao: agendar 30 min com a cliente para revisar e ajustar o GBP em tempo real.
- Aceite:
  - Nome exato: "Aumivet Clinica Veterinaria".
  - Categoria principal: Veterinario.
  - "Banho e tosa" removida (ou agendada para remocao na data de fechamento).
  - Adicionadas categorias secundarias relevantes ao painel (validar disponibilidade ao vivo).
  - Servicos cadastrados incluem: cirurgia geral, castracao, remocao de tumor, **cirurgia de catarata**, oftalmologia veterinaria, cirurgia odontologica, limpeza dental, anestesia, atendimento de emergencia.
  - Telefone, endereco, horario e URL conferem com o site.
  - Mensagens diretas habilitadas.
- Verifica: print do painel pos-ajuste salvo em `docs/evidencias/gbp-2026-XX-XX.png`.
- Arquivos: nenhum (acao externa).

### T-02 - Subir fotos atuais ao GBP

- Acao: enviar fotos da fachada, interior, equipe atual (que ja temos) ao perfil.
- Aceite: ao menos 6 fotos novas publicadas, com legenda quando possivel.
- Verifica: aba "Fotos" do GBP atualizada.
- Arquivos: nenhum.

### T-03 - Solicitar fotos dos demais medicos a cliente

- Acao: pedir a cliente fotos da Dra. Thaise no centro cirurgico, do anestesista e demais medicos da rotina, com mini-bio e CRMV.
- Aceite: pelo menos 1 foto + 1 paragrafo curto por especialista entregues.
- Verifica: assets salvos em `frontend/public/images/equipe/`.
- Bloqueia: T-12 (perfis nominados nas paginas).

### T-04 - Auditoria NAP cross-platform

- Acao: comparar nome, endereco e telefone entre site atual, GBP, pagina Petlove (`https://saude.petlove.com.br/rede-credenciada/pr/curitiba/aumivet-clinica-veterinaria`), Instagram da clinica, e qualquer outro diretorio que apareca em `"aumivet" + "curitiba"` no Google.
- Aceite: documento `docs/nap-audit.md` com tabela de cada plataforma e diferencas encontradas; lista de correcoes a aplicar.
- Verifica: arquivo criado e commitado.
- Depende de: T-01 (precisa do GBP atualizado primeiro).

### T-05 - Cross-link com Petlove

- Acao: a) garantir que a pagina Petlove da Aumivet tem link para `aumivet.com.br` (solicitar ajuste se nao tiver); b) adicionar selo "Credenciada Petlove Saude" no site linkando para a pagina deles.
- Aceite: link bidirecional ativo.
- Verifica: clicar no selo do site abre a pagina Petlove correta; clicar no link da Petlove (se conseguirmos adicionar) abre `aumivet.com.br`.
- Depende de: T-13 (selo no site faz parte do codigo).

---

## Stream B - On-site (codigo)

### T-06 - Capturar baseline antes da migracao

- Acao: rodar Lighthouse mobile em `https://www.aumivet.com.br/`, salvar relatorio; rodar `site:aumivet.com.br` no Google e copiar resultado.
- Aceite: arquivo `docs/baseline-2026-05-19.md` com pontuacoes Performance/SEO/Acessibilidade e lista de paginas indexadas.
- Verifica: arquivo existe.
- Arquivos: `docs/baseline-2026-05-19.md`.

### T-07 - Confirmar configuracao do projeto Vercel

- Acao: validar que o projeto Vercel aponta para `frontend/` (root directory). Confirmar dominio `www.aumivet.com.br` mapeado.
- Aceite: deploy preview gerado a partir de uma branch teste serve uma rota Next.js.
- Verifica: URL de preview Vercel acessivel.
- Arquivos: configuracao Vercel (UI).

### T-08 - Portar `index.html` para `frontend/app/page.tsx`

- Acao: converter o HTML estatico da home em componente React no App Router, preservando o visual.
- Aceite:
  - Visual identico em desktop e mobile (comparar screenshots).
  - Schema markup `VeterinaryCare` no `metadata`/JSON-LD do `app/layout.tsx`.
  - Imagens migradas para `frontend/public/images/`.
  - `npm run build` passa.
- Verifica: deploy preview da home pareceada com a atual.
- Arquivos: `frontend/app/page.tsx`, `frontend/app/layout.tsx`, `frontend/app/globals.css`, `frontend/public/images/`.

### T-09 - Validar schema markup pos-migracao

- Acao: rodar a URL do preview em `https://validator.schema.org/`.
- Aceite: zero erros, zero warnings criticos.
- Verifica: print do validador salvo em `docs/evidencias/schema-XX.png`.
- Depende de: T-08.

### T-10 - Criar componente `WhatsappCTA` com tracking

- Acao: criar componente client que dispara evento configuravel ao clicar e abre `wa.me/5541988604202` com mensagem pre-preenchida.
- Aceite:
  - Aceita prop `event` (string) e prop `message` (string).
  - Em ambiente dev, loga no console quando clicado.
  - Sem dependencia nova.
- Verifica: render no Storybook nao se aplica; verificar em pagina de teste.
- Arquivos: `frontend/components/WhatsappCTA.tsx`.

### T-11 - Criar componente `PhoneCTA` e `RouteCTA` com tracking

- Acao: equivalentes para telefone (click-to-call) e rota (link para `https://maps.google.com/?q=...`).
- Aceite: dispara eventos `cta_telefone` e `cta_rota` respectivamente.
- Verifica: teste em pagina temporaria.
- Arquivos: `frontend/components/PhoneCTA.tsx`, `frontend/components/RouteCTA.tsx`.

### T-12 - Criar pagina `/servicos/cirurgias` (guarda-chuva)

- Acao: pagina umbrella otimizando "cirurgia veterinaria curitiba". Hero com posicionamento amplo, lista das modalidades cobertas (cirurgia geral assinada por Dra. Thaise: castracao, tumor/nodulo, tecidos moles, abdominal, piometra, cesariana, emergencia; catarata como destaque com link para pagina dedicada; odontologica com link para pagina dedicada). Incluir bloco de equipe, seguranca anestesica, ambiente, **selo Petlove com link** (Petlove cobre todas as modalidades aqui), FAQ curto, CTAs.
- Aceite:
  - URL `https://www.aumivet.com.br/servicos/cirurgias` retorna 200.
  - Schema `MedicalProcedure` ou `Service` valido.
  - Inclui WhatsappCTA, PhoneCTA, RouteCTA com evento `servico=cirurgias`.
  - Link interno para `/servicos/cirurgia-catarata` e `/servicos/odontologia`.
  - Lighthouse mobile: Performance >= 85, SEO = 100.
- Verifica: deploy preview + Lighthouse.
- Arquivos: `frontend/app/servicos/cirurgias/page.tsx`.
- Depende de: T-08, T-10, T-11.

### T-12B - Criar pagina `/servicos/cirurgia-catarata` (USP)

- Acao: pagina dedicada destacando a unicidade: **unica clinica do Parana credenciada Petlove Saude para cirurgia de catarata**. Hero com esse posicionamento como headline. Explicar o procedimento, indicacao, recuperacao, equipe responsavel, seguranca anestesica, cobertura Petlove com selo reforcado, FAQ especifico (catarata em caes idosos, raca predisposta, sintomas), CTAs.
- Aceite:
  - URL `https://www.aumivet.com.br/servicos/cirurgia-catarata` retorna 200.
  - Schema `MedicalProcedure` com `procedureType` ou `Service` valido.
  - Hero contem a frase "unica do Parana credenciada Petlove Saude" de forma visivel.
  - Selo Petlove reforcado (variante com a copy especial).
  - WhatsappCTA com evento `servico=cirurgia_catarata` e mensagem pre-preenchida especifica.
  - Lighthouse mobile: Performance >= 85, SEO = 100.
- Verifica: deploy preview + Lighthouse.
- Arquivos: `frontend/app/servicos/cirurgia-catarata/page.tsx`.
- Depende de: T-08, T-10, T-11.

### T-13 - Criar pagina `/servicos/odontologia`

- Acao: igual a T-12 para odontologia.
- Aceite: mesmos criterios.
- Arquivos: `frontend/app/servicos/odontologia/page.tsx`.
- Depende de: T-08, T-10, T-11.

### T-14 - Criar componente `PetloveBadge` e inserir na home + paginas de servico

- Acao: bloco visual com logo/selo "Credenciada Petlove Saude" e frase curta, linkando para `https://saude.petlove.com.br/rede-credenciada/pr/curitiba/aumivet-clinica-veterinaria` com `rel="noopener"`. Suporta variantes de copy via prop (padrao, catarata-USP).
- Aceite:
  - Aparece em: home, `/servicos/cirurgias`, `/servicos/cirurgia-catarata`, `/servicos/odontologia`.
  - Em `/servicos/cirurgia-catarata`, usa variante "Unica clinica do Parana credenciada Petlove Saude para cirurgia de catarata".
  - Link abre pagina Petlove correta em nova aba.
- Verifica: clique abre pagina Petlove correta em nova aba.
- Arquivos: `frontend/components/PetloveBadge.tsx`.

### T-15 - Instalar GTM no layout

- Acao: incluir script GTM no `app/layout.tsx`, com id parametrizado por env var `NEXT_PUBLIC_GTM_ID`.
- Aceite:
  - GTM container criado.
  - Script presente em todas as paginas.
  - Sem dependencia nova npm.
- Verifica: extensao Tag Assistant detecta o container em preview.
- Arquivos: `frontend/app/layout.tsx`, `frontend/.env.example`.

### T-16 - Configurar GA4 dentro do GTM

- Acao: criar tag GA4 Configuration no GTM com Measurement ID, disparada em todas as paginas.
- Aceite: GA4 recebe pageview em DebugView.
- Verifica: DebugView GA4 mostra eventos.
- Depende de: T-15.

### T-17 - Eventos GTM para cliques de CTA

- Acao: criar triggers de clique e tags GA4 Event para `cta_whatsapp`, `cta_telefone`, `cta_rota`, com parametro `servico` (cirurgias, cirurgia_catarata, odontologia, home).
- Aceite: 3 eventos disparam corretamente em DebugView.
- Verifica: DebugView.
- Depende de: T-16, T-12, T-13.

### T-18 - Configurar conversoes no Google Ads

- Acao: criar conversoes `whatsapp_click`, `phone_click`, `route_click`. Importar do GA4 ou via gtag.
- Aceite:
  - 3 conversoes criadas.
  - `whatsapp_click` marcada como primaria.
  - Outras como secundarias.
- Verifica: aba "Conversoes" do Ads mostra "Recebendo conversoes" depois de cliques de teste.
- Depende de: T-17.

### T-19 - Sitemap e robots

- Acao: verificar `next-sitemap.config.js` gera sitemap correto incluindo paginas novas; confirmar `/robots.txt` permite crawl.
- Aceite: `https://www.aumivet.com.br/sitemap.xml` lista todas as paginas relevantes; `robots.txt` sem `Disallow: /`.
- Verifica: GET nas duas URLs.
- Arquivos: `frontend/next-sitemap.config.js` (validar).
- Depende de: T-12, T-13.

### T-20 - Deploy de producao

- Acao: merge para `master` apos validacao em preview.
- Aceite: `https://www.aumivet.com.br/` serve a nova home Next.js; redirect `aumivet.com.br -> www.aumivet.com.br` ativo.
- Verifica: `curl -I -L https://aumivet.com.br` retorna 200 final no `www`; visual confere.
- Depende de: T-08 ate T-19.

---

## Stream C - Preparacao Ads (sem ativar)

### T-21 - Pesquisa de palavras-chave

- Acao: usar Keyword Planner com sementes de cirurgia geral (castracao, tumor, abdominal, emergencia), **catarata (cirurgia catarata cachorro, oftalmologista veterinario, catarata petlove)** e odontologia.
- Aceite: planilha `docs/keywords.md` com termos, volume estimado, concorrencia, intencao.
- Verifica: arquivo criado.
- Depende de: T-18 (precisa de conta Ads ativa).

### T-22 - Lista de negativas inicial

- Acao: compilar termos a excluir.
- Aceite: arquivo `docs/negativas.md` com >=30 termos.
- Verifica: arquivo criado.

### T-23 - Copy de anuncios

- Acao: redigir headlines (15) e descricoes (4) por grupo, sitelinks (4), callouts (4).
- Aceite: arquivo `docs/ads-copy.md` por grupo de anuncio.
- Verifica: arquivo criado.

### T-24 - Estrutura de campanha em rascunho

- Acao: criar campanha em modo rascunho no Google Ads.
- Aceite: 1 campanha Search "Cirurgias - Curitiba" com 3 grupos (cirurgia geral, **catarata**, odontologia), localizacao, idioma, dispositivos, lance Maximizar cliques, orcamento R$ 16,50/dia, horario de atendimento. Negativas ortopedicas configuradas. Catarata recebe copy diferenciada com "unica do PR pela Petlove".
- Verifica: campanha visivel no Ads em modo pausado.
- Depende de: T-21, T-22, T-23.

---

## Gate final - Pre-lancamento

### T-25 - Checklist tecnico de go/no-go

- Acao: rodar checklist final da secao "Gate" em `docs/04-plano-aquisicao-cirurgias.md`.
- Aceite: todos os 11 itens marcados.
- Verifica: arquivo `docs/go-no-go-YYYY-MM-DD.md` com cada item validado e link/print de evidencia.
- Depende de: T-01 a T-24.

### T-26 - Ativar campanha

- Acao: despausar campanha apos aprovacao escrita da cliente.
- Aceite: campanha ativa, conversoes recebendo.
- Verifica: monitorar primeiras 48h.
- Depende de: T-25.

---

## Ordem sugerida de execucao

Semana 1:
- Stream A: T-01, T-02, T-03 (solicitacao), T-04.
- Stream B: T-06, T-07, T-08, T-09, T-10, T-11.

Semana 2:
- Stream B: T-12, T-13, T-14, T-15, T-16, T-17.
- Stream A: T-05.

Semana 3:
- Stream B: T-18, T-19, T-20.
- Stream C: T-21, T-22, T-23.

Semana 4:
- Stream C: T-24.
- Gate: T-25.
- Ativacao: T-26.

Cronograma assume disponibilidade da cliente para T-01 e T-18 (acessos).
