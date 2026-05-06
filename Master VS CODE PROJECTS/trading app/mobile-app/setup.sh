#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║       📱 Instalador - App Mobile (Buscador de Ofertas)      ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verifica se estamos no diretório certo
if [ ! -f "package.json" ]; then
    echo "❌ ERRO: Execute este script dentro da pasta mobile-app"
    echo "Comando correto:"
    echo "  cd mobile-app"
    echo "  bash setup.sh"
    exit 1
fi

echo "🔍 Verificando Node.js e npm..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale em: https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node --version)
NPM_VERSION=$(npm --version)

echo "✅ Node.js $NODE_VERSION"
echo "✅ npm $NPM_VERSION"

echo ""
echo "📦 Instalando dependências..."
echo "(Isso pode levar 3-5 minutos)"
echo ""

npm install

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo ""
echo "✅ Instalação concluída com sucesso!"
echo ""
echo "🚀 Próximos passos:"
echo ""
echo "   1. Criar conta Expo (grátis): https://expo.dev/signup"
echo ""
echo "   2. Fazer login:"
echo "      npx expo login"
echo ""
echo "   3. Gerar APK:"
echo "      npx eas build --platform android"
echo ""
echo "   4. Leia o README_APK.md para instruções detalhadas"
echo ""
