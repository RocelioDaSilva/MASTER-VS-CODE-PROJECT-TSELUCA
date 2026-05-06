# Website Launch Checklist & Content Guide

---

## PARTE 1 — PERGUNTAS PRÉ-LAUNCH (Preencher Primeiro)

Responder estas perguntas antes de usar os checklists abaixo.

### Informações do Negócio
| # | Pergunta | Resposta |
|---|----------|----------|
| 1 | Nome do negócio | |
| 2 | Objetivo principal do website (leads / vendas / branding) | |
| 3 | Público-alvo | |
| 4 | 3-5 serviços/produtos principais | |
| 5 | Área geográfica de atuação | |

### Metas do Website
| # | Pergunta | Resposta |
|---|----------|----------|
| 6 | Visitantes/mês desejados após 6 meses | |
| 7 | Leads/mês desejados | |
| 8 | Taxa de conversão alvo (típico: 2-5%) | % |
| 9 | 3 páginas/features mais críticas (em ordem) | |

### Time & Responsabilidades
| Função | Nome | Email |
|--------|------|-------|
| Gerente do Projeto | | |
| Responsável Técnico (hosting, domínio) | | |
| Responsável por Conteúdo | | |
| Responsável por Social Media | | |
| Tomador de Decisão Final | | |

### Informações de Contato para o Site
| Campo | Valor |
|-------|-------|
| Telefone principal | |
| Email principal | |
| Endereço | |
| Horários Seg-Sex | |
| Horários Sáb | |
| Redes sociais ativas | |

---

## PARTE 2 — CHECKLIST COMPLETO (5 Fases)

### FASE 1 — Planejamento & Estratégia
- [ ] Definir objetivos do website
- [ ] Identificar público-alvo
- [ ] Planejar estrutura de páginas (sitemap)
- [ ] Definir recursos necessários
- [ ] Estabelecer guia de marca (cores, fontes, logo)
- [ ] Definir orçamento e cronograma

### FASE 2 — Domínio & Hosting
- [ ] Registrar nome de domínio (.com, .com.br, etc.)
- [ ] Contratar provedor de hosting
- [ ] Configurar nameservers do domínio
- [ ] Verificar propagação DNS (24-48 horas)
- [ ] Configurar subdomínios se necessário (www, mail)

### FASE 3 — Desenvolvimento do Website
- [ ] Escolher abordagem:
  - [ ] HTML/CSS/JS manual (este projeto)
  - [ ] AI Builder (10Web, Webflow, Framer — ver docs/AI-TOOLS.md)
  - [ ] CMS (WordPress, Shopify)
- [ ] Design responsivo (mobile, tablet, desktop)
- [ ] Menu de navegação funcional
- [ ] Construir páginas essenciais:
  - [ ] Página inicial (Home)
  - [ ] Serviços / Produtos
  - [ ] Sobre Nós
  - [ ] Contato
  - [ ] Política de Privacidade
  - [ ] Termos & Condições
  - [ ] FAQ (recomendado)
  - [ ] Blog (recomendado para SEO)

### FASE 4 — Conteúdo
- [ ] Escrever copy da página inicial
- [ ] Criar descrições de serviços
- [ ] Escrever seção "Sobre"
- [ ] Criar bios da equipe (se aplicável)
- [ ] Desenvolver página FAQ
- [ ] Escrever posts de blog (mínimo 5 para SEO)
- [ ] Coletar imagens e mídia de alta qualidade
- [ ] Escrever meta descriptions para cada página
- [ ] Otimizar headings e conteúdo
- [ ] Substituir dados placeholder por dados reais:
  - [ ] Email: `contato@corhed.com` → email real
  - [ ] Telefone: `(11) 3000-0000` → telefone real
  - [ ] Endereço: `São Paulo, SP` → endereço real
  - [ ] Horários → horários reais
  - [ ] Testimonials → depoimentos reais (com permissão)
  - [ ] Stats → números reais

