# 🏪 Intermediário de Vendas - WhatsApp Bot

Sistema completo e gratuito para intermediar vendas e compras através do WhatsApp, com armazenamento em nuvem (MongoDB) e painel web de busca.

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação Rápida](#instalação-rápida)
- [Configuração](#configuração)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Solução de Problemas](#solução-de-problemas)
- [Próximos Passos](#próximos-passos)

## ✨ Características

✅ **Bot WhatsApp**
- Monitora grupos de WhatsApp em tempo real
- Detecta automaticamente ofertas e demandas
- Responde comandos de busca em mensagens privadas
- Armazena dados em MongoDB Atlas (gratuito)

✅ **Painel Web**
- Interface bonita e intuitiva para buscar ofertas
- Busca por palavra-chave
- Filtro por tipo (ofertas ou demandas)
- Hospedagem gratuita via Vercel

✅ **Sem Custos**
- MongoDB Atlas: 512 MB gratuitos
- Vercel: hospedagem gratuita do painel
- Oracle Cloud: servidor 24/7 gratuito para o bot

## 📦 Requisitos

- Node.js v14+ ([Baixar](https://nodejs.org))
- Conta MongoDB Atlas ([Criar](https://www.mongodb.com/cloud/atlas))
- Número de telefone (recomenda-se usar um secundário)
- WhatsApp instalado no celular

## 🚀 Instalação Rápida

### 1. Baixar o Projeto

```bash
cd "C:\Users\PCGAME\Desktop\trading app\bot"
```

### 2. Instalar Dependências

```bash
npm install
```

### 3. Configurar MongoDB

1. Acesse [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crie uma conta gratuita
3. Crie um cluster M0 (gratuito)
4. Copie a string de conexão
5. Substitua em `bot/index.js` na linha:
   ```javascript
   const MONGODB_URI = 'SEU_LINK_AQUI';
   ```

### 4. Executar o Bot

```bash
npm start
```

Você verá um QR Code no terminal. Escaneie com o WhatsApp → Dispositivos vinculados.

## ⚙️ Configuração Detalhada

### MongoDB Atlas

**Passo 1: Criar Cluster**
- URL: https://www.mongodb.com/cloud/atlas
- Clique em "Try Free"
- Escolha plano M0, AWS, região São Paulo
- Clique "Create Cluster"

**Passo 2: Criar Usuário**
- Menu esquerdo: "Database Access"
- "Add New Database User"
- Username: `seu_usuario`
- Password: `sua_senha_forte`
- "Add User"

**Passo 3: Liberar IP**
- Menu esquerdo: "Network Access"
- "Add IP Address"
- Clique "Allow Access from Anywhere"

**Passo 4: Obter String**
- Cluster: "Connect"
- "Connect your application"
- Driver: Node.js
- Copie a string e substitua `<username>` e `<password>`

### Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha:

```bash
cp .env.example .env
```

**Conteúdo do `.env`:**
```
MONGODB_URI=mongodb+srv://seu_usuario:sua_senha@cluster0.xxxxx.mongodb.net/intermediario
DB_NAME=intermediario
NODE_ENV=production
```

## 💬 Como Usar

### Armazenar Mensagens

1. Adicione o número do bot aos grupos desejados
2. O bot detecta automaticamente:
   - **Ofertas**: "Vendo...", "Oferta...", "Tenho...", etc.
   - **Demandas**: "Procuro...", "Compro...", "Quero...", etc.

### Buscar pelo WhatsApp

**Em mensagem privada**, envie:

```
!buscar [produto]
!demandas [produto]
!ajuda
```

**Exemplos:**
```
!buscar cadeira
!demandas sofá
!ajuda
```

### Buscar pelo Painel Web

Veja a seção [Painel Web](#painel-web) para mais informações.

## 📁 Estrutura do Projeto

```
trading app/
├── bot/                          # Bot WhatsApp
│   ├── index.js                  # Código principal
│   ├── package.json              # Dependências
│   ├── .env.example              # Exemplo de variáveis
│   └── auth_info/                # Sessão (criada automaticamente)
│
├── painel/                       # Painel Web (Next.js)
│   ├── pages/
│   │   ├── index.js              # Página principal
│   │   ├── _app.js               # App config
│   │   ├── _document.js          # HTML base
│   │   └── api/
│   │       ├── search.js         # API de busca (ofertas)
│   │       └── search-demands.js # API de busca (demandas)
│   ├── styles/
│   │   ├── Home.module.css       # Estilos
│   │   └── globals.css           # Estilos globais
│   ├── package.json              # Dependências
│   └── next.config.js            # Config Next.js
│
└── README.md                     # Este arquivo
```

## 🛠️ Solução de Problemas

### "Error: Cannot find module..."

**Solução:** Instale as dependências novamente
```bash
npm install
```

### "MongoNetworkError"

**Possíveis causas:**
1. String de conexão errada
2. IP não liberado no MongoDB

**Solução:**
- Verifique a string: `MONGODB_URI` em `.env`
- MongoDB Atlas → Network Access → Allow Access from Anywhere

### Puppeteer failed to launch (Linux)

**Solução:**
```bash
sudo apt-get install -y gconf-service libgbm-dev libasound2 libatk-bridge2.0-0 libgtk-3-0
```

### QR Code aparece mas não conecta

**Solução:**
1. Delete a pasta `auth_info`
2. Execute novamente: `npm start`
3. Escaneie o QR Code outra vez

### Bot para de funcionar após horas

**Solução:** Use um servidor 24/7 (veja próximos passos)

### Mensagens não aparecem no MongoDB

**Verificar:**
1. O bot está no grupo?
2. A mensagem contém palavras-chave?
3. MongoDB está conectado (verificar logs)?

## 🌐 Painel Web (Next.js)

### Instalação Local

```bash
cd painel
npm install
npm run dev
```

Abra: http://localhost:3000

### Deploy na Vercel

1. Faça push do código para GitHub
2. Acesse https://vercel.com
3. Importe o repositório
4. Adicione variável: `MONGODB_URI`
5. Deploy automático!

## 🚀 Próximos Passos

### Manter Bot 24/7

Use um servidor gratuito (Oracle Cloud, Render, Railway, etc.)

**Opção 1: Oracle Cloud (Recomendado - Always Free)**
1. Criar conta: https://signup.cloud.oracle.com
2. Criar instância Ubuntu
3. SSH para servidor
4. Clone o repositório
5. `npm install && npm start`
6. Use `pm2` para gerenciar o processo:
   ```bash
   npm install -g pm2
   pm2 start index.js --name whatsapp-bot
   pm2 startup
   pm2 save
   ```

**Opção 2: Replit**
1. Importe o repositório
2. Instale dependências
3. Configure .env
4. Run

## ⚠️ Cuidados Importantes

### Termos de Serviço

⚠️ **WhatsApp não permite bots não-oficiais**
- Use um número secundário
- Não automize envio massiço
- Normalmente não é banido, mas é risco

### Privacidade

- Avise nos grupos que está coletando dados
- Nunca exponha números de telefone
- Armazene dados com segurança

### Manutenção

- Atualize dependências: `npm update`
- Mantenha data/hora do servidor correta
- Monitore logs regularmente

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a seção [Solução de Problemas](#solução-de-problemas)
2. Leia os logs no terminal
3. Verifique a conexão MongoDB
4. Tente restartar o bot

## 📄 Licença

MIT - Use livremente!

---

**Feito com ❤️ para intermediários de vendas 🏪**
