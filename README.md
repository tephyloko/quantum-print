# Quantum Print

![Quantum Print Logo](https://via.placeholder.com/800x200/0d47a1/ffffff?text=Quantum+Print)

**Sistema Avançado de Imposição Gráfica**

## Sobre o Projeto

Quantum Print é um sistema avançado de imposição gráfica desenvolvido para ser o "ESKO Phoenix brasileiro", oferecendo uma solução completa para gráficas que precisam otimizar o encaixe de peças irregulares em chapas de impressão.

O sistema foi projetado com foco especial em formas não-retangulares, como ímãs e adesivos especiais, permitindo rotação em ângulos variáveis para maximizar o aproveitamento de material e minimizar desperdício.

## Características Principais

- **Interface Moderna e Intuitiva**: Canvas HTML5 com drag & drop, rotação e snap to grid
- **Suporte a Formas Irregulares**: Otimizado para ímãs e formas não-retangulares
- **Rotação em Ângulos Variáveis**: Não limitado a múltiplos de 90°
- **Integração com PDFs Reais**: Visualização precisa do resultado final
- **Sistema Completo de Undo/Redo**: Histórico de ações para fácil correção
- **Persistência de Projetos**: Salvamento e carregamento de layouts
- **API REST Completa**: Interface programática para integração

## Tecnologias Utilizadas

### Frontend
- React
- Canvas HTML5
- shadcn/ui (componentes UI)

### Backend
- Python
- FastAPI
- SQLAlchemy
- PyPDF2

### Banco de Dados
- SQLite (desenvolvimento)
- PostgreSQL (recomendado para produção)

## Estrutura do Projeto

```
quantum-print/
├── backend/                # Servidor FastAPI
│   ├── app/
│   │   ├── main.py         # Aplicação principal
│   │   ├── database.py     # Configuração do banco
│   │   ├── models/         # Modelos de dados
│   │   ├── routes/         # Rotas da API
│   │   ├── services/       # Lógica de negócio
│   │   ├── uploads/        # Arquivos PDF enviados
│   │   └── projects/       # Projetos salvos
│   └── requirements.txt    # Dependências Python
│
├── quantum-print-frontend/ # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── services/       # Serviços de API
│   │   ├── hooks/          # Hooks personalizados
│   │   └── App.jsx         # Componente principal
│   ├── public/             # Arquivos estáticos
│   └── package.json        # Dependências Node.js
│
├── test_files/             # Arquivos para teste
├── BRAINROOM.md            # Documentação central
├── TESTE_REPORT.md         # Relatório de testes
├── DEMO_PRESENTATION.md    # Apresentação para demo
├── DEMO_GUIDE.md           # Guia de demonstração
├── IMPROVEMENT_PLAN.md     # Plano de melhorias
├── ENTREGA_FINAL.md        # Documentação de entrega
├── start.sh                # Script de inicialização
└── README.md               # Este arquivo
```

## Instalação e Execução

### Requisitos

- Node.js 14+ e npm
- Python 3.8+
- Navegador moderno (Chrome, Firefox, Edge)

### Passos para Execução

1. Clone o repositório:
```bash
git clone https://github.com/tephyloko/quantum-print.git
cd quantum-print
```

2. Execute o script de inicialização:
```bash
./start.sh
```

3. Acesse a interface no navegador:
```
http://localhost:5173
```

O script `start.sh` automatiza todo o processo de configuração e inicialização, incluindo:
- Instalação de dependências do frontend e backend
- Configuração do ambiente virtual Python
- Inicialização dos servidores frontend e backend
- Abertura automática do navegador

### Execução Manual

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd quantum-print-frontend
npm install
npm run dev
```

## Documentação

O projeto inclui documentação abrangente para diferentes aspectos:

- **BRAINROOM.md**: Documentação central do projeto, incluindo visão geral, roadmap e decisões estratégicas
- **TESTE_REPORT.md**: Relatório detalhado dos testes realizados e resultados obtidos
- **DEMO_PRESENTATION.md**: Apresentação para demonstração do sistema
- **DEMO_GUIDE.md**: Guia passo a passo para demonstração das funcionalidades
- **IMPROVEMENT_PLAN.md**: Plano detalhado de melhorias e otimizações futuras
- **ENTREGA_FINAL.md**: Documentação completa de entrega do projeto

## API REST

O backend expõe uma API REST completa para interação com o sistema:

- `GET /` - Health check da API
- `POST /api/projects/` - Criar projeto
- `GET /api/projects/` - Listar projetos
- `GET /api/projects/{id}` - Obter projeto específico
- `POST /api/projects/{id}/upload` - Upload de PDF
- `PUT /api/projects/{id}/layout` - Salvar layout

Documentação completa da API disponível em `http://localhost:8000/docs` quando o servidor está em execução.

## Roadmap

O desenvolvimento futuro do Quantum Print seguirá estas prioridades:

1. **Algoritmos de Nesting Avançados**: Otimização automática de encaixe
2. **Análise Avançada de PDF**: Detecção de marcas de corte e sangria
3. **Sistema de Exportação Completo**: Geração de PDFs finais para produção
4. **Dashboard Analítico**: Métricas de aproveitamento e economia
5. **Integração com Sistemas Externos**: Conectores para ERPs e sistemas gráficos

Para detalhes completos sobre as melhorias propostas, consulte o arquivo `IMPROVEMENT_PLAN.md`.

## Equipe de Desenvolvimento

- **Product Owner** - Visão de negócio e validação
- **Operelson** - Dev Técnico Backend/Core
- **Chefenelson** - Gerente de Projeto e Arquitetura
- **Freenelson** - Frontend Specialist, UX/UI Developer, QA/Testing

## Licença

Este projeto é propriedade intelectual da empresa desenvolvedora. Todos os direitos reservados.

---

*Quantum Print - O futuro da imposição gráfica no Brasil*
