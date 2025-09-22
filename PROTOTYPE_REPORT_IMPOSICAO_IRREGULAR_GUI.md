# Relatório de Protótipo: Imposição Irregular com GUI

**Data:** 22 de Setembro de 2025
**Autor:** Freenelson (Manus AI)
**Versão:** 1.0

## 1. Introdução

Este relatório documenta o desenvolvimento de um protótipo de sistema de imposição com Interface Gráfica (GUI) focado na demonstração da imposição de formas irregulares com rotação. Este protótipo foi desenvolvido em resposta à necessidade de visualizar e validar a lógica de encaixe (nesting) para materiais como ímãs, onde a otimização do espaço é crucial. O objetivo é servir como uma prova de conceito e uma base para futuras discussões e desenvolvimento dentro do projeto Quantum Print.

## 2. Visão Geral do Protótipo

O protótipo é uma aplicação desktop desenvolvida em Python, utilizando `PyQt5` para a interface gráfica e `PyMuPDF` para a manipulação e renderização de arquivos PDF. Ele permite ao usuário:

*   Selecionar um arquivo PDF de entrada.
*   Configurar parâmetros de imposição (dimensões da folha, dimensões da forma, rotações permitidas, preenchimento, número de formas).
*   Visualizar uma pré-visualização interativa da imposição, mostrando o conteúdo do PDF de entrada rotacionado e posicionado.
*   Gerar um arquivo PDF final com a imposição aplicada.

## 3. Funcionalidades Implementadas

*   **Interface Gráfica (GUI):** Desenvolvida com PyQt5, oferece uma interface intuitiva para configuração de parâmetros e interação.
*   **Seleção de PDF de Entrada:** Permite ao usuário escolher um arquivo PDF para ser usado como a "forma" a ser imposta.
*   **Configuração de Parâmetros:** Campos de entrada para definir largura/altura da folha, largura/altura da forma, ângulos de rotação (0, 90, 180, 270 graus), preenchimento entre as formas e o número total de formas a impor.
*   **Lógica de Encaixe (Nesting) Básico:** Implementa um algoritmo guloso simples que tenta encaixar as formas retangulares na folha, aplicando as rotações permitidas para otimizar o espaço. Ele avança da esquerda para a direita, de cima para baixo, e inicia uma nova linha ou página quando não há mais espaço.
*   **Pré-visualização Visual:** A GUI renderiza uma imagem da folha de imposição, mostrando o conteúdo da primeira página do PDF de entrada (renderizado como imagem) em suas posições e rotações calculadas. Isso oferece feedback visual imediato ao usuário.
*   **Geração de PDF Final:** Cria um novo arquivo PDF onde o conteúdo da primeira página do PDF de entrada é inserido múltiplas vezes, com as rotações e posicionamentos calculados, mantendo a qualidade vetorial do PDF original.
*   **Persistência de Configurações:** As configurações são salvas e carregadas de um arquivo `config.json`.

## 4. Limitações Atuais e Próximos Passos

Este protótipo, embora funcional, possui limitações que devem ser abordadas em futuras iterações para alcançar a visão de um sistema de imposição de classe mundial:

*   **Representação da Forma:** Atualmente, a "forma irregular" é tratada como um *bounding box* retangular. Para uma imposição verdadeiramente irregular, é necessário:
    *   **Análise Geométrica Avançada:** Capacidade de extrair e manipular a geometria vetorial real das formas do PDF de entrada (e.g., contornos de faca, *die-lines*).
    *   **Algoritmos de Nesting Otimizados:** Implementar algoritmos de encaixe (nesting) mais sofisticados (e.g., *true shape nesting*) que considerem a forma real das peças, permitam rotações arbitrárias (não apenas múltiplos de 90 graus) e até mesmo espelhamento para maximizar o aproveitamento do material.
*   **Imposição por Trim/Thru-cut:** A funcionalidade de imposição baseada em *trim* ou áreas de faca (Thru-cut) é crucial. Isso exigirá:
    *   **Detecção de Camadas/Metadados:** Capacidade de identificar e extrair informações de camadas ou cores especiais (spot colors) dentro do PDF que definam as áreas de corte (Thru-cut).
    *   **Integração com o Algoritmo de Nesting:** O algoritmo de encaixe precisará usar essas informações de corte para posicionar as peças, permitindo sobreposições controladas ou compartilhamento de linhas de corte.
*   **Otimização de Performance:** Para grandes volumes de formas ou PDFs complexos, a performance do algoritmo de encaixe e da renderização pode precisar de otimização, possivelmente com o uso de C++ ou bibliotecas mais otimizadas para geometria computacional.
*   **Multi-página/Multi-item:** Atualmente, o protótipo impõe apenas a primeira página do PDF de entrada. Um sistema completo precisaria lidar com múltiplos itens e múltiplas páginas por item.
*   **Marcas de Impressão:** Implementação de marcas de corte, dobras, registro, barras de cores, etc.

## 5. Conclusão

Este protótipo GUI representa um avanço significativo na validação da capacidade de manipular e impor PDFs de forma visual e interativa. Ele serve como uma base sólida para o desenvolvimento futuro do Quantum Print, especialmente na área de imposição irregular. Os próximos passos devem focar na pesquisa e implementação de algoritmos de nesting mais avançados e na integração da detecção de áreas de corte (trim/thru-cut) para atender plenamente às necessidades do mercado brasileiro e global.

## 6. Localização dos Arquivos

Os arquivos do protótipo estão localizados em `quantum-print/prototypes/imposicao_irregular_gui/`:

*   `gui_imposicao.py`: Código-fonte da aplicação GUI.
*   `config.json`: Arquivo de configuração para persistência de parâmetros.
*   `run.sh`: Script para instalação de dependências e execução da aplicação.
