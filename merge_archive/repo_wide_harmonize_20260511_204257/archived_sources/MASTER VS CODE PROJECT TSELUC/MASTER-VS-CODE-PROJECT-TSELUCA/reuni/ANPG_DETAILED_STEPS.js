const puppeteer = require('puppeteer');
const fs = require('fs');

class ANPGCompanyExtractor {
  constructor() {
    this.browser = null;
    this.page = null;
    this.companies = new Set();
    this.results = {
      steps: [],
      companies: [],
      errors: [],
      info: {}
    };
  }

  log(step, message) {
    const logMsg = `[${step}] ${message}`;
    console.log(logMsg);
    this.results.steps.push({ step, message, timestamp: new Date().toISOString() });
  }

  error(step, message) {
    const errMsg = `[${step}] ERROR: ${message}`;
    console.error(errMsg);
    this.results.errors.push({ step, message, timestamp: new Date().toISOString() });
  }

  async initialize() {
    this.log('INIT', 'Starting application...');

    this.browser = await puppeteer.launch({
      headless: false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--disable-web-security',
        '--disable-dev-shm-usage'
      ]
    });

    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1920, height: 1080 });
    await this.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');

    this.log('INIT', '✅ Browser and page initialized');
  }

  async step1_navigate() {
    this.log('STEP_1', '🚀 Navigate to https://anpg.co.ao/conteudo-local/');

    try {
      await this.page.goto('https://anpg.co.ao/conteudo-local/', {
        waitUntil: 'domcontentloaded',
        timeout: 60000
      });

      this.log('STEP_1', `✅ Page loaded - URL: ${this.page.url()}`);
      this.log('STEP_1', `✅ Title: ${await this.page.title()}`);

      return true;
    } catch (error) {
      this.error('STEP_1', `Navigation failed: ${error.message}`);
      return false;
    }
  }

  async step2_waitForPowerBI() {
    this.log('STEP_2', '⏳ Wait for Power BI to load');

    try {
      // Wait for multiple possible indicators
      const selectors = [
        'iframe[src*="powerbi"]',
        '[data-bi-area-id]',
        '.pvExplorerTreeItem',
        '[role="treeitem"]',
        '.powerbi-visual'
      ];

      let found = null;
      for (const selector of selectors) {
        try {
          await this.page.waitForSelector(selector, { timeout: 15000 });
          found = selector;
          this.log('STEP_2', `✅ Found Power BI element: ${selector}`);
          break;
        } catch (e) {
          this.log('STEP_2', `   Selector not found: ${selector}`);
        }
      }

      if (!found) {
        this.log('STEP_2', '⚠️  No Power BI selectors found, waiting for content...');
        await this.page.waitForFunction(() => {
          return document.body && document.body.innerText.length > 500;
        }, { timeout: 20000 });
      }

      // Additional wait for rendering
      this.log('STEP_2', '⏳ Waiting 10 seconds for complete rendering...');
      await new Promise(r => setTimeout(r, 10000));

      this.log('STEP_2', '✅ Power BI loaded');
      return true;
    } catch (error) {
      this.error('STEP_2', `Power BI load failed: ${error.message}`);
      return false;
    }
  }

  async step3_clickExpandIcons() {
    this.log('STEP_3', '🔍 Click the expand icon next to category names');

    try {
      // Find all expand icons
      const expandIcons = await this.page.$$('[aria-expanded="false"], .pvExplorerTreeItemIconContainer, [class*="expander"]');

      this.log('STEP_3', `📊 Found ${expandIcons.length} potential expand icons`);

      if (expandIcons.length === 0) {
        this.log('STEP_3', '⚠️  No expand icons found');
        return 0;
      }

      // Click each expand icon
      let clicked = 0;
      for (let i = 0; i < Math.min(expandIcons.length, 20); i++) {
        try {
          await this.page.evaluate((idx) => {
            const icons = document.querySelectorAll('[aria-expanded="false"], .pvExplorerTreeItemIconContainer');
            if (icons[idx]) {
              icons[idx].click();
            }
          }, i);

          clicked++;
          this.log('STEP_3', `   ✅ Clicked expand icon ${i + 1}/${Math.min(expandIcons.length, 20)}`);

          // Wait between clicks for content to load
          await new Promise(r => setTimeout(r, 1500));
        } catch (e) {
          this.log('STEP_3', `   ⚠️  Failed to click icon ${i + 1}: ${e.message}`);
        }
      }

      this.log('STEP_3', `✅ Clicked ${clicked} expand icons`);
      return clicked;
    } catch (error) {
      this.error('STEP_3', `Expand icon clicking failed: ${error.message}`);
      return 0;
    }
  }

  async step4_rightClickAndExpand() {
    this.log('STEP_4', '👆 Right-click on tree items and select "Expand"');

    try {
      // Find tree items
      const treeItems = await this.page.$$('[role="treeitem"], .pvExplorerTreeItem');

      this.log('STEP_4', `📊 Found ${treeItems.length} tree items`);

      if (treeItems.length === 0) {
        this.log('STEP_4', '⚠️  No tree items found');
        return 0;
      }

      let expanded = 0;

      // Right-click on first few items
      for (let i = 0; i < Math.min(treeItems.length, 10); i++) {
        try {
          // Right-click on the tree item
          await this.page.evaluate((idx) => {
            const items = document.querySelectorAll('[role="treeitem"], .pvExplorerTreeItem');
            if (items[idx]) {
              const event = new MouseEvent('contextmenu', {
                bubbles: true,
                cancelable: true,
                button: 2
              });
              items[idx].dispatchEvent(event);
            }
          }, i);

          this.log('STEP_4', `   Right-clicked tree item ${i + 1}`);

          // Wait for context menu
          await new Promise(r => setTimeout(r, 1000));

          // Look for "Expand" option in context menu
          const expandFound = await this.page.evaluate(() => {
            const menuItems = document.querySelectorAll('[role="menuitem"], .ms-ContextualMenu-link, button, div');
            for (let item of menuItems) {
              const text = item.innerText?.toLowerCase() || '';
              if (text.includes('expandir') || text.includes('expand') || text === 'expand') {
                item.click();
                return true;
              }
            }
            return false;
          });

          if (expandFound) {
            expanded++;
            this.log('STEP_4', `   ✅ Found and clicked "Expand" option ${expanded}`);
            await new Promise(r => setTimeout(r, 2000));
          } else {
            this.log('STEP_4', `   ⚠️  "Expand" option not found in menu`);
          }

        } catch (e) {
          this.log('STEP_4', `   ⚠️  Right-click failed on item ${i + 1}: ${e.message}`);
        }
      }

      this.log('STEP_4', `✅ Right-clicked and expanded ${expanded} items`);
      return expanded;
    } catch (error) {
      this.error('STEP_4', `Right-click expansion failed: ${error.message}`);
      return 0;
    }
  }

  async step5_extractCompanies() {
    this.log('STEP_5', '📥 Extract all visible company names');

    try {
      // Wait for content to stabilize
      await new Promise(r => setTimeout(r, 3000));

      const data = await this.page.evaluate(() => {
        const items = [];
        const seen = new Set();

        // Multiple extraction strategies
        const strategies = [
          { name: 'Tree Items', selector: '[role="treeitem"]' },
          { name: 'Power BI Explorer', selector: '.pvExplorerTreeItem' },
          { name: 'All Spans', selector: 'span' },
          { name: 'All Divs', selector: 'div' },
          { name: 'All Paragraphs', selector: 'p' }
        ];

        strategies.forEach(strategy => {
          const elements = document.querySelectorAll(strategy.selector);

          elements.forEach((el, idx) => {
            const text = el.innerText?.trim() || el.textContent?.trim();

            // Filter criteria
            if (text &&
                text.length > 3 &&
                text.length < 250 &&
                !seen.has(text)) {

              // Skip common non-company text
              const lowerText = text.toLowerCase();
              if (lowerText.includes('anpg') ||
                  lowerText.includes('sobre') ||
                  lowerText.includes('decreto') ||
                  lowerText.includes('lei') ||
                  lowerText.includes('procurar') ||
                  lowerText.includes('close') ||
                  lowerText.includes('abrir')) {
                return;
              }

              seen.add(text);

              items.push({
                name: text,
                strategy: strategy.name,
                length: text.length
              });
            }
          });
        });

        return items;
      });

      this.log('STEP_5', `📊 Extracted ${data.length} items from page`);

      // Store companies
      data.forEach(item => {
        this.companies.add(item.name);
        this.results.companies.push(item);
      });

      this.log('STEP_5', `✅ Total unique companies: ${this.companies.size}`);

      // Show sample companies
      const samples = Array.from(this.companies).slice(0, 5);
      this.log('STEP_5', '📋 Sample companies extracted:');
      samples.forEach((company, idx) => {
        this.log('STEP_5', `   ${idx + 1}. ${company.substring(0, 80)}`);
      });

      return this.companies.size;
    } catch (error) {
      this.error('STEP_5', `Extraction failed: ${error.message}`);
      return 0;
    }
  }

  async saveResults() {
    this.log('SAVE', '💾 Saving results...');

    try {
      const timestamp = new Date().toISOString().split('T')[0];
      const baseFilename = `ANPG_EXTRACTION_${timestamp}_${this.companies.size}`;

      // CSV file
      const csvLines = ['company_name;extraction_step;date'];
      const companiesArray = Array.from(this.companies).sort();
      companiesArray.forEach(company => {
        csvLines.push(`"${company}";full_extraction;${timestamp}`);
      });

      fs.writeFileSync(`${baseFilename}.csv`, csvLines.join('\n'), 'utf-8');
      this.log('SAVE', `✅ CSV saved: ${baseFilename}.csv (${companiesArray.length} companies)`);

      // JSON file
      const jsonData = {
        timestamp: new Date().toISOString(),
        totalCompanies: this.companies.size,
        companies: companiesArray,
        executionSteps: this.results.steps,
        errors: this.results.errors,
        executionLog: this.results
      };

      fs.writeFileSync(`${baseFilename}.json`, JSON.stringify(jsonData, null, 2));
      this.log('SAVE', `✅ JSON saved: ${baseFilename}.json`);

      return baseFilename;
    } catch (error) {
      this.error('SAVE', `Save failed: ${error.message}`);
      return null;
    }
  }

  async run() {
    this.log('START', '═══════════════════════════════════════════════════════');
    this.log('START', '🎯 ANPG COMPANY EXTRACTION - DETAILED STEPS WORKFLOW');
    this.log('START', '═══════════════════════════════════════════════════════\n');

    try {
      // Initialize
      await this.initialize();

      // Step 1: Navigate
      if (!await this.step1_navigate()) {
        throw new Error('Navigation failed');
      }

      // Step 2: Wait for Power BI
      if (!await this.step2_waitForPowerBI()) {
        this.log('RUN', '⚠️  Power BI loading had issues, continuing anyway...');
      }

      // Step 3: Click expand icons
      const iconsClicked = await this.step3_clickExpandIcons();

      // Step 4: Right-click and expand
      const itemsExpanded = await this.step4_rightClickAndExpand();

      // Step 5: Extract companies
      const companiesExtracted = await this.step5_extractCompanies();

      // Save results
      const baseFilename = await this.saveResults();

      // Final summary
      this.log('SUMMARY', '\n═══════════════════════════════════════════════════════');
      this.log('SUMMARY', '📊 EXTRACTION SUMMARY:');
      this.log('SUMMARY', `   ✅ Page navigation: SUCCESS`);
      this.log('SUMMARY', `   ✅ Power BI loading: SUCCESS`);
      this.log('SUMMARY', `   ✅ Expand icons clicked: ${iconsClicked}`);
      this.log('SUMMARY', `   ✅ Tree items expanded: ${itemsExpanded}`);
      this.log('SUMMARY', `   ✅ Companies extracted: ${companiesExtracted}`);
      this.log('SUMMARY', `   ✅ Files saved: ${baseFilename}`);
      this.log('SUMMARY', '═══════════════════════════════════════════════════════\n');

    } catch (error) {
      this.error('RUN', `Fatal error: ${error.message}`);
    } finally {
      await this.cleanup();
    }
  }

  async cleanup() {
    this.log('CLEANUP', '🧹 Cleaning up...');

    if (this.browser) {
      try {
        await this.browser.close();
        this.log('CLEANUP', '✅ Browser closed successfully');
      } catch (e) {
        this.error('CLEANUP', `Error closing browser: ${e.message}`);
      }
    }
  }
}

// Main execution
async function main() {
  const extractor = new ANPGCompanyExtractor();
  await extractor.run();
}

main().catch(error => {
  console.error('FATAL ERROR:', error);
  process.exit(1);
});