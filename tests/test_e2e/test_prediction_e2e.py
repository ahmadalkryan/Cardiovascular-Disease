"""End-to-End tests for Prediction Service"""
import pytest
import json
import os
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch
from flask import Flask
from business.services.prediction_service import PredictionService
from business.services.data_service import DataService
from application.routes.prediction_routes import register_prediction_routes
from config import Config


class TestPredictionE2E:
    """End-to-End tests for Prediction workflow"""
    
    @pytest.fixture
    def app(self):
        """Create Flask app for testing"""
        app = Flask(__name__)
        app.secret_key = 'test-secret-key'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture
    def prediction_service(self):
        """Create real PredictionService with mock models"""
        models = {}
        scalers = {}
        
        for model_name in ['minimal', 'top8', 'all11']:
            # Create real mock models
            mock_model = Mock()
            mock_model.predict.return_value = np.array([1])
            mock_model.predict_proba.return_value = np.array([[0.15, 0.85]])
            models[model_name] = mock_model
            
            mock_scaler = Mock()
            mock_scaler.transform.return_value = np.random.rand(1, len(Config.ALL_FEATURES))
            scalers[model_name] = mock_scaler
        
        return PredictionService(models, scalers)
    
    @pytest.fixture
    def data_service(self, tmp_path):
        """Create real DataService with temp folder"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()
        patient_files = {
            'minimal': str(data_folder / 'minimal_patients.csv'),
            'top8': str(data_folder / 'top8_patients.csv'),
            'all11': str(data_folder / 'all11_patients.csv')
        }
        return DataService(str(data_folder), patient_files)
    
    @pytest.fixture
    def ai_service(self):
        """Create mock AI service"""
        mock_ai = Mock()
        mock_ai.available = True
        mock_ai.get_interpretation.return_value = {
            'summary': 'High risk factors detected',
            'recommendation': 'Immediate medical attention required',
            'risk_factors': ['Age', 'Blood Pressure', 'Cholesterol']
        }
        return mock_ai
    
    @pytest.fixture
    def config(self):
        """Mock config"""
        return Config
    
    def test_full_prediction_flow(self, app, client, prediction_service, data_service, ai_service, config):
        """Test complete prediction flow: input → predict → save → retrieve"""
        print("\n🔬 Step 1: Setting up routes...")
        register_prediction_routes(app, ai_service, data_service, prediction_service, config)
        
        # === STEP 2: Predict disease ===
        print("\n📊 Step 2: Making prediction...")
        patient_data = {
            'age': 55,
            'sex': 1,
            'chest pain type': 2,
            'resting bp s': 140,
            'cholesterol': 240,
            'fasting blood sugar': 0,
            'resting ecg': 0,
            'max heart rate': 150,
            'exercise angina': 1,
            'oldpeak': 1.5,
            'ST slope': 2
        }
        
        response = client.post(
            '/predict/minimal',
            data=json.dumps(patient_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        prediction_result = json.loads(response.data)
        assert prediction_result['success'] == True
        assert 'prediction' in prediction_result
        assert 'probability' in prediction_result
        assert 'result' in prediction_result
        assert 'risk_level' in prediction_result
        assert 'temp_id' in prediction_result
        
        print(f"✅ Prediction: {prediction_result['result']} (Probability: {prediction_result['probability_percent']})")
        print(f"✅ Risk Level: {prediction_result['risk_level_ar']}")
        print(f"✅ Temp ID: {prediction_result['temp_id']}")
        
        # === STEP 3: Save patient data ===
        print("\n💾 Step 3: Saving patient data...")
        save_data = {
            'patient_data': patient_data,
            'prediction': prediction_result['prediction'],
            'probability': prediction_result['probability'],
            'model_used': 'minimal',
            'doctor_modified': False,
            'doctor_prediction': prediction_result['prediction'],
            'doctor_notes': ''
        }
        
        response = client.post(
            '/api/save-patient',
            data=json.dumps(save_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        save_result = json.loads(response.data)
        assert save_result['success'] == True
        assert 'patient_id' in save_result
        patient_id = save_result['patient_id']
        
        print(f"✅ Patient saved with ID: {patient_id}")
        
        # === STEP 4: Retrieve saved patient data ===
        print("\n📋 Step 4: Retrieving patient data...")
        df = data_service.get_patients_data('minimal')
        assert not df.empty
        assert len(df) >= 1
        
        # Verify data
        record = df.iloc[-1]  # Last record
        assert record['patient_id'] == patient_id
        assert record['prediction'] == prediction_result['prediction']
        assert record['probability'] == prediction_result['probability']
        assert record['model_used'] == 'minimal'
        assert record['age'] == patient_data['age']
        
        print(f"✅ Patient data verified: {record['patient_name'] if 'patient_name' in record else 'No name'}")
        
        # === STEP 5: Update diagnosis ===
        print("\n🔄 Step 5: Updating diagnosis...")
        update_data = {
            'prediction': 0,
            'notes': 'Doctor reviewed and changed diagnosis to healthy'
        }
        
        response = client.put(
            f'/api/update-diagnosis/{patient_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        update_result = json.loads(response.data)
        assert update_result['success'] == True
        assert update_result['new_prediction'] == 0
        
        print(f"✅ Diagnosis updated to: {update_result['new_prediction']}")
        
        # === STEP 6: Get statistics ===
        print("\n📊 Step 6: Getting statistics...")
        stats = data_service.get_statistics()
        assert stats['total'] >= 1
        assert stats['by_model']['minimal'] >= 1
        
        print(f"✅ Statistics: Total={stats['total']}, Disease={stats['disease']}, Healthy={stats['healthy']}")
        
        # === STEP 7: Cleanup ===
        print("\n🧹 Step 7: Cleaning up...")
        # Delete saved file
        file_path = data_service.patient_files['minimal']
        if os.path.exists(file_path):
            os.remove(file_path)
            print("✅ Cleanup complete")
    
    def test_prediction_with_doctor_modification(self, app, client, prediction_service, data_service, ai_service, config):
        """Test prediction with doctor modification"""
        print("\n👨‍⚕️ Testing doctor modification workflow...")
        register_prediction_routes(app, ai_service, data_service, prediction_service, config)
        
        # Initial prediction (AI says DISEASE)
        patient_data = {
            'age': 60,
            'sex': 1,
            'chest pain type': 3,
            'resting bp s': 150,
            'cholesterol': 280,
            'fasting blood sugar': 1,
            'resting ecg': 1,
            'max heart rate': 140,
            'exercise angina': 1,
            'oldpeak': 2.0,
            'ST slope': 1
        }
        
        # Make prediction
        response = client.post(
            '/predict/minimal',
            data=json.dumps(patient_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        result = json.loads(response.data)
        ai_prediction = result['prediction']
        print(f"🤖 AI Prediction: {result['result_ar']}")
        
        # Doctor modifies (overrides AI)
        save_data = {
            'patient_data': patient_data,
            'prediction': ai_prediction,
            'probability': result['probability'],
            'model_used': 'minimal',
            'doctor_modified': True,
            'doctor_prediction': 1 if ai_prediction == 0 else 0,  # Flip the diagnosis
            'doctor_notes': 'Clinical examination confirms disease'
        }
        
        response = client.post(
            '/api/save-patient',
            data=json.dumps(save_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        save_result = json.loads(response.data)
        assert save_result['success'] == True
        assert save_result['doctor_modified'] == True
        assert save_result['doctor_prediction'] != ai_prediction
        
        print(f"👨‍⚕️ Doctor modified: {ai_prediction} → {save_result['doctor_prediction']}")
        print("✅ Doctor modification workflow successful")
    
    def test_batch_prediction_workflow(self, app, client, prediction_service, data_service, ai_service, config):
        """Test batch prediction workflow"""
        print("\n📦 Testing batch prediction workflow...")
        register_prediction_routes(app, ai_service, data_service, prediction_service, config)
        
        # Create multiple patient records
        patients = [
            {'age': 45, 'sex': 1, 'chest pain type': 2, 'resting bp s': 130, 'cholesterol': 220,
             'fasting blood sugar': 0, 'resting ecg': 0, 'max heart rate': 155, 'exercise angina': 0,
             'oldpeak': 0.5, 'ST slope': 2},
            {'age': 65, 'sex': 0, 'chest pain type': 3, 'resting bp s': 160, 'cholesterol': 300,
             'fasting blood sugar': 1, 'resting ecg': 1, 'max heart rate': 130, 'exercise angina': 1,
             'oldpeak': 2.5, 'ST slope': 1},
            {'age': 50, 'sex': 1, 'chest pain type': 1, 'resting bp s': 120, 'cholesterol': 190,
             'fasting blood sugar': 0, 'resting ecg': 0, 'max heart rate': 165, 'exercise angina': 0,
             'oldpeak': 0.2, 'ST slope': 3}
        ]
        
        # Predict each patient
        results = []
        for i, patient in enumerate(patients):
            response = client.post(
                '/predict/minimal',
                data=json.dumps(patient),
                content_type='application/json'
            )
            
            assert response.status_code == 200
            result = json.loads(response.data)
            results.append(result)
            
            print(f"Patient {i+1}: {result['result_ar']} ({result['probability_percent']})")
            
            # Save each patient
            save_data = {
                'patient_data': patient,
                'prediction': result['prediction'],
                'probability': result['probability'],
                'model_used': 'minimal',
                'doctor_modified': False,
                'doctor_prediction': result['prediction'],
                'doctor_notes': ''
            }
            
            response = client.post(
                '/api/save-patient',
                data=json.dumps(save_data),
                content_type='application/json'
            )
            
            assert response.status_code == 200
        
        # Get statistics
        stats = data_service.get_statistics()
        assert stats['total'] == len(patients)
        print(f"✅ Batch prediction complete: {stats['total']} patients processed")
        print(f"   Disease: {stats['disease']}, Healthy: {stats['healthy']}")
        
        # Cleanup
        file_path = data_service.patient_files['minimal']
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def test_prediction_error_handling(self, app, client, prediction_service, data_service, ai_service, config):
        """Test prediction error handling"""
        print("\n🔴 Testing error handling...")
        register_prediction_routes(app, ai_service, data_service, prediction_service, config)
        
        # Test 1: No data
        response = client.post(
            '/predict/minimal',
            data=None,
            content_type='application/json'
        )
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False
        assert 'error' in result
        print("✅ No data error handled")
        
        # Test 2: Invalid model
        response = client.post(
            '/predict/invalid_model',
            data=json.dumps({'age': 55}),
            content_type='application/json'
        )
        assert response.status_code == 404
        result = json.loads(response.data)
        assert result['success'] == False
        print("✅ Invalid model error handled")
        
        # Test 3: Missing required fields (no data service)
        response = client.post(
            '/api/save-patient',
            data=None,
            content_type='application/json'
        )
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False
        print("✅ Missing data error handled")
        
        # Test 4: Update non-existent patient
        response = client.put(
            '/api/update-diagnosis/NON_EXISTENT',
            data=json.dumps({'prediction': 1}),
            content_type='application/json'
        )
        # Should still work (no actual DB)
        assert response.status_code == 200
        print("✅ Update non-existent handled")
    
    def test_prediction_with_ai_interpretation(self, app, client, prediction_service, data_service, ai_service, config):
        """Test prediction with AI interpretation"""
        print("\n🤖 Testing AI interpretation...")
        register_prediction_routes(app, ai_service, data_service, prediction_service, config)
        
        patient_data = {
            'age': 55,
            'sex': 1,
            'chest pain type': 2,
            'resting bp s': 140,
            'cholesterol': 240,
            'fasting blood sugar': 0,
            'resting ecg': 0,
            'max heart rate': 150,
            'exercise angina': 1,
            'oldpeak': 1.5,
            'ST slope': 2
        }
        
        response = client.post(
            '/predict/minimal',
            data=json.dumps(patient_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        result = json.loads(response.data)
        
        assert result['ai_available'] == True
        assert 'ai_interpretation' in result
        assert result['ai_interpretation'] is not None
        
        print("✅ AI interpretation available")
        print(f"   Summary: {result['ai_interpretation']['summary']}")
        print(f"   Recommendation: {result['ai_interpretation']['recommendation']}")
    
    def test_full_model_comparison(self, app, client, prediction_service, data_service, ai_service, config):
        """Test prediction with all three models"""
        print("\n📊 Testing all models comparison...")
        register_prediction_routes(app, ai_service, data_service, prediction_service, config)
        
        patient_data = {
            'age': 55,
            'sex': 1,
            'chest pain type': 2,
            'resting bp s': 140,
            'cholesterol': 240,
            'fasting blood sugar': 0,
            'resting ecg': 0,
            'max heart rate': 150,
            'exercise angina': 1,
            'oldpeak': 1.5,
            'ST slope': 2
        }
        
        models = ['minimal', 'top8', 'all11']
        results = {}
        
        for model in models:
            response = client.post(
                f'/predict/{model}',
                data=json.dumps(patient_data),
                content_type='application/json'
            )
            
            assert response.status_code == 200
            result = json.loads(response.data)
            results[model] = result
            
            print(f"📊 {model.upper()}: {result['result_ar']} ({result['probability_percent']})")
        
        print("\n✅ All models completed")
        print("   Model comparison:")
        for model, result in results.items():
            print(f"   - {model}: {result['result']} (Probability: {result['probability']:.3f})")