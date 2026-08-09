
# application/routes/settings_routes.py
"""Settings Routes - UI Settings Management"""

from flask import request, jsonify, render_template
from business.services.setting_service import SettingService
from application.exceptions import ValidationError
from infrastructure.models.setting import Setting

def register_settings_routes(app):
    """Register settings routes"""
    
    # ============================================
    # ✅ Page Route
    # ============================================
    
    @app.route('/settings')
    def settings_page():
        """Settings management page"""
        return render_template('settings/index.html')
    
    # ============================================
    # ✅ API Routes
    # ============================================
    
    @app.route('/api/settings', methods=['GET'])
    def get_settings():
        """Get all settings"""
        category = request.args.get('category')
        
        if category:
            settings = SettingService.get_settings_by_category(category)
        else:
            settings = SettingService.get_all_settings()
        
        categories = [
            {'id': 'models', 'name': 'النماذج', 'icon': 'fa-brain'},
            {'id': 'storage', 'name': 'التخزين', 'icon': 'fa-database'},
            {'id': 'logging', 'name': 'السجلات', 'icon': 'fa-history'},
            {'id': 'api', 'name': 'API', 'icon': 'fa-plug'},
            {'id': 'ui', 'name': 'الواجهة', 'icon': 'fa-palette'},
            {'id': 'notifications', 'name': 'الإشعارات', 'icon': 'fa-bell'}
        ]
        
        return jsonify({
            'success': True,
            'settings': settings,
            'categories': categories
        })
    
    @app.route('/api/settings', methods=['POST'])
    def update_settings():
        """Update multiple settings"""
        data = request.get_json()
        if not data:
            raise ValidationError("لا توجد بيانات")
        
        updated = []
        for key, value in data.items():
            setting = Setting.query.filter_by(key=key).first()
            if setting:
                SettingService.set_setting(
                    key=key,
                    value=value,
                    category=setting.category,
                    data_type=setting.data_type,
                    description=setting.description
                )
                updated.append(key)
        
        return jsonify({
            'success': True,
            'message': f'تم تحديث {len(updated)} إعداد',
            'updated': updated
        })