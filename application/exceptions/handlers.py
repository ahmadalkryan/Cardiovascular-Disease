
# application/exceptions/handlers.py
"""Global Exception Handlers - Flask Native Best Practice"""

import logging
from flask import jsonify, render_template, request, current_app
from werkzeug.exceptions import HTTPException

from .custom_exceptions import AppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    """Register all global exception handlers with the Flask app"""
    
    
    @app.errorhandler(Exception)
    def handle_all_exceptions(e):
        """معالج واحد لكل الأخطاء - أفضل ممارسة في Flask"""
        
        status_code = 500
        error_message = str(e)
        error_code = 'INTERNAL_ERROR'
        
        # التعامل مع أخطاء HTTP
        if isinstance(e, HTTPException):
            status_code = e.code
            error_message = e.description or e.name
            error_code = f'HTTP_{status_code}'
        
        # التعامل مع الاستثناءات المخصصة
        if hasattr(e, 'status_code'):
            status_code = e.status_code
        if hasattr(e, 'error_code'):
            error_code = e.error_code
        if hasattr(e, 'message'):
            error_message = e.message
        
        # تسجيل الخطأ
        logger.error(f"Exception: {error_code} - {error_message}")
        if current_app.debug:
            import traceback
            logger.error(traceback.format_exc())
        
        # بناء الاستجابة
        response_data = {
            'success': False,
            'error': error_message if current_app.debug else "حدث خطأ في الخادم",
            'error_code': error_code,
            'status_code': status_code
        }
        
      
        if current_app.debug:
            import traceback
            response_data['debug'] = {
                'traceback': traceback.format_exc(),
                'type': e.__class__.__name__
            }
        
       
        if request.path.startswith('/api/') or request.is_json:
            return jsonify(response_data), status_code
        
        # استجابة HTML للصفحات
        return render_template(
            'error.html',
            error_message=response_data['error'],
            error_code=error_code,
            status_code=status_code,
            debug_info=response_data.get('debug')
        ), status_code
    
   
    
    @app.errorhandler(404)
    def handle_404(e):
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'المسار غير موجود',
                'error_code': 'NOT_FOUND',
                'status_code': 404
            }), 404
        return render_template('error.html',
                              error_message='الصفحة غير موجودة',
                              status_code=404), 404
    
    @app.errorhandler(403)
    def handle_403(e):
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'غير مصرح بالوصول',
                'error_code': 'FORBIDDEN',
                'status_code': 403
            }), 403
        return render_template('error.html',
                              error_message='غير مصرح بالوصول',
                              status_code=403), 403
    
    @app.errorhandler(413)
    def handle_413(e):
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
        max_mb = max_size / (1024 * 1024)
        return jsonify({
            'success': False,
            'error': f'الملف كبير جداً. الحد الأقصى {max_mb:.0f}MB',
            'error_code': 'FILE_TOO_LARGE',
            'status_code': 413
        }), 413
    
    logger.info(" Global exception handlers registered (Flask Native)")