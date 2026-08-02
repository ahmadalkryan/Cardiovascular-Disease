# # app.py - Application Entry Point

# import os
# import sys
# import joblib
# from flask import Flask
# from flask_cors import CORS

# # Add project root to path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # Import configuration from root config.py
# from config import Config

# # Import services from business layer
# from business.services import (
#     AIService,
#     DataService,
#     ECGService,
#     PredictionService
# )
# from business.services.report_service import ReportService

# # Import database
# from infrastructure.database import init_db

# # Import routes from application layer
# from application.routes import register_routes
# from application.routes.report_routes import register_report_routes

# # ================================================
# # Create Flask Application
# # ================================================
# app = Flask(
#     __name__,
#     static_folder=Config.STATIC_FOLDER,      # presentation/static/
#     static_url_path='/static',
#     template_folder=Config.TEMPLATE_FOLDER    # presentation/templates/
# )
# app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(Config.STORAGE_FOLDER, "app.db")}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = Config.SECRET_KEY
# CORS(app)

# # Create required folders
# Config.init_folders()

# # Initialize Database
# init_db(app)

# # ================================================
# # Load Clinical Models from storage/models/
# # ================================================
# print("=" * 60)
# print("📂 Loading clinical models...")
# print("=" * 60)

# models_loaded = {}
# scalers_loaded = {}

# for model_key, model_info in Config.MODELS_INFO.items():
#     model_file = model_info['model_file']
#     scaler_file = model_info['scaler_file']
    
#     model_path = os.path.join(Config.MODELS_PATH, model_file)
#     scaler_path = os.path.join(Config.MODELS_PATH, scaler_file)
    
#     try:
#         models_loaded[model_key] = joblib.load(model_path)
#         scalers_loaded[model_key] = joblib.load(scaler_path)
#         print(f"✅ Loaded {model_info['display_name']}")
#     except FileNotFoundError as e:
#         print(f"❌ Failed to load {model_info['display_name']}: {e}")
#         models_loaded[model_key] = None
#         scalers_loaded[model_key] = None

# # ================================================
# # Load ECG Models from storage/models/
# # ================================================
# print("\n" + "=" * 60)
# print("📂 Loading ECG models...")
# print("=" * 60)

# ecg_service = ECGService(models_path=Config.ECG_MODELS_PATH)
# app.config['ecg_service'] = ecg_service

# # ================================================
# # Initialize Services
# # ================================================
# ai_service = AIService(
#     api_key=Config.OPENROUTER_API_KEY,
#     api_url=Config.OPENROUTER_API_URL,
#     model_name=Config.NEMOTRON_MODEL
# )

# data_service = DataService(
#     data_folder=Config.DATA_FOLDER,
#     patient_files=Config.PATIENT_FILES
# )

# prediction_service = PredictionService(
#     models_loaded=models_loaded,
#     scalers_loaded=scalers_loaded
# )

# # Initialize Report Service
# report_service = ReportService(
#     reports_folder=os.path.join(Config.STORAGE_FOLDER, 'reports')
# )

# # ================================================
# # Register Routes
# # ================================================
# register_routes(app, ai_service, data_service, prediction_service, Config, ecg_service)
# register_report_routes(app, report_service)

# # ================================================
# # Run Application
# # ================================================
# if __name__ == '__main__':
#     print("\n" + "=" * 60)
#     print("❤️  Heart Disease Diagnosis System")
#     print("=" * 60)
    
#     stats = data_service.get_statistics()
#     print(f"\n📊 Current Statistics:")
#     print(f"   Total patients: {stats['total']}")
#     print(f"   Disease cases: {stats['disease']}")
#     print(f"   Healthy cases: {stats['healthy']}")
#     print(f"   Average risk: {stats['avg_probability']:.1f}%")
    
