
# config.py - Application Configuration (Root Level)
import os
from dotenv import load_dotenv 

load_dotenv()

class Config:
        
    # ================================================
    # Flask Settings 
    # ================================================
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        import warnings
        warnings.warn(
            "⚠️ SECRET_KEY not set in .env! Using default (NOT SAFE for production).",
            RuntimeWarning
        )
        SECRET_KEY = 'dev-secret-key-2024'
    
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
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
    # Database (دعم SQLite و PostgreSQL)
    # ================================================
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(STORAGE_FOLDER, "app.db")}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # ================================================
    # Patient Files 
    # ================================================
    PATIENT_FILES = {
        'minimal': os.path.join(DATA_FOLDER, 'patients_minimal.csv'),
        'top8': os.path.join(DATA_FOLDER, 'patients_top8.csv'),
        'all11': os.path.join(DATA_FOLDER, 'patients_all11.csv')
    }
    
    # ================================================
    # Upload Settings
    # ================================================
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16)) * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # ================================================
    # CORS Settings
    # ================================================
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000').split(',')
    
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
        'age': 'العمر', 'sex': 'الجنس',
        'chest pain type': 'نوع ألم الصدر',
        'resting bp s': 'ضغط الدم الانقباضي',
        'cholesterol': 'الكوليسترول',
        'fasting blood sugar': 'سكر الدم الصائم',
        'resting ecg': 'تخطيط القلب',
        'max heart rate': 'أقصى معدل لضربات القلب',
        'exercise angina': 'ذبحة أثناء الجهد',
        'oldpeak': 'انخفاض ST',
        'ST slope': 'ميل مقطع ST'
    }

    # ================================================
    # Clinical Models Information
    # ================================================
    MODELS_INFO = {
        'minimal': {
            'name': 'النموذج المبسط',
            'display_name': 'النموذج المبسط (4 ميزات)',
            'features': FEATURES_MINIMAL,
            'n_features': 4,
            'model_type': 'Logistic Regression',
            'accuracy': None,
            'icon': '⚡',
            'color': '#3498db',
            'desc': 'أسرع نموذج - يستخدم 4 ميزات فقط',
            'model_file': 'Set6_Minimal_Logistic Regression.pkl',
            'scaler_file': 'Set6_Minimal_Logistic Regression_scaler.pkl'
        },
        'top8': {
            'name': 'النموذج المتوسط',
            'display_name': 'النموذج المتوسط (8 ميزات)',
            'features': FEATURES_TOP8,
            'n_features': 8,
            'model_type': 'Random Forest',
            'accuracy': None,
            'icon': '⭐',
            'color': '#f39c12',
            'desc': 'نموذج متوازن - يستخدم 8 ميزات',
            'model_file': 'Set2_Top_8_Random Forest.pkl',
            'scaler_file': 'Set2_Top_8_Random Forest_scaler.pkl'
        },
        'all11': {
            'name': 'النموذج الشامل',
            'display_name': 'النموذج الشامل (11 ميزة)',
            'features': FEATURES_ALL11,
            'n_features': 11,
            'model_type': 'KNN',
            'accuracy': None,
            'icon': '🏆',
            'color': '#9b59b6',
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
            'name': 'DenseNet Binary',
            'display_name': 'ECG - (Normal/Abnormal)',
            'model_file': 'densenet_binary.onnx',
            'type': 'onnx',
            'classes': ['Normal', 'Abnormal'],
            'classes_ar': ['طبيعي', 'غير طبيعي'],
            'colors': ['#2ecc71', '#e74c3c'],
            'accuracy': '~95%',
            'description': 'DenseNet121 - Binary',
            'icon': '🧠',
            'color': '#3498db'
        },
        'densenet_multiclass': {
            'name': 'DenseNet Multi-Class',
            'display_name': 'ECG - (3 Classes)',
            'model_file': 'densenet_3multiclass.onnx',
            'type': 'onnx',
            'classes': ['Abnormal', 'Normal', 'History_MI'],
            'classes_ar': ['غير طبيعي', 'طبيعي', 'تاريخ مرضي'],
            'colors': ['#e74c3c', '#2ecc71', '#f39c12'],
            'accuracy': '~94%',
            'description': 'DenseNet121 - 3-Class',
            'icon': '🧬',
            'color': '#9b59b6'
        },
        'onnx_original': {
            'name': 'ONNX Original',
            'display_name': 'ECG -  (4 Classes)',
            'model_file': 'ecg_median_model.onnx',
            'type': 'onnx',
            'classes': ['Abnormal', 'MI', 'Normal', 'History_MI'],
            'classes_ar': ['غير طبيعي', 'احتشاء', 'طبيعي', 'تاريخ مرضي'],
            'colors': ['#e74c3c', '#ff0000', '#2ecc71', '#f39c12'],
            'accuracy': '94.29%',
            'description': 'ONNX Median Filter - 4-Class',
            'icon': '📊',
            'color': '#e74c3c'
        }
    }

    # ================================================
    # Logging Settings
    # ================================================
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES', 10)) * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 5))
    ERROR_LOG_BACKUP_COUNT = int(os.environ.get('ERROR_LOG_BACKUP_COUNT', 3))
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    
    # ================================================
    # Report Categories
    # ================================================
    REPORT_CATEGORIES = {
        'general': 'عام',
        'cardiology': 'قلبية',
        'surgery': 'جراحة',
        'laboratory': 'مخبرية',
    }

    # ================================================
    # Helper Methods
    # ================================================
    @classmethod
    def init_folders(cls):
        """Create all required folders"""
        folders = [
            cls.DATA_FOLDER,
            cls.MODELS_PATH,
            cls.UPLOAD_FOLDER,
            cls.RESULTS_FOLDER,
            cls.REPORTS_FOLDER,
            cls.TEMPLATE_FOLDER,
            cls.STATIC_FOLDER,
            cls.LOG_DIR,
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate configuration settings"""
        if cls.SECRET_KEY == 'dev-secret-key-2024':
            print("⚠️ WARNING: Using default SECRET_KEY. Set it in .env for production.")
        
        if cls.DEBUG:
            print("⚠️ WARNING: DEBUG mode is ON. Disable in production.")
        
        
        for model_key, model_info in cls.MODELS_INFO.items():
            model_path = os.path.join(cls.MODELS_PATH, model_info['model_file'])
            if not os.path.exists(model_path):
                print(f"⚠️ WARNING: Model file not found: {model_path}")
        
        print("✅ Configuration validated")