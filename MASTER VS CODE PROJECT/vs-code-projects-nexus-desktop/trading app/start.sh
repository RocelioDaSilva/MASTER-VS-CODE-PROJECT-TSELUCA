#!/bin/bash

# Script para executar Bot + Painel simultaneamente no Linux/Mac

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Iniciando Intermediário de Vendas...${NC}"
echo ""

# Verificar se as pastas existem
if [ ! -d "bot" ] || [ ! -d "painel" ]; then
    echo -e "${RED}❌ Erro: Pastas 'bot' ou 'painel' não encontradas!${NC}"
    echo "Certifique-se de estar no diretório raiz do projeto"
    exit 1
fi

# Verificar se os arquivos .env existem
if [ ! -f "bot/.env" ]; then
    echo -e "${RED}❌ bot/.env não encontrado! Copie bot/.env.example:${NC}"
    echo "cp bot/.env.example bot/.env"
    exit 1
fi

if [ ! -f "painel/.env.local" ]; then
    echo -e "${RED}❌ painel/.env.local não encontrado! Copie painel/.env.local.example:${NC}"
    echo "cp painel/.env.local.example painel/.env.local"
    exit 1
fi

# Criar pasta de logs
mkdir -p logs

echo -e "${YELLOW}📦 Iniciando o Bot...${NC}"
cd bot
npm start > ../logs/bot.log 2>&1 &
BOT_PID=$!
echo -e "${GREEN}✅ Bot iniciado (PID: $BOT_PID)${NC}"
echo "   Logs: logs/bot.log"
cd ..

echo ""
sleep 3

echo -e "${YELLOW}📦 Iniciando o Painel Web...${NC}"
cd painel
npm run dev > ../logs/painel.log 2>&1 &
PAINEL_PID=$!
echo -e "${GREEN}✅ Painel iniciado (PID: $PAINEL_PID)${NC}"
echo "   Logs: logs/painel.log"
cd ..

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ AMBOS SERVIÇOS INICIADOS!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📋 Informações:"
echo "   Bot:   http://localhost (terminal do WhatsApp)"
echo "   Painel: http://localhost:3000"
echo ""
echo "📝 Ver logs em tempo real:"
echo "   tail -f logs/bot.log"
echo "   tail -f logs/painel.log"
echo ""
echo "🛑 Para parar:"
echo "   kill $BOT_PID"
echo "   kill $PAINEL_PID"
echo "   Ou pressione Ctrl+C (podem ser necessários múltiplos)"
echo ""

# Aguardar sinal SIGINT
trap "
    echo ''
    echo -e '${YELLOW}Desligando serviços...${NC}'
    kill $BOT_PID 2>/dev/null
    kill $PAINEL_PID 2>/dev/null
    echo -e '${GREEN}✅ Desligado${NC}'
    exit 0
" SIGINT

# Manter script rodando
wait
