/**
 * PowerBI Embedado - Extrator de Dados
 * =====================================
 * Estratégia 1: Interceptação de chamadas de rede (mais confiável)
 * Estratégia 2: Scraping do DOM com scroll (fallback)
 *
 * Instalação:
 *   npm install puppeteer csv-writer
 *
 * Uso:
 *   node powerbi_extractor.js
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const https = require('https');

// =============================================
//  CONFIGURAÇÕES — edite antes de rodar
// =============================================
const CONFIG = {
  // URL da página que contém o iframe do Power BI
  pageUrl: 'https://seu-site.com/pagina-com-iframe',

  // Arquivo de saída
  outputFile: 'dados_extraidos.csv',

  // Timeout geral em ms
  timeout: 30000,

  // Número de scrolls para carregar conteúdo virtualizado
  scrollSteps: 30,

  // Delay entre scrolls (ms)
  scrollDelay: 600,

  // Mostrar browser? (false = headless)
  headless: true,
};

// =============================================
//  UTILITÁRIOS
// =============================================

function log(msg) {
  console.log(`[${new Date().toISOString()}] ${msg}`);
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

/** Salva array de arrays como CSV */
function salvarCSV(dados, arquivo) {
  if (!dados || dados.length === 0) {
    log('Nenhum dado para salvar.');
    return;
  }
  const conteudo = dados
    .map(linha =>
      linha
        .map(cel => `"${String(cel ?? '').replace(/"/g, '""')}"`)
        .join(',')
    )
    .join('\n');
  fs.writeFileSync(arquivo, '\uFEFF' + conteudo, 'utf8'); // BOM para Excel
  log(`CSV salvo em: ${arquivo} (${dados.length} linhas)`);
}

/** Decodifica o src do iframe Power BI e extrai resourceKey e clusterUri */
function extrairConfigIframe(src) {
  try {
    const url = new URL(src);
    // O parâmetro "r" ou "config" é base64 com a configuração
    const param = url.searchParams.get('r') || url.searchParams.get('config');
    if (!param) return null;
    const decoded = Buffer.from(decodeURIComponent(param), 'base64').toString('utf8');
    const config = JSON.parse(decoded);
    return {
      clusterUri: config.clusterUri || config.hostname,
      resourceKey: config.reportId || config.k,
      raw: config,
    };
  } catch (e) {
    log(`Erro ao decodificar iframe src: ${e.message}`);
    return null;
  }
}

// =============================================
//  ESTRATÉGIA 1: INTERCEPTAÇÃO DE REDE
// =============================================

/**
 * Monitora respostas XHR do Power BI e captura payloads JSON
 * com dados de tabelas/matrizes.
 */
async function estrategia1_interceptarRede(page) {
  log('=== Estratégia 1: Interceptação de rede ===');
  const dadosCapturados = [];

  // Interceptar respostas que contenham dados de query
  page.on('response', async response => {
    const url = response.url();
    if (
      url.includes('querydata') ||
      url.includes('modelsAndExploration') ||
      url.includes('visualquery')
    ) {
      try {
        const json = await response.json();
        log(`Resposta capturada de: ${url}`);
        dadosCapturados.push({ url, data: json });
      } catch (_) {
        // Não era JSON ou já foi consumido
      }
    }
  });

  await page.goto(CONFIG.pageUrl, {
    waitUntil: 'networkidle2',
    timeout: CONFIG.timeout,
  });

  // Aguarda carregamento do relatório
  await sleep(5000);

  // Tenta clicar em visuais para forçar queries adicionais
  const frame = page.frames().find(f => f.url().includes('powerbi.com'));
  if (frame) {
    try {
      await frame.waitForSelector('div[class*="visualContainer"]', {
        timeout: 10000,
      });
      // Clica em cada visual para disparar carregamento de dados
      const visuais = await frame.$$('div[class*="visualContainer"]');
      for (const visual of visuais) {
        try {
          await visual.click();
          await sleep(800);
        } catch (_) {}
      }
    } catch (e) {
      log(`Aviso: ${e.message}`);
    }
  }

  await sleep(3000);

  if (dadosCapturados.length === 0) {
    log('Nenhum dado capturado via rede.');
    return null;
  }

  // Processa os JSON capturados e extrai tabelas
  const todasLinhas = [];
  for (const captura of dadosCapturados) {
    const linhas = processarJsonPowerBI(captura.data);
    todasLinhas.push(...linhas);
  }

  return todasLinhas.length > 0 ? todasLinhas : null;
}

/**
 * Tenta extrair linhas de tabela de um JSON de resposta do Power BI.
 * A estrutura varia, mas geralmente há results > data > dsr > DS > PH > DM0
 */
