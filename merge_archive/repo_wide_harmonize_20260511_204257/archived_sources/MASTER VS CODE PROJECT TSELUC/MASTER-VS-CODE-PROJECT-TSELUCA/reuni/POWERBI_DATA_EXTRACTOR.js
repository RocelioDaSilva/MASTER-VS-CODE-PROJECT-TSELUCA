const puppeteer = require('puppeteer');
const fs = require('fs');

class PowerBIDataExtractor {
  constructor() {
    this.reportId = 'b45fe264-d2ac-4038-9597-ff37c5313ce4';
    this.workspaceId = '78a0e229-4463-40c8-872a-b4942c3c310d';
    this.embedUrl = 'https://app.powerbi.com/view?r=eyJrIjoiYjQ1ZmUyNjQtZDJhYy00MDM4LTk1OTctZmYzN2M1MzEzY2U0IiwidCI6Ijc4YTBlMjI5LTQ0NjMtNDBjOC04NzJhLWI0OTQyYzNjMzEwZCIsImMiOjl9';
    this.logs = [];
    this.data = {
      tables: [],
      visuals: [],
      raw_text: [],
      companies: new Set()
    };
  }

  log(msg) {
    const t = new Date().toLocaleTimeString('pt-BR');
    console.log(`[${t}] ${msg}`);
    this.logs.push(`[${t}] ${msg}`);
  }

  async extractFromPowerBIPage() {
    let browser, page;
    try {
      this.log('');
      this.log('═════════════════════════════════════════════════════════');
      this.log('🎯 POWER BI - EXTRAÇÃO DE DADOS DO RELATÓRIO');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');

      this.log('📊 IDs DO RELATÓRIO:');
      this.log(`   Report ID: ${this.reportId}`);
      this.log(`   Workspace ID: ${this.workspaceId}`);
      this.log('');

      // Iniciar navegador
      this.log('🚀 Iniciando navegador...');
      browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'],
        timeout: 90000
      });

      page = await browser.newPage();
      page.on('error', () => {});

      // Abrir o embed URL diretamente
      this.log('📍 Abrindo Power BI embed report...');
      
      try {
        await page.goto(this.embedUrl, {
          waitUntil: 'domcontentloaded',
          timeout: 40000
        }).catch(e => this.log(`⚠️  ${e.message}`));
      } catch (e) {
        this.log(`⚠️  Timeout na navegação`);
      }

      // Aguardar render
      this.log('⏳ Aguardando carregamento (15s)...');
      await new Promise(r => setTimeout(r, 15000));

      // Extrair conteúdo
      this.log('🔍 Extraindo dados da página...');

      const pageData = await page.evaluate(() => {
        const data = {
          title: document.title,
          url: window.location.href,
          text_content: [],
          tables: [],
          canvas_elements: [],
          json_data: [],
          table_cells: []
        };

        // 1. Todo o texto
        const splittedText = document.body.innerText.split('\n').filter(l => l.trim().length > 0);
        data.text_content = splittedText.slice(0, 200); // Primeiros 200 linhas

        // 2. Tabelas HTML
        const tables = document.querySelectorAll('table');
        for (let i = 0; i < Math.min(tables.length, 5); i++) {
          const rows = [];
          const cells = tables[i].querySelectorAll('tr');
          for (const cell of cells) {
            rows.push(cell.innerText);
          }
          if (rows.length > 0) {
            data.tables.push({ table_index: i, rows: rows });
          }
        }

        // 3. Canvas (Power BI usa canvas para renderizar visuals)
        const canvases = document.querySelectorAll('canvas');
        data.canvas_elements = canvases.length;

        // 4. Procurar elementos com dados
        const divs = document.querySelectorAll('div[class*="tile"], div[class*="visual"], div[role="group"]');
        for (let i = 0; i < Math.min(divs.length, 20); i++) {
          const text = divs[i].innerText;
          if (text && text.length > 5) {
            data.table_cells.push({
              index: i,
              text: text.substring(0, 200)
            });
          }
        }

        // 5. Procurar por JSON em scripts
        const scripts = document.querySelectorAll('script[type="application/json"], script:not([src])');
        for (let i = 0; i < Math.min(scripts.length, 3); i++) {
          const text = scripts[i].innerText;
          if (text && text.length > 20) {
            try {
              const obj = JSON.parse(text);
              data.json_data.push({ script_index: i, data: JSON.stringify(obj).substring(0, 500) });
            } catch (e) {
              // Ignorar parse errors
            }
          }
        }

        return data;
      });

