# Cronograma de Atividades — RZ VET
## Abril a Junho de 2026

**Data:** 09/04/2026
**Responsável:** Johny Oliveira — Arquitetura Digital / Gestão de Tráfego / Comercial
**Para:** Rafael — RZ Vet

---

## VISÃO GERAL

Este documento consolida todas as atividades pendentes e em andamento, organizadas por área e prioridade. O foco é **resultado direto no faturamento**: tema da loja rodando 100%, Google Ads otimizado, API Tray integrada ao Chatwoot, catálogo Merchant Center completo e SEO/AIO do e-commerce.

**ZOR Importadora**: retirada do escopo conforme alinhado em 08/03. Toda a metodologia desenvolvida para a ZOR (SEO, GMN, AIO) será aplicada na RZ Vet primeiro. Quando a RZ estiver consolidada, replica-se para a ZOR.

---

## 1. TEMA DA LOJA TRAY — PRIORIDADE MÁXIMA

**Deadline: 20/04/2026** (conforme reunião 08/03)

| # | Atividade | Status | Detalhe |
|---|---|---|---|
| 1.1 | Implementar layout planejado sobre tema base da Tray | Em andamento | Código limpo, sem dívida técnica da DevRocket |
| 1.2 | Migrar customizações visuais dos layouts HTML salvos | Pendente | Aproveitar os layouts já prontos em HTML |
| 1.3 | Testar todas as páginas na loja teste da Tray | Pendente | Ambiente teste liberado pela Tray esta semana |
| 1.4 | Validar responsividade (mobile/tablet/desktop) | Pendente | — |
| 1.5 | Testar fluxo completo: navegação → produto → carrinho → checkout → pagamento | Pendente | Zero bugs antes de subir |
| 1.6 | Validar integração com meios de pagamento | Pendente | — |
| 1.7 | Subir tema otimizado na loja de produção | Pendente | Só após todos os testes passarem |

**Entrega até 20/04:** Tema novo otimizado no ar, rodando 100%, sem bugs.

**Nota:** O prazo de 20/04 é especificamente para o tema otimizado. As demais atividades (API Tray, Merchant Center, SEO avançado, etc.) seguem o cronograma geral abaixo.

---

## 2. GOOGLE ADS — OTIMIZAÇÃO CONTÍNUA

| # | Atividade | Status | Detalhe |
|---|---|---|---|
| 2.1 | Monitoramento semanal via API Python | Ativo | Scripts `core/` já construídos e funcionando |
| 2.2 | Aguardar recalibração do Smart Bidding | Em andamento | 2-3 semanas após ativação (01/04). Avaliar em ~15/04 |
| 2.3 | Trocar cartão de pagamento padrão | **URGENTE** | Usar cartão ••••0369 (que funcionou em 09/mar) como padrão para evitar nova recusa |
| 2.4 | Configurar alertas de pagamento no Google Ads | Pendente | Para nunca mais ter campanha parada por falta de pagamento |
| 2.5 | Revisão de budget após dados limpos (meta: abril) | Pendente | Budget atual R$55,80/dia — avaliar aumento após ticket médio recuperar |
| 2.6 | Relatório mensal abril com comparativo vs. março | Pendente | Entregar até 05/05 |

**Contexto:** A queda de faturamento em março (R$94k → R$54k) foi causada por falha de pagamento do cartão ••••4026 que deixou campanhas offline por 21 dias. O pagamento foi regularizado em 09/mar com cartão ••••0369. Keywords de monitores (alto ticket) foram reativadas em 01/04. Aguardando recalibração.

---

## 3. CHATWOOT + API TRAY — INTEGRAÇÃO

**Dependência:** Homologação da integração na Tray (acesso à loja teste já funcional; após homologação, chaves oficiais da RZ Vet serão liberadas)

