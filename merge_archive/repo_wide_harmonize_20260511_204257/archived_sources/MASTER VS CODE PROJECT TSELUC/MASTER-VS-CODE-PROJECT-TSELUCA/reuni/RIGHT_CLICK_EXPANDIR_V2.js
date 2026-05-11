const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('\n🎯 RIGHT-CLICK PARA EXPANDIR TUDO - V2\n');
  console.log('═════════════════════════════════════════════════════════\n');

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: false,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    console.log('📍 Navegando para ANPG...');
    await page.goto('https://anpg.co.ao/conteudo-local/', { 
      waitUntil: 'domcontentloaded',
      timeout: 60000 
    });

    console.log('⏳ Aguardando 5 segundos para UI carregar...');
    await new Promise(r => setTimeout(r, 5000));

    // Procurar primeiro item expansível
    console.log('\n👆 Localizando primeiro item para right-click...\n');

    const itemEncontrado = await page.evaluate(() => {
      // Procurar elementos clicáveis/expansíveis
      const allElements = document.querySelectorAll('[role="treeitem"], [class*="explorer"]');
      
      if (allElements.length > 0) {
        const item = allElements[0];
        console.log('Item encontrado:', item.innerText?.substring(0, 50));
        return true;
      }
      return false;
    });

    if (itemEncontrado) {
      console.log('✅ Item localizado, fazendo RIGHT-CLICK...\n');

      // Right-click no primeiro item
      await page.mouse.click(200, 300, { button: 'right' });
      await new Promise(r => setTimeout(r, 1500));

      // Screenshot do menu
      await page.screenshot({ path: 'menu_context.png' });
      console.log('📸 Screenshot salvo: menu_context.png\n');

      // Procurar e clicar em "Expandir"
      console.log('🔍 Procurando botão "Expandir" no menu...\n');

      const expandirOk = await page.evaluate(() => {
        // Diferentes formas de encontrar o botão
        let elementos = Array.from(document.querySelectorAll('*')).filter(el => {
          return el.innerText?.trim().toLowerCase() === 'expandir' ||
                 el.title?.toLowerCase().includes('expandir') ||
                 el.textContent?.trim().toLowerCase() === 'expandir';
        });

        if (elementos.length > 0) {
          console.log(`Encontrado elemento "Expandir"`);
          elementos[0].click();
          return true;
        }
        return false;
      });

      if (expandirOk) {
        console.log('✅ Click em "Expandir" realizado!\n');
        await new Promise(r => setTimeout(r, 3000));

        // Screenshot após expandir
        await page.screenshot({ path: 'apos_expandir.png' });
        console.log('📸 Screenshot após expandir: apos_expandir.png\n');
      } else {
        console.log('⚠️  Botão "Expandir" não encontrado, continuando...\n');
      }
    }

    // Extrair dados
    console.log('📥 Extraindo todos os dados visíveis...\n');

    const dados = await page.evaluate(() => {
      const items = [];
      
      // Estratégia 1: Procurar todos os elementos com texto
      const textElements = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem, [class*="tree"]');
      
      textElements.forEach((el, idx) => {
        const texto = el.innerText?.trim();
        if (texto && texto.length > 2 && !texto.includes('ANPG')) {
          items.push({
            nivel: 0,
            texto: texto,
            tipo: 'ITEM',
            index: idx
          });
        }
      });

      // Estratégia 2: Procurar spans e divs com serviços
      if (items.length === 0) {
        const allText = [];
        document.querySelectorAll('span, div, p').forEach(el => {
          const txt = el.innerText?.trim();
          if (txt && txt.length > 3 && txt.length < 200 && 
              !txt.includes('ANPG') && !txt.includes('Sobre')) {
            allText.push(txt);
          }
        });

        // Remover duplicatas
        const unique = [...new Set(allText)];
        unique.forEach((txt, idx) => {
          items.push({
            nivel: 0,
            texto: txt,
            tipo: 'ITEM',
            index: idx
          });
        });
      }

      return items;
    });

    console.log(`✅ Extraídos ${dados.length} itens\n`);

    // Salvar dados
    const timestamp = new Date().toISOString().split('T')[0];
    const csvFile = `DADOS_RIGHT_CLICK_${timestamp}_${dados.length}.csv`;

    const csvLines = ['nivel;texto;tipo;index'];
    dados.forEach(item => {
      csvLines.push(`${item.nivel};"${item.texto.replace(/"/g, '""')}";${item.tipo};${item.index}`);
    });

    fs.writeFileSync(csvFile, csvLines.join('\n'), 'utf-8');
    console.log(`💾 CSV: ${csvFile}`);

    // JSON
    const jsonFile = csvFile.replace('.csv', '.json');
    fs.writeFileSync(jsonFile, JSON.stringify({
      timestamp: new Date().toISOString(),
      metodo: 'right_click_contextual_menu',
      totalItems: dados.length,
      dados: dados
    }, null, 2));

    console.log(`💾 JSON: ${jsonFile}`);

    console.log('\n═════════════════════════════════════════════════════════');
    console.log(`✅ Extração concluída: ${dados.length} itens\n`);

    await new Promise(r => setTimeout(r, 2000));
    await browser.close();

  } catch (err) {
    console.error('❌ Erro:', err.message);
    if (browser) await browser.close();
  }
})();
