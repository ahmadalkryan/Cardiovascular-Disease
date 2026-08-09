# application/routes/batch_routes.py
"""Batch Prediction Routes - File upload for bulk predictions"""

from flask import request, jsonify, send_file
import pandas as pd
import io
from datetime import datetime
import os
import numpy as np
import logging
from werkzeug.utils import secure_filename

from config import Config
from application.exceptions import (
    FileUploadError,
    InvalidFileTypeError,
    ValidationError,
    ModelNotFoundError,
    PatientDataValidationError,
    FileNotFoundError
)

logger = logging.getLogger(__name__)


def register_batch_routes(app, prediction_service, data_service, config):
    """Register batch prediction routes"""
    
    def read_uploaded_file(file):
        """Helper function to read uploaded file based on its extension"""
        filename = file.filename.lower()
        try:
            if filename.endswith('.csv'):
                try:
                    return pd.read_csv(file.stream, encoding='utf-8')
                except UnicodeDecodeError:
                    file.stream.seek(0)
                    return pd.read_csv(file.stream, encoding='latin-1')
            elif filename.endswith('.xlsx'):
                return pd.read_excel(file.stream, engine='openpyxl')
            elif filename.endswith('.xls'):
                try:
                    return pd.read_excel(file.stream, engine='xlrd')
                except ImportError:
                    file.stream.seek(0)
                    try:
                        return pd.read_excel(file.stream, engine='openpyxl')
                    except Exception:
                        raise ValidationError(
                            "Cannot read .xls files. Please install xlrd >= 2.0.1 "
                            "or convert your file to .xlsx or .csv format."
                        )
            else:
                raise InvalidFileTypeError(filename, ['.csv', '.xlsx', '.xls'])
        except Exception as e:
            raise ValidationError(f"Error reading file: {str(e)}")
    
    def save_uploaded_file(file):
        """Save the uploaded file to storage/uploads/"""
        try:
            original_filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(original_filename)
            saved_filename = f"{name}_{timestamp}{ext}"
            saved_filepath = os.path.join(Config.UPLOAD_FOLDER, saved_filename)
            
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            file.save(saved_filepath)
            logger.info(f"✅ Uploaded file saved: {saved_filepath}")
            
            return saved_filename, saved_filepath
        except Exception as e:
            logger.error(f"Failed to save uploaded file: {e}")
            raise FileUploadError(str(e))
    
    @app.route('/api/batch-predict', methods=['POST'])
    def batch_predict():
        """Batch prediction API endpoint"""
        # Validate file presence
        if 'file' not in request.files:
            raise FileUploadError("لم يتم رفع ملف")
        
        file = request.files['file']
        if file.filename == '':
            raise FileUploadError("اسم الملف فارغ")
        
        # Get model name
        model_name = request.form.get('model', 'top8')
        
        # Validate model exists
        if model_name not in Config.MODELS_INFO:
            raise ModelNotFoundError(model_name)
        
        # Save uploaded file
        saved_filename, saved_filepath = save_uploaded_file(file)
        
        # Read file for prediction
        file.stream.seek(0)
        df = read_uploaded_file(file)
        
        if df.empty:
            raise ValidationError("الملف فارغ. يرجى رفع ملف يحتوي على بيانات")
        
        # Perform batch prediction
        results, error = prediction_service.batch_predict(
            df, model_name, data_service=None, auto_save=False
        )
        
        if error:
            raise ValidationError(error)
        
        # Calculate statistics
        successful = len([r for r in results if 'error' not in r])
        failed = len(results) - successful
        disease_count = len([r for r in results if r.get('prediction') == 1])
        healthy_count = len([r for r in results if r.get('prediction') == 0])
        
        probabilities = [
            r.get('probability', 0)
            for r in results
            if 'error' not in r and 'probability' in r
        ]
        avg_risk = np.mean(probabilities) * 100 if probabilities else 0
        
        can_save_all = all(
            r.get('can_save', False)
            for r in results
            if 'error' not in r
        )
        
        return jsonify({
            'success': True,
            'total_records': len(df),
            'successful': successful,
            'failed': failed,
            'disease_count': disease_count,
            'healthy_count': healthy_count,
            'avg_risk_percent': f"{avg_risk:.1f}%",
            'results': results,
            'model_used': Config.MODELS_INFO[model_name]['display_name'],
            'model_key': model_name,
            'can_save_all': can_save_all,
            'uploaded_file': {
                'original_name': file.filename,
                'saved_name': saved_filename,
                'saved_path': saved_filepath
            }
        })
    
    @app.route('/api/batch-save-all', methods=['POST'])
    def batch_save_all():
        """Save all batch prediction results at once"""
        data = request.get_json()
        if not data:
            raise ValidationError("لا توجد بيانات")
        
        model_name = data.get('model_name', 'top8')
        results = data.get('results', [])
        
        if not results:
            raise ValidationError("لا توجد نتائج للحفظ")
        
        # Filter valid results
        valid_results = [
            r for r in results
            if 'error' not in r and r.get('can_save', False)
        ]
        
        if not valid_results:
            raise ValidationError("لا توجد نتائج صالحة للحفظ")
        
        # Get model features
        _, model_features, _ = prediction_service.get_model_and_features(model_name)
        
        saved_count = 0
        modified_count = 0
        saved_ids = []
        failed_count = 0
        
        # Save each patient
        for result in valid_results:
            try:
                patient_data = result.get('patient_data', {})
                prediction = result.get('prediction', 0)
                probability = result.get('probability', 0)
                doctor_modified = result.get('doctor_modified', False)
                doctor_prediction = result.get('doctor_prediction', prediction)
                
                final_prediction = doctor_prediction if doctor_modified else prediction
                
                if doctor_modified:
                    modified_count += 1
                
                patient_id = data_service.save_patient_data(
                    patient_data,
                    final_prediction,
                    probability,
                    model_name,
                    model_features
                )
                
                if patient_id:
                    saved_ids.append({
                        'row_index': result.get('row_index'),
                        'patient_id': patient_id,
                        'modified': doctor_modified
                    })
                    saved_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                failed_count += 1
                logger.error(f"Error saving row {result.get('row_index')}: {e}")
        
        # Save results summary
        try:
            os.makedirs(Config.RESULTS_FOLDER, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_filename = f'batch_results_{timestamp}.csv'
            results_path = os.path.join(Config.RESULTS_FOLDER, results_filename)
            
            results_data = []
            for result in valid_results:
                row_data = {
                    'row_index': result.get('row_index'),
                    'patient_id': next(
                        (sid['patient_id'] for sid in saved_ids
                         if sid['row_index'] == result.get('row_index')),
                        'FAILED'
                    ),
                    'prediction': result.get('prediction'),
                    'result': result.get('result_ar', ''),
                    'probability_percent': result.get('probability_percent', ''),
                    'risk_level': result.get('risk_level_ar', ''),
                    'doctor_modified': result.get('doctor_modified', False),
                }
                patient_data = result.get('patient_data', {})
                for key, value in patient_data.items():
                    row_data[key] = value
                results_data.append(row_data)
            
            results_df = pd.DataFrame(results_data)
            results_df.to_csv(results_path, index=False, encoding='utf-8-sig')
            logger.info(f"✅ Batch results saved: {results_path}")
            
        except Exception as e:
            logger.error(f"Error saving batch results file: {e}")
            results_path = None
            results_filename = None
        
        return jsonify({
            'success': True,
            'total_saved': saved_count,
            'total_modified': modified_count,
            'total_failed': failed_count,
            'saved_ids': saved_ids,
            'results_file': results_filename,
            'download_url': f'/api/download-batch-results/{results_filename}' if results_filename else None,
            'message': (
                f'تم حفظ {saved_count} مريض بنجاح' +
                (f' (منها {modified_count} معدلة بواسطة الطبيب)' if modified_count > 0 else '') +
                (f' | فشل: {failed_count}' if failed_count > 0 else '')
            )
        })
    
    @app.route('/api/download-batch-results/<filename>', methods=['GET'])
    def download_batch_results(filename):
        """Download batch prediction results CSV"""
        filename = os.path.basename(filename)
        file_path = os.path.join(Config.RESULTS_FOLDER, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(filename)
        
        return send_file(
            file_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'prediction_results_{filename}'
        )
    
    @app.route('/api/batch-template', methods=['GET'])
    def download_batch_template():
        """Download a template CSV file for batch prediction"""
        model_name = request.args.get('model', 'top8')
        
        if model_name not in Config.MODELS_INFO:
            raise ModelNotFoundError(model_name)
        
        # Select feature set based on model
        if model_name == 'minimal':
            features = Config.FEATURES_MINIMAL
        elif model_name == 'top8':
            features = Config.FEATURES_TOP8
        else:
            features = Config.FEATURES_ALL11
        
        # Create sample row
        sample_row = {
            'age': 55, 'sex': 1, 'chest pain type': 4,
            'resting bp s': 120, 'cholesterol': 200,
            'fasting blood sugar': 0, 'resting ecg': 0,
            'max heart rate': 150, 'exercise angina': 0,
            'oldpeak': 0.6, 'ST slope': 2
        }
        
        filtered_sample = {k: v for k, v in sample_row.items() if k in features}
        template_df = pd.DataFrame([filtered_sample])
        
        # Add 5 empty rows
        for _ in range(5):
            template_df = pd.concat([
                template_df,
                pd.DataFrame([{f: '' for f in features}])
            ], ignore_index=True)
        
        output = io.StringIO()
        template_df.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'template_{model_name}_{datetime.now().strftime("%Y%m%d")}.csv'
        )