#     print("\n📍 Available Pages:")
#     print("   http://localhost:5000/              - Clinical Data (Home)")
#     print("   http://localhost:5000/diagnosis      - Individual Diagnosis")
#     print("   http://localhost:5000/batch-predict  - Batch Prediction")
#     print("   http://localhost:5000/dashboard      - Dashboard")
#     print("   http://localhost:5000/patients       - Patients List")
#     print("   http://localhost:5000/models-info    - Models Info")
#     print("   http://localhost:5000/ecg            - ECG Analysis")
#     print("   http://localhost:5000/reports        - Medical Reports")
#     print("   http://localhost:5000/reports/builder - Template Builder")
    
#     print("\n📋 Loaded Clinical Models:")
#     for model_key, model_info in Config.MODELS_INFO.items():
#         status = "✅" if models_loaded.get(model_key) is not None else "❌"
#         print(f"   {status} {model_info['display_name']} ({model_info['model_type']})")
    
#     print("\n📋 Available ECG Models:")
#     available = ecg_service.get_available_models()
#     for model_key in available:
#         if model_key in Config.ECG_MODELS_INFO:
#             info = Config.ECG_MODELS_INFO[model_key]
#             print(f"   ✅ {info['display_name']} ({info['accuracy']})")
    
#     if ai_service.available:
#         print(f"\n🤖 AI Service: Active - {ai_service.model_name}")
#     else:
#         print("\n⚠️  AI Service: Inactive")
    
#     print(f"\n📄 Reports System: Active (SQLite DB)")
#     print(f"   Templates and reports stored in: {Config.STORAGE_FOLDER}/app.db")
    
#     print("\n🚀 Starting Flask server...")
#     print("=" * 60)
    
#     app.run(host='0.0.0.0', port=5000, debug=True)



# app.py - Application Entry Point

import os
import sys
import joblib
from flask import Flask
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from business.services import AIService, DataService, ECGService, PredictionService
from business.services.report_service import ReportService
from infrastructure.database import init_db
from application.routes import register_routes
from application.routes.report_routes import register_report_routes

# ═══════════════════════════════════════════
# Create Flask Application
# ═══════════════════════════════════════════
app = Flask(
    __name__,
    static_folder=Config.STATIC_FOLDER,
    static_url_path='/static',
    template_folder=Config.TEMPLATE_FOLDER
)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
CORS(app)

Config.init_folders()
init_db(app)

# ═══════════════════════════════════════════
# Load Models
# ═══════════════════════════════════════════
models_loaded, scalers_loaded = {}, {}

for model_key, model_info in Config.MODELS_INFO.items():
    model_path = os.path.join(Config.MODELS_PATH, model_info['model_file'])
    scaler_path = os.path.join(Config.MODELS_PATH, model_info['scaler_file'])
    try:
        models_loaded[model_key] = joblib.load(model_path)
        scalers_loaded[model_key] = joblib.load(scaler_path)
        print(f"✅ Loaded {model_info['display_name']}")
    except FileNotFoundError:
        print(f"❌ Failed: {model_info['display_name']}")
        models_loaded[model_key] = None
        scalers_loaded[model_key] = None

ecg_service = ECGService(models_path=Config.ECG_MODELS_PATH)
app.config['ecg_service'] = ecg_service

# ═══════════════════════════════════════════
# Initialize Services
# ═══════════════════════════════════════════
ai_service = AIService(Config.OPENROUTER_API_KEY, Config.OPENROUTER_API_URL, Config.NEMOTRON_MODEL)
data_service = DataService(Config.DATA_FOLDER, Config.PATIENT_FILES)
prediction_service = PredictionService(models_loaded, scalers_loaded)
report_service = ReportService(Config.REPORTS_FOLDER)

# ═══════════════════════════════════════════
# Register Routes
# ═══════════════════════════════════════════
register_routes(app, ai_service, data_service, prediction_service, Config, ecg_service)
register_report_routes(app, report_service)

# ═══════════════════════════════════════════
# Run
# ═══════════════════════════════════════════
if __name__ == '__main__':
    print(f"\ Starting Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)