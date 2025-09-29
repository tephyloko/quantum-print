"""
Modelos de dados para o sistema Quantum Print
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Project(Base):
    """
    Modelo para projetos de imposição
    """
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Dimensões da chapa
    sheet_width = Column(Float, nullable=False)
    sheet_height = Column(Float, nullable=False)
    
    # Arquivo PDF original
    pdf_filename = Column(String(255), nullable=True)
    pdf_path = Column(String(500), nullable=True)
    
    # Layout da imposição (JSON com posições dos itens)
    layout_data = Column(JSON, nullable=True)
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class ProjectItem(Base):
    """
    Modelo para itens individuais dentro de um projeto
    """
    __tablename__ = "project_items"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)  # FK para Project
    
    # Dimensões do item
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    
    # Posição na chapa
    x_position = Column(Float, default=0)
    y_position = Column(Float, default=0)
    
    # Rotação (0, 90, 180, 270 graus)
    rotation = Column(Integer, default=0)
    
    # Metadados do item
    name = Column(String(255), nullable=True)
    page_number = Column(Integer, nullable=True)  # Página do PDF original
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<ProjectItem(id={self.id}, project_id={self.project_id})>"
