# business/services/report_pdf_service.py
"""PDF Generation Service - Arabic RTL PDF Builder"""

import os
import base64
from fpdf import FPDF
from business.config.pdf_config import PDFConfig
import arabic_reshaper
from bidi.algorithm import get_display


class ArabicPDF(FPDF):
    """Custom FPDF with Arabic RTL support"""
    
    def __init__(self):
        super().__init__(PDFConfig.PAGE_ORIENTATION, PDFConfig.PAGE_UNIT, PDFConfig.PAGE_FORMAT)
        self.arabic_font = PDFConfig.FONT_FALLBACK
        
        for path in PDFConfig.FONT_PATHS:
            if os.path.exists(path):
                self.add_font(PDFConfig.FONT_FAMILY, '', path, uni=True)
                self.add_font(PDFConfig.FONT_FAMILY, 'B', path, uni=True)
                self.arabic_font = PDFConfig.FONT_FAMILY
                break
    
    def reshape(self, text):
        """Reshape Arabic text for proper display"""
        if not text:
            return ''
        return get_display(arabic_reshaper.reshape(str(text)))
    
    def draw_rtl_row(self, x, y, label, value, label_width, value_width,
                     label_size=None, value_size=None, row_height=None, bg_color=None):
        """Draw RTL row: Label RIGHT, Value LEFT"""
        if label_size is None: label_size = PDFConfig.LABEL_FONT_SIZE
        if value_size is None: value_size = PDFConfig.VALUE_FONT_SIZE
        if row_height is None: row_height = PDFConfig.ROW_HEIGHT
        
        page_w = self.w - 2 * self.l_margin
        
        if bg_color:
            self.set_fill_color(*bg_color)
            self.rect(x, y, page_w, row_height, 'F')
        
        # Label (Right side)
        label_text = self.reshape(label)
        self.set_font(self.arabic_font, 'B', label_size)
        self.set_text_color(*PDFConfig.LABEL_COLOR)
        label_x = x + page_w - label_width - 2
        self.set_xy(label_x, y + 1)
        self.cell(label_width, row_height - 2, label_text, align='R')
        
        # Value (Left side)
        value_text = self.reshape(str(value) if value else PDFConfig.NOT_AVAILABLE)
        self.set_font(self.arabic_font, '', value_size)
        self.set_text_color(*PDFConfig.VALUE_COLOR)
        value_x = x + 2
        self.set_xy(value_x, y + 1)
        self.cell(value_width - 2, row_height - 2, value_text, align='L')
        
        # Separator
        self.set_draw_color(*PDFConfig.SEPARATOR_COLOR)
        self.line(x, y + row_height, x + page_w, y + row_height)
        
        return y + row_height
    
    def draw_section_header(self, x, y, title, page_w):
        """Draw colored section header"""
        self.set_fill_color(*PDFConfig.SECTION_BG_COLOR)
        self.set_draw_color(*PDFConfig.SECTION_BG_COLOR)
        self.rect(x, y, page_w, PDFConfig.SECTION_HEADER_HEIGHT, 'DF')
        
        clean_title = self._replace_emoji(title)
        title_text = self.reshape(f"{PDFConfig.SECTION_PREFIX}{clean_title}")
        self.set_font(self.arabic_font, 'B', PDFConfig.SECTION_FONT_SIZE)
        self.set_text_color(*PDFConfig.SECTION_TEXT_COLOR)
        self.set_xy(x + 3, y + 1)
        self.cell(page_w - 6, 8, title_text, align='R')
        
        return y + PDFConfig.SECTION_HEADER_HEIGHT + 4
    
    def _replace_emoji(self, text):
        """Replace emojis with text equivalents"""
        result = text
        for emoji, replacement in PDFConfig.EMOJI_REPLACEMENTS.items():
            result = result.replace(emoji, replacement)
        return ''.join(c for c in result if ord(c) < 65536)


