# 🌐 Painel Web - Intermediário de Vendas

Interface web moderna e responsiva para buscar ofertas e demandas.

## 📋 Índice

- [Características](#características)
- [Início Rápido](#início-rápido)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração](#configuração)
- [Deploy](#deploy)

## ✨ Características

✅ Interface moderna e responsiva
✅ Busca em tempo real
✅ Filtro por tipo (ofertas/demandas)
✅ Exibição formatada de datas
✅ Design mobile-friendly
✅ Zero dependências pesadas

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
npm install
```

### 2. Configurar Variáveis de Ambiente

```bash
cp .env.local.example .env.local
```

Abra `.env.local` e preencha:
```env
MONGODB_URI=mongodb+srv://usuario:senha@cluster0.xxxxx.mongodb.net/intermediario
DB_NAME=intermediario
```

### 3. Executar Localmente

```bash
npm run dev
```

Abra: http://localhost:3000

Você verá:
```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
```

### 4. Testar

1. Acesse http://localhost:3000
2. Digite "cadeira" na busca
3. Clique em "Buscar"
4. Veja os resultados do MongoDB

## 📁 Estrutura do Projeto

```
painel/
├── pages/
│   ├── index.js              # Página principal (formulário de busca)
│   ├── _app.js               # Wrapper da aplicação
│   ├── _document.js          # HTML base
│   └── api/
│       ├── search.js         # API de busca (ofertas)
│       └── search-demands.js # API de busca (demandas)
├── styles/
│   ├── Home.module.css       # Estilos da página
│   └── globals.css           # Estilos globais
├── public/                   # Assets estáticos
├── package.json              # Dependências
├── next.config.js            # Configuração Next.js
├── tsconfig.json             # Configuração TypeScript
└── README.md                 # Este arquivo
```

## ⚙️ Configuração Detalhada

### Variáveis de Ambiente

**Arquivo: `.env.local`**

```env
# Conexão com MongoDB
MONGODB_URI=mongodb+srv://seu_usuario:sua_senha@cluster0.abc123.mongodb.net/intermediario

# Nome do banco
DB_NAME=intermediario
```

### APIs Disponíveis

#### GET `/api/search?q=cadeira`

**Busca ofertas contendo a palavra-chave**

Request:
```
GET /api/search?q=cadeira
```

Response:
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "groupName": "Marketplace Local",
    "sender": "5521999999999@c.us",
    "content": "Vendo cadeira gamer, pouco usada",
    "timestamp": "2026-03-31T14:30:00.000Z",
    "groupId": "120123456789-1234567890@g.us"
  }
]
```

#### GET `/api/search-demands?q=sofá`

**Busca demandas contendo a palavra-chave**

Request:
```
GET /api/search-demands?q=sofá
```

Response:
```json
[
  {
    "_id": "507f1f77bcf86cd799439012",
    "groupName": "Bairro das Vendas",
    "sender": "5521988888888@c.us",
    "content": "Procuro um sofá 3 lugares",
    "timestamp": "2026-03-31T15:45:00.000Z",
    "groupId": "120123456789-1234567890@g.us"
  }
]
```

## 🎨 Customização

### Alterar Cores

Edite `styles/Home.module.css`:

```css
/* Cor primária */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Altere para suas cores preferidas */
```

### Alterar Textos

Edite `pages/index.js`:

```javascript
<h1>🏪 Intermediário de Vendas</h1>
// Mude para algo como:
<h1>🛍️ Seu Negócio Aqui</h1>
```

### Alterar Limite de Resultados

Edite `pages/api/search.js`:

```javascript
.limit(50)  // Mude para o número desejado
```

## 🧪 Testar APIs

### Usando cURL

```bash
# Buscar ofertas
curl "http://localhost:3000/api/search?q=cadeira"

# Buscar demandas
curl "http://localhost:3000/api/search-demands?q=sofá"
```

### Usando Postman

1. GET: `http://localhost:3000/api/search?q=cadeira`
2. GET: `http://localhost:3000/api/search-demands?q=sofá`

## 🚀 Deploy na Vercel (Gratuito)

### Pré-requisitos

- GitHub conta
- Vercel conta (https://vercel.com)

### Passo a Passo

**1. Fazer Push para GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/seu_usuario/painel-vendas.git
git push -u origin main
```

**2. Conectar na Vercel**

1. Acesse https://vercel.com/login
2. Clique "New Project"
3. Selecione seu repositório
4. Clique "Import"

**3. Adicionar Variáveis de Ambiente**

Na Vercel:
1. Vá para "Settings" → "Environment Variables"
2. Adicione:
   - Nome: `MONGODB_URI`
   - Valor: Sua string de conexão
3. Adicione:
   - Nome: `DB_NAME`
   - Valor: `intermediario`

**4. Deploy**

Clique "Deploy"

Sua URL será algo como: `https://painel-vendas.vercel.app`

### Deploy Automático

Após configurar no Vercel:
- Cada push para `main` faz deploy automático
- Você verá a URL em seu dashboard Vercel

## 🛠️ Troubleshooting

### ❌ "Cannot GET /"

**Causa:** Porta não está sendo ouvida

**Solução:**
```bash
npm run dev
```

### ❌ "MONGODB_URI is not defined"

**Causa:** Variável de ambiente não configurada

**Solução:**
1. Crie/atualize `.env.local`
2. Coloque sua `MONGODB_URI`
3. Reinicie: `npm run dev`

### ❌ "Error connecting to MongoDB"

**Causas possíveis:**
1. String de conexão incorreta
2. IP não liberado
3. Credenciais erradas

**Solução:**
1. Teste a string localmente
2. Verifique MongoDB Atlas → Network Access
3. Teste credenciais!

### ❌ "No results found" mas há dados

**Causas:**
1. Dados não foram salvos pelo bot
2. Busca errada (case sensitive?)
3. Dados em outra coleção

**Solução:**
1. Verifique dados no MongoDB Atlas
2. Tente buscar por palavra exata
3. Verifique se bot está salvando

## 📝 Estrutura de Página

### `pages/index.js`

```javascript
export default function Home() {
  const [query, setQuery] = useState('');      // Campo de busca
  const [results, setResults] = useState([]);  // Resultados
  const [loading, setLoading] = useState(false); // Loading state
  const [searchType, setSearchType] = useState('offers'); // Tipo de busca
  const [error, setError] = useState('');      // Mensagens de erro

  const search = async () => {
    // Chamada à API
  };

  return (
    <div>
      {/* Input de busca */}
      {/* Botões de filtro */}
      {/* Exibição de resultados */}
    </div>
  );
}
```

## 🎯 Funcionalidades

- ✅ Busca em tempo real
- ✅ Filtro por tipo
- ✅ Formatação de datas
- ✅ Tratamento de erros
- ✅ Loading state
- ✅ Responsivo (mobile + desktop)

## 📱 Responsividade

O painel funciona perfeitamente em:
- ✅ Desktop (1920px+)
- ✅ Tablet (768px+)
- ✅ Mobile (320px+)

## 🔒 Segurança

- ✅ Variáveis de ambiente não expostas
- ✅ Validação de entrada
- ✅ Conexão HTTPS na Vercel
- ✅ MongoDB Atlas com autenticação

## 🚚 Build para Produção

```bash
npm run build
npm start
```

Isso cria uma versão otimizada para produção em `.next/`

## 📊 Analytics Opcional

Para adicionar analytics (Google Analytics):

Edite `pages/_document.js`:

```javascript
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
```

---

**Feito com ❤️ para negócios online** 🌐
