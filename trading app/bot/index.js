const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const { MongoClient } = require('mongodb');
require('dotenv').config();

// ========== CONFIGURAÇÕES ==========
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb+srv://SEU_USUARIO:SUA_SENHA@cluster0.xxxxx.mongodb.net/intermediario';
const DB_NAME = process.env.DB_NAME || 'intermediario';
const COLLECTION_OFFERS = 'ofertas';
const COLLECTION_DEMANDS = 'demandas';

let db; // variável global para acesso ao banco
let mongoClient; // manter conexão aberta

// Conecta ao MongoDB
async function connectMongo() {
    try {
        mongoClient = new MongoClient(MONGODB_URI);
        await mongoClient.connect();
        db = mongoClient.db(DB_NAME);
        console.log('✅ Conectado ao MongoDB Atlas com sucesso!');
    } catch (error) {
        console.error('❌ Erro ao conectar ao MongoDB:', error.message);
        process.exit(1);
    }
}

// Classifica a mensagem como oferta, demanda, ambos ou desconhecido
function classifyMessage(text) {
    text = text.toLowerCase();
    // Palavras que indicam venda
    const sellingKeywords = [
        'vendo', 'oferta', 'tenho', 'entrego', 'preço', 'r$', 'valor', 'venda', 
        'à venda', 'vendo', 'estou vendendo', 'à disposição', 'custa', 'sai por'
    ];
    // Palavras que indicam compra
    const buyingKeywords = [
        'procuro', 'alguém tem', 'compro', 'quero', 'busco', 'preciso', 'comprar', 
        'procurando', 'estou procurando', 'alguém vende', 'tem alguém', 'preciso de'
    ];

    const isSelling = sellingKeywords.some(kw => text.includes(kw));
    const isBuying = buyingKeywords.some(kw => text.includes(kw));

    if (isSelling && !isBuying) return 'offer';
    if (isBuying && !isSelling) return 'demand';
    if (isSelling && isBuying) return 'both';
    return 'unknown';
}

// Salva a mensagem no banco
async function saveMessage(messageData, type) {
    try {
        const collectionName = (type === 'offer') ? COLLECTION_OFFERS : COLLECTION_DEMANDS;
        const collection = db.collection(collectionName);
        await collection.insertOne(messageData);
        console.log(`✅ [${type.toUpperCase()}] Salva: ${messageData.content.substring(0, 50)}...`);
    } catch (error) {
        console.error(`❌ Erro ao salvar mensagem:`, error.message);
    }
}

// Busca ofertas no banco
async function searchOffers(query) {
    try {
        const collection = db.collection(COLLECTION_OFFERS);
        const offers = await collection.find({ 
            content: { $regex: query, $options: 'i' } 
        })
        .sort({ timestamp: -1 })
        .limit(10)
        .toArray();
        return offers;
    } catch (error) {
        console.error('❌ Erro ao buscar ofertas:', error.message);
        return [];
    }
}

// Busca demandas no banco
async function searchDemands(query) {
    try {
        const collection = db.collection(COLLECTION_DEMANDS);
        const demands = await collection.find({ 
            content: { $regex: query, $options: 'i' } 
        })
        .sort({ timestamp: -1 })
        .limit(10)
        .toArray();
        return demands;
    } catch (error) {
        console.error('❌ Erro ao buscar demandas:', error.message);
        return [];
    }
}

// Formata a resposta de busca
function formatSearchResponse(results, type, query) {
    if (results.length === 0) {
        return `❌ Nenhuma ${type} encontrada para "${query}".`;
    }

    let reply = `🔍 *${type.charAt(0).toUpperCase() + type.slice(1)}s encontradas para "${query}":*\n\n`;
    results.forEach((item, i) => {
        const date = new Date(item.timestamp).toLocaleString('pt-BR');
        reply += `${i+1}. *Grupo:* ${item.groupName}\n`;
        reply += `   *Mensagem:* ${item.content.substring(0, 100)}${item.content.length > 100 ? '...' : ''}\n`;
        reply += `   *Data:* ${date}\n\n`;
    });
    return reply;
}

