# Script para gerar APK do app mobile
# Este script automat iza todo o processo de build do Expo

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "║               📱 Gerador de APK - Buscador Mobile              ║" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verifica se está no diretório certo
if (-Not (Test-Path "package.json")) {
    Write-Host "❌ ERRO: package.json não encontrado" -ForegroundColor Red
    Write-Host "Execute dentro de: mobile-app" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "1️⃣  Verificando dependências..." -ForegroundColor Yellow
Write-Host ""

# Verifica Node.js
$nodeVersion = & node --version 2>$null
if (-Not $nodeVersion) {
    Write-Host "❌ Node.js não instalado" -ForegroundColor Red
    Write-Host "Baixe em: https://nodejs.org" -ForegroundColor Yellow
    Read-Host "Pressione Enter"
    exit 1
}

Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
Write-Host "✅ npm pronto" -ForegroundColor Green
Write-Host ""

Write-Host "2️⃣  Verificando módulos npm..." -ForegroundColor Yellow
if (-Not (Test-Path "node_modules")) {
    Write-Host "📦 node_modules não encontrado. Instalando..." -ForegroundColor Yellow
    & npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erro ao instalar" -ForegroundColor Red
        Read-Host "Pressione Enter"
        exit 1
    }
}

Write-Host "✅ Dependências prontas" -ForegroundColor Green
Write-Host ""

Write-Host "3️⃣  Checando Expo..." -ForegroundColor Yellow

# Tenta usar expo local ou global
& npx expo --version >$null 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Expo CLI disponível" -ForegroundColor Green
} else {
    Write-Host "⚠️  Instalando Expo CLI..." -ForegroundColor Yellow
    & npm install -g expo-cli
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                                ║" -ForegroundColor Green
Write-Host "║                   🚀 OPÇÕES DE BUILD                           ║" -ForegroundColor Green
Write-Host "║                                                                ║" -ForegroundColor Green
Write-Host "║  1. Build Local (Rápido, requer 5GB)                          ║" -ForegroundColor Green
Write-Host "║     npx eas build --platform android --local                  ║" -ForegroundColor Green
Write-Host "║                                                                ║" -ForegroundColor Green
Write-Host "║  2. Build Cloud (Sem instalar Android Studio)                 ║" -ForegroundColor Green
Write-Host "║     npx eas build --platform android                          ║" -ForegroundColor Green
Write-Host "║                                                                ║" -ForegroundColor Green
Write-Host "║  3. Preview (Teste rápido sem gerar APK)                      ║" -ForegroundColor Green
Write-Host "║     npx expo start                                             ║" -ForegroundColor Green
Write-Host "║                                                                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "Qual opção você deseja? (1/2/3): " -NoNewline -ForegroundColor Yellow
$choice = Read-Host

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🔨 Iniciando build local..." -ForegroundColor Cyan
        Write-Host "Isso pode levar 10-20 minutos..." -ForegroundColor Yellow
        Write-Host ""
        & npx eas build --platform android --local
    }
    "2" {
        Write-Host ""
        Write-Host "☁️  Iniciando build na nuvem..." -ForegroundColor Cyan
        Write-Host "Você será redirecionado para login Expo (grátis)" -ForegroundColor Yellow
        Write-Host ""
        & npx eas build --platform android
    }
    "3" {
        Write-Host ""
        Write-Host "▶️  Iniciando preview..." -ForegroundColor Cyan
        Write-Host "Escaneie o QR code com Expo Go no seu celular" -ForegroundColor Yellow
        Write-Host ""
        & npx expo start --android
    }
    default {
        Write-Host "❌ Opção inválida" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Processo concluído!" -ForegroundColor Green
Write-Host "📱 Procure pelo APK em: dist/buscador-ofertas-*.apk" -ForegroundColor Cyan
Read-Host "Pressione Enter"
