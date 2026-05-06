# 📱 Guia Completo: APK para Samsung Galaxy A33

## 🎯 Objetivo

Transformar o app React Native em um arquivo `.apk` que você pode instalar direto no seu Samsung Galaxy A33 como qualquer outro app.

---

## 📋 Pré-requisitos

- ✅ Node.js v18+ (você já tem)
- ✅ npm v9+ (você já tem)
- ✅ Conta Expo grátis (5 min para criar)
- ✅ Samsung Galaxy A33 com Android 5.0+ (seu celular tem)
- ✅ Computador com acesso à internet

---

## 🚀 FORMA MAIS RÁPIDA (Recomendada)

### Opção A: Build via Nuvem Expo (Sem instalar nada extra)

**Tempo: ~15 minutos** ⏱️

#### Passo 1: Crie uma conta Expo (1 min)
1. Acesse: https://expo.dev/signup
2. Inscreva-se com email/Google
3. Confirme o email
4. Guarde o username e senha

#### Passo 2: Instale dependências do app (3 min)
```powershell
cd "c:\Users\PCGAME\Desktop\trading app\mobile-app"
npm install
```

#### Passo 3: Faça login no Expo (1 min)
```powershell
npx expo login
# Digite seu email/username e senha
```

#### Passo 4: Inicie o build na nuvem (10 min)
```powershell
npx eas build --platform android
```

**O que acontece:**
- Expo faz o build automaticamente em seus servidores
- Você vê o progresso no terminal
- Um APK `.apk` é criado
- Um link para baixar aparece no terminal e no https://expo.dev/dashboard

#### Passo 5: Baixe o APK
```
✅ Android app build finished!
📱 Android app: https://expo.dev/artifacts/xxxxxxx
```

Clique no link ou vá em https://expo.dev/dashboard → Builds → Download

---

## 🔧 FORMA ALTERNATIVA (Se o build cloud não funcionar)

### Opção B: Build Local com EAS CLI

**Tempo: ~20 minutos** ⏱️

```powershell
cd mobile-app
npm install
npx eas build --platform android --local
```

Requer ~5GB de espaço livre em disco.

---

## 💻 FORMA EXPERT (Build total local)

### Opção C: Compilar com Android Studio

**Tempo: ~1 hora** ⏱️

```powershell
cd mobile-app
npx expo prebuild --clean
npm run build-local
```

Requer: Android SDK (5GB), JDK, Gradle.

---

## 📥 Como Instalar o APK no Samsung Galaxy A33

### Método 1: Via USB (Recomendado)

**Passo 1: Transfira o APK**
1. Conecte o Samsung no PC via USB
2. Espere aparecer a conexão USB
3. Copie o arquivo `buscador-ofertas-xxxxx.apk` para a pasta Downloads do celular

**Passo 2: Instale**
1. No celular, abra Arquivos
2. Vá para Downloads
3. Toque em `buscador-ofertas-xxxxx.apk`
4. Toque em "Instalar"
5. Se pedir permissão, toque "Instalar"
6. Aguarde 30-60 segundos

**Pronto!** O app aparecerá na tela inicial com ícone 🔍

### Método 2: Via Google Drive

1. Faça upload do APK para Google Drive
2. No celular, acesse Drive
3. Toque no arquivo → "Download"
4. Toque nele para instalar

### Método 3: Via QR Code (Mais fácil)

Expo gera um QR code. Você pode compartilhá-lo assim:

```powershell
# Depois de gerar o APK
npx eas build:list --platform android
# Copie o link e crie um QR code em: qr-code-generator.com
```

---

## ⚙️ Configuração do App (Importante!)

### Para celular físico no mesmo Wi-Fi:

**Passo 1: Descubra o IP do seu PC**
```powershell
ipconfig
```

Procure por algo como:
```
IPv4 Address . . . . . . . . . . . : 192.168.1.100
```
(Anote esse número)

**Passo 2: Abra o arquivo `App.js` em:**
```
c:\Users\PCGAME\Desktop\trading app\mobile-app\App.js
```

