# Plano de implementacao - Aquisicao de Cirurgias

Spec base: `docs/03-spec-aquisicao-cirurgias.md`
Ultima atualizacao: 2026-05-19

## Visao geral

Quatro fluxos rodam em paralelo onde possivel, com gates entre fases. Ads so ativa quando o gate final de verificacao passar.

```
┌─────────────────────────────────────────────────────────────────┐
│ STREAM A - Sinais off-site (sem codigo)                         │
│   GBP audit -> NAP audit -> Petlove cross-link                  │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│ STREAM B - On-site (codigo no Next.js)                          │
│   Baseline -> Portar home -> Paginas servico -> Tracking -> Deploy│
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│ STREAM C - Preparacao Ads (sem ativar)                          │
│   Keywords -> Negativas -> Copy -> Estrutura -> Conversoes      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ GATE: verificacao final │
                  └─────────────────────────┘
                              │
                              ▼
                       Ativar Ads
```

Streams A e B podem comecar simultaneamente. Stream C comeca depois que B tem ao menos as paginas de servico publicadas. Gate final bloqueia ativacao do Ads.

## Stream A - Off-site (alta alavanca, sem codigo)

Sequencial dentro do stream.

1. **Auditoria GBP**
   - Confirmar nome exato "Aumivet Clinica Veterinaria".
   - Remover categoria "Banho e tosa".
   - Adicionar categorias secundarias se disponiveis: "Clinica veterinaria", "Hospital veterinario", "Servico de cirurgia veterinaria" (validar quais existem no painel).
   - Cadastrar servicos individuais com descricao: cirurgia geral, castracao, remocao de tumor, cirurgia de catarata, oftalmologia veterinaria, cirurgia odontologica, limpeza dental, exames, anestesia, atendimento de emergencia. Nao destacar cirurgia ortopedica (terceirizada e fora da cobertura Petlove).
   - Adicionar "Cirurgia de catarata" como servico principal com descricao reforcando "unica do Parana credenciada Petlove Saude".
   - Atualizar horario, telefone, endereco, URL do site.
   - Subir fotos atualizadas (interior, fachada, equipe que ja temos).
   - Habilitar mensagens diretas se nao estiver ativo.
   - Pedir e responder reviews (definir rotina).

2. **NAP audit cross-platform**
   - Validar consistencia entre: site (`aumivet.com.br`), GBP, pagina Petlove (`saude.petlove.com.br/rede-credenciada/pr/curitiba/aumivet-clinica-veterinaria`), Instagram, qualquer diretorio listado.
   - Documentar variacoes encontradas em `docs/nap-audit.md`.

3. **Petlove cross-link e prova social**
   - Adicionar selo "Credenciada Petlove Saude" no site, linkando para a pagina publica da Aumivet no diretorio Petlove.
   - Confirmar com a cliente se podemos solicitar a Petlove um botao "Site da clinica" linkando para `aumivet.com.br` (se ainda nao existe na pagina deles).

Risco: GBP exige acao no painel da cliente. Mitigacao: agendar sessao guiada de 30 min com ela.

## Stream B - On-site (codigo)

Sequencial dentro do stream. Comecar em paralelo com Stream A.

1. **Baseline de performance e indexacao**
   - Capturar Lighthouse mobile da landing estatica atual em `/`.
   - Capturar lista de paginas indexadas hoje (via `site:aumivet.com.br` no Google).
   - Salvar em `docs/baseline-2026-05-19.md` para comparar pos-migracao.

2. **Decisao de stack canonico**
   - Confirmar: portar a landing estatica para o Next.js (home React preservando o visual atual) e deployar Next.js como unico site no `aumivet.com.br`.
   - Justificativa: site unico evita conflito de canonico; permite escalar com mais paginas indexaveis; design atual e simples o suficiente para portar em horas.

3. **Portar home estatica para Next.js**
   - Mover `index.html` para `frontend/app/page.tsx` como componentes React.
   - Mover `styles.css` para `frontend/app/globals.css` ou modulos.
   - Garantir que o schema markup `VeterinaryCare` esta no `frontend/app/layout.tsx` ou `page.tsx`.
   - Validar com `validator.schema.org`.

