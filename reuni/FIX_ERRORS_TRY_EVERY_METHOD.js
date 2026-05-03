const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('\n🎯 FIX ERRORS - TRY EVERY METHOD\n');
  console.log('═════════════════════════════════════════════════════════\n');

  let browser;
  const results = {
    methods: [],
    errors: [],
    data: []
  };

  try {
    console.log('🚀 Iniciando browser...');
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-web-security', '--disable-dev-shm-usage']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    // Set timeout for page operations
    page.setDefaultTimeout(30000);

    console.log('📍 Carregando página ANPG...');
    try {
      await page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'domcontentloaded',
        timeout: 30000
      });
      results.methods.push('page_load_success');
    } catch (e) {
      results.errors.push(`page_load_failed: ${e.message}`);
      console.log('❌ Erro no carregamento da página');
      return;
    }

    console.log('⏳ Aguardando Power BI...');
    await new Promise(r => setTimeout(r, 8000));

    // MÉTODO 1: Expandir via ícones diretos
    console.log('🔍 MÉTODO 1: Ícones de expansão...');
    try {
      const method1 = await page.evaluate(() => {
        const expanders = document.querySelectorAll('[aria-expanded="false"], .pvExplorerTreeItemIconContainer, [class*="expander"]');
        let clicked = 0;
        expanders.forEach(el => {
          try {
            if (el.getAttribute('aria-expanded') !== 'true') {
              el.click();
              clicked++;
            }
          } catch (e) {}
        });
        return clicked;
      });
      results.methods.push(`icon_clicks: ${method1}`);
      console.log(`✅ ${method1} ícones clicados`);
    } catch (e) {
      results.errors.push(`method1_error: ${e.message}`);
      console.log('❌ Erro no método 1');
    }

    // MÉTODO 2: Right-click + Expandir
    console.log('🔍 MÉTODO 2: Right-click...');
    try {
      const rightClickDone = await page.evaluate(() => {
        const item = document.querySelector('[role="treeitem"]') || document.querySelector('.pvExplorerTreeItem');
        if (item) {
          const event = new MouseEvent('contextmenu', { bubbles: true, button: 2 });
          item.dispatchEvent(event);
          return true;
        }
        return false;
      });

      if (rightClickDone) {
        await new Promise(r => setTimeout(r, 1000));

        const expandFound = await page.evaluate(() => {
          const menus = document.querySelectorAll('[role="menuitem"], button, .ms-ContextualMenu-link');
          for (let menu of menus) {
            const text = menu.innerText?.toLowerCase() || '';
            if (text.includes('expandir') || text.includes('expand')) {
              menu.click();
              return true;
            }
          }
          return false;
        });

        results.methods.push(`right_click_expand: ${expandFound}`);
        console.log(`✅ Right-click + expand: ${expandFound}`);
      }
    } catch (e) {
      results.errors.push(`method2_error: ${e.message}`);
      console.log('❌ Erro no método 2');
    }

    // MÉTODO 3: Atalhos de teclado
    console.log('🔍 MÉTODO 3: Atalhos...');
    try {
      await page.keyboard.press('Tab');
      await page.keyboard.press('Enter');
      await new Promise(r => setTimeout(r, 1000));
      results.methods.push('keyboard_shortcuts');
      console.log('✅ Atalhos testados');
    } catch (e) {
      results.errors.push(`method3_error: ${e.message}`);
      console.log('❌ Erro no método 3');
    }

    // MÉTODO 4: Scroll progressivo
    console.log('🔍 MÉTODO 4: Scroll...');
    try {
      await page.evaluate(() => {
        window.scrollTo(0, document.body.scrollHeight);
      });
      await new Promise(r => setTimeout(r, 2000));
      await page.evaluate(() => {
        window.scrollTo(0, 0);
      });
      results.methods.push('scroll_method');
      console.log('✅ Scroll realizado');
    } catch (e) {
      results.errors.push(`method4_error: ${e.message}`);
      console.log('❌ Erro no método 4');
    }

    // EXTRAÇÃO DE DADOS
    console.log('📥 Extraindo dados...');
    try {
      const data = await page.evaluate(() => {
        const items = [];
        const seen = new Set();

        // Múltiplas estratégias de extração
        const strategies = [
          { selector: '[role="treeitem"]', type: 'tree' },
          { selector: '.pvExplorerTreeItem', type: 'pv_tree' },
          { selector: 'span', type: 'spans' },
          { selector: 'div', type: 'divs' }
        ];

        strategies.forEach(strategy => {
          document.querySelectorAll(strategy.selector).forEach(el => {
            const text = el.innerText?.trim() || el.textContent?.trim();
            if (text &&
                text.length > 3 &&
                text.length < 200 &&
                !seen.has(text) &&
                !text.toLowerCase().includes('anpg') &&
                !text.toLowerCase().includes('sobre')) {
              seen.add(text);
              items.push({
                text: text,
                strategy: strategy.type,
                length: text.length
              });
            }
          });
        });

        return items;
      });

      results.data = data;
      console.log(`✅ ${data.length} itens extraídos`);
    } catch (e) {
      results.errors.push(`extraction_error: ${e.message}`);
      console.log('❌ Erro na extração');
    }

    // SALVAR RESULTADOS
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `FIX_ERRORS_TRY_ALL_${timestamp}_${results.data.length}`;

    // CSV
    const csvContent = ['text;strategy;length'];
    results.data.forEach(item => {
      csvContent.push(`"${item.text.replace(/"/g, '""')}";${item.strategy};${item.length}`);
    });
    fs.writeFileSync(`${filename}.csv`, csvContent.join('\n'), 'utf-8');

    // JSON
    fs.writeFileSync(`${filename}.json`, JSON.stringify({
      timestamp: new Date().toISOString(),
      methods: results.methods,
      errors: results.errors,
      dataCount: results.data.length,
      data: results.data
    }, null, 2));

    console.log(`\n💾 Arquivos salvos: ${filename}.csv e ${filename}.json`);
    console.log('✅ Script concluído com sucesso!');

  } catch (err) {
    results.errors.push(`main_error: ${err.message}`);
    console.error('❌ Erro geral:', err.message);
  } finally {
    if (browser) {
      try {
        await browser.close();
        console.log('🔒 Browser fechado');
      } catch (e) {
        console.error('❌ Erro ao fechar browser');
      }
    }
  }

  // Resumo final
  console.log('\n═════════════════════════════════════════════════════════');
  console.log('📊 RESUMO FINAL:');
  console.log(`   ✅ Métodos tentados: ${results.methods.length}`);
  console.log(`   ❌ Erros encontrados: ${results.errors.length}`);
  console.log(`   📥 Dados extraídos: ${results.data.length}`);
  console.log('═════════════════════════════════════════════════════════\n');

})();