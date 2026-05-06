const puppeteer = require('puppeteer');
const fs = require('fs');

class PowerBIExtractor {
  constructor() {
    this.logs = [];
  }

  log(msg) {
    const t = new Date().toLocaleTimeString('pt-BR');
    console.log(`[${t}] ${msg}`);
    this.logs.push(`[${t}] ${msg}`);
  }

  decodeBase64Url(str) {
    try {
      // Adicionar padding se necessário
      let base64 = str.replace(/-/g, '+').replace(/_/g, '/');
      while (base64.length % 4) base64 += '=';
      return Buffer.from(base64, 'base64').toString('utf-8');
    } catch (e) {
      return null;
    }
  }

  async run() {
    let browser, page;
    try {
      this.log('');
      this.log('═════════════════════════════════════════════════════════');
      this.log('🎯 POWER BI IFRAME - EXTRAÇÃO DE DADOS');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');

      // Iniciar navegador
      this.log('🚀 Iniciando navegador...');
      browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: ['--no-sandbox']
      });

      page = await browser.newPage();
      page.on('error', () => {});

      // Navegar
      this.log('📍 Navegando para ANPG...');
      await page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'networkidle2',
        timeout: 60000
      }).catch(() => this.log('⚠️ Timeout (continuando...)'));

      this.log('⏳ Aguardando Power BI carregar (10 segundos)...');
      await new Promise(resolve => setTimeout(resolve, 10000));

      // Extrair informações do iframe
      this.log('🔍 Procurando iframe do Power BI...');

      const iframeInfo = await page.evaluate(() => {
        // Procurar iframe com powerbi.com
        const iframes = document.querySelectorAll('iframe');
        
        for (const iframe of iframes) {
          const src = iframe.getAttribute('src') || '';
          const title = iframe.getAttribute('title') || '';
          
          if (src.includes('powerbi.com')) {
            return {
              title: title,
              src: src,
              width: iframe.getAttribute('width'),
              height: iframe.getAttribute('height'),
              allowfullscreen: iframe.getAttribute('allowfullscreen')
            };
          }
        }
        
        // Se não encontrar, retornar todos os iframes
        const allIframes = [];
        for (const iframe of iframes) {
          allIframes.push({
            src: iframe.getAttribute('src'),
            title: iframe.getAttribute('title')
          });
        }
        
        return { error: 'Power BI iframe not found', all_iframes: allIframes };
      });

      if (iframeInfo.error) {
        this.log(`⚠️ ${iframeInfo.error}`);
        this.log(`Total de iframes na página: ${iframeInfo.all_iframes.length}`);
        this.log('Iframes encontrados:');
        for (const iframe of iframeInfo.all_iframes) {
          this.log(`  • Title: ${iframe.title || 'N/A'}`);
          this.log(`    Src: ${iframe.src ? iframe.src.substring(0, 100) + '...' : 'N/A'}`);
        }
      } else {
        this.log('✅ iframe Power BI encontrado!');
        this.log(`   Title: ${iframeInfo.title}`);
        this.log(`   Width: ${iframeInfo.width}px | Height: ${iframeInfo.height}px`);
        this.log(`   AllowFullscreen: ${iframeInfo.allowfullscreen}`);
        this.log('');
        this.log(`📍 URL do iframe:`);
        this.log(`   ${iframeInfo.src}`);
        this.log('');

        // Decodificar parâmetro r
        const urlObj = new URL(iframeInfo.src);
        const rParam = urlObj.searchParams.get('r');
        
        if (rParam) {
          this.log('🔑 Decodificando token de acesso...');
          const decoded = this.decodeBase64Url(rParam);
          
          if (decoded) {
            this.log('✅ Token decodificado com sucesso!');
            this.log('');
            this.log('📊 Informações do Relatório Power BI:');
            
            try {
              const tokenData = JSON.parse(decoded);
              this.log(`   Report ID (r): ${tokenData.r || 'N/A'}`);
              this.log(`   Workspace ID (w): ${tokenData.w || 'N/A'}`);
              this.log(`   Config (c): ${tokenData.c || 'N/A'}`);
              this.log('');
              
              // Salvar informações decodificadas
              fs.writeFileSync('POWERBI_TOKEN_INFO.json', JSON.stringify({
                full_url: iframeInfo.src,
                url_base: 'https://app.powerbi.com/view',
                parameters: {
                  r_encoded: rParam,
                  r_decoded: tokenData
                },
                extracted_ids: {
                  report_id: tokenData.r,
                  workspace_id: tokenData.w,
                  config: tokenData.c
                },
                timestamp: new Date().toISOString(),
                notes: [
                  'Report ID pode ser usado com Power BI REST API',
                  'Requer autenticação com Azure AD',
                  'Para acessar dados, use: https://api.powerbi.com/v1.0/myorg/reports/{reportId}',
                  'Ou acesse via Power BI Service dashboard'
                ]
              }, null, 2), 'utf-8');
              
              this.log('✅ Informações salvas em: POWERBI_TOKEN_INFO.json');
            } catch (e) {
              this.log(`⚠️ Não foi possível fazer parse do JSON`);
            }
          } else {
            this.log('⚠️ Não foi possível decodificar o token');
          }
        }

        // Tentar acessar a URL do Power BI
        this.log('');
        this.log('🌐 Tentando acessar Power BI report...');
        
        try {
          const newPage = await browser.newPage();
          await newPage.goto(iframeInfo.src, {
            waitUntil: 'networkidle2',
            timeout: 30000
          }).catch(() => {
            this.log('⚠️ Timeout ao acessar - Page pode estar protegida');
          });

          await new Promise(resolve => setTimeout(resolve, 2000));

          // Tentar extrair conteúdo
          const reportContent = await newPage.evaluate(() => {
            const content = {
              title: document.title,
              text: document.body.innerText.substring(0, 1000),
              tables: document.querySelectorAll('table').length,
              data_elements: document.querySelectorAll('[data-type="Table"], [data-role="presentation"], .pivotTable').length
            };
            return content;
          }).catch(() => null);

          if (reportContent) {
            this.log('✅ Conteúdo do Power BI acessado:');
            this.log(`   Title: ${reportContent.title}`);
            this.log(`   Tables: ${reportContent.tables}`);
            this.log(`   Data Elements: ${reportContent.data_elements}`);
            
            if (reportContent.text.length > 0) {
              this.log('   Preview do conteúdo:');
              this.log(`   ${reportContent.text.substring(0, 200)}...`);
            }
          } else {
            this.log('⚠️ Conteúdo protegido ou não carregado');
          }

          await newPage.close();
        } catch (e) {
          this.log(`⚠️ Erro ao acessar: ${e.message}`);
        }
      }

      // Salvar log completo
      fs.writeFileSync('POWERBI_EXTRACTION_LOG.txt', this.logs.join('\n'), 'utf-8');
      this.log('');
      this.log('💾 Log completo salvo em: POWERBI_EXTRACTION_LOG.txt');

    } catch (err) {
      this.log(`❌ ERRO: ${err.message}`);
    } finally {
      if (browser) {
        await browser.close();
        this.log('✅ Navegador encerrado');
      }
      
      this.log('');
      this.log('═════════════════════════════════════════════════════════');
      this.log('✅ EXTRAÇÃO CONCLUSÃO');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');
    }
  }
}

new PowerBIExtractor().run();
