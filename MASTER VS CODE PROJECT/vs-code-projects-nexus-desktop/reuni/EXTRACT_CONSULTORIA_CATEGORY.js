const fs = require('fs');
const path = require('path');

class CategoryFilter {
    constructor() {
        this.inputFile = path.join(__dirname, 'DADOS_EXPANDED_2500_COMPANIES_2026-02-25_2920.csv');
        this.targetCategory = 'Consultoria, Assessoria e Auditoria';
    }

    extractCategoryData() {
        console.log(`🔍 Extraindo dados da categoria: ${this.targetCategory}`);

        if (!fs.existsSync(this.inputFile)) {
            console.error('❌ Arquivo de dados não encontrado:', this.inputFile);
            return;
        }

        const data = fs.readFileSync(this.inputFile, 'utf8');
        const lines = data.split('\n').filter(line => line.trim());

        const header = lines[0];
        const rows = lines.slice(1);

        // Filtrar linhas que pertencem à categoria alvo
        const categoryData = [];
        let inTargetCategory = false;

        for (const row of rows) {
            const columns = row.split(';');
            if (columns.length < 2) continue;

            const nivel = parseInt(columns[0].replace(/"/g, ''));
            const texto = columns[1].replace(/"/g, '');
            const tipo = columns[2] ? columns[2].replace(/"/g, '') : '';

            if (nivel === 0 && texto === this.targetCategory) {
                inTargetCategory = true;
                categoryData.push(row);
            } else if (nivel === 0 && texto !== this.targetCategory) {
                inTargetCategory = false;
            } else if (inTargetCategory && nivel > 0) {
                categoryData.push(row);
            }
        }

        if (categoryData.length === 0) {
            console.log('⚠️ Nenhuma empresa encontrada nesta categoria.');
            return;
        }

        // Salvar dados filtrados
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const outputCsv = path.join(__dirname, `CONSULTORIA_ASSESSORIA_AUDITORIA_${timestamp}.csv`);
        const outputJson = path.join(__dirname, `CONSULTORIA_ASSESSORIA_AUDITORIA_${timestamp}.json`);

        // CSV
        const csvContent = [header, ...categoryData].join('\n');
        fs.writeFileSync(outputCsv, csvContent, 'utf8');

        // JSON
        const jsonData = categoryData.map(row => {
            const cols = row.split(';');
            return {
                nivel: parseInt(cols[0].replace(/"/g, '')),
                texto: cols[1].replace(/"/g, ''),
                tipo: cols[2] ? cols[2].replace(/"/g, '') : '',
                nif: cols[3] ? cols[3].replace(/"/g, '') : '',
                categoria: cols[4] ? cols[4].replace(/"/g, '') : '',
                confirmado: cols[5] ? cols[5].replace(/"/g, '') : '',
                origem: cols[6] ? cols[6].replace(/"/g, '') : ''
            };
        });
        fs.writeFileSync(outputJson, JSON.stringify(jsonData, null, 2), 'utf8');

        console.log('✅ Extração concluída!');
        console.log(`📊 ${categoryData.length} registros encontrados`);
        console.log(`📄 CSV salvo em: ${outputCsv}`);
        console.log(`📋 JSON salvo em: ${outputJson}`);

        // Mostrar resumo
        const companies = jsonData.filter(item => item.tipo === 'EMPRESA');
        console.log(`🏢 Total de empresas: ${companies.length}`);
    }
}

// Executar
const filter = new CategoryFilter();
filter.extractCategoryData();