# application/routes/batch_routes.py
"""Batch Prediction Routes - File upload for bulk predictions"""

from flask import request, jsonify, send_file
import pandas as pd
import io
from datetime import datetime
import os
import numpy as np
from werkzeug.utils import secure_filename

#from infrastructure.config import Config
from config import Config 

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
                        raise ImportError(
                            "Cannot read .xls files. Please install xlrd >= 2.0.1 "
                            "or convert your file to .xlsx or .csv format."
                        )
            else:
                raise ValueError(f"Unsupported file format. Please upload .csv, .xlsx, or .xls files.")
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
    
    def save_uploaded_file(file):
        """
        Save the uploaded file to storage/uploads/
        
        Args:
            file: Flask FileStorage object
            
        Returns:
            tuple: (saved_filename, saved_filepath) or (None, None) if failed
        """
        try:
            # Secure the filename and add timestamp to avoid conflicts
            original_filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(original_filename)
            saved_filename = f"{name}_{timestamp}{ext}"
            saved_filepath = os.path.join(Config.UPLOAD_FOLDER, saved_filename)
            
            # Ensure upload folder exists
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            
            # Save the file
            file.save(saved_filepath)
            print(f"✅ Uploaded file saved: {saved_filepath}")
            
            return saved_filename, saved_filepath
        except Exception as e:
            print(f"❌ Error saving uploaded file: {e}")
            return None, None
    
    @app.route('/api/batch-predict', methods=['POST'])
    def batch_predict():
        """
        Batch prediction API endpoint - Predicts WITHOUT auto-saving.
        Saves the uploaded file to storage/uploads/ and returns results for review.
        """
        try:
            # Validate file presence
            if 'file' not in request.files:
                return jsonify({'success': False, 'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'Empty filename'}), 400
            
            # Get model name from request (default: top8)
            model_name = request.form.get('model', 'top8')
            
            # Validate model exists
            if model_name not in Config.MODELS_INFO:
                return jsonify({
                    'success': False,
                    'error': f'Model "{model_name}" not found. Available: {", ".join(Config.MODELS_INFO.keys())}'
                }), 400
            
            # ✅ 1. Save the uploaded file to storage/uploads/
            saved_filename, saved_filepath = save_uploaded_file(file)
            
            # ✅ 2. Reset file stream and read for prediction
            file.stream.seek(0)
            try:
                df = read_uploaded_file(file)
            except ValueError as ve:
                return jsonify({'success': False, 'error': str(ve)}), 400
            
            # Validate file is not empty
            if df.empty:
                return jsonify({'success': False, 'error': 'File is empty. Please upload a file with data.'}), 400
            
            # ✅ 3. Perform batch prediction WITHOUT auto-saving
            results, error = prediction_service.batch_predict(
                df, model_name, data_service=None, auto_save=False
            )
            
            # Handle prediction error
            if error:
                return jsonify({'success': False, 'error': error}), 400
            
            # Calculate statistics
            successful = len([r for r in results if 'error' not in r])
            failed = len(results) - successful
            disease_count = len([r for r in results if r.get('prediction') == 1])
            healthy_count = len([r for r in results if r.get('prediction') == 0])
            
            # Calculate average risk percentage safely
            probabilities = [
                r.get('probability', 0)
                for r in results
                if 'error' not in r and 'probability' in r
            ]
            avg_risk = np.mean(probabilities) * 100 if probabilities else 0
            
            # Check if all can be saved
            can_save_all = all(
                r.get('can_save', False)
                for r in results
                if 'error' not in r
            )
            
            # Return success response with file info
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
            
        except Exception as e:
            print(f"❌ Batch prediction error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': 'An unexpected error occurred during batch prediction.'
            }), 500
    
    @app.route('/api/batch-save-all', methods=['POST'])
    def batch_save_all():
        """
        Save all batch prediction results at once.
        Each patient is saved to storage/data/patients_{model}.csv
        Results summary is saved to storage/uploads/batch_results/
        """
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
            
            model_name = data.get('model_name', 'top8')
            results = data.get('results', [])
            
            if not results:
                return jsonify({'success': False, 'error': 'No results to save'}), 400
            
            # Filter valid results
            valid_results = [
                r for r in results
                if 'error' not in r and r.get('can_save', False)
            ]
            
            if not valid_results:
                return jsonify({
                    'success': False,
                    'error': 'No valid results to save'
                }), 400
            
            # Get model features
            _, model_features, _ = prediction_service.get_model_and_features(model_name)
            
            saved_count = 0
            modified_count = 0
            saved_ids = []
            failed_count = 0
            
            # ✅ 1. Save each patient to storage/data/patients_{model}.csv
            for result in valid_results:
                try:
                    patient_data = result.get('patient_data', {})
                    prediction = result.get('prediction', 0)
                    probability = result.get('probability', 0)
                    doctor_modified = result.get('doctor_modified', False)
                    doctor_prediction = result.get('doctor_prediction', prediction)
                    
                    # Use doctor's prediction if modified
                    final_prediction = doctor_prediction if doctor_modified else prediction
                    
                    if doctor_modified:
                        modified_count += 1
                    
                    # Save individual patient to CSV
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
                    print(f"❌ Error saving row {result.get('row_index')}: {e}")
            
            # ✅ 2. Save results summary to storage/uploads/batch_results/
            try:
                os.makedirs(Config.RESULTS_FOLDER, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                results_filename = f'batch_results_{timestamp}.csv'
                results_path = os.path.join(Config.RESULTS_FOLDER, results_filename)
                
                # Create results DataFrame
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
                    # Add patient clinical data
                    patient_data = result.get('patient_data', {})
                    for key, value in patient_data.items():
                        row_data[key] = value
                    results_data.append(row_data)
                
                results_df = pd.DataFrame(results_data)
                results_df.to_csv(results_path, index=False, encoding='utf-8-sig')
                print(f"✅ Batch results saved: {results_path}")
                
            except Exception as e:
                print(f"⚠️ Error saving batch results file: {e}")
                results_path = None
                results_filename = None
            
            # Build response
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
            
        except Exception as e:
            print(f"❌ Batch save all error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/download-batch-results/<filename>', methods=['GET'])
    def download_batch_results(filename):
        """
        Download batch prediction results CSV from storage/uploads/batch_results/
        """
        try:
            # Sanitize filename to prevent path traversal
            filename = os.path.basename(filename)
            file_path = os.path.join(Config.RESULTS_FOLDER, filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                return jsonify({
                    'success': False,
                    'error': 'Results file not found. It may have expired or been deleted.'
                }), 404
            
            # Return file for download
            return send_file(
                file_path,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'prediction_results_{filename}'
            )
            
        except Exception as e:
            print(f"❌ Download error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to download results file.'
            }), 500
    
    @app.route('/api/batch-template', methods=['GET'])
    def download_batch_template():
        """Download a template CSV file for batch prediction"""
        try:
            model_name = request.args.get('model', 'top8')
            
            if model_name not in Config.MODELS_INFO:
                return jsonify({
                    'success': False,
                    'error': f'Model "{model_name}" not found. Available: {", ".join(Config.MODELS_INFO.keys())}'
                }), 400
            
            # Select feature set based on model
            if model_name == 'minimal':
                features = Config.FEATURES_MINIMAL
            elif model_name == 'top8':
                features = Config.FEATURES_TOP8
            else:
                features = Config.FEATURES_ALL11
            
            # Create sample row with realistic medical values
            sample_row = {
                'age': 55, 'sex': 1, 'chest pain type': 4,
                'resting bp s': 120, 'cholesterol': 200,
                'fasting blood sugar': 0, 'resting ecg': 0,
                'max heart rate': 150, 'exercise angina': 0,
                'oldpeak': 0.6, 'ST slope': 2
            }
            
            # Filter sample row to only include required features
            filtered_sample = {k: v for k, v in sample_row.items() if k in features}
            
            # Create template DataFrame
            template_df = pd.DataFrame([filtered_sample])
            
            # Add 5 empty rows for user to fill in
            for _ in range(5):
                template_df = pd.concat([
                    template_df,
                    pd.DataFrame([{f: '' for f in features}])
                ], ignore_index=True)
            
            # Convert to CSV
            output = io.StringIO()
            template_df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            
            # Return template as downloadable file
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8-sig')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'template_{model_name}_{datetime.now().strftime("%Y%m%d")}.csv'
            )
            
        except Exception as e:
            print(f"❌ Template download error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to generate template file.'
            }), 500