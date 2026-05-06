@echo off
setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║       📱 Instalador - App Mobile (Buscador de Ofertas)      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verifica se estamos no diretório certo
if not exist "package.json" (
    echo ❌ ERRO: Execute este script dentro da pasta mobile-app
    echo Comando correto:
    echo   cd mobile-app
    echo   setup.bat
    pause
    exit /b 1
)

echo 🔍 Verificando Node.js e npm...
where node >nul 2>nul
if errorlevel 1 (
    echo ❌ Node.js não encontrado. Instale em: https://nodejs.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i

echo ✅ Node.js %NODE_VERSION%
echo ✅ npm %NPM_VERSION%

echo.
echo 📦 Instalando dependências...
echo (Isso pode levar 3-5 minutos)
echo.

call npm install

if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

echo.
echo ✅ Instalação concluída com sucesso!
echo.
echo 🚀 Próximos passos:
echo.
echo   1. Criar conta Expo (grátis): https://expo.dev/signup
echo.
echo   2. Fazer login:
echo      npx expo login
echo.
echo   3. Gerar APK:
echo      npx eas build --platform android
echo.
echo   4. Leia o README_APK.md para instruções detalhadas
echo.
pause
