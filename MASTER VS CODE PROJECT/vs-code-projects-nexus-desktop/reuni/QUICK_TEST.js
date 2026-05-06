const puppeteer = require('puppeteer');
const fs = require('fs');

async function quickTest() {
  console.log('QUICK ANPG TEST');

  let browser;
  try {
    browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage();

    console.log('Loading page...');
    await page.goto('https://anpg.co.ao/conteudo-local/', { waitUntil: 'domcontentloaded', timeout: 20000 });

    const info = await page.evaluate(() => ({
      title: document.title,
      url: window.location.href,
      bodyLength: document.body.innerText.length,
      hasIframe: !!document.querySelector('iframe'),
      hasPowerBI: document.body.innerText.includes('Power BI'),
      elements: {
        treeitems: document.querySelectorAll('[role="treeitem"]').length,
        buttons: document.querySelectorAll('button').length,
        expandables: document.querySelectorAll('[aria-expanded]').length
      }
    }));

    console.log('RESULTS:');
    console.log('- Title:', info.title);
    console.log('- URL:', info.url);
    console.log('- Body length:', info.bodyLength);
    console.log('- Has iframe:', info.hasIframe);
    console.log('- Has Power BI:', info.hasPowerBI);
    console.log('- Tree items:', info.elements.treeitems);
    console.log('- Buttons:', info.elements.buttons);
    console.log('- Expandables:', info.elements.expandables);

    // Save to file
    fs.writeFileSync('quick_test_results.json', JSON.stringify(info, null, 2));
    console.log('Results saved to quick_test_results.json');

  } catch (error) {
    console.error('ERROR:', error.message);
    fs.writeFileSync('quick_test_error.txt', error.message);
  } finally {
    if (browser) await browser.close();
  }
}

quickTest();