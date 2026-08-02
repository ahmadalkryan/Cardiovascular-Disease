


# business/services/ecg_service.py
"""ECG Service - ECG image analysis using ONNX models"""

import os
import numpy as np
import cv2
import onnxruntime as ort
from PIL import Image

from config import Config 
# from infrastructure.config import Config

class ECGService:
    """Analyzes ECG images using ONNX deep learning models"""
    
    def __init__(self, models_path='storage/models'):
        self.models_path = models_path
        self.models = {}
        self.loaded = False
        self._load_models()
    
    def _load_models(self):
        """Load all ONNX models"""
        print("\n📂 Loading ECG models (ONNX)...")
        print("=" * 60)
        
        model_files = {
            'densenet_binary': 'densenet_binary.onnx',
            'densenet_multiclass': 'densenet_3multiclass.onnx',
            'onnx_original': 'ecg_median_model.onnx'
        }
        
        for model_key, filename in model_files.items():
            model_path = os.path.join(self.models_path, filename)
            
            if os.path.exists(model_path):
                try:
                    session = ort.InferenceSession(model_path)
                    
                    if model_key == 'densenet_binary':
                        classes = ['Normal', 'Abnormal']
                        classes_ar = ['طبيعي ✅', 'غير طبيعي ⚠️']
                    elif model_key == 'densenet_multiclass':
                        classes = ['Abnormal', 'Normal', 'History_MI']
                        classes_ar = ['غير طبيعي ⚠️', 'طبيعي ✅', 'تاريخ مرضي 📋']
                    else:
                        classes = ['Abnormal', 'MI', 'Normal', 'History_MI']
                        classes_ar = ['غير طبيعي ⚠️', 'احتشاء عضلة القلب 🔴', 'طبيعي ✅', 'تاريخ مرضي 📋']
                    
                    self.models[model_key] = {
                        'session': session,
                        'type': 'onnx',
                        'classes': classes,
                        'classes_ar': classes_ar,
                        'path': model_path
                    }
                    print(f"✅ Loaded {model_key}: {filename}")
                    
                except Exception as e:
                    print(f"⚠️ Error loading {model_key}: {e}")
            else:
                print(f"⚠️ File not found: {filename}")
        
        self.loaded = len(self.models) > 0
        print(f"\n📊 Loaded {len(self.models)} ONNX models")
        if self.loaded:
            print("   Available models:", ', '.join(self.models.keys()))
    
    def _preprocess_onnx_original(self, image):
        """Preprocess for original ONNX model with median filter"""
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        h, w = img_array.shape[:2]
        top, bottom = int(h * 0.18), int(h * (1 - 0.06))
        cropped = img_array[top:bottom, :]
        
        gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
        filtered = cv2.medianBlur(gray, 5)
        processed = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
        resized = cv2.resize(processed, (224, 224))
        normalized = resized.astype(np.float32) / 255.0
        
        return np.expand_dims(normalized, axis=0)
    
    def _preprocess_densenet(self, image):
        """Preprocess for DenseNet models with CLAHE"""
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        h, w = img_array.shape[:2]
        top, bottom = int(h * 0.20), int(h * (1 - 0.07))
        cropped = img_array[top:bottom, :]
        
        gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
        processed = cv2.cvtColor(blurred, cv2.COLOR_GRAY2RGB)
        resized = cv2.resize(processed, (224, 224))
        normalized = resized.astype(np.float32) / 255.0
        
        return np.expand_dims(normalized, axis=0)
    
    def _preprocess_image(self, image, model_key):
        """Route image to appropriate preprocessing function"""
        if model_key == 'onnx_original':
            return self._preprocess_onnx_original(image)
        else:
            return self._preprocess_densenet(image)
    
    def predict(self, image, model_key='densenet_binary'):
        """Run prediction using specified model"""
        if model_key not in self.models:
            return None, None, None
        
        try:
            model_info = self.models[model_key]
            session = model_info['session']
            
            input_data = self._preprocess_image(image, model_key)
            input_name = session.get_inputs()[0].name
            
            outputs = session.run(None, {input_name: input_data.astype(np.float32)})
            predictions = outputs[0][0]
            
            predicted_idx = np.argmax(predictions)
            predicted_class = model_info['classes'][predicted_idx]
            confidence = float(predictions[predicted_idx])
            
            return predicted_class, confidence, predictions
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None, None, None
    
    def predict_with_details(self, image, model_key='densenet_binary'):
        """Run prediction with detailed results"""
        predicted_class, confidence, all_probs = self.predict(image, model_key)
        
        if predicted_class is None:
            return None
        
        model_info = self.models[model_key]
        classes = model_info['classes']
        classes_ar = model_info['classes_ar']
        
        probs_dict = {}
        probs_dict_ar = {}
        for i, cls in enumerate(classes):
            probs_dict[cls] = float(all_probs[i])
            probs_dict_ar[classes_ar[i]] = float(all_probs[i])
        
        return {
            'success': True,
            'predicted_class': predicted_class,
            'predicted_class_ar': classes_ar[classes.index(predicted_class)],
            'confidence': confidence,
            'confidence_percent': f"{confidence*100:.2f}%",
            'all_probabilities': probs_dict,
            'all_probabilities_ar': probs_dict_ar,
            'model_used': model_key,
            'classes': classes,
            'classes_ar': classes_ar
        }
    
    def get_available_models(self):
        """Get list of available model keys"""
        return list(self.models.keys())