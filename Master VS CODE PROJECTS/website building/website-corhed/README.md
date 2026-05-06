# Website Building — Client Projects Repository

Professional website projects and reusable templates. Contains two clients: **Corhed** (real B2B banking client, Portuguese) and **YourBusiness** (English template).

**Live demo:** https://roceliodasilva.github.io/website-building/

---

## Repository Structure

```
website building/
├── corhed/               # Corhed client — landing page (pt-BR)
│   └── index.html        # Best merged version (banking-specific content)
│
├── template/             # Reusable YourBusiness template (English)
│   ├── index.html
│   ├── about.html
│   ├── services.html
│   ├── contact.html
│   ├── faq.html
│   ├── 404.html
│   ├── mobile-landing.html
│   └── legal/
│       ├── privacy-policy.html
│       ├── terms-and-conditions.html
│       └── cookie-policy.html
│
├── assets/               # Shared assets (used by template)
│   ├── css/styles.css
│   ├── js/scripts.js
│   └── img/
│       ├── favicon.svg
│       ├── og-image.svg
│       └── corhed-logo.png
│
├── docs/                 # Merged documentation
│   ├── CORHED-CLIENT.md     # Design specs + interview questions + personalization guide
│   ├── SETUP-GUIDES.md      # Domain, hosting, email, SEO, social media
│   ├── LAUNCH-CHECKLIST.md  # Pre-launch checklists + content templates
│   └── AI-TOOLS.md          # AI website builders + prompts
│
└── [root config files]   # package.json, robots.txt, sitemap.xml, server.ps1, etc.
```

---

## Quick Start

### View locally

**Option 1 — Open file directly:**
Double-click `corhed/index.html` or `template/index.html` in File Explorer.

**Option 2 — Local server (recommended):**
```powershell
# PowerShell server on port 8000
.\server.ps1
```
Then open: http://localhost:8000/corhed/

**Option 3 — npm:**
```bash
npm install
npm start
```

### Deploy to GitHub Pages
```bash
# Push to main (auto-deploys gh-pages if configured)
git add -A
git commit -m "Update"
git push origin main
```

---

## Client: Corhed

**Company:** Corhed - Comércio e Serviços LDA  
**Specialty:** Electronic payment management + banking consumables  
**File:** `corhed/index.html`  
**Live:** https://roceliodasilva.github.io/website-building/

**Brand colors:**
- Primary: `#1F4E79` (navy blue)
- Accent: `#C00000` (dark red)
- Body: `#7A7A7A` (gray)

**To personalize:** See `docs/CORHED-CLIENT.md`

---

## Template: YourBusiness

English B2B template with 7 pages + legal pages. Ready to fork and rebrand for any new client.

**Assets path from template files:** `../assets/` (CSS, JS, images)

**To use for a new client:**
1. Copy `template/` folder and rename
2. Update brand colors in `assets/css/styles.css`
3. Replace all placeholder text and images
4. Follow `docs/LAUNCH-CHECKLIST.md`

---

## Documentation

| File | Contents |
|------|----------|
| `docs/CORHED-CLIENT.md` | Corhed design specs, 30-question client interview, personalization guide, form integration |
| `docs/SETUP-GUIDES.md` | Domain registration, hosting, email (Google Workspace / M365), SEO, social media |
| `docs/LAUNCH-CHECKLIST.md` | 5-phase build checklist, pre-launch QA, content templates, email templates |
| `docs/AI-TOOLS.md` | AI website builders comparison, Lovable prompt, Claude/GPT prompt, free templates |

---

## How to Open on Phone (Client Instructions)

**Option 1 — Direct file (offline):**
Transfer the `corhed/` folder to phone via USB or Google Drive, then open `index.html` in mobile browser.

**Option 2 — GitHub Pages (online, zero setup):**
Share this link: https://roceliodasilva.github.io/website-building/

**Option 3 — Local server on same WiFi:**
```powershell
.\server.ps1
```
Open on phone: `http://[YOUR-PC-IP]:8000/corhed/`

