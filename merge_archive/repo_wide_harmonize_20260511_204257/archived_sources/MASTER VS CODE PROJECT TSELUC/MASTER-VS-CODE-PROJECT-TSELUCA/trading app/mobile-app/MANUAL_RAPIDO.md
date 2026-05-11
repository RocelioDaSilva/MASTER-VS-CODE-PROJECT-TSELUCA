# 📋 Manual Rápido - Tudo Essencial

Leia isto uma vez. Depois, ignore o resto.

---

## 🎯 OPÇÃO 1: Exponential Go (Recomendado - SEM LOGIN)

**Ideal para:** Testar rápido, desenvolver, múltiplos celulares

### Passo 1: PC
```powershell
cd mobile-app
npx expo start --android
```

Vai aparecer um QR code enorme.

### Passo 2: Samsung
1. Play Store → Busca "Expo Go" → Instala (grátis)
2. Abre Expo Go
3. Aperta no botão de câmera (no app)
4. Escaneia o QR code do PC
5. App abre em 3 segundos

### Cada Vez Que Quiser Abrir
```powershell
cd mobile-app
npx expo start --android
# Escaneia de novo
```

**Tempo:** 5 minutos inicio + 10 segundos depois

---

## 📦 OPÇÃO 2: APK (Opcional - Sem Expo Go)

**Ideal para:** Compartilhar com outros, instalar permanente

### Passo 1: Precisa de conta Expo (grátis em expo.dev)

### Passo 2: Build
```powershell
npx expo login
npx eas build --platform android
```

Aguarda 15 minutos.

### Passo 3: Instala
- Baixa o APK: `https://expo.dev/dashboard`
- Copia para Samsung via USB
- Settings > Security > Unknown Sources > ON
- Toca no APK

**Tempo:** 20 minutos

---

## 🌐 OPÇÃO 3: Online (Acessar de Qualquer Lugar)

**Ideal para:** Usar no trabalho, na rua, em outra casa

### Passo 1: Deploy painel
Ver `DEPLOY_VERCEL.md` (10 minutos extra)

### Passo 2: Usa qualque uma das duas opções acima

**Tempo:** +10 minutos

---

## ❓ QUAL ESCOLHO?

| Situação | Use |
|----------|-----|
| Quero testar AGORA | Opção 1 |
| Quero instalar "de verdade" | Opção 2 |
| Quer fazer login | Nenhuma! Expo Go não precisa |
| Mesma rede Wi-Fi? | Opção 1 |
| Qualquer lugar? | Opção 2 + Opção 3 |

**→ Comece com OPÇÃO 1 (Expo Go), é o mais simples!**

---

## 🔑 Comandos Rápidos

```bash
# Expo Go (agora)
cd mobile-app
npx expo start --android

# APK (depois)
npx eas build --platform android

# Testar sem Android
npx expo start --web
```

---

## ⚡ O App Faz

- 🔍 Busca em tempo real
- ❤️ Favoritos
- 📜 Histórico
- 📱 Interface bonita

---

## 🆘 Problemas?

### "Não apareceu QR code"
```
Pressiona 'a' no terminal
Ou tenta: npx expo start --dev-client
```

### "Não consigo escanear"
```
Câmera Samsung aberta?
Expo Go precisa de permissão de câmera
Settings > Apps > Expo Go > Permissions > Câmera ON
```

### "Sem resultados"
```
Há dados no MongoDB?
Painel está online?
Tenta outra palavra
```

### "APK não instala"
```
Unknown Sources está ON?
Espaço em disco?
Android 5.0+?
```

---

## 📂 Documentação

Só precisa ler ISTO. Ignora os outros se não precisar.

- `COMECE_AGORA.md` - 5 minutos exatos
- `TUDO_SIMPLES.md` - Resumo com 3 opções
- `DEPLOY_VERCEL.md` - Se quer online (opcional)

Pronto!

---

## 🚀 INÍCIO

Execute AGORA:

```powershell
cd 'c:\Users\PCGAME\Desktop\trading app\mobile-app'
npx expo start --android
```

Vais ver um QR code. Escaneia com Expo Go. Pronto! 🎉

---

*Feito.*
