# 🎯 Guia Rápido de Setup

Siga este guia passo a passo para configurar seu intermediário de vendas.

## ✅ Checklist de Setup

- [ ] Node.js instalado (v14+)
- [ ] Conta MongoDB Atlas criada
- [ ] String de conexão MongoDB copiada
- [ ] Arquivo `.env` do bot configurado
- [ ] Arquivo `.env.local` do painel configurado
- [ ] Dependências instaladas
- [ ] Bot iniciado com QR Code
- [ ] Painel iniciado com sucesso

## 🚀 Passo 1: Preparar MongoDB Atlas

**Tempo estimado: 10-15 minutos**

1. Acesse https://www.mongodb.com/cloud/atlas
2. Clique em "Try Free"
3. Preencha: nome, email, senha (ou entre com Google)
4. Confirme email
5. Escolha:
   - Plano: **M0** (gratuito)
   - Provedor: **AWS**
   - Região: **São Paulo** (sa-east-1)
6. Clique "Create Cluster"
7. Aguarde 2-3 minutos até ficar verde

### Criar Usuário do Banco

1. Clique em "Database Access" (menu esquerdo)
2. Clique "Add New Database User"
3. Escolha "Password"
4. Presets:
   ```
   Username: intermediario
   Password: Tr@d1ng@pp2024! (trocar depois)
   ```
5. Role para baixo
6. "Database User Privileges": selecione "Edit default custom role"
7. Escolha "Read and write to any database"
8. Clique "Add User"

### Liberar IP

1. Clique "Network Access" (menu esquerdo)
2. Clique "Add IP Address"
3. Clique "Allow Access from Anywhere" (0.0.0.0/0)
4. Clique "Confirm"

### Copiar String de Conexão

1. Volta ao cluster
2. Clique "Connect"
3. Clique "Connect your application"
4. Driver: **Node.js**
5. Copie a string (parecida com):
   ```
   mongodb+srv://intermediario:Tr@d1ng@pp2024!@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
   ```
6. **Salve** esta string em um bloco de notas

---

## 🚀 Passo 2: Instalar Dependências (Windows)

**Tempo estimado: 5-10 minutos**

### Opção A: Script Automático (Recomendado)

1. Abra PowerShell na pasta do projeto
2. Digite: `.\setup.bat`
3. Aguarde a instalação completar

### Opção B: Manual

```powershell
# Bot
cd bot
npm install
cd ..

# Painel
cd painel
npm install
cd ..
```

---

## 🚀 Passo 3: Configurar Variáveis de Ambiente

**Tempo estimado: 2 minutos**

### Bot

1. Abra `bot/.env` em um editor
2. Substitua a string de conexão:

```
MONGODB_URI=mongodb+srv://intermediario:Tr@d1ng@pp2024!@cluster0.abc123.mongodb.net/intermediario
DB_NAME=intermediario
NODE_ENV=production
```

**Importante:** Adicione `/intermediario` no final da URL!

### Painel

1. Abra `painel/.env.local` em um editor
2. Coloque a **MESMA** string:

```
MONGODB_URI=mongodb+srv://intermediario:Tr@d1ng@pp2024!@cluster0.abc123.mongodb.net/intermediario
DB_NAME=intermediario
```

---

## 🚀 Passo 4: Iniciar o Bot

**Tempo estimado: 2 minutos**

1. Abra PowerShell na pasta `bot/`
2. Digite: `npm start`
3. Você verá:
   ```
   ✅ Conectado ao MongoDB Atlas com sucesso!
   📱 Escaneie o QR Code com o WhatsApp:
   ```

### Escanear QR Code

1. Abra WhatsApp no celular
2. Toque nos 3 pontinhos → **Dispositivos vinculados**
3. **Vincular um dispositivo**
4. Aponte a câmera para o QR Code no terminal
5. Aguarde a conexão

**Esperado:** `✅ Bot conectado e funcionando!`

---

## 🚀 Passo 5: Iniciar o Painel Web

**Tempo estimado: 2 minutos**

1. **Abra um novo terminal** (não feche o bot!)
2. Navegue para `painel/`
3. Digite: `npm run dev`
4. Você verá:
   ```
   ▲ Next.js 14.0.0
   - Local:        http://localhost:3000
   ```

5. Abra no navegador: **http://localhost:3000**

---

## 🧪 Passo 6: Testar o Sistema

**Tempo estimado: 5 minutos**

### Teste 1: Armazenar Oferta

1. Vá para um grupo no WhatsApp onde o bot está
2. Envie a mensagem:
   ```
   Vendo cadeira gamer, R$ 500, em perfeito estado
   ```
3. No terminal do bot, você deve ver:
   ```
   ✅ [OFFER] Salva: Vendo cadeira gamer, R$ 500...
   ```

### Teste 2: Buscar pelo WhatsApp

1. Envie uma **mensagem privada** ao bot:
   ```
   !buscar cadeira
   ```
2. O bot deve responder com as ofertas

### Teste 3: Buscar no Painel Web

1. Abra http://localhost:3000
2. Digite "cadeira"
3. Clique "Buscar"
4. Você must ver a oferta que enviou

---

## ✅ Sucesso!

Se tudo funcionou:
- ✅ Bot conectado
- ✅ Dados salvos no MongoDB
- ✅ Busca funcionando no WhatsApp
- ✅ Painel web carregando dados

## 📚 Próximos Passos

1. **Adicionar em Grupos**: Adicione o bot aos seus grupos
2. **Customizar**: Edite palavras-chave no `index.js`
3. **Deploy**: Hospede em servidor 24/7
4. **Leia**: Consulte `README.md` para mais opções

---

## 🆘 Problemas Comuns

### Bot não conecta
- Delete a pasta `bot/auth_info/`
- Execute `npm start` novamente
- Escaneie o QR Code outra vez

### "Cannot find module"
```powershell
npm install
```

### MongoDB não conecta
- Verifique a string em `.env`
- Confirme IP 0.0.0.0/0 no MongoDB Atlas
- Teste a senha

### Painel não carrega dados
- Verifique se bot está salvando
- Confira `.env.local`
- Abra console (F12) e veja erros

---

**Feito? Parabéns! 🎉 Seu intermediário está rodando!**
