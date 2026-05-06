const puppeteer = require('puppeteer');
const fs = require('fs');
const http = require('http');
const path = require('path');

let capturedCompanies = [];

async function startManualCopying() {
  console.log('═══════════════════════════════════════════════════════');
  console.log('📋 ANPG - MANUAL COMPANY COPYING VIA CONTEXT MENUS');
  console.log('═══════════════════════════════════════════════════════\n');

  console.log('INSTRUÇÕES:');
  console.log('1. O navegador vai abrir na página ANPG');
  console.log('2. Expanda as categorias');
  console.log('3. Faça RIGHT-CLICK nos nomes das empresas');
  console.log('4. Selecione "Copiar" do menu');
  console.log('5. Cole aqui ou use a pasta especial criada\n');

  let browser;

  try {
    // Launch browser with visible interface
    console.log('🚀 Abrindo navegador ANPG...\n');
    browser = await puppeteer.launch({
      headless: false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--disable-web-security'
      ]
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    // Add clipboard monitoring
    console.log('⏳ Navegando para ANPG...');
    await page.goto('https://anpg.co.ao/conteudo-local/', {
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });

    console.log('✅ Página carregada!');
    console.log('\n'.repeat(2));
    console.log('╔═══════════════════════════════════════════════════════╗');
    console.log('║  📍 BROWSER ABERTO - FAÇA RIGHT-CLICK NAS EMPRESAS   ║');
    console.log('║  ⏳ Aguardando suas ações...                          ║');
    console.log('║  (Este script ficará rodando enquanto você trabalha)  ║');
    console.log('╚═══════════════════════════════════════════════════════╝');
    console.log('\n');

    // Keep browser open indefinitely while user copies
    console.log('💡 Dicas:');
    console.log('   • Clique na seta "+" para expandir categorias');
    console.log('   • Localize o nome da empresa');
    console.log('   • Faça RIGHT-CLICK no nome');
    console.log('   • Selecione "Copiar" (Copy)\n');

    console.log('Pressione Ctrl+C aqui quando terminar de copiar as empresas...\n');

    // Inject a helper script to capture clipboard changes
    await page.evaluateOnNewDocument(() => {
      window.copiedCompanies = [];

      // Override copy to capture what was copied
      document.addEventListener('copy', (event) => {
        const text = event.clipboardData.getData('text/plain');
        if (text && text.length < 200) {
          window.copiedCompanies.push(text);
          console.log('✅ CAPTURADO:', text);
        }
      });

      // Allow manual right-click menu
      document.addEventListener('contextmenu', (event) => {
        // Don't prevent - let user see context menu
      });
    });

    // Every 5 seconds, check if there are copied companies
    const captureInterval = setInterval(async () => {
      try {
        const companies = await page.evaluate(() => window.copiedCompanies || []);
        if (companies.length > capturedCompanies.length) {
          const newCompanies = companies.slice(capturedCompanies.length);
          capturedCompanies = companies;

          newCompanies.forEach(company => {
            console.log(`🎯 Empresa capturada: ${company}`);
          });

          // Save progressively
          saveProgress();
        }
      } catch (e) {
        // Page might be closed
      }
    }, 2000);

    // Wait indefinitely (user closes with Ctrl+C)
    await new Promise(() => {});

  } catch (error) {
    console.error('❌ Erro:', error.message);
  } finally {
    console.log('\n\n🧹 Encerrando...');
    if (browser) {
      await browser.close();
    }

    // Final save
    saveProgress();
    console.log('✅ Concluído!');
  }
}

function saveProgress() {
  if (capturedCompanies.length === 0) return;

  const timestamp = new Date().toISOString().split('T')[0];
  const csvFile = `EMPRESAS_COPIADAS_${timestamp}.csv`;

  // Deduplicate
  const unique = [...new Set(capturedCompanies)];

  // Save CSV
  let csv = 'nome_empresa;data_captura\n';
  unique.forEach(company => {
    csv += `"${company.replace(/"/g, '""')}";${timestamp}\n`;
  });

  fs.writeFileSync(csvFile, csv);
  console.log(`💾 ${csvFile} - ${unique.length} empresas`);

  // Save JSON
  const jsonFile = csvFile.replace('.csv', '.json');
  fs.writeFileSync(jsonFile, JSON.stringify({
    timestamp: new Date().toISOString(),
    total: unique.length,
    companies: unique
  }, null, 2));
}

startManualCopying().catch(console.error);