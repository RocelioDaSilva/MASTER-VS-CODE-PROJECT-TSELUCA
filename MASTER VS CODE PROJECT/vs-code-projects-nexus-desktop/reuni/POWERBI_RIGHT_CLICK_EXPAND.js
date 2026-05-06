const puppeteer = require('puppeteer');
const fs = require('fs');

class PowerBIRightClickExpander {
  constructor() {
    this.logs = [];
    this.companies = new Set();
    this.embedUrl = 'https://app.powerbi.com/view?r=eyJrIjoiYjQ1ZmUyNjQtZDJhYy00MDM4LTk1OTctZmYzN2M1MzEzY2U0IiwidCI6Ijc4YTBlMjI5LTQ0NjMtNDBjOC04NzJhLWI0OTQyYzNjMzEwZCIsImMiOjl9';
  }

  log(msg) {
    const t = new Date().toLocaleTimeString('pt-BR');
    console.log(`[${t}] ${msg}`);
    this.logs.push(`[${t}] ${msg}`);
  }

  async run() {
    let browser, page;
    try {
      this.log('');
      this.log('═════════════════════════════════════════════════════════');
      this.log('🎯 POWER BI - RIGHT CLICK + EXPAND + EXTRACT COMPANIES');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');

      // Iniciar
      this.log('🚀 Iniciando navegador...');
      browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: ['--no-sandbox', '--disable-blink-features=AutomationControlled']
      });

      page = await browser.newPage();
      page.on('error', () => {});

      // Navegar
      this.log('📍 Abrindo Power BI report...');
      try {
        await page.goto(this.embedUrl, {
          waitUntil: 'domcontentloaded',
          timeout: 40000
        }).catch(() => {});
      } catch (e) {
        this.log(`⚠️  Timeout (continuando)`);
      }

      this.log('⏳ Aguardando render (12s)...');
      await new Promise(r => setTimeout(r, 12000));

      // Procurar e fazer right-click no item
      this.log('🖱️ Procurando item "Consultoria, Assessoria e Auditoria"...');

      const foundItem = await page.evaluate(() => {
        // Procurar elemento com esse texto
        const allElements = document.querySelectorAll('*');
        for (const el of allElements) {
          const text = el.innerText || el.textContent || '';
          if (text.includes('Consultoria') && text.includes('Assessoria') && text.includes('Auditoria')) {
            // Se é o elemento exato ou um container
            if (text.trim() === 'Consultoria, Assessoria e Auditoria' || 
                text.includes('Consultoria, Assessoria e Auditoria')) {
              return {
                found: true,
                text: text.substring(0, 100),
                tag: el.tagName,
                classes: el.className
              };
            }
          }
        }
        return { found: false };
      });

      if (!foundItem.found) {
        this.log('⚠️  Item não encontrado por texto exato');
        this.log('🔍 Procurando por partial match...');
        
        // Procurar com relaxed matching
        const partialMatch = await page.evaluate(() => {
          const allElements = Array.from(document.querySelectorAll('*'));
          for (const el of allElements) {
            const text = (el.innerText || el.textContent || '').toLowerCase();
            if (text.includes('consultoria') && text.includes('assessoria')) {
              return {
                found: true,
                text: el.innerText || el.textContent,
                tag: el.tagName,
                classes: el.className,
                rect: el.getBoundingClientRect()
              };
            }
          }
          return { found: false };
        });

        if (!partialMatch.found) {
          this.log('❌ Item não encontrado na página');
          this.log('📸 Capturando screenshot para debug...');
          await page.screenshot({ path: 'powerbi_debug_not_found.png', fullPage: true });
          return;
        }

        foundItem.found = true;
        foundItem.text = partialMatch.text;
        foundItem.rect = partialMatch.rect;
      }

      this.log(`✅ Item encontrado: "${foundItem.text.substring(0, 50)}..."`);

      // Right-click no elemento
      this.log('🖱️ Executando right-click...');

      const rightClickResult = await page.evaluate(() => {
        const allElements = Array.from(document.querySelectorAll('*'));
        
        for (const el of allElements) {
          const text = (el.innerText || el.textContent || '').toLowerCase();
          if (text.includes('consultoria') && text.includes('assessoria')) {
            // Criar e disparar eventos de right-click
            const contextMenuEvent = new MouseEvent('contextmenu', {
              bubbles: true,
              cancelable: true,
              view: window,
              button: 2,
              buttons: 2
            });
            
            el.dispatchEvent(contextMenuEvent);
            
            return {
              clicked: true,
              element: el.tagName,
              text: el.innerText || el.textContent
            };
          }
        }
        
        return { clicked: false };
      });

