# business/services/report_template_service.py
"""Report Template Service - Template CRUD operations"""

import json
import logging
from datetime import datetime

from infrastructure.database import db, Template, Report

logger = logging.getLogger(__name__)


class ReportTemplateService:
    """Service for managing report templates"""
    
    def create_template(self, title, structure, description=None, category='general'):
        """Create a new template"""
        try:
            template = Template(
                title=title,
                description=description,
                structure_json=json.dumps(structure, ensure_ascii=False),
                category=category,
                is_active=True
            )
            db.session.add(template)
            db.session.commit()
            
            logger.info(f"Template created: {title}")
            return {'success': True, 'template': template.to_dict()}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create template: {e}")
            raise
    
    def get_all_templates(self, category=None):
        """Get all templates with optional category filter"""
        query = Template.query.filter_by(is_active=True)
        if category:
            query = query.filter_by(category=category)
        templates = query.order_by(Template.created_at.desc()).all()
        return [t.to_dict() for t in templates]
    
    def get_template(self, template_id):
        """Get template by ID"""
        template = Template.query.get(template_id)
        if not template:
            return {'success': False}
        return {'success': True, 'template': template.to_dict()}
    
    def update_template(self, template_id, title=None, structure=None, description=None):
        """Update template"""
        try:
            template = Template.query.get(template_id)
            if not template:
                return {'success': False, 'error': 'Template not found'}
            
            if title:
                template.title = title
            if structure:
                template.structure_json = json.dumps(structure, ensure_ascii=False)
            if description:
                template.description = description
            
            template.updated_at = datetime.now()
            db.session.commit()
            
            return {'success': True, 'template': template.to_dict()}
            
        except Exception as e:
            db.session.rollback()
            raise
    
    def delete_template(self, template_id):
        """Delete template"""
        try:
            template = Template.query.get(template_id)
            if not template:
                return {'success': False, 'error': 'Template not found'}
            
            template.is_active = False
            db.session.commit()
            return {'success': True, 'message': 'Template deleted'}
            
        except Exception as e:
            db.session.rollback()
            raise
    
    def get_template_reports(self, template_id):
        """Get all reports for a template"""
        reports = Report.query.filter_by(template_id=template_id).all()
        return [r.to_dict() for r in reports]
    
    def get_default_field_types(self):
        """Get default field types from config"""
        from business.config.field_types import FieldTypes
        return FieldTypes.get_all()