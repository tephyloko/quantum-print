# main.py
from fastapi import FastAPI

app = FastAPI(
    title="Quantum Print API",
    description="API para o sistema de imposição inteligente Quantum Print.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Quantum Print!"}

# Aqui virão os endpoints para projetos, upload, etc.

