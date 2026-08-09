
# app.py - Application Entry Point
import os
import sys
import joblib
import logging
import time
import uuid
from flask import Flask, g, request
from logging.handlers import RotatingFileHandler 
from flask_cors import CORS
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from business.services import DataService, ECGService, PredictionService
from business.services.report_service import ReportService
from infrastructure.database import init_db
from application.routes import register_routes
from application.routes.report_routes import register_report_routes
from application.exceptions import register_exception_handlers  
from application.routes.settings_routes import register_settings_routes


# ═══════════════════════════════════════════
# Setup Logging
# ═══════════════════════════════════════════

os.makedirs(Config.LOG_DIR, exist_ok=True)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler = RotatingFileHandler(
    os.path.join(Config.LOG_DIR, 'app.log'),
    maxBytes=Config.LOG_MAX_BYTES,
    backupCount=Config.LOG_BACKUP_COUNT,
    encoding='utf-8'
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

error_handler = RotatingFileHandler(
    os.path.join(Config.LOG_DIR, 'errors.log'),
    maxBytes=Config.LOG_MAX_BYTES,
    backupCount=Config.ERROR_LOG_BACKUP_COUNT,
    encoding='utf-8'
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

root_logger = logging.getLogger()
if root_logger.handlers:
    root_logger.handlers.clear()

root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)
root_logger.addHandler(error_handler)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)


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


register_exception_handlers(app)


Config.init_folders()
init_db(app)


# ═══════════════════════════════════════════
#  Request Timing Logging
# ═══════════════════════════════════════════

@app.before_request
def before_request():
   
    g.start_time = time.time()
    g.request_id = str(uuid.uuid4())[:8]


@app.after_request
def after_request(response):
   
    elapsed_time = time.time() - g.start_time
    status_code = response.status_code
    
    log_message = (
        f"⏱️ {request.method} {request.path} "
        f"→ {status_code} "
        f"({elapsed_time*1000:.2f}ms) "
        f"[ID: {g.request_id}]"
    )
    
    if status_code >= 500:
        logger.error(log_message)
    elif status_code >= 400:
        logger.warning(log_message)
    else:
        logger.info(log_message)
    
    return response


# ═══════════════════════════════════════════
# Load Models
# ═══════════════════════════════════════════
logger.info("Loading models...")
models_loaded, scalers_loaded = {}, {}

for model_key, model_info in Config.MODELS_INFO.items():
    model_path = os.path.join(Config.MODELS_PATH, model_info['model_file'])
    scaler_path = os.path.join(Config.MODELS_PATH, model_info['scaler_file'])
    try:
        models_loaded[model_key] = joblib.load(model_path)
        scalers_loaded[model_key] = joblib.load(scaler_path)
        logger.info(f"✅ Loaded {model_info['display_name']}")
    except FileNotFoundError:
        logger.error(f"❌ Failed: {model_info['display_name']} - File not found")
        models_loaded[model_key] = None
        scalers_loaded[model_key] = None


# ═══════════════════════════════════════════
# Initialize Services
# ═══════════════════════════════════════════

data_service = DataService(Config.DATA_FOLDER, Config.PATIENT_FILES)
prediction_service = PredictionService(models_loaded, scalers_loaded)
report_service = ReportService(Config.REPORTS_FOLDER)

ecg_service = ECGService(models_path=Config.ECG_MODELS_PATH)
app.config['ecg_service'] = ecg_service


try:
    from business.services.setting_service import SettingService
    with app.app_context():
        SettingService.init_default_settings()
        logger.info("✅ Settings initialized")
except ImportError:
    logger.warning("⚠️ SettingService not found, skipping settings initialization")


# ═══════════════════════════════════════════
# ✅ Register Routes
# ═══════════════════════════════════════════

register_routes(app, data_service, prediction_service, Config, ecg_service)
register_report_routes(app, report_service)

try:
    register_settings_routes(app)
    logger.info("✅ Settings routes registered")
except NameError:
    logger.warning("⚠️ Settings routes not found, skipping")



# ═══════════════════════════════════════════
# Run
# ═══════════════════════════════════════════
if __name__ == '__main__':
    logger.info("🚀 Starting Flask server on port 5000...")
    print("\n" + "=" * 60)
    print("🫀 Heart Disease Diagnosis System v2.0")
    print("=" * 60)
    print(" Data Source:")
    print("    Patients: CSV files (storage/data/)")
    print("    Templates: SQLite (storage/app.db)")
    print("    Reports: SQLite (storage/app.db)")
    print("=" * 60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)