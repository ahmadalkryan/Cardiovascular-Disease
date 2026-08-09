# business/factories/patient_factory.py
"""Patient Factory"""

import uuid
from datetime import datetime

from infrastructure.database import Patient
from config import Config


class PatientFactory:
    """Factory for creating Patient objects"""
    
    @staticmethod
    def create_from_prediction(patient_data, prediction, probability, model_name):
        """Create Patient from prediction data"""
        
        model_display = Config.MODELS_INFO.get(model_name, {}).get('display_name', model_name)
        
        return Patient(
            patient_id=str(uuid.uuid4())[:8],
            patient_uid=f"PAT-{str(uuid.uuid4())[:8].upper()}",
            age=patient_data.get('age', 0),
            sex=patient_data.get('sex', 0),
            chest_pain_type=patient_data.get('chest pain type', 0),
            resting_bp_s=patient_data.get('resting bp s', 0),
            cholesterol=patient_data.get('cholesterol', 0),
            fasting_blood_sugar=patient_data.get('fasting blood sugar', 0),
            resting_ecg=patient_data.get('resting ecg', 0),
            max_heart_rate=patient_data.get('max heart rate', 0),
            exercise_angina=patient_data.get('exercise angina', 0),
            oldpeak=patient_data.get('oldpeak', 0),
            st_slope=patient_data.get('ST slope', 0),
            prediction=prediction,
            probability=probability,
            model_used=model_name,
            model_display=model_display,
            created_at=datetime.now(),
            date=datetime.now().strftime('%Y-%m-%d'),
            time=datetime.now().strftime('%H:%M:%S')
        )