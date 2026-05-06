const puppeteer = require('puppeteer');
const fs = require('fs');

class ANPGScraper {
  constructor() {
    this.browser = null;
    this.page = null;
    this.maxRetries = 3;
    this.timeout = 60000;
  }

  async initialize() {
    console.log('🚀 Initializing browser...');
    this.browser = await puppeteer.launch({
      headless: false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--disable-web-security',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--no-first-run',
        '--no-zygote',
        '--disable-gpu-sandbox'
      ],
      ignoreDefaultArgs: ['--disable-extensions']
    });

    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1920, height: 1080 });
    await this.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

    // Enable console logging
    this.page.on('console', msg => {
      if (msg.text().includes('error') || msg.text().includes('Error')) {
        console.log('🔴 PAGE ERROR:', msg.text());
      }
    });

    console.log('✅ Browser initialized');
  }

  async loadPage(url, retries = 0) {
    try {
      console.log(`📍 Loading page: ${url} (attempt ${retries + 1})`);

      await this.page.goto(url, {
        waitUntil: 'networkidle0',
        timeout: this.timeout
      });

      console.log('✅ Page loaded successfully');
      return true;
    } catch (error) {
      console.log(`❌ Page load failed: ${error.message}`);

      if (retries < this.maxRetries) {
        console.log(`🔄 Retrying in 5 seconds...`);
        await new Promise(r => setTimeout(r, 5000));
        return this.loadPage(url, retries + 1);
      }

      return false;
    }
  }

  async waitForContent() {
    console.log('⏳ Waiting for Power BI content to load...');

    // Wait for various possible indicators that content is loaded
    const selectors = [
      '[data-bi-area-id]',
      '.pvExplorerTreeItem',
      '[role="treeitem"]',
      '.powerbi-report',
      'iframe[src*="powerbi"]',
      'div[style*="powerbi"]'
    ];

    for (const selector of selectors) {
      try {
        await this.page.waitForSelector(selector, { timeout: 10000 });
        console.log(`✅ Found content indicator: ${selector}`);
        return true;
      } catch (e) {
        // Continue to next selector
      }
    }

    // Fallback: wait for any significant content
    await this.page.waitForFunction(() => {
      return document.body && document.body.innerText.length > 1000;
    }, { timeout: 30000 });

    console.log('✅ Content loaded (fallback method)');
    return true;
  }

  async findAndClickExpanders() {
    console.log('🔍 Looking for expandable elements...');

    const expanders = await this.page.evaluate(() => {
      const found = [];

      // Strategy 1: Power BI specific selectors
      const pbSelectors = [
        '.pvExplorerTreeItemIconContainer',
        '[aria-expanded="false"]',
        '.powerbi-tree-item-expander',
        '[data-expanded="false"]'
      ];

      pbSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
          found.push({
            element: el,
            selector: selector,
            text: el.innerText?.substring(0, 50) || 'No text',
            ariaExpanded: el.getAttribute('aria-expanded')
          });
        });
      });

      // Strategy 2: Generic expanders
      const genericSelectors = [
        'button[aria-label*="expand"]',
        'button[title*="expand"]',
        'span[role="button"]',
        '.expander',
        '.expand-icon'
      ];

      genericSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
          if (!found.some(f => f.element === el)) {
            found.push({
              element: el,
              selector: selector,
              text: el.innerText?.substring(0, 50) || 'No text',
              ariaExpanded: el.getAttribute('aria-expanded')
            });
          }
        });
      });

      return found;
    });

    console.log(`📊 Found ${expanders.length} potential expanders`);

    if (expanders.length === 0) {
      console.log('⚠️ No expanders found, trying alternative methods...');
      return await this.tryAlternativeExpansion();
    }

    // Click expanders in batches
    let clicked = 0;
    for (let i = 0; i < Math.min(expanders.length, 10); i++) {
      try {
        await this.page.evaluate((idx) => {
          const expanders = document.querySelectorAll('[aria-expanded="false"], .pvExplorerTreeItemIconContainer');
          if (expanders[idx]) {
            expanders[idx].click();
          }
        }, i);

        clicked++;
        console.log(`✅ Clicked expander ${i + 1}/${Math.min(expanders.length, 10)}`);
        await new Promise(r => setTimeout(r, 1000));
      } catch (e) {
        console.log(`❌ Failed to click expander ${i + 1}: ${e.message}`);
      }
    }

    return clicked;
  }

  async tryAlternativeExpansion() {
    console.log('🔄 Trying alternative expansion methods...');

    // Method 1: Keyboard navigation
    console.log('⌨️ Trying keyboard expansion...');
    try {
      await this.page.keyboard.press('Tab');
      await this.page.keyboard.press('Enter');
      await new Promise(r => setTimeout(r, 2000));
      console.log('✅ Keyboard expansion attempted');
    } catch (e) {
      console.log('❌ Keyboard expansion failed');
    }

    // Method 2: Click on tree items
    console.log('🖱️ Trying to click tree items...');
    try {
      const treeItems = await this.page.$$('[role="treeitem"]');
      if (treeItems.length > 0) {
        for (let i = 0; i < Math.min(treeItems.length, 3); i++) {
          await treeItems[i].click();
          await new Promise(r => setTimeout(r, 500));
        }
        console.log('✅ Clicked tree items');
        return treeItems.length;
      }
    } catch (e) {
      console.log('❌ Tree item clicking failed');
    }

    // Method 3: Scroll and wait
    console.log('📜 Trying scroll method...');
    try {
      await this.page.evaluate(() => {
        window.scrollTo(0, document.body.scrollHeight);
      });
      await new Promise(r => setTimeout(r, 3000));
      await this.page.evaluate(() => {
        window.scrollTo(0, 0);
      });
      console.log('✅ Scroll method completed');
    } catch (e) {
      console.log('❌ Scroll method failed');
    }

    return 0;
  }

  async extractData() {
    console.log('📥 Extracting data from page...');

    const data = await this.page.evaluate(() => {
      const items = [];
      const seen = new Set();

      // Multiple extraction strategies
      const strategies = [
        {
          name: 'Power BI Tree Items',
          selector: '[role="treeitem"]',
          type: 'tree_item'
        },
        {
          name: 'Power BI Explorer Items',
          selector: '.pvExplorerTreeItem',
          type: 'explorer_item'
        },
        {
          name: 'Generic Tree Items',
          selector: '[aria-level]',
          type: 'aria_tree'
        },
        {
          name: 'Text Content',
          selector: 'span, div, p',
          type: 'text_content'
        }
      ];

      strategies.forEach(strategy => {
        try {
          const elements = document.querySelectorAll(strategy.selector);

          elements.forEach((el, idx) => {
            const text = el.innerText?.trim() || el.textContent?.trim();

            if (text &&
                text.length > 3 &&
                text.length < 200 &&
                !seen.has(text) &&
                !text.toLowerCase().includes('anpg') &&
                !text.toLowerCase().includes('sobre') &&
                !text.toLowerCase().includes('decreto') &&
                !text.toLowerCase().includes('lei')) {

              seen.add(text);

              // Try to determine level
              let level = 2; // Default to company level
              const ariaLevel = el.getAttribute('aria-level');
              if (ariaLevel) {
                level = parseInt(ariaLevel) - 1;
              } else if (text.toLowerCase().includes('consultoria') ||
                        text.toLowerCase().includes('serviço') ||
                        text.toLowerCase().includes('sistema')) {
                level = 0; // Category
              } else if (text.length > 80) {
                level = 1; // Subcategory
              }

              items.push({
                level: level,
                text: text,
                type: level === 0 ? 'CATEGORIA' : level === 1 ? 'SUBCATEGORIA' : 'EMPRESA',
                strategy: strategy.name,
                selector: strategy.selector,
                index: idx
              });
            }
          });
        } catch (e) {
          console.log(`Error with strategy ${strategy.name}:`, e.message);
        }
      });

      return items;
    });

    console.log(`✅ Extracted ${data.length} items`);
    return data;
  }

  async takeScreenshot(filename) {
    try {
      await this.page.screenshot({ path: filename, fullPage: true });
      console.log(`📸 Screenshot saved: ${filename}`);
    } catch (e) {
      console.log(`❌ Screenshot failed: ${e.message}`);
    }
  }

  async run() {
    const results = {
      success: false,
      methods: [],
      data: [],
      errors: [],
      screenshots: []
    };

    try {
      await this.initialize();

      // Load the page
      const pageLoaded = await this.loadPage('https://anpg.co.ao/conteudo-local/');
      if (!pageLoaded) {
        throw new Error('Failed to load page after retries');
      }
      results.methods.push('page_loaded');

      // Wait for content
      await this.waitForContent();
      results.methods.push('content_loaded');

      // Take initial screenshot
      await this.takeScreenshot('screenshot_initial.png');
      results.screenshots.push('screenshot_initial.png');

      // Wait for Power BI to fully load
      console.log('⏳ Waiting for Power BI to initialize...');
      await new Promise(r => setTimeout(r, 10000));

      // Try to expand content
      const expandersClicked = await this.findAndClickExpanders();
      results.methods.push(`expanders_clicked: ${expandersClicked}`);

      // Wait for expansion
      await new Promise(r => setTimeout(r, 5000));

      // Take screenshot after expansion
      await this.takeScreenshot('screenshot_after_expansion.png');
      results.screenshots.push('screenshot_after_expansion.png');

      // Extract data
      const data = await this.extractData();
      results.data = data;
      results.methods.push(`data_extracted: ${data.length} items`);

      // Take final screenshot
      await this.takeScreenshot('screenshot_final.png');
      results.screenshots.push('screenshot_final.png');

      results.success = true;

    } catch (error) {
      console.error('❌ Scraping failed:', error.message);
      results.errors.push(error.message);
    } finally {
      await this.cleanup();
    }

    return results;
  }

  async cleanup() {
    if (this.browser) {
      try {
        console.log('🧹 Cleaning up browser...');
        await this.browser.close();
        console.log('✅ Browser closed');
      } catch (e) {
        console.error('❌ Error closing browser:', e.message);
        // Force kill if needed
        try {
          if (this.browser.process()) {
            this.browser.process().kill('SIGKILL');
          }
        } catch (killErr) {
          console.error('❌ Error force killing browser:', killErr.message);
        }
      }
    }
  }

  async saveResults(results) {
    const timestamp = new Date().toISOString().split('T')[0];
    const baseFilename = `ANPG_SCRAPE_${timestamp}_${results.data.length}`;

    // Save CSV
    const csvLines = ['level;text;type;strategy;selector;index'];
    results.data.forEach(item => {
      csvLines.push(`${item.level};"${item.text.replace(/"/g, '""')}";${item.type};${item.strategy};${item.selector};${item.index}`);
    });

    fs.writeFileSync(`${baseFilename}.csv`, csvLines.join('\n'), 'utf-8');
    console.log(`💾 CSV saved: ${baseFilename}.csv`);

    // Save JSON
    const jsonData = {
      timestamp: new Date().toISOString(),
      success: results.success,
      methods: results.methods,
      errors: results.errors,
      screenshots: results.screenshots,
      dataCount: results.data.length,
      data: results.data
    };

    fs.writeFileSync(`${baseFilename}.json`, JSON.stringify(jsonData, null, 2));
    console.log(`💾 JSON saved: ${baseFilename}.json`);

    return baseFilename;
  }
}

// Main execution
async function main() {
  console.log('🎯 ANPG SCRAPER - ROBUST VERSION\n');
  console.log('═════════════════════════════════════════════════════════\n');

  const scraper = new ANPGScraper();

  try {
    const results = await scraper.run();

    console.log('\n📊 RESULTS SUMMARY:');
    console.log('═════════════════════════════════════════════════════════');
    console.log(`✅ Success: ${results.success}`);
    console.log(`🔧 Methods attempted: ${results.methods.length}`);
    console.log(`📥 Data extracted: ${results.data.length} items`);
    console.log(`❌ Errors: ${results.errors.length}`);
    console.log(`📸 Screenshots: ${results.screenshots.length}`);

    if (results.errors.length > 0) {
      console.log('\n❌ ERRORS:');
      results.errors.forEach(error => console.log(`   - ${error}`));
    }

    if (results.data.length > 0) {
      const filename = await scraper.saveResults(results);
      console.log(`\n💾 Files saved with prefix: ${filename}`);
    }

  } catch (error) {
    console.error('💥 Fatal error:', error.message);
  }
}

main().catch(console.error);