---

## 🚀 Instalação e Execução

### Pré-requisitos

- **Windows**: Node.js (versão 14 ou superior)
- **macOS/Linux**: Node.js (versão 14 ou superior) + NPM ou Yarn

### Instalação Automática

#### Windows
```cmd
setup.bat
```

#### macOS/Linux
```bash
chmod +x setup.sh && ./setup.sh
```

### Instalação Manual

1. **Baixe e instale o Node.js**
   - Acesse: https://nodejs.org/
   - Instale a versão LTS (recomendada)

2. **Instale as dependências**
   ```bash
   npm install
   ```

3. **Adicione o logo da empresa**
   - Coloque o arquivo `corhed-logo.png` na raiz do projeto
   - Ou ajuste o caminho no arquivo `index.html` se necessário

### Execução

#### Desenvolvimento Local
```bash
# Windows
npm run dev

# macOS/Linux
npm run dev
```

#### Preview de Produção
```bash
# Abre automaticamente no navegador na porta 8000
npm run preview
```

#### Servidor Básico
```bash
# Servidor simples na porta 3000
npm start
```

## 📁 Estrutura do Projeto

```
corhed-landing-page/
├── index.html              # Página principal
├── package.json            # Configurações do projeto Node.js
├── README.md              # Este arquivo (instruções completas)
├── .gitignore             # Arquivos ignorados pelo Git
├── config.env             # Configurações personalizáveis
├── setup.sh               # Script de instalação (macOS/Linux)
├── setup.bat              # Script de instalação (Windows)
├── corhed-logo.png        # Logo da empresa (adicionar)
├── Privacy_Policy.html    # Política de privacidade
├── Terms_and_Conditions.html # Termos de uso
├── Cookie_Policy.html     # Política de cookies
├── Corhed_AI_Builder_Prompt.md # Prompt para gerar versão com IA
└── [outros arquivos HTML] # Páginas adicionais
```

## ⚙️ Configuração

### Arquivo `config.env`
Personalize as configurações editando o arquivo `config.env`:

```bash
# Informações da empresa
COMPANY_NAME="Corhed"
COMPANY_EMAIL="contato@corhed.com"

# Cores da marca
PRIMARY_COLOR="#1F4E79"
ACCENT_COLOR="#C00000"

# URLs e integrações
PRODUCTION_URL="https://corhed.com"
FORMSPREE_URL=""  # Adicione sua URL do Formspree
GA_TRACKING_ID="" # Adicione seu ID do Google Analytics
```

### Scripts de Instalação
- **`setup.bat`** (Windows): Instalação automática com verificações
- **`setup.sh`** (macOS/Linux): Instalação automática com verificações
- Ambos verificam Node.js, instalam dependências e validam arquivos

## 🎨 Personalização

### Cores da Marca
- **Azul Primário**: #1F4E79
- **Vermelho Destaque**: #C00000
- **Cinza Secundário**: #7A7A7A
- **Branco**: #FFFFFF
- **Preto**: #000000

### Conteúdo
Edite o arquivo `index.html` para personalizar:
- Textos e títulos
- Informações de contato
- Serviços oferecidos
- Estatísticas e depoimentos

### Logo
Substitua `corhed-logo.png` pelo logo oficial da Corhed.

## 🌐 Deploy

### Opções de Hospedagem

#### 1. Netlify (Recomendado)
```bash
# Instale Netlify CLI
npm install -g netlify-cli

# Faça deploy
netlify deploy --prod --dir=.
```

#### 2. Vercel
```bash
# Instale Vercel CLI
npm install -g vercel

# Faça deploy
vercel --prod
```

#### 3. GitHub Pages
```bash
# Instale gh-pages
npm install -g gh-pages

# Adicione ao package.json:
"scripts": {
  "deploy": "gh-pages -d ."
}

# Execute
npm run deploy
```