// Inicializa o cliente do WhatsApp
const client = new Client({
    authStrategy: new LocalAuth(),     // mantém a sessão salva no disco
    puppeteer: { 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Exibe o QR Code no terminal
client.on('qr', qr => {
    console.log('\n📱 Escaneie o QR Code com o WhatsApp:\n');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('✅ Bot conectado e funcionando!');
    console.log('📨 Aguardando mensagens nos grupos...\n');
});

client.on('authenticated', () => {
    console.log('🔓 Autenticação bem-sucedida!');
});

client.on('auth_failure', msg => {
    console.log('❌ Falha na autenticação:', msg);
});

client.on('disconnected', reason => {
    console.log('⚠️ Bot desconectado:', reason);
});

// Processa cada mensagem recebida
client.on('message', async (message) => {
    try {
        const content = message.body.trim();
        if (!content) return;

        const isGroupMessage = message.from.endsWith('@g.us');
        const isPrivateMessage = !isGroupMessage;

        // ========== COMANDO DE BUSCA (MENSAGEM PRIVADA) ==========
        if (isPrivateMessage && message.body.startsWith('!buscar')) {
            const query = message.body.slice(8).trim(); // remove "!buscar " do início
            if (!query) {
                message.reply('❌ Use: !buscar [produto]');
                return;
            }

            message.reply('🔍 Buscando ofertas...');
            const offers = await searchOffers(query);
            const reply = formatSearchResponse(offers, 'ofertas', query);
            message.reply(reply);
            return;
        }

        // ========== COMANDO DE BUSCA DEMANDAS (MENSAGEM PRIVADA) ==========
        if (isPrivateMessage && message.body.startsWith('!demandas')) {
            const query = message.body.slice(10).trim(); // remove "!demandas " do início
            if (!query) {
                message.reply('❌ Use: !demandas [produto]');
                return;
            }

            message.reply('🔍 Buscando demandas...');
            const demands = await searchDemands(query);
            const reply = formatSearchResponse(demands, 'demandas', query);
            message.reply(reply);
            return;
        }

        // ========== COMANDO DE AJUDA ==========
        if (isPrivateMessage && (message.body === '!ajuda' || message.body === '!help')) {
            const helpMessage = `
📋 *COMANDOS DISPONÍVEIS*

🔍 *!buscar [produto]*
   Busca ofertas contendo a palavra-chave

🔍 *!demandas [produto]*
   Busca demandas contendo a palavra-chave

❓ *!ajuda ou !help*
   Exibe esta mensagem

exemple:
!buscar cadeira
!demandas sofá
            `;
            message.reply(helpMessage);
            return;
        }

        // ========== ARMAZENAR MENSAGENS DE GRUPOS ==========
        if (!isGroupMessage) return; // Ignora mensagens privadas que não são comandos

        // Ignora mensagens que não são texto
        if (message.type !== 'chat') return;

        // Obtém informações do grupo
        const groupId = message.from;
        const chat = await message.getChat();
        const groupName = chat.name || 'Grupo Desconhecido';
        const sender = message.author || message.from; // autor da mensagem

        const messageData = {
            groupId,
            groupName,
            sender,
            content,
            timestamp: new Date(),
            originalTimestamp: message.timestamp ? new Date(message.timestamp * 1000) : new Date(),
        };

        const classification = classifyMessage(content);

        if (classification === 'offer') {
            await saveMessage(messageData, 'offer');
        } else if (classification === 'demand') {
            await saveMessage(messageData, 'demand');
        } else if (classification === 'both') {
            await saveMessage(messageData, 'offer');
            await saveMessage(messageData, 'demand');
        }
    } catch (error) {
        console.error('❌ Erro ao processar mensagem:', error.message);
    }
});

// Inicia o bot
(async () => {
    await connectMongo();
    client.initialize();
})();

// Graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n⏹️ Desligando bot...');
    if (mongoClient) {
        await mongoClient.close();
        console.log('✅ Conexão com MongoDB fechada');
    }
    process.exit(0);
});
