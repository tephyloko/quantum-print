"""
Módulo de Cálculo de Imposição - Quantum Print
Sistema para calcular o número máximo de itens que cabem em uma folha.

Este módulo implementa algoritmos para resolver o problema de empacotamento bidimensional,
considerando a possibilidade de rotação dos produtos.
"""

import math
from typing import Tuple, Dict, Any


def calcular_imposicao(largura_produto: float, altura_produto: float, 
                      largura_folha: float, altura_folha: float) -> int:
    """
    Calcula o número máximo de itens que cabem em uma folha considerando rotação.
    
    Esta função implementa uma abordagem heurística simples e eficiente para o problema
    de empacotamento bidimensional. Considera tanto a orientação original quanto a
    rotacionada do produto para maximizar o aproveitamento da folha.
    
    Args:
        largura_produto (float): Largura do produto em unidades de medida
        altura_produto (float): Altura do produto em unidades de medida
        largura_folha (float): Largura da folha em unidades de medida
        altura_folha (float): Altura da folha em unidades de medida
    
    Returns:
        int: Número máximo de itens que cabem na folha
    
    Raises:
        ValueError: Se alguma dimensão for menor ou igual a zero
    
    Examples:
        >>> calcular_imposicao(10, 15, 100, 150)
        100
        >>> calcular_imposicao(20, 10, 100, 150)
        75
    """
    
    # Validação de entrada
    if any(dim <= 0 for dim in [largura_produto, altura_produto, largura_folha, altura_folha]):
        raise ValueError("Todas as dimensões devem ser maiores que zero")
    
    # Verifica se o produto cabe na folha em pelo menos uma orientação
    if not _produto_cabe_na_folha(largura_produto, altura_produto, largura_folha, altura_folha):
        return 0
    
    # Calcula imposição sem rotação
    imposicao_normal = _calcular_imposicao_orientacao(
        largura_produto, altura_produto, largura_folha, altura_folha
    )
    
    # Calcula imposição com rotação (se as dimensões forem diferentes)
    imposicao_rotacionada = 0
    if largura_produto != altura_produto:
        imposicao_rotacionada = _calcular_imposicao_orientacao(
            altura_produto, largura_produto, largura_folha, altura_folha
        )
    
    # Retorna o melhor resultado
    return max(imposicao_normal, imposicao_rotacionada)


def _produto_cabe_na_folha(largura_produto: float, altura_produto: float,
                          largura_folha: float, altura_folha: float) -> bool:
    """
    Verifica se o produto cabe na folha em pelo menos uma orientação.
    
    Args:
        largura_produto (float): Largura do produto
        altura_produto (float): Altura do produto
        largura_folha (float): Largura da folha
        altura_folha (float): Altura da folha
    
    Returns:
        bool: True se o produto cabe na folha, False caso contrário
    """
    # Orientação normal
    cabe_normal = (largura_produto <= largura_folha and altura_produto <= altura_folha)
    
    # Orientação rotacionada
    cabe_rotacionado = (altura_produto <= largura_folha and largura_produto <= altura_folha)
    
    return cabe_normal or cabe_rotacionado


