# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables
from .routes import projects

# Cria as tabelas no banco de dados
create_tables()

app = FastAPI(
    title="Quantum Print API",
    description="API para o sistema de imposição inteligente Quantum Print.",
    version="0.1.0",
)

# Configuração CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(projects.router)

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à API do Quantum Print!",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "quantum-print-api"}