      if (rightClickResult.clicked) {
        this.log('✅ Right-click executado');
      } else {
        this.log('⚠️  Right-click pode não ter funcionado');
      }

      // Aguardar context menu aparecer
      this.log('⏳ Aguardando context menu (5s)...');
      await new Promise(r => setTimeout(r, 5000));

      // Procurar opcões no context menu
      this.log('🔍 Procurando opções no context menu...');

      const contextMenuOptions = await page.evaluate(() => {
        // Procurar context menu (pode ter classes variadas)
        const possibleMenus = document.querySelectorAll('[role="menu"], .context-menu, .contextMenu, [class*="menu"], [class*="dropdown"]');
        
        const options = [];
        for (const menu of possibleMenus) {
          if (menu.offsetHeight > 0) { // Visível
            const items = menu.querySelectorAll('[role="menuitem"], [role="option"], button, a, span');
            for (const item of items) {
              const text = (item.innerText || item.textContent || '').trim();
              if (text && text.length > 0 && text.length < 100) {
                options.push({
                  text: text,
                  tag: item.tagName,
                  visible: item.offsetHeight > 0
                });
              }
            }
          }
        }
        
        // Se não encontrar menu específico, procurar elementos "Expandir", "drill down", etc
        if (options.length === 0) {
          const allElements = document.querySelectorAll('*');
          const keywords = ['expand', 'expandir', 'drill', 'tudo', 'all', 'expand all'];
          
          for (const el of allElements) {
            const text = (el.innerText || el.textContent || '').toLowerCase();
            if (keywords.some(kw => text.includes(kw)) && el.offsetHeight > 0) {
              options.push({
                text: el.innerText || el.textContent,
                tag: el.tagName,
                isButton: el.tagName === 'BUTTON'
              });
            }
          }
        }
        
        return options;
      });

      this.log(`✅ ${contextMenuOptions.length} opções encontradas no context menu`);
      
      if (contextMenuOptions.length > 0) {
        this.log('');
        this.log('📋 Opções disponíveis:');
        for (let i = 0; i < Math.min(contextMenuOptions.length, 15); i++) {
          this.log(`   ${i + 1}. ${contextMenuOptions[i].text}`);
        }
      }

      // Procurar por "Expandir" ou "Expand All"
      this.log('');
      this.log('🔎 Procurando por opção "Expandir" / "Expand All"...');

      const expandOption = contextMenuOptions.find(opt => {
        const text = opt.text.toLowerCase();
        return text.includes('expand') || text.includes('expandir') || text.includes('tudo');
      });

      if (expandOption) {
        this.log(`✅ Opção encontrada: "${expandOption.text}"`);
        this.log('🖱️ Clicando em "Expandir"...');

        // Clicar na opção
        await page.evaluate((text) => {
          const allElements = document.querySelectorAll('*');
          for (const el of allElements) {
            if ((el.innerText || el.textContent).trim() === text) {
              el.click();
              return;
            }
          }
        }, expandOption.text);

        this.log('⏳ Aguardando expansão (10s)...');
        await new Promise(r => setTimeout(r, 10000));

        // Screenshot após expand
        this.log('📸 Capturando screenshot após expand...');
        await page.screenshot({ path: 'powerbi_after_expand.png', fullPage: true });

      } else {
        this.log('⚠️  Opção "Expandir" não encontrada no context menu');
        this.log('💡 Tentando click direto em qualquer opção com "expand"...');

        const clicked = await page.evaluate(() => {
          const allElements = document.querySelectorAll('*');
          for (const el of allElements) {
            const text = (el.innerText || el.textContent || '').toLowerCase();
            if (text.includes('expand')) {
              el.click();
              return true;
            }
          }
          return false;
        });

        if (clicked) {
          this.log('✅ Click executado em elemento com "expand"');
          await new Promise(r => setTimeout(r, 8000));
        }
      }

      // Extrair empresas/dados após expansão
      this.log('');
      this.log('🔍 Extraindo dados após expansão...');

