const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('\n🎯 EXTRAÇÃO COM MENU CONTEXTUAL - SCROLL FINAL\n');
  console.log('═════════════════════════════════════════════════════════\n');

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: false,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    console.log('📍 Acedendo a ANPG Conteúdo Local...');
    await page.goto('https://anpg.co.ao/conteudo-local/', { 
      waitUntil: 'domcontentloaded',
      timeout: 60000 
    });

    console.log('⏳ Aguardando 6 segundos para Power BI carregar...\n');
    await new Promise(r => setTimeout(r, 6000));

    // Tentar fazer scroll dentro do frame
    console.log('📜 Fazendo scroll para expor todos os dados...\n');

    for (let i = 0; i < 10; i++) {
      await page.evaluate(() => {
        // Fazer scroll no elemento explorer
        const explorer = document.querySelector('[data-bi-area-id]') || document.querySelector('div[role="main"]');
        if (explorer) {
          explorer.scroll({ top: explorer.scrollTop + 500, behavior: 'smooth' });
        }
      });
      console.log(`✓ Scroll ${i + 1}/10`);
      await new Promise(r => setTimeout(r, 800));
    }

    console.log('\n⏳ Aguardando estabilização...\n');
    await new Promise(r => setTimeout(r, 2000));

    // Screenshot final
    await page.screenshot({ path: 'scroll_final.png' });
    console.log('📸 Screenshot: scroll_final.png\n');

    // EXTRAÇÃO MASSIVA
    console.log('📥 Extraindo todos os dados visíveis no DOM...\n');

    const dadosExtraidos = await page.evaluate(() => {
      const dados = [];
      const unicas = new Map();

      // Estratégia 1: Todo o texto da página
      const pageText = document.documentElement.innerText;
      const linhas = pageText.split('\n').map(l => l.trim()).filter(l => l.length > 0);

      // Estratégia 2: Elementos específicos
      document.querySelectorAll('span, div, p, li, td').forEach((el, idx) => {
        const text = el.innerText?.trim();
        
        if (text && text.length > 1 && text.length < 400) {
          // Verificar se é único
          if (!unicas.has(text)) {
            unicas.set(text, true);
            
            // Classificar por contexto
            let tipo = 'ITEM';
            let nivel = 0;
            
            if (text.toLowerCase().includes('consultoria') ||
                text.toLowerCase().includes('serviço') ||
                text.toLowerCase().includes('inspeção') ||
                text.toLowerCase().includes('assistência') ||
                text.toLowerCase().includes('suporte') ||
                text.toLowerCase().includes('engenharia') ||
                text.toLowerCase().includes('fabricação') ||
                text.toLowerCase().includes('finanças') ||
                text.toLowerCase().includes('formação') ||
                text.toLowerCase().includes('geociências') ||
                text.toLowerCase().includes('operação') ||
                text.toLowerCase().includes('reservatório') ||
                text.toLowerCase().includes('saúde') ||
                text.toLowerCase().includes('tecnologia') ||
                text.toLowerCase().includes('transporte') ||
                text.toLowerCase().includes('perfuração') ||
                text.toLowerCase().includes('logístico') ||
                text.toLowerCase().includes('avaliação') ||
                text.toLowerCase().includes('submarino')) {
              
              tipo = 'CATEGORIA';
              nivel = 0;
            } else if (text.length > 50) {
              tipo = 'DESCRIÇÃO';
              nivel = 1;
            }

            dados.push({
              nivel: nivel,
              texto: text,
              tipo: tipo,
              fonte: 'DOM_extraction'
            });
          }
        }
      });

      return dados;
    });

    console.log(`✅ Extraídos ${dadosExtraidos.length} itens únicos\n`);

    // Filtrar e organizar
    const categorias = dadosExtraidos.filter(d => d.tipo === 'CATEGORIA');
    const descricoes = dadosExtraidos.filter(d => d.tipo === 'DESCRIÇÃO');
    const outros = dadosExtraidos.filter(d => d.tipo === 'ITEM');

    console.log(`📊 Breakdown:`);
    console.log(`   • Categorias: ${categorias.length}`);
    console.log(`   • Descrições: ${descricoes.length}`);
    console.log(`   • Outros: ${outros.length}\n`);

    // Salvar
    const timestamp = new Date().toISOString().split('T')[0];
    const csvFile = `DADOS_SCROLL_CONTEXTUAL_${timestamp}_${dadosExtraidos.length}.csv`;

    const csvLines = ['nivel;texto;tipo;fonte'];
    dadosExtraidos.forEach(item => {
      csvLines.push(`${item.nivel};"${item.texto.replace(/"/g, '""')}";${item.tipo};${item.fonte}`);
    });

    fs.writeFileSync(csvFile, csvLines.join('\n'), 'utf-8');
    console.log(`💾 CSV: ${csvFile}\n`);

    const jsonFile = csvFile.replace('.csv', '.json');
    fs.writeFileSync(jsonFile, JSON.stringify({
      timestamp: new Date().toISOString(),
      metodo: 'scroll_e_dom_extraction',
      totalItems: dadosExtraidos.length,
      categorias: categorias.length,
      descricoes: descricoes.length,
      outros: outros.length,
      dados: dadosExtraidos
    }, null, 2));

    console.log(`💾 JSON: ${jsonFile}\n`);

    console.log('═════════════════════════════════════════════════════════');
    console.log(`✅ EXTRAÇÃO COM SCROLL PROGRESSIVO CONCLUÍDA!`);
    console.log(`   📊 Total: ${dadosExtraidos.length} itens`);
    console.log(`   📁 Categorias: ${categorias.length}`);
    console.log(`   📖 Descrições: ${descricoes.length}\n`);

    await new Promise(r => setTimeout(r, 2000));
    await browser.close();

  } catch (err) {
    console.error('❌ Erro:', err.message);
    if (browser) await browser.close();
  }
})();
