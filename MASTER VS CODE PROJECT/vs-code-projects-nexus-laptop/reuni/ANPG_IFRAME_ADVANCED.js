const puppeteer = require('puppeteer');
const fs = require('fs');

class ANPGPowerBIMiner {
  constructor() {
    this.browser = null;
    this.page = null;
    this.companies = new Set();
    this.logs = [];
  }

  log(msg) {
    const t = new Date().toLocaleTimeString('pt-BR');
    const line = `[${t}] ${msg}`;
    console.log(line);
    this.logs.push(line);
  }

  async init() {
    this.log('🚀 Iniciando navegador...');
    this.browser = await puppeteer.launch({
      headless: false,
      defaultViewport: null,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    this.log('✅ Navegador pronto');
  }

  async openPage() {
    this.log('📍 Abrindo ANPG...');
    this.page = await this.browser.newPage();
    this.page.on('error', (e) => this.log(`❌ Erro: ${e.message}`));
    
    try {
      await this.page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'networkidle2',
        timeout: 60000
      });
      this.log('✅ Página aberta');
    } catch (e) {
      this.log(`⚠️ Timeout na navegação (continuando): ${e.message}`);
    }
  }

  async waitPowerBI() {
    this.log('⏳ Aguardando Power BI (90 segundos)...');

    for (let i = 0; i < 30; i++) {
      try {
        const ready = await this.page.evaluate(() => {
          // Procurar indicadores de Power BI carregado
          const hasIframe = document.querySelector('iframe') !== null;
          const hasExplorer = document.body.innerText.includes('Certificadas') || 
                              document.body.innerText.includes('Explorer') ||
                              document.querySelectorAll('[role="treeitem"]').length > 0;
          
          return hasIframe && hasExplorer;
        });

        if (ready) {
          this.log('✅ Power BI carregado!');
          await this.page.waitForTimeout(5000); // Buffer final
          return true;
        }

        this.log(`⏳ Tentativa ${i + 1}/30 - Aguardando...`);
        await this.page.waitForTimeout(3000);
      } catch (e) {
        this.log(`⚠️ Erro na verificação: ${e.message}`);
      }
    }

    this.log('⚠️ Power BI não carregou completamente, continuando mesmo assim...');
    return false;
  }

  async takeScreenshots() {
    this.log('📸 Capturando screenshots...');
    try {
      await this.page.screenshot({ path: 'iframe_page_full.png', fullPage: true });
      this.log('✅ Screenshot da página salvo');
    } catch (e) {
      this.log(`⚠️ Erro ao capturar: ${e.message}`);
    }
  }

  async expandTree() {
    this.log('📂 Expandindo tree explorer...');

    for (let attempt = 1; attempt <= 5; attempt++) {
      try {
        const count = await this.page.evaluate(() => {
          let expanded = 0;

          // Estratégia 1: aria-expanded
          const buttons = document.querySelectorAll('[aria-expanded="false"]');
          for (const btn of buttons) {
            if (btn.offsetHeight > 0) {
              btn.click();
              expanded++;
            }
          }

          // Estratégia 2: Classes Power BI
          const pbiButtons = document.querySelectorAll('.pvExplorerTreeItemIconContainer, .explorerItemIcon');
          for (const btn of pbiButtons) {
            if (btn.offsetHeight > 0) {
              btn.click();
              expanded++;
            }
          }

          // Estratégia 3: Chevrons, setas
          const chevrons = document.querySelectorAll('button[aria-label*="xpand"], button svg');
          for (const btn of chevrons) {
            if (btn.offsetHeight > 0) {
              btn.click();
              expanded++;
            }
          }

          return expanded;
        });

        this.log(`✅ Tentativa ${attempt}: ${count} elementos expandidos`);
        await this.page.waitForTimeout(2000);

      } catch (e) {
        this.log(`⚠️ Erro na expansão: ${e.message}`);
      }
    }
  }

