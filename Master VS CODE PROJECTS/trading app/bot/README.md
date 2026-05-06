# 🤖 Bot WhatsApp - Intermediário de Vendas

Bot inteligente que monitora grupos do WhatsApp e armazena ofertas e demandas em tempo real.

## 📋 Índice Rápido

- [Início Rápido](#início-rápido)
- [Configuração Detalhada](#configuração-detalhada)
- [Comandos do Bot](#comandos-do-bot)
- [Estrutura de Dados](#estrutura-de-dados)
- [Troubleshooting](#troubleshooting)

## 🚀 Início Rápido

### 1. Instalar Node.js

Baixe em https://nodejs.org (versão LTS)

### 2. Instalar Dependências

```bash
npm install
```

**Dependências instaladas:**
- `whatsapp-web.js` - Conecta ao WhatsApp
- `qrcode-terminal` - Exibe QR Code no terminal
- `mongodb` - Banco de dados
- `dotenv` - Variáveis de ambiente

### 3. Configurar MongoDB

1. Acesse https://www.mongodb.com/cloud/atlas
2. Crie conta gratuita
3. Crie cluster M0
4. Crie usuário do banco
5. Libere acesso ao IP
6. Copie string de conexão

### 4. Configurar .env

```bash
cp .env.example .env
```

Abra `.env` e preencha:
```
MONGODB_URI=mongodb+srv://usuario:senha@cluster0.xxxxx.mongodb.net/intermediario
DB_NAME=intermediario
```

### 5. Executar Bot

```bash
npm start
```

**Esperado:**
```
✅ Conectado ao MongoDB Atlas com sucesso!
📱 Escaneie o QR Code com o WhatsApp:

    █████████████████████████
    █                     █
    █  [QR Code aqui]     █
    █                     █
    █████████████████████████

✅ Bot conectado e funcionando!
```

## ⚙️ Configuração Detalhada

### MongoDB Atlas - Passo a Passo

**Passo 1: Criar Cluster**
```
1. Acesse https://www.mongodb.com/cloud/atlas
2. Clique "Try Free"
3. Preencha: nome, email, senha
4. Escolha:
   - Plano: M0 (gratuito)
   - Provedor: AWS
   - Região: São Paulo (sa-east-1)
5. Clique "Create Cluster"
6. Aguarde 2-3 minutos
```

**Passo 2: Criar Usuário de Banco**
```
1. No cluster, clique "Database Access"
2. "Add New Database User"
3. Escolha "Password"
4. Digite:
   - Username: seu_usuario (ex: intermediario_user)
   - Password: senha_forte (ex: Tr@d1ng@pp2024!)
5. Role para baixo
6. "Database User Privileges": escolha "Read and write to any database"
7. "Add User"
```

**Passo 3: Liberar IP**
```
1. Menu: "Network Access"
2. "Add IP Address"
3. Clique "Allow Access from Anywhere"
   (Alternativa: adicionar apenas seu IP)
4. "Confirm"
```

**Passo 4: Copiar String de Conexão**
```
1. Cluster: "Connect"
2. "Connect your application"
3. Driver: "Node.js"
4. Versão: selecione a versão mais recente
5. Copie: A string parecida com:
   mongodb+srv://seu_usuario:sua_senha@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
6. Substitua:
   - <seu_usuario> pelo username
   - <sua_senha> pela senha
   - Adicione nome do banco no final: /intermediario
```

**String final esperada:**
```
mongodb+srv://seu_usuario:sua_senha@cluster0.abc123.mongodb.net/intermediario
```

### Variáveis de Ambiente

**Arquivo `.env`:**
```env
# Conexão com MongoDB
MONGODB_URI=mongodb+srv://seu_usuario:sua_senha@cluster0.abc123.mongodb.net/intermediario

# Nome do banco de dados
DB_NAME=intermediario

# Ambiente (production, development)
NODE_ENV=production
```

## 💬 Comandos do Bot

### Comandos em Mensagem Privada

**Buscar Ofertas**
```
!buscar [produto]
```
Exemplo: `!buscar cadeira`

Resposta:
```
🔍 Ofertas encontradas para "cadeira":

1. Grupo: Marketplace Local
   Mensagem: Vendo cadeira gamer, super conservada, R$ 400...
   Data: 31/03/2026 14:30

2. Grupo: Bairro das Vendas
   Mensagem: Cadeira de escritório, entrego, R$ 150...
```

**Buscar Demandas**
```
!demandas [produto]
```
Exemplo: `!demandas sofá`

**Ver Ajuda**
```
!ajuda
!help
```

### Detecção Automática de Mensagens no Grupo

O bot detecta automaticamente:

**Ofertas** (palavras-chave):
- vendo, oferta, tenho, entrego, preço, r$, valor, venda, à venda, custa, sai por

**Demandas** (palavras-chave):
- procuro, alguém tem, compro, quero, busco, preciso, comprar, procurando, alguém vende

**Exemplo:**
```
Usuário no grupo: "Vendo cadeira gamer, pouco usada, R$ 500 reais"
Bot salva: OFFER em ofertas.json

Usuário no grupo: "Procuro sofá 3 lugares, quem tem?"
Bot salva: DEMAND em demandas.json
```

## 📊 Estrutura de Dados

### Coleção: ofertas

```javascript
{
  "_id": ObjectId("..."),
  "groupId": "120123456789-1234567890@g.us",
  "groupName": "Marketplace Local",
  "sender": "5521999999999@c.us",
  "content": "Vendo cadeira gamer, super conservada, R$ 400",
  "timestamp": "2026-03-31T14:30:00.000Z",
  "originalTimestamp": "2026-03-31T14:25:00.000Z"
}
```

### Coleção: demandas

```javascript
{
  "_id": ObjectId("..."),
  "groupId": "120123456789-1234567890@g.us",
  "groupName": "Bairro das Vendas",
  "sender": "5521988888888@c.us",
  "content": "Procuro sofá 3 lugares, quem tem?",
  "timestamp": "2026-03-31T15:45:00.000Z",
  "originalTimestamp": "2026-03-31T15:40:00.000Z"
}
```

## 🧪 Testar o Bot

### Teste 1: Detectar Oferta

1. No grupo, envie: `"Vendo cadeira, R$ 100"`
2. Terminal deve mostrar: `✅ [OFFER] Salva: Vendo cadeira, R$ 100...`
3. MongoDB: collecton `ofertas` deve ter um novo documento

### Teste 2: Detectar Demanda

1. No grupo, envie: `"Procuro alguém que venda mesa"`
2. Terminal deve mostrar: `✅ [DEMAND] Salva: Procuro alguém que venda mesa...`
3. MongoDB: collection `demandas` deve ter um novo documento

### Teste 3: Buscar pelo WhatsApp

1. Envie mensagem privada: `!buscar cadeira`
2. Bot deve responder com as ofertas encontradas

## 🔍 Verificar Dados no MongoDB Atlas

**No navegador:**

1. Acesse https://cloud.mongodb.com
2. Login na sua conta
3. Clique no cluster
4. Clique **"Browse Collections"**
5. Selecione banco: `intermediario`
6. Browse `ofertas` ou `demandas`
7. Veja os documentos salvos

## 🛠️ Troubleshooting

### ❌ "Error: Cannot find module 'whatsapp-web.js'"

**Causa:** Dependências não instaladas

**Solução:**
```bash
npm install
```

Se ainda não funcionar:
```bash
npm install --force
rm -rf node_modules package-lock.json
npm install
```

---

### ❌ "MongoNetworkError: failed to connect to server"

**Causas possíveis:**
1. String de conexão incorreta
2. IP não liberado
3. Credenciais erradas

**Soluções:**
1. Verifique o `.env`:
   ```bash
   cat .env
   ```
2. Teste a conexão:
   ```bash
   node -e "const {MongoClient} = require('mongodb'); new MongoClient('SEU_LINK').connect().then(()=>console.log('✅ Conectado!')).catch(e=>console.log('❌ Erro:',e.message))"
   ```
3. MongoDB Atlas → Network Access → Confirme 0.0.0.0/0

---

### ❌ "Puppeteer failed to launch"

**Causa:** Faltam dependências do sistema (Linux)

**Solução (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y \
  gconf-service \
  libgbm-dev \
  libasound2 \
  libatk-bridge2.0-0 \
  libgtk-3-0 \
  libxss1 \
  libappindicator3-1
```

---

### ❌ "QR Code aparece mas não conecta"

**Causas:**
1. Sessão corrompida
2. Câmera não escaneou corretamente
3. WhatsApp versão incompatível

**Soluções:**
```bash
# Delete a pasta de sessão
rm -rf auth_info

# Execute novamente
npm start

# Escaneie o QR Code outra vez
```

---

### ❌ "Bot para de funcionar após algumas horas"

**Causa:** Sessão expirada por inatividade

**Solução:** Use um servidor 24/7 (Oracle Cloud, Render, Railway, etc.)

---

### ❌ "Mensagens não aparecem no MongoDB"

**Verificar:**
1. Bot está no grupo?
   ```bash
   # Digite no terminal: "node"
   # Depois: client.getChats().then(chats => console.log(chats.map(c => c.name)))
   ```

2. Mensagem contém palavras-chave?
   - Tente: `"Vendo cadeira"`

3. MongoDB está conectado?
   - Verifique logs: procure por `✅ Conectado ao MongoDB`

4. Função de classificação está funcionando?
   - Edite `index.js` e log a classificação:
   ```javascript
   const classification = classifyMessage(content);
   console.log(`Classificação: ${classification} para: "${content}"`);
   ```

---

## 📁 Estrutura do Arquivo index.js

```javascript
// 1. Imports
const { Client, LocalAuth } = require('whatsapp-web.js');

// 2. Configurações
const MONGODB_URI = process.env.MONGODB_URI;
const DB_NAME = process.env.DB_NAME;

// 3. Funções
- connectMongo()           // Conecta ao banco
- classifyMessage()        // Detecta oferta/demanda
- saveMessage()            // Salva no banco
- searchOffers()           // Busca ofertas
- searchDemands()          // Busca demandas
- formatSearchResponse()   // Formata resposta

// 4. Eventos do WhatsApp
client.on('qr', ...)              // QR Code
client.on('ready', ...)            // Bot pronto
client.on('message', ...)          // Recebe mensagem
```

## 🚀 Executar em Servidor 24/7

### Opção: Oracle Cloud (Always Free)

1. Criar conta: https://signup.cloud.oracle.com
2. Criar instância Ubuntu
3. SSH para servidor:
   ```bash
   ssh -i chave.pem ubuntu@seu_ip
   ```
4. Instalar Node.js:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```
5. Clone o repositório:
   ```bash
   git clone seu_repositorio
   cd bot
   ```
6. Instale dependências e configure `.env`
7. Use PM2 para gerenciar:
   ```bash
   sudo npm install -g pm2
   pm2 start index.js --name "whatsapp-bot"
   pm2 startup
   pm2 save
   ```

## 📝 Notas

- O bot precisa estar NO GRUPO para monitorar mensagens
- A primeira execução pode levar alguns minutos ao instalar Puppeteer
- O arquivo `auth_info` contém a sessão do WhatsApp - NÃO compartilhe
- Recomenda-se usar um número secundário pela questão de ToS

---

**Feito com ❤️ para vendedores inteligentes** 🤖
