# 🔌 Conectar App Móvel ao Painel (IP Local)

## ⚠️ IMPORTANTE

Você **DEVE** fazer esta configuração se quer que o app funcione no seu Samsung Galaxy A33!

---

## Passo 1: Descobrir o IP do seu PC

### Windows (PowerShell):
```powershell
ipconfig
```

Procure pela seção da sua rede Wi-Fi (provavelmente "Wireless LAN adapter" ou "Ethernet"):

```
Adaptador Ethernet Ethernet:
   ...
   IPv4 Address . . . . . . . . . . . : 192.168.1.100     ← COPIE ESTE NÚMERO
   ```

**Resultado esperado:** algo como `192.168.1.XXX` ou `10.0.0.XXX`

### Confirme o IP:
```powershell
# Teste se consegue acessar
curl http://192.168.1.100:3000

# Deve retornar HTML do painel
```

---

## Passo 2: Editar o `App.js`

### Arquivo:
```
c:\Users\PCGAME\Desktop\trading app\mobile-app\App.js
```

### Localize (linha ~17):
```javascript
const API_BASE_URL = 'http://10.0.2.2:3000/api'; // Localhost no Android Emulator
// Para celular físico, mude para: http://SEU_IP_LOCAL:3000/api
```

### Mude para:
```javascript
const API_BASE_URL = 'http://192.168.1.100:3000/api'; // Substitua 192.168.1.100 pelo seu IP
```

### Salve o arquivo (Ctrl+S)

---

## Passo 3: Regenerar o APK

Depois de mudar o IP, você **PRECISA** regenerar o APK:

### Opção A (Recomendada):
```powershell
cd mobile-app
npx eas build --platform android
```

### Opção B (Local):
```powershell
cd mobile-app
npx eas build --platform android --local
```

---

## Passo 4: Certificar-se da Conectividade

### No PC:
```powershell
# Terminal 1 - Subir o painel
cd painel
npm run dev

# Terminal 2 - Testar acesso à API
curl http://192.168.1.100:3000/api/search?q=teste
```

### Resultado esperado:
```json
[
  {
    "text": "iPhone 12, não usado...",
    "group": "Tech Group",
    "timestamp": "2026-04-02T10:30:00Z"
  }
]
```

### No Celular:
1. Certifique-se **que está no MESMO Wi-Fi** do PC
2. Abra o app
3. Busque por algo
4. Deve mostrar resultados

---

## 🐛 Debugging

### Se não conectar...

#### Verificar Firewall:
```powershell
# Windows Defender
# Settings > Firewall & Network > Allow an app through firewall
# Encontre Node.js e permita em "Private networks"
```

#### Verificar Painel:
```powershell
cd painel
npm run dev

# Deve mostrar:
# ✓ Ready in 2.1s
# ✓ Local: http://localhost:3000
```

#### Testar API diretamente:
```powershell
# Substitua 192.168.1.100 pelo seu IP real
curl http://192.168.1.100:3000/api/search?q=iphone

# Ou abra no navegador:
# http://192.168.1.100:3000/api/search?q=iphone
```

#### Verificar Conectividade:
```powershell
# Ping do PC pelo celular (no mesmo Wi-Fi)
# Abra Chrome no celular e digite:
# http://192.168.1.100:3000
# Deve carregar o painel
```

### Logs do App:
Se instalar com `npm run dev`:
```powershell
cd mobile-app
npx expo start --android
```

Você verá os logs em tempo real:
```
[2026-04-02T10:35:20Z] Fetching from: http://192.168.1.100:3000/api/search?q=iphone
[2026-04-02T10:35:21Z] Response: 200 OK
[2026-04-02T10:35:21Z] Results: 5 items
```

---

## 📡 Resumo das URLs

| Cenário | URL |
|---------|-----|
| Painel web (PC) | `http://localhost:3000` |
| API (PC) | `http://localhost:3000/api/search` |
| App (Emulador) | `http://10.0.2.2:3000/api` |
| App (Celular físico) | `http://192.168.1.100:3000/api` |

---

## ✅ Checklist

Antes de usar o app:

- [ ] IP do PC descoberto (`ipconfig`)
- [ ] App.js editado com IP correto
- [ ] APK regenerado (`eas build`)
- [ ] Painel web rodando (`npm run dev`)
- [ ] PC e celular mesmo Wi-Fi
- [ ] Firewall permite Node.js
- [ ] API testada (`curl http://IP:3000/api/search?q=teste`)
- [ ] App instalado no celular
- [ ] Busca funciona no app

---

## 🎓 Conceito

```
PC (192.168.1.100)
├── Painel Web (http://localhost:3000)
└── API (http://localhost:3000/api)
    ↑
    └─ Celular (mesmo Wi-Fi)
       └── App Mobile
           └── Conecta em: http://192.168.1.100:3000/api
```

---

Qualquer dúvida, volte a este arquivo ou abra `GUIA_APK_SAMSUNG.md`!
