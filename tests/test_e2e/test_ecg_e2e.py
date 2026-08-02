"""End-to-End tests for ECG Service"""
import pytest
import json
import os
import io
import numpy as np
from unittest.mock import Mock, patch
from flask import Flask
from PIL import Image
from business.services.ecg_service import ECGService
from application.routes.ecg_routes import register_ecg_routes
from config import Config


class TestECGE2E:
    """End-to-End tests for ECG workflow"""
    
    @pytest.fixture
    def app(self):
        """Create Flask app for testing"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.secret_key = 'test-secret-key'
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture
    def ecg_service(self):
        """Create ECG service with mock models"""
        with patch('onnxruntime.InferenceSession') as mock_session:
            mock_session_instance = Mock()
            mock_session_instance.get_inputs.return_value = [Mock(name='input')]
            mock_session_instance.get_inputs.return_value[0].name = 'input'
            mock_session.return_value = mock_session_instance
            
            service = ECGService('storage/models')
            
            # Setup mock models
            service.models = {
                'densenet_binary': {
                    'session': mock_session_instance,
                    'type': 'onnx',
                    'classes': ['Normal', 'Abnormal'],
                    'classes_ar': ['طبيعي ✅', 'غير طبيعي ⚠️'],
                    'path': 'densenet_binary.onnx'
                },
                'densenet_multiclass': {
                    'session': mock_session_instance,
                    'type': 'onnx',
                    'classes': ['Abnormal', 'Normal', 'History_MI'],
                    'classes_ar': ['غير طبيعي ⚠️', 'طبيعي ✅', 'تاريخ مرضي 📋'],
                    'path': 'densenet_3multiclass.onnx'
                },
                'onnx_original': {
                    'session': mock_session_instance,
                    'type': 'onnx',
                    'classes': ['Abnormal', 'MI', 'Normal', 'History_MI'],
                    'classes_ar': ['غير طبيعي ⚠️', 'احتشاء عضلة القلب 🔴', 'طبيعي ✅', 'تاريخ مرضي 📋'],
                    'path': 'ecg_median_model.onnx'
                }
            }
            
            # Mock the session.run for predictions
            def mock_run(self, *args, **kwargs):
                return [np.array([[0.1, 0.9]])]
            
            mock_session_instance.run = mock_run
            
            service.loaded = True
            return service
    
    @pytest.fixture
    def sample_image_file(self):
        """Create a sample ECG image file"""
        # Create a realistic-looking ECG image
        img = Image.new('RGB', (224, 224), color='white')
        
        # Draw some ECG-like lines
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Simulate ECG waveform
        points = []
        for x in range(0, 224, 2):
            y = 112 + 50 * np.sin(x / 20) * np.exp(-x / 200)
            points.append((x, int(y)))
        
        draw.line(points, fill='black', width=2)
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return (img_byte_arr, 'ecg_image.png')
    
    def test_full_ecg_workflow(self, app, client, ecg_service, sample_image_file):
        """Test complete ECG workflow: upload → predict → get results"""
        print("\n🫀 Step 1: Setting up ECG routes...")
        register_ecg_routes(app, ecg_service, Config)
        
        # === STEP 2: Get available models ===
        print("\n📊 Step 2: Getting available models...")
        response = client.get('/api/ecg-models')
        assert response.status_code == 200
        models_data = json.loads(response.data)
        assert models_data['success'] == True
        assert 'available' in models_data
        assert len(models_data['available']) >= 1
        
        print(f"✅ Available models: {', '.join(models_data['available'])}")
        
        # === STEP 3: Predict ECG ===
        print("\n📊 Step 3: Predicting ECG...")
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
        result = json.loads(response.data)
        assert result['success'] == True
        assert 'predicted_class' in result
        assert 'predicted_class_ar' in result
        assert 'confidence' in result
        assert 'confidence_percent' in result
        assert 'all_probabilities' in result
        assert 'model_used' in result
        
        print(f"✅ ECG Prediction: {result['predicted_class_ar']}")
        print(f"   Confidence: {result['confidence_percent']}")
        print(f"   Model: {result['model_display']}")
        
        # === STEP 4: Test with different models ===
        print("\n📊 Step 4: Testing all models...")
        models = ['densenet_binary', 'densenet_multiclass', 'onnx_original']
        
        for model in models:
            if model in ecg_service.models:
                img_bytes, filename = sample_image_file
                response = client.post(
                    '/api/predict/ecg',
                    data={
                        'image': (img_bytes, filename),
                        'model': model
                    },
                    content_type='multipart/form-data'
                )
                
                if response.status_code == 200:
                    result = json.loads(response.data)
                    print(f"   {model}: {result['predicted_class']} ({result['confidence_percent']})")
        
        print("✅ All models tested")
    
    def test_ecg_multiple_predictions(self, app, client, ecg_service):
        """Test multiple ECG predictions"""
        print("\n📊 Testing multiple ECG predictions...")
        register_ecg_routes(app, ecg_service, Config)
        
        # Create multiple test images
        test_images = []
        for i in range(3):
            img = Image.new('RGB', (224, 224), color='white')
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            
            # Different patterns for each image
            offset = i * 20
            points = []
            for x in range(0, 224, 2):
                y = 112 + 40 * np.sin((x + offset) / 15) * np.exp(-x / 300)
                points.append((x, int(y)))
            
            draw.line(points, fill='black', width=2)
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            test_images.append(img_byte_arr)
        
        # Predict each image
        results = []
        for i, img_bytes in enumerate(test_images):
            response = client.post(
                '/api/predict/ecg',
                data={
                    'image': (img_bytes, f'ecg_{i}.png'),
                    'model': 'densenet_binary'
                },
                content_type='multipart/form-data'
            )
            
            if response.status_code == 200:
                result = json.loads(response.data)
                results.append(result)
                print(f"   Image {i+1}: {result['predicted_class']} ({result['confidence_percent']})")
        
        assert len(results) >= 1
        print(f"✅ Processed {len(results)} ECG images")
    
    def test_ecg_error_handling(self, app, client, ecg_service):
        """Test ECG error handling"""
        print("\n🔴 Testing ECG error handling...")
        register_ecg_routes(app, ecg_service, Config)
        
        # Test 1: No image uploaded
        response = client.post('/api/predict/ecg')
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False
        assert 'error' in result
        print("✅ No image error handled")
        
        # Test 2: Empty filename
        response = client.post(
            '/api/predict/ecg',
            data={
                'image': (io.BytesIO(b''), '')
            },
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False
        print("✅ Empty filename error handled")
        
        # Test 3: Invalid model
        img_byte_arr = io.BytesIO()
        img = Image.new('RGB', (224, 224), color='white')
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        response = client.post(
            '/api/predict/ecg',
            data={
                'image': (img_byte_arr, 'test.png'),
                'model': 'invalid_model'
            },
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False
        assert 'error' in result
        print("✅ Invalid model error handled")
    
    def test_ecg_response_structure(self, app, client, ecg_service, sample_image_file):
        """Test ECG response structure completeness"""
        print("\n📊 Testing ECG response structure...")
        register_ecg_routes(app, ecg_service, Config)
        
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
        result = json.loads(response.data)
        
        # Check all expected fields
        expected_fields = [
            'success', 'predicted_class', 'predicted_class_ar',
            'confidence', 'confidence_percent', 'class_color',
            'description', 'all_probabilities', 'all_probabilities_ar',
            'model_used', 'model_display', 'model_accuracy',
            'classes', 'classes_ar'
        ]
        
        missing_fields = []
        for field in expected_fields:
            if field not in result:
                missing_fields.append(field)
        
        assert len(missing_fields) == 0, f"Missing fields: {missing_fields}"
        
        print("✅ All response fields present")
        print(f"   Predicted: {result['predicted_class_ar']}")
        print(f"   Confidence: {result['confidence_percent']}")
        print(f"   Description: {result['description']}")
    
    def test_ecg_with_abnormal_image(self, app, client, ecg_service):
        """Test ECG with abnormal pattern"""
        print("\n📊 Testing ECG with abnormal pattern...")
        register_ecg_routes(app, ecg_service, Config)
        
        # Create abnormal ECG pattern
        img = Image.new('RGB', (224, 224), color='white')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Abnormal ECG - irregular pattern
        points = []
        for x in range(0, 224, 2):
            # Irregular waveform
            if 80 < x < 120:
                y = 112 + 60 * np.sin(x / 5) * np.exp(-x / 100)
            else:
                y = 112 + 30 * np.sin(x / 10) * np.exp(-x / 400)
            points.append((x, int(y)))
        
        draw.line(points, fill='black', width=2)
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        response = client.post(
            '/api/predict/ecg',
            data={
                'image': (img_byte_arr, 'abnormal_ecg.png'),
                'model': 'densenet_binary'
            },
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        result = json.loads(response.data)
        print(f"   Abnormal ECG result: {result['predicted_class_ar']}")
        print("✅ Abnormal pattern processed successfully")
    
    def test_ecg_model_accuracy_display(self, app, client, ecg_service, sample_image_file):
        """Test ECG model accuracy display"""
        print("\n📊 Testing model accuracy display...")
        register_ecg_routes(app, ecg_service, Config)
        
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
        result = json.loads(response.data)
        
        assert 'model_accuracy' in result
        assert result['model_accuracy'] is not None
        
        print(f"   Model Accuracy: {result['model_accuracy']}")
        print("✅ Model accuracy displayed")
    
    def test_ecg_batch_processing(self, app, client, ecg_service):
        """Test batch ECG processing"""
        print("\n📦 Testing batch ECG processing...")
        register_ecg_routes(app, ecg_service, Config)
        
        # Create multiple ECG images with different patterns
        patterns = [
            {'name': 'normal', 'amplitude': 30, 'frequency': 10},
            {'name': 'irregular', 'amplitude': 50, 'frequency': 5},
            {'name': 'high_risk', 'amplitude': 70, 'frequency': 3}
        ]
        
        results = []
        for pattern in patterns:
            img = Image.new('RGB', (224, 224), color='white')
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            
            points = []
            for x in range(0, 224, 2):
                y = 112 + pattern['amplitude'] * np.sin(x / pattern['frequency']) * np.exp(-x / 300)
                points.append((x, int(y)))
            
            draw.line(points, fill='black', width=2)
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            response = client.post(
                '/api/predict/ecg',
                data={
                    'image': (img_byte_arr, f"{pattern['name']}.png"),
                    'model': 'densenet_binary'
                },
                content_type='multipart/form-data'
            )
            
            if response.status_code == 200:
                result = json.loads(response.data)
                results.append(result)
                print(f"   {pattern['name']}: {result['predicted_class']} ({result['confidence_percent']})")
        
        assert len(results) >= 1
        print(f"✅ Batch processed {len(results)} ECG images")