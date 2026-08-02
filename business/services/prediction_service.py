# business/services/prediction_service.py
"""Prediction Service - Disease prediction using clinical ML models"""

import numpy as np
import pandas as pd
import warnings
from config import Config 
# from infrastructure.config import Config

class PredictionService:
    """
    Handles heart disease prediction using clinical models.
    Manages three models: minimal (4 features), top8 (8 features), all11 (11 features).
    """
    
    def __init__(self, models_loaded, scalers_loaded):
        self.models = models_loaded
        self.scalers = scalers_loaded
    
    def predict_disease(self, model, model_features, patient_data, scaler):
        """Predict heart disease risk for a single patient"""
        full_X = np.zeros((1, len(Config.ALL_FEATURES)))
        
        for i, f in enumerate(Config.ALL_FEATURES):
            if f in model_features:
                value = patient_data.get(f, 0)
                if isinstance(value, str):
                    try:
                        value = float(value)
                    except:
                        value = 0
                full_X[0, i] = value if not np.isnan(value) else 0
            elif f == 'resting ecg':
                full_X[0, i] = 0
            elif f == 'fasting blood sugar':
                full_X[0, i] = 0
            elif f == 'cholesterol':
                full_X[0, i] = 200
            elif f == 'age':
                full_X[0, i] = 50
            elif f == 'sex':
                full_X[0, i] = 1
            elif f == 'resting bp s':
                full_X[0, i] = 120
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
            X_scaled = scaler.transform(full_X)
        
        indices = [Config.ALL_FEATURES.index(f) for f in model_features]
        X_final = X_scaled[:, indices]
        
        prediction = model.predict(X_final)[0]
        probability = model.predict_proba(X_final)[0][1]
        
        return int(prediction), float(probability)
    
    def get_model_and_features(self, model_name):
        """Get model, features, and scaler for a given model name"""
        if model_name == 'minimal':
            return self.models.get('minimal'), Config.FEATURES_MINIMAL, self.scalers.get('minimal')
        elif model_name == 'top8':
            return self.models.get('top8'), Config.FEATURES_TOP8, self.scalers.get('top8')
        else:
            return self.models.get('all11'), Config.FEATURES_ALL11, self.scalers.get('all11')
    
    def batch_predict(self, df, model_name, data_service=None, auto_save=False):
        """Perform batch prediction on multiple patients"""
        model, model_features, scaler = self.get_model_and_features(model_name)
        
        if model is None or scaler is None:
            return None, f'Model {model_name} not loaded'
        
        missing_features = [f for f in model_features if f not in df.columns]
        if missing_features:
            return None, f'Missing features: {", ".join(missing_features)}'
        
        results = []
        for idx, row in df.iterrows():
            patient_data = row.to_dict()
            try:
                prediction, probability = self.predict_disease(
                    model, model_features, patient_data, scaler
                )
                
                patient_id = None
                if auto_save and data_service:
                    patient_id = data_service.save_patient_data(
                        patient_data, prediction, probability, model_name, model_features
                    )
                
                if probability > 0.7:
                    risk_level, risk_ar = "HIGH", "عالي 🔴"
                elif probability > 0.3:
                    risk_level, risk_ar = "MEDIUM", "متوسط 🟡"
                else:
                    risk_level, risk_ar = "LOW", "منخفض 🟢"
                
                result_entry = {
                    'row_index': idx + 1,
                    'prediction': int(prediction),
                    'result': 'DISEASE' if prediction == 1 else 'HEALTHY',
                    'result_ar': 'مريض' if prediction == 1 else 'سليم',
                    'probability': float(probability),
                    'probability_percent': f"{probability*100:.1f}%",
                    'risk_level': risk_level,
                    'risk_level_ar': risk_ar,
                    'patient_data': {k: (float(v) if not isinstance(v, str) and not np.isnan(float(v)) else v) for k, v in patient_data.items()},
                    'model_used': model_name,
                    'doctor_modified': False,
                    'doctor_prediction': int(prediction),
                    'doctor_notes': '',
                    'can_save': True
                }
                
                if patient_id:
                    result_entry['patient_id'] = patient_id
                    result_entry['saved'] = True
                else:
                    result_entry['saved'] = False
                
                results.append(result_entry)
                
            except Exception as e:
                results.append({
                    'row_index': idx + 1,
                    'error': str(e),
                    'patient_data': row.to_dict(),
                    'can_save': False
                })
        
        return results, None