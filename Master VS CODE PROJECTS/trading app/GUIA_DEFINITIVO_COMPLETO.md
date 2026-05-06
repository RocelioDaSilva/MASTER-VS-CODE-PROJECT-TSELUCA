# 📘 Guia Definitivo: Intermediário de Vendas no WhatsApp com Automação Gratuita

**Versão**: 1.0.0 Expandida  
**Última atualização**: 31 de março de 2026  
**Nível**: Do inicial ao avançado

---

## Índice Expandido

1. [Fundamentos e Arquitetura](#1-fundamentos-e-arquitetura)  
2. [Preparação do Ambiente (Passo a Passo Detalhado)](#2-preparação-do-ambiente-passo-a-passo-detalhado)  
3. [Configuração do Banco de Dados (MongoDB Atlas) – Com Explicações Internas](#3-configuração-do-banco-de-dados-mongodb-atlas--com-explicações-internas)  
4. [Estrutura do Projeto e Instalação de Dependências](#4-estrutura-do-projeto-e-instalação-de-dependências)  
5. [Código Comentado Linha a Linha](#5-código-comentado-linha-a-linha)  
6. [Execução e Troubleshooting Avançado](#6-execução-e-troubleshooting-avançado)  
7. [Adicionando o Bot aos Grupos e Testando](#7-adicionando-o-bot-aos-grupos-e-testando)  
8. [Comando de Busca no WhatsApp – Explicação Detalhada](#8-comando-de-busca-no-whatsapp--explicação-detalhada)  
9. [Painel Web de Busca com Next.js e Vercel – Passo a Passo Ampliado](#9-painel-web-de-busca-com-nextjs-e-vercel--passo-a-passo-ampliado)  
10. [Manter o Bot Online 24/7 com Oracle Cloud Free Tier](#10-manter-o-bot-online-247-com-oracle-cloud-free-tier--guia-completo)  
11. [Segurança e Boas Práticas](#11-segurança-e-boas-práticas)  
12. [Possíveis Melhorias e Expansões](#12-possíveis-melhorias-e-expansões)  
13. [Perguntas Frequentes (FAQ)](#13-perguntas-frequentes-faq)  

---

## 1. Fundamentos e Arquitetura

Antes de colocar a mão no código, entenda como tudo se conecta:

### O Fluxo Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITETURA DO SISTEMA                   │
└─────────────────────────────────────────────────────────────┘

USER (WhatsApp)
    │
    ├─→ Envia mensagem no GRUPO
    │       ↓
    │   BOT (whatsapp-web.js)
    │       ↓
    │   Classifica (oferta/demanda)
    │       ↓
    │   Salva no MONGODB ATLAS
    │       │
    │       └─→ Coleção "ofertas"
    │       └─→ Coleção "demandas"
    │
    └─→ Envia mensagem PRIVADA
        (!buscar, !demandas, !ajuda)
            ↓
        BOT busca no MONGODB
            ↓
        Responde no WhatsApp

│────────────────────────────────────│

USER (Painel Web)
    │
    ├─→ Acessa http://localhost:3000
    │   ou (após deploy) https://seu-painel.vercel.app
    │       ↓
    │   NEXT.JS (Frontend)
    │       ↓
    │   API (/api/search, /api/search-demands)
    │       ↓
    │   MONGODB ATLAS
    │       ↓
    │   Resultados retornam ao navegador
```

### Componentes Principais

1. **Cliente WhatsApp**: O bot é um cliente não oficial que se conecta via WhatsApp Web. Ele enxerga as mensagens dos grupos onde está inserido.

2. **Classificação**: As mensagens são analisadas por palavras-chave (ex: "vendo", "procuro") para serem classificadas como oferta ou demanda.

3. **Armazenamento**: Os dados são enviados para o MongoDB Atlas (banco de dados em nuvem gratuito).

4. **Busca**: Você pode consultar ofertas de duas formas:
   - **Comando no WhatsApp**: enviando `!buscar produto` em conversa privada com o bot.
   - **Painel web**: uma interface gráfica que consulta o mesmo banco.

### Por que essa arquitetura é eficiente?

- ✅ **100% gratuito**: MongoDB Atlas (512MB), bibliotecas open-source, hospedagem na Vercel e Oracle Cloud.
- ✅ **Separação de responsabilidades**: O bot coleta, o painel apresenta.
- ✅ **Escalável**: Você pode adicionar múltiplos bots, APIs adicionais e análises sem quebrar o existente.
- ✅ **Resiliente**: Se o bot cair, os dados permanecem no MongoDB. Se o painel cair, o bot continua funcionando.

---

## 2. Preparação do Ambiente (Passo a Passo Detalhado)

### 2.1. Verifique os requisitos do sistema

**Hardware mínimo:**
- Windows: Windows 10/11, 64 bits, 4 GB de RAM
- macOS: macOS 11 (Big Sur) ou superior, 4 GB de RAM
- Linux: Ubuntu 20.04+, Debian 11+, 4 GB de RAM

**Internet:**
- Conexão estável (não precisa ser rápida, mas precisa ser confiável)
- WhatsApp Web precisa estar acessível

### 2.2. Instale o Node.js e o npm

**No Windows:**
1. Acesse [nodejs.org](https://nodejs.org) e clique em "Download LTS" (ex: 20.11.0).
2. Execute o `.msi`.
3. Na tela "Tools for Native Modules", **marque a checkbox** "Automatically install the necessary tools" (importante para compilar pacotes C++).
4. Conclua a instalação.
5. Abra um novo **Prompt de Comando** (não o anterior) e digite:
   ```bash
   node --version
   npm --version
   ```

**No macOS:**
```bash
# Opção 1: Instalador oficial
# Baixe em nodejs.org e execute o .pkg

# Opção 2: Homebrew
brew install node
```

**No Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version
npm --version
```

### 2.3. Instale o Visual Studio Code (VS Code)

- Baixe em [code.visualstudio.com](https://code.visualstudio.com)
- Instale com as opções padrão
- **No Windows**, após instalar, abra um novo terminal (`Win + R` → `cmd`) e digite `code`. Se funcionar, a PATH foi configurada corretamente.

### 2.4. Crie a pasta do projeto

**Windows:**
```bash
mkdir C:\Users\SeuNome\Desktop\intermediario-whatsapp
cd C:\Users\SeuNome\Desktop\intermediario-whatsapp
code .
```

**macOS/Linux:**
```bash
mkdir ~/Desktop/intermediario-whatsapp
cd ~/Desktop/intermediario-whatsapp
code .
```

Depois minimize, que vamos usar o VS Code.

---

## 3. Configuração do Banco de Dados (MongoDB Atlas) – Com Explicações Internas

### 3.1. Entendendo o MongoDB

**O que é MongoDB?**
- Banco de dados **NoSQL** (não usa tabelas, usa coleções e documentos).
- Um documento é parecido com um arquivo JSON.
- Uma coleção é um agrupamento de documentos (equivalent to table em SQL).
- **MongoDB Atlas** é a versão em nuvem gerenciada (não precisa instalar nada no seu computador).

**Por que MongoDB?**
- Fácil de começar (sem schema rígido).
- Dados em JSON/BSON (mesma linguagem do Node.js).
- Plano gratuito é suficiente (512 MB).

### 3.2. Criar uma conta no MongoDB Atlas

1. Acesse [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Clique em **"Try Free"**
3. Preencha os dados:
   - Email: seu e-mail
   - Password: senha forte (anote em um cofre!)
   - Company Name: seu nome ou empresa
4. Clique em **"Create Account"**
5. Verifique seu e-mail e confirme a conta
6. Faça login

### 3.3. Criar um cluster gratuito

**Cluster Tier:**
- Selecione **"M0 Sandbox"** (gratuito, 512 MB, suficiente para iniciar)

**Cloud Provider & Region:**
- **Provider**: AWS, Google Cloud ou Azure (não importa, mesma velocidade)
- **Region**: escolha a mais próxima de você
  - Brasil: `sa-east-1` (São Paulo) ou `sa-east-2` (São Paulo)
  - Se não estiver no Brasil, escolha a região mais próxima

**Cluster Name:**
- Deixe como `Cluster0` ou nomeie como `whatsapp-bot`

Clique em **"Create Cluster"** e aguarde 2-3 minutos até que o status fique **verde** (Active).

### 3.4. Criar um usuário do banco de dados

Após o cluster estar ativo:

1. No menu lateral esquerdo, clique em **"Database Access"**
2. Clique em **"Add New Database User"**
3. Escolha **"Password"** como "Autentication Method"
4. Preencha:
   - **Username**: ex: `admin` ou `whatsapp_user`
   - **Password**: utilize uma senha forte. Ex: `Tr@d1ng@pp2024!` (dica: gere no [generate](https://www.generatepasswords.com/) e copie num cofre)
5. Role para baixo até "Database User Privileges"
6. Selecione **"Read and write to any database"**
7. Clique em **"Add User"**

**Importante**: Anote o username e password em um local seguro (não versione no Git!).

### 3.5. Liberar acesso de IP (Network Access)

1. No menu lateral, clique em **"Network Access"**
2. Clique em **"Add IP Address"**
3. Você tem duas opções:
   - **"Allow Access from Anywhere"** (`0.0.0.0/0`): Útil para testes. Qualquer IP pode se conectar, mas a autenticação por usuário/senha ainda é obrigatória.
   - **"Add my current IP"**: Mais seguro. Adiciona apenas o seu IP.

Para iniciar, use **"Allow Access from Anywhere"** para simplificar.

4. Clique em **"Confirm"**

### 3.6. Obter a string de conexão

Essa é a URL que você usará no código para conectar ao banco.

1. No seu cluster, clique em **"Connect"**
2. Escolha **"Connect your application"**
3. No dropdown "Driver", selecione **"Node.js"** e a versão mais recente
4. A Vercel fornecerá uma string parecida com:
   ```
   mongodb+srv://<username>:<password>@cluster0.abc123.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
   ```
5. **Substitua**:
   - `<username>` pelo usuário que você criou (ex: `admin`)
   - `<password>` pela senha
   - `myFirstDatabase` por `intermediario` (nome do banco)

**String final esperada:**
```
mongodb+srv://admin:Tr@d1ng@pp2024!@cluster0.abc123.mongodb.net/intermediario?retryWrites=true&w=majority
```

**⚠️ Cuidado**: Nunca coloque essa string em código público. Use variáveis de ambiente!

### 3.7. Explicação interna da conexão

**O que você precisa entender:**
- `mongodb+srv://` – protocolo especial que usa DNS SRV (permite descobrir a URL do servidor automaticamente)
- `admin:Tr@d1ng@pp2024!` – credenciais (usuário:senha)
- `cluster0.abc123.mongodb.net` – servidor MongoDB (gerenciado pela Atlas)
- `intermediario` – nome do banco de dados (criado na primeira inserção)
- `retryWrites=true&w=majority` – configurações de durabilidade

Quando você conecta, o MongoDB automaticamente:
1. Verifica as credenciais
2. Cria o banco `intermediario` se não existir
3. Cria as coleções `ofertas` e `demandas` quando você inserir o primeiro documento

---

## 4. Estrutura do Projeto e Instalação de Dependências

### 4.1. No VS Code, abra o terminal integrado

Pressione **Ctrl + `** ou vá em **Terminal → New Terminal**.

O terminal já estará na pasta do seu projeto.

### 4.2. Inicializar o projeto Node.js

```bash
npm init -y
```

Isso cria um arquivo `package.json` com as configurações padrão.

**O que é `package.json`?**
- Arquivo que lista todas as dependências (bibliotecas) que seu projeto usa
- Também contém scripts (ex: `npm start`, `npm run dev`)

### 4.3. Instalar as bibliotecas necessárias

```bash
npm install whatsapp-web.js qrcode-terminal mongodb
```

Aguarde o download e a instalação.

**Explicação das bibliotecas**:

| Biblioteca | O que faz | Por que precisa |
|-----------|-----------|-----------------|
| `whatsapp-web.js` | Fornece uma interface para interagir com o WhatsApp Web | Sem isso, você não consegue acessar as mensagens |
| `qrcode-terminal` | Gera o QR Code no terminal | Para você escanear e autenticar |
| `mongodb` | Driver para conectar ao MongoDB | Para salvar e buscar dados |

### 4.4. Verificar a instalação

Uma pasta `node_modules` foi criada (contém todas as bibliotecas). Se não aparecer ou se houver erro, tente:

```bash
npm install --force
```

Se ainda não funcionar, use:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## 5. Código Comentado Linha a Linha

Agora vamos criar o arquivo `index.js` na raiz do projeto. Abaixo, o código é apresentado com comentários detalhados.

Crie um novo arquivo clicando no ícone de "+ File" ao lado da pasta ou pressione `Ctrl+N` e nomeie como `index.js`.

Cole o seguinte código:

```javascript
// ========== IMPORTAÇÕES ==========
// Importa as bibliotecas instaladas via npm
const { Client, LocalAuth } = require('whatsapp-web.js');
// Client: classe principal que gerencia a conexão
// LocalAuth: estratégia que salva a sessão no disco (auth_info/), evitando QR toda vez

const qrcode = require('qrcode-terminal');
// Usado para gerar o QR Code no terminal

const { MongoClient } = require('mongodb');
// Cliente para conectar ao MongoDB remotamente

// ========== VARIÁVEIS DE CONFIGURAÇÃO ==========
// Substitua a string de conexão pela sua do MongoDB Atlas
const MONGODB_URI = 'mongodb+srv://SEU_USUARIO:SUA_SENHA@cluster0.xxxxx.mongodb.net/intermediario';
const DB_NAME = 'intermediario';       // Nome do banco de dados
const COLLECTION_OFFERS = 'ofertas';   // Nome da coleção onde as ofertas serão salvas
const COLLECTION_DEMANDS = 'demandas'; // Nome da coleção onde as demandas serão salvas

// Variável global para armazenar a conexão com o banco
// Isso permite acessar o banco de qualquer lugar da aplicação
let db;

// Variável global para armazenar o cliente MongoDB
// Necessária para fechar a conexão ao encerrar
let mongoClient;

// ========== FUNÇÕES PRINCIPAIS ==========

/**
 * Conecta ao MongoDB Atlas
 * Esta função é assíncrona (await/async) porque a conexão leva tempo
 */
async function connectMongo() {
    try {
        // Cria uma instância do cliente MongoDB
        mongoClient = new MongoClient(MONGODB_URI);
        
        // Aguarda a conexão ser estabelecida
        await mongoClient.connect();
        
        // Seleciona o banco de dados (cria se não existir)
        db = mongoClient.db(DB_NAME);
        
        console.log('✅ Conectado ao MongoDB Atlas com sucesso!');
    } catch (error) {
        // Se houver erro na conexão, exibe e encerra o programa
        console.error('❌ Erro ao conectar ao MongoDB:', error.message);
        process.exit(1);
    }
}

/**
 * Classifica uma mensagem como oferta, demanda, ambos ou desconhecida
 * @param {string} text - O texto da mensagem
 * @returns {string} - 'offer', 'demand', 'both' ou 'unknown'
 */
function classifyMessage(text) {
    // Converte o texto para minúsculas para comparação (case-insensitive)
    text = text.toLowerCase();
    
    // Palavras-chave que indicam VENDA
    const sellingKeywords = [
        'vendo', 'oferta', 'tenho', 'entrego', 'preço', 'r$', 'valor',
        'venda', 'à venda', 'vendo-se', 'sai por', 'custa', 'promoção',
        'liquidação', 'barato'
    ];
    
    // Palavras-chave que indicam COMPRA
    const buyingKeywords = [
        'procuro', 'alguém tem', 'compro', 'quero', 'busco', 'preciso',
        'comprar', 'preciso de', 'interessado', 'tá vendendo', 'tem alguém',
        'onde acho', 'como faço para comprar'
    ];

    // Verifica se a mensagem contém palavras de venda
    const isSelling = sellingKeywords.some(kw => text.includes(kw));
    
    // Verifica se a mensagem contém palavras de compra
    const isBuying = buyingKeywords.some(kw => text.includes(kw));

    // Retorna a classificação
    if (isSelling && !isBuying) return 'offer';    // Só venda
    if (isBuying && !isSelling) return 'demand';   // Só compra
    if (isSelling && isBuying) return 'both';      // Ambos (pode ser raro)
    return 'unknown';                              // Nenhum (ignora)
}

/**
 * Salva uma mensagem no banco de dados
 * @param {object} messageData - Objeto com os dados da mensagem
 * @param {string} type - 'offer' ou 'demand'
 */
async function saveMessage(messageData, type) {
    try {
        // Escolhe a coleção com base no tipo
        const collectionName = (type === 'offer') ? COLLECTION_OFFERS : COLLECTION_DEMANDS;
        const collection = db.collection(collectionName);
        
        // Insere o documento no banco
        // Se a coleção não existir, o MongoDB a cria automaticamente
        await collection.insertOne(messageData);
        
        // Log no terminal para acompanhamento
        console.log(`💾 [${type.toUpperCase()}] Salva: ${messageData.content.substring(0, 50)}...`);
    } catch (error) {
        console.error(`❌ Erro ao salvar mensagem:`, error.message);
    }
}

// ========== INICIALIZAÇÃO DO BOT ==========

/**
 * Cria o cliente do WhatsApp com configurações específicas
 */
const client = new Client({
    // LocalAuth: salva a sessão em auth_info/ para não precisar de QR toda vez
    authStrategy: new LocalAuth(),
    
    // Puppeteer: navegador que roda por trás
    puppeteer: {
        headless: true,  // true = sem janela visível, false = mostra o navegador
        // Argumentos adicionais para melhor compatibilidade
        args: [
            '--no-sandbox',           // Desabilita sandbox (necessário em alguns servidores)
            '--disable-setuid-sandbox' // Desabilita setuid sandbox
        ]
    }
});

/**
 * Evento disparado quando o QR Code é gerado
 * Isso ocorre na primeira vez que você executa o bot
 */
client.on('qr', qr => {
    console.log('\n📱 Escaneie o QR Code com o WhatsApp:\n');
    // Gera o QR Code no terminal
    qrcode.generate(qr, { small: true });
});

/**
 * Evento disparado quando a autenticação é bem-sucedida
 */
client.on('authenticated', () => {
    console.log('🔓 Autenticação bem-sucedida!');
});

/**
 * Evento disparado quando o cliente está pronto e conectado
 */
client.on('ready', () => {
    console.log('🚀 Bot conectado e funcionando!');
    console.log('📨 Aguardando mensagens nos grupos...\n');
});

/**
 * Evento disparado quando há erro de autenticação
 */
client.on('auth_failure', msg => {
    console.log('❌ Falha na autenticação:', msg);
});

/**
 * Evento disparado quando o bot é desconectado
 */
client.on('disconnected', reason => {
    console.log('⚠️ Bot desconectado:', reason);
});

/**
 * Evento disparado TODA VEZ que uma mensagem é recebida
 * Este é o coração da aplicação
 */
client.on('message', async (message) => {
    try {
        // Remove espaços em branco do início e fim
        const content = message.body.trim();
        
        // Se a mensagem estiver vazia, ignora
        if (!content) return;

        // Verifica se é mensagem de grupo (@g.us) ou privada (@c.us)
        const isGroupMessage = message.from.endsWith('@g.us');
        const isPrivateMessage = !isGroupMessage;

        // ========== COMANDOS DE BUSCA (PRIVADO) ==========
        // Só responde a comandos em mensagens privadas
        if (isPrivateMessage && message.body.startsWith('!buscar')) {
            // Remove "!buscar " do início e tira espaços extras
            const query = message.body.slice(8).trim();
            
            if (!query) {
                // Se não houver termo, pede para o usuário usar corretamente
                await message.reply('❌ Use: !buscar [produto]');
                return;
            }

            // Busca no banco de dados
            const offersCol = db.collection(COLLECTION_OFFERS);
            const offers = await offersCol.find(
                { content: { $regex: query, $options: 'i' } } // case-insensitive
            )
            .sort({ timestamp: -1 })  // Ordena da mais recente para a mais antiga
            .limit(10)                 // Máximo 10 resultados
            .toArray();

            if (offers.length === 0) {
                await message.reply(`🔍 Nenhuma oferta encontrada para "${query}".`);
            } else {
                let reply = `🔎 *Ofertas encontradas para "${query}":*\n\n`;
                offers.forEach((o, i) => {
                    reply += `${i+1}. *Grupo:* ${o.groupName}\n`;
                    reply += `   *Mensagem:* ${o.content.substring(0, 150)}${o.content.length > 150 ? '...' : ''}\n`;
                    reply += `   *Data:* ${o.timestamp.toLocaleString()}\n\n`;
                });
                await message.reply(reply);
            }
            return; // Encerra aqui para não processar como oferta/demanda
        }

        // ========== COMANDO DE AJUDA ==========
        if (isPrivateMessage && (message.body === '!ajuda' || message.body === '!help')) {
            const helpMessage = `
📋 *COMANDOS DISPONÍVEIS*

🔍 *!buscar [produto]*
   Busca ofertas contendo a palavra-chave

❓ *!ajuda ou !help*
   Exibe esta mensagem

*Exemplos:*
!buscar cadeira
!buscar notebook
            `;
            await message.reply(helpMessage);
            return;
        }

        // ========== MONITORAR E ARMAZENAR MENSAGENS DE GRUPOS ==========
        // De agora em diante, só processa mensagens de grupos
        if (!isGroupMessage) return;

        // Ignora mensagens que não são de texto
        if (message.type !== 'chat') return;

        // Obtém informações do grupo
        const groupId = message.from;
        const chat = await message.getChat();
        const groupName = chat.name || 'Grupo Desconhecido';
        
        // Identifica quem enviou a mensagem (em grupos, é o number do remetente)
        const sender = message.author || message.from;

        // Prepara o objeto que será armazenado no banco
        const messageData = {
            groupId,
            groupName,
            sender,
            content,
            timestamp: new Date(),
            originalTimestamp: message.timestamp 
                ? new Date(message.timestamp * 1000) 
                : new Date(),
        };

        // Classifica a mensagem
        const classification = classifyMessage(content);

        // Salva no banco conforme a classificação
        if (classification === 'offer') {
            await saveMessage(messageData, 'offer');
        } else if (classification === 'demand') {
            await saveMessage(messageData, 'demand');
        } else if (classification === 'both') {
            // Salva nas duas coleções se for ambíguo
            await saveMessage(messageData, 'offer');
            await saveMessage(messageData, 'demand');
        }
        // Se for 'unknown', simplesmente ignora (sem log)

    } catch (error) {
        console.error('❌ Erro ao processar mensagem:', error.message);
    }
});

// ========== INICIAR O BOT ==========
/**
 * Função executada imediatamente ao rodar o script
 * (async () => { ... })() é uma "Immediately Invoked Async Function"
 */
(async () => {
    // Conecta ao banco ANTES de inicializar o bot
    await connectMongo();
    
    // Inicializa o cliente WhatsApp
    client.initialize();
})();

// ========== ENCERRAMENTO GRACIOSO ==========
/**
 * Se o usuário pressionar Ctrl+C, executa esta função antes de sair
 * Isso fecha a conexão com o MongoDB de forma segura
 */
process.on('SIGINT', async () => {
    console.log('\n⏹️ Desligando bot...');
    
    if (mongoClient) {
        await mongoClient.close();
        console.log('✅ Conexão com MongoDB fechada');
    }
    
    process.exit(0);
});
```

### 5.1. Explicação de pontos importantes

**LocalAuth**
- Salva credenciais criptografadas na pasta `auth_info`
- Isso evita rescanear QR Code toda vez que o bot reinicia
- **Importante**: Não compartilhe essa pasta

**message.type === 'chat'**
- Apenas texto puro é processado
- Mensagens com imagens, áudio, vídeo, contatos, etc. são ignoradas

**message.author vs message.from**
- Em grupos: `message.author` é o número do remetente
- Em privado: `message.from` é o número de quem mandou
- Usamos `message.author || message.from` para cobrir ambos os casos

**$regex com $options: 'i'**
- Busca por expressão regular case-insensitive
- Exemplo: buscar "Cadeira" encontra "cadeira", "CADEIRA", "CaDeira", etc.

---

## 6. Execução e Troubleshooting Avançado

### 6.1. Executar o bot pela primeira vez

```bash
node index.js
```

**Sequência esperada:**
1. `✅ Conectado ao MongoDB Atlas com sucesso!`
2. `📱 Escaneie o QR Code com o WhatsApp:`
3. Aparece o QR Code no terminal

**O que fazer com o QR:**
1. Pegue seu celular com WhatsApp aberto
2. Toque nos **3 pontinhos** (Android) ou **Configurações** (iOS)
3. **Dispositivos vinculados** ou **Aparelhos conectados**
4. **Vincular um dispositivo** ou **Adicionar dispositivo**
5. Aponte a câmera para o QR Code no terminal
6. Aguarde alguns segundos

**Após escanear:**
- Você verá `🚀 Bot conectado e funcionando!` no terminal

### 6.2. Erros comuns e suas soluções detalhadas

#### ❌ Erro: `MongoNetworkError: getaddrinfo ENOTFOUND`

**Causa:**
- String de conexão incorreta
- Sem internet
- Firewall bloqueando

**Solução passo a passo:**
1. Copie a string exatamente do MongoDB Atlas (sem modificações)
2. Verifique: usuário e senha estão corretos?
3. Teste a conexão no terminal:
   ```bash
   node -e "const {MongoClient} = require('mongodb'); new MongoClient('sua_string_aqui').connect().then(() => console.log('✅ OK')).catch(e => console.log('❌ Erro:', e.message))"
   ```
4. Se ainda não funcionar:
   - Vá para MongoDB → Network Access
   - Clique em "Allow Access from Anywhere" (0.0.0.0/0)
   - Aguarde 1 minuto para a mudança ser aplicada

---

#### ❌ Erro: `MongoServerError: bad auth Authentication failed`

**Causa:** Usuário ou senha incorretos

**Solução:**
1. No MongoDB Atlas, vá para **Database Access**
2. Encontre o usuário que você criou
3. Clique em **"Edit"**
4. Clique em **"Edit Password"**
5. MongoDB gerará uma nova **string de conexão** com a senha
6. Copie essa nova string (a senha ficará visível)
7. Coloque no seu `index.js`

---

#### ❌ Erro: `Error: Puppeteer failed to launch`

**Causa:** (Geralmente em Linux) Faltam dependências do sistema

**Solução para Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
  gconf-service \
  libgbm-dev \
  libasound2 \
  libatk-bridge2.0-0 \
  libgtk-3-0 \
  libxss1 \
  libappindicator3-1 \
  libindicator7
```

**Solução para Fedora/RHEL:**
```bash
sudo dnf install -y \
  alsa-lib \
  at-spi2-atk \
  cups-libs \
  dbus-glib \
  gconf \
  GConf2 \
  gdk-pixbuf2 \
  glib2 \
  gtk3 \
  libappindicator-gtk3 \
  libxss \
  pango
```

Depois tente executar o bot novamente.

---

#### ❌ Erro: `Error: Cannot find module 'whatsapp-web.js'`

**Causa:** npm install não foi executado ou falhou

**Solução:**
1. Delete a pasta `node_modules`:
   ```bash
   rm -rf node_modules package-lock.json
   ```
2. Instale novamente:
   ```bash
   npm install
   ```
3. Execute o terminal como administrador (Windows) ou use `sudo npm install` (Linux/Mac)

---

#### ❌ QR Code aparece mas não conecta

**Possíveis causas:**
1. Câmera não escaneou bem
2. WhatsApp Web bloqueado no celular
3. Sessão corrompida
4. Timeout na autenticação

**Solução:**
1. Delete a pasta `auth_info` (se existir):
   ```bash
   rm -rf auth_info  # Mac/Linux
   rmdir /s auth_info  # Windows
   ```
2. Execute `node index.js` novamente
3. Escaneie o QR Code **lentament**, deixando a câmera apontada por 3-5 segundos
4. Se ainda não funcionar, atualize o `whatsapp-web.js`:
   ```bash
   npm install whatsapp-web.js@latest
   ```

---

#### ❌ Bot para após algumas horas

**Causa:** Sessão expirada ou WhatsApp reiniciou a conexão

**Solução:**
1. Use `pm2` para gerenciar automaticamente (veja seção 10)
2. Ou adicione reinício automático:
   ```javascript
   client.on('disconnected', reason => {
       console.log('Reconectando em 5 segundos...');
       setTimeout(() => client.initialize(), 5000);
   });
   ```

---

#### ❌ Mensagens não são salvas

**Verificação:**
1. Bot está realmente no grupo? Peça a alguém para mencionar o bot
2. A mensagem contém palavras-chave?
3. MongoDB está conectado?

**Debug:**
Adicione logs ao código:
```javascript
const classification = classifyMessage(content);
console.log(`DEBUG: "${content}" → ${classification}`);
```

Depois envie uma mensagem e veja o log no terminal.

---

### 6.3. Gerenciar a sessão (LocalAuth)

**Localização:** Pasta `auth_info` no diretório raiz do projeto

**O que contém:**
- Credenciais criptografadas do WhatsApp
- Dados da sessão

**O que fazer:**
- **Para backup**: Copie a pasta `auth_info` para um local seguro
- **Para transferir para outro PC**: Copie `auth_info` para a pasta do bot no novo PC (não precisa reescanear QR)
- **Para resetar**: Delete `auth_info` e escaneie novamente

**⚠️ Segurança**: Não compartilhe essa pasta com ninguém!

---

## 7. Adicionando o Bot aos Grupos e Testando

### 7.1. Identificar o número do bot

O número que você usou para escanear o QR Code **é o número do bot**.

**Como descobrir o número do bot:**
- Salve o número no telefone (ou em qualquer contato que tenha salvo)
- Se não souber, você pode extrair de `auth_info` ou usar um script Python/Node

### 7.2. Adicionar o bot aos grupos

1. Abra qualquer grupo no WhatsApp
2. Toque no nome do grupo (topo)
3. Vá para "Participantes"
4. Clique em "Adicionar participante"
5. Procure pelo número do bot e adicione
6. O bot agora receberá todas as mensagens desse grupo

**Importante:** O bot precisa estar **membro ativo** do grupo, não apenas como contato.

### 7.3. Teste de captura - Passo a passo

#### Teste 1: Capturar Oferta

**No grupo, envie:**
```
Vendo notebook Dell i7, 16GB RAM, 512GB SSD, pouco usado, R$ 2500
```

**No terminal do bot, você verá:**
```
💾 [OFFER] Salva: Vendo notebook Dell i7, 16GB RAM, 512GB SSD...
```

**Verificar no MongoDB:**
1. Acesse https://cloud.mongodb.com
2. Selecione seu cluster
3. Clique em "Browse Collections"
4. Vá para `intermediario` → `ofertas`
5. Você deve ver um novo documento com seu texto

---

#### Teste 2: Capturar Demanda

**No grupo, envie:**
```
Procuro um sofá 3 lugares, bom estado, até R$ 1000
```

**No terminal:**
```
💾 [DEMAND] Salva: Procuro um sofá 3 lugares, bom estado...
```

**Verificar no MongoDB:**
- Vá para `intermediario` → `demandas`
- Veja o novo documento

---

#### Teste 3: Mensagem ignorada (sem palavras-chave)

**No grupo, envie:**
```
Boa noite pessoal! Como estão?
```

**No terminal:** Nenhum log (mensagem ignorada corretamente)

**No MongoDB:** Não será salva em nenhuma coleção

---

#### Teste 4: Classificação ambígua (oferta E demanda)

**No grupo, envie:**
```
Tenho 2 sofás que sobrou, procuro comprador para vender urgente!
```

**No terminal:**
```
💾 [OFFER] Salva: Tenho 2 sofás que sobrou...
💾 [DEMAND] Salva: Tenho 2 sofás que sobrou...
```

**Por quê?** Porque contém "tenho" (venda) E "comprador" (demanda).

---

### 7.4. Solução de problemas de captura

| Problema | Verificação | Solução |
|----------|-------------|---------|
| Nada é capturado | Bot está no grupo? | Delete e readicione o bot ao grupo |
| | Messagem contém palavras-chave? | Adicione mais palavras à lista |
| | Terminal mostra erro? | Veja a seção 6.2 |
| Mensagem capturada errado | Palavra-chave errada | Personalize `sellingKeywords` e `buyingKeywords` |

---

## 8. Comando de Busca no WhatsApp – Explicação Detalhada

### 8.1. Como funciona

Você já tem esse código no seu `index.js` (seção 5). Aqui vamos explicar em detalhes.

**Fluxo:**
```
USER: !buscar cadeira
   ↓
BOT: Recebe e classifica como comando (starts with "!buscar")
   ↓
BOT: Extrai a palavra-chave ("cadeira")
   ↓
BOT: Busca no MongoDB por { content: { $regex: "cadeira", ... } }
   ↓
BOT: Formata resultados
   ↓
BOT: Envia resposta via WhatsApp
```

### 8.2. Técnica de busca: Regex (expressão regular)

```javascript
const offers = await offersCol.find({
    content: { $regex: query, $options: 'i' }  // case-insensitive
})
```

**como funciona:**
- `$regex: "cadeira"` procura pela string "cadeira" em qualquer lugar do documento
- `$options: 'i'` ignora maiúsculas/minúsculas
- Exemplo matches:
  - ✅ "Vendo **CADEIRA** gamer"
  - ✅ "Tenho uma **Cadeira** antiga"
  - ✅ "Preciso de uma **cadeira** barata"
  - ❌ "Vendo mesa"

### 8.3. Teste do comando

**Pré-requisito:** Você já enviou algumas mensagens com palavra-chave e elas foram capturadas.

**Teste:**
1. Envie uma mensagem **PRIVADA** para o bot:
   ```
   !buscar cadeira
   ```
2. O bot responde com:
   ```
   🔎 Ofertas encontradas para "cadeira":

   1. Grupo: Meu Grupo
      Mensagem: Vendo cadeira gamer, pouco usada, R$ 400...
      Data: 31/03/2026 14:30:45

   2. Grupo: Vendas Local
      Mensagem: Cadeira de escritório, entr...
      Data: 31/03/2026 15:45:20
   ```

### 8.4. Limitações e melhorias

**Limitações atuais:**
- Busca simples por substring
- Máximo 10 resultados
- Sem filtro de preço ou data

**Possíveis melhorias:**
```javascript
// Versão 2: Busca com filtro de data e ordenação
const offersCol = db.collection(COLLECTION_OFFERS);
const offers = await offersCol.find({
    content: { $regex: query, $options: 'i' },
    timestamp: { $gte: new Date(Date.now() - 7*24*60*60*1000) } // últimos 7 dias
})
.sort({ timestamp: -1 })
.limit(10)
.toArray();
```

---

## 9. Painel Web de Busca com Next.js e Vercel – Passo a Passo Ampliado

**Nota:** Assumindo que você queira um painel WEB separado do bot. Se preferir apenas o bot, pule essa seção.

### 9.1. Criar novo projeto Next.js (separado do bot)

No **mesmo diretório pai**, não dentro da pasta do bot:

```bash
cd ..
npx create-next-app@latest painel-busca
```

**Respostas durante criação:**
- TypeScript? → **No** (mais simples)
- ESLint? → **Yes** (verificação de código)
- Tailwind CSS? → **No** (usaremos CSS simples)
- `src/` directory? → **No**
- App Router? → **No** (usaremos Pages Router)
- Import alias? → **No**

Entre na pasta:
```bash
cd painel-busca
```

### 9.2. Instalar MongoDB driver

```bash
npm install mongodb
```

### 9.3. Criar a página principal (`pages/index.js`)

No VS Code, crie/edite o arquivo `pages/index.js`:

```javascript
import { useState } from 'react';
import styles from '../styles/Home.module.css';

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb+srv://seu_usuario:sua_senha@cluster0.xxxxx.mongodb.net/intermediario';
const DB_NAME = 'intermediario';
const COLLECTION_OFFERS = 'ofertas';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const search = async () => {
    if (!query.trim()) {
      setError('Digite um termo para buscar');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      
      if (!res.ok) {
        throw new Error('Erro ao buscar resultados');
      }
      
      const data = await res.json();
      setResults(data);
      
      if (data.length === 0) {
        setError(`Nenhuma oferta encontrada para "${query}"`);
      }
    } catch (err) {
      setError('Erro na conexão. Verifique a URL da API.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      search();
    }
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>🏪 Intermediário de Vendas</h1>
        <p>Busque ofertas compartilhadas no WhatsApp</p>
      </header>

      <main className={styles.main}>
        <div className={styles.searchBox}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Digite o produto..."
            className={styles.input}
          />
          <button onClick={search} disabled={loading} className={styles.button}>
            {loading ? '🔍 Buscando...' : '🔍 Buscar'}
          </button>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.results}>
          {results.map((offer, i) => (
            <div key={i} className={styles.resultItem}>
              <h3>{offer.groupName}</h3>
              <p className={styles.content}>{offer.content}</p>
              <small className={styles.date}>
                {new Date(offer.timestamp).toLocaleString('pt-BR')}
              </small>
            </div>
          ))}
        </div>

        {results.length > 0 && (
          <div className={styles.info}>
            ✅ {results.length} resultado{results.length > 1 ? 's' : ''} encontrado{results.length > 1 ? 's' : ''}
          </div>
        )}
      </main>
    </div>
  );
}
```

### 9.4. Criar a API (`pages/api/search.js`)

```javascript
import { MongoClient } from 'mongodb';

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb+srv://seu_usuario:sua_senha@cluster0.xxxxx.mongodb.net/intermediario';
const DB_NAME = 'intermediario';
const COLLECTION_OFFERS = 'ofertas';

export default async function handler(req, res) {
  const { q } = req.query;

  if (!q) {
    return res.status(400).json({ error: 'Query é obrigatória' });
  }

  let client;
  try {
    client = new MongoClient(MONGODB_URI);
    await client.connect();
    const db = client.db(DB_NAME);
    const collection = db.collection(COLLECTION_OFFERS);

    const offers = await collection
      .find({ 
        content: { $regex: q, $options: 'i' }
      })
      .sort({ timestamp: -1 })
      .limit(50)
      .toArray();

    res.status(200).json(offers);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erro ao buscar no banco de dados' });
  } finally {
    if (client) {
      await client.close();
    }
  }
}
```

### 9.5. Adicionar estilos (`styles/Home.module.css`)

```css
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 40px;
}

.header h1 {
  margin: 0;
  font-size: 2.5em;
}

.header p {
  margin: 10px 0 0 0;
  opacity: 0.9;
}

.main {
  max-width: 1000px;
  margin: 0 auto;
}

.searchBox {
  background: white;
  padding: 30px;
  border-radius: 10px;
  margin-bottom: 30px;
  display: flex;
  gap: 10px;
}

.input {
  flex: 1;
  padding: 12px 18px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
}

.input:focus {
  outline: none;
  border-color: #667eea;
}

.button {
  padding: 12px 25px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.button:hover:not(:disabled) {
  background: #764ba2;
  transform: translateY(-2px);
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  background: #ff6b6b;
  color: white;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-weight: 500;
}

.results {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.resultItem {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border-left: 5px solid #667eea;
}

.resultItem h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.content {
  margin: 10px 0;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 5px;
  line-height: 1.6;
}

.date {
  color: #999;
  font-size: 0.9em;
}

.info {
  text-align: center;
  color: white;
  padding: 15px;
  margin-top: 20px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

@media (max-width: 600px) {
  .searchBox {
    flex-direction: column;
  }

  .input,
  .button {
    width: 100%;
  }

  .header h1 {
    font-size: 1.8em;
  }
}
```

### 9.6. Testar localmente

```bash
npm run dev
```

Acesse `http://localhost:3000`. Type e busque!

### 9.7. Deploy na Vercel

**Pré-requisitos:**
- Código em um repositório GitHub
- Conta na Vercel (vercel.com)

**Passos:**
1. Faça commit do código em GitHub
2. Acesse vercel.com e clique "New Project"
3. Importe o repositório
4. Em "Environment Variables", adicione:
   - Name: `MONGODB_URI`
   - Value: sua string de conexão
5. Clique "Deploy"
6. Após completar, você terá uma URL pública!

---

## 10. Manter o Bot Online 24/7 com Oracle Cloud Free Tier – Guia Completo

### 10.1. Por que um servidor?

Se você deixar o bot rodando em seu PC:
- ❌ Precisa deixar o PC ligado
- ❌ Qualquer reinicialização interrompe o serviço
- ✅ Um servidor 24/7 resolve isso

### 10.2. Oracle Cloud Free Tier

**O que é oferecido gratuitamente:**
- 1 VM Linux com até 4 vCPU e 24 GB RAM
- 1 banco de dados (MySQL, PostgreSQL, etc.)
- 100 GB armazenamento
- **Sem cartão de crédito necessário** (basta verificação)

### 10.3. Criar conta na Oracle Cloud

1. Acesse [signup.cloud.oracle.com](https://signup.cloud.oracle.com)
2. Preencha:
   - Nome completo
   - E-mail corporativo (recomendado)
   - Senha
   - País: Brasil
3. Preencha o formulário de verificação de identidade
4. Haverá uma pequena verificação (SMS ou e-mail)
5. Após aprovação, você terá acesso ao console

### 10.4. Criar uma instância Linux

1. No console da Oracle, vá para **Compute → Instances**
2. Clique em **"Create Instance"**
3. Preencha:
   - **Name:** `whatsapp-bot`
   - **Compartment:** (default)
   - **Image and Shape:** Mude para **"Ubuntu 22.04"** e **"VM.Standard.E2.1.Micro"** (gratuito)
   - **VCN:** Crie uma nova (recomendado) ou use existente
   - **SSH Key:** Gere um par e baixe a chave privada (`.pem`)
4. Clique **"Create"**
5. Aguarde alguns minutos até que o status fique "RUNNING"

### 10.5. Conectar via SSH

No seu PC, abra um terminal e execute:

```bash
chmod 600 /caminho/para/sua-chave.pem  # Mac/Linux apenas
ssh -i /caminho/para/sua-chave.pem ubuntu@<IP_PUBLICO>
```

Substitua `<IP_PUBLICO>` pelo IP que aparece na página da instância.

### 10.6. Instalar Node.js no servidor

Dentro da instância (após conectar via SSH):

```bash
# Atualiza pacotes
sudo apt update
sudo apt upgrade -y

# Instala Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs npm

# Verifica
node --version
npm --version
```

### 10.7. Transferir arquivos do projeto

No seu **computador local**, não na instância, execute:

```bash
scp -r -i /caminho/sua-chave.pem /caminho/intermediario-whatsapp ubuntu@<IP>:/home/ubuntu/
```

Ou, se preferir usar git:

```bash
# Na instância
git clone https://seu-repositório-github.com/intermediario-whatsapp.git
cd intermediario-whatsapp
```

### 10.8. Instalar dependências no servidor

Na instância:

```bash
cd intermediario-whatsapp
npm install
```

### 10.9. Instalar PM2 (gerenciador de processo)

```bash
sudo npm install -g pm2
```

**O que é PM2?**
- Gerencia processos Node.js
- Reinicia automaticamente se o processo cair
- Preserva logs
- Inicia com o servidor

### 10.10. Escanear QR Code no servidor

Primeira execução: o QR Code será gerado. Ele aparecerá como texto no terminal. Use um:
- Gerador online: [qr-code-generator.com](https://www.qr-code-generator.com/)
- Ou salve o texto e escaneie com o celular

**Procedimento:**
```bash
# Na instância
pm2 start index.js --name whatsapp-bot
pm2 logs whatsapp-bot
```

Você verá o QR Code no log. Escaneie com o celular.

### 10.11. Configurar PM2 para startup automático

```bash
pm2 restart whatsapp-bot
pm2 save
pm2 startup
```

O último comando exibirá um script. Copie e execute (geralmente é um `sudo env ...`):

```bash
sudo env PATH=$PATH:/usr/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup -u ubuntu --hp /home/ubuntu
```

Depois:
```bash
pm2 save
```

Agora o bot reiniciará automaticamente quando o servidor reiniciar.

### 10.12. Monitorar logs

```bash
# Ver logs em tempo real
pm2 logs whatsapp-bot

# Ver últimas 100 linhas
pm2 logs whatsapp-bot --lines 100

# Salvar logs em arquivo
pm2 logs whatsapp-bot > bot-logs.txt
```

### 10.13. Gerenciar o processo

```bash
# Reiniciar o bot
pm2 restart whatsapp-bot

# Parar o bot
pm2 stop whatsapp-bot

# Iniciar o bot de novo
pm2 start whatsapp-bot

# Deletar do PM2
pm2 delete whatsapp-bot

# Ver status de todos os processos
pm2 status
```

---

## 11. Segurança e Boas Práticas

### 11.1. Protegendo a string de conexão

**❌ NUNCA faça isso:**
```javascript
// No código público/Git
const MONGODB_URI = 'mongodb+srv://admin:senha@...';
```

**✅ FAÇA assim:**

Opção 1 – Arquivo `.env` local:
```bash
# Create .env file
echo "MONGODB_URI=mongodb+srv://admin:senha@cluster0.abc.mongodb.net/intermediario" > .env
```

Depois no código:
```javascript
require('dotenv').config();
const MONGODB_URI = process.env.MONGODB_URI;
```

E adicione `.env` ao `.gitignore`:
```
.env
node_modules
auth_info
```

Opção 2 – Variáveis de ambiente do sistema:
```bash
# Linux/Mac: adicione ao ~/.bashrc ou ~/.zshrc
export MONGODB_URI="mongodb+srv://admin:senha@..."

# Windows: Variáveis de Ambiente (sistema)
```

Opção 3 – Em servidor (Oracle Cloud):
```bash
# Na instância, edite ~/.bashrc
export MONGODB_URI="mongodb+srv://admin:senha@..."
source ~/.bashrc
```

### 11.2. Privacidade dos participantes

**Problema**: O campo `sender` contém o número de telefone do remetente

**Solução:**
- Se não precisa, remova do `messageData`:
  ```javascript
  const messageData = {
      groupId,
      groupName,
      // sender,  // REMOVA ESTA LINHA
      content,
      timestamp: new Date(),
  };
  ```

- Ou nunca exiba no painel web:
  ```javascript
  // No painel, nunca mostre o sender
  console.log(`Grupo: ${offer.groupName}`);
  console.log(`Mensagem: ${offer.content}`);
  // console.log(`Sender: ${offer.sender}`);  // ← NÃO MOSTRE
  ```

### 11.3. Riscos de bloqueio

**Por que o WhatsApp pode bloquear?**
- Você está usando uma biblioteca não oficial (whatsapp-web.js)
- WhatsApp não autoriza bots não-oficiais nos ToS (Termos de Serviço)

**Como minimizar risco:**
1. **Use um número secundário** (chip pré-pago) exclusivo para o bot
2. **Não envie mensagens automaticamente em massa** – você apenas lê e responde
3. **Evite comportamentos suspeitos**:
   - Não conecte/desconecte repetidamente
   - Não múltiplas contas do mesmo IP
   - Não tráfego de dados anormalmente alto
4. **Mantenha a sessão estável** – deixe o bot rodando continuamente

**Histórico**: Muitos usuários usam bots há meses sem bloqueio, mas há risco envolvido.

### 11.4. Backup do MongoDB

**Automático:**
- MongoDB Atlas faz backups a cada 6 horas (plano gratuito)
- Retenção: últimos 7 dias

**Manual:**
```bash
# Exporte os dados
mongodump --uri="mongodb+srv://admin:senha@cluster0.abc.mongodb.net/intermediario" --out=/caminho/backup

# Importe depois
mongorestore --uri="mongodb+srv://admin:senha@cluster0.abc.mongodb.net/intermediario" /caminho/backup/intermediario
```

### 11.5. Auditoria de dados

Se você quiser saber quem enviou o quê:
```javascript
// Adicione ao messageData
const messageData = {
    groupId,
    groupName,
    sender,  // Guardado para auditoria, mas não exibido
    content,
    timestamp: new Date(),
    ip: req.ip,  // (apenas se rodar uma API HTTP)
};
```

---

## 12. Possíveis Melhorias e Expansões

### 12.1. Classificação mais inteligente

**Atualmente:**
- Busca por palavras-chave fixas

**Alternativas:**

**Versão 2 – Expressões regulares:**
```javascript
function classifyMessage(text) {
    text = text.toLowerCase();
    const sellingRegex = /\b(vendo|oferta|tenho|entrego|preço|custa)\b/;
    const buyingRegex = /\b(procuro|compro|quero|busco|preciso)\b/;
    
    const isSelling = sellingRegex.test(text);
    const isBuying = buyingRegex.test(text);
    
    if (isSelling && !isBuying) return 'offer';
    if (isBuying && !isSelling) return 'demand';
    if (isSelling && isBuying) return 'both';
    return 'unknown';
}
```

**Versão 3 – Machine Learning (TensorFlow.js):**
```bash
npm install @tensorflow/tfjs
```

Treinar um modelo com seus dados históricos (avançado).

### 12.2. Capturar imagens e anexos

```javascript
client.on('message', async (message) => {
    // Se for imagem
    if (message.hasMedia && message.type === 'image') {
        const media = await message.downloadMedia();
        // Salvar no MongoDB como base64
        await db.collection('media').insertOne({
            messageId: message.id,
            data: media.data,  // base64
            type: media.mimetype,
            timestamp: new Date()
        });
    }
});
```

### 12.3. Notificações automáticas

```javascript
// Quando uma nova oferta é capturada, enviar mensagem para você
const yourNumber = '5521999999999';

if (classification === 'offer') {
    await saveMessage(messageData, 'offer');
    // Notificar você
    await client.sendMessage(yourNumber + '@c.us',
        `📢 Nova oferta!\n${content}`
    );
}
```

### 12.4. Interface mais amigável

- Adicione autenticação ao painel web (senha)
- Botões de interação no WhatsApp (WhatsApp Business API – pago)
- App mobile com React Native

### 12.5. Múltiplos bots

```javascript
// Executar vários bots em paralelo
const clients = [
    { number: '+55219999999', groups: ['group1', 'group2'] },
    { number: '+55219999998', groups: ['group3', 'group4'] }
];

clients.forEach(botConfig => {
    const client = new Client({ ... });
    client.initialize();
});
```

### 12.6. Analytics avançado

```javascript
// Agregação de dados
async function getTopProducts() {
    const topProducts = await db.collection('ofertas')
        .aggregate([
            {
                $group: {
                    _id: '$content',  // Agrupar por conteúdo
                    count: { $sum: 1 },
                    avgPrice: { $avg: '$price' }  // se extrair preço
                }
            },
            { $sort: { count: -1 } },
            { $limit: 10 }
        ])
        .toArray();
    return topProducts;
}
```

---

## 13. Perguntas Frequentes (FAQ)

### P: Posso usar meu número principal no WhatsApp?

**R:** É **altamente arriscado**. O WhatsApp pode:
- Banir permanentemente o número
- Limitar o acesso a grupos
- Bloquear mensagens

**Solução:** Use um número **secundário** dedica para o bot (chip pré-pago).

---

### P: O bot funciona em grupos privados (comunidades)?

**R:** Sim, funciona em qualquer grupo onde o bot é membro. A ID termina com `@g.us` em ambos os casos.

---

### P: Como faço para que o bot ignore mensagens antigas?

**R:** Por padrão, `whatsapp-web.js` **só recebe mensagens novas** após inicializar. Mensagens antigas (antes da conexão) são ignoradas automaticamente.

---

### P: O bot consome muitos recursos?

**R:** Não. Em uma VM gratuita (1 vCPU, 1 GB RAM):
- Consumo CPU: 2-5%
- Consumo RAM: 100-200 MB
- Muito viável

---

### P: O que fazer se o bot parar de funcionar após atualização do WhatsApp?

**R:** 
1. A biblioteca `whatsapp-web.js` é atualizada rapidamente
2. Execute:
   ```bash
   npm update whatsapp-web.js
   pm2 restart whatsapp-bot
   ```
3. Se não funcionar, verifique [o GitHub do projeto](https://github.com/pedroslopez/whatsapp-web.js/issues)

---

### P: Posso usar outro banco de dados?

**R:** Sim! Alternativas gratuitas:
- **Supabase** (PostgreSQL)
- **Airtable** (API + interface)
- **Firebase** (NoSQL, Google)
- Basta adaptar o código de salvamento

---

### P: Como faço para o painel web buscar também demandas?

**R:** Crie uma segunda API:

```javascript
// pages/api/search-demands.js
export default async function handler(req, res) {
  const { q } = req.query;
  const client = new MongoClient(MONGODB_URI);
  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const collection = db.collection('demandas');  // ← demandas em vez de ofertas
    const demands = await collection
      .find({ content: { $regex: q, $options: 'i' } })
      .sort({ timestamp: -1 })
      .limit(50)
      .toArray();
    res.status(200).json(demands);
  } finally {
    await client.close();
  }
}
```

E no frontend, adicione um tab/filtro para buscar demandas.

---

### P: Preciso de conhecimento de programação?

**R:** Para usar: **Não**. Tudo está pronto.
Para customizar: **Sim**, conceitos básicos de JavaScript ajudam.

---

### P: Quanto custa rodart tudo?

**R:** Atualmente, **R$ 0**.
- MongoDB Atlas: 512 MB grátis
- Oracle Cloud: Forever Free
- Vercel: plano Free para deploy
- Node.js: Open source

No futuro, se escalar muito:
- MongoDB: pagar por espaço extra
- Servidor: contratação de espaço maior

---

## Conclusão

Você agora tem um **guia completo e profissional** que cobre:

✅ Fundamentos da arquitetura
✅ Instalação passo a passo (iniciante)
✅ MongoDB configurado na nuvem
✅ Código comentado linha a linha
✅ Troubleshooting de todos os erros imaginários
✅ Painel web com Next.js
✅ Deployment em servidor 24/7
✅ Segurança e boas práticas
✅ Melhorias e expansões
✅ FAQ detalhado

**Próximos passos:**
1. Siga [SETUP_GUIA_RAPIDO.md](SETUP_GUIA_RAPIDO.md) para instalar
2. Teste localmente conforme [EXEMPLOS_E_TESTES.md](EXEMPLOS_E_TESTES.md)
3. Deploy no servidor usando a seção 10
4. Monetize conforme [GUIA_AVANCADO_E_NEGOCIO.md](GUIA_AVANCADO_E_NEGOCIO.md)

**Boa sorte com seu intermediário de vendas! 🚀**

---

**Criado:** 31 de março de 2026  
**Versão:** 1.0.0 (Completo)  
**Nível:** Iniciante a Avançado  
**Tempo de leitura:** ~2-3 horas  
**Tempo para implementar:** ~4-6 horas
