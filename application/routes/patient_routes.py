# application/routes/patient_routes.py
"""Patient Management Routes - Patient data and statistics"""

from flask import request, jsonify, send_file
import pandas as pd
import io
from datetime import datetime
import os
#from infrastructure.config import Config
from config import Config 


def register_patient_routes(app, data_service, prediction_service, config):
    """Register patient management routes"""
    
    @app.route('/api/statistics', methods=['GET'])
    def get_statistics_api():
        try:
            stats = data_service.get_statistics()
            return jsonify({'success': True, 'statistics': stats})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/patients', methods=['GET'])
    def get_patients_api():
        try:
            model_filter = request.args.get('model', None)
            df = data_service.get_patients_data(model_filter)
            
            if df.empty:
                return jsonify({'success': True, 'count': 0, 'patients': []})
            
            patients = data_service.clean_data_for_json(df)
            
            return jsonify({
                'success': True,
                'count': len(patients),
                'patients': patients
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/patients/count', methods=['GET'])
    def get_patients_count_api():
        try:
            counts = {}
            for model in Config.MODELS_INFO.keys():
                file_path = Config.PATIENT_FILES[model]
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
                    counts[model] = len(df)
                else:
                    counts[model] = 0
            
            return jsonify({
                'success': True,
                'counts': counts,
                'total': sum(counts.values())
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/patients/export', methods=['GET'])
    def export_patients():
        try:
            model_filter = request.args.get('model', None)
            df = data_service.get_patients_data(model_filter)
            
            if df.empty:
                return jsonify({'success': False, 'error': 'No data to export'}), 404
            
            df = df.fillna('')
            
            output = io.StringIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8-sig')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'patients_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            )
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500


def register_ai_status_route(app, ai_service):
    """Register AI service status route"""
    
    @app.route('/api/ai-status', methods=['GET'])
    def ai_status():
        try:
            return jsonify({
                'ai_available': ai_service.available if ai_service else False,
                'ai_model': ai_service.model_name if ai_service and ai_service.available else None,
                'message': 'AI model is working' if ai_service and ai_service.available else 'Connecting to AI model...'
            })
        except Exception as e:
            return jsonify({
                'ai_available': False,
                'ai_model': None,
                'message': f'Error: {str(e)}'
            })