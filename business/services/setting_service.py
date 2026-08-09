
# business/services/setting_service.py
"""Settings Service - Manage application settings"""

import json
import logging
from infrastructure.models.setting import Setting
from infrastructure.database import db

logger = logging.getLogger(__name__)


class SettingService:
    """Service for managing application settings"""
    
    @staticmethod
    def get_setting(key, default=None):
        """Get a setting by key"""
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            return setting.get_value()
        return default
    
    @staticmethod
    def set_setting(key, value, category='general', data_type='string', description=''):
        """Set or update a setting"""
        setting = Setting.query.filter_by(key=key).first()
        
        if setting:
            setting.set_value(value)
            setting.category = category
            setting.data_type = data_type
            setting.description = description
        else:
            setting = Setting(
                key=key,
                value=str(value) if not isinstance(value, (dict, list)) else json.dumps(value),
                category=category,
                data_type=data_type,
                description=description
            )
            db.session.add(setting)
        
        db.session.commit()
        return setting
    
    @staticmethod
    def get_all_settings():
        """Get all settings"""
        settings = Setting.query.all()
        return {s.key: s.get_value() for s in settings}
    
    @staticmethod
    def get_settings_by_category(category):
        """Get settings by category"""
        settings = Setting.query.filter_by(category=category).all()
        return [s.to_dict() for s in settings]
    
    @staticmethod
    def reset_setting(key):
        """Reset a setting to default (delete it)"""
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            db.session.delete(setting)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def init_default_settings():
        """Initialize default settings"""
        default_settings = {
            # Model Settings
            'DEFAULT_MODEL': {
                'value': 'top8',
                'category': 'models',
                'data_type': 'string',
                'description': 'النموذج الافتراضي للتشخيص'
            },
            'MODEL_ACCURACY_THRESHOLD': {
                'value': 0.7,
                'category': 'models',
                'data_type': 'float',
                'description': 'عتبة دقة النموذج (0-1)'
            },
            
            # Storage Settings
            'MAX_UPLOAD_SIZE': {
                'value': 16,
                'category': 'storage',
                'data_type': 'integer',
                'description': 'الحد الأقصى لحجم الملف (MB)'
            },
            'AUTO_BACKUP': {
                'value': True,
                'category': 'storage',
                'data_type': 'boolean',
                'description': 'تفعيل النسخ الاحتياطي التلقائي'
            },
            'BACKUP_INTERVAL': {
                'value': 24,
                'category': 'storage',
                'data_type': 'integer',
                'description': 'فترة النسخ الاحتياطي (ساعات)'
            },
            
            # Logging Settings
            'LOG_LEVEL': {
                'value': 'INFO',
                'category': 'logging',
                'data_type': 'string',
                'description': 'مستوى التسجيل (DEBUG/INFO/WARNING/ERROR)'
            },
            'LOG_RETENTION_DAYS': {
                'value': 30,
                'category': 'logging',
                'data_type': 'integer',
                'description': 'عدد أيام الاحتفاظ بالسجلات'
            },
            
            # API Settings
            'API_TIMEOUT': {
                'value': 30,
                'category': 'api',
                'data_type': 'integer',
                'description': 'مهلة API (ثواني)'
            },
            'MAX_RETRIES': {
                'value': 3,
                'category': 'api',
                'data_type': 'integer',
                'description': 'عدد محاولات إعادة الاتصال'
            },
            
            # UI Settings
            'THEME': {
                'value': 'light',
                'category': 'ui',
                'data_type': 'string',
                'description': 'سمة الواجهة (light/dark)'
            },
            'LANGUAGE': {
                'value': 'ar',
                'category': 'ui',
                'data_type': 'string',
                'description': 'اللغة (ar/en)'
            },
            'ITEMS_PER_PAGE': {
                'value': 15,
                'category': 'ui',
                'data_type': 'integer',
                'description': 'عدد العناصر في الصفحة'
            },
            
            # Notification Settings
            'ENABLE_EMAIL_NOTIFICATIONS': {
                'value': False,
                'category': 'notifications',
                'data_type': 'boolean',
                'description': 'تفعيل إشعارات البريد الإلكتروني'
            },
            'NOTIFICATION_EMAIL': {
                'value': '',
                'category': 'notifications',
                'data_type': 'string',
                'description': 'البريد الإلكتروني للإشعارات'
            }
        }
        
        for key, data in default_settings.items():
            existing = Setting.query.filter_by(key=key).first()
            if not existing:
                setting = Setting(
                    key=key,
                    value=str(data['value']),
                    category=data['category'],
                    data_type=data['data_type'],
                    description=data['description']
                )
                db.session.add(setting)
        
        db.session.commit()
        logger.info("✅ Default settings initialized")