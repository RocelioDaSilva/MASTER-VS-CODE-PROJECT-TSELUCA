const puppeteer = require('puppeteer');
const fs = require('fs');

class ANPGIframeExtractor {
  constructor() {
    this.companies = new Set();
    this.log = [];
    this.browser = null;
    this.page = null;
    this.iframeFrame = null;
  }

  logMessage(message) {
    const timestamp = new Date().toLocaleTimeString();
    const fullMsg = `[${timestamp}] ${message}`;
    console.log(fullMsg);
    this.log.push(fullMsg);
  }

  async initialize() {
    this.logMessage('');
    this.logMessage('═══════════════════════════════════════════════════════');
    this.logMessage('🎯 ANPG - EXTRAÇÃO DENTRO DO IFRAME (Power BI)');
    this.logMessage('═══════════════════════════════════════════════════════');
    this.logMessage('');

    this.logMessage('[1/6] 🚀 Iniciando navegador...');
    this.browser = await puppeteer.launch({
      headless: false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--disable-web-security',
        '--disable-dev-shm-usage',
        '--disable-blink-features=AutomationControlled'
      ]
    });

    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1920, height: 1080 });
    
    // Mask automation
    await this.page.evaluateOnNewDocument(() => {
      Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
      });
    });

    this.logMessage('✅ Navegador pronto');
  }

  async loadPage() {
    this.logMessage('[2/6] 📍 Abrindo https://anpg.co.ao/conteudo-local/...');

    try {
      const response = await this.page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'networkidle2',
        timeout: 60000
      });

      this.logMessage(`✅ Página carregada (Status: ${response.status()})`);
      return true;
    } catch (error) {
      this.logMessage(`⚠️  Timeout na navegação: ${error.message}`);
      this.logMessage('   Continuando mesmo assim...');
      await new Promise(r => setTimeout(r, 5000));
      return false;
    }
  }

  async findAndEnterIframe() {
    this.logMessage('[3/6] 🔍 Procurando iframe do Power BI...');

    try {
      // Wait for iframe to appear
      await this.page.waitForSelector('iframe', { timeout: 30000 });
      this.logMessage('✅ Iframe detectado');

      // Get all iframes
      const frames = await this.page.frames();
      this.logMessage(`   Total de frames na página: ${frames.length}`);

      // List all iframes
      for (let i = 0; i < frames.length; i++) {
        const url = frames[i].url();
        this.logMessage(`   Frame ${i}: ${url}`);
      }

      // Find Power BI iframe (usually contains 'powerbi' or 'app.powerbi')
      let iframeFrame = null;
      
      for (const frame of frames) {
        const url = frame.url();
        if (url.includes('powerbi') || url.includes('app.bi.') || url.length > 50) {
          iframeFrame = frame;
          this.logMessage(`✅ Frame do Power BI encontrado: ${url.substring(0, 100)}`);
          break;
        }
      }

      // If not found by URL, try the last iframe (usually Power BI is the last one)
      if (!iframeFrame && frames.length > 1) {
        iframeFrame = frames[frames.length - 1];
        this.logMessage(`✅ Usando último frame como Power BI: ${iframeFrame.url().substring(0, 100)}`);
      }

      if (iframeFrame) {
        this.iframeFrame = iframeFrame;

        // Verify content in iframe
        const contentLength = await iframeFrame.evaluate(() => {
          return document.body.innerText.length;
        });

        this.logMessage(`✅ Conteúdo do iframe: ${contentLength} caracteres`);
        return true;
      } else {
        this.logMessage('⚠️  Nenhum iframe encontrado!');
        return false;
      }

    } catch (error) {
      this.logMessage(`❌ Erro ao procurar iframe: ${error.message}`);
      return false;
    }
  }

  async waitForIframeContent() {
    this.logMessage('[4/6] ⏳ Aguardando conteúdo dentro do iframe...');

    if (!this.iframeFrame) {
      this.logMessage('❌ Nenhum iframe para esperar');
      return false;
    }

    try {
      await this.iframeFrame.waitForFunction(() => {
        const treeItems = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem');
        return treeItems.length > 0 && document.body.innerText.length > 500;
      }, { timeout: 30000 });

      this.logMessage('✅ Conteúdo do Power BI detectado');

      // Wait for more rendering
      this.logMessage('   Aguardando 5 segundos para renderização completa...');
      await new Promise(r => setTimeout(r, 5000));

      return true;
    } catch (error) {
      this.logMessage(`⚠️  Timeout na espera do conteúdo: ${error.message}`);
      return false;
    }
  }

  async expandAllCategoriesInIframe() {
    this.logMessage('[5/6] 🔄 Expandindo categorias NO IFRAME...');

    if (!this.iframeFrame) {
      this.logMessage('❌ Nenhum iframe para expandir');
      return 0;
    }

    let totalExpanded = 0;

    for (let attempt = 1; attempt <= 3; attempt++) {
      this.logMessage(`   Tentativa ${attempt}/3...`);

      try {
        const expanded = await this.iframeFrame.evaluate(() => {
          let count = 0;

          // Strategy 1: Click aria-expanded="false"
          const collapsed = document.querySelectorAll('[aria-expanded="false"]');
          collapsed.forEach(el => {
            try {
              el.click();
              count++;
            } catch (e) {}
          });

          // Strategy 2: Click expander icons
          const expanders = document.querySelectorAll('.pvExplorerTreeItemIconContainer, [class*="expander"]');
          expanders.forEach(el => {
            try {
              const parent = el.closest('[aria-expanded="false"]');
              if (parent) {
                parent.click();
                count++;
              }
            } catch (e) {}
          });

          return count;
        });

        totalExpanded += expanded;
        this.logMessage(`   ✓ ${expanded} clicks executados`);

        // Wait for DOM to settle
        await new Promise(r => setTimeout(r, 3000));

        // Check if more items exist
        const hasMore = await this.iframeFrame.evaluate(() => {
          return document.querySelectorAll('[aria-expanded="false"]').length;
        });

        this.logMessage(`   • Itens ainda colapsados: ${hasMore}`);

        if (hasMore === 0) {
          this.logMessage('✅ Todas as categorias expandidas!');
          break;
        }
      } catch (error) {
        this.logMessage(`   ⚠️  Erro na expansão: ${error.message}`);
      }
    }

    this.logMessage(`✅ Expansão concluída (${totalExpanded} clicks total)`);
    return totalExpanded;
  }

  async extractCompaniesFromIframe() {
    this.logMessage('[5.5/6] 📥 Extraindo nomes do IFRAME...');

    if (!this.iframeFrame) {
      this.logMessage('❌ Nenhum iframe para extrair');
      return [];
    }

    try {
      const data = await this.iframeFrame.evaluate(() => {
        const items = [];
        const seen = new Set();

        // Get all tree items from Power BI
        const selectors = [
          '[role="treeitem"]',
          '.pvExplorerTreeItem',
          '[class*="treeItem"]',
          'span[role="treeitem"]'
        ];

        selectors.forEach(selector => {
          const elements = document.querySelectorAll(selector);
          
          elements.forEach((el) => {
            let text = el.innerText?.trim() || el.textContent?.trim() || el.getAttribute('aria-label');

            if (text) {
              text = text.trim();

              // Clean up text
              text = text.replace(/[\n\r\t]+/g, ' ').replace(/\s+/g, ' ').trim();

              if (text && 
                  text.length > 3 && 
                  text.length < 300 &&
                  !seen.has(text)) {

                const lower = text.toLowerCase();

                // Filter out UI elements
                const isUIElement = 
                  lower.includes('anpg') ||
                  lower.includes('sobre') ||
                  lower.includes('procurar') ||
                  lower.includes('close') ||
                  lower.includes('menu') ||
                  lower.includes('fechar') ||
                  lower.includes('decreto') ||
                  lower.includes('lei') ||
                  lower.includes('loading') ||
                  lower.includes('filters') ||
                  lower.includes('página') ||
                  lower.includes('page') ||
                  lower === '+' ||
                  lower === '-' ||
                  lower === '...' ||
                  /^\d+$/.test(lower) ||
                  lower.length < 3;

                if (!isUIElement && text.length > 5) {
                  seen.add(text);
                  items.push({
                    text: text,
                    selector: selector,
                    length: text.length
                  });
                }
              }
            }
          });
        });

        return items;
      });

      this.logMessage(`✅ ${data.length} itens extraídos do iframe`);

      // Store unique
      data.forEach(item => {
        this.companies.add(item.text);
      });

      return Array.from(this.companies);

    } catch (error) {
      this.logMessage(`❌ Erro na extração: ${error.message}`);
      return [];
    }
  }

  async performRightClicksInIframe() {
    this.logMessage('[5.2/6] 👆 Right-clicks DENTRO do iframe...');

    if (!this.iframeFrame) {
      this.logMessage('❌ Nenhum iframe para right-click');
      return 0;
    }

    try {
      const count = await this.iframeFrame.evaluate(() => {
        let clicked = 0;

        const items = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem');
        
        for (let i = 0; i < Math.min(items.length, 100); i++) {
          try {
            const event = new MouseEvent('contextmenu', {
              bubbles: true,
              cancelable: true,
              button: 2,
              buttons: 2
            });
            items[i].dispatchEvent(event);
            clicked++;
          } catch (e) {}
        }

        return clicked;
      });

      this.logMessage(`✅ ${count} right-clicks executados`);
      await new Promise(r => setTimeout(r, 2000));

      return count;

    } catch (error) {
      this.logMessage(`⚠️  Erro no right-click: ${error.message}`);
      return 0;
    }
  }

  async scrollIframeToBottom() {
    this.logMessage('[5.3/6] 📜 Scrollando para carregar mais itens...');

    if (!this.iframeFrame) return;

    try {
      for (let i = 0; i < 5; i++) {
        await this.iframeFrame.evaluate(() => {
          // Scroll to bottom within iframe
          const container = document.querySelector('.pvExplorerTree, [class*="explorer"]') || 
                          document.querySelector('[role="tree"]') || 
                          document.body;
          container.scrollTop = container.scrollHeight;
        });

        await new Promise(r => setTimeout(r, 1000));
      }

      this.logMessage('✅ Scroll concluído');
    } catch (error) {
      this.logMessage(`⚠️  Erro no scroll: ${error.message}`);
    }
  }

  async saveResults(companies) {
    this.logMessage('[6/6] 💾 Salvando resultados...');

    const timestamp = new Date().toISOString().split('T')[0];
    const timeHMS = new Date().toLocaleTimeString('pt-BR', { hour12: false });
    const baseFilename = `ANPG_IFRAME_EXTRACTED_${timestamp}_${companies.length}`;

    try {
      // CSV
      let csvContent = 'numero;empresa;data;hora;fonte\n';
      companies.forEach((company, idx) => {
        const escaped = company.replace(/"/g, '""');
        csvContent += `${idx + 1};"${escaped}";${timestamp};${timeHMS};anpg_iframe_extraction\n`;
      });

      fs.writeFileSync(`${baseFilename}.csv`, csvContent, 'utf-8');
      this.logMessage(`✅ CSV: ${baseFilename}.csv (${companies.length} empresas)`);

      // JSON
      const jsonData = {
        timestamp: new Date().toISOString(),
        data_extracao: timestamp,
        hora_extracao: timeHMS,
        metodo: 'iframe_frame_extraction',
        fonte: 'https://anpg.co.ao/conteudo-local/ [DENTRO DO IFRAME POWERBI]',
        total_empresas: companies.length,
        empresas: companies,
        execucao_log: this.log
      };

      fs.writeFileSync(`${baseFilename}.json`, JSON.stringify(jsonData, null, 2), 'utf-8');
      this.logMessage(`✅ JSON: ${baseFilename}.json`);

      // TXT Log
      fs.writeFileSync(`${baseFilename}_LOG.txt`, this.log.join('\n'), 'utf-8');
      this.logMessage(`✅ LOG: ${baseFilename}_LOG.txt`);

      return baseFilename;

    } catch (error) {
      this.logMessage(`❌ Erro ao salvar: ${error.message}`);
      return null;
    }
  }

  async run() {
    try {
      // Step 1: Initialize
      await this.initialize();

      // Step 2: Load page
      await this.loadPage();

      // Step 3: Find and enter iframe
      const foundIframe = await this.findAndEnterIframe();
      if (!foundIframe) {
        this.logMessage('❌ Não foi possível entrar no iframe. Abortando...');
        return;
      }

      // Step 4: Wait for iframe content
      await this.waitForIframeContent();

      // Step 5: Expand categories (DENTRO DO IFRAME)
      await this.expandAllCategoriesInIframe();

      // Step 5.2: Right-clicks (DENTRO DO IFRAME)
      await this.performRightClicksInIframe();

      // Step 5.3: Scroll
      await this.scrollIframeToBottom();

      // Step 5.5: Extract companies (DENTRO DO IFRAME)
      const companies = await this.extractCompaniesFromIframe();

      if (companies.length === 0) {
        this.logMessage('⚠️  Nenhuma empresa extraída!');
      }

      // Step 6: Save results
      const baseFilename = await this.saveResults(companies);

      // Final summary
      this.logMessage('');
      this.logMessage('═══════════════════════════════════════════════════════');
      this.logMessage('✅ EXTRAÇÃO CONCLUÍDA!');
      this.logMessage('═══════════════════════════════════════════════════════');
      this.logMessage('');
      this.logMessage('📊 RESUMO FINAL:');
      this.logMessage(`   ✓ Empresas extraídas: ${companies.length}`);
      this.logMessage(`   ✓ Arquivo: ${baseFilename}.csv`);
      this.logMessage(`   ✓ Arquivo: ${baseFilename}.json`);
      this.logMessage(`   ✓ Log: ${baseFilename}_LOG.txt`);
      this.logMessage('');
      this.logMessage('💡 Metodo: EXTRAÇÃO DENTRO DO IFRAME DO POWER BI');
      this.logMessage('');

      // Keep browser open briefly
      this.logMessage('⏳ Browser ficará aberto por 10 segundos...');
      await new Promise(r => setTimeout(r, 10000));

    } catch (error) {
      this.logMessage(`❌ ERRO FATAL: ${error.message}`);
      this.logMessage(error.stack);
    } finally {
      await this.cleanup();
    }
  }

  async cleanup() {
    this.logMessage('🧹 Limpando...');

    if (this.browser) {
      try {
        await this.browser.close();
        this.logMessage('✅ Browser fechado');
      } catch (e) {
        this.logMessage(`⚠️  Erro ao fechar browser: ${e.message}`);
      }
    }

    this.logMessage('');
    this.logMessage('═══════════════════════════════════════════════════════');
    this.logMessage('🎉 PROCESSO FINALIZADO');
    this.logMessage('═══════════════════════════════════════════════════════');
  }
}

// Execute
async function main() {
  const extractor = new ANPGIframeExtractor();
  await extractor.run();
}

main().catch(error => {
  console.error('FATAL ERROR:', error);
  process.exit(1);
});
