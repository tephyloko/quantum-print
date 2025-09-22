"""
Testes para o módulo de cálculo de imposição - Quantum Print
Desenvolvido pelo Engenheiro de Qualidade

Este arquivo contém testes unitários para validar o funcionamento correto
da função calcular_imposicao e suas funções auxiliares.
"""

import sys
import os

# Adiciona o diretório src ao path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from imposicao import calcular_imposicao, calcular_imposicao_detalhada


def test_imposicao_simples():
    """
    Teste simples: produto 10x10 em folha 20x20
    Resultado esperado: 4 produtos (2x2)
    """
    print("=== TESTE 1: Imposição Simples ===")
    largura_produto = 10
    altura_produto = 10
    largura_folha = 20
    altura_folha = 20
    
    resultado = calcular_imposicao(largura_produto, altura_produto, largura_folha, altura_folha)
    esperado = 4
    
    print(f"Produto: {largura_produto}x{altura_produto}")
    print(f"Folha: {largura_folha}x{altura_folha}")
    print(f"Resultado obtido: {resultado}")
    print(f"Resultado esperado: {esperado}")
    
    if resultado == esperado:
        print("✅ TESTE PASSOU")
        return True
    else:
        print("❌ TESTE FALHOU")
        return False


def test_imposicao_com_rotacao():
    """
    Teste que exige rotação: produto 2x8 em folha 10x10
    Sem rotação: 5x1 = 5 produtos
    Com rotação: 1x5 = 5 produtos
    Resultado esperado: 5 produtos
    """
    print("\n=== TESTE 2: Imposição com Rotação ===")
    largura_produto = 2
    altura_produto = 8
    largura_folha = 10
    altura_folha = 10
    
    resultado = calcular_imposicao(largura_produto, altura_produto, largura_folha, altura_folha)
    esperado = 5
    
    # Obter detalhes para verificar a orientação escolhida
    detalhes = calcular_imposicao_detalhada(largura_produto, altura_produto, largura_folha, altura_folha)
    
    print(f"Produto: {largura_produto}x{altura_produto}")
    print(f"Folha: {largura_folha}x{altura_folha}")
    print(f"Resultado obtido: {resultado}")
    print(f"Resultado esperado: {esperado}")
    print(f"Orientação escolhida: {detalhes['orientacao']}")
    print(f"Distribuição: {detalhes['produtos_largura']} x {detalhes['produtos_altura']}")
    
    if resultado == esperado:
        print("✅ TESTE PASSOU")
        return True
    else:
        print("❌ TESTE FALHOU")
        return False


def test_imposicao_medidas_quebradas():
    """
    Teste com medidas "quebradas": produto 3.5x8.8 em folha A4 (21x29.7cm)
    Verifica como o sistema lida com números decimais
    """
    print("\n=== TESTE 3: Imposição com Medidas Quebradas ===")
    largura_produto = 3.5
    altura_produto = 8.8
    largura_folha = 21.0
    altura_folha = 29.7
    
    resultado = calcular_imposicao(largura_produto, altura_produto, largura_folha, altura_folha)
    
    # Cálculo manual para verificação:
    # Orientação normal: (21//3.5) * (29.7//8.8) = 6 * 3 = 18
    # Orientação rotacionada: (21//8.8) * (29.7//3.5) = 2 * 8 = 16
    # Esperado: 18 (orientação normal é melhor)
    esperado = 18
    
    # Obter detalhes
    detalhes = calcular_imposicao_detalhada(largura_produto, altura_produto, largura_folha, altura_folha)
    
    print(f"Produto: {largura_produto}x{altura_produto}")
    print(f"Folha: {largura_folha}x{altura_folha} (A4)")
    print(f"Resultado obtido: {resultado}")
    print(f"Resultado esperado: {esperado}")
    print(f"Orientação escolhida: {detalhes['orientacao']}")
    print(f"Distribuição: {detalhes['produtos_largura']} x {detalhes['produtos_altura']}")
    print(f"Aproveitamento: {detalhes['aproveitamento']}%")
    
    if resultado == esperado:
        print("✅ TESTE PASSOU")
        return True
    else:
        print("❌ TESTE FALHOU")
        return False


def test_produto_nao_cabe():
    """
    Teste adicional: produto maior que a folha
    Resultado esperado: 0
    """
    print("\n=== TESTE 4: Produto Não Cabe na Folha ===")
    largura_produto = 25
    altura_produto = 35
    largura_folha = 20
    altura_folha = 30
    
    resultado = calcular_imposicao(largura_produto, altura_produto, largura_folha, altura_folha)
    esperado = 0
    
    print(f"Produto: {largura_produto}x{altura_produto}")
    print(f"Folha: {largura_folha}x{altura_folha}")
    print(f"Resultado obtido: {resultado}")
    print(f"Resultado esperado: {esperado}")
    
    if resultado == esperado:
        print("✅ TESTE PASSOU")
        return True
    else:
        print("❌ TESTE FALHOU")
        return False


def test_validacao_entrada():
    """
    Teste de validação: dimensões inválidas
    Deve gerar ValueError
    """
    print("\n=== TESTE 5: Validação de Entrada ===")
    
    try:
        # Teste com dimensão zero
        calcular_imposicao(0, 10, 20, 30)
        print("❌ TESTE FALHOU - Deveria ter gerado ValueError")
        return False
    except ValueError:
        print("✅ TESTE PASSOU - ValueError gerado corretamente para dimensão zero")
    
    try:
        # Teste com dimensão negativa
        calcular_imposicao(10, -5, 20, 30)
        print("❌ TESTE FALHOU - Deveria ter gerado ValueError")
        return False
    except ValueError:
        print("✅ TESTE PASSOU - ValueError gerado corretamente para dimensão negativa")
    
    return True


def executar_todos_os_testes():
    """
    Executa todos os testes e apresenta um resumo final
    """
    print("=" * 60)
    print("EXECUTANDO TESTES DO MÓDULO DE IMPOSIÇÃO - QUANTUM PRINT")
    print("Desenvolvido pelo Engenheiro de Qualidade")
    print("=" * 60)
    
    testes = [
        test_imposicao_simples,
        test_imposicao_com_rotacao,
        test_imposicao_medidas_quebradas,
        test_produto_nao_cabe,
        test_validacao_entrada
    ]
    
    resultados = []
    
    for teste in testes:
        try:
            resultado = teste()
            resultados.append(resultado)
        except Exception as e:
            print(f"❌ ERRO INESPERADO no teste {teste.__name__}: {e}")
            resultados.append(False)
    
    # Resumo final
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    testes_passaram = sum(resultados)
    total_testes = len(resultados)
    
    for i, (teste, resultado) in enumerate(zip(testes, resultados)):
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"Teste {i+1} ({teste.__name__}): {status}")
    
    print(f"\nResultado Final: {testes_passaram}/{total_testes} testes passaram")
    
    if testes_passaram == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM! O módulo está funcionando corretamente.")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM. Revisar implementação necessária.")
    
    return testes_passaram == total_testes


if __name__ == "__main__":
    executar_todos_os_testes()