4. **Paginas de servico**
   - `frontend/app/servicos/cirurgias/page.tsx` (guarda-chuva: cirurgia veterinaria com todas as modalidades cobertas, excluindo ortopedica).
   - `frontend/app/servicos/cirurgia-catarata/page.tsx` (USP: unica do Parana credenciada Petlove para catarata).
   - `frontend/app/servicos/odontologia/page.tsx`.
   - Cada uma com: hero, descricao do procedimento, equipe (placeholder se faltar foto), seguranca anestesica, ambiente, selo Petlove com link para diretorio, FAQ curto, CTA WhatsApp + telefone + rota.
   - Pagina de catarata destaca em hero e em selo o status de unicidade Petlove-PR.
   - Schema markup `MedicalProcedure` ou `Service`.

5. **Selo Petlove na home e nas paginas cobertas**
   - Bloco "Credenciada Petlove Saude" com logo, frase curta de prova e link externo para a pagina da Aumivet no diretorio Petlove.
   - Aparece em: home, `/servicos/cirurgias`, `/servicos/cirurgia-catarata`, `/servicos/odontologia`.
   - Em `/servicos/cirurgia-catarata`, o selo carrega copy reforcada: "Unica clinica do Parana credenciada Petlove Saude para cirurgia de catarata."

6. **Tracking GTM + GA4**
   - Adicionar GTM no `frontend/app/layout.tsx`.
   - Criar container GA4 (se nao existir).
   - Eventos: `cta_whatsapp`, `cta_telefone`, `cta_rota`, `view_servico` (com parametro de qual servico).
   - Configurar DebugView GA4 para validar.

7. **Conversao Google Ads**
   - Criar conta Google Ads (se nao existir) ou usar acesso existente.
   - Criar conversoes: `whatsapp_click`, `phone_click`, `route_click`.
   - Importar via GTM ou direto via gtag.
   - Marcar `whatsapp_click` como primaria, demais como secundarias.

8. **Deploy Vercel**
   - Configurar projeto Vercel apontando para `frontend/`.
   - Domain settings: `aumivet.com.br` -> redirect 308 para `www.aumivet.com.br`.
   - Garantir que push para `master` deploya producao.
   - Validar redirects e canonico.

9. **Sitemap + robots**
   - Confirmar `next-sitemap` rodando no build.
   - `robots.txt` permitindo crawl.
   - Quando GSC liberar, submeter sitemap.

Riscos do stream B:
- Portar landing pode introduzir regressao visual. Mitigacao: comparar screenshot antes/depois em desktop e mobile.
- Tracking quebrado nao bloqueia o site, mas bloqueia o Ads. Validar com DebugView antes do gate.

## Stream C - Preparacao Ads (sem ativar)

Comeca depois que Stream B termina pelo menos as paginas de servico (etapa B.4).

1. **Pesquisa de palavras-chave**
   - Termos cirurgia geral (umbrella): "cirurgia veterinaria curitiba", "castracao cachorro curitiba", "castracao gato curitiba", "remocao tumor cachorro", "cirurgia abdominal cachorro", "piometra cachorro", "cesariana cadela", "emergencia veterinaria curitiba".
   - Termos catarata (USP, alta prioridade): "cirurgia catarata cachorro", "cirurgia catarata cachorro curitiba", "catarata em cachorro", "oftalmologista veterinario curitiba", "cirurgia catarata petlove", "catarata cachorro plano de saude".
   - Termos odontologia: "limpeza dental cachorro curitiba", "extracao dente cachorro", "tartaro cachorro curitiba", "odontologia veterinaria curitiba".
   - Negativar termos ortopedicos ("ortopedia", "fratura", "ruptura ligamento", "tplo", "joelho") ja que e terceirizado e nao coberto Petlove.
   - Validar volume via Keyword Planner (precisa de conta Ads ativa).

2. **Lista de negativas iniciais**
   - "gratis", "curso", "faculdade", "concurso", "ufpr", "puc", "preco baixo" (se nao for posicionamento), "low cost", "domiciliar" (se nao oferecermos), "24h" (se nao for o caso para cirurgia agendada).