      this.log(`✅ Extração completada:`);
      this.log(`   Linhas de texto: ${pageData.text_content.length}`);
      this.log(`   Tabelas encontradas: ${pageData.tables.length}`);
      this.log(`   Canvas elements: ${pageData.canvas_elements}`);
      this.log(`   Elementos com dados: ${pageData.table_cells.length}`);
      this.log(`   Scripts JSON: ${pageData.json_data.length}`);
      this.log('');

      // Processar texto para encontrar empresas
      this.log('🔎 Procurando nomes de empresas no conteúdo...');
      
      const companies = new Set();
      for (const line of pageData.text_content) {
        const cleaned = line.trim();
        
        // Filtros simples
        if (cleaned.length < 3 || cleaned.length > 100) continue;
        if (/^\d+$/.test(cleaned)) continue;
        if (!/[A-Za-zÀ-ÿ]/.test(cleaned)) continue;
        
        // Não incluir UI
        const ui = ['Skip', 'Power', 'BI', 'Home', 'Back', 'Next', 'Previous', 'Page',
                   'Loading', 'Expand', 'Collapse', 'Filter', 'Sort', 'Export', 'Dashboard',
                   'Report', 'Slicer', 'Visual', 'Tile', 'Canvas', 'Group', 'Field', 'Value'];
        
        if (ui.some(word => cleaned.includes(word))) continue;

        companies.add(cleaned);
      }

      this.data.companies = companies;
      this.log(`✅ ${companies.size} items potenciais encontrados`);
      
      if (companies.size > 0) {
        this.log('');
        this.log('📋 Primeiros 20 items:');
        let count = 0;
        for (const company of companies) {
          if (count >= 20) break;
          this.log(`   ${count + 1}. ${company}`);
          count++;
        }
      }

      // Salvar dados
      this.log('');
      this.log('💾 Salvando dados...');

      const output = {
        timestamp: new Date().toISOString(),
        report_ids: {
          report_id: this.reportId,
          workspace_id: this.workspaceId
        },
        extracted_data: {
          total_items: companies.size,
          page_title: pageData.title,
          tables_found: pageData.tables.length,
          canvas_elements: pageData.canvas_elements,
          text_lines: pageData.text_content.length
        },
        page_content_preview: {
          first_20_lines: pageData.text_content.slice(0, 20),
          total_tables: pageData.tables.map(t => ({ rows: t.rows.length }))
        },
        extracted_items: Array.from(companies).sort(),
        raw_page_data: pageData
      };

      // JSON com tudo
      fs.writeFileSync('POWERBI_EXTRACTED_DATA.json', JSON.stringify(output, null, 2), 'utf-8');
      this.log('✅ POWERBI_EXTRACTED_DATA.json salvo');

      // CSV apenas com os items
      if (companies.size > 0) {
        let csv = 'numero;item;data;hora;fonte\n';
        let num = 1;
        for (const item of companies) {
          const date = new Date().toLocaleDateString('pt-BR');
          const time = new Date().toLocaleTimeString('pt-BR');
          csv += `${num};${item};${date};${time};POWERBI_EMBEDDED\n`;
          num++;
        }
        fs.writeFileSync('POWERBI_ITEMS.csv', csv, 'utf-8');
        this.log(`✅ POWERBI_ITEMS.csv salvo (${companies.size} items)`);
      }

      // Screenshot
      this.log('📸 Capturando screenshot...');
      await page.screenshot({ path: 'powerbi_report_screenshot.png', fullPage: true });
      this.log('✅ powerbi_report_screenshot.png');

    } catch (err) {
      this.log(`❌ ERRO: ${err.message}`);
      this.log(err.stack);
    } finally {
      if (browser) {
        await browser.close();
      }

      // Salvar log
      fs.writeFileSync('POWERBI_EXTRACTION.log', this.logs.join('\n'), 'utf-8');

      this.log('');
      this.log('═════════════════════════════════════════════════════════');
      this.log('✅ PROCESSO CONCLUÍDO');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');
    }
  }
}

new PowerBIDataExtractor().extractFromPowerBIPage();
