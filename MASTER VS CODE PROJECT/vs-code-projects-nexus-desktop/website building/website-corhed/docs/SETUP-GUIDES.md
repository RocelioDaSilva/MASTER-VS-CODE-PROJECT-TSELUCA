# Setup Guides — Domain, Hosting, Email & SEO

---

## PARTE 1 — DOMÍNIO & HOSTING

### 1.1 Escolher o Nome de Domínio

**Boas Práticas:**
- Curto (2-3 palavras máximo)
- Fácil de memorizar e soletrar
- Incluir keyword principal se possível
- Evitar hífens e números
- `.com` é o mais confiável — alternativas: `.co`, `.business`, `.io`, `.net`

**Exemplos:**
```
corhed.com          ✓ Ideal
corhed.com.br       ✓ Para Brasil
corhed-solucoes.com ○ Aceitável
corhedservicos.com.br ✓ Alternativa
```

### 1.2 Registradores Recomendados

| Registrador | Vantagem | Link |
|-------------|----------|------|
| **Namecheap** | Melhor custo-benefício + WHOIS grátis | namecheap.com |
| **GoDaddy** | Maior disponibilidade, bundling | godaddy.com |
| **Google Domains** | Simples, suporte excelente | domains.google.com |
| **Registro.br** | Para domínios .br no Brasil | registro.br |

### 1.3 Processo de Registro
1. Buscar o domínio desejado no registrador
2. Criar conta e adicionar ao carrinho
3. Habilitar WHOIS/privacy protection
4. Ativar domain lock (segurança)
5. Verificar email de confirmação

### 1.4 Provedores de Hosting

| Provedor | Tipo | Melhor para |
|----------|------|-------------|
| **Netlify** | Estático / Jamstack | Sites HTML/CSS/JS sem backend |
| **GitHub Pages** | Estático (gratuito) | Sites pequenos / demos |
| **Vercel** | Estático + Edge | Performance máxima |
| **Hostinger** | Shared / VPS | Sites PHP/WordPress budget |
| **Bluehost** | Shared | WordPress + bundle domínio |
| **DigitalOcean** | VPS | Controle total / Node.js |

**Para este projeto (HTML estático):** Netlify ou GitHub Pages são suficientes e gratuitos.

### 1.5 Configurar DNS