### FASE 5 — Segurança, SEO & Analytics
- [ ] Instalar certificado SSL (HTTPS)
- [ ] Atualizar todos os links para HTTPS
- [ ] Testar validade do SSL
- [ ] Configurar headers de segurança
- [ ] Configurar sistema de backup
- [ ] Configurar robots.txt (já existe na raiz)
- [ ] Criar/atualizar sitemap.xml com URLs reais
- [ ] Submeter sitemap no Google Search Console
- [ ] Verificar site no Bing Webmaster Tools
- [ ] Criar Google Business Profile (para negócios locais)
- [ ] Otimizar títulos e meta descriptions
- [ ] Adicionar schema markup se necessário
- [ ] Configurar Google Analytics 4
- [ ] Configurar metas/conversões no Analytics
- [ ] Testar formulários de contato
- [ ] Testar performance em mobile (Lighthouse)

---

## PARTE 3 — PRÉ-LAUNCH: CHECKLIST FINAL

### Conteúdo & Funcionalidade
- [ ] Todos os dados placeholder substituídos por dados reais
- [ ] Todos os links internos funcionando
- [ ] Formulário de contato testado e recebendo emails
- [ ] Sem typos ou erros gramaticais
- [ ] Todas as imagens têm alt text
- [ ] Nenhuma página com `index.html` em 404

### Performance & Compatibilidade
- [ ] Score Lighthouse: Performance ≥80, Acessibilidade ≥90
- [ ] Testado em Chrome, Firefox, Safari, Edge
- [ ] Testado em mobile (Android e iPhone)
- [ ] Tempo de carregamento < 3 segundos
- [ ] Imagens otimizadas (< 200KB cada)

### SEO & Segurança
- [ ] HTTPS ativo e sem avisos de conteúdo misto
- [ ] Meta title e description únicos em cada página
- [ ] Um `<h1>` por página
- [ ] sitemap.xml com URLs corretas submetido
- [ ] robots.txt não bloqueando páginas importantes
- [ ] Google Analytics instalado e coletando dados

### Legal & Privacidade
- [ ] Política de Privacidade publicada e vinculada no footer
- [ ] Termos & Condições publicados e vinculados
- [ ] Cookie Banner implementado (se usar cookies de tracking)
- [ ] LGPD/GDPR compliant (coleta de dados no formulário)

### Go-Live
- [ ] Backup completo antes do lançamento
- [ ] DNS apontado para servidor de produção
- [ ] DNS propagado e site acessível pelo domínio real
- [ ] Anunciar lançamento nas redes sociais
- [ ] Enviar link para clientes atuais e parceiros

---

## PARTE 4 — TEMPLATES DE CONTEÚDO

### Template de Post de Blog

```markdown
# [Keyword Principal] — [Benefício ou Gancho Numérico]

**Publicado:** [Data]
**Autor:** [Nome]
**Leitura:** [X] minutos

## Introdução
[Por que o leitor deveria se importar?]
[Apresentar o tema]
[O que vai aprender]

---

## [Subtópico 1]
[Explicação + exemplo + dados se disponíveis]

### [Sub-seção]
[Detalhes adicionais]

---

## [Subtópico 2]
[Conteúdo]

---

## [Subtópico 3]
[Conteúdo]

---

## Pontos-Chave
- Takeaway 1
- Takeaway 2
- Takeaway 3

## Conclusão
[Resumir pontos principais]
[Reafirmar valor]
[Call to Action]

---
**Pronto para [alcançar benefício]?**
[Link para página de contato ou serviço]
```

### Exemplos de Posts para Corhed

| Título | Keyword | Objetivo |
|--------|---------|----------|
| "5 erros em gestão de terminais POS que custam dinheiro ao banco" | gestão terminais POS | SEO + educação |
| "O que mudou com PCI DSS 4.0 e o que seu banco precisa fazer" | PCI DSS 4.0 | Autoridade |
| "Consumíveis bancários: como economizar sem comprometer a operação" | consumíveis bancários | awareness |
| "Gestão de meios de pagamento: guia completo para gerentes de TI bancário" | gestão meios pagamento | SEO principal |

### Template de Email de Prospecção B2B

```
Assunto: [Problema específico do banco] — Solução da Corhed

Olá [Nome],

Trabalho com bancos como o [Nome do Banco do Contato] ajudando a 
[benefício principal, ex: "reduzir custos com consumíveis em até 30%"].

A Corhed é especializada em gestão de meios de pagamento eletrónica 
e venda de consumíveis para instituições bancárias.

Teria 15 minutos esta semana para uma conversa rápida?

Atenciosamente,
[Nome]
Corhed - Comércio e Serviços LDA
[Telefone] | [Email]
```
