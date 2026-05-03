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
      this.log('🎯 POWER BI IFRAME - EXTRAÇÃO DE TOKEN E DADOS');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');

      // Iniciar navegador
      this.log('🚀 Iniciando navegador...');
      browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: ['--no-sandbox', '--disable-blink-features=AutomationControlled']
      });

      page = await browser.newPage();
      page.on('error', () => {});

      // Navegar com timeout curto
      this.log('📍 Navegando para ANPG (30s timeout)...');
      let pageLoaded = true;
      
      try {
        await Promise.race([
          page.goto('https://anpg.co.ao/conteudo-local/', {
            waitUntil: 'domcontentloaded',
            timeout: 30000
          }),
          new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Navigation timeout')), 35000)
          )
        ]);
        this.log('✅ Página carregada');
      } catch (e) {
        this.log(`⚠️ Timeout na navegação: ${e.message}`);
        pageLoaded = false;
      }

      // Aguardar um pouco
      await new Promise(resolve => setTimeout(resolve, 3000));

      // Extrair informações do iframe DIRETAMENTE DO HTML
      this.log('🔍 Procurando iframe do Power BI no HTML...');

      const htmlContent = await page.content();
      
      // Procurar string powerbi.com no HTML
      const powerbiMatches = htmlContent.match(/src="(https:\/\/app\.powerbi\.com[^"]*)/g);
      
      if (powerbiMatches && powerbiMatches.length > 0) {
        for (const match of powerbiMatches) {
          const src = match.replace('src="', '');
          
          this.log('✅ iframe Power BI encontrado!');
          this.log(`📍 URL: ${src}`);
          this.log('');

          // Extrair parâmetro r
          const urlObj = new URL(src);
          const rParam = urlObj.searchParams.get('r');
          
          if (rParam) {
            this.log('🔑 Decodificando token...');
            
            const decoded = this.decodeBase64Url(rParam);
            
            if (decoded) {
              this.log('✅ Token decodificado!');
              this.log('');
              this.log('📊 INFORMAÇÕES DO RELATÓRIO POWER BI:');
              this.log('');
              
              try {
                const tokenData = JSON.parse(decoded);
                
                this.log(`🆔 Report ID: ${tokenData.r || 'N/A'}`);
                this.log(`🏢 Workspace ID: ${tokenData.w || 'N/A'}`);
                this.log(`⚙️  Config: ${tokenData.c || 'N/A'}`);
                this.log('');
                
                // Salvar em JSON
                const output = {
                  timestamp: new Date().toISOString(),
                  iframe_url: src,
                  url_base: 'https://app.powerbi.com/view',
                  token_parameters: {
                    r_encoded: rParam
                  },
                  report_info: tokenData,
                  decode_attempt: {
                    success: true,
                    data: tokenData
                  },
                  api_endpoints: {
                    report_details: `https://api.powerbi.com/v1.0/myorg/reports/${tokenData.r}`,
                    workspace_datasets: `https://api.powerbi.com/v1.0/myorg/groups/${tokenData.w}/datasets`,
                    note: 'Requer autenticação via Azure AD e token de acesso'
                  },
                  access_instructions: [
                    '1. Para acessar via API, você precisa:',
                    '   - Registrar um App no Azure AD',
                    '   - Obter um token de acesso',
                    '   - Ter permissões no workspace Power BI',
                    '',
                    '2. Usar endpoints acima com header: Authorization: Bearer {token}',
                    '',
                    '3. Alternativa: Usar Power BI REST API ou Power Query'
                  ]
                };
                
                fs.writeFileSync('POWERBI_DECODE_RESULT.json', JSON.stringify(output, null, 2), 'utf-8');
                this.log('💾 Resultado salvo: POWERBI_DECODE_RESULT.json');
                this.log('');
              } catch (parseErr) {
                this.log(`⚠️ Erro ao fazer parse JSON: ${parseErr.message}`);
                
                // Salvar mesmo assim
                fs.writeFileSync('POWERBI_DECODE_RESULT.json', JSON.stringify({
                  timestamp: new Date().toISOString(),
                  iframe_url: src,
                  token_encoded: rParam,
                  token_decoded_raw: decoded,
                  parse_error: parseErr.message
                }, null, 2), 'utf-8');
              }
            } else {
              this.log('⚠️ Não foi possível decodificar o token');
            }
          } else {
            this.log('⚠️ Parâmetro r não encontrado na URL');
          }
        }
      } else {
        this.log('⚠️ Nenhum iframe Power BI encontrado no HTML');
        
        // Procurar qualquer iframe
        const iframeMatches = htmlContent.match(/<iframe[^>]*src="([^"]*)"[^>]*>/g);
        if (iframeMatches && iframeMatches.length > 0) {
          this.log(`ℹ️  Total de iframes na página: ${iframeMatches.length}`);
          this.log('Iframes encontrados:');
          for (let i = 0; i < Math.min(iframeMatches.length, 5); i++) {
            const srcMatch = iframeMatches[i].match(/src="([^"]*)"/);
            if (srcMatch) {
              const url = srcMatch[1];
              this.log(`  ${i + 1}. ${url.substring(0, 80)}...`);
            }
          }
        }
      }

    } catch (err) {
      this.log(`❌ ERRO GERAL: ${err.message}`);
      this.log(err.stack);
    } finally {
      if (browser) {
        await browser.close();
        this.log('');
        this.log('✅ Navegador encerrado');
      }
      
      // Salvar log
      fs.writeFileSync('POWERBI_EXTRACTION.log', this.logs.join('\n'), 'utf-8');
      
      this.log('');
      this.log('═════════════════════════════════════════════════════════');
      this.log('✅ PROCESSO CONCLUSÃO');
      this.log('═════════════════════════════════════════════════════════');
      this.log('');
    }
  }
}

new PowerBIExtractor().run();
