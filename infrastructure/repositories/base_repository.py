# infrastructure/repositories/base_repository.py
"""Base Repository - CRUD operations"""

from infrastructure.database import db


class BaseRepository:
    """Base repository with common CRUD operations"""
    
    def __init__(self, model):
        self.model = model
        self.db = db
    
    def get_by_id(self, id):
        return self.model.query.get(id)
    
    def get_all(self, limit=100, offset=0):
        return self.model.query.offset(offset).limit(limit).all()
    
    def save(self, entity):
        self.db.session.add(entity)
        self.db.session.commit()
        return entity
    
    def delete(self, entity):
        self.db.session.delete(entity)
        self.db.session.commit()
    
    def count(self):
        return self.model.query.count()