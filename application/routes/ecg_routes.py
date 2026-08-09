# application/routes/ecg_routes.py
"""ECG Routes - ECG image analysis endpoints"""

from flask import request, jsonify
from PIL import Image
import io
import logging

from config import Config
from application.exceptions import (
    ECGModelNotFoundError,
    ECGProcessingError,
    FileUploadError,
    InvalidFileTypeError
)

logger = logging.getLogger(__name__)


def register_ecg_routes(app, ecg_service, config):
    """Register ECG analysis routes"""
    
    @app.route('/api/ecg-models', methods=['GET'])
    def get_ecg_models():
        """Get available ECG models"""
        available = ecg_service.get_available_models()
        models_info = {}
        for key in available:
            if key in Config.ECG_MODELS_INFO:
                models_info[key] = Config.ECG_MODELS_INFO[key]
        return jsonify({
            'success': True,
            'models': models_info,
            'available': available
        })
    
    @app.route('/api/predict/ecg', methods=['POST'])
    def predict_ecg_api():
        """Predict ECG image"""
        if 'image' not in request.files:
            raise FileUploadError("لم يتم رفع صورة")
        
        file = request.files['image']
        if file.filename == '':
            raise FileUploadError("اسم الملف فارغ")
        
        # التحقق من نوع الملف
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            raise InvalidFileTypeError(
                file.filename,
                ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
            )
        
        model_key = request.form.get('model', 'densenet_binary')
        
        available_models = ecg_service.get_available_models()
        if model_key not in available_models:
            raise ECGModelNotFoundError(model_key)
        
        try:
            image = Image.open(io.BytesIO(file.read()))
            result = ecg_service.predict_with_details(image, model_key)
            
            if result is None:
                raise ECGProcessingError("فشل التنبؤ")
            
            model_info = Config.ECG_MODELS_INFO.get(model_key, {})
            
            class_colors = {
                'Normal': '#2ecc71', 'Abnormal': '#e74c3c',
                'MI': '#ff0000', 'History_MI': '#f39c12'
            }
            
            class_descriptions = {
                'Normal': '🟢 قلب طبيعي - مخطط القلب ضمن الحدود الطبيعية',
                'Abnormal': '🟡 ضربات قلب غير طبيعية - تشير إلى عدم انتظام في ضربات القلب',
                'MI': '🔴 احتشاء عضلة القلب - يشير إلى وجود علامات تدل على نوبة قلبية',
                'History_MI': '🟠 تاريخ مرضي باحتشاء عضلة القلب'
            }
            
            return jsonify({
                'success': True,
                'predicted_class': result['predicted_class'],
                'predicted_class_ar': result['predicted_class_ar'],
                'confidence': result['confidence'],
                'confidence_percent': result['confidence_percent'],
                'class_color': class_colors.get(result['predicted_class'], '#000000'),
                'description': class_descriptions.get(result['predicted_class'], ''),
                'all_probabilities': result['all_probabilities'],
                'all_probabilities_ar': result['all_probabilities_ar'],
                'model_used': model_key,
                'model_display': model_info.get('display_name', model_key),
                'model_accuracy': model_info.get('accuracy', 'غير معروف'),
                'classes': result['classes'],
                'classes_ar': result['classes_ar']
            })
            
        except Exception as e:
            logger.error(f"ECG prediction error: {e}")
            raise ECGProcessingError(str(e))