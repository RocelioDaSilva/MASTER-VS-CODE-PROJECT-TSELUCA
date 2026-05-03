const puppeteer = require('puppeteer');
const fs = require('fs');

class PowerBIClickExpandButton {
  async run() {
    let browser;
    const logs = [];
    const log = (msg) => {
      const t = new Date().toLocaleTimeString('pt-BR');
      const line = `[${t}] ${msg}`;
      console.log(line);
      logs.push(line);
    };

    try {
      log('');
      log('🎯 POWER BI - CLICAR "+" PARA EXPANDIR CONSULTORIA');
      log('');

      browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: ['--no-sandbox']
      });

      const page = await browser.newPage();

      const embedUrl = 'https://app.powerbi.com/view?r=eyJrIjoiYjQ1ZmUyNjQtZDJhYy00MDM4LTk1OTctZmYzN2M1MzEzY2U0IiwidCI6Ijc4YTBlMjI5LTQ0NjMtNDBjOC04NzJhLWI0OTQyYzNjMzEwZCIsImMiOjl9';

      log('📍 Abrindo Power BI...');
      try {
        await page.goto(embedUrl, { waitUntil: 'domcontentloaded', timeout: 40000 }).catch(() => {});
      } catch (e) {
        log(`⚠️  ${e.message}`);
      }

      log('⏳ Aguardando 15 segundos...');
      await new Promise(r => setTimeout(r, 15000));

      log('📸 Screenshot 1: Antes de expandir');
      await page.screenshot({ path: 'SCREENSHOT_01_ANTES_EXPANDIR.png', fullPage: true });

      // Procurar e clicar no "+"
      log('🔍 Procurando elemento "Consultoria, Assessoria e Auditoria"...');

      const clickResult = await page.evaluate(() => {
        // Encontrar a linha que contém "Consultoria"
        const elements = document.querySelectorAll('*');
        
        for (const el of elements) {
          const text = (el.innerText || el.textContent || '').trim();
          
          if (text.includes('Consultoria') && text.includes('Assessoria')) {
            // Procurar por um botão "+", button, ou svg expandable próximo
            let parent = el.parentElement;
            
            // Ir para cima até 5 níveis
            for (let i = 0; i < 5 && parent; i++) {
              // Procurar por botões de expandir dentro do parent
              const buttons = parent.querySelectorAll('button, [role="button"], svg');
              for (const btn of buttons) {
                const btnText = (btn.innerText || btn.textContent || '').trim();
                // Procurar por "+", "expand", ou ícone de expandir
                if (btnText === '+' || btnText.toLowerCase().includes('expand')) {
                  btn.click();
                  return { clicked: true, element: 'button + found' };
                }
              }
              parent = parent.parentElement;
            }

            // Se não encontrou botão, tenta clicar no elemento mesmo
            el.click();
            return { clicked: true, element: 'consultoria element' };
          }
        }

        // Fallback: procurar QUALQUER "+" perto de "Consultoria"
        let consultoriaIndex = -1;
        const allText = document.body.innerText.split('\n');
        
        for (let i = 0; i < allText.length; i++) {
          if (allText[i].includes('Consultoria')) {
            consultoriaIndex = i;
            break;
          }
        }

        if (consultoriaIndex > 0) {
          // Procurar por elementos na região
          const allElements = document.querySelectorAll('*');
          for (const el of allElements) {
            const text = (el.innerText || el.textContent || '').trim();
            if (text === '+' && el.offsetHeight > 0) {
              el.click();
              return { clicked: true, element: 'plus button' };
            }
          }
        }

        return { clicked: false };
      });

      if (clickResult.clicked) {
        log(`✅ Clicado em: ${clickResult.element}`);
      } else {
        log('⚠️  Não conseguiu clicar no botão de expandir');
      }

      log('⏳ Aguardando expansão (10 segundos)...');
      await new Promise(r => setTimeout(r, 10000));

      log('📸 Screenshot 2: Após expandir');
      await page.screenshot({ path: 'SCREENSHOT_02_APOS_EXPANDIR.png', fullPage: true });

      // Extrair dados após expansão
      log('📊 Extraindo dados...');

      const afterExpandData = await page.evaluate(() => {
        const lines = document.body.innerText.split('\n').filter(l => l.trim().length > 1);
        return {
          total_lines: lines.length,
          first_100_lines: lines.slice(0, 100)
        };
      });

      log(`✅ ${afterExpandData.total_lines} linhas encontradas após expansão`);
      log(`✅ Primeiras 100 linhas capturadas`);

      // Salvar dados
      const companies = [];
      for (const line of afterExpandData.first_100_lines) {
        const cleaned = line.trim();
        if (cleaned.length > 3 && cleaned.length < 150 && !cleaned.match(/^[+-]$/)) {
          companies.push(cleaned);
        }
      }

      const output = {
        timestamp: new Date().toISOString(),
        category: 'Consultoria, Assessoria e Auditoria',
        action: 'Expandir via clique (+)',
        total_items: companies.length,
        items: companies
      };

      fs.writeFileSync('POWERBI_CONSULTORIA_EXPANDIDO.json', JSON.stringify(output, null, 2), 'utf-8');
      log('💾 POWERBI_CONSULTORIA_EXPANDIDO.json');

      // CSV
      if (companies.length > 0) {
        let csv = 'numero;empresa_item;data;hora;fonte\n';
        for (let i = 0; i < companies.length; i++) {
          const date = new Date().toLocaleDateString('pt-BR');
          const time = new Date().toLocaleTimeString('pt-BR');
          csv += `${i + 1};"${companies[i]}";${date};${time};POWERBI_CLICK_EXPAND\n`;
        }
        fs.writeFileSync('POWERBI_CONSULTORIA_EXPANDIDO.csv', csv, 'utf-8');
        log(`💾 POWERBI_CONSULTORIA_EXPANDIDO.csv (${companies.length} items)`);
      }

      log('');
      log('📋 Primeiros 30 items extraídos:');
      for (let i = 0; i < Math.min(companies.length, 30); i++) {
        log(`   ${i + 1}. ${companies[i]}`);
      }

    } catch (err) {
      log(`❌ ERRO: ${err.message}`);
    } finally {
      if (browser) {
        await browser.close();
      }

      fs.writeFileSync('POWERBI_CLICK_EXPAND.log', logs.join('\n'), 'utf-8');

      log('');
      log('✅ CONCLUÍDO');
      log('');
    }
  }
}

new PowerBIClickExpandButton().run();
