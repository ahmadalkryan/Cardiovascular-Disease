# business/services/report_template_service.py
"""Template Service - CRUD operations for report templates"""

import json
import os
from datetime import datetime
from infrastructure.database import db, Template, Report
from business.config.field_types import FieldTypes


class ReportTemplateService:
    """Handles CRUD operations for report templates"""
    
    # ═══════════════════════════════════════════════
    # Create
    # ═══════════════════════════════════════════════
    def create_template(self, title, structure, description=None, category='general'):
        """Create a new report template"""
        try:
            template = Template(
                title=title,
                description=description,
                structure_json=json.dumps(structure, ensure_ascii=False),
                category=category
            )
            db.session.add(template)
            db.session.commit()
            return {'success': True, 'template': template.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    # ═══════════════════════════════════════════════
    # Read
    # ═══════════════════════════════════════════════
    def get_all_templates(self, category=None):
        """Get all active templates, optionally filtered by category"""
        query = Template.query.filter_by(is_active=True)
        if category:
            query = query.filter_by(category=category)
        templates = query.order_by(Template.created_at.desc()).all()
        return [t.to_dict() for t in templates]
    
    def get_template(self, template_id):
        """Get a single template with its reports"""
        template = Template.query.get(template_id)
        if template:
            data = template.to_dict()
            data['reports'] = [r.to_dict() for r in template.reports]
            return {'success': True, 'template': data}
        return {'success': False, 'error': 'Template not found'}
    
    def get_template_reports(self, template_id):
        """Get all reports for a specific template"""
        template = Template.query.get(template_id)
        if not template:
            return {'success': False, 'error': 'Template not found'}
        
        reports = Report.query.filter_by(template_id=template_id)\
                    .order_by(Report.created_at.desc()).all()
        
        return {
            'success': True,
            'template': template.to_dict(),
            'reports': [r.to_dict() for r in reports]
        }
    
    # ═══════════════════════════════════════════════
    # Update
    # ═══════════════════════════════════════════════
    def update_template(self, template_id, title=None, structure=None, description=None):
        """Update an existing template"""
        try:
            template = Template.query.get(template_id)
            if not template:
                return {'success': False, 'error': 'Template not found'}
            
            if title is not None:
                template.title = title
            if description is not None:
                template.description = description
            if structure is not None:
                template.structure_json = json.dumps(structure, ensure_ascii=False)
            
            template.updated_at = datetime.utcnow()
            db.session.commit()
            return {'success': True, 'template': template.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    # ═══════════════════════════════════════════════
    # Delete
    # ═══════════════════════════════════════════════
    def delete_template(self, template_id):
        """Delete template and all associated reports + PDF files"""
        try:
            template = Template.query.get(template_id)
            if not template:
                return {'success': False, 'error': 'Template not found'}
            
            # Delete PDF files first
            for report in template.reports:
                if report.pdf_path and os.path.exists(report.pdf_path):
                    try:
                        os.remove(report.pdf_path)
                    except Exception as e:
                        print(f"⚠️ Could not delete PDF: {e}")
            
            # Delete template (cascade deletes reports)
            db.session.delete(template)
            db.session.commit()
            return {'success': True, 'message': f'Template "{template.title}" deleted'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    # ═══════════════════════════════════════════════
    # Field Types
    # ═══════════════════════════════════════════════
    def get_default_field_types(self):
        """Return available field types for template builder"""
        return FieldTypes.get_all()