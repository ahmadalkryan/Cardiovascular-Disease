# infrastructure/repositories/template_repository.py
"""Template Repository"""

from .base_repository import BaseRepository
from infrastructure.database import Template


class TemplateRepository(BaseRepository):
    """Repository for Template model"""
    
    def __init__(self):
        super().__init__(Template)
    
    def get_by_category(self, category):
        return self.model.query.filter_by(category=category).all()
    
    def get_active(self):
        return self.model.query.filter_by(is_active=True).all()
    
    def get_by_title(self, title):
        return self.model.query.filter_by(title=title).first()