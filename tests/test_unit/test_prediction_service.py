"""Unit tests for Prediction Service"""
import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from business.services.prediction_service import PredictionService
from config import Config


class TestPredictionService:
    """Tests for Prediction Service"""
    
    @pytest.fixture
    def prediction_service(self):
        """Create prediction service with mock models"""
        models = {}
        scalers = {}
        
        for model_name in ['minimal', 'top8', 'all11']:
            # Mock model
            mock_model = Mock()
            mock_model.predict.return_value = np.array([1])
            mock_model.predict_proba.return_value = np.array([[0.2, 0.8]])
            models[model_name] = mock_model
            
            # Mock scaler
            mock_scaler = Mock()
            # استخدام np.random.rand بدلاً من return_value مباشرة
            mock_scaler.transform = Mock(return_value=np.random.rand(1, len(Config.ALL_FEATURES)))
            scalers[model_name] = mock_scaler
        
        return PredictionService(models, scalers)
    
    def test_init(self, prediction_service):
        """Test service initialization"""
        assert prediction_service.models is not None
        assert prediction_service.scalers is not None
        assert len(prediction_service.models) == 3
        assert 'minimal' in prediction_service.models
        assert 'top8' in prediction_service.models
        assert 'all11' in prediction_service.models
    
    def test_predict_disease_minimal(self, prediction_service):
        """Test prediction with minimal model"""
        patient_data = {
            'age': 55,
            'sex': 1,
            'resting bp s': 140,
            'cholesterol': 240,
            'max heart rate': 150,
            'exercise angina': 1,
            'ST slope': 2,
            'chest pain type': 2,
            'resting ecg': 0,
            'oldpeak': 1.5,
            'fasting blood sugar': 0
        }
        
        model, features, scaler = prediction_service.get_model_and_features('minimal')
        prediction, probability = prediction_service.predict_disease(
            model, features, patient_data, scaler
        )
        
        assert prediction in [0, 1]
        assert 0 <= probability <= 1
    
    def test_predict_disease_all_features(self, prediction_service):
        """Test prediction with all 11 features"""
        patient_data = {
            'age': 60,
            'sex': 0,
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
        
        model, features, scaler = prediction_service.get_model_and_features('all11')
        prediction, probability = prediction_service.predict_disease(
            model, features, patient_data, scaler
        )
        
        assert prediction in [0, 1]
        assert 0 <= probability <= 1
    
    def test_predict_disease_with_string_values(self, prediction_service):
        """Test prediction with string values"""
        patient_data = {
            'age': '55',
            'sex': '1',
            'resting bp s': '140',
            'cholesterol': '240'
        }
        
        model, features, scaler = prediction_service.get_model_and_features('minimal')
        prediction, probability = prediction_service.predict_disease(
            model, features, patient_data, scaler
        )
        
        assert prediction in [0, 1]
        assert 0 <= probability <= 1
    
    def test_predict_disease_with_nan_values(self, prediction_service):
        """Test prediction with NaN values"""
        patient_data = {
            'age': float('nan'),
            'sex': 1,
            'resting bp s': float('nan'),
            'cholesterol': 240
        }
        
        model, features, scaler = prediction_service.get_model_and_features('minimal')
        prediction, probability = prediction_service.predict_disease(
            model, features, patient_data, scaler
        )
        
        assert prediction in [0, 1]
        assert 0 <= probability <= 1
    
    def test_predict_disease_missing_features(self, prediction_service):
        """Test prediction with missing features"""
        patient_data = {
            'age': 55,
            'sex': 1
            # Missing other features
        }
        
        model, features, scaler = prediction_service.get_model_and_features('minimal')
        prediction, probability = prediction_service.predict_disease(
            model, features, patient_data, scaler
        )
        
        # Should use default values for missing features
        assert prediction in [0, 1]
        assert 0 <= probability <= 1
    
    def test_get_model_and_features_minimal(self, prediction_service):
        """Test getting minimal model"""
        model, features, scaler = prediction_service.get_model_and_features('minimal')
        
        assert model is not None
        assert isinstance(features, list)
        assert len(features) == len(Config.FEATURES_MINIMAL)
        assert scaler is not None
    
    def test_get_model_and_features_top8(self, prediction_service):
        """Test getting top8 model"""
        model, features, scaler = prediction_service.get_model_and_features('top8')
        
        assert model is not None
        assert isinstance(features, list)
        assert len(features) == len(Config.FEATURES_TOP8)
        assert scaler is not None
    
    def test_get_model_and_features_all11(self, prediction_service):
        """Test getting all11 model"""
        model, features, scaler = prediction_service.get_model_and_features('all11')
        
        assert model is not None
        assert isinstance(features, list)
        assert len(features) == len(Config.FEATURES_ALL11)
        assert scaler is not None
    
    
    
    def test_batch_predict_success(self, prediction_service):
        """Test batch prediction success"""
        df = pd.DataFrame({
            'age': [55, 60, 45],
            'sex': [1, 0, 1],
            'resting bp s': [140, 150, 120],
            'cholesterol': [240, 280, 200],
            'max heart rate': [150, 140, 160],
            'exercise angina': [1, 0, 0],
            'ST slope': [2, 1, 3],
            'chest pain type': [2, 3, 1],
            'resting ecg': [0, 1, 0],
            'oldpeak': [1.5, 2.0, 0.5],
            'fasting blood sugar': [0, 1, 0]
        })
        
        results, error = prediction_service.batch_predict(df, 'minimal')
        
        assert error is None
        assert results is not None
        assert len(results) == len(df)
        assert 'prediction' in results[0]
        assert 'probability' in results[0]
        assert 'risk_level' in results[0]
        assert 'risk_level_ar' in results[0]
    
    def test_batch_predict_missing_features(self, prediction_service):
        """Test batch prediction with missing features"""
        df = pd.DataFrame({
            'age': [55, 60],
            'sex': [1, 0]
            # Missing other features
        })
        
        results, error = prediction_service.batch_predict(df, 'minimal')
        
        # يجب أن يعطي خطأ بسبب الميزات المفقودة
        assert results is None
        assert error is not None
        assert 'Missing features' in error
    
    
    def test_batch_predict_with_auto_save(self, prediction_service):
        """Test batch prediction with auto save"""
        df = pd.DataFrame({
            'age': [55, 60],
            'sex': [1, 0],
            'resting bp s': [140, 150],
            'cholesterol': [240, 280],
            'max heart rate': [150, 140],
            'exercise angina': [1, 0],
            'ST slope': [2, 1],
            'chest pain type': [2, 3],
            'resting ecg': [0, 1],
            'oldpeak': [1.5, 2.0],
            'fasting blood sugar': [0, 1]
        })
        
        # Mock data service
        mock_data_service = Mock()
        mock_data_service.save_patient_data.return_value = 'PAT-123456'
        
        results, error = prediction_service.batch_predict(
            df, 'minimal', data_service=mock_data_service, auto_save=True
        )
        
        assert error is None
        assert results is not None
        assert len(results) == len(df)
        assert results[0]['saved'] == True
        assert results[0]['patient_id'] == 'PAT-123456'
    
    def test_risk_levels_calculation(self, prediction_service):
        """Test risk level classification by checking results from batch_predict"""
        # Create a simple DataFrame
        df = pd.DataFrame({
            'age': [55],
            'sex': [1],
            'resting bp s': [140],
            'cholesterol': [240],
            'max heart rate': [150],
            'exercise angina': [1],
            'ST slope': [2],
            'chest pain type': [2],
            'resting ecg': [0],
            'oldpeak': [1.5],
            'fasting blood sugar': [0]
        })
        
        # Mock the predict_disease to return different probabilities
        original_predict = prediction_service.predict_disease
        
        # Test high risk
        def mock_predict_high(model, features, data, scaler):
            return 1, 0.85
        
        prediction_service.predict_disease = mock_predict_high
        results, error = prediction_service.batch_predict(df, 'minimal')
        
        assert error is None
        assert results[0]['risk_level'] == "HIGH"
        assert "عالي" in results[0]['risk_level_ar']
        
        # Test medium risk
        def mock_predict_medium(model, features, data, scaler):
            return 0, 0.50
        
        prediction_service.predict_disease = mock_predict_medium
        results, error = prediction_service.batch_predict(df, 'minimal')
        
        assert error is None
        assert results[0]['risk_level'] == "MEDIUM"
        assert "متوسط" in results[0]['risk_level_ar']
        
        # Test low risk
        def mock_predict_low(model, features, data, scaler):
            return 0, 0.15
        
        prediction_service.predict_disease = mock_predict_low
        results, error = prediction_service.batch_predict(df, 'minimal')
        
        assert error is None
        assert results[0]['risk_level'] == "LOW"
        assert "منخفض" in results[0]['risk_level_ar']
        
        # Restore original
        prediction_service.predict_disease = original_predict


class TestPredictionServiceIntegration:
    """Integration tests for Prediction Service"""
    
    @pytest.fixture
    def prediction_service(self):
        """Create prediction service with mock models for integration tests"""
        models = {}
        scalers = {}
        
        for model_name in ['minimal', 'top8', 'all11']:
            mock_model = Mock()
            mock_model.predict.return_value = np.array([1])
            mock_model.predict_proba.return_value = np.array([[0.2, 0.8]])
            models[model_name] = mock_model
            
            mock_scaler = Mock()
            mock_scaler.transform = Mock(return_value=np.random.rand(1, len(Config.ALL_FEATURES)))
            scalers[model_name] = mock_scaler
        
        return PredictionService(models, scalers)
    
    def test_full_prediction_workflow(self, prediction_service):
        """Test full prediction workflow"""
        # 1. Create patient data
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
        
        # 2. Get model and predict for each model
        for model_name in ['minimal', 'top8', 'all11']:
            model, features, scaler = prediction_service.get_model_and_features(model_name)
            assert model is not None
            
            prediction, probability = prediction_service.predict_disease(
                model, features, patient_data, scaler
            )
            
            assert prediction in [0, 1]
            assert 0 <= probability <= 1
    
    def test_batch_prediction_with_different_models(self, prediction_service):
        """Test batch prediction with different models"""
        df = pd.DataFrame({
            'age': [55, 60, 45, 50],
            'sex': [1, 0, 1, 0],
            'resting bp s': [140, 150, 120, 130],
            'cholesterol': [240, 280, 200, 220],
            'max heart rate': [150, 140, 160, 155],
            'exercise angina': [1, 0, 0, 1],
            'ST slope': [2, 1, 3, 2],
            'chest pain type': [2, 3, 1, 2],
            'resting ecg': [0, 1, 0, 0],
            'oldpeak': [1.5, 2.0, 0.5, 1.0],
            'fasting blood sugar': [0, 1, 0, 0]
        })
        
        for model_name in ['minimal', 'top8', 'all11']:
            results, error = prediction_service.batch_predict(df, model_name)
            
            assert error is None
            assert results is not None
            assert len(results) == len(df)
            assert all('risk_level' in r for r in results)