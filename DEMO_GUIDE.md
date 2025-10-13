# Guia de Demonstração - Quantum Print
**Data:** 29/09/2025  
**Apresentador:** Freenelson (Frontend Specialist)  
**Versão:** 1.0.0

## 📋 Preparação para Demo

### Requisitos Técnicos
- Computador com Node.js e Python instalados
- Navegador Chrome ou Firefox atualizado
- Arquivos de teste disponíveis em `/test_files/`
- Terminais separados para frontend e backend

### Checklist Pré-Demo
- [ ] Iniciar backend FastAPI (porta 8000)
- [ ] Iniciar frontend React (porta 5173)
- [ ] Verificar conexão entre frontend e backend
- [ ] Testar upload de arquivo PDF
- [ ] Limpar projetos de teste anteriores (opcional)
- [ ] Preparar PDF de demonstração (`test_document.pdf`)

## 🚀 Roteiro da Demonstração

### 1. Introdução (2 minutos)
- Apresentar o conceito do Quantum Print
- Explicar o problema que estamos resolvendo (imposição de formas irregulares)
- Mencionar a inspiração no ESKO Phoenix e nossos diferenciais

### 2. Visão Geral da Arquitetura (3 minutos)
- Mostrar diagrama da arquitetura (opcional)
- Explicar brevemente a stack tecnológica
- Destacar a integração frontend/backend

### 3. Demonstração Prática (10 minutos)

#### Passo 1: Iniciar os Servidores
```bash
# Terminal 1 - Backend
cd /home/ubuntu/quantum-print/backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd /home/ubuntu/quantum-print/quantum-print-frontend
npm run dev
```

#### Passo 2: Acessar a Interface
- Abrir o navegador em `http://localhost:5173/`
- Mostrar a interface inicial limpa
- Destacar os componentes principais (Canvas, Toolbar, Upload)

#### Passo 3: Criar Novo Projeto
- Clicar em "Novo Projeto"
- Definir dimensões da chapa (ex: 500mm x 700mm)
- Mostrar a grade do Canvas e explicar o sistema de snap to grid

#### Passo 4: Upload de PDF
- Arrastar o arquivo `test_document.pdf` para a área de upload
- Mostrar o feedback visual durante o upload
- Destacar como o backend processa o PDF e extrai dimensões

#### Passo 5: Manipulação de Layout
- Arrastar itens pelo Canvas
- Demonstrar o snap to grid em ação
- Rotacionar alguns itens (usando a ferramenta de rotação)
- Mostrar como os itens mantêm suas proporções originais

#### Passo 6: Sistema de Undo/Redo
- Fazer algumas alterações no layout
- Usar o botão Undo para reverter
- Usar o botão Redo para refazer
- Explicar como o histórico é mantido

#### Passo 7: Salvar Projeto
- Clicar em "Salvar Projeto"
- Mostrar a mensagem de confirmação
- Explicar como o projeto é salvo no backend (formato JSON)

#### Passo 8: Carregar Projeto
- Clicar em "Carregar Projeto"
- Selecionar o projeto recém-salvo
- Mostrar como o layout é restaurado exatamente como estava

### 4. Funcionalidades Avançadas (5 minutos)

#### Demonstração de Rotação Variável
- Selecionar um item
- Usar a ferramenta de rotação livre
- Mostrar como o ângulo pode ser ajustado precisamente
- Destacar a importância para formas irregulares

#### Demonstração de Seleção Múltipla
- Selecionar vários itens (com Shift ou área de seleção)
- Mover os itens selecionados juntos
- Aplicar rotação a múltiplos itens

#### Visualização de Informações
- Mostrar as coordenadas dos itens
- Exibir dimensões e ângulo de rotação
- Destacar como isso ajuda na precisão do layout

### 5. Roadmap e Próximos Passos (3 minutos)
- Apresentar o roadmap de desenvolvimento
- Destacar as próximas funcionalidades planejadas
- Mencionar o cronograma estimado

### 6. Perguntas e Respostas (5 minutos)
- Abrir espaço para perguntas
- Estar preparado para questões técnicas e de negócio
- Ter screenshots de backup caso ocorra algum problema técnico

## 🎯 Pontos-Chave a Destacar

### Diferenciais Técnicos
- **Canvas HTML5 Avançado** - Performance e responsividade
- **Integração Real com PDF** - Não apenas simulação
- **Arquitetura Escalável** - Pronta para crescer
- **UX/UI Profissional** - Fácil de aprender e usar

### Benefícios para o Usuário
- **Economia de Material** - Melhor aproveitamento de chapa
- **Flexibilidade** - Trabalha com formas irregulares
- **Produtividade** - Interface intuitiva e rápida
- **Precisão** - Snap to grid e rotação variável

## 🔄 Plano de Contingência

### Problemas Potenciais e Soluções
- **Backend não inicia**: Verificar logs, reiniciar com `--reload`
- **Frontend não conecta**: Verificar CORS, usar modo de desenvolvimento
- **Upload falha**: Ter PDF alternativo pronto
- **Demonstração lenta**: Ter screenshots/vídeo de backup

### Perguntas Difíceis Antecipadas
- **Comparação com ESKO Phoenix**: "Nosso foco é o mercado brasileiro, com preço acessível e suporte local"
- **Timeline para versão comercial**: "Estamos seguindo um roadmap de 12 semanas, com entregas incrementais"
- **Limitações atuais**: "Este é um protótipo funcional, estamos priorizando as funcionalidades mais importantes primeiro"

## 📝 Notas Adicionais

- Falar devagar e claramente
- Fazer pausas para perguntas
- Destacar o trabalho em equipe
- Mencionar que este é um protótipo, não a versão final
- Ter confiança no produto - ele funciona!

---

*Guia preparado por Freenelson - Frontend Specialist*  
*Quantum Print Development Team*
