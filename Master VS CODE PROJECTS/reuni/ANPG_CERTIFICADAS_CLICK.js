const puppeteer = require('puppeteer');
const fs = require('fs');

class ANPGCompanyExtractor {
  constructor() {
    this.companies = new Set();
    this.logs = [];
  }

  log(msg) {
    const t = new Date().toLocaleTimeString('pt-BR');
    const line = `[${t}] ${msg}`;
    console.log(line);
    this.logs.push(line);
  }

  async run() {
    let browser, page;
    try {
      this.log('');
      this.log('═════════════════════════════════════════════');
      this.log('🎯 ANPG - EXTRAÇÃO DE EMPRESAS CERTIFICADAS');
      this.log('═════════════════════════════════════════════');
      this.log('');

      // Iniciar
      this.log('🚀 Iniciando navegador...');
      browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: ['--no-sandbox']
      });

      page = await browser.newPage();
      page.on('error', (e) => {});

      // Navegar
      this.log('📍 Navegando para ANPG (Conteúdo Local)...');
      await page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'networkidle2',
        timeout: 60000
      }).catch(() => this.log('⚠️ Timeout na navegação (continuando...)'));

      this.log('✅ Página carregada, aguardando 8 segundos...');
      await page.waitForTimeout(8000);

      // Procurar e clicar em "Empresas Certificadas"
      this.log('🔍 Procurando botão "Empresas Certificadas"...');
      
      const found = await page.evaluate(() => {
        // Procurar por links/botões com "Certificadas"
        const elements = Array.from(document.querySelectorAll('a, button, div[role="link"], span'));
        
        for (const el of elements) {
          const text = (el.innerText || el.textContent || '').toLowerCase();
          if (text.includes('certificad')) {
            return {
              found: true,
              text: el.innerText || el.textContent,
              selector: el.className
            };
          }
        }
        return { found: false };
      });

      if (found.found) {
        this.log(`✅ Encontrado: "${found.text}"`);
        
        // Clicar nele
        this.log('🖱️ Clicando em Empresas Certificadas...');
        await page.evaluate(() => {
          const elements = Array.from(document.querySelectorAll('a, button, div[role="link"], span'));
          for (const el of elements) {
            const text = (el.innerText || el.textContent || '').toLowerCase();
            if (text.includes('certificad')) {
              el.click();
              return;
            }
          }
        });

        this.log('⏳ Aguardando conteúdo carregar (15 segundos)...');
        await page.waitForTimeout(15000);
      } else {
        this.log('⚠️ Botão não encontrado, continuando com a página atual...');
        await page.waitForTimeout(5000);
      }

      // Expandir tudo
      this.log('📂 Expandindo todos os itens (5 tentativas)...');
      for (let i = 0; i < 5; i++) {
        const count = await page.evaluate(() => {
          let expanded = 0;

          // Todos os botões/elementos expandíveis
          const buttons = document.querySelectorAll('[aria-expanded="false"], button, div[role="button"]');
          for (const btn of buttons) {
            if (btn.offsetHeight > 0 && btn.offsetWidth > 0) {
              btn.click();
              expanded++;
            }
          }

          return expanded;
        });

        this.log(`  ✅ Tentativa ${i + 1}: ${count} elementos clicados`);
        await page.waitForTimeout(2000);
      }

      // Extrair empresas
      this.log('🔍 Extraindo nomes de empresas...');
      const extracted = await page.evaluate(() => {
        const companies = new Set();

        // Todas as linhas de texto
        const allText = document.body.innerText;
        const lines = allText.split('\n');

        for (const line of lines) {
          const cleaned = line.trim();
          
          // Filtros
          if (cleaned.length < 4 || cleaned.length > 120) continue;
          if (/^\d+$/.test(cleaned)) continue; // Número puro
          if (!/[A-Za-z]/.test(cleaned)) continue; // Sem letras
          
          // Filtrar UI
          const ui = ['Skip', 'Content', 'Sobre', 'nós', 'Oportunidades', 'Dados',
                      'Media', 'Produção', 'Conteúdo', 'Local', 'Procurar', 'DECRETO',
                      'REGISTO', 'Certificação', 'Empresas', 'Sector', 'Petrolífero',
                      'VER MAIS', 'Introdução', 'Regimes', 'Contratação', 'Ciclo',
                      'Lista', 'Bens', 'Serviços', 'Instrutivo', 'Manual', 'Fornecedor',
                      'Visitadas', 'História', 'Responsabilidade', 'Social', 'Contactos',
                      'Licitações', 'Permanente', 'Conferência', 'Power', 'BI', 'Loading',
                      'Expand', 'Collapse', 'Filter', 'Sort', 'Export', 'Home', 'Back',
                      'Menu', 'Help', 'Settings', 'Close', 'Open', 'Save', 'Cancel'];
          
          if (ui.some(word => cleaned.includes(word))) continue;

          // Aceitar
          companies.add(cleaned);
        }

        return Array.from(companies);
      });

      this.log(`✅ Extraídas ${extracted.length} linhas de texto`);
      
      for (const company of extracted) {
        this.companies.add(company);
      }

      // Screenshot
      this.log('📸 Capturando screenshot...');
      await page.screenshot({ path: 'anpg_empresas_certificadas.png', fullPage: true });
      this.log('✅ Screenshot salvo');

      // Salvar
      this.log('💾 Salvando resultados...');
      const date = new Date().toISOString().split('T')[0];
      const count = this.companies.size;

      // CSV
      const csv = `ANPG_CERTIFICADAS_${date}_${count}.csv`;
      let csvContent = 'numero;empresa;data;hora;fonte\n';
      let num = 1;
      for (const company of this.companies) {
        const hora = new Date().toLocaleTimeString('pt-BR');
        const data = new Date().toLocaleDateString('pt-BR');
        csvContent += `${num};${company};${data};${hora};ANPG_CERTIFICADAS\n`;
        num++;
      }
      fs.writeFileSync(csv, csvContent, 'utf-8');
      this.log(`✅ CSV: ${csv} (${count} empresas)`);

      // JSON
      const json = `ANPG_CERTIFICADAS_${date}_${count}.json`;
      fs.writeFileSync(json, JSON.stringify({
        count,
        date: new Date().toISOString(),
        companies: Array.from(this.companies).sort(),
        logs: this.logs
      }, null, 2), 'utf-8');
      this.log(`✅ JSON: ${json}`);

      this.log('');
      this.log('═════════════════════════════════════════════');
      this.log(`✅ SUCESSO! ${count} empresas extraídas`);
      this.log('═════════════════════════════════════════════');
      this.log('');

    } catch (err) {
      this.log(`❌ ERRO: ${err.message}`);
      this.log(err.stack);
    } finally {
      if (browser) {
        await browser.close();
        this.log('✅ Navegador encerrado');
      }
    }
  }
}

new ANPGCompanyExtractor().run();
