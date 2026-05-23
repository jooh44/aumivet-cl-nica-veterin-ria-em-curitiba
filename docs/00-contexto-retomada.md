# Contexto de retomada - Aumivet

Ultima atualizacao: 2026-05-14

## Cliente

Aumivet, clinica veterinaria em Curitiba.

Dados presentes no site/codigo:

- Marca: Aumivet Clinica Veterinaria.
- Responsavel/fundadora em destaque: Dra. Thaise, medica veterinaria, PUCPR.
- Endereco: R. Santo Antonio, 891 - Reboucas, Curitiba - PR, 80230-120.
- WhatsApp/telefone principal: (41) 98860-4202.
- Email no schema da landing: `aumivet.clinica@gmail.com`.
- Site: `https://aumivet.com.br`, com redirecionamento para `https://www.aumivet.com.br/`.

## Oferta atual percebida

Servicos principais:

- Consultas e vacinas.
- Cirurgias especializadas.
- Exames e diagnostico.
- Odontologia veterinaria.
- Banho, tosa e estetica pet.
- Adestramento.
- Atendimento/estrutura para veterinarios parceiros.
- Consultas com especialistas.
- Anestesista volante.
- Cirurgia volante.
- Leva e traz / taxi pet.

Provas e diferenciais existentes:

- Fotos reais da clinica, equipe e carro.
- Tour virtual 360 incorporado na landing estatica.
- Depoimentos atribuidos ao Google.
- Equipe com especialidades relevantes: clinica/cirurgia, anestesiologia, odontologia, oftalmologia.
- Localizacao em Reboucas, com potencial para campanhas hiperlocais em Curitiba.

## Estado tecnico do repositorio

Estrutura relevante:

- `index.html` e `styles.css`: landing estatica completa.
- `images/`: imagens usadas pela landing estatica.
- `frontend/`: app Next.js 15 com App Router, Tailwind, TypeScript, componentes React e blog estatico.
- `frontend/public/images/`: copia dos ativos usados pelo Next.js.
- `docker-compose.yaml` e `docker-compose-frontend.yaml`: configuracao para frontend em container com Traefik/Coolify.
- Documentos antigos de CMS/deploy foram removidos na limpeza de retomada.

## Verificacoes feitas em 2026-05-14

Clone:

```bash
git clone https://github.com/jooh44/aumivet-cl-nica-veterin-ria-em-curitiba .
```

Repositorio:

- Branch atual: `master`.
- Ultimos commits indicam remocao do CMS da entrega principal e correcao de posts estaticos.

Site publico:

```bash
curl -I -L https://aumivet.com.br
```

Resultado observado:

- `https://aumivet.com.br` retorna `307` para `https://www.aumivet.com.br/`.
- `https://www.aumivet.com.br/` retorna `200`.
- Servidor: Vercel.
- Conteudo publico bate com a landing estatica da raiz.

Build local do Next.js:

```bash
cd frontend
npm ci
npm run build
```

Resultado:

- Build concluido com sucesso.
- Rotas geradas: `/`, `/blog`, `/blog/[slug]`, `/contato`, `/servicos`, `/sobre`, `/robots.txt`, `/sitemap.xml`.
- `next-sitemap` gerou sitemap.
- Em 2026-05-14, `npm audit --omit=dev` retornou `found 0 vulnerabilities` apos atualizacao de dependencias.

Riscos tecnicos encontrados:

- O `next` foi atualizado para `16.3.0-canary.19` porque a versao estavel mais recente disponivel ainda mantinha dependencia vulneravel de `postcss`.
- O app atual possui blog estatico e nao depende de CMS.
- `frontend/app/layout.tsx` contem `verification.google` placeholder (`google-site-verification-code`), que precisa ser substituido antes de qualquer claim no Search Console.
- Nao ha confirmacao local de GA4/GTM/conversoes do Google Ads funcionando.

## Implicacoes para Google Ads

O site ja tem material suficiente para campanha de fundo de funil, mas a proposta nao deve prometer performance sem antes fechar medicao.

Prioridades antes/depois de iniciar midia:

1. Confirmar acesso a Google Ads, GA4, Search Console e Google Business Profile.
2. Instalar ou validar GTM/GA4.
3. Medir cliques no WhatsApp, chamadas, formulario e rotas de contato.
4. Separar conversoes primarias de conversoes secundarias.
5. Definir regioes e servicos de maior margem/capacidade.
6. Criar estrutura de campanha por intencao: marca, emergencia/consulta, servicos especificos e B2B veterinario parceiro, se fizer sentido.

## Leitura comercial

Aumivet tem dois blocos de receita que podem ser trabalhados separadamente:

- B2C: tutores buscando veterinario, consulta, banho/tosa, vacina, odontologia, exames, cirurgia e emergencia.
- B2B/local-profissional: veterinarios/clininicas buscando estrutura, anestesista volante ou cirurgiao volante.

Isso abre um upsell defensavel: nao vender apenas "gestao de trafego", mas um pacote de ativacao comercial com tracking, pagina/landing por servico, Google Business Profile, SEO local e organizacao do funil de WhatsApp.