#### 4. Hospedagem Tradicional
- Faça upload de todos os arquivos `.html`, `.css`, `.js` e imagens
- Configure o servidor web (Apache/Nginx)
- Certifique-se de que o arquivo `index.html` seja o padrão

## 🔧 Configurações Técnicas

### Formulários
Os formulários atualmente mostram alertas. Para funcionalidade real:

1. **Formspree** (Recomendado)
   - Acesse [formspree.io](https://formspree.io)
   - Crie um formulário
   - Substitua `action="#"` por sua URL do Formspree

2. **EmailJS**
   - Configure conta no EmailJS
   - Adicione script e configure envio

### Analytics
Para adicionar Google Analytics:
1. Obtenha seu código de rastreamento
2. Adicione antes da tag `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 📊 Performance

### Otimizações Implementadas
- ✅ CSS e JavaScript minificados
- ✅ Imagens otimizadas
- ✅ Lazy loading de animações
- ✅ Cache inteligente
- ✅ Mobile-first design

### Testes de Performance
```bash
# Instale Lighthouse
npm install -g lighthouse

# Teste local
lighthouse http://localhost:3000 --output html --output-path ./report.html
```

## 🛠️ Desenvolvimento

### Tecnologias Utilizadas
- **HTML5** - Estrutura semântica
- **CSS3** - Estilos modernos com Grid/Flexbox
- **JavaScript** - Interatividade vanilla
- **Fontes** - Segoe UI (fallback seguro)

### Scripts Disponíveis
```bash
npm run dev      # Desenvolvimento com live reload
npm run start    # Servidor básico
npm run preview  # Preview de produção
npm run build    # Build para produção
```

## 📞 Suporte

Para suporte técnico ou customizações:
- **Email**: contato@corhed.com
- **Telefone**: (11) 3000-0000
- **Website**: https://corhed.com

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Corhed © 2026** - Soluções Profissionais para Instituições Bancárias

#### 3. **services.html**
**What it is:** Detailed services page with pricing table
**Includes:**
- 6 detailed service descriptions
- What's included in each service
- Pricing packets
- Best for each service
- Call-to-action buttons
**Use for:** Helping customers understand offerings

---

#### 4. **faq.html**
**What it is:** Interactive FAQ page
**Includes:**
- 15+ common questions
- Expandable answers
- Categories (general, pricing, getting started)
- Contact CTA
**Use for:** Reducing customer questions via support

---

### Setup & Strategy Guides (Read & Follow)

#### 5. **Complete_Website_Checklist.md**
**What it is:** Master checklist for all 20 phases of website building
**Contains:** 
- All 120+ tasks organized by phase
- Timeline estimates
- Tool recommendations
- Cost estimates
**Use:** Reference while building - check off items as you complete

**Start with:** Phase 1 (Planning) and work through systematically

---

#### 6. **Domain_and_Hosting_Setup.md** 🌐
**What it is:** Step-by-step guide for domain registration and hosting
**Covers:**
- How to choose a domain name
- Where to buy domains (comparison)
- Web hosting selection
- Installation process
- DNS configuration
- Troubleshooting
**Action Items:**
1. Choose domain name
2. Register with Namecheap or GoDaddy
3. Choose hosting (Bluehost, SiteGround, or similar)
4. Point domain to hosting
5. Verify SSL certificate

**Estimated Time:** 2-4 hours

---

#### 7. **Email_Setup_Guide.md** 📧
**What it is:** Professional email configuration guide
**Covers:**
- Google Workspace setup (recommended)
- Alternative email services
- MX records configuration
- Email integration with website
- Email security best practices
**Action Items:**
1. Choose email service (Google Workspace recommended)
2. Set up professional email
3. Configure MX records
4. Test email delivery
5. Integrate with contact form

**Estimated Time:** 2-3 hours

---

#### 8. **SEO_Setup_Guide.md** 🔍
**What it is:** Complete SEO optimization guide
**Covers:**
- Google Search Console setup
- XML sitemap creation
- robots.txt setup
- Keyword research
- Meta tags optimization
- Internal linking strategy
- Analytics setup
**Action Items:**
1. Create XML sitemap
2. Submit to Google Search Console
3. Research target keywords
4. Optimize page titles/descriptions
5. Create quality content

**Estimated Time:** 1-2 weeks ongoing

---

#### 9. **Social_Media_Strategy.md** 📱
**What it is:** Complete social media and marketing strategy
**Covers:**
- Platform selection (LinkedIn, Facebook, etc.)
- Content strategy for each platform
- Email marketing
- Community building
- Analytics and metrics
- Marketing budget
**Action Items:**
1. Create LinkedIn company page
2. Create Facebook business page
3. Set up email marketing
4. Plan content calendar
5. Define success metrics

**Estimated Time:** Ongoing 15-20 hours/month

---

#### 10. **Content_Templates.md** 📝
**What it is:** Ready-to-use templates for content creation
**Includes:**
- Blog post template + example
- Case study template
- Email templates (welcome, follow-up, promotional)
- Newsletter template
- Social media templates
- Content calendar
**Use:** Copy and customize for your business

---

### Legal & Compliance Documents (Customize & Use)

#### 11. **Privacy_Policy.md** 
**What it is:** Comprehensive privacy policy
**Required for:** All websites collecting customer data
**Steps to customize:**
1. Find all [placeholders]
2. Replace with your info
3. Review entire document
4. Consult lawyer (optional)
5. Add to website

**Note:** GDPR and CCPA compliant

---

#### 12. **Terms_and_Conditions.md**
**What it is:** Legal terms for website use
**Required for:** E-commerce, services, any business website
**Steps to customize:**
1. Replace [placeholders] with your info
2. Adjust terms as needed
3. Review for your industry
4. Add to website footer

---

#### 13. **Cookie_Policy.md**
**What it is:** Cookie disclosure and management policy
**Required for:** EU/GDPR compliance (and good practice)
**Steps to customize:**
1. Update cookie list
2. Add services you use
3. Add to website
4. Update cookie banner

---

### Lists & References (For Planning)

#### 14. **website ai list.md**
**What it is:** Filtered list of 7 AI website builders with code export
**Contains:**
- Top AI builders comparison
- Features table
- Best choices by use case
**Use:** If you want to rebuild using AI builder instead of HTML

---

---

## 🚀 Quick Start Guide (First 30 Days)

### Week 1: Setup Foundation
- [ ] Register domain name
- [ ] Set up web hosting account
- [ ] Configure SSL certificate
- [ ] Set up professional email
- [ ] Verify domain is working

**Time: 4-8 hours**

### Week 2: Customize Your Site
- [ ] Update index.html with your business info
- [ ] Customize About page
- [ ] Update Services page with your offerings
- [ ] Add Privacy Policy, Terms, Cookie Policy
- [ ] Set up contact form

**Time: 6-10 hours**

### Week 3: SEO & Analytics
- [ ] Create XML sitemap
- [ ] Submit sitemap to Google Search Console
- [ ] Set up Google Analytics
- [ ] Optimize meta titles and descriptions
- [ ] Create robots.txt

**Time: 4-6 hours**

### Week 4: Launch
- [ ] Final testing
- [ ] Upload website to hosting
- [ ] Test contact form
- [ ] Announce on social media
- [ ] Monitor for any issues

**Time: 4-6 hours**

---

## 📱 How to Customize Your Website

### 1. Update Business Information

Edit `index.html` and locate:
```
YourBusiness → [Your Business Name]
contact@yourbusiness.com → [Your Email]
+1 (555) 123-4567 → [Your Phone]
[Your Business Address] → [Your Address]
```

### 2. Update Service Descriptions

Edit each of these files:
- `index.html` - Service cards
- `services.html` - Detailed service pages
- `about.html` - Company information

### 3. Add Your Colors (Optional)

Current colors:
- Blue: #003366
- Red: #ff0000  
- White: #ffffff

To change, search-and-replace in all HTML files.

### 4. Add Images

Create an `/images/` folder and upload:
- Logo
- Team photos
- Service images
- Background images

Update image paths in HTML files.

---

## 🎯 Implementation Timeline

```
Week 1: Domain, Hosting, Email Setup
         ↓
Week 2: Website Customization
         ↓
Week 3: Content & SEO
         ↓
Week 4: Launch & Marketing
         ↓
Month 2-3: Content Creation & Promotion
          ↓
Month 3-6: Optimization & Growth
```

---

## 💰 Cost Breakdown (First Year)

| Item | Cost | Where |
|------|------|-------|
| Domain | $12 | Namecheap/GoDaddy |
| Hosting | $60/year | Bluehost/SiteGround |
| Email | $84/year | Google Workspace |
| SSL | FREE | Let's Encrypt |
| Design | FREE | Using templates provided |
| **Total** | **~$150** | Budget option |

---

## 📞 Support & Resources

### Questions About Setup?
1. Check the relevant guide (Email_Setup_Guide.md, etc.)
2. Search Google for specific error
3. Check hosting support
4. Ask in business forums

### Need Additional Pages?
Use Content_Templates.md to create:
- Blog pages
- Product pages
- Case studies
- Team member pages

### Want More Content?
See Content_Templates.md for templates for:
- Blog posts
- Email campaigns
- Social media posts
- Newsletters

---

## ✅ Success Indicators (After Launch)

**First Month:**
- Website accessible globally
- Forms working properly
- 100+ organic visitors
- Positive user feedback

**First 3 Months:**
- Appearing in Google search results
- 500+ organic visitors
- First customer inquiries
- Good analytics data

**First 6 Months:**
- 2000+ organic visitors
- Ranking for target keywords
- Customer leads/sales
- Regular content published

**First Year:**
- 5000+ organic visitors
- Strong keyword rankings
- Established authority
- Consistent lead generation

---

## 📊 Key Metrics to Track

Keep these metrics on a spreadsheet:

**Website Metrics:**
- Monthly visitors
- Conversion rate (visitors -> leads)
- Bounce rate
- Pages per session
- Average time on site

**Business Metrics:**
- Leads generated
- Conversion rate (leads -> customers)
- Customer acquisition cost
- Return on investment

**Track with tools:**
- Google Analytics
- Google Search Console
- Custom spreadsheet

---

## 🛠️ Tools You'll Need

### Essential (Free/Cheap)
- Domain registrar: Namecheap, GoDaddy
- Hosting: Bluehost, SiteGround
- Email: Google Workspace ($7/month)
- Analytics: Google Analytics (Free)
- SEO: Google Search Console (Free)

### Highly Recommended
- Email marketing: Mailchimp (Free up to 500)
- Social media: Hootsuite (Free limited)
- Backup: Hosting provider backup

### Optional (More Advanced)
- SEO tools: SEMrush, Ahrefs ($100+/month)
- Email: ActiveCampaign, HubSpot
- Analytics: Better analytics tools

---

## 📚 Learning Resources

### Free Guides
- Google Search Console Guides
- Google Analytics Academy
- HubSpot Blog (marketing)
- Moz SEO Guide (seopgraphy.com)

### Paid Courses
- HubSpot Academy
- Coursera SEO Course
- Udemy Web Design
- LinkedIn Learning

---

## 🎓 File Reading Order

**To get the most value, read in this order:**

1. **This file** (you are here!) - Overview
2. **Complete_Website_Checklist.md** - See all tasks
3. **Domain_and_Hosting_Setup.md** - Start here
4. **Email_Setup_Guide.md** - After hosting
5. **Website_Launch_Checklist.md** - Before launching
6. **SEO_Setup_Guide.md** - Ongoing optimization
7. **Social_Media_Strategy.md** - Marketing plan
8. **Content_Templates.md** - Content creation

---

## ❓ FAQ About This Package

**Q: Can I use these files with my current domain?**
A: Yes! Just upload HTML files to your hosting server.

**Q: Do I need to use the AI website builder instead?**
A: No, these HTML files work great. Use index.html as-is, customize it, or use an AI builder - your choice!

**Q: How often should I update my website?**
A: At minimum monthly (new blog post, social post). Ideally 2-3x per week.

**Q: When will I see customers from my website?**
A: 3-6 months for organic search. Faster if using paid ads.

**Q: Can I hire someone to help?**
A: Yes! Consider hiring for: design (if needed), content writing, social media.

**Q: What's the most important thing to do first?**
A: Get your domain and hosting set up. Everything else builds from there.

---

## 🚀 Next Steps (Right Now)

1. **Read:** Domain_and_Hosting_Setup.md
2. **Do:** Register a domain name
3. **Do:** Set up hosting account
4. **Do:** Customize index.html with your info
5. **Do:** Upload to hosting
6. **Do:** Test everything
7. **Do:** Announce your launch!

---

## 📝 Note About Customization

Every file in this package is a template. You should:

- ✅ Update company name, contact info, emails
- ✅ Customize content examples
- ✅ Replace generic images with yours
- ✅ Adjust colors to match brand
- ✅ Update all [placeholders]
- ✅ Review for accuracy
- ✅ Add your unique value proposition

---

## 🎯 Final Advice

1. **Don't be perfect.** Launch with 70% - you can improve later.
2. **Start simple.** Add features as you grow.
3. **Focus on content.** Good content beats fancy design.
4. **Measure everything.** Use analytics to guide decisions.
5. **Keep improving.** Website building is never "done."
6. **Ask for help.** You don't have to do it alone.

---

## 📞 Your Website is Now Ready!

You have:
- ✅ Professional HTML website
- ✅ All legal documents  
- ✅ Setup guides for everything
- ✅ Marketing & SEO strategy
- ✅ Content templates
- ✅ Launch checklist
- ✅ Ongoing maintenance plan

**What you need to do:**
1. Register domain
2. Set up hosting
3. Customize this website
4. Launch
5. Keep improving

---

## 📞 Contact & Support

**For questions about:**
- Domain setup: See Domain_and_Hosting_Setup.md
- Email issues: See Email_Setup_Guide.md
- SEO help: See SEO_Setup_Guide.md
- Content: See Content_Templates.md
- Marketing: See Social_Media_Strategy.md
- Legal: See Privacy_Policy.md, etc.

**Remember:** You have complete guides for everything!

---

**Last Updated:** March 21, 2026
**Status:** Complete & Ready to Launch 🚀

**Congratulations on taking this step toward your online presence!**

Your website building journey is just beginning. Follow the guides, take action, and watch your business grow!

---

## 📋 Quick Reference Checklist

Copy this to your notes and track your progress:

```
Day 1: Read overview
  ☐ Read all guides quickly to see what's available
  ☐ Understand timeline (30 days to launch)

Week 1: Setup
  ☐ Register domain (1 hour)
  ☐ Get hosting (1 hour)
  ☐ Set up email (2 hours)
  ☐ Enable SSL (1 hour)

Week 2: Customize
  ☐ Edit HTML files (4 hours)
  ☐ Update info (2 hours)
  ☐ Add images (1 hour)

Week 3: SEO & Analytics
  ☐ Create sitemap (1 hour)
  ☐ Submit to Google (1 hour)
  ☐ Set up analytics (1 hour)
  ☐ Configure meta tags (2 hours)

Week 4: Launch
  ☐ Final testing (3 hours)
  ☐ Upload to server (1 hour)
  ☐ Go live!
  ☐ Monitor & announce (2 hours)

Post-Launch (Ongoing)
  ☐ Monitor analytics
  ☐ Create content monthly
  ☐ Update social media
  ☐ Respond to inquiries
```

---

You're all set! Start with Domain_and_Hosting_Setup.md and begin your journey! 🎉
