# ⚡ 3 COMANDOS - PRONTO!

Se você é do tipo que quer só os comandos, aqui estão:

---

## 🔑 3 Linhas para Começar

```powershell
npx expo login

npx eas build --platform android

# Aguarde 15 min e baixe o APK do Expo Dashboard
# Copie para Samsung Galaxy A33 e instale
```

**Pronto! Você tem o APK! 🎉**

---

## Antes de Executar...

### Choose 1:

#### A) Quer usar ONLINE (em qualquer lugar)?

1. Deploy painel: Veja `DEPLOY_VERCEL.md` (10 min)
2. Após URL: Edite `App.js` linha 12 com a URL
3. Execute os 3 comandos acima

#### B) Quer usar LOCAL (só em casa)?

1. Descubra IP: `ipconfig` → Nota o IPv4
2. Edite `App.js` linha 13 com seu IP (ex: `192.168.1.100`)
3. Execute os 3 comandos acima

#### C) Quer testar SEM APK?

```powershell
npx expo start --android
# Escaneie QR code com Expo Go (app grátis)
```

---

## Depois de Instalar

1. Samsung: **Settings > Security > Unknown Sources > ON**
2. Copie APK para Downloads via USB
3. Toque → Instalar
4. Pronto! 🎉

---

## Features do App

- 🔍 Busca em tempo real
- ❤️ Favoritos (toque coração)
- 📜 Histórico (últimas 5)
- 💾 Cache local
- 📱 Design bonito

---

## Troubleshooting Rápido

```
"Sem conexão" 
→ Painel rodando? IP correto? Internet?

"Nenhum resultado"
→ Há dados no MongoDB?

"APK não instala"
→ Unknown Sources ativado?

"Exposição não login"
→ npx expo login (criar conta em expo.dev)
```

---

## Todos os Docs

```
PARA_USO_PESSOAL.md        ← Versão completa desta
DEPLOY_VERCEL.md           ← Como colocar online
CONECTAR_IP_LOCAL.md       ← Como usar com IP
README_PESSOAL.md          ← Overview
REFERENCIA_RAPIDA.md       ← Cheat sheet
QUAL_DOCUMENTO_LER.md      ← Guia de leitura
```

---

**Precisa de mais detalhes? Abra `PARA_USO_PESSOAL.md`**

**Só quer comandos? 👆 Você está aqui!**

---

`npx eas build --platform android` → 15 min → APK pronto! 🚀
