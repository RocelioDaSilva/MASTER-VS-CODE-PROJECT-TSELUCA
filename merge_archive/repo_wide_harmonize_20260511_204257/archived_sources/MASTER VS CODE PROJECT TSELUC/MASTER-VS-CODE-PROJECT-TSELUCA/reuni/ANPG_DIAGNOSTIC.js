const puppeteer = require('puppeteer');
const fs = require('fs');

async function diagnoseANPG() {
  console.log('🔍 ANPG WEBSITE DIAGNOSTIC\n');

  let browser;
  try {
    console.log('1. Testing Puppeteer launch...');
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
      timeout: 10000
    });
    console.log('✅ Puppeteer launched successfully');

    const page = await browser.newPage();
    console.log('✅ Page created');

    console.log('2. Testing basic navigation...');
    const response = await page.goto('https://anpg.co.ao', {
      waitUntil: 'domcontentloaded',
      timeout: 15000
    });

    console.log(`✅ Navigation successful - Status: ${response.status()}`);
    console.log(`   URL: ${page.url()}`);
    console.log(`   Title: ${await page.title()}`);

    console.log('3. Testing conteudo-local page...');
    await page.goto('https://anpg.co.ao/conteudo-local/', {
      waitUntil: 'domcontentloaded',
      timeout: 15000
    });

    console.log(`✅ Conteudo-local loaded - Status: ${response.status()}`);
    console.log(`   URL: ${page.url()}`);
    console.log(`   Title: ${await page.title()}`);

    console.log('4. Analyzing page content...');
    const analysis = await page.evaluate(() => {
      return {
        bodyTextLength: document.body.innerText.length,
        hasIframe: document.querySelector('iframe') !== null,
        iframes: Array.from(document.querySelectorAll('iframe')).map(ifr => ({
          src: ifr.src,
          width: ifr.width,
          height: ifr.height
        })),
        powerBIIndicators: {
          hasPowerBIText: document.body.innerText.includes('Power BI'),
          hasPowerBIClass: document.querySelector('[class*="powerbi"]') !== null,
          hasDataBI: document.querySelector('[data-bi]') !== null
        },
        interactiveElements: {
          buttons: document.querySelectorAll('button').length,
          links: document.querySelectorAll('a').length,
          treeItems: document.querySelectorAll('[role="treeitem"]').length,
          expandables: document.querySelectorAll('[aria-expanded]').length
        },
        firstLines: document.body.innerText.split('\n').slice(0, 10).filter(line => line.trim())
      };
    });

    console.log('📊 CONTENT ANALYSIS:');
    console.log(`   - Body text length: ${analysis.bodyTextLength} characters`);
    console.log(`   - Has iframe: ${analysis.hasIframe}`);
    console.log(`   - Iframes found: ${analysis.iframes.length}`);
    console.log(`   - Power BI indicators: ${JSON.stringify(analysis.powerBIIndicators, null, 2)}`);
    console.log(`   - Interactive elements: ${JSON.stringify(analysis.interactiveElements, null, 2)}`);

    console.log('\n📝 FIRST LINES OF CONTENT:');
    analysis.firstLines.forEach((line, i) => {
      console.log(`   ${i + 1}. ${line.substring(0, 80)}${line.length > 80 ? '...' : ''}`);
    });

    // Save detailed analysis
    fs.writeFileSync('anpg_diagnostic.json', JSON.stringify({
      timestamp: new Date().toISOString(),
      analysis: analysis,
      pageInfo: {
        url: page.url(),
        title: await page.title()
      }
    }, null, 2));

    console.log('\n💾 Detailed analysis saved to anpg_diagnostic.json');

    // Take screenshot
    await page.screenshot({ path: 'anpg_diagnostic.png', fullPage: true });
    console.log('📸 Screenshot saved to anpg_diagnostic.png');

    console.log('\n✅ DIAGNOSTIC COMPLETED SUCCESSFULLY');

  } catch (error) {
    console.error('❌ DIAGNOSTIC FAILED:', error.message);

    // Save error info
    fs.writeFileSync('anpg_diagnostic_error.json', JSON.stringify({
      timestamp: new Date().toISOString(),
      error: error.message,
      stack: error.stack
    }, null, 2));

  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 Browser closed');
    }
  }
}

diagnoseANPG();