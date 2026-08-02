

# config.py - Application Configuration (Root Level)

import os

class Config:
    """Main configuration class for the Heart Disease Diagnosis System"""
    
    # ================================================
    # Flask Settings
    # ================================================
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-2024')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # ================================================
    # Base Directory
    # ================================================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # ================================================
    # Storage Paths
    # ================================================
    STORAGE_FOLDER = os.path.join(BASE_DIR, 'storage')
    DATA_FOLDER = os.path.join(STORAGE_FOLDER, 'data')
    MODELS_PATH = os.path.join(STORAGE_FOLDER, 'models')
    ECG_MODELS_PATH = os.path.join(STORAGE_FOLDER, 'models')
    UPLOAD_FOLDER = os.path.join(STORAGE_FOLDER, 'uploads')
    RESULTS_FOLDER = os.path.join(STORAGE_FOLDER, 'uploads', 'batch_results')
    REPORTS_FOLDER = os.path.join(STORAGE_FOLDER, 'reports')
    
    # ================================================
    # Presentation Paths
    # ================================================
    PRESENTATION_FOLDER = os.path.join(BASE_DIR, 'presentation')
    TEMPLATE_FOLDER = os.path.join(PRESENTATION_FOLDER, 'templates')
    STATIC_FOLDER = os.path.join(PRESENTATION_FOLDER, 'static')
    
    # ================================================
    # Database
    # ================================================
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(STORAGE_FOLDER, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ================================================
    # Patient Files
    # ================================================
    PATIENT_FILES = {
        'minimal': os.path.join(DATA_FOLDER, 'patients_minimal.csv'),
        'top8': os.path.join(DATA_FOLDER, 'patients_top8.csv'),
        'all11': os.path.join(DATA_FOLDER, 'patients_all11.csv')
    }
    
    # ================================================
    # OpenRouter API Settings
    # ================================================
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    NEMOTRON_MODEL = "nvidia/llama-3.1-nemotron-70b-instruct"
    
    # ================================================
    # Upload Settings
    # ================================================
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # ================================================
    # Medical Feature Definitions
    # ================================================
    ALL_FEATURES = [
        'age', 'sex', 'chest pain type', 'resting bp s', 'cholesterol',
        'fasting blood sugar', 'resting ecg', 'max heart rate',
        'exercise angina', 'oldpeak', 'ST slope'
    ]

    FEATURES_MINIMAL = ['ST slope', 'exercise angina', 'chest pain type', 'oldpeak']
    FEATURES_TOP8 = ['ST slope', 'chest pain type', 'exercise angina', 'oldpeak',
                     'max heart rate', 'sex', 'fasting blood sugar', 'cholesterol']
    FEATURES_ALL11 = ALL_FEATURES

    FEATURES_AR = {
        'age': 'العمر', 'sex': 'الجنس', 'chest pain type': 'نوع ألم الصدر',
        'resting bp s': 'ضغط الدم الانقباضي', 'cholesterol': 'الكوليسترول',
        'fasting blood sugar': 'سكر الدم الصائم', 'resting ecg': 'تخطيط القلب',
        'max heart rate': 'أقصى معدل لضربات القلب', 'exercise angina': 'ذبحة أثناء الجهد',
        'oldpeak': 'انخفاض ST', 'ST slope': 'ميل مقطع ST'
    }

    # ================================================
    # Clinical Models Information
    # ================================================
    MODELS_INFO = {
        'minimal': {
            'name': 'النموذج المبسط', 'display_name': 'النموذج المبسط (4 ميزات)',
            'features': FEATURES_MINIMAL, 'n_features': 4,
            'model_type': 'Logistic Regression', 'accuracy': None,
            'icon': '⚡', 'color': '#3498db',
            'desc': 'أسرع نموذج - يستخدم 4 ميزات فقط',
            'model_file': 'Set6_Minimal_Logistic Regression.pkl',
            'scaler_file': 'Set6_Minimal_Logistic Regression_scaler.pkl'
        },
        'top8': {
            'name': 'النموذج المتوسط', 'display_name': 'النموذج المتوسط (8 ميزات)',
            'features': FEATURES_TOP8, 'n_features': 8,
            'model_type': 'Random Forest', 'accuracy': None,
            'icon': '⭐', 'color': '#f39c12',
            'desc': 'نموذج متوازن - يستخدم 8 ميزات',
            'model_file': 'Set2_Top_8_Random Forest.pkl',
            'scaler_file': 'Set2_Top_8_Random Forest_scaler.pkl'
        },
        'all11': {
            'name': 'النموذج الشامل', 'display_name': 'النموذج الشامل (11 ميزة)',
            'features': FEATURES_ALL11, 'n_features': 11,
            'model_type': 'KNN', 'accuracy': None,
            'icon': '🏆', 'color': '#9b59b6',
            'desc': 'أعلى دقة - يستخدم جميع الميزات',
            'model_file': 'Set4_All_11_KNN.pkl',
            'scaler_file': 'Set4_All_11_KNN_scaler.pkl'
        }
    }

    # ================================================
    # ECG Models Information
    # ================================================
    ECG_MODELS_INFO = {
        'densenet_binary': {
            'name': 'DenseNet Binary', 'display_name': 'ECG - DenseNet (Normal/Abnormal)',
            'model_file': 'densenet_binary.onnx', 'type': 'onnx',
            'classes': ['Normal', 'Abnormal'], 'classes_ar': ['طبيعي', 'غير طبيعي'],
            'colors': ['#2ecc71', '#e74c3c'], 'accuracy': '~95%',
            'description': 'DenseNet121 - Binary', 'icon': '🧠', 'color': '#3498db'
        },
        'densenet_multiclass': {
            'name': 'DenseNet Multi-Class', 'display_name': 'ECG - DenseNet (3 Classes)',
            'model_file': 'densenet_3multiclass.onnx', 'type': 'onnx',
            'classes': ['Abnormal', 'Normal', 'History_MI'],
            'classes_ar': ['غير طبيعي', 'طبيعي', 'تاريخ مرضي'],
            'colors': ['#e74c3c', '#2ecc71', '#f39c12'], 'accuracy': '~94%',
            'description': 'DenseNet121 - 3-Class', 'icon': '🧬', 'color': '#9b59b6'
        },
        'onnx_original': {
            'name': 'ONNX Original', 'display_name': 'ECG - ONNX (4 Classes)',
            'model_file': 'ecg_median_model.onnx', 'type': 'onnx',
            'classes': ['Abnormal', 'MI', 'Normal', 'History_MI'],
            'classes_ar': ['غير طبيعي', 'احتشاء', 'طبيعي', 'تاريخ مرضي'],
            'colors': ['#e74c3c', '#ff0000', '#2ecc71', '#f39c12'], 'accuracy': '94.29%',
            'description': 'ONNX Median Filter - 4-Class', 'icon': '📊', 'color': '#e74c3c'
        }
    }

    # ================================================
    # Report Categories
    # ================================================
    REPORT_CATEGORIES = {
        'general': 'عام', 'cardiology': 'قلبية',
        'surgery': 'جراحة', 'laboratory': 'مخبرية',
    }

    # ================================================
    # Helper Methods
    # ================================================
    @classmethod
    def init_folders(cls):
        folders = [
            cls.DATA_FOLDER, cls.MODELS_PATH, cls.UPLOAD_FOLDER,
            cls.RESULTS_FOLDER, cls.REPORTS_FOLDER,
            cls.TEMPLATE_FOLDER, cls.STATIC_FOLDER,
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)