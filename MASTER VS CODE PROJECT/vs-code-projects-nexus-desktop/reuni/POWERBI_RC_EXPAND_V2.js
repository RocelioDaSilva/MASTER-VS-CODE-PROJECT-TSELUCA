const puppeteer = require('puppeteer');
const fs = require('fs');

class PowerBIRightClickExpandV2 {
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
      this.log('🎯 POWER BI - RIGHT CLICK EXPAND V2 (COM DEBUG)');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');

      browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: ['--no-sandbox']
      });

      page = await browser.newPage();
      page.on('error', () => {});

      this.log('📍 Navegando para Power BI...');
      try {
        await page.goto(this.embedUrl, {
          waitUntil: 'domcontentloaded',
          timeout: 40000
        }).catch(() => {});
      } catch (e) {
        this.log(`⚠️  ${e.message}`);
      }

      this.log('⏳ Aguardando carregamento (15 segundos)...');
      await new Promise(r => setTimeout(r, 15000));

      // Screenshot 1: Estado inicial
      this.log('📸 Screenshot 1: Estado inicial');
      await page.screenshot({ path: 'S1_Estado_Inicial.png', fullPage: true });

      // Verificar elementos na página
      this.log('🔍 Analisando elementos na página...');
      const allElements = await page.evaluate(() => {
        const elements = [];
        const allEls = document.querySelectorAll('*');
        
        for (const el of allEls) {
          const text = (el.innerText || el.textContent || '').trim();
          
          // Procurar por "Consultoria"
          if (text.toLowerCase().includes('consultoria')) {
            elements.push({
              tag: el.tagName,
              text: text.substring(0, 100),
              classes: el.className,
              id: el.id,
              visible: el.offsetHeight > 0
            });
          }
        }
        
        return elements;
      });

      this.log(`✅ ${allElements.length} elementos com "consultoria" encontrados`);
      
      if (allElements.length > 0) {
        for (let i = 0; i < Math.min(allElements.length, 5); i++) {
          this.log(`   ${i + 1}. Tag:${allElements[i].tag} | Text:"${allElements[i].text}" | Visible:${allElements[i].visible}`);
        }
      }

      // Tentar hover + right-click
      if (allElements.length > 0 && allElements[0].visible) {
        this.log('');
        this.log('🖱️ Tentando hover + right-click no primeiro elemento...');

        await page.evaluate(() => {
          const elements = document.querySelectorAll('*');
          for (const el of elements) {
            const text = (el.innerText || el.textContent || '').toLowerCase();
            if (text.includes('consultoria')) {
              
              // Hover
              const hoverEvent = new MouseEvent('mouseover', {
                bubbles: true,
                cancelable: true,
                view: window
              });
              el.dispatchEvent(hoverEvent);

              // Right-click
              const contextEvent = new MouseEvent('contextmenu', {
                bubbles: true,
                cancelable: true,
                view: window,
                button: 2,
                buttons: 2
              });
              el.dispatchEvent(contextEvent);

              return true;
            }
          }
          return false;
        });

        this.log('✅ Context menu triggered');

        // Screenshot 2: Com context menu
        this.log('⏳ Aguardando context menu aparecer (3s)...');
        await new Promise(r => setTimeout(r, 3000));

        this.log('📸 Screenshot 2: Context menu');
        await page.screenshot({ path: 'S2_Context_Menu.png', fullPage: true });

        // Procurar opções no context menu
        const menuOptions = await page.evaluate(() => {
          const options = [];
          
          // Procurar por elementos visíveis com texto relevante
          const allEls = document.querySelectorAll('*');
          for (const el of allEls) {
            if (el.offsetHeight === 0) continue; // Invisível
            
            const text = (el.innerText || el.textContent || '').trim();
            
            // Palavras-chave para expandir
            const keywords = ['expand', 'expandir', 'drill', 'drill down', 'drill through', 'tudo', 'all'];
            if (keywords.some(kw => text.toLowerCase().includes(kw)) && text.length < 50) {
              options.push({
                text: text,
                tag: el.tagName,
                classes: el.className,
                clickable: el.onclick || el.tagName === 'BUTTON'
              });
            }
          }
          
          return options;
        });

        this.log(`✅ ${menuOptions.length} opções encontradas`);
        
        if (menuOptions.length > 0) {
          for (let i = 0; i < Math.min(menuOptions.length, 10); i++) {
            this.log(`   ${i + 1}. "${menuOptions[i].text}" (${menuOptions[i].tag})`);
          }

          // Clicar na primeira opção com "expand"
          const expandOption = menuOptions.find(opt => opt.text.toLowerCase().includes('expand'));
          
          if (expandOption) {
            this.log('');
            this.log(`🖱️ Clicando em: "${expandOption.text}"`);

            await page.evaluate((optText) => {
              const elements = document.querySelectorAll('*');
              for (const el of elements) {
                const text = (el.innerText || el.textContent || '').trim();
                if (text === optText) {
                  el.click();
                  return;
                }
              }
            }, expandOption.text);

            this.log('⏳ Aguardando expansão (12 segundos)...');
            await new Promise(r => setTimeout(r, 12000));

            // Screenshot 3: Após expandir
            this.log('📸 Screenshot 3: Após expandir');
            await page.screenshot({ path: 'S3_Apos_Expandir.png', fullPage: true });

            // Extrair dados
            this.log('📊 Extraindo dados após expansão...');
            
            const extractedData = await page.evaluate(() => {
              const allText = document.body.innerText;
              const lines = allText.split('\n')
                .filter(l => l.trim().length > 2)
                .filter(l => !l.toLowerCase().match(/keyboard|shortcut|navigation|menu|filter|expand|collapse|page|loading/));
              
              return {
                total_lines: lines.length,
                first_100: lines.slice(0, 100)
              };
            });

            this.log(`✅ ${extractedData.total_lines} linhas de dados encontradas`);
            this.log(`✅ ${extractedData.first_100.length} primeiras linhas capturadas`);

            // Salvar
            for (const item of extractedData.first_100) {
              this.companies.add(item);
            }

          } else {
            this.log('⚠️  Opção "expand" não encontrada');
          }
        } else {
          this.log('⚠️  Nenhuma opção de context menu encontrada');
        }
      } else {
        this.log('⚠️  Elemento consultoria não visível ou não encontrado');
      }

      // Salvar resultados
      this.log('');
      this.log('💾 Salvando resultados...');

      const json_out = {
        timestamp: new Date().toISOString(),
        companies_found: this.companies.size,
        companies: Array.from(this.companies),
        debug_info: {
          elements_found_with_consultoria: allElements.length,
          screenshots_saved: ['S1_Estado_Inicial.png', 'S2_Context_Menu.png', 'S3_Apos_Expandir.png']
        }
      };

      fs.writeFileSync('POWERBI_CONSULTORIA_V2.json', JSON.stringify(json_out, null, 2), 'utf-8');
      this.log('✅ POWERBI_CONSULTORIA_V2.json');

      if (this.companies.size > 0) {
        let csv = 'numero;empresa_item;categoria;data;hora;fonte\n';
        let num = 1;
        for (const company of this.companies) {
          const date = new Date().toLocaleDateString('pt-BR');
          const time = new Date().toLocaleTimeString('pt-BR');
          csv += `${num};"${company}";"Consultoria, Assessoria e Auditoria";${date};${time};POWERBI_RC_EXPAND_V2\n`;
          num++;
        }
        fs.writeFileSync('POWERBI_CONSULTORIA_V2.csv', csv, 'utf-8');
        this.log(`✅ POWERBI_CONSULTORIA_V2.csv (${this.companies.size} items)`);
      }

    } catch (err) {
      this.log(`❌ ERRO: ${err.message}`);
    } finally {
      if (browser) {
        await browser.close();
      }

      fs.writeFileSync('POWERBI_RC_EXPAND_V2.log', this.logs.join('\n'), 'utf-8');

      this.log('');
      this.log('═════════════════════════════════════════════════════════');
      this.log('✅ PROCESSO CONCLUÍDO');
      this.log('═════════════════════════════════════════════════════════');
    }
  }
}

new PowerBIRightClickExpandV2().run();
