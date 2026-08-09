"""Integration tests for Prediction Routes"""
import pytest
import json
from unittest.mock import Mock, patch
from flask import Flask
from application.routes.prediction_routes import register_prediction_routes


class TestPredictionRoutes:
    """Tests for Prediction Routes"""
    
    @pytest.fixture
    def app(self):
        """Create Flask app for testing"""
        app = Flask(__name__)
        app.secret_key = 'test-secret-key'
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture
    def mock_services(self):
        """Create mock services"""
        # Mock Prediction Service
        mock_prediction = Mock()
        mock_prediction.get_model_and_features.return_value = (Mock(), ['age'], Mock())
        mock_prediction.predict_disease.return_value = (1, 0.85)
        
        # Mock AI Service
        mock_ai = Mock()
        mock_ai.available = True
        mock_ai.get_interpretation.return_value = {
            'summary': 'Test interpretation',
            'recommendation': 'Test recommendation'
        }
        
        # Mock Data Service
        mock_data = Mock()
        mock_data.save_patient_data.return_value = 'PAT-123456'
        
        # Mock Config
        mock_config = Mock()
        mock_config.MODELS_INFO = {
            'minimal': {'display_name': 'Minimal Model', 'accuracy': '0.85'},
            'top8': {'display_name': 'Top 8 Model', 'accuracy': '0.88'},
            'all11': {'display_name': 'All Features', 'accuracy': '0.90'}
        }
        
        return {
            'prediction_service': mock_prediction,
            'ai_service': mock_ai,
            'data_service': mock_data,
            'config': mock_config
        }
    
    def test_predict_endpoint_success(self, app, client, mock_services):
        """Test successful prediction"""
        # Register routes
        register_prediction_routes(
            app,
            mock_services['ai_service'],
            mock_services['data_service'],
            mock_services['prediction_service'],
            mock_services['config']
        )
        
        # Test data
        patient_data = {
            'age': 55,
            'sex': 1,
            'resting bp s': 140,
            'cholesterol': 240
        }
        
        response = client.post(
            '/predict/minimal',
            data=json.dumps(patient_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'prediction' in data
        assert 'probability' in data
        assert 'result' in data
        assert 'result_ar' in data
    
    def test_predict_endpoint_invalid_model(self, app, client, mock_services):
        """Test prediction with invalid model"""
        register_prediction_routes(
            app,
            mock_services['ai_service'],
            mock_services['data_service'],
            mock_services['prediction_service'],
            mock_services['config']
        )
        
        response = client.post(
            '/predict/invalid_model',
            data=json.dumps({'age': 55}),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] == False
    
  
    def test_save_patient_endpoint(self, app, client, mock_services):
        """Test saving patient data"""
        register_prediction_routes(
            app,
            mock_services['ai_service'],
            mock_services['data_service'],
            mock_services['prediction_service'],
            mock_services['config']
        )
        
        patient_data = {
            'patient_data': {'age': 55, 'sex': 1},
            'prediction': 1,
            'probability': 0.85,
            'model_used': 'minimal'
        }
        
        response = client.post(
            '/api/save-patient',
            data=json.dumps(patient_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'patient_id' in data
    
    def test_save_patient_with_doctor_modification(self, app, client, mock_services):
        """Test saving patient with doctor modification"""
        register_prediction_routes(
            app,
            mock_services['ai_service'],
            mock_services['data_service'],
            mock_services['prediction_service'],
            mock_services['config']
        )
        
        patient_data = {
            'patient_data': {'age': 55, 'sex': 1},
            'prediction': 0,
            'probability': 0.35,
            'model_used': 'minimal',
            'doctor_modified': True,
            'doctor_prediction': 1,
            'doctor_notes': 'Confirmed disease based on clinical signs'
        }
        
        response = client.post(
            '/api/save-patient',
            data=json.dumps(patient_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['doctor_modified'] == True
    
    def test_update_diagnosis_endpoint(self, app, client, mock_services):
        """Test updating diagnosis"""
        register_prediction_routes(
            app,
            mock_services['ai_service'],
            mock_services['data_service'],
            mock_services['prediction_service'],
            mock_services['config']
        )
        
        update_data = {
            'prediction': 1,
            'notes': 'Updated diagnosis based on new test results'
        }
        
        response = client.put(
            '/api/update-diagnosis/PAT-123456',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['new_prediction'] == 1
    
    def test_get_temp_patient(self, app, client, mock_services):
        """Test getting temporary patient data"""
        register_prediction_routes(
            app,
            mock_services['ai_service'],
            mock_services['data_service'],
            mock_services['prediction_service'],
            mock_services['config']
        )
        
        # First, create temp patient via prediction
        with client.session_transaction() as sess:
            sess['temp_patient'] = {
                'temp_id': 'TEMP_123456',
                'patient_data': {'age': 55},
                'prediction': 1,
                'model_used': 'minimal'
            }
        
        response = client.get('/api/temp-patient/TEMP_123456')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'patient' in data
    
    def test_get_temp_patient_not_found(self, app, client, mock_services):
        """Test getting non-existent temporary patient"""
        register_prediction_routes(
            app,
            mock_services['ai_service'],
            mock_services['data_service'],
            mock_services['prediction_service'],
            mock_services['config']
        )
        
        response = client.get('/api/temp-patient/NON_EXISTENT')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] == False
    
    def test_predict_with_ai_interpretation(self, app, client, mock_services):
        """Test prediction with AI interpretation"""
        register_prediction_routes(
            app,
            mock_services['ai_service'],
            mock_services['data_service'],
            mock_services['prediction_service'],
            mock_services['config']
        )
        
        patient_data = {'age': 55, 'sex': 1}
        
        response = client.post(
            '/predict/minimal',
            data=json.dumps(patient_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['ai_available'] == True
        assert 'ai_interpretation' in data