| # | Atividade | Status | Detalhe |
|---|---|---|---|
| 3.1 | Homologação da integração API Tray | Em andamento | Acesso à loja teste funcional; após aprovação, chaves oficiais da RZ Vet serão liberadas |
| 3.2 | Implementar consulta de pedidos via API Tray | Pendente | Endpoint: buscar pedido por nome/CPF/número |
| 3.3 | Integrar consulta no fluxo do DataCrazy | Pendente | Cliente pergunta "cadê meu pedido?" → DataCrazy aciona integração Tray → responde automaticamente |
| 3.4 | Implementar consulta de rastreio via API Tray | Pendente | Puxar código de rastreio + transportadora + status (a confirmar disponibilidade do endpoint) |
| 3.5 | Automação de confirmação de pedido | Pendente | Novo pedido na Tray → template Meta automático para o cliente |
| 3.6 | Automação de atualização de rastreio | Pendente | Status muda na Tray → template Meta com código de rastreio |
| 3.7 | Widget do Chatwoot no site da loja | **Pendente** | Era pra ter sido implementado antes — ficou atrasado pelos problemas com a Meta |

**Impacto esperado:** Vendedores param de enviar rastreio manualmente. Clientes consultam pedidos direto pelo WhatsApp oficial. Libera tempo da equipe para prospecção ativa (conforme alinhado na ata de 16/03).

---

## 4. GOOGLE MERCHANT CENTER — CATÁLOGO

| # | Atividade | Status | Detalhe |
|---|---|---|---|
| 4.1 | Auditar feed de produtos atual | Pendente | Verificar títulos, descrições, GTINs, imagens, categorias |
| 4.2 | Otimizar títulos de produtos para busca | Pendente | Incluir marca + tipo + especificação (ex: "Monitor Multiparamétrico Veterinário Portátil") |
| 4.3 | Corrigir imagens que não atendem requisitos do Merchant | Pendente | Fundo branco, sem texto sobreposto, resolução mínima |
| 4.4 | Completar atributos obrigatórios faltantes | Pendente | GTIN, MPN, brand, condition, availability |
| 4.5 | Ativar avaliações de produto (se elegível) | Pendente | Usar tag GTM "Google Avaliações - Variáveis" que já extrai GTINs |
| 4.6 | Revisar Shopping campaigns vinculadas ao Ads | Pendente | Após feed otimizado |

---

## 5. SEO + AIO DO E-COMMERCE

**Contexto:** Mesmo sendo PHP/Twig (Tray), a RZ Vet já tem autoridade de domínio. Com o tema novo, vamos otimizar.

| # | Atividade | Status | Detalhe |
|---|---|---|---|
| 5.1 | Estrutura de headings (H1/H2/H3) no tema novo | No tema | Implementar junto com o layout |
| 5.2 | Meta titles e descriptions otimizados por categoria | Pendente | Templates com keyword + marca + diferencial |
| 5.3 | Schema markup de produtos (Product, Offer, Review) | Pendente | Structured data para rich snippets no Google |
| 5.4 | Schema markup da organização (LocalBusiness) | Pendente | NAP consistente |
| 5.5 | Otimizar URLs de categorias e produtos | Pendente | Verificar o que a Tray permite customizar |
| 5.6 | Alt text de imagens de produtos | Pendente | Descritivo, com keyword natural |
| 5.7 | Velocidade de carregamento (Core Web Vitals) | Pendente | Tema base da Tray tende a ser mais leve que DevRocket customizado |
| 5.8 | Conteúdo AIO: FAQ de produto com perguntas reais | Pendente | "Qual monitor veterinário comprar?", "Diferença entre monitor X e Y" — pra IAs citarem |
| 5.9 | Breadcrumbs estruturados | No tema | Implementar no layout |

---

## 6. OPERACIONAL COMERCIAL (já implementado / manutenção)

