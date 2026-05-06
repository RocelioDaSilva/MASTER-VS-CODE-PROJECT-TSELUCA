const fs = require('fs');
const path = require('path');

class ConsultoriaExtractor {
    constructor() {
        this.consolidacaoFile = path.join(__dirname, 'CONSOLIDACAO_NOMES_REAIS.js');
        this.targetCategory = 'Consultoria, Assessoria e Auditoria';
    }

    extractConsultoriaData() {
        console.log(`🎯 Extraindo dados da categoria: ${this.targetCategory}`);

        if (!fs.existsSync(this.consolidacaoFile)) {
            console.error('❌ Arquivo de consolidação não encontrado:', this.consolidacaoFile);
            return;
        }

        const data = fs.readFileSync(this.consolidacaoFile, 'utf8');

        // Extrair o array de empresas verificadas
        const empresasMatch = data.match(/const empresasVerificadas = \[([\s\S]*?)\];/);
        if (!empresasMatch) {
            console.error('❌ Não foi possível encontrar o array de empresas verificadas');
            return;
        }

        // Parsear as empresas (simples, assumindo formato consistente)
        const empresasText = empresasMatch[1];
        const empresas = [];

        // Usar regex para extrair cada empresa
        const empresaRegex = /\{\s*nif:\s*'([^']+)',\s*nome:\s*'([^']+)',\s*categoria:\s*'([^']+)'\s*\}/g;
        let match;

        while ((match = empresaRegex.exec(empresasText)) !== null) {
            const [_, nif, nome, categoria] = match;
            if (categoria === this.targetCategory) {
                empresas.push({ nif, nome, categoria });
            }
        }

        if (empresas.length === 0) {
            console.log('⚠️ Nenhuma empresa encontrada nesta categoria.');
            return;
        }

        // Salvar dados
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const outputCsv = path.join(__dirname, `CONSULTORIA_COMPLETA_${timestamp}.csv`);
        const outputJson = path.join(__dirname, `CONSULTORIA_COMPLETA_${timestamp}.json`);

        // CSV
        let csv = 'NIF;Nome;Categoria\n';
        empresas.forEach(empresa => {
            csv += `"${empresa.nif}";"${empresa.nome}";"${empresa.categoria}"\n`;
        });
        fs.writeFileSync(outputCsv, csv, 'utf8');

        // JSON
        fs.writeFileSync(outputJson, JSON.stringify(empresas, null, 2), 'utf8');

        console.log('✅ Extração concluída!');
        console.log(`🏢 Total de empresas: ${empresas.length}`);
        console.log(`📄 CSV salvo em: ${outputCsv}`);
        console.log(`📋 JSON salvo em: ${outputJson}`);

        // Mostrar lista das empresas
        console.log('\n📋 Lista de Empresas:');
        console.log('═══════════════════════════════════════════════════════════════');
        empresas.forEach((empresa, index) => {
            console.log(`${index + 1}. ${empresa.nome} (NIF: ${empresa.nif})`);
        });
    }
}

// Executar
const extractor = new ConsultoriaExtractor();
extractor.extractConsultoriaData();