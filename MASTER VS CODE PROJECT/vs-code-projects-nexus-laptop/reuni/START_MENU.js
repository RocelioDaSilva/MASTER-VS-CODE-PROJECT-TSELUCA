const readline = require('readline');
const { exec } = require('child_process');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function showMenu() {
  console.clear();
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║     🎯 COPIAR NOMES DE EMPRESAS DO ANPG - MENU PRINCIPAL   ║');
  console.log('╚═══════════════════════════════════════════════════════════╝\n');

  console.log('Escolha um método para coletar nomes de empresas:\n');

  console.log('┌─ OPÇÃO 1: Coletor Interativo (⭐ RECOMENDADO) ─────────────┐');
  console.log('│                                                            │');
  console.log('│ Comando: node COLETOR_INTERATIVO.js                       │');
  console.log('│                                                            │');
  console.log('│ ✅ Simples e intuitivo                                     │');
  console.log('│ ✅ Valida nomes em tempo real                             │');
  console.log('│ ✅ Remove duplicatas automaticamente                       │');
  console.log('│ ✅ Mostra progresso                                        │');
  console.log('│ ✅ Permite desfazer (UNDO)                                 │');
  console.log('│ ✅ Cria CSV e JSON                                         │');
  console.log('│                                                            │');
  console.log('│ Ideal para: 100-500 empresas num workflow                 │');
  console.log('│ Tempo: ~10 minutos para 100 empresas                      │');
  console.log('└────────────────────────────────────────────────────────────┘\n');

  console.log('┌─ OPÇÃO 2: Script com Navegador Aberto ──────────────────────┐');
  console.log('│                                                             │');
  console.log('│ Comando: node ANPG_MANUAL_COPY_VIA_CONTEXT_MENU.js         │');
  console.log('│                                                             │');
  console.log('│ ✅ Abre browser automaticamente                             │');
  console.log('│ ✅ Monitora clipboard                                      │');
  console.log('│ ✅ Salva em tempo real                                      │');
  console.log('│ ⚠️  Requer ação manual no browser                          │');
  console.log('│                                                             │');
  console.log('│ Ideal para: Workflow contínuo, browser + script            │');
  console.log('└────────────────────────────────────────────────────────────┘\n');

  console.log('┌─ OPÇÃO 3: Script Simples & Direto ──────────────────────────┐');
  console.log('│                                                             │');
  console.log('│ Comando: node PASTE_COMPANY_NAMES.js                       │');
  console.log('│                                                             │');
  console.log('│ ✅ Ultrarrápido                                             │');
  console.log('│ ✅ Minimalista                                              │');
  console.log('│ ⚠️  Interface bem simples                                   │');
  console.log('│                                                             │');
  console.log('│ Ideal para: Usuários experientes                           │');
  console.log('└────────────────────────────────────────────────────────────┘\n');

  console.log('┌─ OPÇÃO 4: Ver Guia Completo ────────────────────────────────┐');
  console.log('│                                                             │');
  console.log('│ Comando: type GUIA_COPIA_MANUAL.txt                        │');
  console.log('│                                                             │');
  console.log('│ 📖 Leia instruções detalhadas em português                 │');
  console.log('└────────────────────────────────────────────────────────────┘\n');

  console.log('┌─ VOCÊ QUER... ──────────────────────────────────────────────┐');
  console.log('│                                                             │');
  console.log('│ [1] Iniciar Coletor Interativo (RECOMENDADO)               │');
  console.log('│ [2] Mouse + Browser + Script (avançado)                    │');
  console.log('│ [3] Terminal & Colar (simples)                             │');
  console.log('│ [4] Ver Guia Completo                                      │');
  console.log('│ [0] Sair                                                    │');
  console.log('│                                                             │');
  console.log('└────────────────────────────────────────────────────────────┘\n');

  rl.question('Escolha uma opção (0-4): ', (answer) => {
    handleChoice(answer.trim());
  });
}

function handleChoice(choice) {
  switch(choice) {
    case '1':
      console.log('\n🚀 Iniciando Coletor Interativo...\n');
      rl.close();
      exec('node COLETOR_INTERATIVO.js', (error) => {
        if (error) console.error('Erro:', error.message);
      });
      break;

    case '2':
      console.log('\n🚀 Iniciando Script com Browser...\n');
      rl.close();
      exec('node ANPG_MANUAL_COPY_VIA_CONTEXT_MENU.js', (error) => {
        if (error) console.error('Erro:', error.message);
      });
      break;

    case '3':
      console.log('\n🚀 Iniciando Script Simples...\n');
      rl.close();
      exec('node PASTE_COMPANY_NAMES.js', (error) => {
        if (error) console.error('Erro:', error.message);
      });
      break;

    case '4':
      console.log('\n📖 Abrindo guia...\n');
      rl.close();
      exec('type GUIA_COPIA_MANUAL.txt', (error, stdout) => {
        if (stdout) console.log(stdout);
        if (error) {
          // Fallback: try cat command
          exec('cat GUIA_COPIA_MANUAL.txt', (err, out) => {
            if (out) console.log(out);
            else console.error('Não foi possível abrir o guia');
          });
        }
      });
      break;

    case '0':
      console.log('\n👋 Até logo!\n');
      rl.close();
      break;

    default:
      console.log('\n❌ Opção inválida. Tente novamente.\n');
      setTimeout(showMenu, 1500);
  }
}

// Start
console.log('\n');
setTimeout(showMenu, 500);