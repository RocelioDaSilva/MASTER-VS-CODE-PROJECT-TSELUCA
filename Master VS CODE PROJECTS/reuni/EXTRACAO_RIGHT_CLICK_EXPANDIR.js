const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('\n🎯 EXTRAÇÃO COM RIGHT-CLICK + EXPANDIR TUDO\n');
  console.log('═════════════════════════════════════════════════════════\n');

  const browser = await puppeteer.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  console.log('📍 Acessando ANPG...');
  await page.goto('https://anpg.co.ao/conteudo-local/', { 
    waitUntil: 'networkidle2',
    timeout: 60000 
  });

  console.log('⏳ Aguardando carregamento do painel de serviços...');
  await page.waitForSelector('[data-bi-area-id]', { timeout: 30000 }).catch(() => {
    console.log('⚠️  Painel não carregou, continuando...');
  });

  await new Promise(r => setTimeout(r, 3000));

  console.log('\n🔍 Procurando elementos clicáveis...\n');

  // Extrair dados após expandir
  const dados = await page.evaluate(async () => {
    const items = [];
    
    // Procurar todos os itens da lista
    const elementos = document.querySelectorAll('[role="button"]');
    
    console.log(`Encontrados ${elementos.length} elementos`);
    
    for (let item of elementos) {
      const texto = item.innerText?.trim();
      if (texto && texto.length > 0 && !texto.includes('Fechar')) {
        items.push({
          nivel: 0,
          texto: texto,
          tipo: 'ITEM',
          timestamp: new Date().toISOString()
        });
      }
    }
    
    return items;
  });

  console.log(`📊 Elementos encontrados (antes de expandir): ${dados.length}\n`);

  // Agora fazer RIGHT-CLICK para ver menu contextual
  console.log('👆 Fazendo RIGHT-CLICK para abrir menu contextual...\n');

  const menuAbriu = await page.evaluate(async () => {
    // Procurar primeiro item expandível
    const firstItem = document.querySelector('[aria-expanded="false"]') || 
                     document.querySelector('.pvExplorerTreeItemIconContainer');
    
    if (firstItem) {
      // Simular right-click
      const event = new MouseEvent('contextmenu', {
        bubbles: true,
        cancelable: true,
        view: window,
        button: 2
      });
      firstItem.dispatchEvent(event);
      return true;
    }
    return false;
  });

  if (menuAbriu) {
    console.log('✅ Menu contextual aberto\n');
    await new Promise(r => setTimeout(r, 1000));

    // Screenshot do menu
    await page.screenshot({ path: 'menu_contextual.png' });
    console.log('📸 Screenshot do menu: menu_contextual.png\n');

    // Procurar botão "Expandir"
    const expandirClicado = await page.evaluate(() => {
      // Procurar elemento com texto "Expandir"
      const elementos = Array.from(document.querySelectorAll('*')).filter(el => 
        el.innerText?.includes('Expandir') && 
        el.role === 'menuitem'
      );
      
      if (elementos.length > 0) {
        console.log('Clicando em Expandir...');
        elementos[0].click();
        return true;
      }
      return false;
    });

    if (expandirClicado) {
      console.log('✅ Botão "Expandir" clicado\n');
      await new Promise(r => setTimeout(r, 2000));
    }
  }

  console.log('📥 Extraindo dados após expansão...\n');

  // Extrair dados finais
  const dadosFinais = await page.evaluate(() => {
    const items = [];
    let nivel = 0;
    
    // Procurar em toda a estrutura
    const allText = document.body.innerText;
    const linhas = allText.split('\n').filter(l => l.trim().length > 0);
    
    linhas.forEach(linha => {
      const trimmed = linha.trim();
      if (trimmed && trimmed.length > 3 && 
          !trimmed.includes('ANPG') && 
          !trimmed.includes('Sobre') &&
          !trimmed.includes('Dados de E&P')) {
        items.push({
          nivel: 0,
          texto: trimmed,
          tipo: 'ITEM',
          confirmado: 'NÃO',
          origem: 'right_click_expand'
        });
      }
    });
    
    return items;
  });

  console.log(`✅ Dados extraídos: ${dadosFinais.length} itens\n`);

  // Salvar dados
  const timestamp = new Date().toISOString().split('T')[0];
  const csvFilename = `DADOS_RIGHT_CLICK_EXPANDIR_${timestamp}_${dadosFinais.length}.csv`;
  
  const csvContent = ['nivel;texto;tipo;confirmado;origem'];
  dadosFinais.forEach(item => {
    csvContent.push(`${item.nivel};"${item.texto.replace(/"/g, '""')}";${item.tipo};${item.confirmado};${item.origem}`);
  });

  fs.writeFileSync(csvFilename, csvContent.join('\n'), 'utf-8');
  console.log(`💾 CSV salvo: ${csvFilename}\n`);

  // JSON
  const jsonData = {
    timestamp: new Date().toISOString(),
    metodo: 'right_click_contextual_menu_expandir',
    totalItems: dadosFinais.length,
    dados: dadosFinais
  };

  const jsonFilename = csvFilename.replace('.csv', '.json');
  fs.writeFileSync(jsonFilename, JSON.stringify(jsonData, null, 2));
  console.log(`💾 JSON salvo: ${jsonFilename}\n`);

  console.log('═════════════════════════════════════════════════════════\n');
  console.log(`✅ Extração com RIGHT-CLICK + EXPANDIR TUDO concluída!`);
  console.log(`   📊 Total de itens: ${dadosFinais.length}`);
  console.log(`   📁 Método: Menu Contextual (Right-Click)\n`);

  await browser.close();
})();
