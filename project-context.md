# Project Context - Aumivet

Ultima atualizacao: 2026-05-19

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
- `frontend/`: aplicacao Next.js.
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

## Estado tecnico do repo

Repositorio clonado em:

`/home/johny/Documentos/projetos/aumivet`

Origem:

`https://github.com/jooh44/aumivet-cl-nica-veterin-ria-em-curitiba`

Estado relevante:

- Branch atual: `master`.
- O projeto nao usa CMS no estado atual.
- Codigo e documentacao legada de Strapi/CMS foram removidos.
- Busca por termos de Strapi ficou limpa fora de `node_modules`, `.next` e `.git`.
- `frontend` usa Next `^16.3.0-canary.19`, necessario na retomada porque a versao estavel mais recente ainda mantinha dependencia vulneravel via `postcss`.
- `npm audit --omit=dev` retornou `found 0 vulnerabilities`.
- `npm run build` em `frontend` passou.
- `frontend/public/sitemap.xml` e `frontend/tsconfig.json` foram alterados pelo build/Next.

Comandos principais:

```bash
cd frontend
npm ci
npm run build
npm audit --omit=dev
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

## Cuidados para o proximo agente

- Antes de editar, verificar `git status --short`; ha muitas alteracoes nao commitadas desta retomada.
- Nao reverter delecoes de Strapi/CMS.
- Se for alterar proposta, editar diretamente `docs/proposta-comercial-aumivet.html`.
- Se for criar planejamento para Claude, usar este arquivo como fonte e manter a proposta final sem jargao tecnico.
- Se for mexer no site, preservar a direcao comercial: Petlove em evidencia, presenca local, contato facil, ranqueamento e busca com IA.
- Confirmar depois se o deploy oficial continuara na landing estatica da raiz ou migrara para o app Next.js.
