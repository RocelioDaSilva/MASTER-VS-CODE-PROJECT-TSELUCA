const puppeteer = require('puppeteer');

async function getPowerBIUrl() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    try {
        console.log('Navegando para ANPG...');
        await page.goto('https://anpg.org.ao/', { waitUntil: 'networkidle2', timeout: 60000 });

        // Procurar pelo iframe do Power BI
        const iframeSrc = await page.evaluate(() => {
            const iframes = document.querySelectorAll('iframe');
            for (const iframe of iframes) {
                const src = iframe.src;
                if (src && src.includes('powerbi.com')) {
                    return src;
                }
            }
            return null;
        });

        if (iframeSrc) {
            console.log('URL do Power BI encontrada:', iframeSrc);
            return iframeSrc;
        } else {
            console.log('Iframe do Power BI não encontrado.');
            return null;
        }
    } catch (error) {
        console.error('Erro:', error.message);
        return null;
    } finally {
        await browser.close();
    }
}

getPowerBIUrl();