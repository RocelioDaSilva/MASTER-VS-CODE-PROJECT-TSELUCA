const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

class PowerBIPreciseExtractor {
    constructor() {
        this.embedUrl = 'https://app.powerbi.com/view?r=eyJrIjoiZjYxZjY4ZjYtZjQ4ZS00ZjY4LWIzZjYtZjYxZjY4ZjYtZjQ4ZS00ZjY4LWIzZjYiLCJ0IjoiNzhhMGUyMjktNDQ2My00MGM4LTg3MmEtYjQ5NDJjM2MzMTBkIn0%3D';
        this.outputDir = __dirname;
    }

    async extractAllData() {
        console.log('🚀 Iniciando extração precisa do Power BI com Playwright...');

        const browser = await chromium.launch({ headless: true });
        const page = await browser.newPage();

        try {
            console.log('📄 Navegando para o relatório Power BI...');
            await page.goto(this.embedUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });

            // Aguardar um pouco para o relatório carregar
            await page.waitForTimeout(10000);

            console.log('✅ Página carregada. Extraindo dados via scraping...');

            // Extrair dados via scraping DOM
            const data = await page.evaluate(() => {
                const extracted = [];

                // Procurar por elementos que contenham dados
                const elements = document.querySelectorAll('div, span, p, td, th');
                elements.forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 5 && text.length < 300 &&
                        !text.includes('Mostrar atalhos') &&
                        !text.includes('sugestões de leitores') &&
                        !text.includes('Avançar para o conteúdo') &&
                        !text.includes('Deslocar')) {
                        // Filtrar textos que parecem ser dados relevantes
                        if (/^[A-Z0-9]/.test(text) || text.includes('Ltda') || text.includes('S.A.') || text.includes('Lda')) {
                            extracted.push({
                                texto: text,
                                tipo: 'dados_extraidos'
                            });
                        }
                    }
                });

                return extracted;
            });

            console.log(`📊 Encontrados ${data.length} itens de dados.`);

            // Salvar em JSON
            const jsonFile = path.join(this.outputDir, `POWERBI_SCRAPED_DATA_${this.getTimestamp()}.json`);
            fs.writeFileSync(jsonFile, JSON.stringify(data, null, 2), 'utf8');

            // Salvar em CSV
            const csvFile = path.join(this.outputDir, `POWERBI_SCRAPED_DATA_${this.getTimestamp()}.csv`);
            let csv = 'Texto;Tipo\n';
            data.forEach(item => {
                csv += `"${item.texto.replace(/"/g, '""')}";"${item.tipo}"\n`;
            });
            fs.writeFileSync(csvFile, csv, 'utf8');

            console.log('✅ Extração concluída!');
            console.log(`📄 Dados salvos em: ${jsonFile}`);
            console.log(`📊 CSV salvo em: ${csvFile}`);

        } catch (error) {
            console.error('❌ Erro durante a extração:', error.message);
        } finally {
            await browser.close();
        }
    }

    getTimestamp() {
        const now = new Date();
        return now.toISOString().replace(/[:.]/g, '-').slice(0, -5);
    }
}

// Executar
const extractor = new PowerBIPreciseExtractor();
extractor.extractAllData().catch(console.error);