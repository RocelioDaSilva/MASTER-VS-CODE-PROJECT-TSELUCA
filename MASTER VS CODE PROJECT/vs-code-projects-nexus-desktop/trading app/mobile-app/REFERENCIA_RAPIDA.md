# 📚 REFERÊNCIA RÁPIDA - Comandos & Links

## 🔗 Links Importantes

| Item | URL |
|------|-----|
| Expo Dashboard | https://expo.dev/dashboard |
| Expo Docs | https://docs.expo.dev |
| React Native | https://reactnative.dev |
| Samsung A33 Specs | https://www.gsmarena.com/samsung_galaxy_a33_5g-11121.php |

---

## ⌨️ Comandos Essenciais

### Setup
```bash
cd mobile-app
npm install --legacy-peer-deps
npx expo login
```

### Build APK
```bash
# Cloud (recomendado)
npx eas build --platform android

# Local
npx eas build --platform android --local

# Preview
npx expo start --android
```

### Desenvolvimento
```bash
# Teste em tempo real
npx expo start

# Ver logs
npx expo start --android > logs.txt
```

### Limpeza
```bash
npx expo prebuild --clean
rm -rf node_modules/.expo
```

---

## 📱 Instalação no Celular

### 1. Preparar Samsung
```
Settings > Security > Unknown Sources > ON
```

### 2. Transferir APK
- Via USB para pasta Downloads
- Ou via Google Drive
- Ou via WhatsApp

### 3. Instalar
```
Arquivos > Downloads > buscador-ofertas-xxxxx.apk > Instalar
```

---

## 🔧 Configuração

### IP Local
```powershell
# Descobrir IP
ipconfig

# Editar App.js linha 17
const API_BASE_URL = 'http://192.168.1.100:3000/api';
```

### Firewall
```
Windows: Defender > Firewall > Permitir Node.js na rede privada
```

### Painel Web
```bash
cd painel
npm run dev
# http://localhost:3000
```

---

## 🐛 Troubleshooting Rápido

### APK não gera
- Crie conta Expo: https://expo.dev/signup
- Faça login: `npx expo login`
- Tente novamente: `npx eas build --platform android`

### APK não instala
- Ative "Unknown Sources" nas Settings do celular
- Tente desabilitar Google Play Protect

### App não conecta
- Painel web rodando? `npm run dev` no painel/
- IP correto em App.js?
- Firewall permite Node.js?
- PC e celular mesmo Wi-Fi?

### Sem resultados
- Há dados no MongoDB?
- API testada? `curl http://IP:3000/api/search?q=teste`
- Tipos corretos? Ofertas vs Demandas

---

## 📖 Documentos

| Arquivo | Propósito | Tempo |
|---------|-----------|-------|
| INICIO_RAPIDO.md | Quick start | 5 min |
| GUIA_APK_SAMSUNG.md | Guia completo | 15 min |
| CONECTAR_IP_LOCAL.md | Conexão por IP | 10 min |
| README_APK.md | Referência técnica | 20 min |

---

## 🎯 Resumo Rápido

```
1. Criar conta Expo (2 min)
   ↓
2. npx expo login (1 min)
   ↓
3. npx eas build --platform android (15 min)
   ↓
4. Baixar APK da dashboard (1 min)
   ↓
5. Instalar no Samsung (2 min)
   ↓
6. Pronto! 🎉
```

---

## 💡 Dicas

- Use build cloud (Opção 2) para evitar instalar Android SDK (5GB)
- Celular físico é melhor que emulador para testar
- Sempre configure o IP correto antes de gerar APK final
- Salve o APK em local seguro após gerar

---

## 📞 Suporte

Para problemas avançados:
1. Leia GUIA_APK_SAMSUNG.md (seção Troubleshooting)
2. Verifique CONECTAR_IP_LOCAL.md
3. Consulte logs: `npx expo start --android`
4. Docs Expo: https://docs.expo.dev/troubleshooting/

---

**Última atualização:** Abril 2026
**Versão App:** 1.0.0
**Compatibilidade:** Android 5.0+
