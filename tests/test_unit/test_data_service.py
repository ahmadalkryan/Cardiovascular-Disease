import pytest
import pandas as pd
import numpy as np
import os
import json

class TestDataService:
    """اختبارات خدمة البيانات"""
    
    def test_save_patient_data(self, data_service):
        
        patient_data = {
            'age': 55,
            'sex': 1,
            'resting_bp': 140,
            'cholesterol': 240,
            'max_heart_rate': 150,
            'oldpeak': 1.5
        }
        
        patient_id = data_service.save_patient_data(
            patient_data=patient_data,
            prediction=1,
            probability=0.85,
            model_name='minimal',
            model_features=['age', 'sex', 'resting_bp']
        )
        
        assert patient_id is not None
        assert len(patient_id) == 8
        
        # نتحقق من وجود الملف
        assert os.path.exists(data_service.patient_files['minimal'])
    
    def test_save_patient_data_with_nan(self, data_service):
       
        patient_data = {
            'age': float('nan'),
            'sex': 1,
            'resting_bp': 140,
            'cholesterol': float('inf'),
            'max_heart_rate': 150
        }
        
        patient_id = data_service.save_patient_data(
            patient_data=patient_data,
            prediction=0,
            probability=0.25,
            model_name='top8',
            model_features=['age', 'sex', 'resting_bp']
        )
        
        assert patient_id is not None
        
        # نتحقق من وجود الملف
        assert os.path.exists(data_service.patient_files['top8'])
    
    def test_get_patients_data_empty(self, data_service):
        
        df = data_service.get_patients_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    
    def test_get_patients_data_with_data(self, data_service):
       
        # حفظ بيانات أولاً
        patient_data = {'age': 45, 'sex': 0, 'resting_bp': 120}
        data_service.save_patient_data(
            patient_data=patient_data,
            prediction=1,
            probability=0.90,
            model_name='minimal',
            model_features=['age']
        )
        
        df = data_service.get_patients_data()
        assert len(df) >= 1
    
    def test_get_patients_data_by_model(self, data_service):
        
       
        data_service.save_patient_data(
            patient_data={'age': 45},
            prediction=1,
            probability=0.90,
            model_name='minimal',
            model_features=['age']
        )
        
        data_service.save_patient_data(
            patient_data={'age': 50},
            prediction=0,
            probability=0.20,
            model_name='top8',
            model_features=['age']
        )
        
        df_minimal = data_service.get_patients_data(model_name='minimal')
        df_top8 = data_service.get_patients_data(model_name='top8')
        
        assert len(df_minimal) >= 1
        assert len(df_top8) >= 1
    
    def test_clean_data_for_json(self, data_service):
       
        df = pd.DataFrame([
            {'patient_id': '123', 'age': 45, 'name': 'أحمد', 'probability': 0.85},
            {'patient_id': '456', 'age': np.nan, 'name': 'سارة', 'probability': 0.92},
            {'patient_id': '789', 'age': 60, 'name': None, 'probability': 0.45}
        ])
        
        cleaned = data_service.clean_data_for_json(df)
        
        assert isinstance(cleaned, list)
        assert len(cleaned) == 3
        assert cleaned[0]['patient_id'] == '123'
        
        assert cleaned[1]['age'] == 0 or cleaned[1]['age'] is None
    
    def test_get_statistics_empty(self, data_service):
       
        stats = data_service.get_statistics()
        
        assert stats['total'] == 0
        assert stats['disease'] == 0
        assert stats['healthy'] == 0
        assert stats['avg_probability'] == 0
        assert stats['by_model']['minimal'] == 0
        assert stats['by_model']['top8'] == 0
        assert stats['by_model']['all11'] == 0
        assert len(stats['recent']) == 0
    
    def test_get_statistics_with_data(self, data_service):
        
        for i in range(5):
            data_service.save_patient_data(
                patient_data={'age': 40 + i, 'sex': i % 2},
                prediction=1 if i % 2 == 0 else 0,
                probability=0.5 + i * 0.1,
                model_name='minimal' if i < 3 else 'top8',
                model_features=['age']
            )
        
        stats = data_service.get_statistics()
        
        assert stats['total'] >= 5
        assert stats['disease'] >= 2
        assert stats['healthy'] >= 2
        assert stats['avg_probability'] > 0
        assert stats['by_model']['minimal'] >= 3
        assert stats['by_model']['top8'] >= 2
        assert len(stats['recent']) >= 5