function processarJsonPowerBI(json) {
  const linhas = [];
  try {
    // Caminho típico de respostas querydata
    const results =
      json?.results ||
      json?.data?.results ||
      (Array.isArray(json) ? json : null);

    if (!results) return linhas;

    for (const result of results) {
      const ds = result?.result?.data?.dsr?.DS;
      if (!ds) continue;
      for (const dataset of ds) {
        const rows = dataset?.PH?.[0]?.DM0 || dataset?.PH?.[1]?.DM0 || [];
        for (const row of rows) {
          // Cada linha pode ter campo C (columns) com os valores
          if (Array.isArray(row.C)) {
            linhas.push(row.C);
          }
        }
      }
    }
  } catch (e) {
    log(`Erro ao processar JSON: ${e.message}`);
  }
  return linhas;
}

// =============================================
//  ESTRATÉGIA 2: SCRAPING DO DOM
// =============================================

/**
 * Acessa o iframe, rola até o fim e coleta células visíveis do DOM.
 */
async function estrategia2_scrapingDOM(page) {
  log('=== Estratégia 2: Scraping do DOM ===');

  await page.goto(CONFIG.pageUrl, {
    waitUntil: 'networkidle2',
    timeout: CONFIG.timeout,
  });

  // Localiza o frame do Power BI
  let frame = null;
  for (let tentativa = 0; tentativa < 10; tentativa++) {
    frame = page.frames().find(
      f => f.url().includes('powerbi.com') || f.url().includes('app.powerbi')
    );
    if (frame) break;
    await sleep(1000);
  }

  if (!frame) {
    // Tenta direto na página (iframe pode ser same-origin)
    log('Frame Power BI não encontrado, tentando na página principal.');
    frame = page.mainFrame();
  }

  log(`Frame encontrado: ${frame.url()}`);

  // Aguarda visual carregar
  try {
    await frame.waitForSelector(
      'div[class*="visualContainer"], div[class*="visual-container"]',
      { timeout: CONFIG.timeout }
    );
  } catch (e) {
    log(`Aviso ao aguardar visual: ${e.message}`);
  }

  await sleep(2000);

  // Scroll para carregar conteúdo virtualizado
  log('Rolando para carregar conteúdo virtualizado...');
  await frame.evaluate(
    async ({ steps, delay }) => {
      // Possíveis contêineres scrolláveis
      const seletores = [
        'div[role="grid"]',
        'div[class*="scrollRegion"]',
        'div[class*="bodyCells"]',
        'div[class*="tableEx"]',
        'div[class*="scroll"]',
      ];

      for (const sel of seletores) {
        const el = document.querySelector(sel);
        if (el && el.scrollHeight > el.clientHeight) {
          for (let i = 0; i < steps; i++) {
            el.scrollBy(0, el.clientHeight);
            await new Promise(r => setTimeout(r, delay));
          }
          // Rola de volta ao início para captura completa
          el.scrollTop = 0;
          await new Promise(r => setTimeout(r, 500));
          break;
        }
      }
    },
    { steps: CONFIG.scrollSteps, delay: CONFIG.scrollDelay }
  );

  // Coleta células — tenta múltiplos seletores conhecidos do Power BI
  const seletoresCelulas = [
    'div.pivotTableCellWrap',
    'div[class*="pivotTableCell"]',
    'div[class*="tableCell"]',
    'div[class*="cellValue"]',
    'span[class*="cellValue"]',
    'div[role="gridcell"]',
    'td',
  ];

  let celulas = [];
  for (const sel of seletoresCelulas) {
    celulas = await frame.$$eval(sel, els =>
      els.map(el => el.innerText.trim()).filter(t => t.length > 0)
    );
    if (celulas.length > 0) {
      log(`Células encontradas com seletor: ${sel} (${celulas.length} itens)`);
      break;
    }
  }

  if (celulas.length === 0) {
    log('Nenhuma célula encontrada com os seletores padrão.');
    // Tira screenshot para debug
    await page.screenshot({ path: 'debug_screenshot.png', fullPage: true });
    log('Screenshot salvo em debug_screenshot.png para inspeção.');
    return null;
  }

  // Tenta detectar número de colunas via cabeçalhos
  const cabecalhos = await frame.$$eval(
    'div[class*="columnHeader"], th, div[role="columnheader"]',
    els => els.map(el => el.innerText.trim()).filter(t => t.length > 0)
  );

  const numColunas = cabecalhos.length > 0 ? cabecalhos.length : 1;
  log(`Colunas detectadas: ${numColunas}`);

  // Monta matriz de linhas
  const linhas = [];
  if (cabecalhos.length > 0) linhas.push(cabecalhos);

  for (let i = 0; i < celulas.length; i += numColunas) {
    linhas.push(celulas.slice(i, i + numColunas));
  }

  return linhas;
}

// =============================================
//  ESTRATÉGIA 3: API INTERNA (via resourceKey)
// =============================================

