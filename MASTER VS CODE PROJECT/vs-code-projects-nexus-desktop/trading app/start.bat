@echo off
REM Script para executar Bot + Painel simultaneamente no Windows

setlocal enabledelayedexpansion

echo.
echo 🚀 Iniciando Intermediário de Vendas...
echo.

REM Verificar se as pastas existem
if not exist "bot" (
    echo ❌ Erro: Pasta 'bot' não encontrada!
    pause
    exit /b 1
)

if not exist "painel" (
    echo ❌ Erro: Pasta 'painel' não encontrada!
    pause
    exit /b 1
)

REM Verificar se os arquivos .env existem
if not exist "bot\.env" (
    echo ❌ bot\.env não encontrado!
    echo Copie bot\.env.example:
    echo copy bot\.env.example bot\.env
    pause
    exit /b 1
)

if not exist "painel\.env.local" (
    echo ❌ painel\.env.local não encontrado!
    echo Copie painel\.env.local.example:
    echo copy painel\.env.local.example painel\.env.local
    pause
    exit /b 1
)

REM Criar pasta de logs
if not exist "logs" mkdir logs

echo 📦 Iniciando o Bot...
start "Bot WhatsApp" /D bot cmd /k "npm start"
echo ✅ Bot iniciado em nova janela
echo    Logs: logs/bot.log
echo.

timeout /t 3 /nobreak

echo 📦 Iniciando o Painel Web...
start "Painel Web" /D painel cmd /k "npm run dev"
echo ✅ Painel iniciado em nova janela
echo.

echo.
echo ==========================================
echo ✅ AMBOS SERVIÇOS INICIADOS!
echo ==========================================
echo.
echo 📋 Informações:
echo    Bot:   Veja a janela do terminal
echo    Painel: http://localhost:3000
echo.
echo 🛑 Para parar:
echo    Feche as janelas dos terminais
echo    Ou use Ctrl+C em cada uma
echo.
pause
