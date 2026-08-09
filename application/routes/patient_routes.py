
# application/routes/patient_routes.py
"""Patient Management Routes - Patient data from CSV files only"""

from flask import request, jsonify, send_file
import pandas as pd
import io
from datetime import datetime
import os
import logging

from config import Config
from application.exceptions import ValidationError, PatientNotFoundError

logger = logging.getLogger(__name__)


def register_patient_routes(app, data_service, prediction_service, config):
    """Register patient management routes (CSV only)"""
    
    # ================================================
    # Statistics
    # ================================================
    
    @app.route('/api/statistics', methods=['GET'])
    def get_statistics_api():
        """Get patient statistics from CSV"""
        try:
            stats = data_service.get_statistics()
            return jsonify({'success': True, 'statistics': stats})
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ================================================
    # Get Patients (with filtering)
    # ================================================
    
    @app.route('/api/patients', methods=['GET'])
    def get_patients_api():
        """Get all patients from CSV"""
        try:
            model_filter = request.args.get('model', None)
            
          
            patients = data_service.get_all_patients(model_filter)
            
            return jsonify({
                'success': True,
                'count': len(patients),
                'patients': patients
            })
        except Exception as e:
            logger.error(f"Error getting patients: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ================================================
    # Get Single Patient by ID
    # ================================================
    
    @app.route('/api/patients/<patient_id>', methods=['GET'])
    def get_patient_api(patient_id):
        """Get a single patient by ID from CSV"""
        try:
            patient = data_service.get_patient(patient_id)
            
            if not patient:
                raise PatientNotFoundError(patient_id)
            
            # ✅ Convert dict to response
            return jsonify({
                'success': True,
                'patient': patient
            })
        except PatientNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting patient {patient_id}: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ================================================
    # Get Single Patient by UID
    # ================================================
    
    @app.route('/api/patients/uid/<patient_uid>', methods=['GET'])
    def get_patient_by_uid_api(patient_uid):
        """Get a single patient by UID from CSV"""
        try:
            patient = data_service.get_patient_by_uid(patient_uid)
            
            if not patient:
                raise PatientNotFoundError(patient_uid)
            
            return jsonify({
                'success': True,
                'patient': patient
            })
        except PatientNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting patient by UID {patient_uid}: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ================================================
    # Get Recent Patients
    # ================================================
    
    @app.route('/api/patients/recent', methods=['GET'])
    def get_recent_patients_api():
        """Get recent patients from CSV"""
        try:
            limit = request.args.get('limit', 10, type=int)
            
            
            if limit > 100:
                limit = 100
            
            patients = data_service.get_recent_patients(limit)
            
            return jsonify({
                'success': True,
                'count': len(patients),
                'patients': patients
            })
        except Exception as e:
            logger.error(f"Error getting recent patients: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ================================================
    # Get Patient Counts by Model
    # ================================================
    
    @app.route('/api/patients/count', methods=['GET'])
    def get_patients_count_api():
        """Get patient counts from CSV files"""
        try:
            counts = {}
            total = 0
            
            for model in Config.MODELS_INFO.keys():
                file_path = Config.PATIENT_FILES[model]
                if os.path.exists(file_path):
                    try:
                        df = pd.read_csv(file_path, encoding='utf-8-sig')
                        counts[model] = len(df)
                        total += len(df)
                    except Exception as e:
                        logger.warning(f"Error reading {file_path}: {e}")
                        counts[model] = 0
                else:
                    counts[model] = 0
            
            return jsonify({
                'success': True,
                'counts': counts,
                'total': total
            })
        except Exception as e:
            logger.error(f"Error getting patient counts: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ================================================
    # Export Patients to CSV
    # ================================================
    
    @app.route('/patients/export', methods=['GET'])
    def export_patients():
        """Export patients to CSV"""
        try:
            model_filter = request.args.get('model', None)
            df = data_service.get_patients_data(model_filter)
            
            if df.empty:
                raise ValidationError("لا توجد بيانات للتصدير")
            
            df = df.fillna('')
            
            output = io.StringIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            
          
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'patients_{timestamp}.csv'
            if model_filter:
                filename = f'patients_{model_filter}_{timestamp}.csv'
            
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8-sig')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error exporting patients: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500