#!/bin/bash

# Script de inicialização do Quantum Print
# Autor: Freenelson (Frontend Specialist)
# Data: 29/09/2025

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "  ██████  ██    ██  █████  ███    ██ ████████ ██    ██ ███    ███"
echo " ██    ██ ██    ██ ██   ██ ████   ██    ██    ██    ██ ████  ████"
echo " ██    ██ ██    ██ ███████ ██ ██  ██    ██    ██    ██ ██ ████ ██"
echo " ██ ▄▄ ██ ██    ██ ██   ██ ██  ██ ██    ██    ██    ██ ██  ██  ██"
echo "  ██████   ██████  ██   ██ ██   ████    ██     ██████  ██      ██"
echo "     ▀▀                                                          "
echo -e "${GREEN}                      PRINT SYSTEM${NC}"
echo -e "${YELLOW}                  Versão 1.0.0 - Demo${NC}\n"

# Diretórios
BACKEND_DIR="$(pwd)/backend"
FRONTEND_DIR="$(pwd)/quantum-print-frontend"

# Verificar se estamos no diretório correto
if [ ! -d "$BACKEND_DIR" ] || [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}Erro: Diretórios do projeto não encontrados.${NC}"
    echo -e "Este script deve ser executado do diretório raiz do projeto Quantum Print."
    echo -e "Execute: cd /caminho/para/quantum-print && ./start.sh"
    exit 1
fi

# Função para verificar dependências
check_dependencies() {
    echo -e "${BLUE}Verificando dependências...${NC}"
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 não encontrado. Por favor, instale Python 3.${NC}"
        exit 1
    else
        PYTHON_VERSION=$(python3 --version)
        echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
    fi
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}Node.js não encontrado. Por favor, instale Node.js.${NC}"
        exit 1
    else
        NODE_VERSION=$(node --version)
        echo -e "${GREEN}✓${NC} Node.js $NODE_VERSION"
    fi
    
    # Verificar npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}npm não encontrado. Por favor, instale npm.${NC}"
        exit 1
    else
        NPM_VERSION=$(npm --version)
        echo -e "${GREEN}✓${NC} npm $NPM_VERSION"
    fi
    
    echo -e "${GREEN}Todas as dependências estão instaladas!${NC}\n"
}

# Função para instalar dependências do backend
setup_backend() {
    echo -e "${BLUE}Configurando backend...${NC}"
    cd "$BACKEND_DIR" || exit
    
    # Verificar se o ambiente virtual existe
    if [ ! -d "venv" ]; then
        echo "Criando ambiente virtual Python..."
        python3 -m venv venv
    fi
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Instalar dependências
    echo "Instalando dependências do backend..."
    pip install -r requirements.txt
    
    # Criar diretórios necessários
    mkdir -p app/uploads
    mkdir -p app/projects
    
    echo -e "${GREEN}Backend configurado com sucesso!${NC}\n"
}

# Função para instalar dependências do frontend
setup_frontend() {
    echo -e "${BLUE}Configurando frontend...${NC}"
    cd "$FRONTEND_DIR" || exit
    
    # Instalar dependências
    echo "Instalando dependências do frontend..."
    npm install
    
    echo -e "${GREEN}Frontend configurado com sucesso!${NC}\n"
}

# Função para iniciar o backend
start_backend() {
    echo -e "${BLUE}Iniciando servidor backend...${NC}"
    cd "$BACKEND_DIR" || exit
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Iniciar servidor FastAPI
    echo "Iniciando FastAPI na porta 8000..."
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    # Verificar se o servidor iniciou corretamente
    sleep 2
    if ps -p $BACKEND_PID > /dev/null; then
        echo -e "${GREEN}Servidor backend iniciado com sucesso! (PID: $BACKEND_PID)${NC}"
        echo -e "API disponível em: ${YELLOW}http://localhost:8000${NC}\n"
    else
        echo -e "${RED}Falha ao iniciar o servidor backend.${NC}"
        exit 1
    fi
}

# Função para iniciar o frontend
start_frontend() {
    echo -e "${BLUE}Iniciando servidor frontend...${NC}"
    cd "$FRONTEND_DIR" || exit
    
    # Iniciar servidor de desenvolvimento React
    echo "Iniciando servidor React na porta 5173..."
    npm run dev &
    FRONTEND_PID=$!
    
    # Verificar se o servidor iniciou corretamente
    sleep 5
    if ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${GREEN}Servidor frontend iniciado com sucesso! (PID: $FRONTEND_PID)${NC}"
        echo -e "Interface disponível em: ${YELLOW}http://localhost:5173${NC}\n"
    else
        echo -e "${RED}Falha ao iniciar o servidor frontend.${NC}"
        exit 1
    fi
}

# Função para abrir o navegador
open_browser() {
    echo -e "${BLUE}Abrindo aplicação no navegador...${NC}"
    sleep 2
    
    # Tentar abrir o navegador (funciona em diferentes sistemas)
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:5173
    elif command -v open &> /dev/null; then
        open http://localhost:5173
    elif command -v start &> /dev/null; then
        start http://localhost:5173
    else
        echo -e "${YELLOW}Não foi possível abrir o navegador automaticamente.${NC}"
        echo -e "Por favor, acesse manualmente: ${YELLOW}http://localhost:5173${NC}"
    fi
}

# Função para mostrar instruções
show_instructions() {
    echo -e "${BLUE}=== QUANTUM PRINT - INSTRUÇÕES ===${NC}"
    echo -e "O sistema está rodando em:"
    echo -e "  - Frontend: ${YELLOW}http://localhost:5173${NC}"
    echo -e "  - Backend API: ${YELLOW}http://localhost:8000${NC}"
    echo -e "  - API Docs: ${YELLOW}http://localhost:8000/docs${NC}"
    echo -e "\nPara parar o sistema, pressione ${RED}CTRL+C${NC}"
    echo -e "${BLUE}===================================${NC}\n"
}

# Função para limpar ao sair
cleanup() {
    echo -e "\n${YELLOW}Encerrando Quantum Print...${NC}"
    
    # Matar processos
    if [ -n "$BACKEND_PID" ]; then
        echo "Parando servidor backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null
    fi
    
    if [ -n "$FRONTEND_PID" ]; then
        echo "Parando servidor frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    echo -e "${GREEN}Sistema encerrado com sucesso!${NC}"
    exit 0
}

# Registrar função de limpeza para quando o script for interrompido
trap cleanup SIGINT SIGTERM

# Executar funções principais
check_dependencies
setup_backend
setup_frontend
start_backend
start_frontend
open_browser
show_instructions

# Manter o script rodando
echo -e "Pressione ${RED}CTRL+C${NC} para encerrar o sistema."
while true; do
    sleep 1
done
