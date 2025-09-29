#!/usr/bin/env python3
"""
Script de teste para a API do Quantum Print
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa se a API está funcionando"""
    print("🔍 Testando saúde da API...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_create_project():
    """Testa criação de projeto"""
    print("\n🔍 Testando criação de projeto...")
    
    params = {
        "name": "Projeto Teste API",
        "description": "Projeto criado via script de teste",
        "sheet_width": 297.0,
        "sheet_height": 420.0
    }
    
    response = requests.post(f"{BASE_URL}/api/projects/", params=params)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json().get("project_id")
    return None

def test_list_projects():
    """Testa listagem de projetos"""
    print("\n🔍 Testando listagem de projetos...")
    response = requests.get(f"{BASE_URL}/api/projects/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def main():
    print("🚀 Iniciando testes da API Quantum Print")
    print("=" * 50)
    
    # Teste 1: Health check
    if not test_health():
        print("❌ API não está respondendo!")
        return
    
    # Teste 2: Criar projeto
    project_id = test_create_project()
    if not project_id:
        print("❌ Falha na criação de projeto!")
        return
    
    print(f"✅ Projeto criado com ID: {project_id}")
    
    # Teste 3: Listar projetos
    if not test_list_projects():
        print("❌ Falha na listagem de projetos!")
        return
    
    print("\n🎉 Todos os testes passaram!")
    print("✅ Backend está funcionando corretamente!")

if __name__ == "__main__":
    main()
