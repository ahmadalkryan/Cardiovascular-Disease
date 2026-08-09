# business/services/prediction_service.py 
"""Prediction Service - Disease prediction using Strategy Pattern"""

import numpy as np
import warnings
import logging

from config import Config
from application.exceptions import ModelNotFoundError, ModelLoadError, PatientDataValidationError
from business.strategies import (
    MinimalModelStrategy,
    Top8ModelStrategy,
    All11ModelStrategy,
    ModelContext
)

logger = logging.getLogger(__name__)


class PredictionService:
    """Handles heart disease prediction using Strategy pattern"""
    
    def __init__(self, models_loaded, scalers_loaded):
        self.models = models_loaded
        self.scalers = scalers_loaded
        self.strategies = {}
        self._register_strategies()
    
    # ================================================
    # Register Strategies
    # ================================================
    def _register_strategies(self):
        """Register all model strategies"""
        if self.models.get('minimal') and self.scalers.get('minimal'):
            self.strategies['minimal'] = MinimalModelStrategy(
                self.models['minimal'], self.scalers['minimal']
            )
            logger.info("✅ Registered Minimal strategy")
        
        if self.models.get('top8') and self.scalers.get('top8'):
            self.strategies['top8'] = Top8ModelStrategy(
                self.models['top8'], self.scalers['top8']
            )
            logger.info("✅ Registered Top8 strategy")
        
        if self.models.get('all11') and self.scalers.get('all11'):
            self.strategies['all11'] = All11ModelStrategy(
                self.models['all11'], self.scalers['all11']
            )
            logger.info("✅ Registered All11 strategy")
    
    # ================================================
    # Predict with Strategy
    # ================================================
    def predict_with_strategy(self, model_name, patient_data):
        """Predict using specific strategy"""
        if model_name not in self.strategies:
            raise ModelNotFoundError(model_name)
        
        try:
            strategy = self.strategies[model_name]
            prediction, probability = strategy.predict(patient_data)
            return int(prediction), float(probability)
        except Exception as e:
            logger.error(f"Prediction failed for {model_name}: {e}")
            raise ModelLoadError(model_name, str(e))
    
    # ================================================
    # Predict Disease (Legacy compatibility)
    # ================================================
    def predict_disease(self, model, model_features, patient_data, scaler):
        """Predict heart disease risk (legacy method)"""
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
        
        try:
            prediction = model.predict(X_final)[0]
            probability = model.predict_proba(X_final)[0][1]
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise ModelLoadError("غير معروف", f"فشل التنبؤ: {str(e)}")
        
        return int(prediction), float(probability)
    
    # ================================================
    # Get Model and Features
    # ================================================
    def get_model_and_features(self, model_name):
        """Get model, features, and scaler for a given model name"""
        if model_name == 'minimal':
            model = self.models.get('minimal')
            features = Config.FEATURES_MINIMAL
            scaler = self.scalers.get('minimal')
        elif model_name == 'top8':
            model = self.models.get('top8')
            features = Config.FEATURES_TOP8
            scaler = self.scalers.get('top8')
        else:
            model = self.models.get('all11')
            features = Config.FEATURES_ALL11
            scaler = self.scalers.get('all11')
        
        if model is None or scaler is None:
            raise ModelNotFoundError(model_name)
        
        return model, features, scaler
    
    # ================================================
    # Batch Predict
    # ================================================
    def batch_predict(self, df, model_name, data_service=None, auto_save=False):
        """Perform batch prediction on multiple patients"""
        model, model_features, scaler = self.get_model_and_features(model_name)
        
        missing_features = [f for f in model_features if f not in df.columns]
        if missing_features:
            raise PatientDataValidationError(f"الميزات المفقودة: {', '.join(missing_features)}")
        
        results = []
        for idx, row in df.iterrows():
            patient_data = row.to_dict()
            try:
                # ✅ Use strategy for prediction
                if model_name in self.strategies:
                    prediction, probability = self.predict_with_strategy(model_name, patient_data)
                else:
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
                    'patient_data': patient_data,
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
                logger.error(f"Batch prediction error at row {idx+1}: {e}")
                results.append({
                    'row_index': idx + 1,
                    'error': str(e),
                    'patient_data': row.to_dict(),
                    'can_save': False
                })
        
        return results, None