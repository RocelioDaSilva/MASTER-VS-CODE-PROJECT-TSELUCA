const puppeteer = require('puppeteer');

class PowerBISimpleScroll {
    constructor() {
        this.powerbiUrl = 'https://app.powerbi.com/view?r=eyJrIjoiZjYxZjY4ZjYtZjQ4ZS00ZjY4LWIzZjYtZjYxZjY4ZjYtZjQ4ZS00ZjY4LWIzZjYiLCJ0IjoiNzhhMGUyMjktNDQ2My00MGM4LTg3MmEtYjQ5NDJjM2MzMTBkIn0%3D';
    }

    async scrollAndExtract() {
        console.log('🚀 Iniciando scrolling direto no Power BI...');

        const browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });

        const page = await browser.newPage();

        try {
            console.log('📄 Carregando Power BI...');
            await page.goto(this.powerbiUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });

            // Aguardar um pouco para carregamento
            await page.waitForTimeout(3000);

            console.log('🔄 Executando scrolling...');

            // Fazer múltiplos scrolls
            for (let i = 0; i < 5; i++) {
                console.log(`📜 Scroll ${i + 1}/5...`);

                // Scroll para baixo
                await page.evaluate(() => {
                    window.scrollTo(0, document.body.scrollHeight);
                });

                await page.waitForTimeout(2000);

                // Scroll para cima
                await page.evaluate(() => {
                    window.scrollTo(0, 0);
                });

                await page.waitForTimeout(1000);
            }

            console.log('📊 Extraindo dados após scrolling...');

            // Extrair dados
            const data = await page.evaluate(() => {
                const extracted = [];

                // Procurar por textos visíveis
                const elements = document.querySelectorAll('*');
                elements.forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 5 && text.length < 150 &&
                        !text.includes('This content') &&
                        !text.includes('Learn more') &&
                        /^[A-Z0-9]/.test(text)) {
                        extracted.push({
                            texto: text,
                            tipo: 'scroll_extraction'
                        });
                    }
                });

                return extracted.slice(0, 50); // Limitar a 50 itens
            });

            console.log(`📊 Extraídos ${data.length} itens.`);

            // Salvar
            const fs = require('fs');
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);

            const jsonFile = `POWERBI_SCROLL_SIMPLE_${timestamp}.json`;
            const csvFile = `POWERBI_SCROLL_SIMPLE_${timestamp}.csv`;

            fs.writeFileSync(jsonFile, JSON.stringify(data, null, 2));

            let csv = 'Texto;Tipo\n';
            data.forEach(item => {
                csv += `"${item.texto.replace(/"/g, '""')}";"${item.tipo}"\n`;
            });
            fs.writeFileSync(csvFile, csv);

            console.log('✅ Concluído!');
            console.log(`📄 Salvo: ${jsonFile}`);
            console.log(`📊 Salvo: ${csvFile}`);

        } catch (error) {
            console.error('❌ Erro:', error.message);
        } finally {
            await browser.close();
        }
    }
}

// Executar
const scroller = new PowerBISimpleScroll();
scroller.scrollAndExtract().catch(console.error);