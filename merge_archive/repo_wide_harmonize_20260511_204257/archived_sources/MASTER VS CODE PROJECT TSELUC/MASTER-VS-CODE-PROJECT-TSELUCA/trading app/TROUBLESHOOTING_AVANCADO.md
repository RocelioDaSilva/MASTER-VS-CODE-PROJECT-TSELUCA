# 🔧 Guia Avançado de Troubleshooting

Soluções detalhadas para problemas mais complexos.

## 📋 Índice

1. [Problemas de MongoDB](#problemas-de-mongodb)
2. [Problemas do Bot WhatsApp](#problemas-do-bot-whatsapp)
3. [Problemas do Painel Web](#problemas-do-painel-web)
4. [Problemas de Performance](#problemas-de-performance)
5. [Problemas de Segurança](#problemas-de-segurança)

---

## 🗄️ Problemas de MongoDB

### Erro 1: "MongoNetworkError: failed to connect"

**Possíveis causas:**
- String de conexão incorreta
- Credenciais erradas
- IP não autorizado
- Servidor MongoDB fora do ar

**Solução passo a passo:**

```bash
# 1. Verifique a string de conexão
cat bot/.env
# Procure por MONGODB_URI

# 2. Teste a conexão localmente
node
> const {MongoClient} = require('mongodb');
> const uri = 'sua_string_aqui';
> new MongoClient(uri).connect()
>   .then(() => console.log('✅ Conectado!'))
>   .catch(e => console.log('❌ Erro:', e.message));
```

**Se ainda não funcionar:**

1. **Redefinir Senha no MongoDB Atlas**
   - Acesse https://cloud.mongodb.com
   - Database Access
   - Clique em "Edit" do seu usuário
   - "Edit Password"
   - Copie a nova senha
   - Atualize em `.env`

2. **Verificar IP**
   - MongoDB → Network Access
   - Verifique se seu IP está na lista (0.0.0.0/0 para testes)
   - Se em servidor, adicione o IP do servidor

3. **Verificar Status do Cluster**
   - Clusters
   - Veja se o status está "Active" (verde)
   - Se estiver parado, clique "Resume"

---

### Erro 2: "AuthenticationError"

**Causa:** Credenciais incorretas

**Solução:**

1. Vá para MongoDB → Database Access
2. Encontre seu usuário
3. Clique "Edit"
4. Clique "Edit Password"
5. Copie a **nova** string de conexão fornecida
6. Coloque em `.env`

**Importante:** A senha mudou, use a nova string fornecida!

---

### Erro 3: "Timeout after 30000ms"

**Causa:** Conexão muito lenta

**Solução:**

```javascript
// Em bot/index.js, aumente o timeout:
const mongoClient = new MongoClient(MONGODB_URI, {
  serverSelectionTimeoutMS: 60000, // foi 30000
  connectTimeoutMS: 60000,
  socketTimeoutMS: 60000,
});
```

---

### Erro 4: "Não consigo ver os dados no MongoDB"

**Verificação:**

1. MongoDB Atlas → Databases → Browse Collections
2. Selecione o banco: `intermediario`
3. Veja as coleções: `ofertas` e `demandas`
4. Se não aparecerem:

```javascript
// Verifique no bot/index.js se está salvando
console.log('Salva na coleção:', collectionName);
```

---

## 🤖 Problemas do Bot WhatsApp

### Erro 1: "QR Code aparece mas não conecta"

**Causas:**
- Câmera não escaneou bem
- Sessão corrompida
- WhatsApp versão muito antiga

**Solução:**

```bash
# 1. Delete a sessão
rm -rf bot/auth_info/  # Linux/Mac
rmdir /s bot\auth_info\  # Windows

# 2. Execute novamente
npm start

# 3. Escaneie o QR Code LENTAMENTE
# Deixe a câmera apontada por 3-5 segundos
```

---

### Erro 2: "Puppeteer failed to launch"

**Causa:** Faltam dependências do sistema (Linux)

**Solução Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install -y \
  gconf-service \
  libgbm-dev \
  libasound2 \
  libatk-bridge2.0-0 \
  libgtk-3-0 \
  libgconf-2-4 \
  libxss1 \
  libappindicator3-1 \
  libindicator7
```

**Solução Fedora/RHEL:**

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
  libxss1 \
  pango \
  xdg-utils \
  xorg-x11-fonts-100dpi \
  xorg-x11-fonts-75dpi \
  xorg-x11-util-macros
```

---

### Erro 3: "Mensagens não aparecem no MongoDB"

**Verificação:**

1. Bot está no grupo?
```javascript
// Teste no terminal node
client.getChats().then(chats => {
  console.log(chats.map(c => c.name));
});
```

2. Mensagem contém palavras-chave?
```bash
# Adicione log em index.js
const classification = classifyMessage(content);
console.log(`Texto: "${content}" → Classificação: ${classification}`);
```

3. Banco está recebendo?
```bash
# Teste envio direto
node -e "
const {MongoClient} = require('mongodb');
const uri = 'sua_uri';
new MongoClient(uri).connect().then(async c => {
  const db = c.db('intermediario');
  const result = await db.collection('ofertas').insertOne({
    content: 'Teste',
    timestamp: new Date()
  });
  console.log('✅ Teste inserido:', result.insertedId);
  process.exit();
});
"
```

---

### Erro 4: "Bot desconecta após algumas horas"

**Causa:** Sessão expirada

**Solução:**

```javascript
// Em bot/index.js, adicione restart automático:
client.on('disconnected', reason => {
  console.log('⚠️ Desconectado:', reason);
  console.log('🔄 Reconectando em 5 segundos...');
  setTimeout(() => {
    client.initialize();
  }, 5000);
});
```

---

### Erro 5: "Error: ENOENT: no such file or directory"

**Causa:** Pasta `auth_info` foi deletada ou perdida

**Solução:**

```bash
# Delete tudo relacionado a autenticação
rm -rf bot/auth_info/  # Linux/Mac
rmdir /s bot\auth_info\  # Windows

# Reinicie com novo QR Code
npm start
```

---

## 🌐 Problemas do Painel Web

### Erro 1: "Cannot GET /"

**Causa:** Porta 3000 já em uso ou app não iniciou

**Solução:**

```bash
# Verifique porta 3000
lsof -i :3000  # Linux/Mac
netstat -ano | findstr :3000  # Windows

# Se estiver em uso, kill o processo
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Ou use outra porta
npm run dev -- -p 3001
```

---

### Erro 2: "MONGODB_URI is not defined"

**Causa:** Arquivo `.env.local` não foi criado

**Solução:**

```bash
# Crie o arquivo
cp painel/.env.local.example painel/.env.local

# Edite com suas credenciais
# ABRA: painel/.env.local
# COLOQUE: sua string de conexão
```

---

### Erro 3: "No results found" mas há dados no MongoDB

**Verificação:**

1. Dados realmente existem?
```javascript
// Terminal mongo
use intermediario
db.ofertas.find()  // Vê todos os documentos
db.ofertas.count()  // Conta documentos
```

2. Busca está correta?
```javascript
// A busca é case-insensitive, mas verifique
db.ofertas.find({ content: { $regex: 'cadeira' } })
```

3. API está retornando dados?
```bash
# Acesse no navegador
http://localhost:3000/api/search?q=cadeira
# Deve aparir JSON com os resultados
```

---

### Erro 4: "Build failed" ao fazer deploy

**Causa:** Erro no código ou dependências

**Solução:**

```bash
# Teste localmente
npm run build
npm start

# Se funciona localmente, problema é no Vercel
# Verifique o log de build na Vercel
```

---

## ⚡ Problemas de Performance

### Problema 1: Busca lenta

**Causa:** Banco tem muitos dados

**Solução:**

```javascript
// Em painel/pages/api/search.js, adicione index
const collection = db.collection(COLLECTION_OFFERS);
await collection.createIndex({ content: "text" });  // Índice de texto
// Depois use busca de texto:
const offers = await collection.find({ $text: { $search: query } });
```

---

### Problema 2: Bot pausado/lento

**Causa:** Muitas mensagens → processamento lento

**Solução:**

```javascript
// Em bot/index.js, otimize
client.on('message', async (message) => {
  try {
    // Processamento rápido
    if (!message.body.trim()) return;  // Saída rápida
    
    // Processamento assíncrono
    setTimeout(async () => {
      // Salvar no banco sem bloquear
    }, 0);
  } catch (e) {
    console.error(e);
  }
});
```

---

## 🔒 Problemas de Segurança

### Problema 1: "Senha em arquivo .env"

**Risco:** Alguém pode ver a senha

**Solução:**

```bash
# 1. Nunca faça push de .env
echo ".env" >> .gitignore

# 2. Use variáveis de ambiente do sistema
export MONGODB_URI="mongodb+srv://..."
export DB_NAME="intermediario"

# 3. Em produção, use secrets do servidor
# Vercel: Settings → Environment Variables
# Oracle Cloud: Secrets Manager
# GitHub: Settings → Secrets
```

---

### Problema 2: "Alguém pode ver os números dos participantes"

**Risco:** Privacidade

**Solução:**

```javascript
// Não salve o número no painel
// Em bot/index.js, remova sender:
const messageData = {
  groupId,
  groupName,
  // sender,  // REMOVA ESTA LINHA
  content,
  timestamp: new Date(),
};
```

---

### Problema 3: "Qualquer um pode acessar a API"

**Risco:** Dados públicos

**Solução:**

```javascript
// Em painel/pages/api/search.js, adicione autenticação
export default async function handler(req, res) {
  // Verificar token
  const token = req.headers.authorization?.split(' ')[1];
  if (token !== process.env.API_KEY) {
    return res.status(401).json({ error: 'Não autorizado' });
  }
  
  // ... resto do código
}
```

---

## 📞 Ainda com problemas?

1. **Leia os logs completos**
   ```bash
   npm start 2>&1 | tee bot.log
   # Salva todos os erros em bot.log
   ```

2. **Adicione logs detalhados**
   ```javascript
   console.log('DEBUG:', variavel);
   console.error('ERRO:', erro.message);
   ```

3. **Teste isoladamente**
   ```bash
   # Teste apenas a conexão MongoDB
   node -e "require('mongodb').MongoClient.connect(...)"
   
   # Teste apenas o bot
   npm start
   
   # Teste apenas o painel
   npm run dev
   ```

4. **Procure issues no GitHub**
   - whatsapp-web.js: https://github.com/pedroslopez/whatsapp-web.js/issues
   - Next.js: https://github.com/vercel/next.js/discussions

---

**Última ativu: 31 de março de 2026**
