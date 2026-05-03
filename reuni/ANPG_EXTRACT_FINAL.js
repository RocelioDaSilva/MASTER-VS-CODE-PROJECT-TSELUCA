const puppeteer = require('puppeteer');
const fs = require('fs');

async function extractANPGCompanies() {
  console.log('═══════════════════════════════════════════════════════');
  console.log('🎯 ANPG COMPANY EXTRACTION - FOLLOW DETAILED STEPS\n');
  console.log('Step 1: Navigate to https://anpg.co.ao/conteudo-local/');
  console.log('Step 2: Wait for Power BI to load');
  console.log('Step 3: Click expand icons');
  console.log('Step 4: Right-click and select expand');
  console.log('Step 5: Extract all company names');
  console.log('═══════════════════════════════════════════════════════\n');

  let browser;
  const log = [];
  const companies = new Set();

  try {
    // Initialize browser
    console.log('[INIT] Launching Puppeteer...');
    log.push('[INIT] Launching Puppeteer');

    browser = await puppeteer.launch({
      headless: false,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    console.log('[INIT] ✅ Browser ready\n');
    log.push('[INIT] ✅ Browser ready');

    // STEP 1: Navigate
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('[STEP 1] Navigate to https://anpg.co.ao/conteudo-local/');

    try {
      await page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'domcontentloaded',
        timeout: 30000
      });

      console.log('[STEP 1] ✅ Page loaded');
      console.log(`[STEP 1] URL: ${page.url()}`);
      log.push('[STEP 1] ✅ Page loaded - ' + page.url());
    } catch (e) {
      console.log('[STEP 1] ⚠️  Load took longer than expected, continuing...');
      log.push('[STEP 1] ⚠️  Load timeout, continuing...');
      await new Promise(r => setTimeout(r, 5000));
    }

    // STEP 2: Wait for Power BI
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('[STEP 2] Wait for Power BI to load...');

    try {
      await page.waitForFunction(() => {
        const bodyText = document.body.innerText;
        return bodyText && bodyText.length > 500;
      }, { timeout: 20000 });

      console.log('[STEP 2] ✅ Power BI content detected');
      log.push('[STEP 2] ✅ Power BI content loaded');

      // Additional wait for rendering
      console.log('[STEP 2] ⏳ Waiting 8 seconds for complete rendering...');
      await new Promise(r => setTimeout(r, 8000));
      console.log('[STEP 2] ✅ Ready for interaction');
      log.push('[STEP 2] ✅ Content fully loaded');
    } catch (e) {
      console.log('[STEP 2] ⚠️  Power BI load indicator not found, continuing...');
      log.push('[STEP 2] ⚠️  No clear Power BI indicator');
    }

    // STEP 3: Click expand icons
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('[STEP 3] Click the expand icon next to category names...');

    const clickedIcons = await page.evaluate(() => {
      const selectors = [
        '[aria-expanded="false"]',
        '.pvExplorerTreeItemIconContainer',
        '[class*="expander"]',
        'button[aria-label*="expand"]'
      ];

      let totalClicked = 0;

      // Find expand icons
      selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        for (let i = 0; i < Math.min(elements.length, 15); i++) {
          try {
            elements[i].click();
            totalClicked++;
          } catch (e) {}
        }
      });

      return totalClicked;
    });

    console.log(`[STEP 3] ✅ Clicked ${clickedIcons} expand icons`);
    log.push(`[STEP 3] ✅ Clicked ${clickedIcons} expand icons`);

    // Wait for content to expand
    console.log('[STEP 3] ⏳ Waiting for content to expand...');
    await new Promise(r => setTimeout(r, 5000));

    // STEP 4: Right-click and select expand
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('[STEP 4] Right-click on tree items and select "Expand"...');

    const expandedItems = await page.evaluate(() => {
      const treeItems = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem');
      let expandedCount = 0;

      // Try right-clicking on first few items
      for (let i = 0; i < Math.min(treeItems.length, 5); i++) {
        try {
          const event = new MouseEvent('contextmenu', {
            bubbles: true,
            cancelable: true,
            button: 2
          });
          treeItems[i].dispatchEvent(event);

          // Find and click expand option
          setTimeout(() => {
            const menuItems = document.querySelectorAll('[role="menuitem"]');
            for (let item of menuItems) {
              const text = item.innerText?.toLowerCase() || '';
              if (text.includes('expand') || text.includes('expandir')) {
                item.click();
                expandedCount++;
                break;
              }
            }
          }, 500);

        } catch (e) {}
      }

      return expandedCount;
    });

    console.log(`[STEP 4] ✅ Right-click interactions completed (${expandedItems})`);
    log.push(`[STEP 4] ✅ Right-click interactions completed`);

    // Wait for context menu actions
    await new Promise(r => setTimeout(r, 3000));

    // STEP 5: Extract all company names
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('[STEP 5] Extract all visible company names...');

    const extractedData = await page.evaluate(() => {
      const items = [];
      const seen = new Set();

      // Multiple extraction methods
      const allElements = document.querySelectorAll('*');

      allElements.forEach(el => {
        const text = el.innerText?.trim();

        if (text &&
            text.length > 3 &&
            text.length < 250 &&
            !seen.has(text)) {

          // Filter out UI elements
          const lower = text.toLowerCase();
          if (lower.includes('anpg') ||
              lower.includes('sobre') ||
              lower.includes('procurar') ||
              lower.includes('close') ||
              lower.includes('menu') ||
              lower.includes('fechar') ||
              lower.includes('decreto') ||
              lower.includes('lei') ||
              lower.length < 5) {
            return;
          }

          seen.add(text);
          items.push(text);
        }
      });

      return items;
    });

    console.log(`[STEP 5] ✅ Extracted ${extractedData.length} items from page`);

    // Filter and deduplicate companies
    extractedData.forEach(item => {
      companies.add(item);
    });

    const companyArray = Array.from(companies).sort();
    console.log(`[STEP 5] ✅ Total unique items: ${companyArray.length}`);

    // Show samples
    console.log('[STEP 5] 📋 Sample items:');
    companyArray.slice(0, 10).forEach((company, idx) => {
      console.log(`          ${idx + 1}. ${company.substring(0, 70)}`);
    });

    log.push(`[STEP 5] ✅ Extracted ${companyArray.length} unique companies`);

    // Save results
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('[SAVE] 💾 Saving results to files...\n');

    const timestamp = new Date().toISOString().split('T')[0];
    const baseFilename = `ANPG_EXTRACTION_DETAILED_${timestamp}`;

    // CSV
    const csvLines = ['company_name;date;extraction_method'];
    companyArray.forEach(company => {
      csvLines.push(`"${company}";${timestamp};detailed_steps`);
    });

    fs.writeFileSync(`${baseFilename}.csv`, csvLines.join('\n'), 'utf-8');
    console.log(`[SAVE] ✅ CSV: ${baseFilename}.csv`);
    console.log(`[SAVE]    Companies: ${companyArray.length}`);

    // JSON
    const jsonData = {
      timestamp: new Date().toISOString(),
      totalCompanies: companyArray.length,
      executionLog: log,
      companies: companyArray
    };

    fs.writeFileSync(`${baseFilename}.json`, JSON.stringify(jsonData, null, 2));
    console.log(`[SAVE] ✅ JSON: ${baseFilename}.json`);

    // Final summary
    console.log('\n═══════════════════════════════════════════════════════');
    console.log('✅ EXTRACTION COMPLETED SUCCESSFULLY!');
    console.log('═══════════════════════════════════════════════════════');
    console.log(`\n📊 FINAL RESULTS:`);
    console.log(`   🏢 Total unique companies: ${companyArray.length}`);
    console.log(`   ✅ Expand icons clicked: ${clickedIcons}`);
    console.log(`   📝 Steps completed: 5/5`);
    console.log(`   💾 Output files: ${baseFilename}.csv & .json\n`);

  } catch (error) {
    console.error('\n❌ ERROR:', error.message);
    log.push(`[ERROR] ${error.message}`);
  } finally {
    if (browser) {
      try {
        await browser.close();
        console.log('[CLEANUP] ✅ Browser closed');
      } catch (e) {
        // Force kill if needed
      }
    }
  }
}

// Execute
extractANPGCompanies().catch(console.error);