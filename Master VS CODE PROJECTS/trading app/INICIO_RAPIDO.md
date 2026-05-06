# ⚡ INÍCIO RÁPIDO (5 MINUTOS)

Seu projeto está 100% pronto. Siga estes passos:

---

## PASSO 1: Abra o Painel Web (AGORA)
```
🌐 http://localhost:3000
```
✅ O painel já está rodando! Abra no navegador.
*(Sem MongoDB, a busca não retorna resultados - isso é normal)*

---

## PASSO 2: Crie MongoDB (5 minutos)

1. Acesse: https://www.mongodb.com/cloud/atlas
2. Clique "Sign Up" ou "Log In"
3. Preencha dados e crie conta
4. Clique "Create a Deployment" → M0 (Free)
5. Escolha AWS → São Paulo (sa-east-1)
6. Clique "Create Cluster"
7. Aguarde (2-3 minutos)
8. Menu esquerdo: "Database Access" → "Add New Database User"
   - Username: `admin`
   - Password: `senhaForte123!`
   - Clique "Add User"
9. Menu esquerdo: "Network Access" → "Add IP Address"
   - Clique "Allow Access from Anywhere"
   - Clique "Confirm"
10. Volte ao cluster, clique "Connect" → "Connect your application"
    - Selecione Node.js
    - Copie a string (example: mongodb+srv://admin:senhaForte123!@cluster0.abc.mongodb.net/)
    - **No final da string, adicione `/intermediario`**
    - String final: `mongodb+srv://admin:senhaForte123!@cluster0.abc.mongodb.net/intermediario`

---

## PASSO 3: Configure os Arquivos .env (2 minutos)

### Arquivo 1: `bot/.env`
Localize: `C:\Users\PCGAME\Desktop\trading app\bot\.env`

Substitua TODO o conteúdo por:
```
MONGODB_URI=mongodb+srv://admin:senhaForte123!@cluster0.abc.mongodb.net/intermediario
DB_NAME=intermediario
NODE_ENV=production
```
*(Cole a string que você copiou do MongoDB)*

Salve (Ctrl+S).

### Arquivo 2: `painel/.env.local`
Localize: `C:\Users\PCGAME\Desktop\trading app\painel\.env.local`

Substitua TODO o conteúdo por:
```
MONGODB_URI=mongodb+srv://admin:senhaForte123!@cluster0.abc.mongodb.net/intermediario
```
*(Mesma string do MongoDB)*

Salve (Ctrl+S).

---

## PASSO 4: Inicie o Bot (novo terminal)

Abra PowerShell/CMD nova janela e execute:
```powershell
cd "C:\Users\PCGAME\Desktop\trading app\bot"
npm start
```

Espere aparecer:
```
📱 Escaneie o QR Code com o WhatsApp:
```

Com seu celular:
1. Abra WhatsApp
2. Configurações (⚙️) → Dispositivos vinculados
3. Adicionar dispositivo
4. Aponte câmera para o QR Code no terminal
5. Espere conectar

Deve aparecer: `🚀 Bot conectado e funcionando!`

---

## PASSO 5: Teste! (3 minutos)

### Teste 1: Envie mensagem em um grupo
```
Grupo no WhatsApp: "Vendo notebook, R$ 2500"
```
No terminal do bot, aparecerá:
```
💾 [OFFER] Salva: Vendo notebook, R$ 2500...
```

### Teste 2: Busque no WhatsApp (privado)
Envie mensagem PRIVADA ao bot:
```
!buscar notebook
```
Bot responde com a oferta que você enviou no grupo.

### Teste 3: Busque no Painel Web
Acesse: http://localhost:3000
- Digite: `notebook`
- Clique: `📤 Ofertas`
- Clique: `Buscar`
- Veja a oferta aparecer!

---

## ✅ PRONTO!

Seu sistema está:
- ✅ Bot monitorando WhatsApp
- ✅ Painel web buscando dados
- ✅ MongoDB armazenando mensagens
- ✅ Tudo funcionando integrado

---

## 🆘 Erros?

Veja: `TROUBLESHOOTING_AVANCADO.md`

---

## 📚 Leia depois

1. `ENTREGA_FINAL.md` - Resumo completo
2. `GUIA_DEFINITIVO_COMPLETO.md` - Aprofundamento
3. `GUIA_AVANCADO_E_NEGOCIO.md` - Monetizar seu projeto

---

**Tempo total**: ~25 minutos  
**Dificuldade**: Fácil  
**Resultado**: Sistema completo 24/7 funcionando! 🚀

Aprovente seu projeto! 🎉
