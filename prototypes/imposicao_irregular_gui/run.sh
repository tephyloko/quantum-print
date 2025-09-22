#!/bin/bash

# Instalar as dependências
pip install PyQt5 PyMuPDF reportlab

# Executar a aplicação GUI
python3.11 gui_imposicao.py

echo "\nAplicação GUI iniciada. Verifique 'imposicao_final.pdf' após a geração."

