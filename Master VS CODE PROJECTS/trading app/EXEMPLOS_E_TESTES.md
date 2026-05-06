# 💡 Exemplos de Uso e Testes

Exemplos práticos de como usar o sistema em diferentes cenários.

## 📱 Mensagens para Testar

### Teste 1: Detectar Oferta Simples

**Enviar no grupo:**
```
Vendo cadeira gamer, R$ 500
```

**Resultado esperado:**
- Terminal bot: `✅ [OFFER] Salva: Vendo cadeira gamer, R$ 500...`
- MongoDB: Documento adicionado em `ofertas`

---

### Teste 2: Detectar Demanda Simples

**Enviar no grupo:**
```
Procuro um sofá bom e barato
```

**Resultado esperado:**
- Terminal bot: `✅ [DEMAND] Salva: Procuro um sofá bom e barato...`
- MongoDB: Documento adicionado em `demandas`

---

### Teste 3: Oferta com Detalhes Completos

**Enviar no grupo:**
```
Vendo notebook Dell i7, 16GB RAM, 512GB SSD, pouco usado, R$ 2500. Entrego em São Paulo. Interessados? 📱
```

**Resultado esperado:**
- Salvo em `ofertas`
- Buscável por: notebook, Dell, RAM, SSD, São Paulo, etc.

---

### Teste 4: Demanda com Múltiplas Palavras-chave

**Enviar no grupo:**
```
Alguém vende cadeira de escritório? Preciso de 4 unidades, qualidade boa, R$ 200 a 300 cada
```

**Resultado esperado:**
- Salvo em `demandas`
- Detecta tanto 'vende' quanto 'preciso'

---

### Teste 5: Mensagem Ignorada (Sem Contexto de Venda)

**Enviar no grupo:**
```
Boa noite pessoal! Como estão?
```

**Resultado esperado:**
- Terminal: Sem log de OFFER ou DEMAND
- MongoDB: Não é salvo

---

## 🔍 Comandos do WhatsApp

### Teste 6: Buscar Ofertas

**Enviar em mensagem privada ao bot:**
```
!buscar cadeira
```

**Resposta esperada:**
```
🔍 Ofertas encontradas para "cadeira":

1. Grupo: Meu Grupo
   Mensagem: Vendo cadeira gamer, R$ 500...
   Data: 31/03/2026 14:30

2. Grupo: Vendas Local
   Mensagem: Cadeira de escritório, R$ 150...
   Data: 31/03/2026 15:45
```

---

### Teste 7: Buscar Demandas

**Enviar em mensagem privada ao bot:**
```
!demandas sofá
```

**Resposta esperada:**
```
🔍 Demandas encontradas para "sofá":

1. Grupo: Bairro das Vendas
   Mensagem: Procuro um sofá 3 lugares...
   Data: 31/03/2026 16:20
```

---

### Teste 8: Comando de Ajuda

**Enviar em mensagem privada:**
```
!ajuda
```

**Resposta esperada:**
```
📋 COMANDOS DISPONÍVEIS

🔍 !buscar [produto]
   Busca ofertas contendo a palavra-chave

🔍 !demandas [produto]
   Busca demandas contendo a palavra-chave

❓ !ajuda ou !help
   Exibe esta mensagem
```

---

### Teste 9: Busca Sem Resultados

**Enviar em mensagem privada:**
```
!buscar refrigerador
```

**Resposta esperada (se não houver ofertas de refrigerador):**
```
❌ Nenhuma oferta encontrada para "refrigerador".
```

---

## 🌐 Painel Web

### Teste 10: Buscar no Painel

1. Abra http://localhost:3000
2. Digite "cadeira"
3. Clique "Buscar"

**Resultado esperado:**
- Lista com todas as cadeiras encontradas
- Botões "Ofertas" e "Demandas" funcionando
- Dados atualizando em tempo real

---

### Teste 11: Filtrar por Tipo

1. Abra http://localhost:3000
2. Clique no botão "Demandas"
3. Digite "sofá"
4. Clique "Buscar"

**Resultado esperado:**
- Mostra apenas demandas
- Não mostra ofertas

---

## 🧪 Testes de Erro

### Teste 12: Busca Vazia

**Enviar em mensagem privada:**
```
!buscar
```

**Resultado esperado:**
```
❌ Use: !buscar [produto]
```

---

### Teste 13: Comando Inválido

**Enviar em mensagem privada:**
```
!comando_invalido
```

**Resultado esperado:**
- Nenhuma resposta (comando ignorado)

---

### Teste 14: Mensagem Vazia

**Enviar em mensagem privada:**
```
(enviar espaço vazio ou enter)
```

**Resultado esperado:**
- Nenhuma resposta
- Sem erro

---

## 📊 Testes de Dados

### Teste 15: Verificar MongoDB Localmente

**Via terminal:**

