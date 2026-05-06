const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('\n🎯 RIGHT-CLICK + EXPANDIR CATEGORIAS - v3 (MULTI-METHOD)\n');
  console.log('═════════════════════════════════════════════════════════\n');

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true, // Changed to headless for better reliability
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-web-security', '--disable-dev-shm-usage']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    // Enable console logging from page
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));

    console.log('📍 Navegando para ANPG Conteúdo Local...');
    await page.goto('https://anpg.co.ao/conteudo-local/', { 
      waitUntil: 'domcontentloaded',
      timeout: 60000 
    });

    console.log('⏳ Aguardando 8 segundos para Power BI carregar completamente...\n');
    await new Promise(r => setTimeout(r, 8000));

    // Método 1: Procurar e clicar em ícones de expansão diretamente
    console.log('🔍 MÉTODO 1: Procurando ícones de expansão...\n');

    const expansaoDireta = await page.evaluate(() => {
      // Procurar ícones de expansão (setas, + , etc.)
      const iconesExpansao = document.querySelectorAll('[class*="expander"], [class*="expand"], [aria-expanded="false"], .pvExplorerTreeItemIconContainer, [data-icon-name="ChevronRight"]');
      
      console.log(`Encontrados ${iconesExpansao.length} ícones de expansão`);
      
      let cliquesRealizados = 0;
      iconesExpansao.forEach((icone, idx) => {
        if (idx < 5) { // Clicar nos primeiros 5
          try {
            icone.click();
            cliquesRealizados++;
          } catch (e) {
            console.log(`Erro ao clicar ícone ${idx}:`, e.message);
          }
        }
      });
      
      return cliquesRealizados;
    });

    console.log(`✅ Método 1: ${expansaoDireta} cliques em ícones de expansão\n`);
    await new Promise(r => setTimeout(r, 3000));

    // Método 2: Right-click em diferentes elementos
    console.log('🔍 MÉTODO 2: Tentando RIGHT-CLICK em múltiplos elementos...\n');

    const rightClickMethods = [
      { selector: '[role="treeitem"]', name: 'treeitem' },
      { selector: '.pvExplorerTreeItem', name: 'pvExplorerTreeItem' },
      { selector: '[class*="explorer"]', name: 'explorer class' },
      { selector: '[aria-expanded="false"]', name: 'aria-expanded false' },
      { selector: 'span', name: 'span elements' }
    ];

    let rightClickRealizado = false;
    let metodoUsado = '';

    for (const method of rightClickMethods) {
      if (rightClickRealizado) break;
      
      console.log(`Tentando right-click em: ${method.name}`);
      
      const result = await page.evaluate((sel) => {
        const elements = document.querySelectorAll(sel);
        if (elements.length > 0) {
          const element = elements[0];
          
          // Simular right-click
          const rightClickEvent = new MouseEvent('contextmenu', {
            bubbles: true,
            cancelable: true,
            view: window,
            button: 2,
            buttons: 2,
            clientX: element.getBoundingClientRect().left + 10,
            clientY: element.getBoundingClientRect().top + 10
          });
          
          element.dispatchEvent(rightClickEvent);
          console.log(`Right-click simulado em ${sel}`);
          return true;
        }
        return false;
      }, method.selector);

      if (result) {
        rightClickRealizado = true;
        metodoUsado = method.name;
        console.log(`✅ Right-click realizado via ${method.name}\n`);
        await new Promise(r => setTimeout(r, 2000));
        break;
      }
    }

    // Método 3: Procurar "Expandir" no menu contextual
    let expandirExecutado = 'NAO_TENTADO';
    
    if (rightClickRealizado) {
      console.log('🔎 Procurando opção "Expandir" no menu contextual...\n');

      const expandirMethods = [
        { selector: '[role="menuitem"]', text: 'expandir' },
        { selector: '.ms-ContextualMenu-link', text: 'expandir' },
        { selector: 'button', text: 'expandir' },
        { selector: '*', text: 'expandir' },
        { selector: '[role="menuitem"]', text: 'expand' },
        { selector: '*', text: 'expand' }
      ];

      for (const method of expandirMethods) {
        const result = await page.evaluate((sel, txt) => {
          const menuItems = document.querySelectorAll(sel);
          
          for (let item of menuItems) {
            const text = item.innerText?.trim().toLowerCase() || item.textContent?.trim().toLowerCase();
            
            if (text && (text.includes(txt) || text === txt)) {
              console.log(`Encontrado: "${text}", clicando...`);
              item.click();
              return 'CLICK_EXECUTADO';
            }
          }
          return 'NAO_ENCONTRADO';
        }, method.selector, method.text);

        if (result === 'CLICK_EXECUTADO') {
          expandirExecutado = 'CLICK_EXECUTADO';
          console.log(`✅ Expandir executado via ${method.selector} com texto "${method.text}"\n`);
          await new Promise(r => setTimeout(r, 3000));
          break;
        }
      }
    }

    // Método 4: Tentar atalhos de teclado
    if (expandirExecutado !== 'CLICK_EXECUTADO') {
      console.log('🔍 MÉTODO 4: Tentando atalhos de teclado...\n');
      
      // Tentar Ctrl+A (selecionar tudo) + alguma tecla
      await page.keyboard.down('Control');
      await page.keyboard.press('A');
      await page.keyboard.up('Control');
      await new Promise(r => setTimeout(r, 1000));
      
      // Tentar tecla Enter ou Space
      await page.keyboard.press('Enter');
      await new Promise(r => setTimeout(r, 2000));
      
      console.log('✅ Atalhos de teclado tentados\n');
    }

    // Método 5: Scroll e tentar encontrar mais elementos
    console.log('🔍 MÉTODO 5: Scroll progressivo para carregar mais dados...\n');
    
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await new Promise(r => setTimeout(r, 2000));
    
    await page.evaluate(() => {
      window.scrollTo(0, 0);
    });
    await new Promise(r => setTimeout(r, 1000));

    // Tirar screenshot final
    await page.screenshot({ path: 'screenshot_final_expandir.png' });
    console.log('📸 Screenshot final: screenshot_final_expandir.png\n');

    // Extração de dados com múltiplas estratégias
    console.log('📥 Extraindo dados com múltiplas estratégias...\n');

    const dadosExtraidos = await page.evaluate(() => {
      const dados = [];
      const processados = new Set();

      // Estratégia 1: Elementos de árvore
      const treeElements = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem, [class*="tree"]');
      treeElements.forEach((el, idx) => {
        const text = el.innerText?.trim() || el.textContent?.trim();
        if (text && text.length > 2 && text.length < 300 && !processados.has(text)) {
          processados.add(text);
          dados.push({
            nivel: 0,
            texto: text,
            tipo: 'TREE_ITEM',
            estrategia: 'tree_elements',
            index: idx
          });
        }
      });

      // Estratégia 2: Todos os spans e divs com texto relevante
      const textElements = document.querySelectorAll('span, div, p');
      textElements.forEach((el, idx) => {
        const text = el.innerText?.trim() || el.textContent?.trim();
        if (text && 
            text.length > 3 && 
            text.length < 200 &&
            !processados.has(text) &&
            (text.includes('Consultoria') || text.includes('Serviço') || text.includes('Inspeção') || 
             text.includes('Assistência') || text.includes('Engenharia') || text.includes('Geociências'))) {
          
          processados.add(text);
          dados.push({
            nivel: 0,
            texto: text,
            tipo: 'TEXT_ELEMENT',
            estrategia: 'text_filter',
            index: idx
          });
        }
      });

      // Estratégia 3: Busca por padrões de empresa/serviço
      const allText = document.body.innerText;
      const lines = allText.split('\n').filter(line => line.trim().length > 0);
      
      lines.forEach((line, idx) => {
        const trimmed = line.trim();
        if (trimmed && 
            trimmed.length > 3 && 
            trimmed.length < 150 &&
            !processados.has(trimmed) &&
            !trimmed.toLowerCase().includes('anpg') &&
            !trimmed.toLowerCase().includes('sobre') &&
            !trimmed.toLowerCase().includes('dados')) {
          
          processados.add(trimmed);
          dados.push({
            nivel: 0,
            texto: trimmed,
            tipo: 'LINE_TEXT',
            estrategia: 'body_text_split',
            index: idx
          });
        }
      });

      return dados;
    });

    console.log(`✅ Extraídos ${dadosExtraidos.length} itens\n`);

    // Salvar
    const timestamp = new Date().toISOString().split('T')[0];
    const csvFile = `DADOS_RIGHT_CLICK_EXPANDIR_${timestamp}_${dadosExtraidos.length}.csv`;

    const csvLines = ['nivel;texto;tipo;estrategia;index'];
    dadosExtraidos.forEach(item => {
      csvLines.push(`${item.nivel};"${item.texto.replace(/"/g, '""')}";${item.tipo};${item.estrategia};${item.index}`);
    });

    fs.writeFileSync(csvFile, csvLines.join('\n'), 'utf-8');
    console.log(`💾 CSV: ${csvFile}\n`);

    const jsonFile = csvFile.replace('.csv', '.json');
    fs.writeFileSync(jsonFile, JSON.stringify({
      timestamp: new Date().toISOString(),
      metodo: 'right_click_multi_method',
      metodosTentados: {
        expansaoDireta: expansaoDireta,
        rightClickRealizado: rightClickRealizado,
        metodoRightClick: metodoUsado,
        expandirExecutado: expandirExecutado
      },
      estrategiasExtracao: ['tree_elements', 'text_filter', 'body_text_split'],
      totalItems: dadosExtraidos.length,
      dados: dadosExtraidos
    }, null, 2));

    console.log(`💾 JSON: ${jsonFile}\n`);

    console.log('═════════════════════════════════════════════════════════');
    console.log(`✅ Extração multi-método concluída!`);
    console.log(`   📊 Total: ${dadosExtraidos.length} itens`);
    console.log(`   🎯 Métodos: Expansão direta + Right-click + Atalhos + Scroll\n`);

    await new Promise(r => setTimeout(r, 1000));

  } catch (err) {
    console.error('❌ Erro durante execução:', err.message);
    console.error('Stack trace:', err.stack);
  } finally {
    if (browser) {
      try {
        console.log('🔒 Fechando browser...');
        await browser.close();
        console.log('✅ Browser fechado com sucesso\n');
      } catch (closeErr) {
        console.error('❌ Erro ao fechar browser:', closeErr.message);
        // Force kill if needed
        try {
          await browser.process().kill('SIGKILL');
        } catch (killErr) {
          console.error('❌ Erro ao forçar fechamento:', killErr.message);
        }
      }
    }
  }
})();
