const puppeteer = require('puppeteer');
const fs = require('fs');

class PowerBICategoryExtractor {
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
      log('🎯 POWER BI - EX TRAÇÃ O DE CATEGORIAS (SEM RIGHT-CLICK)');
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

      log('⏳ Aguardando 20 segundos...');
      await new Promise(r => setTimeout(r, 20000));

      log('📸 Tirand o screenshot...');
      await page.screenshot({ path: 'DEBUG_POWERBI_ESTADO.png', fullPage: true });

      // Extrair TODO o conteúdo da página
      log('📊 Extraindo conteúdo completo...');

      const pageData = await page.evaluate(() => {
        return {
          title: document.title,
          bodyText: document.body.innerText,
          allElements: Array.from(document.querySelectorAll('*')).map(el => ({
            tag: el.tagName,
            text: (el.innerText || el.textContent || '').substring(0, 100),
            classes: el.className,
            id: el.id,
            visible: el.offsetHeight > 0
          })).filter(el => el.text && el.text.length > 3 && el.visible).slice(0, 50)
        };
      });

      log(`✅ Título: ${pageData.title}`);
      log(`✅ ${pageData.allElements.length} elementos com texto encontrados`);

      // Salvar página HTML
      const pageHTML = await page.content();
      fs.writeFileSync('DEBUG_POWERBI_HTML.html', pageHTML, 'utf-8');
      log('💾 DEBUG_POWERBI_HTML.html');

      // Processar linhas de texto
      const lines = pageData.bodyText.split('\n').filter(l => l.trim().length > 0).slice(0, 200);
      
      log('');
      log('📋 Primeiras 50 linhas da página:');
      for (let i = 0; i < Math.min(lines.length, 50); i++) {
        log(`   ${i + 1}. ${lines[i].substring(0, 80)}`);
      }

      // Salvar dados
      const output = {
        timestamp: new Date().toISOString(),
        title: pageData.title,
        total_lines: lines.length,
        first_50_lines: lines.slice(0, 50),
        elements_found: pageData.allElements.length,
        elements_sample: pageData.allElements.slice(0, 20)
      };

      fs.writeFileSync('DEBUG_POWERBI_CONTENT.json', JSON.stringify(output, null, 2), 'utf-8');
      log('💾 DEBUG_POWERBI_CONTENT.json');

    } catch (err) {
      log(`❌ ERRO: ${err.message}`);
    } finally {
      if (browser) {
        await browser.close();
      }

      fs.writeFileSync('DEBUG_POWERBI_EXTRACTION.log', logs.join('\n'), 'utf-8');

      log('');
      log('✅ CONCLUÍDO');
      log('');
    }
  }
}

new PowerBICategoryExtractor().run();
