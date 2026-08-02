# business/config/pdf_config.py
"""PDF Generation Configuration"""

class PDFConfig:
    """All PDF settings in one place - no hardcoded values"""
    
    # ═══════════════════════════════════════════════
    # Page Settings
    # ═══════════════════════════════════════════════
    PAGE_FORMAT = 'A4'
    PAGE_ORIENTATION = 'P'
    PAGE_UNIT = 'mm'
    AUTO_PAGE_BREAK = True
    PAGE_BREAK_MARGIN = 20
    MARGIN = 10
    
    # ═══════════════════════════════════════════════
    # Colors (RGB)
    # ═══════════════════════════════════════════════
    PRIMARY_COLOR = (26, 82, 118)
    SECONDARY_COLOR = (44, 62, 80)
    LABEL_COLOR = (80, 80, 80)
    VALUE_COLOR = (44, 62, 80)
    META_BG_COLOR = (234, 242, 248)
    META_TEXT_COLOR = (100, 100, 100)
    SECTION_BG_COLOR = (26, 82, 118)
    SECTION_TEXT_COLOR = (255, 255, 255)
    SEPARATOR_COLOR = (235, 235, 235)
    DIVIDER_COLOR = (200, 200, 200)
    ROW_BG_COLOR = (248, 249, 250)
    SIGNATURE_LINE_COLOR = (26, 82, 118)
    SIGNATURE_TEXT_COLOR = (127, 140, 141)
    FOOTER_LINE_COLOR = (26, 82, 118)
    FOOTER_TEXT_COLOR = (170, 170, 170)
    
    # ═══════════════════════════════════════════════
    # Fonts
    # ═══════════════════════════════════════════════
    FONT_PATHS = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/segoui.ttf",
    ]
    FONT_FAMILY = 'Arabic'
    FONT_FALLBACK = 'Helvetica'
    
    HEADER_FONT_SIZE = 22
    TITLE_FONT_SIZE = 16
    SECTION_FONT_SIZE = 13
    LABEL_FONT_SIZE = 11
    VALUE_FONT_SIZE = 11
    META_FONT_SIZE = 9
    SIGNATURE_FONT_SIZE = 10
    FOOTER_FONT_SIZE = 8
    
    # ═══════════════════════════════════════════════
    # Layout
    # ═══════════════════════════════════════════════
    LABEL_WIDTH = 55
    VALUE_WIDTH_OFFSET = 8
    ROW_HEIGHT = 10
    SECTION_HEADER_HEIGHT = 10
    SIGNATURE_IMAGE_WIDTH = 55
    SIGNATURE_IMAGE_HEIGHT = 18
    
    # ═══════════════════════════════════════════════
    # Text Labels
    # ═══════════════════════════════════════════════
    APP_NAME = " طبيب قلبية"
    REPORT_PREFIX = "تقرير: "
    PATIENT_PREFIX = "مريض: "
    DATE_PREFIX = "تاريخ: "
    PATIENT_UNKNOWN = "غير محدد"
    SIGNATURE_PLACEHOLDER = "توقيع الطبيب"
    FOOTER_TEXT = "(c) 2026 مساعد طبيب قلبية"
    SECTION_PREFIX = "■ "
    NOT_AVAILABLE = "-"
    CHECKBOX_YES = "نعم"
    CHECKBOX_NO = "لا"
    
    # ═══════════════════════════════════════════════
    # EMOJI Replacements
    # ═══════════════════════════════════════════════
    EMOJI_REPLACEMENTS = {
        '🏥': '[مستشفى]', '📌': '*', '✅': '(نعم)', '❌': '(لا)',
        '📋': '', '📊': '', '📁': '', '⚠️': '!', '🎯': '',
        '⭐': '*', '⚡': '>>', '🏆': '***',
        '📄': '', '💾': '', '✍️': '', '👨‍⚕️': '', '℞': 'Rx:',
        '🧠': '', '🧬': '', '💊': '', '🩺': '', '🫀': '',
        '🔬': '', '➕': '+', '🗑️': '', '👁️': '', '🔍': '', '📝': '',
    }