# business/strategies/model_strategy.py
"""Model Strategy - Strategy pattern for different models"""

from abc import ABC, abstractmethod
import numpy as np
import warnings

from config import Config


class ModelStrategy(ABC):
    """Abstract strategy for prediction models"""
    
    @abstractmethod
    def predict(self, data):
        pass
    
    @abstractmethod
    def get_name(self):
        pass


class MinimalModelStrategy(ModelStrategy):
    """Strategy for Minimal model (4 features)"""
    
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self._name = 'minimal'
        self._features = Config.FEATURES_MINIMAL
    
    def predict(self, data):
       
        full_X = np.zeros((1, len(Config.ALL_FEATURES)))
        
        for i, f in enumerate(Config.ALL_FEATURES):
            if f in self._features:
                value = data.get(f, 0)
                if isinstance(value, str):
                    try:
                        value = float(value)
                    except:
                        value = 0
                full_X[0, i] = value if not np.isnan(value) else 0
            else:
               
                if f == 'resting ecg':
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
            X_scaled = self.scaler.transform(full_X)
        
     
        indices = [Config.ALL_FEATURES.index(f) for f in self._features]
        X_final = X_scaled[:, indices]
        
        
        prediction = self.model.predict(X_final)[0]
        probability = self.model.predict_proba(X_final)[0][1]
        
        return int(prediction), float(probability)
    
    def get_name(self):
        return self._name


class Top8ModelStrategy(ModelStrategy):
    """Strategy for Top8 model (8 features)"""
    
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self._name = 'top8'
        self._features = Config.FEATURES_TOP8
    
    def predict(self, data):
    
        full_X = np.zeros((1, len(Config.ALL_FEATURES)))
        
        for i, f in enumerate(Config.ALL_FEATURES):
            if f in self._features:
                value = data.get(f, 0)
                if isinstance(value, str):
                    try:
                        value = float(value)
                    except:
                        value = 0
                full_X[0, i] = value if not np.isnan(value) else 0
            else:
                #  قيم افتراضية للميزات غير المستخدمة
                if f == 'resting ecg':
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
            X_scaled = self.scaler.transform(full_X)
        
        #  استخراج الميزات المطلوبة فقط
        indices = [Config.ALL_FEATURES.index(f) for f in self._features]
        X_final = X_scaled[:, indices]
        
        #  التنبؤ
        prediction = self.model.predict(X_final)[0]
        probability = self.model.predict_proba(X_final)[0][1]
        
        return int(prediction), float(probability)
    
    def get_name(self):
        return self._name


class All11ModelStrategy(ModelStrategy):
    """Strategy for All11 model (11 features)"""
    
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self._name = 'all11'
        self._features = Config.FEATURES_ALL11
    
    def predict(self, data):
        # إنشاء مصفوفة من 11 ميزة
        full_X = np.zeros((1, len(Config.ALL_FEATURES)))
        
        for i, f in enumerate(Config.ALL_FEATURES):
            if f in self._features:
                value = data.get(f, 0)
                if isinstance(value, str):
                    try:
                        value = float(value)
                    except:
                        value = 0
                full_X[0, i] = value if not np.isnan(value) else 0
            else:
                # قيم افتراضية (لن تستخدم لأن كل الميزات موجودة)
                full_X[0, i] = 0
        
        #  تطبيع المصفوفة الكاملة
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
            X_scaled = self.scaler.transform(full_X)
        
        
        indices = [Config.ALL_FEATURES.index(f) for f in self._features]
        X_final = X_scaled[:, indices]
        
        #  التنبؤ
        prediction = self.model.predict(X_final)[0]
        probability = self.model.predict_proba(X_final)[0][1]
        
        return int(prediction), float(probability)
    
    def get_name(self):
        return self._name


class ModelContext:
    """Context for model strategies"""
    
    def __init__(self):
        self._strategy = None
    
    def set_strategy(self, strategy):
        self._strategy = strategy
    
    def predict(self, data):
        if not self._strategy:
            raise ValueError("No strategy set")
        return self._strategy.predict(data)
    
    def get_model_name(self):
        return self._strategy.get_name() if self._strategy else None