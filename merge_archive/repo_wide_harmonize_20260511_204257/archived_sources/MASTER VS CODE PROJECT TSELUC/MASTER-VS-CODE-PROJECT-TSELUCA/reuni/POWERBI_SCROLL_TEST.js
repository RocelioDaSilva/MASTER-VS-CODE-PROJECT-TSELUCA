const puppeteer = require('puppeteer');

async function quickScrollTest() {
    console.log('🧪 Teste rápido de scrolling no Power BI...');

    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    try {
        const powerbiUrl = 'https://app.powerbi.com/view?r=eyJrIjoiZjYxZjY4ZjYtZjQ4ZS00ZjY4LWIzZjYtZjYxZjY4ZjYtZjQ4ZS00ZjY4LWIzZjYiLCJ0IjoiNzhhMGUyMjktNDQ2My00MGM4LTg3MmEtYjQ5NDJjM2MzMTBkIn0%3D';

        console.log('📄 Acessando Power BI...');
        await page.goto(powerbiUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });

        console.log('🔄 Fazendo scroll...');

        // Scroll simples
        await page.evaluate(() => {
            window.scrollTo(0, 500);
        });

        await page.waitForTimeout(1000);

        await page.evaluate(() => {
            window.scrollTo(0, 1000);
        });

        await page.waitForTimeout(1000);

        await page.evaluate(() => {
            window.scrollTo(0, document.body.scrollHeight);
        });

        await page.waitForTimeout(2000);

        console.log('📊 Extraindo dados...');

        const content = await page.evaluate(() => {
            const texts = [];
            const elements = document.querySelectorAll('div, span, p');

            for (let el of elements) {
                const text = el.textContent?.trim();
                if (text && text.length > 10 && text.length < 100 &&
                    !text.includes('This content') &&
                    !text.includes('Learn more')) {
                    texts.push(text);
                }
            }

            return texts.slice(0, 20); // Apenas primeiros 20
        });

        console.log(`📊 Encontrados ${content.length} textos:`);
        content.forEach((text, i) => {
            console.log(`${i + 1}. ${text}`);
        });

        // Salvar
        const fs = require('fs');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const filename = `POWERBI_SCROLL_TEST_${timestamp}.json`;

        fs.writeFileSync(filename, JSON.stringify(content, null, 2));
        console.log(`✅ Salvo em: ${filename}`);

    } catch (error) {
        console.error('❌ Erro:', error.message);
    } finally {
        await browser.close();
    }
}

quickScrollTest();