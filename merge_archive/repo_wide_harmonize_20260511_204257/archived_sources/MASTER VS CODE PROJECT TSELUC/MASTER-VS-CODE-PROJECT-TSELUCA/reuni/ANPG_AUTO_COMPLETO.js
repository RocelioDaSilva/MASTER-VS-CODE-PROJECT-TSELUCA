const puppeteer = require('puppeteer');
const fs = require('fs');

class ANPGAutoExtractor {
  constructor() {
    this.companies = new Set();
    this.log = [];
    this.browser = null;
    this.page = null;
  }

  logMessage(message) {
    const timestamp = new Date().toLocaleTimeString();
    const fullMsg = `[${timestamp}] ${message}`;
    console.log(fullMsg);
    this.log.push(fullMsg);
  }

  async initialize() {
    this.logMessage('═══════════════════════════════════════════════════════');
    this.logMessage('🎯 ANPG - EXTRAÇÃO AUTOMÁTICA COMPLETA');
    this.logMessage('═══════════════════════════════════════════════════════');
    this.logMessage('');

    this.logMessage('[1/5] 🚀 Iniciando navegador...');
    this.browser = await puppeteer.launch({
      headless: false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--disable-web-security',
        '--disable-dev-shm-usage'
      ]
    });

    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1920, height: 1080 });
    this.logMessage('✅ Navegador pronto');
  }

  async loadPage() {
    this.logMessage('[2/5] 📍 Abrindo https://anpg.co.ao/conteudo-local/...');

    try {
      const response = await this.page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'domcontentloaded',
        timeout: 45000
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

  async waitForContent() {
    this.logMessage('[2.5] ⏳ Aguardando Power BI carregar...');

    try {
      await this.page.waitForFunction(() => {
        return document.body.innerText.length > 500;
      }, { timeout: 30000 });

      this.logMessage('✅ Conteúdo detectado');

      this.logMessage('[2.6] ⏳ Aguardando 10 segundos para renderização...');
      await new Promise(r => setTimeout(r, 10000));
      this.logMessage('✅ Pronto para interação');

      return true;
    } catch (error) {
      this.logMessage(`⚠️  Timeout na espera: ${error.message}`);
      return false;
    }
  }

  async expandAllCategories() {
    this.logMessage('[3/5] 🔄 Expandindo todas as categorias...');

    let totalExpanded = 0;

    // Try multiple expansion attempts to ensure all are expanded
    for (let attempt = 1; attempt <= 3; attempt++) {
      this.logMessage(`   Tentativa ${attempt}/3 de expansão...`);

      const expanded = await this.page.evaluate(() => {
        let count = 0;

        // Find all expandable elements
        const selectors = [
          '[aria-expanded="false"]',
          '.pvExplorerTreeItemIconContainer',
          '[class*="expander"][aria-expanded="false"]',
          'button[aria-expanded="false"]'
        ];

        selectors.forEach(selector => {
          const elements = document.querySelectorAll(selector);
          for (let i = 0; i < elements.length; i++) {
            try {
              elements[i].click();
              count++;
            } catch (e) {}
          }
        });

        return count;
      });

      totalExpanded += expanded;
      this.logMessage(`   ✓ ${expanded} elementos clicados`);

      // Wait for content to expand
      await new Promise(r => setTimeout(r, 3000));

      // Check if there are more collapsed items
      const hasMore = await this.page.evaluate(() => {
        return document.querySelectorAll('[aria-expanded="false"]').length > 0;
      });

      if (!hasMore) {
        this.logMessage('✅ Todas as categorias expandidas!');
        break;
      }
    }

    this.logMessage(`✅ Expansão concluída (${totalExpanded} clicks)`);
    return totalExpanded;
  }

  async extractCompanies() {
    this.logMessage('[4/5] 📥 Extraindo nomes de empresas...');

    const data = await this.page.evaluate(() => {
      const items = [];
      const seen = new Set();

      // Multiple extraction strategies
      const strategies = [
        { name: 'Tree Items', selector: '[role="treeitem"]' },
        { name: 'Power BI Items', selector: '.pvExplorerTreeItem' },
        { name: 'All Text Elements', selector: 'span, div, p, a' }
      ];

      strategies.forEach(strategy => {
        const elements = document.querySelectorAll(strategy.selector);

        elements.forEach((el) => {
          const text = el.innerText?.trim() || el.textContent?.trim();

          if (text && 
              text.length > 5 && 
              text.length < 250 &&
              !seen.has(text)) {

            // Filter out UI elements and common words
            const lower = text.toLowerCase();
            const isUIElement = lower.includes('anpg') ||
                               lower.includes('sobre') ||
                               lower.includes('procurar') ||
                               lower.includes('close') ||
                               lower.includes('menu') ||
                               lower.includes('fechar') ||
                               lower.includes('decreto') ||
                               lower.includes('lei') ||
                               lower.includes('expand') ||
                               lower.includes('collapse') ||
                               lower.includes('loading') ||
                               lower.includes('home') ||
                               lower.includes('search') ||
                               lower.includes('filter');

            if (!isUIElement) {
              seen.add(text);
              items.push({
                text: text,
                length: text.length,
                strategy: strategy.name
              });
            }
          }
        });
      });

      return items;
    });

    this.logMessage(`✅ Extraídos ${data.length} itens da página`);

    // Store in set (automatic deduplication)
    data.forEach(item => {
      this.companies.add(item.text);
    });

    this.logMessage(`✅ Total único: ${this.companies.size} empresas`);

    // Show first 10
    this.logMessage('\n   Primeiras 10 empresas extraídas:');
    const companyArray = Array.from(this.companies);
    companyArray.slice(0, 10).forEach((company, idx) => {
      const display = company.substring(0, 60);
      this.logMessage(`   ${idx + 1}. ${display}${company.length > 60 ? '...' : ''}`);
    });

    return companyArray;
  }

  async performRightClicks() {
    this.logMessage('[3.5] 👆 Executando right-clicks nas empresas...');

    const rightClicked = await this.page.evaluate(() => {
      let count = 0;

      // Right-click on tree items to trigger context menus
      const items = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem');

      for (let i = 0; i < Math.min(items.length, 50); i++) {
        try {
          const event = new MouseEvent('contextmenu', {
            bubbles: true,
            cancelable: true,
            button: 2,
            view: window
          });
          items[i].dispatchEvent(event);
          count++;
        } catch (e) {}
      }

      return count;
    });

    this.logMessage(`✅ ${rightClicked} right-clicks executados`);
    await new Promise(r => setTimeout(r, 2000));

    return rightClicked;
  }

  async saveResults(companies) {
    this.logMessage('[5/5] 💾 Salvando resultados...');

    const timestamp = new Date().toISOString().split('T')[0];
    const timeHMS = new Date().toLocaleTimeString('pt-BR', { hour12: false });
    const baseFilename = `ANPG_EXTRACTED_${timestamp}_${companies.length}`;

    // CSV
    let csvContent = 'numero;empresa;data;hora;fonte\n';
    companies.forEach((company, idx) => {
      csvContent += `${idx + 1};"${company.replace(/"/g, '""')}";${timestamp};${timeHMS};anpg_auto_extraction\n`;
    });

    fs.writeFileSync(`${baseFilename}.csv`, csvContent, 'utf-8');
    this.logMessage(`✅ CSV: ${baseFilename}.csv`);

    // JSON
    const jsonData = {
      timestamp: new Date().toISOString(),
      data_extracao: timestamp,
      hora_extracao: timeHMS,
      total_empresas: companies.length,
      metodo: 'automatic_expansion_extraction',
      fonte: 'https://anpg.co.ao/conteudo-local/',
      empresas: companies,
      execucao: this.log
    };

    fs.writeFileSync(`${baseFilename}.json`, JSON.stringify(jsonData, null, 2), 'utf-8');
    this.logMessage(`✅ JSON: ${baseFilename}.json`);

    // TXT Log
    fs.writeFileSync(`${baseFilename}_EXECUCAO.txt`, this.log.join('\n'), 'utf-8');
    this.logMessage(`✅ LOG: ${baseFilename}_EXECUCAO.txt`);

    return baseFilename;
  }

  async run() {
    try {
      // Initialize
      await this.initialize();

      // Load ANPG page
      await this.loadPage();

      // Wait for content
      await this.waitForContent();

      // Expand all categories
      await this.expandAllCategories();

      // Perform right-clicks
      await this.performRightClicks();

      // Extract companies
      const companies = await this.extractCompanies();

      // Save results
      const baseFilename = await this.saveResults(companies);

      // Final summary
      this.logMessage('');
      this.logMessage('═══════════════════════════════════════════════════════');
      this.logMessage('✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!');
      this.logMessage('═══════════════════════════════════════════════════════');
      this.logMessage('');
      this.logMessage('📊 RESUMO FINAL:');
      this.logMessage(`   ✓ Empresas extraídas: ${companies.length}`);
      this.logMessage(`   ✓ Arquivo: ${baseFilename}.csv`);
      this.logMessage(`   ✓ Arquivo: ${baseFilename}.json`);
      this.logMessage(`   ✓ Log: ${baseFilename}_EXECUCAO.txt`);
      this.logMessage('');
      this.logMessage('💡 Próximos passos:');
      this.logMessage('   1. Abra o arquivo .csv em Excel ou Google Sheets');
      this.logMessage('   2. Valide os nomes');
      this.logMessage('   3. Importe em base de dados');
      this.logMessage('');

      // Keep browser open for 10 seconds
      this.logMessage('⏳ Browser ficará aberto por 10 segundos...');
      await new Promise(r => setTimeout(r, 10000));

    } catch (error) {
      this.logMessage(`❌ ERRO: ${error.message}`);
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
  const extractor = new ANPGAutoExtractor();
  await extractor.run();
}

main().catch(error => {
  console.error('FATAL ERROR:', error);
  process.exit(1);
});