class ReportPDFService:
    """Handles PDF generation for medical reports"""
    
    def __init__(self, reports_folder):
        self.reports_folder = reports_folder
        os.makedirs(reports_folder, exist_ok=True)
    
    def generate_pdf(self, report, template):
        """
        Generate PDF for a report.
        
        Args:
            report: Report model instance
            template: Template model instance
            
        Returns:
            tuple: (pdf_path, pdf_filename) or (None, None)
        """
        try:
            structure = template.get_structure()
            report_data = report.get_data()
            
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_filename = f'report_{report.report_uid}_{timestamp}.pdf'
            pdf_path = os.path.join(self.reports_folder, pdf_filename)
            
            self._build_rtl_pdf(pdf_path, template.title, structure, report_data, report)
            
            print(f"✅ PDF generated: {pdf_path}")
            return pdf_path, pdf_filename
            
        except Exception as e:
            print(f"❌ PDF error: {e}")
            import traceback
            traceback.print_exc()
            return None, None
    
    def _build_rtl_pdf(self, pdf_path, title, structure, data, report):
        """Build complete RTL PDF document"""
        pdf = ArabicPDF()
        pdf.set_auto_page_break(PDFConfig.AUTO_PAGE_BREAK, PDFConfig.PAGE_BREAK_MARGIN)
        pdf.add_page()
        
        margin = PDFConfig.MARGIN
        page_w = pdf.w - 2 * margin
        label_w = PDFConfig.LABEL_WIDTH
        value_w = page_w - label_w - PDFConfig.VALUE_WIDTH_OFFSET
        y = 15
        
        # ═══ Header ═══
        y = self._draw_header(pdf, margin, page_w, y, title, report)
        
        # ═══ Content ═══
        y = self._draw_content(pdf, margin, page_w, label_w, value_w, y, structure, data, report)
        
        # ═══ Footer ═══
        self._draw_footer(pdf, margin, page_w, y, report)
        
        pdf.output(pdf_path)
    
    def _draw_header(self, pdf, margin, page_w, y, title, report):
        """Draw PDF header: app name, title, meta box"""
        pdf.set_font(pdf.arabic_font, 'B', PDFConfig.HEADER_FONT_SIZE)
        pdf.set_text_color(*PDFConfig.PRIMARY_COLOR)
        pdf.set_xy(margin, y)
        pdf.cell(page_w, 12, pdf.reshape(PDFConfig.APP_NAME), align='C')
        y += 12
        
        pdf.set_font(pdf.arabic_font, 'B', PDFConfig.TITLE_FONT_SIZE)
        pdf.set_text_color(*PDFConfig.SECONDARY_COLOR)
        pdf.set_xy(margin, y)
        pdf.cell(page_w, 10, pdf.reshape(pdf._replace_emoji(title)), align='C')
        y += 12
        
        # Meta box
        pdf.set_fill_color(*PDFConfig.META_BG_COLOR)
        pdf.set_draw_color(*PDFConfig.PRIMARY_COLOR)
        pdf.rect(margin, y, page_w, 10, 'DF')
        meta = pdf.reshape(
            f"{PDFConfig.REPORT_PREFIX}{report.report_uid}  |  "
            f"{PDFConfig.PATIENT_PREFIX}{report.patient_uid or PDFConfig.PATIENT_UNKNOWN}  |  "
            f"{PDFConfig.DATE_PREFIX}{report.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
        pdf.set_font(pdf.arabic_font, '', PDFConfig.META_FONT_SIZE)
        pdf.set_text_color(*PDFConfig.META_TEXT_COLOR)
        pdf.set_xy(margin, y + 2)
        pdf.cell(page_w, 6, meta, align='C')
        
        return y + 16
    
    def _draw_content(self, pdf, margin, page_w, label_w, value_w, y, structure, data, report):
        """Draw all content fields"""
        row_bg = False
        
        for field in structure:
            field_type = field.get('type', 'text')
            field_label = field.get('label', '')
            field_name = field.get('name', '')
            
            if y > 255:
                pdf.add_page()
                y = 15
            
            if field_type == 'heading':
                y = pdf.draw_section_header(margin, y, field_label, page_w)
                row_bg = False
                
            elif field_type == 'divider':
                pdf.set_draw_color(*PDFConfig.DIVIDER_COLOR)
                pdf.line(margin + 30, y + 3, margin + page_w - 30, y + 3)
                y += 8
                
            elif field_type == 'subheading':
                pdf.set_font(pdf.arabic_font, 'B', PDFConfig.SECTION_FONT_SIZE)
                pdf.set_text_color(*PDFConfig.SECONDARY_COLOR)
                pdf.set_xy(margin, y)
                pdf.cell(page_w, 8, pdf.reshape(field_label), align='R')
                y += 10
                
            elif field_type == 'signature':
                y = self._draw_signature(pdf, margin, page_w, label_w, value_w, y, 
                                        field_label, field_name, data, report)
                
            else:
                y = self._draw_form_field(pdf, margin, label_w, value_w, y,
                                         field_type, field_label, field_name, data, row_bg)
                row_bg = not row_bg
        
        return y
    
    def _draw_signature(self, pdf, margin, page_w, label_w, value_w, y, 
                       field_label, field_name, data, report):
        """Draw signature field (image or placeholder line)"""
        # Label
        pdf.set_font(pdf.arabic_font, 'B', PDFConfig.LABEL_FONT_SIZE)
        pdf.set_text_color(*PDFConfig.LABEL_COLOR)
        pdf.set_xy(margin + page_w - label_w - 2, y + 1)
        pdf.cell(label_w, 8, pdf.reshape(field_label), align='R')
        
        signature_data = data.get(field_name, '')
        
        if signature_data and isinstance(signature_data, str) and signature_data.startswith('data:image'):
            try:
                image_bytes = base64.b64decode(signature_data.split(',')[1])
                temp_img = os.path.join(self.reports_folder, f'temp_sig_{report.id}.png')
                with open(temp_img, 'wb') as f:
                    f.write(image_bytes)
                pdf.image(temp_img, x=margin+2, y=y, 
                         w=PDFConfig.SIGNATURE_IMAGE_WIDTH, h=PDFConfig.SIGNATURE_IMAGE_HEIGHT)
                try: os.remove(temp_img)
                except: pass
                y += PDFConfig.SIGNATURE_IMAGE_HEIGHT + 5
            except Exception:
                y = self._draw_signature_placeholder(pdf, margin, value_w, y)
        else:
            y = self._draw_signature_placeholder(pdf, margin, value_w, y)
        
        return y
    
    def _draw_signature_placeholder(self, pdf, margin, value_w, y):
        """Draw empty signature line"""
        y += 2
        pdf.set_draw_color(*PDFConfig.SIGNATURE_LINE_COLOR)
        pdf.line(margin + 2, y + 4, margin + value_w, y + 4)
        pdf.set_font(pdf.arabic_font, '', PDFConfig.SIGNATURE_FONT_SIZE)
        pdf.set_text_color(*PDFConfig.SIGNATURE_TEXT_COLOR)
        pdf.set_xy(margin + 2, y + 6)
        pdf.cell(value_w, 6, pdf.reshape(PDFConfig.SIGNATURE_PLACEHOLDER), align='L')
        return y + 15
    
    def _draw_form_field(self, pdf, margin, label_w, value_w, y,
                        field_type, field_label, field_name, data, row_bg):
        """Draw a regular form field"""
        raw_value = data.get(field_name, '')
        
        # Format value
        if field_type == 'checkbox':
            display_value = PDFConfig.CHECKBOX_YES if raw_value else PDFConfig.CHECKBOX_NO
        elif isinstance(raw_value, bool):
            display_value = PDFConfig.CHECKBOX_YES if raw_value else PDFConfig.CHECKBOX_NO
        elif raw_value == '' or raw_value is None:
            display_value = PDFConfig.NOT_AVAILABLE
        else:
            display_value = str(raw_value)
        
        bg = PDFConfig.ROW_BG_COLOR if row_bg else None
        return pdf.draw_rtl_row(margin, y, field_label, display_value, 
                               label_w, value_w, bg_color=bg)
    
    def _draw_footer(self, pdf, margin, page_w, y, report):
        """Draw PDF footer"""
        y += 10
        if y > 260:
            pdf.add_page()
            y = 20
        
        pdf.set_draw_color(*PDFConfig.FOOTER_LINE_COLOR)
        pdf.line(margin, y, margin + page_w, y)
        footer = pdf.reshape(
            f"{PDFConfig.FOOTER_TEXT} | {report.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
        pdf.set_font(pdf.arabic_font, '', PDFConfig.FOOTER_FONT_SIZE)
        pdf.set_text_color(*PDFConfig.FOOTER_TEXT_COLOR)
        pdf.set_xy(margin, y + 3)
        pdf.cell(page_w, 6, footer, align='C')