      const extractedData = await page.evaluate(() => {
        const data = {
          total_text_lines: 0,
          items: [],
          tables: [],
          grid_data: []
        };

        // 1. Todo o texto
        const allText = document.body.innerText;
        const lines = allText.split('\n').filter(l => l.trim().length > 0);
        data.total_text_lines = lines.length;

        // Pegar linhas que parecem ser dados (sem ser UI)
        const ui_keywords = ['keyboard', 'shortcuts', 'accessibility', 'navigation', 'menu', 'filter', 'sort', 'page'];
        const dataLines = lines.filter(line => {
          const lower = line.toLowerCase();
          return !ui_keywords.some(kw => lower.includes(kw)) && line.length > 3 && line.length < 150;
        });

        data.items = dataLines.slice(0, 100);

        // 2. Procurar tabelas
        const tables = document.querySelectorAll('table');
        for (let i = 0; i < Math.min(tables.length, 3); i++) {
          const rows = [];
          const cells = tables[i].querySelectorAll('tr');
          for (let j = 0; j < Math.min(cells.length, 50); j++) {
            rows.push(cells[j].innerText);
          }
          if (rows.length > 0) {
            data.tables.push({ table_index: i, row_count: rows.length });
          }
        }

        // 3. Procurar grids/data
        const gridElements = document.querySelectorAll('[role="grid"], [role="table"], .pbi-table, [class*="grid"]');
        for (let i = 0; i < Math.min(gridElements.length, 3); i++) {
          const text = gridElements[i].innerText.substring(0, 500);
          data.grid_data.push({ grid_index: i, preview: text });
        }

        return data;
      });

      this.log(`✅ Dados extraídos:`);
      this.log(`   Linhas de texto: ${extractedData.total_text_lines}`);
      this.log(`   Items de dados: ${extractedData.items.length}`);
      this.log(`   Tabelas: ${extractedData.tables.length}`);
      this.log(`   Grid elements: ${extractedData.grid_data.length}`);

      if (extractedData.items.length > 0) {
        this.log('');
        this.log('📋 Primeiros 30 items extraídos:');
        for (let i = 0; i < Math.min(extractedData.items.length, 30); i++) {
          this.log(`   ${i + 1}. ${extractedData.items[i]}`);
          this.companies.add(extractedData.items[i]);
        }
      }

      // Salvar resultados
      this.log('');
      this.log('💾 Salvando resultados...');

      const output = {
        timestamp: new Date().toISOString(),
        category: 'Consultoria, Assessoria e Auditoria',
        action: 'Right-click > Expandir > Tudo',
        extracted_count: this.companies.size,
        extracted_items: Array.from(this.companies),
        page_data: {
          total_text_lines: extractedData.total_text_lines,
          context_menu_found: contextMenuOptions.length > 0,
          expand_option_found: expandOption ? true : false,
          expand_option_text: expandOption ? expandOption.text : null,
          tables_found: extractedData.tables.length,
          grid_elements_found: extractedData.grid_data.length
        }
      };

      // JSON
      fs.writeFileSync('POWERBI_CONSULTORIA_EXPANDED.json', JSON.stringify(output, null, 2), 'utf-8');
      this.log('✅ POWERBI_CONSULTORIA_EXPANDED.json');

      // CSV
      let csv = 'numero;empresa_ou_item;categoria;data;hora;fonte\n';
      let num = 1;
      for (const item of this.companies) {
        const date = new Date().toLocaleDateString('pt-BR');
        const time = new Date().toLocaleTimeString('pt-BR');
        csv += `${num};"${item}";"Consultoria, Assessoria e Auditoria";${date};${time};POWERBI_RIGHT_CLICK_EXPAND\n`;
        num++;
      }
      fs.writeFileSync('POWERBI_CONSULTORIA_EXPANDED.csv', csv, 'utf-8');
      this.log(`✅ POWERBI_CONSULTORIA_EXPANDED.csv (${this.companies.size} items)`);

    } catch (err) {
      this.log(`❌ ERRO: ${err.message}`);
      this.log(err.stack);
    } finally {
      if (browser) {
        await browser.close();
      }

      fs.writeFileSync('POWERBI_RIGHT_CLICK_EXPAND.log', this.logs.join('\n'), 'utf-8');

      this.log('');
      this.log('═════════════════════════════════════════════════════════');
      this.log('✅ PROCESSO CONCLUÍDO');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');
    }
  }
}

new PowerBIRightClickExpander().run();