**Passo 3: Na linha 17, substitua:**
```javascript
// ANTES:
const API_BASE_URL = 'http://10.0.2.2:3000/api';

// DEPOIS (substitua pelo seu IP):
const API_BASE_URL = 'http://192.168.1.100:3000/api';
```

**Passo 4:** Regenere o APK com `npx eas build --platform android`

### Para Emulador Android:
Já está pronto: `http://10.0.2.2:3000/api`

---

## 🧪 Teste o App

### 1. Inicie o painel web no PC:
```powershell
cd "c:\Users\PCGAME\Desktop\trading app\painel"
npm run dev
```

Você verá:
```
> painel@1.0.0 dev
> next dev

✓ Ready in 2.1s
✓ Local: http://localhost:3000
```

### 2. Abra o app no Samsung:
- Toque no ícone 🔍 "Buscador de Ofertas"

### 3. Busque algo:
- Digite: "smartphone" ou "iphone"
- Toque em 🔍
- Deve aparecer resultados

### 4. Alterne entre Ofertas e Demandas:
- Botões no topo

---

## 🐛 Se algo não funcionar...

### "Erro ao baixar APK"
- Redownload em https://expo.dev/dashboard
- Ou use Opção B (build local)

### "App não instala"
- Erro: "App não é instalado"?
  → Celular está em modo seguro?
  → Desative "Google Play Protect" em Configurações > Apps > Play Store

### "Erro ao conectar à API"
1. Painel web está rodando?
   ```powershell
   cd painel
   npm run dev
   ```

2. IP está certo?
   ```powershell
   # Teste no PC:
   curl http://192.168.1.100:3000/api/search?q=test
   ```

3. Firewall bloqueando?
   - Windows Defender > Firewall > Permitir app
   - Permitir "Node.js" nas redes privadas

### "APK muito grande (100MB+)"
Normal para apps Expo. Se quiser menu, use Opção C com proguard.

---

## 📊 Resumo das 3 Opções

| Opção | Tempo | Requ isitos | Facilidade |
|-------|-------|------------|-----------|
| A: Cloud | 15 min | Conexão internet | ⭐⭐⭐⭐⭐ |
| B: Local EAS | 20 min | 5GB disco | ⭐⭐⭐⭐ |
| C: Android Studio | 1 hora | Android SDK | ⭐⭐ |

**👉 Recomendação: Use Opção A**

---

## ✅ Checklist Final

Antes de "soltar" o app:

- [ ] APK gerado com sucesso
- [ ] Samsung Galaxy A33 conectado ao Wi-Fi
- [ ] Painel web rodando (`npm run dev`)
- [ ] IP do PC inserido em `App.js`
- [ ] APK instalado no celular
- [ ] App abre sem erros
- [ ] Busca retorna resultados
- [ ] Filtros funcionam (Ofertas/Demandas)

---

## 🎉 Parabéns!

Seu app está pronto para usar! 

**Próximos passos opcionais:**
1. Customize o ícone em `app.json`
2. Mude cores em `App.js` (linha ~270)
3. Adicione mais funcionalidades (ver histórico, favoritos, etc)
4. Publique na Google Play Store (opcional)

---

## 📞 Comandos Rápidos

```powershell
# Navegar para pasta do app
cd "c:\Users\PCGAME\Desktop\trading app\mobile-app"

# Ver versão do Expo
npx expo --version

# Login
npx expo login

# Build cloud (recomendado)
npx eas build --platform android

# Build local
npx eas build --platform android --local

# Preview no emulador
npx expo start --android

# Limpar cache
npx expo prebuild --clean
```

---

## 📚 Links Úteis

- Expo Docs: https://docs.expo.dev
- React Native Docs: https://reactnative.dev
- EAS Build: https://docs.expo.dev/eas-update/introduction/
- Android Studio: https://developer.android.com/studio (opcional)
- Samsung Galaxy A33 Specs: https://www.gsmarena.com/samsung_galaxy_a33_5g-11121.php

---

Qualquer dúvida, volte a este guia ou abra um item específico!

**Boa sorte! 🚀**
