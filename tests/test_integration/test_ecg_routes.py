"""Integration tests for ECG Routes"""
import pytest
import json
from unittest.mock import Mock, patch
from flask import Flask
from PIL import Image
import io
from application.routes.ecg_routes import register_ecg_routes


class TestECGRoutes:
    """Tests for ECG Routes"""
    
    @pytest.fixture
    def app(self):
        """Create Flask app for testing"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture
    def mock_ecg_service(self):
        """Create mock ECG service"""
        mock_service = Mock()
        mock_service.get_available_models.return_value = ['densenet_binary', 'densenet_multiclass']
        mock_service.predict_with_details.return_value = {
            'success': True,
            'predicted_class': 'Normal',
            'predicted_class_ar': 'طبيعي ✅',
            'confidence': 0.95,
            'confidence_percent': '95.00%',
            'all_probabilities': {'Normal': 0.95, 'Abnormal': 0.05},
            'all_probabilities_ar': {'طبيعي ✅': 0.95, 'غير طبيعي ⚠️': 0.05},
            'model_used': 'densenet_binary',
            'classes': ['Normal', 'Abnormal'],
            'classes_ar': ['طبيعي ✅', 'غير طبيعي ⚠️']
        }
        return mock_service
    
    @pytest.fixture
    def sample_image_file(self):
        """Create a sample image file for testing"""
        img = Image.new('RGB', (224, 224), color='white')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return (img_byte_arr, 'test_image.png')
    
    def test_get_ecg_models(self, app, client, mock_ecg_service):
        """Test getting ECG models"""
        register_ecg_routes(app, mock_ecg_service, None)
        
        response = client.get('/api/ecg-models')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'models' in data
        assert 'available' in data
        assert 'densenet_binary' in data['available']
    
    def test_predict_ecg_success(self, app, client, mock_ecg_service, sample_image_file):
        """Test successful ECG prediction"""
        register_ecg_routes(app, mock_ecg_service, None)
        
        img_bytes, filename = sample_image_file
        
        response = client.post(
            '/api/predict/ecg',
            data={
                'image': (img_bytes, filename),
                'model': 'densenet_binary'
            },
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'predicted_class' in data
        assert 'predicted_class_ar' in data
        assert 'confidence' in data
    
    def test_predict_ecg_no_image(self, app, client, mock_ecg_service):
        """Test ECG prediction with no image"""
        register_ecg_routes(app, mock_ecg_service, None)
        
        response = client.post('/api/predict/ecg')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'error' in data
    
    def test_predict_ecg_empty_filename(self, app, client, mock_ecg_service):
        """Test ECG prediction with empty filename"""
        register_ecg_routes(app, mock_ecg_service, None)
        
        response = client.post(
            '/api/predict/ecg',
            data={
                'image': (io.BytesIO(b''), '')
            },
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
    
    def test_predict_ecg_invalid_model(self, app, client, mock_ecg_service, sample_image_file):
        """Test ECG prediction with invalid model"""
        register_ecg_routes(app, mock_ecg_service, None)
        
        img_bytes, filename = sample_image_file
        
        response = client.post(
            '/api/predict/ecg',
            data={
                'image': (img_bytes, filename),
                'model': 'invalid_model'
            },
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'error' in data
    
    def test_predict_ecg_prediction_failure(self, app, client, mock_ecg_service, sample_image_file):
        """Test ECG prediction failure"""
        mock_ecg_service.predict_with_details.return_value = None
        register_ecg_routes(app, mock_ecg_service, None)
        
        img_bytes, filename = sample_image_file
        
        response = client.post(
            '/api/predict/ecg',
            data={
                'image': (img_bytes, filename),
                'model': 'densenet_binary'
            },
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] == False
    
   
    
    def test_predict_ecg_response_structure(self, app, client, mock_ecg_service, sample_image_file):
        """Test ECG prediction response structure"""
        register_ecg_routes(app, mock_ecg_service, None)
        
        img_bytes, filename = sample_image_file
        
        response = client.post(
            '/api/predict/ecg',
            data={
                'image': (img_bytes, filename),
                'model': 'densenet_binary'
            },
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check all expected fields
        expected_fields = [
            'success', 'predicted_class', 'predicted_class_ar',
            'confidence', 'confidence_percent', 'class_color',
            'description', 'all_probabilities', 'all_probabilities_ar',
            'model_used', 'model_display', 'model_accuracy',
            'classes', 'classes_ar'
        ]
        
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"