const { chromium } = require('playwright');

class IframeScrollExtractor {
    constructor() {
        this.anpgUrl = 'https://anpg.org.ao/';
        this.powerbiUrl = 'https://app.powerbi.com/view?r=eyJrIjoiZjYxZjY4ZjYtZjQ4ZS00ZjY4LWIzZjYtZjYxZjY4ZjYtZjQ4ZS00ZjY4LWIzZjYiLCJ0IjoiNzhhMGUyMjktNDQ2My00MGM4LTg3MmEtYjQ5NDJjM2MzMTBkIn0%3D';
    }

    async extractWithIframeScroll() {
        console.log('🚀 Iniciando extração com scrolling em iframe...');

        const browser = await chromium.launch({ headless: true });
        const context = await browser.newContext();
        const page = await context.newPage();

        try {
            console.log('📄 Tentando acessar diretamente o Power BI...');
            await page.goto(this.powerbiUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });

            console.log('🔄 Executando scrolling simulado...');

            // Múltiplas tentativas de scroll
            for (let attempt = 1; attempt <= 3; attempt++) {
                console.log(`📜 Tentativa ${attempt}/3...`);

                // Scroll gradual
                await page.evaluate(() => {
                    // Scroll para diferentes posições
                    const scrolls = [300, 600, 900, 1200, document.body.scrollHeight];

                    scrolls.forEach((position, index) => {
                        setTimeout(() => {
                            window.scrollTo(0, position);
                        }, index * 500);
                    });
                });

                // Aguardar scrolls
                await page.waitForTimeout(3000);

                // Tentar interagir com elementos expansíveis
                try {
                    await page.evaluate(() => {
                        // Procurar por botões ou elementos clicáveis
                        const clickableElements = document.querySelectorAll('[role="button"], button, [aria-expanded="false"], .expandable, .collapsed');

                        clickableElements.forEach(el => {
                            if (el.offsetHeight > 0 && el.offsetWidth > 0) { // Elemento visível
                                try {
                                    el.click();
                                } catch (e) {
                                    // Ignorar erros de clique
                                }
                            }
                        });
                    });
                } catch (e) {
                    console.log('⚠️ Erro ao tentar clicar elementos');
                }

                await page.waitForTimeout(2000);
            }

            console.log('📊 Extraindo dados após scrolling...');

            // Extrair dados de todas as posições
            const allData = await page.evaluate(() => {
                const data = [];

                // Função para extrair textos de elementos
                function extractFromElements(selector) {
                    const elements = document.querySelectorAll(selector);
                    const texts = [];

                    elements.forEach(el => {
                        const text = el.textContent?.trim();
                        if (text && text.length > 3 && text.length < 200 &&
                            !text.includes('This content') &&
                            !text.includes('Learn more') &&
                            !text.includes('Microsoft Power BI') &&
                            /^[A-Z0-9]/.test(text)) {
                            texts.push(text);
                        }
                    });

                    return texts;
                }

                // Extrair de diferentes tipos de elementos
                const selectors = ['div', 'span', 'p', 'td', 'th', 'li', 'h1', 'h2', 'h3', 'h4'];

                selectors.forEach(selector => {
                    const texts = extractFromElements(selector);
                    texts.forEach(text => {
                        data.push({
                            texto: text,
                            seletor: selector,
                            tipo: 'iframe_scroll_data'
                        });
                    });
                });

                // Remover duplicatas
                const uniqueData = data.filter((item, index, self) =>
                    index === self.findIndex(t => t.texto === item.texto)
                );

                return uniqueData.slice(0, 100); // Limitar a 100 itens
            });

            console.log(`📊 Extraídos ${allData.length} itens únicos.`);

            // Salvar dados
            const fs = require('fs');
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);

            const jsonFile = `IFRAME_SCROLL_DATA_${timestamp}.json`;
            const csvFile = `IFRAME_SCROLL_DATA_${timestamp}.csv`;

            fs.writeFileSync(jsonFile, JSON.stringify(allData, null, 2));

            let csv = 'Texto;Seletor;Tipo\n';
            allData.forEach(item => {
                csv += `"${item.texto.replace(/"/g, '""')}";"${item.seletor}";"${item.tipo}"\n`;
            });
            fs.writeFileSync(csvFile, csv);

            console.log('✅ Extração concluída!');
            console.log(`📄 JSON: ${jsonFile}`);
            console.log(`📊 CSV: ${csvFile}`);

            // Mostrar alguns exemplos
            if (allData.length > 0) {
                console.log('\n📋 Exemplos de dados extraídos:');
                allData.slice(0, 5).forEach((item, i) => {
                    console.log(`${i + 1}. ${item.texto}`);
                });
            }

        } catch (error) {
            console.error('❌ Erro durante extração:', error.message);
        } finally {
            await browser.close();
        }
    }
}

// Executar
const extractor = new IframeScrollExtractor();
extractor.extractWithIframeScroll().catch(console.error);