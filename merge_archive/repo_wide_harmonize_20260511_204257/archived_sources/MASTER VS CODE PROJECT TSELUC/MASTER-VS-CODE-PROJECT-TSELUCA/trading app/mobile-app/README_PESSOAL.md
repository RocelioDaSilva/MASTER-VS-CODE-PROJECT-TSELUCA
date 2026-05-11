# 📱 App Buscador - Pessoal

App React Native para buscar suas ofertas e demandas no **Samsung Galaxy A33** (e qualquer Android 5.0+).

---

## 🎯 TL;DR - 3 Linhas

1. **Leia:** `PARA_USO_PESSOAL.md`
2. **Escolha:** Online (Vercel) ou Local (Wi-Fi)
3. **Faça:** `npx eas build --platform android` → Instale no celular

**Tempo: 20 minutos.**

---

## ✨ Features

- ✅ Busca em tempo real
- ✅ Favoritos (toque o ❤️)
- ✅ Histórico de buscas
- ✅ Online (qualquer Wi-Fi) ou Local (Wi-Fi de casa)
- ✅ Funciona em múltiplos celulares seus
- ✅ Design moderno e responsivo

---

## 📱 O App

### Tela de Busca
```
┌─────────────────────────┐
│  🔍  Buscador Pessoal   │
│                         │
│  [Busque aqui...]    🔍 │
│  💰 Ofertas | 📦 Dema...│
│                         │
│  ┌─────────────────────┐│
│  │ iPhone 12           ││
│  │ 💰 2000€ | Tech | 10│
│  │         ❤️         ││
│  └─────────────────────┘│
└─────────────────────────┘
```

### Features:
- **Busca:** Digite e procure
- **Filtros:** Ofertas/Demandas
- **Favoritos:** Salve com ❤️
- **Histórico:** Últimas 5 buscas no home

---

## 🚀 Como Começar

### Setup Rápido (1 min)

```powershell
cd mobile-app
npm install --legacy-peer-deps
```

(Já está feito! App tem 1108 packages prontos)

---

### Criar APK (Escolha 1)

#### A) Online (Qualquer lugar do mundo)

```powershell
# Deploy painel
cd painel
npm run build
# Vercel → Deploy

# Configure app
# Edite App.js com URL painel

# Build
npx eas build --platform android

# Instale no celular
```

**Melhor para múltiplos celulares em qualquer lugar**

#### B) Local (Só em casa no Wi-Fi)

```powershell
# Descubra IP
ipconfig

# Configure
# Edite App.js com IP (ex: 192.168.1.100:3000)

# Build
npx eas build --platform android
```

**Mais rápido, sem delay de internet**

---

### Instalar no Celular (2 min)

1. **Samsung Galaxy A33:**
   - Settings → Security → Unknown Sources → ON

2. **Copiar APK:**
   - USB para Downloads
   - Ou Google Drive
   - Ou WhatsApp Web

3. **Instalar:**
   - Arquivos → Downloads → APK → Instalar

4. **Pronto!** ✓

---

## 📂 Estrutura

```
mobile-app/
├── App.js                    (350+ linhas, código app)
├── package.json             (dependências)
├── app.json                 (config Expo)
├── node_modules/            (1108 packages)
│
├── PARA_USO_PESSOAL.md      (👈 COMECE AQUI)
├── DEPLOY_VERCEL.md         (se quiser online)
├── INICIO_RAPIDO.md         (quick reference)
├── CONECTAR_IP_LOCAL.md     (se usar local)
└── ...
```

---

## 🔑 Comandos

```bash
# Instalar
npm install --legacy-peer-deps

# Testar rápido
npx expo start --android

# Gerar APK (online)
npx eas build --platform android

# Gerar APK (local)
npx eas build --platform android --local

# Login Expo
npx expo login
```

---

## 📊 Requisitos

| Item | Valor |
|------|-------|
| Android | 5.0+ |
| Node.js | 18+ |
| Espaço APK | 45-50MB |
| RAM mínima | 512MB |

---

## 🎯 Próximos Passos

1. **Leia:** `PARA_USO_PESSOAL.md` (5 min)
2. **Escolha:** Online ou Local
3. **Execute:** Passos da seção "Criar APK"
4. **Instale:** No seu Samsung Galaxy A33
5. **Use:** Busque ofertas/demandas!

---

## ❓ FAQ

### Posso usar em vários celulares?
**Sim!** Gere 1 APK e instale em todos os seus celulares.

### E em iOS?
**Depois!** Por enquanto é Android. iOS precisa de certificado Apple ($99/ano).

### Os dados sincronizam entre celulares?
**Favoritos não** (são locais em cada celular). **Busca sim** (todos buscam no mesmo painel).

### Preciso estar online?
**Depende:**
- Se usar **Vercel**: Sim, precisa internet
- Se usar **Local**: Não, só precisa de Wi-Fi de casa

### Posso publicar na Play Store depois?
**Sim!** Mas não é necessário - APK funciona direto.

---

## 🛠️ Troubleshooting

| Erro | Solução |
|------|---------|
| "Cannot find module" | `npm install --legacy-peer-deps` |
| "Sem conexão" | Painel rodando? IP correto? |
| "APK não instala" | Unknown Sources → ON |
| "Nenhum resultado" | Há dados no MongoDB? |

Ver detalhes em `PARA_USO_PESSOAL.md`

---

## 📞 Suporte

- **Quick questions:** `REFERENCIA_RAPIDA.md`
- **Setup:** `PARA_USO_PESSOAL.md`
- **Online:** `DEPLOY_VERCEL.md`
- **Local:** `CONECTAR_IP_LOCAL.md`
- **Detalhes:** `GUIA_APK_SAMSUNG.md`

---

## 📊 Stats

- **Versão:** 1.0.0
- **Linhas código:** 350+
- **Pacotes:** 1108
- **Tamanho:** 45-50MB
- **Build time:** 10-15 min
- **Instalar:** 1-2 min
- **Status:** ✅ Pronto para usar

---

## 🎁 Bônus

App inclui:
- ❤️ Favoritos pessoais
- 📜 Histórico de buscas
- 🚀 Funciona online e offline
- 🔄 Cache local
- 📱 Design responsivo

---

**Tudo pronto! Comece com `PARA_USO_PESSOAL.md`** 🚀

---

*Criado especialmente para seu uso pessoal - simples, rápido, direto.*
