#!/bin/bash

# Corhed Landing Page - Setup Script
# Este script configura automaticamente o projeto para desenvolvimento

echo "🚀 Configurando Corhed Landing Page..."
echo "====================================="

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale o Node.js (versão 14 ou superior)"
    echo "   Download: https://nodejs.org/"
    exit 1
fi

# Verificar versão do Node.js
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 14 ]; then
    echo "❌ Node.js versão $NODE_VERSION detectada. É necessário Node.js 14 ou superior."
    exit 1
fi

echo "✅ Node.js versão $(node -v) detectada"

# Instalar dependências
echo "📦 Instalando dependências..."
if command -v yarn &> /dev/null; then
    yarn install
else
    npm install
fi

# Verificar se o logo existe
if [ ! -f "corhed-logo.png" ]; then
    echo "⚠️  Logo não encontrado: corhed-logo.png"
    echo "   Por favor, adicione o logo da Corhed na raiz do projeto"
fi

echo ""
echo "🎉 Instalação concluída!"
echo ""
echo "📋 Comandos disponíveis:"
echo "   npm run dev     - Servidor de desenvolvimento (porta 3000)"
echo "   npm run preview - Preview de produção (porta 8000)"
echo "   npm start       - Servidor básico (porta 3000)"
echo ""
echo "🌐 Para visualizar o site:"
echo "   npm run preview"
echo ""
echo "📖 Leia o README.md para mais informações"