  async extractCompanies() {
    this.log('🔍 Extraindo empresas...');

    try {
      const companies = await this.page.evaluate(() => {
        const found = new Set();

        // Estratégia 1: Tree items
        const treeItems = document.querySelectorAll('[role="treeitem"]');
        for (const item of treeItems) {
          const text = item.innerText || item.textContent;
          if (text) found.add(text.trim());
        }

        // Estratégia 2: Power BI specific
        const pbiItems = document.querySelectorAll('.pvExplorerTreeItem, .explorerItem, [class*="explorer"]');
        for (const item of pbiItems) {
          const text = item.innerText || item.textContent;
          if (text && text.length > 2) {
            // Pegar apenas primeira linha se multi-linha
            const firstLine = text.split('\n')[0].trim();
            if (firstLine.length > 2) found.add(firstLine);
          }
        }

        // Estratégia 3: Spans e elementos de texto
        const spans = document.querySelectorAll('[class*="item"] span, [class*="company"] span, [class*="name"] span');
        for (const span of spans) {
          const text = span.innerText || span.textContent;
          if (text && text.length > 3 && text.length < 100) {
            found.add(text.trim());
          }
        }

        // Estratégia 4: Todo o texto (com filtro)
        const bodyText = document.body.innerText;
        const lines = bodyText.split('\n').filter(l => l.trim().length > 3 && l.trim().length < 100);
        for (const line of lines) {
          const cleaned = line.trim();
          // Apenas linhas que parecem ser empresas
          if (/^[A-Z]/.test(cleaned) && !cleaned.match(/^(Skip|Sobre|Oport|Dados|Media|Produ|Conté|Procu|DECR|REGIS|VER |Intro|Regim|Ciclo|Lista|Instr|Manu|Regis|Empre|Visita|Certif|Noss|Respo|Contac|Licit|Oferta|Confer)/)) {
            found.add(cleaned);
          }
        }

        return Array.from(found);
      });

      for (const company of companies) {
        this.companies.add(company);
      }

      this.log(`✅ ${companies.length} items extraídos (${this.companies.size} únicos no total)`);

    } catch (e) {
      this.log(`❌ Erro na extração: ${e.message}`);
    }
  }

  async filterAndClean() {
    this.log('🧹 Filtrando dados...');

    const ui = ['Skip', 'Sobre', 'Oportunidades', 'Dados', 'Media', 'Produção', 'Conteúdo', 'Procurar',
               'DECRETO', 'REGISTO', 'VER', 'Introdução', 'Regimes', 'Ciclo', 'Lista', 'Instrutivo',
               'Manual', 'Registo', 'Empresas', 'Visitadas', 'Certificadas', 'História', 'Responsabilidade',
               'Contactos', 'Licitações', 'Oferta', 'Conferência', 'Power', 'BI', 'Loading', 'Expand'];

    const filtered = new Set();
    for (const company of this.companies) {
      const c = company.trim();
      
      // Validações
      if (c.length < 3 || c.length > 100) continue;
      if (/^\d+$/.test(c)) continue;
      if (!/[A-Za-z]/i.test(c)) continue;
      if (ui.some(word => c.includes(word))) continue;

      filtered.add(c);
    }

    this.companies = filtered;
    this.log(`✅ Filtrado para ${this.companies.size} empresas`);
  }

  async save() {
    this.log('💾 Salvando...');

    const date = new Date().toISOString().split('T')[0];
    const count = this.companies.size;

    // CSV
    const csv = `ANPG_IFRAME_FINAL_${date}_${count}.csv`;
    let csvContent = 'numero;empresa;data;hora;fonte\n';
    let num = 1;
    for (const company of this.companies) {
      const hora = new Date().toLocaleTimeString('pt-BR');
      const data = new Date().toLocaleDateString('pt-BR');
      csvContent += `${num};${company};${data};${hora};ANPG_IFRAME_ADVANCED\n`;
      num++;
    }
    fs.writeFileSync(csv, csvContent, 'utf-8');
    this.log(`✅ CSV: ${csv}`);

    // JSON
    const json = `ANPG_IFRAME_FINAL_${date}_${count}.json`;
    fs.writeFileSync(json, JSON.stringify({
      count,
      companies: Array.from(this.companies),
      logs: this.logs,
      timestamp: new Date().toISOString()
    }, null, 2), 'utf-8');
    this.log(`✅ JSON: ${json}`);
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
      this.log('✅ Encerrado');
    }
  }

  async run() {
    try {
      this.log('');
      this.log('═════════════════════════════════════════════');
      this.log('🎯 ANPG IFRAME POWER BI - EXTRAÇÃO AVANÇADA');
      this.log('═════════════════════════════════════════════');
      this.log('');

      await this.init();
      await this.openPage();
      await this.waitPowerBI();
      await this.takeScreenshots();
      await this.expandTree();
      await this.extractCompanies();
      await this.filterAndClean();
      await this.save();

      this.log('');
      this.log('═════════════════════════════════════════════');
      this.log(`✅ SUCESSO! ${this.companies.size} empresas extraídas`);
      this.log('═════════════════════════════════════════════');
      this.log('');

    } catch (e) {
      this.log(`❌ CRÍTICO: ${e.message}`);
      this.log(e.stack);
    } finally {
      await this.close();
    }
  }
}

new ANPGPowerBIMiner().run();
