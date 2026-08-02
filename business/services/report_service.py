
# business/services/report_service.py

# business/services/report_service.py
"""Report Service - Report CRUD + PDF Generation"""

import json
import os
from datetime import datetime
from infrastructure.database import db, Template, Report, generate_id
from business.services.report_template_service import ReportTemplateService
from business.services.report_pdf_service import ReportPDFService


class ReportService:
    """
    Main Report Service - Combines Template CRUD, Report CRUD, and PDF Generation.
    Uses ReportTemplateService and ReportPDFService internally.
    """
    
    def __init__(self, reports_folder):
        self.reports_folder = reports_folder
        os.makedirs(reports_folder, exist_ok=True)
        
        # Sub-services
        self.template_service = ReportTemplateService()
        self.pdf_service = ReportPDFService(reports_folder)
    
    # ═══════════════════════════════════════════════
    # Template CRUD (delegated)
    # ═══════════════════════════════════════════════
    def create_template(self, title, structure, description=None, category='general'):
        return self.template_service.create_template(title, structure, description, category)
    
    def get_all_templates(self, category=None):
        return self.template_service.get_all_templates(category)
    
    def get_template(self, template_id):
        return self.template_service.get_template(template_id)
    
    def update_template(self, template_id, title=None, structure=None, description=None):
        return self.template_service.update_template(template_id, title, structure, description)
    
    def delete_template(self, template_id):
        return self.template_service.delete_template(template_id)
    
    def get_template_reports(self, template_id):
        return self.template_service.get_template_reports(template_id)
    
    def get_default_field_types(self):
        return self.template_service.get_default_field_types()
    
    # ═══════════════════════════════════════════════
    # Report CRUD
    # ═══════════════════════════════════════════════
    def create_report(self, template_id, form_data, patient_uid=None):
        """Create a new report from template"""
        try:
            template = Template.query.get(template_id)
            if not template:
                return {'success': False, 'error': 'Template not found'}
            
            if not patient_uid:
                patient_uid = generate_id('PAT-')
            
            report = Report(
                report_uid=generate_id('REP-'),
                template_id=template_id,
                patient_uid=patient_uid,
                data_json=json.dumps(form_data, ensure_ascii=False)
            )
            db.session.add(report)
            db.session.commit()
            
            print(f"✅ Report created: {report.report_uid} | Patient: {report.patient_uid}")
            return {'success': True, 'report': report.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_report(self, report_id):
        """Get a single report by ID"""
        report = Report.query.get(report_id)
        return {'success': True, 'report': report.to_dict()} if report else {'success': False}
    
    def update_report(self, report_id, form_data=None, patient_uid=None):
        """Update an existing report"""
        try:
            report = Report.query.get(report_id)
            if not report:
                return {'success': False, 'error': 'Report not found'}
            
            if form_data is not None:
                report.data_json = json.dumps(form_data, ensure_ascii=False)
            if patient_uid is not None:
                report.patient_uid = patient_uid
            
            report.updated_at = datetime.utcnow()
            db.session.commit()
            return {'success': True, 'report': report.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def delete_report(self, report_id):
        """Delete a single report and its PDF file"""
        try:
            report = Report.query.get(report_id)
            if not report:
                return {'success': False, 'error': 'Report not found'}
            
            if report.pdf_path and os.path.exists(report.pdf_path):
                try: os.remove(report.pdf_path)
                except: pass
            
            db.session.delete(report)
            db.session.commit()
            return {'success': True, 'message': f'Report {report.report_uid} deleted'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    # ═══════════════════════════════════════════════
    # PDF Generation (delegated)
    # ═══════════════════════════════════════════════
    def generate_pdf(self, report_id):
        """Generate PDF for a report"""
        try:
            report = Report.query.get(report_id)
            if not report:
                return {'success': False, 'error': 'Report not found'}
            
            template = Template.query.get(report.template_id)
            if not template:
                return {'success': False, 'error': 'Template not found'}
            
            pdf_path, pdf_filename = self.pdf_service.generate_pdf(report, template)
            
            if pdf_path:
                report.pdf_path = pdf_path
                report.updated_at = datetime.now()
                
                db.session.commit()
                return {'success': True, 'pdf_path': pdf_path, 'pdf_filename': pdf_filename}
            
            return {'success': False, 'error': 'PDF generation failed'}
            
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
        

































































#         # """Report Service - Professional Arabic PDF with RTL Layout"""

# import json
# import os
# from datetime import datetime
# from fpdf import FPDF
# from infrastructure.database import db, Template, Report, generate_id
# from business.config.pdf_config import PDFConfig
# import arabic_reshaper
# from bidi.algorithm import get_display
# from business.config.field_types import FieldTypes

# class ArabicPDF(FPDF):
#     """Custom FPDF with Arabic RTL support"""
    
#     def __init__(self):
#         super().__init__(PDFConfig.PAGE_ORIENTATION, PDFConfig.PAGE_UNIT, PDFConfig.PAGE_FORMAT)
#         self.arabic_font = PDFConfig.FONT_FALLBACK
        
#         for path in PDFConfig.FONT_PATHS:
#             if os.path.exists(path):
#                 self.add_font(PDFConfig.FONT_FAMILY, '', path, uni=True)
#                 self.add_font(PDFConfig.FONT_FAMILY, 'B', path, uni=True)
#                 self.arabic_font = PDFConfig.FONT_FAMILY
#                 break
    
#     def reshape(self, text):
#         if not text: return ''
#         return get_display(arabic_reshaper.reshape(str(text)))
    
#     def draw_rtl_row(self, x, y, label, value, label_width, value_width,
#                      label_size=None, value_size=None, row_height=None, bg_color=None):
#         if label_size is None: label_size = PDFConfig.LABEL_FONT_SIZE
#         if value_size is None: value_size = PDFConfig.VALUE_FONT_SIZE
#         if row_height is None: row_height = PDFConfig.ROW_HEIGHT
        
#         page_w = self.w - 2 * self.l_margin
        
#         if bg_color:
#             self.set_fill_color(*bg_color)
#             self.rect(x, y, page_w, row_height, 'F')
        
#         label_text = self.reshape(label)
#         self.set_font(self.arabic_font, 'B', label_size)
#         self.set_text_color(*PDFConfig.LABEL_COLOR)
#         label_x = x + page_w - label_width - 2
#         self.set_xy(label_x, y + 1)
#         self.cell(label_width, row_height - 2, label_text, align='R')
        
#         value_text = self.reshape(str(value) if value else PDFConfig.NOT_AVAILABLE)
#         self.set_font(self.arabic_font, '', value_size)
#         self.set_text_color(*PDFConfig.VALUE_COLOR)
#         value_x = x + 2
#         self.set_xy(value_x, y + 1)
#         self.cell(value_width - 2, row_height - 2, value_text, align='L')
        
#         self.set_draw_color(*PDFConfig.SEPARATOR_COLOR)
#         self.line(x, y + row_height, x + page_w, y + row_height)
        
#         return y + row_height
    
#     def draw_section_header(self, x, y, title, page_w):
#         self.set_fill_color(*PDFConfig.SECTION_BG_COLOR)
#         self.set_draw_color(*PDFConfig.SECTION_BG_COLOR)
#         self.rect(x, y, page_w, PDFConfig.SECTION_HEADER_HEIGHT, 'DF')
        
#         clean_title = self._replace_emoji(title)
#         title_text = self.reshape(f"{PDFConfig.SECTION_PREFIX}{clean_title}")
#         self.set_font(self.arabic_font, 'B', PDFConfig.SECTION_FONT_SIZE)
#         self.set_text_color(*PDFConfig.SECTION_TEXT_COLOR)
#         self.set_xy(x + 3, y + 1)
#         self.cell(page_w - 6, 8, title_text, align='R')
        
#         return y + PDFConfig.SECTION_HEADER_HEIGHT + 4
    
#     def _replace_emoji(self, text):
#         result = text
#         for emoji, replacement in PDFConfig.EMOJI_REPLACEMENTS.items():
#             result = result.replace(emoji, replacement)
#         return ''.join(c for c in result if ord(c) < 65536)


# class ReportService:
#     """Handles report template CRUD and PDF generation (Single Doctor System)"""
    
#     def __init__(self, reports_folder):
#         self.reports_folder = reports_folder
#         os.makedirs(reports_folder, exist_ok=True)
    
#     # ═══════════════════════════════════════════════
#     # Template CRUD
#     # ═══════════════════════════════════════════════
    
#     def create_template(self, title, structure, description=None, category='general'):
#         try:
#             template = Template(title=title, description=description,
#                               structure_json=json.dumps(structure, ensure_ascii=False),
#                               category=category)
#             db.session.add(template); db.session.commit()
#             return {'success': True, 'template': template.to_dict()}
#         except Exception as e:
#             db.session.rollback(); return {'success': False, 'error': str(e)}
    
#     def get_all_templates(self, category=None):
#         query = Template.query.filter_by(is_active=True)
#         if category: query = query.filter_by(category=category)
#         return [t.to_dict() for t in query.order_by(Template.created_at.desc()).all()]
    
#     def get_template(self, template_id):
#         template = Template.query.get(template_id)
#         if template:
#             data = template.to_dict()
#             data['reports'] = [r.to_dict() for r in template.reports]
#             return {'success': True, 'template': data}
#         return {'success': False, 'error': 'Template not found'}
    
#     def update_template(self, template_id, title=None, structure=None, description=None):
#         try:
#             template = Template.query.get(template_id)
#             if not template: return {'success': False, 'error': 'Not found'}
#             if title is not None: template.title = title
#             if description is not None: template.description = description
#             if structure is not None: template.structure_json = json.dumps(structure, ensure_ascii=False)
#             template.updated_at = datetime.utcnow()
#             db.session.commit()
#             return {'success': True, 'template': template.to_dict()}
#         except Exception as e:
#             db.session.rollback(); return {'success': False, 'error': str(e)}
    
#     def delete_template(self, template_id):
#         try:
#             template = Template.query.get(template_id)
#             if not template: return {'success': False, 'error': 'Not found'}
#             for report in template.reports:
#                 if report.pdf_path and os.path.exists(report.pdf_path):
#                     try: os.remove(report.pdf_path)
#                     except: pass
#             db.session.delete(template); db.session.commit()
#             return {'success': True, 'message': 'Deleted'}
#         except Exception as e:
#             db.session.rollback(); return {'success': False, 'error': str(e)}
    
#     # ═══════════════════════════════════════════════
#     # Report CRUD
#     # ═══════════════════════════════════════════════
    
#     def create_report(self, template_id, form_data, patient_uid=None):
#         try:
#             template = Template.query.get(template_id)
#             if not template: return {'success': False, 'error': 'Template not found'}
#             if not patient_uid: patient_uid = generate_id('PAT-')
#             report = Report(report_uid=generate_id('REP-'), template_id=template_id,
#                           patient_uid=patient_uid,
#                           data_json=json.dumps(form_data, ensure_ascii=False))
#             db.session.add(report); db.session.commit()
#             return {'success': True, 'report': report.to_dict()}
#         except Exception as e:
#             db.session.rollback(); return {'success': False, 'error': str(e)}
    
#     def get_report(self, report_id):
#         report = Report.query.get(report_id)
#         return {'success': True, 'report': report.to_dict()} if report else {'success': False}
    
#     def get_template_reports(self, template_id):
#         template = Template.query.get(template_id)
#         if not template: return {'success': False, 'error': 'Template not found'}
#         reports = Report.query.filter_by(template_id=template_id)\
#                     .order_by(Report.created_at.desc()).all()
#         return {'success': True, 'template': template.to_dict(), 'reports': [r.to_dict() for r in reports]}
    
#     def update_report(self, report_id, form_data=None, patient_uid=None):
#         try:
#             report = Report.query.get(report_id)
#             if not report: return {'success': False, 'error': 'Report not found'}
#             if form_data is not None: report.data_json = json.dumps(form_data, ensure_ascii=False)
#             if patient_uid is not None: report.patient_uid = patient_uid
#             report.updated_at = datetime.utcnow()
#             db.session.commit()
#             return {'success': True, 'report': report.to_dict()}
#         except Exception as e:
#             db.session.rollback(); return {'success': False, 'error': str(e)}
    
#     def delete_report(self, report_id):
#         try:
#             report = Report.query.get(report_id)
#             if not report: return {'success': False, 'error': 'Report not found'}
#             if report.pdf_path and os.path.exists(report.pdf_path):
#                 try: os.remove(report.pdf_path)
#                 except: pass
#             db.session.delete(report); db.session.commit()
#             return {'success': True, 'message': f'Report {report.report_uid} deleted'}
#         except Exception as e:
#             db.session.rollback(); return {'success': False, 'error': str(e)}
    
#     def get_default_field_types(self):
#         """Return available field types for template builder"""
#         return FieldTypes.get_all()
    
#     # ═══════════════════════════════════════════════
#     # PDF Generation
#     # ═══════════════════════════════════════════════
    
#     def generate_pdf(self, report_id):
#         try:
#             report = Report.query.get(report_id)
#             if not report: return {'success': False, 'error': 'Report not found'}
#             template = Template.query.get(report.template_id)
#             if not template: return {'success': False, 'error': 'Template not found'}
            
#             structure = template.get_structure()
#             report_data = report.get_data()
            
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             pdf_filename = f'report_{report.report_uid}_{timestamp}.pdf'
#             pdf_path = os.path.join(self.reports_folder, pdf_filename)
            
#             self._build_rtl_pdf(pdf_path, template.title, structure, report_data, report)
            
#             report.pdf_path = pdf_path
#             report.updated_at = datetime.utcnow()
#             db.session.commit()
#             return {'success': True, 'pdf_path': pdf_path, 'pdf_filename': pdf_filename}
#         except Exception as e:
#             db.session.rollback()
#             import traceback; traceback.print_exc()
#             return {'success': False, 'error': str(e)}
    
#     def _build_rtl_pdf(self, pdf_path, title, structure, data, report):
#         pdf = ArabicPDF()
#         pdf.set_auto_page_break(PDFConfig.AUTO_PAGE_BREAK, PDFConfig.PAGE_BREAK_MARGIN)
#         pdf.add_page()
        
#         margin = PDFConfig.MARGIN
#         page_w = pdf.w - 2 * margin
#         label_w = PDFConfig.LABEL_WIDTH
#         value_w = page_w - label_w - PDFConfig.VALUE_WIDTH_OFFSET
#         y = 15
        
#         # ═══ Header ═══
#         pdf.set_font(pdf.arabic_font, 'B', PDFConfig.HEADER_FONT_SIZE)
#         pdf.set_text_color(*PDFConfig.PRIMARY_COLOR)
#         pdf.set_xy(margin, y)
#         pdf.cell(page_w, 12, pdf.reshape(PDFConfig.APP_NAME), align='C')
#         y += 12
        
#         pdf.set_font(pdf.arabic_font, 'B', PDFConfig.TITLE_FONT_SIZE)
#         pdf.set_text_color(*PDFConfig.SECONDARY_COLOR)
#         pdf.set_xy(margin, y)
#         pdf.cell(page_w, 10, pdf.reshape(pdf._replace_emoji(title)), align='C')
#         y += 12
        
#         # Meta box
#         pdf.set_fill_color(*PDFConfig.META_BG_COLOR)
#         pdf.set_draw_color(*PDFConfig.PRIMARY_COLOR)
#         pdf.rect(margin, y, page_w, 10, 'DF')
#         meta = pdf.reshape(f"{PDFConfig.REPORT_PREFIX}{report.report_uid}  |  {PDFConfig.PATIENT_PREFIX}{report.patient_uid or PDFConfig.PATIENT_UNKNOWN}  |  {PDFConfig.DATE_PREFIX}{report.created_at.strftime('%Y-%m-%d %H:%M')}")
#         pdf.set_font(pdf.arabic_font, '', PDFConfig.META_FONT_SIZE)
#         pdf.set_text_color(*PDFConfig.META_TEXT_COLOR)
#         pdf.set_xy(margin, y + 2)
#         pdf.cell(page_w, 6, meta, align='C')
#         y += 16
        
#         # ═══ Content ═══
#         row_bg = False
#         for field in structure:
#             field_type = field.get('type', 'text')
#             field_label = field.get('label', '')
#             field_name = field.get('name', '')
            
#             if y > 255: pdf.add_page(); y = 15
            
#             if field_type == 'heading':
#                 y = pdf.draw_section_header(margin, y, field_label, page_w)
#                 row_bg = False
#             elif field_type == 'divider':
#                 pdf.set_draw_color(*PDFConfig.DIVIDER_COLOR)
#                 pdf.line(margin + 30, y + 3, margin + page_w - 30, y + 3)
#                 y += 8
#             elif field_type == 'subheading':
#                 pdf.set_font(pdf.arabic_font, 'B', PDFConfig.SECTION_FONT_SIZE)
#                 pdf.set_text_color(*PDFConfig.SECONDARY_COLOR)
#                 pdf.set_xy(margin, y)
#                 pdf.cell(page_w, 8, pdf.reshape(field_label), align='R')
#                 y += 10
#             elif field_type == 'signature':
#                 pdf.set_font(pdf.arabic_font, 'B', PDFConfig.LABEL_FONT_SIZE)
#                 pdf.set_text_color(*PDFConfig.LABEL_COLOR)
#                 pdf.set_xy(margin + page_w - label_w - 2, y + 1)
#                 pdf.cell(label_w, 8, pdf.reshape(field_label), align='R')
                
#                 signature_data = data.get(field_name, '')
#                 if signature_data and isinstance(signature_data, str) and signature_data.startswith('data:image'):
#                     try:
#                         import base64
#                         image_bytes = base64.b64decode(signature_data.split(',')[1])
#                         temp_img = os.path.join(self.reports_folder, f'temp_sig_{report.id}.png')
#                         with open(temp_img, 'wb') as f: f.write(image_bytes)
#                         pdf.image(temp_img, x=margin+2, y=y, w=PDFConfig.SIGNATURE_IMAGE_WIDTH, h=PDFConfig.SIGNATURE_IMAGE_HEIGHT)
#                         try: os.remove(temp_img)
#                         except: pass
#                         y += PDFConfig.SIGNATURE_IMAGE_HEIGHT + 5
#                     except Exception:
#                         y += 2
#                         pdf.set_draw_color(*PDFConfig.SIGNATURE_LINE_COLOR)
#                         pdf.line(margin+2, y+4, margin+value_w, y+4)
#                         pdf.set_font(pdf.arabic_font, '', PDFConfig.SIGNATURE_FONT_SIZE)
#                         pdf.set_text_color(*PDFConfig.SIGNATURE_TEXT_COLOR)
#                         pdf.set_xy(margin+2, y+6)
#                         pdf.cell(value_w, 6, pdf.reshape(PDFConfig.SIGNATURE_PLACEHOLDER), align='L')
#                         y += 15
#                 else:
#                     y += 2
#                     pdf.set_draw_color(*PDFConfig.SIGNATURE_LINE_COLOR)
#                     pdf.line(margin+2, y+4, margin+value_w, y+4)
#                     pdf.set_font(pdf.arabic_font, '', PDFConfig.SIGNATURE_FONT_SIZE)
#                     pdf.set_text_color(*PDFConfig.SIGNATURE_TEXT_COLOR)
#                     pdf.set_xy(margin+2, y+6)
#                     pdf.cell(value_w, 6, pdf.reshape(PDFConfig.SIGNATURE_PLACEHOLDER), align='L')
#                     y += 15
#             else:
#                 raw_value = data.get(field_name, '')
#                 if field_type == 'checkbox':
#                     display_value = PDFConfig.CHECKBOX_YES if raw_value else PDFConfig.CHECKBOX_NO
#                 elif isinstance(raw_value, bool):
#                     display_value = PDFConfig.CHECKBOX_YES if raw_value else PDFConfig.CHECKBOX_NO
#                 elif raw_value == '' or raw_value is None:
#                     display_value = PDFConfig.NOT_AVAILABLE
#                 else:
#                     display_value = str(raw_value)
                
#                 bg = PDFConfig.ROW_BG_COLOR if row_bg else None
#                 row_bg = not row_bg
#                 y = pdf.draw_rtl_row(margin, y, field_label, display_value, label_w, value_w, bg_color=bg)
        
#         # ═══ Footer ═══
#         y += 10
#         if y > 260: pdf.add_page(); y = 20
#         pdf.set_draw_color(*PDFConfig.FOOTER_LINE_COLOR)
#         pdf.line(margin, y, margin + page_w, y)
#         footer = pdf.reshape(f"{PDFConfig.FOOTER_TEXT} | {report.created_at.strftime('%Y-%m-%d %H:%M')}")
#         pdf.set_font(pdf.arabic_font, '', PDFConfig.FOOTER_FONT_SIZE)
#         pdf.set_text_color(*PDFConfig.FOOTER_TEXT_COLOR)
#         pdf.set_xy(margin, y + 3)
#         pdf.cell(page_w, 6, footer, align='C')
        
#         pdf.output(pdf_path)