Após registrar domínio e contratar hosting:
1. Acesse o painel DNS do registrador
2. Aponte `A record` para o IP do servidor (ou CNAME para providers como Netlify)
3. Aguardar propagação: 15 min a 48 horas
4. Verificar em: [dnschecker.org](https://dnschecker.org)

---

## PARTE 2 — EMAIL PROFISSIONAL

### 2.1 Google Workspace (Recomendado para PMEs)

**Plano Business Starter: ~$7/usuário/mês**

**Passo 1 — Contratar:**
1. Ir a workspace.google.com
2. Clicar "Get started"
3. Inserir domínio (ex: corhed.com)
4. Seguir o assistente de configuração

**Passo 2 — Verificar Domínio:**
1. Admin Console → Domains → Add domain
2. Adicionar registro TXT fornecido pelo Google no DNS do registrador

**Passo 3 — Criar Contas de Email:**
1. Admin Console → Users → Add user
2. Exemplos: `contato@corhed.com`, `suporte@corhed.com`

**Passo 4 — Configurar MX Records (no registrador):**
```
Prioridade 5:  gmail-smtp-in.l.google.com
Prioridade 10: alt1.gmail-smtp-in.l.google.com
Prioridade 20: alt2.gmail-smtp-in.l.google.com
Prioridade 30: alt3.gmail-smtp-in.l.google.com
Prioridade 40: alt4.gmail-smtp-in.l.google.com
```

**Passo 5 — Registros de Segurança de Email:**
```
SPF:  v=spf1 include:_spf.google.com ~all
DKIM: (Gerado no Admin Console → Apps → Google Workspace → Gmail → Authenticate email)
DMARC: v=DMARC1; p=none; rua=mailto:admin@corhed.com
```

### 2.2 Microsoft 365 (Opção Avançada)

**Plano Business Basic: ~$6/usuário/mês**

1. Ir a microsoft365.com/business
2. Escolher plano e inserir domínio
3. Verificar domínio via TXT record
4. Configurar MX records no registrador
5. Criar caixas de email no Admin Center

### 2.3 Email no Formulário do Website

Para o formulário de contato funcionar, usar um destes:

**Opção A — Formspree (gratuito até 50 submissões/mês):**
```html
<form method="POST" action="https://formspree.io/f/SEU_ID">
```

**Opção B — EmailJS (gratuito até 200 emails/mês):**
```javascript
emailjs.send('service_id', 'template_id', formData);
```

**Opção C — Backend PHP:**
```html
<form method="POST" action="send-email.php">
```

---

## PARTE 3 — SEO (Search Engine Optimization)

### 3.1 Os 3 Pilares do SEO

| Pilar | O que é | Como implementar |
|-------|---------|-----------------|
| **SEO Técnico** | Estrutura, velocidade, mobile | Sitemap, robots.txt, meta tags |
| **SEO On-Page** | Conteúdo e keywords | Títulos H1-H6, meta description |
| **SEO Off-Page** | Autoridade externa | Backlinks, Google Business |

### 3.2 Google Search Console

**Setup:**
1. Ir a [search.google.com/search-console](https://search.google.com/search-console)
2. Adicionar propriedade → Domain property
3. Verificar via DNS TXT record (recomendado) ou meta tag HTML
4. Submeter sitemap: `https://seusite.com/sitemap.xml`

**Tarefas Importantes:**
- Monitorar erros de rastreamento
- Verificar usabilidade em dispositivos móveis
- Analisar consultas de pesquisa
- Verificar problemas de segurança
- Checar velocidade de página (Core Web Vitals)

### 3.3 Bing Webmaster Tools

1. Ir a [bing.com/webmasters](https://bing.com/webmasters)
2. Adicionar site e verificar propriedade
3. Submeter sitemap
4. Monitorar performance

### 3.4 Google Business Profile (Para Negócios Locais)

1. Ir a [business.google.com](https://business.google.com)
2. Adicionar/reivindicar negócio
3. Verificar endereço (carta com código ou vídeo)
4. Completar: fotos, horários, descrição, serviços
5. Responder avaliações regularmente

### 3.5 Sitemap XML

O arquivo `sitemap.xml` já está criado na raiz do projeto.  
**Atualizar as URLs** substituindo `https://yourbusiness.com/` pelo domínio real.

Depois de publicar: submeter em Google Search Console e Bing Webmaster.

### 3.6 On-Page SEO — Checklist Rápido

- [ ] `<title>` único por página (50-60 caracteres)
- [ ] `<meta name="description">` único (150-160 caracteres)
- [ ] Um único `<h1>` por página com keyword principal
- [ ] H2/H3 com variações da keyword
- [ ] Alt text em todas as imagens
- [ ] URLs amigáveis (sem espaços, minúsculas)
- [ ] Links internos entre páginas
- [ ] robots.txt configurado (já existe na raiz)
- [ ] HTTPS ativo no servidor

### 3.7 Ferramentas SEO Gratuitas

| Ferramenta | Uso |
|-----------|-----|
| Google Search Console | Monitorar indexação e performance |
| Google Analytics | Análise de tráfego |
| Bing Webmaster Tools | Índice Bing |
| GTmetrix | Velocidade da página |
| Lighthouse (DevTools) | Auditoria geral (SEO, performance, acessibilidade) |
| Screaming Frog (Free tier) | Rastrear erros on-page |

---

## PARTE 4 — SOCIAL MEDIA STRATEGY

### 4.1 Plataformas Recomendadas para Corhed (B2B Bancário)

| Plataforma | Prioridade | Tipo de Conteúdo |
|------------|-----------|-----------------|
| **LinkedIn** | 🔴 Alta | Artigos técnicos, cases, atualizações de mercado |
| **Facebook** | 🟡 Média | Anúncios locais, eventos, conteúdo de awareness |
| **Instagram** | 🟡 Média | Visual: infográficos, bastidores, conquistas |
| **YouTube** | 🟢 Baixa | Tutoriais, demos de produto, webinars |

### 4.2 Calendário de Conteúdo Sugerido

**LinkedIn (3-4x por semana):**
- Segunda: Artigo de educação/mercado bancário
- Quarta: Case de sucesso ou dado relevante
- Sexta: Conteúdo humanizado (time, bastidores)

**Tipos de Post Eficazes para B2B:**
- "5 erros em gestão de terminais POS que custam dinheiro ao banco"
- "O que muda com a nova regulamentação PCI DSS 4.0"
- "Case: como o Banco X reduziu 30% dos custos com consumíveis"

### 4.3 Métricas a Monitorar

| Métrica | Meta Inicial | Ferramenta |
|---------|-------------|-----------|
| Seguidores LinkedIn | +50/mês | LinkedIn Analytics |
| Alcance orgânico | Crescimento 10%/mês | Plataforma nativa |
| Taxa de engajamento | >3% | Sprout Social / Nativo |
| Leads via social | 5-10/mês | CRM + UTM links |