3. **Copy de anuncio**
   - 3 grupos: cirurgia geral (umbrella), cirurgia catarata (USP), odontologia.
   - 3 headlines + 2 descricoes por grupo, com sitelinks para WhatsApp, /servicos/cirurgia-geral, /servicos/odontologia, /sobre.

4. **Estrutura da campanha**
   - 1 campanha Search "Cirurgias - Curitiba".
   - Localizacao: Curitiba + raio de 15 km (validar com a cliente).
   - Idioma: portugues.
   - Lance: Maximizar cliques inicialmente (poucos dados); migrar para Maximizar conversoes apos 30 conversoes.
   - Orcamento diario: ~R$ 16,50 (teto R$ 500/mes).
   - Horario: dias e horarios de atendimento da clinica.
   - Dispositivos: priorizar mobile.

5. **Importacao de conversao**
   - Conversao primaria: `whatsapp_click`.
   - Secundarias: `phone_click`, `route_click`.

Risco: verba pequena. Mitigacao: comecar com catarata (baixa concorrencia, alta intencao, ticket alto, USP unica) e cirurgia geral (volume); ligar odontologia quando os primeiros estabilizarem CPL. Catarata tende a entregar o melhor ROAS pela combinacao de baixo CPC esperado + USP forte.

## Gate de verificacao final

Antes de ativar a campanha, validar todos os 6 criterios do spec (`docs/03-spec-aquisicao-cirurgias.md` secao Success Criteria).

Checklist tecnico imediato:

- [ ] `https://www.aumivet.com.br/servicos/cirurgias` retorna 200 e tem schema valido.
- [ ] `https://www.aumivet.com.br/servicos/cirurgia-catarata` retorna 200, schema valido, hero reforca "unica do Parana credenciada Petlove".
- [ ] `https://www.aumivet.com.br/servicos/odontologia` retorna 200 e tem schema valido.
- [ ] Click em WhatsApp dispara `cta_whatsapp` no GA4 DebugView.
- [ ] Click em telefone dispara `cta_telefone`.
- [ ] Click em rota dispara `cta_rota`.
- [ ] Conta Ads tem conversao `whatsapp_click` importada e marcada como primaria.
- [ ] GBP sem categoria "Banho e tosa", com servicos de cirurgia cadastrados.
- [ ] Selo Petlove visivel no site com link para diretorio Petlove.
- [ ] NAP identico em site, GBP, Petlove.
- [ ] Lighthouse mobile das paginas de servico: Performance >= 85, SEO = 100.
- [ ] `npm run build` sem erros, `npm audit --omit=dev` sem vulnerabilidades.

Quando todos checados: liberar ativacao Ads.

## Pos-lancamento (primeiros 30 dias)

Acompanhar semanalmente:

- Cliques por palavra-chave; bloquear quem nao gera contato.
- CPL por servico.
- Conversa qualificada vs lixo no WhatsApp (cliente classifica).
- Aparecimento da marca "Aumivet" no autocomplete sem variantes erradas.
- Crescimento de paginas indexadas (`site:aumivet.com.br`).

## Dependencias e ordem

Caminho critico (sequencial obrigatorio):

```
Decisao stack (B.2) -> Portar home (B.3) -> Servicos (B.4) -> Tracking (B.6) -> Conversao Ads (B.7) -> Deploy (B.8) -> Gate -> Ativar Ads
```

Pode rodar em paralelo:

- Stream A inteiro com Stream B.
- B.5 (selo Petlove) com B.6 (tracking).
- Stream C.1 ate C.4 com Stream B a partir de B.4.

Bloqueadores explicitos:

- Solicitar fotos dos outros medicos -> nao bloqueia lancamento; bloqueia "perfis nominados".
- Acesso Google Ads -> bloqueia Stream C completo.
- Acesso GBP -> bloqueia Stream A.1.
- Decisao de preco publico -> bloqueia copy final das paginas (pode ir com "solicite orcamento" como fallback).
