# infrastructure/database.py
"""Database Setup - SQLAlchemy Models ( Templates + Reports)"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import uuid
import logging
from sqlalchemy import text  

from application.exceptions import DatabaseError

logger = logging.getLogger(__name__)

db = SQLAlchemy()


def generate_id(prefix=''):
    """Generate a unique ID with optional prefix."""
    return f"{prefix}{str(uuid.uuid4())[:8].upper()}"


# ================================================
# Template Model
# ================================================
class Template(db.Model):
    """Report Template Model - Stores the structure/design of medical report templates"""
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    structure_json = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default='general')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship to Reports
    reports = db.relationship('Report', backref='template', lazy=True,
                              cascade="all, delete-orphan", passive_deletes=True)
    
    @property
    def report_count(self):
        return len(self.reports)
    
    @property
    def field_count(self):
        structure = self.get_structure()
        return len(structure) if structure else 0
    
    def get_structure(self):
        try:
            return json.loads(self.structure_json)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def to_dict(self, include_reports=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'structure': self.get_structure(),
            'category': self.category,
            'is_active': self.is_active,
            'report_count': self.report_count,
            'field_count': self.field_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None,
        }
        if include_reports:
            data['reports'] = [r.to_dict() for r in self.reports]
        return data


# ================================================
# Report Model
# ================================================
class Report(db.Model):
    """Medical Report Model - Stores filled reports for patients"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_uid = db.Column(db.String(50), unique=True, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id', ondelete='CASCADE'), nullable=False)
    
    
    patient_uid = db.Column(db.String(50), nullable=True, default=None)
    
    data_json = db.Column(db.Text, nullable=False)
    pdf_path = db.Column(db.String(500), nullable=True, default=None)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    @property
    def has_pdf(self):
        import os
        return bool(self.pdf_path and os.path.exists(self.pdf_path))
    
    @property
    def template_title(self):
        return self.template.title if self.template else None
    
    def get_data(self):
        try:
            return json.loads(self.data_json)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def get_field_value(self, field_name, default='-'):
        return self.get_data().get(field_name, default)
    
    def to_dict(self, include_template=False):
        data = {
            'id': self.id,
            'report_uid': self.report_uid,
            'template_id': self.template_id,
            'template_title': self.template_title,
            'patient_uid': self.patient_uid or '',
            'data': self.get_data(),
            'pdf_path': self.pdf_path,
            'has_pdf': self.has_pdf,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None,
        }
        if include_template and self.template:
            data['template'] = self.template.to_dict()
        return data


# ================================================
# Database Initialization 
# ================================================
def init_db(app):
    """Initialize database with Flask application."""
    try:
        db.init_app(app)
        
        with app.app_context():
           
            with db.engine.connect() as conn:
               
                conn.execute(text("PRAGMA foreign_keys = ON"))
                conn.execute(text("PRAGMA journal_mode = WAL"))
                
                
                result = conn.execute(text("PRAGMA integrity_check"))
                row = result.fetchone()
                if row and row[0] != 'ok':
                    raise DatabaseError(f"Integrity check failed: {row[0]}")
                
                conn.commit()  
            
            
            db.create_all()
            
            print("=" * 60)
            print("  Database Initialized")
            print("=" * 60)
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise DatabaseError(f"فشل تهيئة قاعدة البيانات: {str(e)}")