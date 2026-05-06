# 🌐 Deploy da Painel na Vercel (Online)

Se quer usar o app **em qualquer lugar**, coloque o painel online primeiro.

---

## Passo 1: Prepare o Painel

```powershell
cd painel
npm run build
```

Você deve ver:
```
✓ Compiled successfully
✓ 3 pages
✓ Build time: 2.1s
```

---

## Passo 2: Crie Conta na Vercel

1. Acesse: https://vercel.com
2. Clique "Sign Up" (inscrever com GitHub é mais fácil)
3. Confirme email

---

## Passo 3: Faça Deploy

### Opção A: Via GitHub (Mais Fácil)

1. **Crie repositório GitHub**
   - https://github.com/new
   - Nome: `intermediario-painel`
   - Público ou Privado (sem importância)

2. **Uma vez criado:**
   ```powershell
   cd painel
   git init
   git add .
   git commit -m "Painel online"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/intermediario-painel.git
   git push -u origin main
   ```

3. **Na Vercel:** 
   - Clique "New Project"
   - Selecione o repositório `intermediario-painel`
   - Clique "Deploy"
   - Aguarde ~1 min

**Resultado:** URL como `https://intermediario-painel-xxxxx.vercel.app`

---

### Opção B: Direto (Sem GitHub)

1. **Na Vercel:**
   - Clique "New Project"
   - "Create from Existing Repository"
   - Conecte sua conta GitHub
   - Selecione seu repositório

---

## Passo 4: Configurar Variáveis (Se Needed)

Na Vercel:
- Project Settings
- Environment Variables
- Adicione se tiver (ex: MONGODB_URI)

**Nota:** Se MongoDB está em Atlas, as APIs funcionam lá também!

---

## Passo 5: Copie a URL

Após deploy:
```
🎉 Deployment Successful!
Production: https://seu-painel-xxxxx.vercel.app
```

**Copie essa URL!**

---

## Passo 6: Configure a App

Edite `mobile-app\App.js` linha 12:

```javascript
const API_URLS = [
  'https://seu-painel-xxxxx.vercel.app/api',  // ← MUDE AQUI
  'http://localhost:3000/api',
  ...
];
```

---

## Passo 7: Regenere o APK

```powershell
cd mobile-app
npx eas build --platform android
```

Desta vez vai usar a URL online!

---

## ✅ Testado?

1. **Painel online rodando?**
   - Acesse: `https://seu-painel-xxxxx.vercel.app`
   - Deve carregar a interface

2. **API funcionando?**
   - Tente: `https://seu-painel-xxxxx.vercel.app/api/search?q=teste`
   - Deve retornar JSON

3. **App funciona agora?**
   - Abra app no celular
   - Busque por algo
   - Deve trazer resultados

---

## 🐛 Se algo não funcionar

### "Erro ao acessar painel online"
- URL está correta em `.env`?
- MongoDB está **online** também (Atlas)?
- Aguarde 2-3 min (Vercel bootstrap)

### "Status 500 na API"
- Erro no MongoDB?
- Verifie `.env.local` do painel
- Vercel consegue conectar ao MongoDB?

### "Painel funciona mas app não busca"
- URL em App.js está correta?
- Celular está online?
- Tente primeira com app em localhost para testar

---

## 📊 Resumo

| Passo | O Que Fazer | Tempo |
|-------|-----------|-------|
| 1 | `npm run build` na painel | 2 min |
| 2 | Criar conta Vercel | 2 min |
| 3 | Fazer deploy | 5 min |
| 4 | Copiar URL | 1 min |
| 5 | Editar App.js | 1 min |
| 6 | Gerar APK | 15 min |
| 7 | Instalar no celular | 2 min |

**Total: ~28 min**

---

## 🎊 Pronto!

Agora seu app funciona em **qualquer Wi-Fi do mundo**!

```
Computador (qualquer lugar)
    ↓
    Vercel (online)
    ↓
    API (MongoDB Atlas)
    ↓
Celular (qualquer lugar)
```

---

## 💡 Dica: Atualizar o Painel

Se mudar o código do painel:

```powershell
cd painel
git add .
git commit -m "Nova feature"
git push

# Vercel faz deploy automaticamente em 1-2 min!
```

---

Se usar **vários celulares seus**, basta instalar o mesmo APK em todos!
