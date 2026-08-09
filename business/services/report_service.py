# business/services/report_service.py
"""Report Service - Report CRUD + PDF Generation with Repository + DTO"""

import json
import os
import logging
from datetime import datetime

from infrastructure.database import db, Template, Report, generate_id
from infrastructure.repositories import TemplateRepository, ReportRepository
from application.dtos import TemplateDTO, ReportDTO
from business.services.report_template_service import ReportTemplateService
from business.services.report_pdf_service import ReportPDFService
from application.exceptions import (
    TemplateNotFoundError,
    ReportNotFoundError,
    DatabaseError,
    PDFGenerationError
)

logger = logging.getLogger(__name__)


class ReportService:
   
    
    def __init__(self, reports_folder):
        self.reports_folder = reports_folder
        os.makedirs(reports_folder, exist_ok=True)
        
        self.template_repo = TemplateRepository()
        self.report_repo = ReportRepository()
        
        self.template_service = ReportTemplateService()
        self.pdf_service = ReportPDFService(reports_folder)
    
    # ═══════════════════════════════════════════════
    # Template CRUD
    # ═══════════════════════════════════════════════
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
            saved = self.template_repo.save(template)
            logger.info(f" Template created: {saved.title} (ID: {saved.id})")
            return {'success': True, 'template': TemplateDTO.from_model(saved).to_dict()}
        except Exception as e:
            logger.error(f"Failed to create template: {e}")
            raise DatabaseError(f"فشل إنشاء القالب: {str(e)}")
    
    def get_all_templates(self, category=None):
        """Get all templates with optional category filter"""
        try:
            if category:
                templates = self.template_repo.get_by_category(category)
            else:
                templates = self.template_repo.get_all()
            return [TemplateDTO.from_model(t).to_dict() for t in templates]
        except Exception as e:
            logger.error(f"Failed to get templates: {e}")
            return []
    
    def get_template(self, template_id):
        """Get a single template by ID"""
        template = self.template_repo.get_by_id(template_id)
        if not template:
            raise TemplateNotFoundError(template_id)
        return {'success': True, 'template': TemplateDTO.from_model(template).to_dict()}
    
    def update_template(self, template_id, title=None, structure=None, description=None):
        """Update an existing template"""
        try:
            template = self.template_repo.get_by_id(template_id)
            if not template:
                raise TemplateNotFoundError(template_id)
            
            if title:
                template.title = title
            if structure is not None:
                template.structure_json = json.dumps(structure, ensure_ascii=False)
            if description is not None:
                template.description = description
            
            updated = self.template_repo.save(template)
            logger.info(f"✅ Template updated: {updated.title} (ID: {updated.id})")
            return {'success': True, 'template': TemplateDTO.from_model(updated).to_dict()}
        except Exception as e:
            logger.error(f"Failed to update template: {e}")
            raise DatabaseError(f"فشل تحديث القالب: {str(e)}")
    
    def delete_template(self, template_id):
        """Delete a template"""
        try:
            template = self.template_repo.get_by_id(template_id)
            if not template:
                raise TemplateNotFoundError(template_id)
            
            # التحقق من وجود تقارير مرتبطة
            reports_count = len(self.report_repo.get_by_template_id(template_id))
            if reports_count > 0:
                logger.warning(f"Deleting template {template_id} with {reports_count} reports")
            
            self.template_repo.delete(template)
            logger.info(f"🗑️ Template deleted: {template.title} (ID: {template.id})")
            return {'success': True, 'message': f'Template {template_id} deleted'}
        except Exception as e:
            logger.error(f"Failed to delete template: {e}")
            raise DatabaseError(f"فشل حذف القالب: {str(e)}")
    
    def get_template_reports(self, template_id):
        """Get all reports for a template"""
        try:
            reports = self.report_repo.get_by_template_id(template_id)
            return [ReportDTO.from_model(r).to_dict() for r in reports]
        except Exception as e:
            logger.error(f"Failed to get template reports: {e}")
            return []
    
    def get_default_field_types(self):
        """Get default field types for template builder"""
        return self.template_service.get_default_field_types()
    
    # ═══════════════════════════════════════════════
    # Report CRUD
    # ═══════════════════════════════════════════════
    def create_report(self, template_id, form_data, patient_uid=None):
        """Create a new report from template"""
        try:
            template = self.template_repo.get_by_id(template_id)
            if not template:
                raise TemplateNotFoundError(template_id)
            
            if not patient_uid:
                patient_uid = generate_id('PAT-')
            
            report = Report(
                report_uid=generate_id('REP-'),
                template_id=template_id,
                patient_uid=patient_uid,
                data_json=json.dumps(form_data, ensure_ascii=False)
            )
            saved = self.report_repo.save(report)
            
            logger.info(f"✅ Report created: {saved.report_uid} | Patient: {saved.patient_uid}")
            return {'success': True, 'report': ReportDTO.from_model(saved).to_dict()}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create report: {e}")
            raise DatabaseError(f"فشل إنشاء التقرير: {str(e)}")
    
    def get_report(self, report_id):
        """Get a single report by ID"""
        report = self.report_repo.get_by_id(report_id)
        if not report:
            raise ReportNotFoundError(report_id)
        return {'success': True, 'report': ReportDTO.from_model(report).to_dict()}
    
    def update_report(self, report_id, form_data=None, patient_uid=None):
        """Update an existing report"""
        try:
            report = self.report_repo.get_by_id(report_id)
            if not report:
                raise ReportNotFoundError(report_id)
            
            if form_data is not None:
                report.data_json = json.dumps(form_data, ensure_ascii=False)
            if patient_uid is not None:
                report.patient_uid = patient_uid
            
            report.updated_at = datetime.utcnow()
            updated = self.report_repo.save(report)
            logger.info(f"✅ Report updated: {updated.report_uid}")
            return {'success': True, 'report': ReportDTO.from_model(updated).to_dict()}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to update report: {e}")
            raise DatabaseError(f"فشل تحديث التقرير: {str(e)}")
    
    def delete_report(self, report_id):
        """Delete a report and its PDF file"""
        try:
            report = self.report_repo.get_by_id(report_id)
            if not report:
                raise ReportNotFoundError(report_id)
            
            #  حذف ملف PDF إذا كان موجوداً
            if report.pdf_path and os.path.exists(report.pdf_path):
                try:
                    os.remove(report.pdf_path)
                    logger.info(f"🗑️ Deleted PDF: {report.pdf_path}")
                except Exception as e:
                    logger.warning(f"Could not delete PDF: {e}")
            
            # ✅ حفظ معلومات التقرير قبل الحذف للتسجيل
            report_uid = report.report_uid
            
            self.report_repo.delete(report)
            logger.info(f"🗑️ Report deleted: {report_uid}")
            return {'success': True, 'message': f'Report {report_uid} deleted'}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete report: {e}")
            raise DatabaseError(f"فشل حذف التقرير: {str(e)}")
    
    # ═══════════════════════════════════════════════
    # PDF Generation
    # ═══════════════════════════════════════════════
    def generate_pdf(self, report_id):
        """Generate PDF for a report"""
        try:
            report = self.report_repo.get_by_id(report_id)
            if not report:
                raise ReportNotFoundError(report_id)
            
            #  التحقق من وجود قالب
            template = self.template_repo.get_by_id(report.template_id)
            if not template:
                raise TemplateNotFoundError(report.template_id)
            
            #  التحقق من وجود بيانات في التقرير
            if not report.data_json or report.data_json == '{}':
                logger.warning(f"Report {report_id} has empty data")
            
            pdf_path, pdf_filename = self.pdf_service.generate_pdf(report, template)
            
            if pdf_path:
                report.pdf_path = pdf_path
                report.updated_at = datetime.now()
                self.report_repo.save(report)
                logger.info(f"✅ PDF generated: {pdf_filename} for report {report.report_uid}")
                return {'success': True, 'pdf_path': pdf_path, 'pdf_filename': pdf_filename}
            
            raise PDFGenerationError("فشل توليد ملف PDF")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"PDF generation failed: {e}")
            raise PDFGenerationError(str(e))
    
    # ═══════════════════════════════════════════════
    #  Helper Methods
    # ═══════════════════════════════════════════════
    def get_reports_by_patient(self, patient_uid):
        """Get all reports for a specific patient UID"""
        try:
            if not patient_uid:
                return []
            reports = self.report_repo.get_by_patient_uid(patient_uid)
            return [ReportDTO.from_model(r).to_dict() for r in reports]
        except Exception as e:
            logger.error(f"Failed to get reports for patient {patient_uid}: {e}")
            return []
    
    def get_report_count(self):
        """Get total number of reports"""
        try:
            return self.report_repo.count()
        except Exception as e:
            logger.error(f"Failed to get report count: {e}")
            return 0
    
    def get_reports_summary(self):
        """Get summary of reports"""
        try:
            total = self.report_repo.count()
            #  الحصول على أحدث 5 تقارير
            recent = self.report_repo.get_all(limit=5)
            return {
                'total': total,
                'recent': [ReportDTO.from_model(r).to_dict() for r in recent]
            }
        except Exception as e:
            logger.error(f"Failed to get reports summary: {e}")
            return {'total': 0, 'recent': []}