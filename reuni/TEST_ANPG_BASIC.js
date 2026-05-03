const puppeteer = require('puppeteer');

async function testANPG() {
  console.log('🧪 TESTING ANPG WEBSITE ACCESS\n');

  let browser;
  try {
    console.log('🚀 Launching browser...');
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    console.log('📄 Created new page');

    console.log('📍 Navigating to ANPG...');
    await page.goto('https://anpg.co.ao/conteudo-local/', {
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });
    console.log('✅ Page loaded');

    // Get basic page info
    const title = await page.title();
    console.log(`📋 Page title: ${title}`);

    const url = page.url();
    console.log(`🔗 Current URL: ${url}`);

    // Check for Power BI content
    const hasPowerBI = await page.evaluate(() => {
      const bodyText = document.body.innerText;
      const hasIframe = document.querySelector('iframe') !== null;
      const hasPowerBI = bodyText.includes('Power BI') || bodyText.includes('powerbi');
      const hasTree = document.querySelector('[role="treeitem"]') !== null;

      return {
        bodyLength: bodyText.length,
        hasIframe,
        hasPowerBI,
        hasTree,
        firstFewLines: bodyText.split('\n').slice(0, 5).join('\n')
      };
    });

    console.log('📊 Page analysis:');
    console.log(`   - Body text length: ${hasPowerBI.bodyLength} characters`);
    console.log(`   - Has iframe: ${hasPowerBI.hasIframe}`);
    console.log(`   - Has Power BI text: ${hasPowerBI.hasPowerBI}`);
    console.log(`   - Has tree items: ${hasPowerBI.hasTree}`);

    console.log('\n📝 First few lines of content:');
    console.log(hasPowerBI.firstFewLines);

    // Try to find any expandable content
    const expandableElements = await page.evaluate(() => {
      const selectors = [
        '[aria-expanded]',
        '[role="treeitem"]',
        '.pvExplorerTreeItem',
        'button',
        '[class*="expand"]'
      ];

      const results = {};
      selectors.forEach(selector => {
        const count = document.querySelectorAll(selector).length;
        if (count > 0) {
          results[selector] = count;
        }
      });

      return results;
    });

    console.log('\n🔍 Expandable elements found:');
    Object.entries(expandableElements).forEach(([selector, count]) => {
      console.log(`   ${selector}: ${count} elements`);
    });

    console.log('\n✅ Test completed successfully!');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 Browser closed');
    }
  }
}

testANPG();