"""
Serviço para processamento de arquivos PDF
"""
import os
from typing import List, Dict, Any
from PyPDF2 import PdfReader
import tempfile

class PDFService:
    """
    Serviço responsável por processar arquivos PDF e extrair informações
    """
    
    @staticmethod
    def process_pdf(file_path: str) -> Dict[str, Any]:
        """
        Processa um arquivo PDF e extrai informações básicas
        
        Args:
            file_path: Caminho para o arquivo PDF
            
        Returns:
            Dict com informações do PDF (número de páginas, dimensões, etc.)
        """
        try:
            reader = PdfReader(file_path)
            num_pages = len(reader.pages)
            
            # Extrai dimensões da primeira página (em pontos)
            first_page = reader.pages[0]
            mediabox = first_page.mediabox
            
            # Converte de pontos para milímetros (1 ponto = 0.352778 mm)
            width_mm = float(mediabox.width) * 0.352778
            height_mm = float(mediabox.height) * 0.352778
            
            return {
                "success": True,
                "num_pages": num_pages,
                "width_mm": round(width_mm, 2),
                "height_mm": round(height_mm, 2),
                "width_points": float(mediabox.width),
                "height_points": float(mediabox.height)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def extract_pages_info(file_path: str) -> List[Dict[str, Any]]:
        """
        Extrai informações de todas as páginas do PDF
        
        Args:
            file_path: Caminho para o arquivo PDF
            
        Returns:
            Lista com informações de cada página
        """
        try:
            reader = PdfReader(file_path)
            pages_info = []
            
            for i, page in enumerate(reader.pages):
                mediabox = page.mediabox
                width_mm = float(mediabox.width) * 0.352778
                height_mm = float(mediabox.height) * 0.352778
                
                pages_info.append({
                    "page_number": i + 1,
                    "width_mm": round(width_mm, 2),
                    "height_mm": round(height_mm, 2),
                    "width_points": float(mediabox.width),
                    "height_points": float(mediabox.height)
                })
            
            return pages_info
            
        except Exception as e:
            return []
    
    @staticmethod
    def save_uploaded_file(file_content: bytes, filename: str) -> str:
        """
        Salva arquivo enviado no sistema de arquivos
        
        Args:
            file_content: Conteúdo do arquivo em bytes
            filename: Nome do arquivo
            
        Returns:
            Caminho onde o arquivo foi salvo
        """
        # Cria diretório de uploads se não existir
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Gera nome único para evitar conflitos
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Salva o arquivo
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return file_path
