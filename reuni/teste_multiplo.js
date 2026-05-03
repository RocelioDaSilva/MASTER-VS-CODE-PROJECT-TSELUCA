const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('\n🎯 TESTE RÁPIDO - MÚLTIPLOS MÉTODOS DE EXPANSÃO\n');
  console.log('═════════════════════════════════════════════════════════\n');

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-web-security']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    console.log('📍 Carregando página...');
    await page.goto('https://anpg.co.ao/conteudo-local/', {
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });

    console.log('⏳ Aguardando carregamento...');
    await new Promise(r => setTimeout(r, 5000));

    // Método 1: Clicar em todos os ícones de expansão
    console.log('🔍 MÉTODO 1: Clicando em ícones de expansão...');
    const method1 = await page.evaluate(() => {
      const expanders = document.querySelectorAll('[aria-expanded="false"], [class*="expander"], .pvExplorerTreeItemIconContainer');
      let clicked = 0;
      expanders.forEach(el => {
        try { el.click(); clicked++; } catch(e) {}
      });
      return clicked;
    });
    console.log(`✅ ${method1} ícones clicados\n`);

    // Método 2: Right-click no primeiro item
    console.log('🔍 MÉTODO 2: Right-click...');
    const method2 = await page.evaluate(() => {
      const item = document.querySelector('[role="treeitem"]') || document.querySelector('.pvExplorerTreeItem');
      if (item) {
        const event = new MouseEvent('contextmenu', { bubbles: true, button: 2 });
        item.dispatchEvent(event);
        return true;
      }
      return false;
    });
    console.log(`✅ Right-click: ${method2}\n`);

    // Método 3: Procurar "Expandir" no menu
    await new Promise(r => setTimeout(r, 1000));
    console.log('🔍 MÉTODO 3: Procurando "Expandir"...');
    const method3 = await page.evaluate(() => {
      const items = document.querySelectorAll('[role="menuitem"], button, .ms-ContextualMenu-link');
      for (let item of items) {
        const text = item.innerText?.toLowerCase() || '';
        if (text.includes('expandir') || text.includes('expand')) {
          item.click();
          return true;
        }
      }
      return false;
    });
    console.log(`✅ Expandir encontrado: ${method3}\n`);

    // Método 4: Scroll
    console.log('🔍 MÉTODO 4: Scroll...');
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await new Promise(r => setTimeout(r, 2000));
    console.log('✅ Scroll realizado\n');

    // Extração
    console.log('📥 Extraindo dados...');
    const dados = await page.evaluate(() => {
      const items = [];
      const seen = new Set();

      // Estratégia múltipla
      const selectors = ['[role="treeitem"]', '.pvExplorerTreeItem', 'span', 'div'];
      selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
          const text = el.innerText?.trim();
          if (text && text.length > 3 && text.length < 200 && !seen.has(text) &&
              !text.toLowerCase().includes('anpg')) {
            seen.add(text);
            items.push({ texto: text, seletor: sel });
          }
        });
      });

      return items;
    });

    console.log(`✅ ${dados.length} itens extraídos\n`);

    // Salvar
    const csvFile = `TESTE_MULTIPLO_${new Date().toISOString().split('T')[0]}_${dados.length}.csv`;
    const csvContent = ['texto;seletor'];
    dados.forEach(item => csvContent.push(`"${item.texto.replace(/"/g, '""')}";${item.seletor}`));
    fs.writeFileSync(csvFile, csvContent.join('\n'), 'utf-8');

    console.log(`💾 Salvo: ${csvFile}`);
    console.log('✅ Teste concluído!\n');

  } catch (err) {
    console.error('❌ Erro:', err.message);
  } finally {
    if (browser) await browser.close();
  }
})();