@echo off
REM Corhed Landing Page - Setup Script para Windows
REM Este script configura automaticamente o projeto para desenvolvimento

echo 🚀 Configurando Corhed Landing Page...
echo =====================================

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado. Por favor, instale o Node.js (versão 14 ou superior)
    echo    Download: https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar versão do Node.js
for /f "tokens=1 delims=v." %%i in ('node --version') do set NODE_MAJOR=%%i
if %NODE_MAJOR% lss 14 (
    echo ❌ Node.js versão detectada: %NODE_MAJOR%. É necessário Node.js 14 ou superior.
    pause
    exit /b 1
)

echo ✅ Node.js detectado

REM Instalar dependências
echo 📦 Instalando dependências...
if exist yarn.lock (
    yarn install
) else (
    npm install
)

REM Verificar se o logo existe
if not exist "corhed-logo.png" (
    echo ⚠️  Logo não encontrado: corhed-logo.png
    echo    Por favor, adicione o logo da Corhed na raiz do projeto
)

echo.
echo 🎉 Instalação concluída!
echo.
echo 📋 Comandos disponíveis:
echo    npm run dev     - Servidor de desenvolvimento (porta 3000)
echo    npm run preview - Preview de produção (porta 8000)
echo    npm start       - Servidor básico (porta 3000)
echo.
echo 🌐 Para visualizar o site:
echo    Execute: npm run preview
echo.
echo 📖 Leia o README.md para mais informações

pause