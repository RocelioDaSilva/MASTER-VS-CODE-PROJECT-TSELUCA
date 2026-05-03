@echo off
REM Script de Setup Automático - Intermediário de Vendas (Windows)

echo.
echo 🚀 Iniciando setup do Intermediário de Vendas...
echo.

REM Instalar dependências do bot
echo 📦 Instalando dependências do bot...
cd bot
call npm install
cd ..

echo.
echo ✅ Bot instalado com sucesso!
echo.

REM Instalar dependências do painel
echo 📦 Instalando dependências do painel web...
cd painel
call npm install
cd ..

echo.
echo ✅ Painel instalado com sucesso!
echo.

REM Criar arquivos .env
echo 🔧 Criando arquivos de configuração...

if not exist "bot\.env" (
    copy bot\.env.example bot\.env
    echo ✅ bot\.env criado (edite com suas credenciais^)
)

if not exist "painel\.env.local" (
    copy painel\.env.local.example painel\.env.local
    echo ✅ painel\.env.local criado (edite com suas credenciais^)
)

echo.
echo ==========================================
echo ✅ SETUP COMPLETO!
echo ==========================================
echo.
echo 📝 Próximos passos:
echo.
echo 1. Edite bot\.env com suas credenciais MongoDB:
echo    - MONGODB_URI
echo    - DB_NAME
echo.
echo 2. Edite painel\.env.local com as mesmas credenciais
echo.
echo 3. Execute o bot:
echo    cd bot ^&^& npm start
echo.
echo 4. Em outro terminal, execute o painel:
echo    cd painel ^&^& npm run dev
echo.
echo 5. Abra http://localhost:3000 no navegador
echo.
echo 📚 Leia o README.md para mais informações
echo.
pause
