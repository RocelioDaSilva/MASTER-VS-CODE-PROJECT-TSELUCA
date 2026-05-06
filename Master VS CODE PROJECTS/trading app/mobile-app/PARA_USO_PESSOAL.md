# 📱 App Pessoal - Para Você

Como este é **exclusivamente seu**, simplificamos tudo!

---

## 🎯 Versão Melhorada do App

Adicionamos:
- ✅ **Favoritos** - Toque no ❤️ para salvar ofertas
- ✅ **Histórico** - Últimas 5 buscas aparecem no home
- ✅ **Modo Online** - Funciona em qualquer Wi-Fi
- ✅ **Cache Local** - Dados em memória quando offline

---

## 🚀 3 OPÇÕES RÁPIDAS

### Opção A: Usar Online (Melhor!)
Se você quer acessar de **qualquer lugar** (não precisa estar em casa):

```powershell
# 1. Deploy do painel na Vercel (5 min, grátis)
cd painel
npm run build
# Siga em https://vercel.com/new/git (conectar GitHub)

# 2. Após deploy, copie a URL (ex: https://seu-painel.vercel.app)

# 3. Edite mobile-app\App.js linha 12:
const API_BASE_URL = 'https://seu-painel.vercel.app/api';  // ← Sua URL

# 4. Gere o APK
npx eas build --platform android

# 5. Baixe e instale no celular - Pronto!
```

**Vantagem:** Funciona em qualquer Wi-Fi, em qualquer lugar do mundo

---

### Opção B: Usar Local (Mais Rápido!)
Se você quer usar **apenas em casa no Wi-Fi:**

```powershell
# 1. Descubra seu IP
ipconfig
# Nota: 192.168.1.XXX (ou seu IP)

# 2. Edite mobile-app\App.js linha 13:
const API_BASE_URL = 'http://192.168.1.100:3000/api';  // Seu IP

# 3. Gere o APK
npx eas build --platform android

# 4. Para usar:
# Terminal 1: cd painel && npm run dev
# Terminal 2: Abra app no celular e busque
```

**Vantagem:** Mais rápido, sem delay de internet

---

### Opção C: Teste Rápido (Sem Build)
Se quer testar AGORA sem gerar APK:

```powershell
cd mobile-app
npx expo start --android
```
Escaneie o QR code com Expo Go no celular. Em 5 min está testando!

---

## 💾 Para Múltiplos Celulares Seus

Após gerar 1 APK:

1. **Compartilhe com você em outro dispositivo**
   - Via WhatsApp Web
   - Via Google Drive
   - Via AirDrop/Bluetooth
   - Via USB/Email

2. **Instale igual** em cada celular
   - Settings > Security > Unknown Sources ON
   - Toque no APK
   - Pronto!

3. **Nos seus múltiplos celulares:**
   - Todos veem os **mesmos dados** (vêm do painel)
   - Favoritos são **locais** em cada celular (cache)
   - Histórico é **local** em cada celular

---

## 🔑 Features Novas

### ❤️ Favoritos
- Toque no ❤️ de qualquer resultado
- Vira ❤️ vermelho = salvo
- Aba "Favoritos" mostra só os salvos
- Útil para ofertas que quer revisar depois

### 📜 Histórico
- Últimas 5 buscas aparecem no home
- Toque para repetir a busca
- Máximo 20 buscas guardadas

### 🌐 Online/Offline
- Funciona online (painel na Vercel)
- Funciona offline com cache local
- Tenta reconectar automaticamente

---

## 📋 Passo a Passo Rápido

### Opção A (Online - Melhor):
```bash
# 1 PASSO - Deploy painel
cd painel
npm run build
# Vercel → Conectar → Fazer deploy

# 2 PASSO - Configurar app
# Edite App.js com URL da Vercel

# 3 PASSO - Build
npx eas build --platform android

# 4 PASSO - Instalar
# Baixe APK e instale nos seus celulares
```

**Tempo: 20 min (maior parte é esperar o build)**

---

### Opção B (Local - Mais Rápido):
```bash
# 1 PASSO - Descobrir IP
ipconfig

# 2 PASSO - Editar App.js
# Linha 13: seu IP

# 3 PASSO - Build
npx eas build --platform android

# 4 PASSO - Instalar
# Baixe APK
```

**Tempo: 15 min**

---

## 🎮 Como Usar

1. **Abra o app** (ícone 🔍)
2. **Digite** o que procura (ex: "iPhone")
3. **Escolha** Ofertas ou Demandas
4. **Toque** em ❤️ para favoritar
5. **Veja** em Favoritos depois

---

## 🆘 Se algo não funciona

### "Sem conexão"
- **Online:** Internet está ligada?
- **Local:** Painel rodando (`npm run dev`)? PC e celular mesmo Wi-Fi?

### "Nenhum resultado"
- Há dados no MongoDB?
- Tente outra palavra-chave

### "Favoritos desapareceram"
- Normal - são locais por celular
- Se reinstalar o app, perde (cache local)
- Para syncronizar entre celulares, precisaria de login (não implementado)

---

## 📱 Compatibilidade

- ✅ Samsung Galaxy A33 (você)
- ✅ Qualquer Android 5.0+
- ✅ iPhone (se quiser fazer versão iOS depois)

---

## 🎁 Bônus: Adicionar Mais Celulares Seus

Todos vendo **os mesmos dados** em tempo real:

1. Gere APK uma vez
2. Compartilhe por WhatsApp/Drive/Email
3. Instale em cada celular
4. Todos conectam ao painel (online ou local)
5. Todos veem as mesmas ofertas/demandas
6. Favoritos são **por-celular** (não sincronizam) 

---

## 🚀 Próximos Passos

**5 min:** Escolher Opção A ou B  
**15 min:** Gerar APK  
**2 min:** Instalar  
**Pronto:** Usar!

---

**Qual você prefere? Opção A (online/melhor) ou B (local/mais rápido)?**

---

*Criado para seu uso pessoal - removemos todas as coisas de publicação pública!*
