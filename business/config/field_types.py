# business/config/field_types.py
"""Field Types Configuration for Template Builder"""


class FieldTypes:
    """Available field types for medical report templates"""
    
    # ═══════════════════════════════════════════════
    # Type Definitions
    # ═══════════════════════════════════════════════
    BASIC_FIELDS = [
        {'type': 'text', 'label': 'نص قصير', 'icon': 'fa-font', 'category': 'basic'},
        {'type': 'textarea', 'label': 'نص طويل', 'icon': 'fa-align-left', 'category': 'basic'},
        {'type': 'number', 'label': 'رقم', 'icon': 'fa-hashtag', 'category': 'basic'},
        {'type': 'date', 'label': 'تاريخ', 'icon': 'fa-calendar', 'category': 'basic'},
    ]

    CHOICE_FIELDS = [
        {'type': 'select', 'label': 'قائمة منسدلة', 'icon': 'fa-list', 'category': 'choice'},
        {'type': 'checkbox', 'label': 'مربع اختيار (نعم/لا)', 'icon': 'fa-check-square', 'category': 'choice'},
    ]

    LAYOUT_FIELDS = [
        {'type': 'heading', 'label': 'عنوان قسم', 'icon': 'fa-heading', 'category': 'layout'},
        {'type': 'subheading', 'label': 'عنوان فرعي', 'icon': 'fa-heading', 'category': 'layout'},
        {'type': 'divider', 'label': 'فاصل', 'icon': 'fa-minus', 'category': 'layout'},
        {'type': 'signature', 'label': 'توقيع الطبيب', 'icon': 'fa-signature', 'category': 'layout'},
    ]

    # ═══════════════════════════════════════════════
    # Combined List
    # ═══════════════════════════════════════════════
    ALL_FIELDS = BASIC_FIELDS + CHOICE_FIELDS + LAYOUT_FIELDS

    # ═══════════════════════════════════════════════
    # Labels for JavaScript (template_builder.js)
    # ═══════════════════════════════════════════════
    TYPE_LABELS = {
        'text': 'نص قصير', 'textarea': 'نص طويل', 'number': 'رقم', 'date': 'تاريخ',
        'select': 'قائمة منسدلة', 'checkbox': 'مربع اختيار',
        'heading': 'عنوان قسم', 'subheading': 'عنوان فرعي',
        'divider': 'فاصل', 'signature': 'توقيع الطبيب',
    }

    TYPE_ICONS = {
        'text': 'fa-font', 'textarea': 'fa-align-left', 'number': 'fa-hashtag', 'date': 'fa-calendar',
        'select': 'fa-list', 'checkbox': 'fa-check-square',
        'heading': 'fa-heading', 'subheading': 'fa-heading',
        'divider': 'fa-minus', 'signature': 'fa-signature',
    }

    # ═══════════════════════════════════════════════
    # Categories (Arabic Labels)
    # ═══════════════════════════════════════════════
    CATEGORIES = {
        'basic': 'أساسي',
        'choice': 'اختيارات',
        'layout': 'تخطيط',
    }

    @classmethod
    def get_all(cls):
        """Get all field types"""
        return cls.ALL_FIELDS

    @classmethod
    def get_by_category(cls, category):
        """Get fields filtered by category"""
        return [f for f in cls.ALL_FIELDS if f['category'] == category]

    @classmethod
    def get_categories(cls):
        """Get available categories"""
        return cls.CATEGORIES