def _calcular_imposicao_orientacao(largura_produto: float, altura_produto: float,
                                  largura_folha: float, altura_folha: float) -> int:
    """
    Calcula a imposição para uma orientação específica do produto.
    
    Utiliza o algoritmo de divisão simples para determinar quantos produtos
    cabem em cada dimensão da folha.
    
    Args:
        largura_produto (float): Largura do produto na orientação atual
        altura_produto (float): Altura do produto na orientação atual
        largura_folha (float): Largura da folha
        altura_folha (float): Altura da folha
    
    Returns:
        int: Número de itens que cabem nesta orientação
    """
    # Verifica se o produto cabe na folha nesta orientação
    if largura_produto > largura_folha or altura_produto > altura_folha:
        return 0
    
    # Calcula quantos produtos cabem em cada dimensão
    produtos_largura = int(largura_folha // largura_produto)
    produtos_altura = int(altura_folha // altura_produto)
    
    return produtos_largura * produtos_altura


def calcular_imposicao_detalhada(largura_produto: float, altura_produto: float,
                                largura_folha: float, altura_folha: float) -> Dict[str, Any]:
    """
    Calcula a imposição com informações detalhadas sobre o resultado.
    
    Esta função fornece não apenas o número máximo de itens, mas também
    informações sobre a orientação escolhida, aproveitamento da folha e
    área desperdiçada.
    
    Args:
        largura_produto (float): Largura do produto
        altura_produto (float): Altura do produto
        largura_folha (float): Largura da folha
        altura_folha (float): Altura da folha
    
    Returns:
        Dict[str, Any]: Dicionário com informações detalhadas:
            - quantidade: número máximo de itens
            - orientacao: 'normal' ou 'rotacionada'
            - aproveitamento: percentual de aproveitamento da folha
            - area_desperdicada: área não utilizada da folha
            - produtos_largura: número de produtos na largura
            - produtos_altura: número de produtos na altura
    """
    
    # Validação de entrada
    if any(dim <= 0 for dim in [largura_produto, altura_produto, largura_folha, altura_folha]):
        raise ValueError("Todas as dimensões devem ser maiores que zero")
    
    # Calcula para ambas as orientações
    resultado_normal = _calcular_detalhes_orientacao(
        largura_produto, altura_produto, largura_folha, altura_folha, "normal"
    )
    
    resultado_rotacionado = _calcular_detalhes_orientacao(
        altura_produto, largura_produto, largura_folha, altura_folha, "rotacionada"
    )
    
    # Retorna o melhor resultado
    if resultado_normal["quantidade"] >= resultado_rotacionado["quantidade"]:
        return resultado_normal
    else:
        return resultado_rotacionado


def _calcular_detalhes_orientacao(largura_produto: float, altura_produto: float,
                                 largura_folha: float, altura_folha: float,
                                 orientacao: str) -> Dict[str, Any]:
    """
    Calcula detalhes da imposição para uma orientação específica.
    
    Args:
        largura_produto (float): Largura do produto na orientação atual
        altura_produto (float): Altura do produto na orientação atual
        largura_folha (float): Largura da folha
        altura_folha (float): Altura da folha
        orientacao (str): 'normal' ou 'rotacionada'
    
    Returns:
        Dict[str, Any]: Detalhes da imposição para esta orientação
    """
    
    # Verifica se o produto cabe na folha
    if largura_produto > largura_folha or altura_produto > altura_folha:
        return {
            "quantidade": 0,
            "orientacao": orientacao,
            "aproveitamento": 0.0,
            "area_desperdicada": largura_folha * altura_folha,
            "produtos_largura": 0,
            "produtos_altura": 0
        }
    
    # Calcula quantos produtos cabem em cada dimensão
    produtos_largura = int(largura_folha // largura_produto)
    produtos_altura = int(altura_folha // altura_produto)
    quantidade = produtos_largura * produtos_altura
    
    # Calcula áreas
    area_folha = largura_folha * altura_folha
    area_produto = largura_produto * altura_produto
    area_utilizada = quantidade * area_produto
    area_desperdicada = area_folha - area_utilizada
    aproveitamento = (area_utilizada / area_folha) * 100 if area_folha > 0 else 0
    
    return {
        "quantidade": quantidade,
        "orientacao": orientacao,
        "aproveitamento": round(aproveitamento, 2),
        "area_desperdicada": round(area_desperdicada, 2),
        "produtos_largura": produtos_largura,
        "produtos_altura": produtos_altura
    }


# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    print("=== Teste do Sistema de Imposição Quantum Print ===")
    
    # Exemplo 1: Cartão de visita em folha A4
    largura_cartao = 85  # mm
    altura_cartao = 55   # mm
    largura_a4 = 210     # mm
    altura_a4 = 297      # mm
    
    quantidade = calcular_imposicao(largura_cartao, altura_cartao, largura_a4, altura_a4)
    detalhes = calcular_imposicao_detalhada(largura_cartao, altura_cartao, largura_a4, altura_a4)
    
    print(f"\nExemplo: Cartão de visita ({largura_cartao}x{altura_cartao}mm) em folha A4 ({largura_a4}x{altura_a4}mm)")
    print(f"Quantidade máxima: {quantidade} cartões")
    print(f"Orientação: {detalhes['orientacao']}")
    print(f"Aproveitamento: {detalhes['aproveitamento']}%")
    print(f"Distribuição: {detalhes['produtos_largura']} x {detalhes['produtos_altura']}")
