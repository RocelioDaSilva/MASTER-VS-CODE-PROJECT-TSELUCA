# 🚀 INÍCIO RÁPIDO - Para Uso Pessoal

## ⚡ Versão SuperRápida

### Passo 1: Login Expo (1 min)
```powershell
npx expo login
# Email/Senha (criar em https://expo.dev)
```

### Passo 2: Gerar APK (15 min)
```powershell
npx eas build --platform android
```

### Passo 3: Instalar (2 min)
1. Espere o APK ficar pronto (Expo sent link)
2. Baixe: `buscador-ofertas-xxxxx.apk`
3. Samsung: **Settings > Security > Unknown Sources = ON**
4. Toque no APK → Instalar
5. **Pronto!** 🎉

---

## 🎯 QUAL CONFIGURAÇÃO VOCÊ PREFERE?

### Opção A: ONLINE (Recomendado)
- **Para:** Usar em qualquer lugar
- **Setup:** 5 min extra
- **Como:** Ver `DEPLOY_VERCEL.md`

```powershell
# Após fazer deploy no Vercel:
# Edite App.js linha 12 com sua URL
# Depois execute: npx eas build --platform android
```

### Opção B: LOCAL (Mais rápido)
- **Para:** Usar só em casa no Wi-Fi
- **Setup:** 2 min
- **Como:** Ver `CONECTAR_IP_LOCAL.md`

```powershell
# Descubra IP: ipconfig
# Edite App.js linha 13 com seu IP
# Depois execute: npx eas build --platform android
```

---

## 📖 Documentação

**Se é para USO PESSOAL, comece por:**

1. **PARA_USO_PESSOAL.md** ← Leia isto primeiro! (5 min)
2. **DEPLOY_VERCEL.md** ← Se quer online (10 min)
3. **CONECTAR_IP_LOCAL.md** ← Se quer local (5 min)

---

## ✨ Seu App Tem:

- ❤️ Favoritos (salve ofertas)
- 📜 Histórico (últimas 5 buscas)
- 🔍 Busca em tempo real
- 💾 Cache local
- 📱 Interface moderna

---

## 🎮 Como Usar Depois

1. Abra app
2. Digite (ex: "iPhone")
3. Escolha Ofertas/Demandas
4. Toque ❤️ para favoritar
5. Veja em aba Favoritos

---

Tudo pronto! **Leia `PARA_USO_PESSOAL.md` para os próximos passos.**

Tempo total: **20 minutos até usar no celular!** ⏱️
