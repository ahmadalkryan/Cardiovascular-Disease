# application/routes/prediction_routes.py
"""Prediction Routes - Disease prediction endpoints"""

from flask import request, jsonify, session
import uuid
from datetime import datetime
import logging

from config import Config
from application.exceptions import (
    ModelNotFoundError,
    PatientDataValidationError,
    ValidationError,
    PatientNotFoundError
)

logger = logging.getLogger(__name__)


def register_prediction_routes(app, data_service, prediction_service, config):
    """Register prediction routes"""
    
    @app.route('/predict/<model_name>', methods=['POST'])
    def predict(model_name):
        """Predict heart disease for a patient"""
        if model_name not in Config.MODELS_INFO:
            raise ModelNotFoundError(model_name)
        
        data = request.get_json()
        if not data:
            raise PatientDataValidationError("لا توجد بيانات مرسلة")
        
        # ✅ استخدام Strategy Pattern للتنبؤ
        prediction, probability = prediction_service.predict_with_strategy(model_name, data)
        
        # تحديد مستوى الخطر والتوصيات
        if probability > 0.7:
            risk_level, risk_ar = "HIGH", "عالي 🔴"
            recommendation = "يرجى مراجعة طبيب القلب فوراً"
            recommendation_en = "Please consult a cardiologist immediately"
        elif probability > 0.3:
            risk_level, risk_ar = "MEDIUM", "متوسط 🟡"
            recommendation = "ينصح بمراجعة الطبيب واتباع نمط حياة صحي"
            recommendation_en = "Consult a doctor and maintain a healthy lifestyle"
        else:
            risk_level, risk_ar = "LOW", "منخفض 🟢"
            recommendation = "نتائج مطمئنة، استمر في نمط الحياة الصحي"
            recommendation_en = "Results are reassuring, maintain a healthy lifestyle"
        
        # إنشاء معرف مؤقت
        temp_id = f"TEMP_{datetime.now().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:6]}"
        
        # حفظ في الجلسة
        session['temp_patient'] = {
            'temp_id': temp_id,
            'patient_data': data,
            'prediction': int(prediction),
            'probability': float(probability),
            'result': 'DISEASE' if prediction == 1 else 'HEALTHY',
            'model_used': model_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify({
            'success': True,
            'temp_id': temp_id,
            'prediction': int(prediction),
            'result': 'DISEASE' if prediction == 1 else 'HEALTHY',
            'result_ar': 'مريض' if prediction == 1 else 'سليم',
            'result_en': 'Patient' if prediction == 1 else 'Healthy',
            'probability': float(probability),
            'probability_percent': f"{probability*100:.1f}%",
            'risk_level': risk_level,
            'risk_level_ar': risk_ar,
            'recommendation_ar': recommendation,
            'recommendation_en': recommendation_en,
            'model_used': Config.MODELS_INFO[model_name]['display_name'],
            'model_accuracy': Config.MODELS_INFO[model_name]['accuracy'],
            'patient_data': data,
            'ai_interpretation': {
                'enabled': False,
                'message': 'AI interpretation is disabled',
                'alternative': 'Please consult a doctor for detailed medical advice'
            },
            'ai_available': False,
            'can_save': True
        })
    
    @app.route('/api/save-patient', methods=['POST'])
    def save_patient():
        """Save patient data and diagnosis"""
        data = request.get_json()
        if not data:
            raise ValidationError("لا توجد بيانات مرسلة")
        
        patient_data = data.get('patient_data', {})
        if not patient_data:
            raise PatientDataValidationError("لا توجد بيانات مريض للحفظ")
        
        prediction = data.get('prediction', 0)
        probability = data.get('probability', 0)
        model_name = data.get('model_used', 'top8')
        
        # تصحيح اسم النموذج إذا لزم الأمر
        if model_name not in Config.MODELS_INFO:
            if 'متوسط' in model_name:
                model_name = 'top8'
            elif 'مبسط' in model_name:
                model_name = 'minimal'
            elif 'شامل' in model_name:
                model_name = 'all11'
            else:
                raise ModelNotFoundError(model_name)
        
        doctor_modified = data.get('doctor_modified', False)
        doctor_prediction = data.get('doctor_prediction', prediction)
        doctor_notes = data.get('doctor_notes', '')
        
        final_prediction = doctor_prediction if doctor_modified else prediction
        
        patient_id = data_service.save_patient_data(
            patient_data, final_prediction, probability, model_name, None
        )
        
        if not patient_id:
            raise ValidationError("فشل حفظ بيانات المريض")
        
        if doctor_modified:
            logger.info(f"👨‍⚕️ Diagnosis modified: {prediction} -> {doctor_prediction}")
            logger.info(f"📝 Doctor notes: {doctor_notes}")
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'message': 'Patient data saved successfully',
            'doctor_modified': doctor_modified,
            'doctor_prediction': doctor_prediction
        })
    
    @app.route('/api/update-diagnosis/<patient_id>', methods=['PUT'])
    def update_diagnosis(patient_id):
        """Update diagnosis for a patient"""
        data = request.get_json()
        if not data:
            raise ValidationError("لا توجد بيانات مرسلة")
        
        new_prediction = data.get('prediction')
        doctor_notes = data.get('notes', '')
        
        if new_prediction is None:
            raise ValidationError("الرجاء تقديم تشخيص جديد")
        
        # تحديث في قاعدة البيانات
        success = data_service.update_diagnosis(patient_id, new_prediction, doctor_notes)
        
        if not success:
            raise PatientNotFoundError(patient_id)
        
        logger.info(f"👨‍⚕️ Updated diagnosis for patient {patient_id}: {new_prediction}")
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'new_prediction': new_prediction,
            'message': 'Diagnosis updated successfully'
        })
    
    @app.route('/api/temp-patient/<temp_id>', methods=['GET'])
    def get_temp_patient(temp_id):
        """Get temporary patient data from session"""
        temp_data = session.get('temp_patient', {})
        
        if temp_data.get('temp_id') != temp_id:
            raise PatientNotFoundError(temp_id)
        
        return jsonify({'success': True, 'patient': temp_data})
    
    @app.route('/api/models-info', methods=['GET'])
    def get_models_info():
        """Get information about all available models"""
        models = {}
        for key, info in Config.MODELS_INFO.items():
            models[key] = {
                'name': info['display_name'],
                'features': info['features'],
                'n_features': info['n_features'],
                'model_type': info['model_type'],
                'accuracy': info.get('accuracy', 'N/A'),
                'icon': info['icon'],
                'color': info['color'],
                'desc': info['desc']
            }
        return jsonify({
            'success': True,
            'models': models,
            'total': len(models)
        })