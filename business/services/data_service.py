
# business/services/data_service.py
"""Data Service - Patient data CRUD operations (CSV only)"""

import os
import pandas as pd
import numpy as np
import uuid
from datetime import datetime
import logging

from config import Config
from application.exceptions import PatientDataValidationError, PatientNotFoundError

logger = logging.getLogger(__name__)


class DataService:
    """Handles patient data using CSV files only - Compatible with existing format"""
    
    def __init__(self, data_folder, patient_files):
        self.data_folder = data_folder
        self.patient_files = patient_files
    
    # ================================================
    # Save Patient
    # ================================================
    def save_patient_data(self, patient_data, prediction, probability, model_name, model_features):
        """Save patient data to CSV file (same format as existing files)"""
        if not patient_data:
            raise PatientDataValidationError("لا توجد بيانات مريض للحفظ")
        
        if model_name not in Config.MODELS_INFO:
            model_display = model_name
        else:
            model_display = Config.MODELS_INFO[model_name].get('display_name', model_name)
        
        
        record = {
            'patient_id': str(uuid.uuid4())[:8],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'prediction': prediction,
            'result': 'DISEASE' if prediction == 1 else 'HEALTHY',
            'result_ar': 'مريض' if prediction == 1 else 'سليم',
            'probability': round(probability, 4),
            'model_used': model_name,
            'model_display': model_display,
        }
        
       
        feature_mapping = {
            'age': 'age',
            'sex': 'sex',
            'chest pain type': 'chest pain type',
            'resting bp s': 'resting bp s',
            'cholesterol': 'cholesterol',
            'fasting blood sugar': 'fasting blood sugar',
            'resting ecg': 'resting ecg',
            'max heart rate': 'max heart rate',
            'exercise angina': 'exercise angina',
            'oldpeak': 'oldpeak',
            'ST slope': 'ST slope'
        }
        
        for key, value in patient_data.items():
            if key in feature_mapping:
                if isinstance(value, float):
                    if np.isnan(value) or np.isinf(value):
                        record[key] = 0
                    else:
                        record[key] = value
                else:
                    record[key] = value if value is not None else 0
        
        new_record_df = pd.DataFrame([record])
        
        
        file_path = self.patient_files.get(model_name)
        if not file_path:
           
            file_path = list(self.patient_files.values())[0]
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file_exists = os.path.exists(file_path)
        
        try:
            new_record_df.to_csv(
                file_path,
                mode='a',
                header=not file_exists,
                index=False,
                encoding='utf-8-sig'
            )
            logger.info(f"Patient data saved to CSV: {record['patient_id']}")
            return record['patient_id']
        except Exception as e:
            logger.error(f"Failed to save patient data: {e}")
            raise
    
    # ================================================
    # Get Patients 
    # ================================================
    def get_all_patients(self, model_name=None):
        """
        Get all patients as list of dictionaries (for API)
        
        Args:
            model_name: Optional model filter (minimal, top8, all11)
            
        Returns:
            list: List of patient dictionaries
        """
        df = self.get_patients_data(model_name)
        return self.clean_data_for_json(df)
    
    def get_patient(self, patient_id):
        """
        Get a single patient by ID from CSV
        
        Args:
            patient_id: Patient ID (e.g., 'df9ac95e')
            
        Returns:
            dict: Patient data or None if not found
        """
        df = self.get_patients_data()
        if df.empty:
            return None
        
        patient_row = df[df['patient_id'] == patient_id]
        if patient_row.empty:
            return None
        
        return patient_row.iloc[0].to_dict()
    
    def get_patient_by_uid(self, patient_uid):
        """
        Get a single patient by UID from CSV
        
        Args:
            patient_uid: Patient UID (e.g., 'PAT-XXXX')
            
        Returns:
            dict: Patient data or None if not found
        """
       
        df = self.get_patients_data()
        if df.empty:
            return None
        
        
        patient_row = df[df['patient_id'] == patient_uid]
        if patient_row.empty:
            return None
        
        return patient_row.iloc[0].to_dict()
    
    def get_recent_patients(self, limit=10):
        """
        Get recent patients from CSV
        
        Args:
            limit: Maximum number of patients to return
            
        Returns:
            list: List of recent patient dictionaries
        """
        df = self.get_patients_data()
        if df.empty:
            return []
        
     
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp', ascending=False)
        
        recent_df = df.head(limit)
        return self.clean_data_for_json(recent_df)
    
    
    def get_patients_data(self, model_name=None):
        """
        Retrieve patient data from CSV with optional model filtering
        Compatible with existing file format
        """
        if model_name and model_name in self.patient_files:
            files = [self.patient_files[model_name]]
        else:
            files = list(self.patient_files.values())
        
        all_data = []
        for file_path in files:
            if os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
                    if len(df) > 0:
                        all_data.append(df)
                except Exception as e:
                    logger.warning(f"Error reading {file_path}: {e}")
        
        if all_data:
            result = pd.concat(all_data, ignore_index=True)
            if 'patient_id' in result.columns:
                result = result.drop_duplicates(subset=['patient_id'], keep='last')
            return result
        
        return pd.DataFrame()
    
    # ================================================
    # تنظيف البيانات للـ JSON
    # ================================================
    def clean_data_for_json(self, df):
        """
        Clean DataFrame for JSON serialization
        Compatible with existing column names
        """
        if df.empty:
            return []
        
     
        expected_columns = [
            'patient_id', 'timestamp', 'date', 'time',
            'prediction', 'result', 'result_ar', 'probability',
            'model_used', 'model_display',
            'age', 'sex', 'chest pain type', 'resting bp s',
            'cholesterol', 'fasting blood sugar', 'resting ecg',
            'max heart rate', 'exercise angina', 'oldpeak', 'ST slope'
        ]
        
       
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None
        
    
        df = df.fillna({
            'patient_id': '', 'timestamp': '', 'date': '', 'time': '',
            'prediction': 0, 'result': 'UNKNOWN', 'result_ar': 'غير معروف',
            'probability': 0.0, 'model_used': '', 'model_display': '',
            'age': 0, 'sex': 0, 'chest pain type': 0,
            'resting bp s': 0, 'cholesterol': 0,
            'fasting blood sugar': 0, 'resting ecg': 0,
            'max heart rate': 0, 'exercise angina': 0,
            'oldpeak': 0.0, 'ST slope': 0
        })
        
      
        records = df.to_dict(orient='records')
        cleaned_records = []
        
        for record in records:
            cleaned = {}
            for key, value in record.items():
                if pd.isna(value):
                    cleaned[key] = None
                elif isinstance(value, float):
                    cleaned[key] = round(value, 4) if not pd.isna(value) else 0
                elif isinstance(value, np.integer):
                    cleaned[key] = int(value)
                else:
                    cleaned[key] = value
            cleaned_records.append(cleaned)
        
        return cleaned_records

    
    def get_statistics(self):
        """Calculate comprehensive patient statistics from CSV"""
        df = self.get_patients_data()
        
        if df.empty:
            return {
                'total': 0, 'disease': 0, 'healthy': 0, 'avg_probability': 0,
                'by_model': {'minimal': 0, 'top8': 0, 'all11': 0}, 'recent': []
            }
        
        df = df.fillna(0)
        total = len(df)
        disease = len(df[df['prediction'] == 1]) if 'prediction' in df.columns else 0
        healthy = total - disease
        
        if 'probability' in df.columns:
            valid_probs = df['probability'][pd.to_numeric(df['probability'], errors='coerce').notna()]
            avg_prob = valid_probs.mean() * 100 if len(valid_probs) > 0 else 0
        else:
            avg_prob = 0
        
        by_model = {}
        for model in ['minimal', 'top8', 'all11']:
            if 'model_used' in df.columns:
                by_model[model] = len(df[df['model_used'] == model])
            else:
                by_model[model] = 0
        
        recent = []
        if len(df) > 0:
            recent_df = df.tail(10).copy()
            recent_df = recent_df.fillna({
                'patient_id': '-', 'date': '-', 'time': '-',
                'result_ar': '-', 'model_used': '-', 'probability': 0
            })
            recent = recent_df.to_dict(orient='records')
            recent = list(reversed(recent))
        
        return {
            'total': int(total), 'disease': int(disease), 'healthy': int(healthy),
            'avg_probability': float(avg_prob), 'by_model': by_model, 'recent': recent
        }