# application/routes/prediction_routes.py
"""Prediction Routes - Disease prediction endpoints"""

from flask import request, jsonify, session
import uuid
from datetime import datetime
#from infrastructure.config import Config
from config import Config 


def register_prediction_routes(app, ai_service, data_service, prediction_service, config):
    """Register prediction routes"""
    
    @app.route('/predict/<model_name>', methods=['POST'])
    def predict(model_name):
        if model_name not in Config.MODELS_INFO:
            return jsonify({'success': False, 'error': 'Model not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        model, model_features, scaler = prediction_service.get_model_and_features(model_name)
        
        if model is None or scaler is None:
            return jsonify({'success': False, 'error': f'Model {model_name} not loaded'}), 500
        
        try:
            prediction, probability = prediction_service.predict_disease(
                model, model_features, data, scaler
            )
            
            if probability > 0.7:
                risk_level, risk_ar = "HIGH", "عالي 🔴"
                recommendation = "يرجى مراجعة طبيب القلب فوراً"
            elif probability > 0.3:
                risk_level, risk_ar = "MEDIUM", "متوسط 🟡"
                recommendation = "ينصح بمراجعة الطبيب واتباع نمط حياة صحي"
            else:
                risk_level, risk_ar = "LOW", "منخفض 🟢"
                recommendation = "نتائج مطمئنة، استمر في نمط الحياة الصحي"
            
            ai_interpretation = None
            if ai_service and ai_service.available:
                ai_interpretation = ai_service.get_interpretation(
                    data, prediction, probability, model_name
                )
            
            temp_id = f"TEMP_{datetime.now().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:6]}"
            
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
                'probability': float(probability),
                'probability_percent': f"{probability*100:.1f}%",
                'risk_level': risk_level,
                'risk_level_ar': risk_ar,
                'recommendation_ar': recommendation,
                'model_used': Config.MODELS_INFO[model_name]['display_name'],
                'model_accuracy': Config.MODELS_INFO[model_name]['accuracy'],
                'patient_data': data,
                'ai_interpretation': ai_interpretation,
                'ai_available': ai_service.available if ai_service else False,
                'can_save': True
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/save-patient', methods=['POST'])
    def save_patient():
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
            
            patient_data = data.get('patient_data', {})
            prediction = data.get('prediction', 0)
            probability = data.get('probability', 0)
            model_name = data.get('model_used', 'top8')
            
            if model_name not in Config.MODELS_INFO:
                if 'متوسط' in model_name:
                    model_name = 'top8'
                elif 'مبسط' in model_name:
                    model_name = 'minimal'
                elif 'شامل' in model_name:
                    model_name = 'all11'
            
            doctor_modified = data.get('doctor_modified', False)
            doctor_prediction = data.get('doctor_prediction', prediction)
            doctor_notes = data.get('doctor_notes', '')
            
            final_prediction = doctor_prediction if doctor_modified else prediction
            
            patient_id = data_service.save_patient_data(
                patient_data, final_prediction, probability, model_name, None
            )
            
            if patient_id:
                if doctor_modified:
                    print(f"👨‍⚕️ Diagnosis modified by doctor: {prediction} -> {doctor_prediction}")
                    print(f"📝 Doctor notes: {doctor_notes}")
                
                return jsonify({
                    'success': True,
                    'patient_id': patient_id,
                    'message': 'Patient data saved successfully',
                    'doctor_modified': doctor_modified,
                    'doctor_prediction': doctor_prediction
                })
            else:
                return jsonify({'success': False, 'error': 'Failed to save data'}), 500
                
        except Exception as e:
            print(f"❌ Error saving patient: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/update-diagnosis/<patient_id>', methods=['PUT'])
    def update_diagnosis(patient_id):
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
            
            new_prediction = data.get('prediction')
            doctor_notes = data.get('notes', '')
            
            if new_prediction is None:
                return jsonify({'success': False, 'error': 'Please provide new diagnosis'}), 400
            
            print(f"👨‍⚕️ Updating diagnosis for patient {patient_id}")
            print(f"   New diagnosis: {'Disease' if new_prediction == 1 else 'Healthy'}")
            print(f"   Doctor notes: {doctor_notes}")
            
            return jsonify({
                'success': True,
                'patient_id': patient_id,
                'new_prediction': new_prediction,
                'message': 'Diagnosis updated successfully'
            })
            
        except Exception as e:
            print(f"❌ Error updating diagnosis: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/temp-patient/<temp_id>', methods=['GET'])
    def get_temp_patient(temp_id):
        try:
            temp_data = session.get('temp_patient', {})
            
            if temp_data.get('temp_id') == temp_id:
                return jsonify({'success': True, 'patient': temp_data})
            else:
                return jsonify({'success': False, 'error': 'Patient data not found'}), 404
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500