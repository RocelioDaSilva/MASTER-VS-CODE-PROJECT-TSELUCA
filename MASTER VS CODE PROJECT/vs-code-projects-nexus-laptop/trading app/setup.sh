#!/bin/bash

# Script de Setup Automático - Intermediário de Vendas

echo "🚀 Iniciando setup do Intermediário de Vendas..."
echo ""

# Instalar dependências do bot
echo "📦 Instalando dependências do bot..."
cd bot
npm install
cd ..

echo ""
echo "✅ Bot instalado com sucesso!"
echo ""

# Instalar dependências do painel
echo "📦 Instalando dependências do painel web..."
cd painel
npm install
cd ..

echo ""
echo "✅ Painel instalado com sucesso!"
echo ""

# Criar arquivos .env
echo "🔧 Criando arquivos de configuração..."

if [ ! -f bot/.env ]; then
    cp bot/.env.example bot/.env
    echo "✅ bot/.env criado (edite com suas credenciais)"
fi

if [ ! -f painel/.env.local ]; then
    cp painel/.env.local.example painel/.env.local
    echo "✅ painel/.env.local criado (edite com suas credenciais)"
fi

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETO!"
echo "=========================================="
echo ""
echo "📝 Próximos passos:"
echo ""
echo "1. Edite bot/.env com suas credenciais MongoDB:"
echo "   - MONGODB_URI"
echo "   - DB_NAME"
echo ""
echo "2. Edite painel/.env.local com as mesmas credenciais"
echo ""
echo "3. Execute o bot:"
echo "   cd bot && npm start"
echo ""
echo "4. Em outro terminal, execute o painel:"
echo "   cd painel && npm run dev"
echo ""
echo "5. Abra http://localhost:3000 no navegador"
echo ""
echo "📚 Leia o README.md para mais informações"
echo ""