```bash
# Entre no terminal Node
node

# Depois:
const {MongoClient} = require('mongodb');
const uri = 'sua_string_mongodb';
const client = new MongoClient(uri);

(async () => {
  await client.connect();
  const db = client.db('intermediario');
  
  // Ver quantas ofertas
  const offerCount = await db.collection('ofertas').countDocuments();
  console.log('Total de ofertas:', offerCount);
  
  // Ver quantas demandas
  const demandCount = await db.collection('demandas').countDocuments();
  console.log('Total de demandas:', demandCount);
  
  // Ver últimas ofertas
  const offers = await db.collection('ofertas')
    .find()
    .sort({ timestamp: -1 })
    .limit(5)
    .toArray();
  console.log('Últimas ofertas:', offers);
  
  await client.close();
})();
```

---

### Teste 16: Limpar Dados de Teste

**Se quiser deletar todos os testes:**

```bash
node

# Depois:
const {MongoClient} = require('mongodb');
const uri = 'sua_string_mongodb';
const client = new MongoClient(uri);

(async () => {
  await client.connect();
  const db = client.db('intermediario');
  
  // Deletar TODAS ofertas
  await db.collection('ofertas').deleteMany({});
  console.log('✅ Todas as ofertas deletadas');
  
  // Deletar TODAS demandas
  await db.collection('demandas').deleteMany({});
  console.log('✅ Todas as demandas deletadas');
  
  await client.close();
})();
```

---

## 🔌 Testes de Conexão

### Teste 17: Testar Conexão MongoDB

```bash
node -e "
const {MongoClient} = require('mongodb');
new MongoClient('sua_string_mongodb').connect()
  .then(() => {
    console.log('✅ MongoDB conectado com sucesso!');
    process.exit(0);
  })
  .catch(e => {
    console.log('❌ Erro:', e.message);
    process.exit(1);
  });
"
```

---

### Teste 18: Testar Conexão WhatsApp

```bash
# No terminal do bot, veja:
# ✅ Conectado ao MongoDB Atlas com sucesso!
# 📱 Escaneie o QR Code...
# ✅ Bot conectado e funcionando!
```

---

### Teste 19: Testar Painel Web

```bash
# No navegador, abra:
# http://localhost:3000

# Você deve ver:
# - Título "Intermediário de Vendas"
# - Campo de busca
# - Botões de filtro
# - Sem erros no console (F12)
```

---

## 📈 Testes de Performance

### Teste 20: Inserir 100 Ofertas

```bash
node

# Depois:
const {MongoClient} = require('mongodb');
const uri = 'sua_string';
const client = new MongoClient(uri);

(async () => {
  await client.connect();
  const db = client.db('intermediario');
  const offers = [];
  
  for (let i = 1; i <= 100; i++) {
    offers.push({
      groupId: 'group-123@g.us',
      groupName: 'Teste',
      sender: '5521999999999@c.us',
      content: `Oferta teste ${i}: produto ${i}`,
      timestamp: new Date(Date.now() - i * 60000),
    });
  }
  
  const result = await db.collection('ofertas').insertMany(offers);
  console.log(`📊 ${result.insertedIds.length} documentos inseridos`);
  
  await client.close();
})();
```

Depois teste a busca:
```
!buscar produto
```

---

## 🎯 Checklist de Testes

- [ ] Oferta detectada
- [ ] Demanda detectada
- [ ] Busca de ofertas funciona
- [ ] Busca de demandas funciona
- [ ] Comando !ajuda funciona
- [ ] Painel carrega dados
- [ ] Filtro de tipo funciona
- [ ] Dados aparecem no MongoDB
- [ ] Sem erros no console
- [ ] Performance aceitável (< 1s para busca)

---

## 📝 Casos de Uso Reais

### Caso 1: Marketplace Local

**Cenário:** Grupo de vendas de um bairro

**Teste:**
1. Envie 5 ofertas variadas
2. Envie 5 demandas variadas
3. Teste busca por vários termos
4. Verifique relatório de produtos mais buscados

---

### Caso 2: Revenda de Produtos

**Cenário:** Revendedora recebendo demandas

**Teste:**
1. Adicione muitas demandas similares
2. Teste busca rápida
3. Verifique tendências

---

### Caso 3: Comunidade de Doações

**Cenário:** Grupo ofertando itens gratuitos

**Teste:**
1. Mensagens com "grátis", "doação"
2. Buscar itens específicos
3. Responder rápido aos comandos

---

## 🐛 Debug Mode

Para logs mais detalhados, edite `bot/index.js`:

```javascript
// Ative logs de debug
const DEBUG = true;

if (DEBUG) {
  console.log('DEBUG: Classificação:', classification);
  console.log('DEBUG: Conteúdo:', content);
  console.log('DEBUG: Grupo:', groupName);
}
```

---

**Todos os testes passando? Parabéns! 🎉 Sistema está 100% funcional!**
