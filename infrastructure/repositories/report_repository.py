# infrastructure/repositories/report_repository.py
"""Report Repository"""

from .base_repository import BaseRepository
from infrastructure.database import Report


class ReportRepository(BaseRepository):
    """Repository for Report model"""
    
    def __init__(self):
        super().__init__(Report)
    
    def get_by_report_uid(self, report_uid):
        """Get report by UID"""
        return self.model.query.filter_by(report_uid=report_uid).first()
    
    def get_by_patient_uid(self, patient_uid):
        """Get all reports for a patient by UID"""
        return self.model.query.filter_by(patient_uid=patient_uid).all()
    
    def get_by_template_id(self, template_id):
        """Get all reports for a template"""
        return self.model.query.filter_by(template_id=template_id).all()
    
    def get_recent(self, limit=10):
        """Get recent reports"""
        return self.model.query.order_by(
            self.model.created_at.desc()
        ).limit(limit).all()
    
    def get_with_template(self, report_id):
        """Get report with template data (join)"""
        from infrastructure.database import Template
        return self.model.query.join(Template).filter(
            self.model.id == report_id
        ).first()
    
    def get_pdf_count(self):
        """Count reports with PDF files"""
        return self.model.query.filter(
            self.model.pdf_path.isnot(None)
        ).count()