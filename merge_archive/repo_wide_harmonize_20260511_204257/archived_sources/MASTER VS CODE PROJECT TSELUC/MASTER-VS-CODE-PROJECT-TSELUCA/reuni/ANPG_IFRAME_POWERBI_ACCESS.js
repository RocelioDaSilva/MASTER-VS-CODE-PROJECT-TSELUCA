const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

class ANPGIframeExtractor {
  constructor() {
    this.browser = null;
    this.page = null;
    this.companies = new Set();
    this.logs = [];
    this.startTime = new Date();
  }

  log(message) {
    const timestamp = new Date().toLocaleTimeString('pt-BR');
    const logMsg = `[${timestamp}] ${message}`;
    console.log(logMsg);
    this.logs.push(logMsg);
  }

  async initialize() {
    this.log('🚀 Iniciando navegador...');
    this.browser = await puppeteer.launch({
      headless: false,
      defaultViewport: null,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-blink-features=AutomationControlled',
        '--disable-web-resources',
      ]
    });
    this.log('✅ Navegador pronto');
  }

  async loadPage() {
    this.log('📍 Abrindo página ANPG...');
    this.page = await this.browser.newPage();
    
    // Desabilitar logs de console
    this.page.on('console', () => {});
    this.page.on('error', (err) => this.log(`❌ Erro na página: ${err.message}`));
    
    try {
      await this.page.goto('https://anpg.co.ao/conteudo-local/', { 
        waitUntil: 'networkidle2',
        timeout: 60000 
      });
      this.log('✅ Página carregada');
      return true;
    } catch (err) {
      this.log(`⚠️ Timeout ao carregar página: ${err.message}`);
      return false;
    }
  }

  async waitForPowerBI() {
    this.log('⏳ Aguardando Power BI carregar...');
    
    try {
      // Esperar o iframe do Power BI
      await this.page.waitForSelector('iframe', { timeout: 30000 });
      this.log('✅ iframe detectado');

      // Esperar conteúdo
      await this.page.waitForFunction(() => {
        return document.body.innerText.length > 500;
      }, { timeout: 30000 });
      
      this.log('✅ Conteúdo carregado');
      await this.page.waitForTimeout(5000); // Buffer
      return true;
    } catch (err) {
      this.log(`⚠️ Timeout ao esperar Power BI: ${err.message}`);
      return false;
    }
  }

  async accessIframeContent() {
    this.log('🔍 Acessando conteúdo do iframe...');

    try {
      // Método 1: Acessar frames diretos
      const frames = await this.page.frames();
      this.log(`📊 Total de frames encontrados: ${frames.length}`);

      for (let i = 0; i < frames.length; i++) {
        try {
          const frameContent = await frames[i].evaluate(() => document.body.innerText);
          if (frameContent && frameContent.length > 100) {
            this.log(`✅ Frame ${i} tem conteúdo (${frameContent.length} chars)`);
            
            // Extrair texto do frame
            const items = frameContent.split('\n').filter(line => line.trim().length > 2);
            for (const item of items) {
              if (item.match(/^[A-Z]/)) {
                this.companies.add(item.trim());
              }
            }
          }
        } catch (e) {
          // Frame pode estar restringido por segurança
        }
      }

      this.log(`📦 Empresas extraídas do iframe: ${this.companies.size}`);
      return this.companies.size > 0;
    } catch (err) {
      this.log(`❌ Erro ao acessar iframe: ${err.message}`);
      return false;
    }
  }

  async extractFromPageDirect() {
    this.log('🔄 Tentando extração direta da página...');

    try {
      const extracted = await this.page.evaluate(() => {
        const companies = new Set();

        // Estratégia 1: Procurar elementos de texto no corpo
        const allText = document.body.innerText;
        const lines = allText.split('\n');
        
        for (const line of lines) {
          const cleaned = line.trim();
          // Procurar por linhas que parecem ser nomes de empresas
          if (cleaned.length > 5 && cleaned.length < 100 && 
              !cleaned.match(/^\d+$/) &&
              !cleaned.match(/^(ANPG|Power|BI|Certificada|Loading|Expand|Categories)$/i)) {
            companies.add(cleaned);
          }
        }

        // Estratégia 2: Procurar em elementos específicos
        const treeItems = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem, .pvExplorerItem');
        treeItems.forEach(item => {
          const text = item.innerText || item.textContent;
          if (text && text.trim().length > 0) {
            companies.add(text.trim());
          }
        });

        // Estratégia 3: Botões, spans, divs
        const elements = document.querySelectorAll('button span, div[aria-label], a[title]');
        elements.forEach(el => {
          const text = (el.getAttribute('aria-label') || el.getAttribute('title') || el.textContent).trim();
          if (text && text.length > 3 && text.length < 100) {
            companies.add(text);
          }
        });

        return Array.from(companies);
      });

      for (const company of extracted) {
        this.companies.add(company);
      }
      
      this.log(`✅ Extração direta: ${extracted.length} empresas capturadas`);
      return true;
    } catch (err) {
      this.log(`❌ Erro na extração direta: ${err.message}`);
      return false;
    }
  }

  async expandAllCategories() {
    this.log('📂 Expandindo categorias...');

    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        const expanded = await this.page.evaluate(() => {
          let count = 0;

          // Encontrar botões colapsados
          const expandButtons = document.querySelectorAll(
            '[aria-expanded="false"], button[aria-label*="Expand"], .pvExplorerTreeItemIconContainer'
          );

          for (const button of expandButtons) {
            button.click();
            count++;
          }

          return count;
        });

        this.log(`✅ Tentativa ${attempt}: ${expanded} elementos expandidos`);
        
        if (expanded > 0) {
          await this.page.waitForTimeout(3000); // Aguardar renderização
          // Extrair após expansão
          await this.extractFromPageDirect();
        }
      } catch (err) {
        this.log(`⚠️ Erro ao expandir (tentativa ${attempt}): ${err.message}`);
      }
    }
  }

  async performRightClicks() {
    this.log('🖱️ Executando right-clicks...');

    try {
      const rightClickCount = await this.page.evaluate(() => {
        const items = document.querySelectorAll(
          '[role="treeitem"], .pvExplorerTreeItem, [aria-expanded], button'
        );
        
        let count = 0;
        for (let i = 0; i < Math.min(items.length, 100); i++) {
          const item = items[i];
          if (item.offsetHeight > 0) { // Elemento visível
            const event = new MouseEvent('contextmenu', {
              bubbles: true,
              cancelable: true,
              button: 2
            });
            item.dispatchEvent(event);
            count++;
          }
        }
        return count;
      });

      this.log(`✅ ${rightClickCount} right-clicks executados`);
      await this.page.waitForTimeout(2000);
      
      // Extrair dados após right-clicks
      await this.extractFromPageDirect();
      return true;
    } catch (err) {
      this.log(`❌ Erro ao executar right-clicks: ${err.message}`);
      return false;
    }
  }

  async cleanAndFilterCompanies() {
    this.log('🧹 Limpando e filtrando dados...');

    // Remover items inválidos
    const filtered = new Set();
    const blacklist = [
      'ANPG', 'Power BI', 'Loading', 'Expand', 'Categories', 'Collapse',
      'Filter', 'Sort', 'Export', 'Home', 'Page', 'Next', 'Previous',
      'Back', 'Menu', 'Help', 'Settings', 'Close', 'Open', 'Save',
      'Cancel', 'OK', 'Search', 'Find', 'View', 'Edit', 'Delete'
    ];

    for (const company of this.companies) {
      const text = company.trim();
      
      // Filtrar vazio, muito curto, ou muito longo
      if (text.length < 3 || text.length > 120) continue;
      
      // Filtrar número puro
      if (/^\d+$/.test(text)) continue;
      
      // Filtrar blacklist
      if (blacklist.some(word => text.includes(word))) continue;
      
      // Deve ter pelo menos uma letra
      if (!/[A-Za-z]/i.test(text)) continue;

      filtered.add(text);
    }

    this.companies = filtered;
    this.log(`✅ Filtrado para ${this.companies.size} empresas únicas`);
  }

  async saveResults() {
    this.log('💾 Salvando resultados...');

    const timestamp = new Date().toISOString().split('T')[0];
    const time = new Date().toLocaleTimeString('pt-BR').replace(/:/g, '-');
    const count = this.companies.size;

    // CSV
    const csvFilename = `ANPG_IFRAME_EXTRACTED_${timestamp}_${count}.csv`;
    let csvContent = 'numero;empresa;data;hora;fonte\n';
    
    let numero = 1;
    for (const company of this.companies) {
      const hora = new Date().toLocaleTimeString('pt-BR');
      const data = new Date().toLocaleDateString('pt-BR');
      csvContent += `${numero};${company};${data};${hora};ANPG_IFRAME\n`;
      numero++;
    }

    fs.writeFileSync(csvFilename, csvContent, 'utf-8');
    this.log(`✅ CSV salvo: ${csvFilename}`);

    // JSON
    const jsonFilename = `ANPG_IFRAME_EXTRACTED_${timestamp}_${count}.json`;
    const jsonData = {
      metadata: {
        timestamp: new Date().toISOString(),
        company_count: count,
        extraction_method: 'ANPG_IFRAME',
        url: 'https://anpg.co.ao/conteudo-local/'
      },
      companies: Array.from(this.companies),
      execution_log: this.logs
    };

    fs.writeFileSync(jsonFilename, JSON.stringify(jsonData, null, 2), 'utf-8');
    this.log(`✅ JSON salvo: ${jsonFilename}`);

    // LOG
    const logFilename = `ANPG_IFRAME_EXECUCAO_${timestamp}_${count}.txt`;
    fs.writeFileSync(logFilename, this.logs.join('\n'), 'utf-8');
    this.log(`✅ LOG salvo: ${logFilename}`);
  }

  async cleanup() {
    this.log('🧹 Encerrando...');
    if (this.browser) {
      await this.browser.close();
      this.log('✅ Navegador encerrado');
    }
  }

  async run() {
    try {
      this.log('═══════════════════════════════════════════════════════');
      this.log('🎯 ANPG - EXTRAÇÃO DENTRO DO IFRAME DO POWER BI');
      this.log('═══════════════════════════════════════════════════════');
      this.log('');

      await this.initialize();
      
      const pageLoaded = await this.loadPage();
      if (!pageLoaded) {
        this.log('⚠️ Página não carregou completamente, continuando...');
      }

      const pbLoaded = await this.waitForPowerBI();
      if (!pbLoaded) {
        this.log('⚠️ Power BI não carregou, tentando extração direta...');
      }

      // Tentar acessar iframe
      await this.accessIframeContent();

      // Extração direta
      await this.extractFromPageDirect();

      // Expandir
      await this.expandAllCategories();

      // Right-clicks
      await this.performRightClicks();

      // Extração final
      await this.extractFromPageDirect();

      // Limpar e filtrar
      await this.cleanAndFilterCompanies();

      // Salvar
      await this.saveResults();

      this.log('');
      this.log('═══════════════════════════════════════════════════════');
      this.log(`✅ SUCESSO! ${this.companies.size} empresas extraídas`);
      this.log('═══════════════════════════════════════════════════════');

    } catch (err) {
      this.log(`❌ ERRO CRÍTICO: ${err.message}`);
      this.log(err.stack);
    } finally {
      await this.cleanup();
    }
  }
}

// Executar
const extractor = new ANPGIframeExtractor();
extractor.run();
