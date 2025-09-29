"""
Rotas da API para gerenciamento de projetos
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import os

from ..database import get_db
from ..models.project import Project, ProjectItem
from ..services.pdf_service import PDFService

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/", response_model=Dict[str, Any])
def create_project(
    name: str,
    description: str = "",
    sheet_width: float = 297.0,  # A4 padrão em mm
    sheet_height: float = 420.0,
    db: Session = Depends(get_db)
):
    """
    Cria um novo projeto de imposição
    """
    project = Project(
        name=name,
        description=description,
        sheet_width=sheet_width,
        sheet_height=sheet_height
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "success": True,
        "project_id": project.id,
        "message": f"Projeto '{name}' criado com sucesso"
    }

@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Obtém informações de um projeto específico
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Busca itens do projeto
    items = db.query(ProjectItem).filter(ProjectItem.project_id == project_id).all()
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "sheet_width": project.sheet_width,
        "sheet_height": project.sheet_height,
        "pdf_filename": project.pdf_filename,
        "layout_data": project.layout_data,
        "items": [
            {
                "id": item.id,
                "width": item.width,
                "height": item.height,
                "x_position": item.x_position,
                "y_position": item.y_position,
                "rotation": item.rotation,
                "name": item.name,
                "page_number": item.page_number
            }
            for item in items
        ],
        "created_at": project.created_at,
        "updated_at": project.updated_at
    }

@router.get("/")
def list_projects(db: Session = Depends(get_db)):
    """
    Lista todos os projetos
    """
    projects = db.query(Project).all()
    
    return {
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "sheet_width": project.sheet_width,
                "sheet_height": project.sheet_height,
                "created_at": project.created_at
            }
            for project in projects
        ]
    }

@router.post("/{project_id}/upload")
async def upload_pdf(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Faz upload de um arquivo PDF para um projeto
    """
    # Verifica se o projeto existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Verifica se é um arquivo PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")
    
    try:
        # Lê o conteúdo do arquivo
        file_content = await file.read()
        
        # Salva o arquivo no sistema
        file_path = PDFService.save_uploaded_file(file_content, file.filename)
        
        # Processa o PDF
        pdf_info = PDFService.process_pdf(file_path)
        
        if not pdf_info["success"]:
            # Remove arquivo se houve erro no processamento
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Erro ao processar PDF: {pdf_info['error']}")
        
        # Atualiza o projeto com informações do PDF
        project.pdf_filename = file.filename
        project.pdf_path = file_path
        
        # Extrai informações de todas as páginas
        pages_info = PDFService.extract_pages_info(file_path)
        
        # Remove itens existentes do projeto
        db.query(ProjectItem).filter(ProjectItem.project_id == project_id).delete()
        
        # Cria itens para cada página do PDF
        for page_info in pages_info:
            item = ProjectItem(
                project_id=project_id,
                width=page_info["width_mm"],
                height=page_info["height_mm"],
                name=f"Página {page_info['page_number']}",
                page_number=page_info["page_number"]
            )
            db.add(item)
        
        db.commit()
        
        return {
            "success": True,
            "message": f"PDF '{file.filename}' processado com sucesso",
            "pdf_info": pdf_info,
            "pages_count": len(pages_info),
            "pages": pages_info
        }
        
    except Exception as e:
        # Remove arquivo se houve erro
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{project_id}/layout")
def save_layout(
    project_id: int,
    layout_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Salva o layout de imposição de um projeto
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Salva dados do layout
    project.layout_data = layout_data
    
    # Atualiza posições dos itens se fornecidas
    if "items" in layout_data:
        for item_data in layout_data["items"]:
            item_id = item_data.get("id")
            if item_id:
                item = db.query(ProjectItem).filter(
                    ProjectItem.id == item_id,
                    ProjectItem.project_id == project_id
                ).first()
                
                if item:
                    item.x_position = item_data.get("x_position", item.x_position)
                    item.y_position = item_data.get("y_position", item.y_position)
                    item.rotation = item_data.get("rotation", item.rotation)
    
    db.commit()
    
    return {
        "success": True,
        "message": "Layout salvo com sucesso"
    }
