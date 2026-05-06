const puppeteer = require('puppeteer');
const fs = require('fs');

async function extractCompanies() {
  const logs = [];

  function logMessage(message) {
    const timestamp = new Date().toLocaleTimeString();
    const fullMsg = `[${timestamp}] ${message}`;
    console.log(fullMsg);
    logs.push(fullMsg);
  }

  try {
    logMessage('═══════════════════════════════════════════════════════');
    logMessage('🎯 ANPG EXTRACTION - STEP BY STEP');
    logMessage('═══════════════════════════════════════════════════════');

    logMessage('\n[INIT] Loading Puppeteer');
    const browser = await puppeteer.launch({
      headless: false,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });
    logMessage('[INIT] ✅ Browser ready');

    // STEP 1
    logMessage('\n[STEP 1] Navigate to https://anpg.co.ao/conteudo-local/');
    try {
      const response = await page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'domcontentloaded',
        timeout: 45000
      });
      logMessage(`[STEP 1] ✅ Page loaded (Status: ${response.status()})`);
    } catch (e) {
      logMessage(`[STEP 1] ⚠️  Timeout - continuing anyway`);
      await new Promise(r => setTimeout(r, 3000));
    }

    // STEP 2
    logMessage('\n[STEP 2] Wait for Power BI to load');
    logMessage('[STEP 2] ⏳ Waiting for content...');
    try {
      await page.waitForFunction(() => {
        return document.body.innerText.length > 300;
      }, { timeout: 30000 });
      logMessage('[STEP 2] ✅ Content found');
    } catch (e) {
      logMessage('[STEP 2] ⚠️  Content check timeout');
    }

    logMessage('[STEP 2] ⏳ Waiting 10 seconds for layout stabilization');
    await new Promise(r => setTimeout(r, 10000));
    logMessage('[STEP 2] ✅ Ready');

    // STEP 3
    logMessage('\n[STEP 3] Click expand icons next to categories');
    const iconClicks = await page.evaluate(() => {
      let count = 0;
      // Find and click expand icons
      const elements = document.querySelectorAll('[aria-expanded="false"], .pvExplorerTreeItemIconContainer, [class*="expander"]');
      for (let i = 0; i < Math.min(elements.length, 20); i++) {
        try {
          elements[i].click();
          count++;
        } catch (e) {}
      }
      return count;
    });

    logMessage(`[STEP 3] ✅ Clicked ${iconClicks} expand icons`);
    logMessage('[STEP 3] ⏳ Waiting for expansion');
    await new Promise(r => setTimeout(r, 5000));

    // STEP 4
    logMessage('\n[STEP 4] Right-click tree items and select Expand');
    const rightClicks = await page.evaluate(() => {
      let count = 0;
      const items = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem');
      for (let i = 0; i < Math.min(items.length, 10); i++) {
        try {
          const event = new MouseEvent('contextmenu', { bubbles: true, button: 2 });
          items[i].dispatchEvent(event);
          count++;
        } catch (e) {}
      }
      return count;
    });

    logMessage(`[STEP 4] ✅ Right-clicked ${rightClicks} items`);
    logMessage('[STEP 4] ⏳ Waiting for menus');
    await new Promise(r => setTimeout(r, 3000));

    // STEP 5
    logMessage('\n[STEP 5] Extract all visible company names');
    const allText = await page.evaluate(() => {
      const items = [];
      const seen = new Set();

      // Get all text from all elements
      document.querySelectorAll('*').forEach(el => {
        const text = el.innerText?.trim() || el.textContent?.trim();
        if (text && text.length > 5 && text.length < 250 && !seen.has(text)) {
          const lower = text.toLowerCase();
          // Skip UI elements
          if (!lower.includes('anpg') &&
              !lower.includes('sobre') &&
              !lower.includes('procurar') &&
              !lower.includes('decree') &&
              !lower.includes('lei')) {
            seen.add(text);
            items.push(text);
          }
        }
      });

      return items;
    });

    logMessage(`[STEP 5] ✅ Extracted ${allText.length} items`);
    logMessage('[STEP 5] 📋 First 10 items:');
    allText.slice(0, 10).forEach((item, i) => {
      logMessage(`        ${i+1}. ${item.substring(0, 70)}`);
    });

    // SAVE
    logMessage('\n[SAVE] 💾 Saving to CSV and JSON');
    const timestamp = new Date().toISOString().split('T')[0];
    const csvFile = `ANPG_COMPANIES_${timestamp}.csv`;
    const jsonFile = `ANPG_COMPANIES_${timestamp}.json`;

    // Create CSV
    let csvContent = 'company_name\n';
    allText.forEach(name => {
      csvContent += `"${name.replace(/"/g, '""')}"\n`;
    });

    fs.writeFileSync(csvFile, csvContent);
    logMessage(`[SAVE] ✅ CSV: ${csvFile} (${allText.length} items)`);

    // Create JSON
    const jsonData = {
      timestamp: new Date().toISOString(),
      totalItems: allText.length,
      companies: allText,
      executionLog: logs
    };

    fs.writeFileSync(jsonFile, JSON.stringify(jsonData, null, 2));
    logMessage(`[SAVE] ✅ JSON: ${jsonFile}`);

    // CLEANUP
    logMessage('\n[CLEANUP] Closing browser');
    await browser.close();
    logMessage('[CLEANUP] ✅ Done');

    // Final summary
    logMessage('\n═══════════════════════════════════════════════════════');
    logMessage('✅ SUCCESS');
    logMessage('═══════════════════════════════════════════════════════');
    logMessage(`Total companies extracted: ${allText.length}`);
    logMessage(`Output files: ${csvFile}, ${jsonFile}`);

  } catch (error) {
    logMessage(`\n❌ ERROR: ${error.message}`);
    logMessage(error.stack);
  } finally {
    // Save execution log
    const logFile = 'ANPG_EXECUTION_LOG.txt';
    fs.writeFileSync(logFile, logs.join('\n'));
    logMessage(`\n📝 Full log saved to: ${logFile}`);
  }
}

extractCompanies().catch(error => {
  console.error('FATAL:', error);
  const logFile = 'ANPG_EXECUTION_ERROR.txt';
  fs.writeFileSync(logFile, error.toString() + '\n' + error.stack);
});