const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

let companies = [];

console.log('═══════════════════════════════════════════════════════');
console.log('📋 COLA E ORGANIZA - NOMES DE EMPRESAS');
console.log('═══════════════════════════════════════════════════════\n');

console.log('INSTRUÇÕES:');
console.log('1. Copie nomes de empresas (Right-Click → Copy)');
console.log('2. Cole aqui um por um (Ctrl+V)');
console.log('3. Pressione ENTER após cada nome');
console.log('4. Digite "pronto" quando terminar');
console.log('5. Os nomes serão salvos em CSV\n');

console.log('╔═══════════════════════════════════════════════════════╗');
console.log('║  Cole o primeiro nome de empresa (ou "sair" para exit)║');
console.log('╚═══════════════════════════════════════════════════════╝\n');

function askForCompany() {
  rl.question(`Empresa ${companies.length + 1}: `, (input) => {
    const trimmed = input.trim();

    if (trimmed.toLowerCase() === 'sair' || trimmed.toLowerCase() === 'pronto') {
      finalize();
      return;
    }

    if (trimmed.length > 3) {
      companies.push(trimmed);
      console.log(`✅ Adicionado: "${trimmed}"`);
      askForCompany();
    } else if (trimmed === '') {
      console.log('⏭️  Pulado (vazio)');
      askForCompany();
    } else {
      console.log('⚠️  Nome muito curto, tente novamente');
      askForCompany();
    }
  });
}

function finalize() {
  if (companies.length === 0) {
    console.log('\n⚠️  Nenhuma empresa foi adicionada.');
    rl.close();
    return;
  }

  const timestamp = new Date().toISOString().split('T')[0];
  const baseFilename = `EMPRESAS_COPIADAS_${timestamp}`;

  // Remove duplicates and sort
  const unique = [...new Set(companies)].sort();

  // CSV
  let csvContent = 'empresa;data;fonte\n';
  unique.forEach(company => {
    csvContent += `"${company.replace(/"/g, '""')}";${timestamp};manual_copy\n`;
  });

  fs.writeFileSync(`${baseFilename}.csv`, csvContent);
  console.log(`\n✅ CSV: ${baseFilename}.csv`);

  // JSON
  const jsonData = {
    timestamp: new Date().toISOString(),
    total: unique.length,
    metodo: 'manual_copy_paste',
    empresas: unique
  };

  fs.writeFileSync(`${baseFilename}.json`, JSON.stringify(jsonData, null, 2));
  console.log(`✅ JSON: ${baseFilename}.json`);

  console.log(`\n📊 RESUMO:`);
  console.log(`   Total de empresas: ${unique.length}`);
  console.log(`   Duplicatas removidas: ${companies.length - unique.length}`);
  console.log(`   Arquivo salvo: ${baseFilename}\n`);

  console.log('Primeiras 5 empresas:');
  unique.slice(0, 5).forEach((c, i) => {
    console.log(`   ${i + 1}. ${c}`);
  });

  rl.close();
}

askForCompany();