/**
 * Tenta extrair o resourceKey do iframe e chamar a API pública do Power BI.
 * Requer que o iframe esteja acessível e que o relatório seja "Publish to Web".
 */
async function estrategia3_apiInterna(page) {
  log('=== Estratégia 3: API Interna Power BI ===');

  await page.goto(CONFIG.pageUrl, {
    waitUntil: 'networkidle2',
    timeout: CONFIG.timeout,
  });

  // Obtém o src do iframe Power BI
  const iframeSrc = await page.evaluate(() => {
    const iframe = document.querySelector(
      'iframe[src*="powerbi.com"], iframe[src*="app.powerbi"]'
    );
    return iframe ? iframe.src : null;
  });

  if (!iframeSrc) {
    log('Iframe Power BI não encontrado na página.');
    return null;
  }

  log(`Iframe src: ${iframeSrc}`);
  const config = extrairConfigIframe(iframeSrc);

  if (!config || !config.resourceKey) {
    log('Não foi possível extrair resourceKey do iframe.');
    log('Config decodificada:', JSON.stringify(config?.raw, null, 2));
    return null;
  }

  log(`resourceKey: ${config.resourceKey}`);
  log(`clusterUri: ${config.clusterUri}`);

  // Captura cookies/headers do contexto do relatório
  const cookies = await page.cookies();
  const cookieStr = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  // Chama endpoint de modelos
  const baseUrl = config.clusterUri
    ? `https://${config.clusterUri}`
    : 'https://app.powerbi.com';

  const modelUrl = `${baseUrl}/public/reports/${config.resourceKey}/modelsAndExploration?preferReadOnlySession=true`;
  log(`Chamando: ${modelUrl}`);

  // Faz requisição via page.evaluate para usar contexto do browser (cookies, CORS)
  const modelData = await page.evaluate(async url => {
    try {
      const res = await fetch(url, { credentials: 'include' });
      return await res.json();
    } catch (e) {
      return { error: e.message };
    }
  }, modelUrl);

  if (modelData.error) {
    log(`Erro na API: ${modelData.error}`);
    return null;
  }

  log('Modelo obtido com sucesso!');
  fs.writeFileSync('powerbi_model.json', JSON.stringify(modelData, null, 2));
  log('Modelo salvo em powerbi_model.json');

  // Extrai nomes de tabelas do modelo
  const tabelas =
    modelData?.exploration?.report?.sections?.[0]?.visualContainers ||
    modelData?.models?.[0]?.tables ||
    [];

  log(`Tabelas/Visuais encontrados: ${tabelas.length}`);
  return null; // Retorna null pois os dados precisam de query DAX adicional
}

// =============================================
//  MAIN
// =============================================

(async () => {
  log('Iniciando extrator Power BI...');
  log(`Página alvo: ${CONFIG.pageUrl}`);

  const browser = await puppeteer.launch({
    headless: CONFIG.headless,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--window-size=1920,1080',
    ],
    defaultViewport: { width: 1920, height: 1080 },
  });

  try {
    // ---- Estratégia 1: Interceptação de rede ----
    let page = await browser.newPage();
    await page.setUserAgent(
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
    );

    let dados = await estrategia1_interceptarRede(page);
    await page.close();

    if (dados && dados.length > 0) {
      log(`Estratégia 1 bem-sucedida: ${dados.length} linhas capturadas.`);
      salvarCSV(dados, CONFIG.outputFile);
    } else {
      log('Estratégia 1 sem resultados. Tentando Estratégia 2...');

      // ---- Estratégia 2: Scraping DOM ----
      page = await browser.newPage();
      await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
      );

      dados = await estrategia2_scrapingDOM(page);
      await page.close();

      if (dados && dados.length > 0) {
        log(`Estratégia 2 bem-sucedida: ${dados.length} linhas capturadas.`);
        salvarCSV(dados, CONFIG.outputFile);
      } else {
        log('Estratégia 2 sem resultados. Tentando Estratégia 3 (API interna)...');

        // ---- Estratégia 3: API Interna ----
        page = await browser.newPage();
        await page.setUserAgent(
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
        );

        dados = await estrategia3_apiInterna(page);
        await page.close();

        if (!dados) {
          log('\n⚠️  Todas as estratégias falharam.');
          log('Sugestões:');
          log('  1. Abra debug_screenshot.png para ver o estado da página.');
          log('  2. Inspecione powerbi_model.json se foi gerado.');
          log('  3. Ajuste os seletores DOM conforme o DevTools do seu relatório.');
          log('  4. Verifique se a URL da página está correta em CONFIG.pageUrl.');
        }
      }
    }
  } catch (err) {
    log(`Erro fatal: ${err.message}`);
    console.error(err);
  } finally {
    await browser.close();
    log('Navegador fechado. Script finalizado.');
  }
})();