| # | Atividade | Status | Detalhe |
|---|---|---|---|
| 6.1 | Chatwoot + Bridge Meta (API oficial) funcionando | Ativo | Porta 3500, inboxes 11-14 |
| 6.2 | Templates Meta (rastreio, confirmação, entrega, reativação) | Em correção | Correção aplicada + testes internos realizados. Testes com a equipe agendados para 10/04 |
| 6.3 | Bridge GOWA (WhatsApp vendedores) | Ativo parcial | Inbox 23 (testes) OK. Lucas como piloto (inbox 21) pendente conexão |
| 6.4 | Fluxo inicial no DataCrazy | A migrar | Typebot deixa de ser runtime alvo; fluxo deve ser implementado no DataCrazy |
| 6.5 | Manual de atendimento atualizado | Ativo | Publicado em rzequipamentos.com.br |
| 6.6 | Sistema de etiquetas do funil | Implementado | lead-novo → qualificado → negociação → proposta → fechamento → venda/perdido |
| 6.7 | Automação de encerramento (24h sem resposta) | Ativo | Resolve conversa + mensagem de reativação automática |
| 6.8 | Regra dos 10 dias para propostas | Definido | Conforme reunião 25/03 — após 10 dias sem evolução, resolver e voltar pra fila |

**Decisão reunião 08/03:** Deixar sistema como está. Equipe continua recebendo pelo Chatwoot. Rastreios vão pelo WhatsApp individual de cada vendedor até a API Tray estar integrada. Bug de envio proativo para contatos frios → engavetado (limitação da Meta, não do sistema).

---

## CRONOGRAMA CONSOLIDADO

### Abril 2026

| Semana | Foco principal | Entregas |
|---|---|---|
| 07-13/abr | Tema Tray: layout + testes loja teste | Layout migrado, testes em andamento |
| 14-20/abr | Tema Tray: finalizar + subir produção | **Tema novo no ar (deadline 20/04)** |
| 21-27/abr | Google Ads: avaliar recalibração Smart Bidding + Widget Chatwoot no site | Relatório de performance + widget ativo |
| 28/abr-04/mai | API Tray: consulta de pedidos | MVP consulta de pedido funcionando |

### Maio 2026

| Semana | Foco principal | Entregas |
|---|---|---|
| 05-11/mai | API Tray: rastreio + integração DataCrazy | Consulta de pedido/rastreio no fluxo do DataCrazy |
| 12-18/mai | Automações de confirmação/rastreio via templates Meta | Fluxo automatizado ativo |
| 19-25/mai | SEO do tema novo: schema, headings, metas | Structured data implementado |
| 26/mai-01/jun | Google Ads: relatório maio + otimizações | Relatório comparativo mar→abr→mai |

### Junho 2026

| Semana | Foco principal | Entregas |
|---|---|---|
| 02-08/jun | Merchant Center: auditoria de feed | Feed auditado + correções iniciadas |
| 09-15/jun | Merchant Center: otimização títulos/imagens/atributos | Feed otimizado completo |
| 16-22/jun | AIO: FAQ de produtos + Shopping campaigns | Conteúdo publicado + campanhas Shopping ativas |
| 23-30/jun | **Entrega final + relatório consolidado** | Documento de tudo entregue e funcionando |

---

## MÉTRICAS DE ACOMPANHAMENTO

| Métrica | Março (baseline) | Meta Abril | Meta Junho |
|---|---|---|---|
| Faturamento loja | R$54.056 | R$70.000+ | R$90.000+ |
| Ticket médio | R$244 | R$350+ | R$450+ |
| Pedidos > R$1.000 | 2 | 6+ | 10+ |
| ROAS Google Ads | 18,4x | 25x+ | 30x+ |
| Receita atribuída Ads | R$25.333 | R$40.000+ | R$60.000+ |

---

## ITENS REMOVIDOS DO ESCOPO

| Item | Motivo | Quando retomar |
|---|---|---|
| ZOR Importadora (GMN, SEO, site) | Foco total na RZ Vet primeiro | Após RZ consolidada (Q3 2026) |
| GOWA rollout vendedores | Sistema estável; não gera faturamento direto agora | Após API Tray funcional |
| Bug envio proativo Meta (contatos frios) | Limitação da Meta, não do sistema | Monitorar atualizações da Meta |
| IP fixo do telefone comercial | Desativar conforme solicitado por Rafael | Imediato |

---

*Documento gerado em 09/04/2026 — Johny Oliveira, Digital Dog / RZ Vet*
