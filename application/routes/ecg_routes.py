# application/routes/ecg_routes.py
"""ECG Routes - ECG image analysis endpoints"""

from flask import request, jsonify
from PIL import Image
import io
#from infrastructure.config import Config
from config import Config 


def register_ecg_routes(app, ecg_service, config):
    """Register ECG analysis routes"""
    
    @app.route('/api/ecg-models', methods=['GET'])
    def get_ecg_models():
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
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'لم يتم رفع صورة'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'اسم الملف فارغ'}), 400
        
        model_key = request.form.get('model', 'densenet_binary')
        
        available_models = ecg_service.get_available_models()
        if model_key not in available_models:
            return jsonify({
                'success': False,
                'error': f'النموذج {model_key} غير متوفر. النماذج المتاحة: {", ".join(available_models)}'
            }), 400
        
        try:
            image = Image.open(io.BytesIO(file.read()))
            result = ecg_service.predict_with_details(image, model_key)
            
            if result is None:
                return jsonify({'success': False, 'error': 'فشل التنبؤ'}), 500
            
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
            print(f"❌ خطأ في معالجة الصورة: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500