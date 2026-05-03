const puppeteer = require('puppeteer');

class PowerBIScroller {
    constructor() {
        this.anpgUrl = 'https://anpg.org.ao/'; // Tentando sem www
        this.outputDir = __dirname;
    }

    async scrollIframeAndExtract() {
        console.log('🚀 Iniciando extração com scrolling no iframe do Power BI...');

        const browser = await puppeteer.launch({
            headless: true, // Modificado para headless para execução mais rápida
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security']
        });

        const page = await browser.newPage();

        try {
            console.log('📄 Navegando para a página da ANPG...');
            await page.goto(this.anpgUrl, { waitUntil: 'networkidle2', timeout: 60000 });

            // Aguardar o iframe carregar
            await page.waitForSelector('iframe', { timeout: 30000 });

            console.log('✅ Página carregada. Localizando iframe do Power BI...');

            // Obter informações do iframe
            const iframeInfo = await page.evaluate(() => {
                const iframes = document.querySelectorAll('iframe');
                const powerbiIframe = Array.from(iframes).find(iframe =>
                    iframe.src && iframe.src.includes('powerbi.com')
                );

                if (powerbiIframe) {
                    return {
                        src: powerbiIframe.src,
                        width: powerbiIframe.width,
                        height: powerbiIframe.height
                    };
                }
                return null;
            });

            if (!iframeInfo) {
                console.log('❌ Iframe do Power BI não encontrado na página.');
                return;
            }

            console.log('🔗 Iframe encontrado:', iframeInfo.src);

            // Navegar diretamente para o iframe (já que é uma URL pública)
            console.log('📄 Navegando diretamente para o iframe...');
            await page.goto(iframeInfo.src, { waitUntil: 'networkidle2', timeout: 60000 });

            // Aguardar o relatório carregar
            await page.waitForTimeout(5000);

            console.log('🔄 Iniciando processo de scrolling...');

            // Fazer scroll gradual pela página
            await this.performScrolling(page);

            console.log('📊 Extraindo dados após scrolling...');

            // Extrair dados após scrolling
            const extractedData = await page.evaluate(() => {
                const data = [];

                // Procurar por elementos de texto relevantes
                const elements = document.querySelectorAll('div, span, p, td, th, li');
                elements.forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 3 && text.length < 200 &&
                        !text.includes('Mostrar atalhos') &&
                        !text.includes('sugestões de leitores') &&
                        !text.includes('Avançar para o conteúdo') &&
                        !text.includes('Deslocar') &&
                        !text.includes('This content isn') &&
                        !text.includes('Learn more about Power BI')) {

                        // Filtrar textos que parecem ser dados
                        if (/^[A-Z0-9]/.test(text) || text.includes('Ltda') || text.includes('S.A.') ||
                            text.includes('Lda') || text.includes('Consultoria') || text.includes('Auditoria')) {
                            data.push({
                                texto: text,
                                tipo: 'dados_apos_scroll',
                                timestamp: new Date().toISOString()
                            });
                        }
                    }
                });

                return data;
            });

            console.log(`📊 Encontrados ${extractedData.length} itens após scrolling.`);

            // Salvar dados
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            const jsonFile = `${this.outputDir}/POWERBI_SCROLL_DATA_${timestamp}.json`;
            const csvFile = `${this.outputDir}/POWERBI_SCROLL_DATA_${timestamp}.csv`;

            // Salvar JSON
            require('fs').writeFileSync(jsonFile, JSON.stringify(extractedData, null, 2));

            // Salvar CSV
            let csv = 'Texto;Tipo;Timestamp\n';
            extractedData.forEach(item => {
                csv += `"${item.texto.replace(/"/g, '""')}";"${item.tipo}";"${item.timestamp}"\n`;
            });
            require('fs').writeFileSync(csvFile, csv);

            console.log('✅ Extração concluída!');
            console.log(`📄 JSON salvo em: ${jsonFile}`);
            console.log(`📊 CSV salvo em: ${csvFile}`);

        } catch (error) {
            console.error('❌ Erro durante o processo:', error.message);
        } finally {
            await browser.close();
        }
    }

    async performScrolling(page) {
        // Fazer scroll gradual para simular interação do usuário
        const scrollSteps = 10;
        const scrollDelay = 1000;

        for (let i = 0; i < scrollSteps; i++) {
            console.log(`🔄 Scroll ${i + 1}/${scrollSteps}...`);

            // Scroll para baixo
            await page.evaluate(() => {
                window.scrollTo(0, document.body.scrollHeight);
            });

            await page.waitForTimeout(scrollDelay);

            // Scroll para cima um pouco
            await page.evaluate(() => {
                window.scrollTo(0, document.body.scrollHeight * 0.8);
            });

            await page.waitForTimeout(scrollDelay / 2);

            // Tentar clicar em elementos expansíveis se encontrados
            try {
                await page.evaluate(() => {
                    // Procurar por botões de expandir/colapsar
                    const expandButtons = document.querySelectorAll('[role="button"], button, [aria-expanded]');
                    expandButtons.forEach(btn => {
                        if (btn.textContent && (
                            btn.textContent.includes('+') ||
                            btn.textContent.includes('▶') ||
                            btn.textContent.toLowerCase().includes('expand') ||
                            btn.getAttribute('aria-expanded') === 'false'
                        )) {
                            btn.click();
                        }
                    });
                });
            } catch (e) {
                // Ignorar erros de clique
            }

            await page.waitForTimeout(scrollDelay);
        }

        console.log('✅ Scrolling concluído.');
    }
}

// Executar
const scroller = new PowerBIScroller();
scroller.scrollIframeAndExtract().catch(console.error);