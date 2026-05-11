# 📱 App Mobile - Buscador de Ofertas

App React Native com Expo para buscar ofertas e demandas no seu Samsung Galaxy A33.

## 📦 O que você recebe

- ✅ App mobile nativo para Android
- ✅ Interface moderna e responsiva
- ✅ Conexão com suas APIs (painel web)
- ✅ Busca de ofertas e demandas
- ✅ Offline-ready architecture

## 🚀 Como Gerar o APK

### Opção 1: Build Rápido (Recomendado) - 5 minutos

1. **Instale dependências:**
```bash
cd mobile-app
npm install
```

2. **Faça login no Expo (conta grátis):**
```bash
npx expo login
# ou criar em https://expo.dev
```

3. **Gere o APK:**
```bash
npx eas build --platform android --local
```

O APK será criado em: `dist/buscador-ofertas-xxxxxxxxxxx.apk`

### Opção 2: Build via Expo Cloud (Mais Rápido)

Sem precisar instalar Android SDK:

```bash
npx eas build --platform android
```

- Vá para https://expo.dev/dashboard
- Entre na seção "Builds"
- Baixe o APK quando terminar (5-10 min)

### Opção 3: Build Local com Android Studio

Requer 5GB de espaço livre e mais tempo:

```bash
npx expo prebuild --clean && npm run build-local
```

## 📱 Como Instalar no Samsung Galaxy A33

### Passo 1: Prepare o Celular

1. **Ative "Origens Desconhecidas":**
   - Configurações > Segurança > Fontes Desconhecidas
   - Ative "Permitir instalação de apps de fontes desconhecidas"

2. **Transfira o APK:**
   - Via USB, AirDrop, Google Drive, ou Email
   - Coloque na pasta Downloads

### Passo 2: Instale o APK

1. **Abra o arquivo gerenciador:**
   - Toque em Downloads
   - Procure por `buscador-ofertas-*.apk`

2. **Toque para instalar:**
   - Quando pedir permissões, toque "Instalar"
   - Aguarde 30-60 segundos

3. **Pronto!**
   - O app aparecerá na sua tela inicial
   - Ícone: 🔍 Buscador de Ofertas

## ⚙️ Configuração Inicial do App

### Para Emulador Android:
Já está configurado para `http://10.0.2.2:3000/api`

### Para Celular Físico (Recomendado):

1. **Descubra o IP do seu computador:**
   ```powershell
   ipconfig
   ```
   Procure por "IPv4 Address" na sua rede Wi-Fi (ex: 192.168.1.100)

2. **Edite `App.js`:**
   ```javascript
   const API_BASE_URL = 'http://192.168.1.100:3000/api'; // Substitua pelo seu IP
   ```

3. **Certifique-se que:**
   - Computador e celular estão NO MESMO Wi-Fi
   - O painel web está rodando (`npm run dev`)
   - Firewall permite conexões internas

## 🔄 Teste o App

1. **Inicie o painel web:**
   ```bash
   cd painel
   npm run dev
   ```

2. **Abra o app no celular**

3. **Busque por algo:**
   - Exemplo: "smartphone", "iphone", "samsung", "tablet"
   - Alterna entre "Ofertas" e "Demandas"

## 🐛 Troubleshooting

### "Erro: Não consegui conectar ao servidor"
- Painel web não está rodando em http://localhost:3000?
- IP configurado incorretamente no `App.js`?
- Celular não está no mesmo Wi-Fi?

### App fecha ao buscar
- Verifique console: `npm run dev` no painel web
- Erros CORS? Adicione essa linha em `painel/pages/api/search.js`:
```javascript
res.setHeader('Access-Control-Allow-Origin', '*');
```

### APK não instala
- Verifique espaço em disco (mínimo 50MB)
- Android 5.0+ é necessário
- Tente via USB: `adb install buscador-ofertas-*.apk`

## 📊 Versões do App

| Versão | Tamanho | Compatibilidade |
|--------|---------|-----------------|
| Android APK | ~45MB | Android 5.0+ |
| React Native | Cross-platform | iOS/Android |

## 🔐 Segurança

- Nenhum dado pessoal é coletado
- Conexão direta com suas APIs
- Código open-source (se quiser revisar)

## 📞 Próximos Passos

1. ✅ Baixar APK
2. ✅ Instalar no celular
3. ✅ Configurar IP da API
4. ✅ Testar buscas
5. ✅ (Opcional) Publicar na Google Play Store

## 💡 Desenvolvimento Futuro

Pode adicionar:
- Notificações Push quando há novas ofertas
- Modo offline com dados em cache
- Filtros avançados
- Dark mode
- Chat integrado com vendedores

---

**Pronto para começar? Execute agora:**

```bash
cd mobile-app
npm install
npx eas build --platform android
```

Qualquer dúvida, veja `App.js` ou `README.md` principal.
