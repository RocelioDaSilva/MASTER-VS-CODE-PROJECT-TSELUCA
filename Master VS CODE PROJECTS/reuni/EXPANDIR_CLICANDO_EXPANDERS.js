const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('\n🎯 ESTRATÉGIA SIMPLES: CLICAR NOS EXPANDERS\n');
  console.log('═════════════════════════════════════════════════════════\n');

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: false,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    console.log('📍 Navegando para ANPG...');
    await page.goto('https://anpg.co.ao/conteudo-local/', { 
      waitUntil: 'domcontentloaded',
      timeout: 60000 
    });

    console.log('⏳ Aguardando 6 segundos...\n');
    await new Promise(r => setTimeout(r, 6000));

    // Procurar e clicar em todos os checkboxes para expandir
    console.log('🔍 Procurando elementos para expandir...\n');

    let totalClicado = 0;
    
    for (let tentativa = 0; tentativa < 25; tentativa++) {
      const clicado = await page.evaluate(() => {
        // Procurar primeiro elemento com "+" ou icon de expandir
        const expandables = document.querySelectorAll(
          '.pvExplorerTreeItemIconContainer, [class*="expander"], [class*="expand"], [class*="plus"]'
        );

        if (expandables.length > 0) {
          // Clicar no primeiro que não está expandido
          for (let exp of expandables) {
            // Verificar se ainda pode expandir
            if (exp.getAttribute('aria-expanded') !== 'true' && 
                !exp.classList.contains('expanded')) {
              exp.click();
              return true;
            }
          }
        }

        return false;
      });

      if (!clicado) {
        console.log(`✅ Todos os elementos foram expandidos (${tentativa} clicks)\n`);
        totalClicado = tentativa;
        break;
      } else {
        totalClicado = tentativa + 1;
        console.log(`✓ Click ${tentativa + 1} realizado, aguardando...`);
        await new Promise(r => setTimeout(r, 500));
      }
    }

    console.log(`\n⏳ Aguardando 3 segundos para renderização...\n`);
    await new Promise(r => setTimeout(r, 3000));

    // Screenshot final
    await page.screenshot({ path: 'final_expandido.png' });
    console.log('📸 Screenshot: final_expandido.png\n');

    // Extrair dados
    console.log('📥 Extraindo todos os dados expandidos...\n');

    const dados = await page.evaluate(() => {
      const items = [];
      const processados = new Set();

      // Estratégia 1: Procurar span que contém texto de categorias/empresas
      document.querySelectorAll('span').forEach((span, idx) => {
        const text = span.innerText?.trim();
        
        if (text && 
            text.length > 2 && 
            text.length < 300 &&
            !processados.has(text) &&
            !text.includes('Procurar') &&
            !text.includes('ANPG') &&
            !text.includes('Decreto')) {
          
          processados.add(text);
          
          // Tentar detectar nível
          let nivel = 0;
          if (text.toLowerCase().includes('consultoria') || 
              text.toLowerCase().includes('serviço') ||
              text.toLowerCase().includes('sistema')) {
            nivel = 0; // Provavelmente uma categoria
          } else if (text.length > 100) {
            nivel = 1; // Provavelmente uma subcategoria/descrição
          } else {
            nivel = 2; // Provavelmente uma empresa
          }
          
          items.push({
            nivel: nivel,
            texto: text,
            tipo: nivel === 0 ? 'CATEGORIA' : nivel === 1 ? 'SUBCATEGORIA' : 'EMPRESA',
            index: idx
          });
        }
      });

      return items;
    });

    console.log(`✅ Extraídos ${dados.length} itens\n`);

    // Salvar
    const timestamp = new Date().toISOString().split('T')[0];
    const csvFile = `DADOS_EXPANDIR_CLIQUES_${timestamp}_${dados.length}.csv`;

    const csvLines = ['nivel;texto;tipo;index'];
    dados.forEach(item => {
      csvLines.push(`${item.nivel};"${item.texto.replace(/"/g, '""')}";${item.tipo};${item.index}`);
    });

    fs.writeFileSync(csvFile, csvLines.join('\n'), 'utf-8');
    console.log(`💾 CSV: ${csvFile}\n`);

    const jsonFile = csvFile.replace('.csv', '.json');
    fs.writeFileSync(jsonFile, JSON.stringify({
      timestamp: new Date().toISOString(),
      metodo: 'clicar_expanders_direto',
      totalCliques: totalClicado,
      totalItems: dados.length,
      breakdown: {
        categorias: dados.filter(d => d.tipo === 'CATEGORIA').length,
        subcategorias: dados.filter(d => d.tipo === 'SUBCATEGORIA').length,
        empresas: dados.filter(d => d.tipo === 'EMPRESA').length
      },
      dados: dados
    }, null, 2));

    console.log(`💾 JSON: ${jsonFile}\n`);

    console.log('═════════════════════════════════════════════════════════');
    console.log(`✅ EXTRAÇÃO CONCLUÍDA!`);
    console.log(`   📊 Total: ${dados.length} itens`);
    console.log(`   🔄 Cliques totais: ${totalClicado}`);
    console.log(`   📁 Categorias: ${dados.filter(d => d.tipo === 'CATEGORIA').length}`);
    console.log(`   📁 Subcategorias: ${dados.filter(d => d.tipo === 'SUBCATEGORIA').length}`);
    console.log(`   🏢 Empresas: ${dados.filter(d => d.tipo === 'EMPRESA').length}\n`);

    await new Promise(r => setTimeout(r, 2000));
    await browser.close();

  } catch (err) {
    console.error('❌ Erro:', err.message);
    if (browser) await browser.close();
  }
})();
