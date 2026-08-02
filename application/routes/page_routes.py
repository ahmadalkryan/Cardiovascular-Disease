# application/routes/page_routes.py
"""Page Routes - HTML page rendering"""

from flask import render_template
#from infrastructure.config import Config
from config import Config 


def register_page_routes(app, config):
    """Register all HTML page routes"""
    
    @app.route('/')
    def clinical_data():
        return render_template('clinical_data.html')
    
    @app.route('/diagnosis')
    def index():
        return render_template('index.html', models=Config.MODELS_INFO)
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/patients')
    def patients_page():
        return render_template('patients.html')
    
    @app.route('/models-info')
    def models_info_page():
        return render_template('models_info.html', ecg_model=Config.ECG_MODELS_INFO)
    
    @app.route('/ecg')
    def ecg_page():
        ecg_service = app.config.get('ecg_service')
        if ecg_service:
            available_models = ecg_service.get_available_models()
        else:
            available_models = []
        
        models_display = {}
        for key in available_models:
            if key in Config.ECG_MODELS_INFO:
                models_display[key] = Config.ECG_MODELS_INFO[key]
        
        return render_template(
            'ecg.html',
            ecg_models=models_display,
            available_models=available_models
        )
    
    @app.route('/batch-predict')
    def batch_predict_page():
        return render_template(
            'batch_predict.html',
            models=Config.MODELS_INFO,
            features=Config.FEATURES_AR
        )