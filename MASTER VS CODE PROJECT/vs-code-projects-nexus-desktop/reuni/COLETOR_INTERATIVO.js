const fs = require('fs');
const readline = require('readline');

class CompanyCollector {
  constructor() {
    this.companies = [];
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: true
    });
  }

  clearScreen() {
    console.clear();
    this.showHeader();
  }

  showHeader() {
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║         📋 COLETOR INTERATIVO DE NOMES DE EMPRESAS        ║');
    console.log('║                                                           ║');
    console.log('║  Right-Click no browser → Copy → Ctrl+V aqui → ENTER     ║');
    console.log('║                                                           ║');
    console.log(`║  Total coletado: ${String(this.companies.length).padEnd(42)}║`);
    console.log('╚═══════════════════════════════════════════════════════════╝\n');
  }

  getStatusBar() {
    const progress = this.companies.length;
    const filled = Math.min(progress / 5, 10); // Max 10 blocks
    const blocks = '█'.repeat(filled);
    const empty = '░'.repeat(10 - filled);

    return `[${blocks}${empty}] ${progress} empresas`;
  }

  validateCompany(name) {
    // Basic validation
    const trimmed = name.trim();

    if (trimmed.length < 3) {
      return { valid: false, reason: 'Muito curto (min 3 caracteres)' };
    }

    if (trimmed.length > 250) {
      return { valid: false, reason: 'Muito longo (max 250 caracteres)' };
    }

    // Check for common garbage text
    const garbage = ['page', 'scroll', 'click', 'menu', 'close', 'anpg', 'sobre', 'decreto'];
    if (garbage.some(g => trimmed.toLowerCase().includes(g))) {
      return { valid: false, reason: 'Contém palavra impedida' };
    }

    // Check for duplicates
    if (this.companies.some(c => c.toLowerCase() === trimmed.toLowerCase())) {
      return { valid: false, reason: 'Duplicado (já existe)' };
    }

    return { valid: true, name: trimmed };
  }

  askForCompany() {
    this.clearScreen();
    console.log(this.getStatusBar());
    console.log('');

    if (this.companies.length > 0) {
      console.log('Últimas 3 empresas adicionadas:');
      this.companies.slice(-3).forEach((c, i) => {
        const num = this.companies.length - 2 + i;
        console.log(`   ${num}. ${c.substring(0, 60)}`);
      });
      console.log('');
    }

    console.log('Opções:');
    console.log('  [Cole nome]  - Adiciona empresa');
    console.log('  [L]ist      - Lista todas empresas');
    console.log('  [U]ndo      - Desfaz última');
    console.log('  [C]lear     - Limpa lista');
    console.log('  [D]one      - Salva e encerra\n');

    this.rl.question('➜ ', (input) => {
      const cmd = input.trim().toLowerCase();

      if (cmd === 'l' || cmd === 'list') {
        this.showList();
      } else if (cmd === 'u' || cmd === 'undo') {
        if (this.companies.length > 0) {
          const removed = this.companies.pop();
          console.log(`\n✓ Removido: ${removed}`);
          setTimeout(() => this.askForCompany(), 1500);
        } else {
          console.log('\n✗ Nada para desfazer');
          setTimeout(() => this.askForCompany(), 1000);
        }
      } else if (cmd === 'c' || cmd === 'clear') {
        if (this.companies.length > 0) {
          const count = this.companies.length;
          this.companies = [];
          console.log(`\n✓ ${count} empresas removidas`);
          setTimeout(() => this.askForCompany(), 1500);
        } else {
          this.askForCompany();
        }
      } else if (cmd === 'd' || cmd === 'done') {
        this.finalize();
      } else if (cmd === '') {
        this.askForCompany();
      } else {
        // Treat as company name
        const validation = this.validateCompany(input);

        if (validation.valid) {
          this.companies.push(validation.name);
          console.log(`✓ Adicionado [${this.companies.length}]: ${validation.name.substring(0, 50)}`);
          setTimeout(() => this.askForCompany(), 800);
        } else {
          console.log(`✗ Rejeitado: ${validation.reason}`);
          console.log(`  Entrada: "${input.substring(0, 50)}"`);
          setTimeout(() => this.askForCompany(), 2000);
        }
      }
    });
  }

  showList() {
    this.clearScreen();

    console.log(`📋 LISTA COMPLETA (${this.companies.length} empresas)\n`);

    if (this.companies.length === 0) {
      console.log('(vazio)\n');
    } else {
      const unique = [...new Set(this.companies)];
      unique.forEach((c, i) => {
        const lineNum = String(i + 1).padStart(4, ' ');
        console.log(`${lineNum}. ${c}`);
      });
      console.log('');
    }

    this.rl.question('Pressione ENTER para voltar...', () => {
      this.askForCompany();
    });
  }

  finalize() {
    if (this.companies.length === 0) {
      console.log('\n✗ Nenhuma empresa foi adicionada.');
      this.rl.close();
      return;
    }

    // Deduplicate
    const unique = [...new Set(this.companies)].sort();

    const timestamp = new Date().toISOString().split('T')[0];
    const baseName = `EMPRESAS_COPIADAS_${timestamp}`;

    // CSV
    let csv = 'empresa;data;numero_sequencial\n';
    unique.forEach((company, idx) => {
      csv += `"${company.replace(/"/g, '""')}";${timestamp};${idx + 1}\n`;
    });

    fs.writeFileSync(`${baseName}.csv`, csv);

    // JSON
    const json = {
      timestamp: new Date().toISOString(),
      total: unique.length,
      metodo: 'manual_copy_paste_interativo',
      data_extracao: timestamp,
      empresas: unique
    };

    fs.writeFileSync(`${baseName}.json`, JSON.stringify(json, null, 2));

    // Show summary
    console.clear();
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║                     ✅ CONCLUÍDO                          ║');
    console.log('╚═══════════════════════════════════════════════════════════╝\n');

    console.log(`📊 RESUMO FINAL:`);
    console.log(`   Total adicionado: ${this.companies.length}`);
    console.log(`   Duplicatas removidas: ${this.companies.length - unique.length}`);
    console.log(`   Total único: ${unique.length}\n`);

    console.log(`📁 ARQUIVOS CRIADOS:`);
    console.log(`   ✓ ${baseName}.csv`);
    console.log(`   ✓ ${baseName}.json\n`);

    console.log(`📋 PRIMEIRAS 5 EMPRESAS:`);
    unique.slice(0, 5).forEach((c, i) => {
      console.log(`   ${i + 1}. ${c}`);
    });

    console.log(`\n💡 Próximos passos:`);
    console.log(`   1. Abra o arquivo .csv com Excel ou Google Sheets`);
    console.log(`   2. Valide e corrija nomes se necessário`);
    console.log(`   3. Importe em base de dados`);
    console.log(`   4. Adicione categorias/NIFs se precisar\n`);

    this.rl.close();
  }

  start() {
    console.clear();
    console.log('\n🚀 INICIANDO COLETOR...\n');
    setTimeout(() => this.askForCompany(), 500);
  }
}

// Start the app
const collector = new CompanyCollector();
collector.start();