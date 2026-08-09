

# application/routes/report_routes.py
"""Report Routes - Template management and report generation with Repository + DTO"""

from flask import request, jsonify, render_template, send_file, current_app
import logging
import os

from application.exceptions import (
    TemplateNotFoundError,
    ReportNotFoundError,
    ValidationError
)

logger = logging.getLogger(__name__)


def register_report_routes(app, report_service):
    """Register all report-related routes"""
    
    # ================================================
    # Page Routes
    # ================================================
    
    @app.route('/reports')
    def reports_page():
        """Reports management page"""
        return render_template('reports/reports_list.html')
    
    @app.route('/reports/builder')
    def template_builder_page():
        """Template builder page"""
        field_types = report_service.get_default_field_types()
        return render_template('reports/template_builder.html', field_types=field_types)
    
    @app.route('/reports/builder/<int:template_id>')
    def edit_template_page(template_id):
        """Edit existing template"""
        result = report_service.get_template(template_id)
        if not result.get('success'):
            raise TemplateNotFoundError(template_id)
        return render_template('reports/template_builder.html',
                             field_types=report_service.get_default_field_types(),
                             edit_template=result['template'])
    
    @app.route('/reports/fill/<int:template_id>')
    def fill_report_page(template_id):
        """Page to fill a new report"""
        result = report_service.get_template(template_id)
        if not result.get('success'):
            raise TemplateNotFoundError(template_id)
        return render_template('reports/report_form.html', template=result['template'])
    
    @app.route('/reports/edit/<int:report_id>')
    def edit_report_page(report_id):
        """Page to edit an existing report"""
        report_result = report_service.get_report(report_id)
        if not report_result.get('success'):
            raise ReportNotFoundError(report_id)
        
        report = report_result['report']
        
        template_result = report_service.get_template(report['template_id'])
        if not template_result.get('success'):
            raise TemplateNotFoundError(report['template_id'])
        
        return render_template('reports/report_form.html',
                             template=template_result['template'],
                             edit_report=report)
    
    @app.route('/reports/view/<int:template_id>')
    def view_template_reports_page(template_id):
        """View all reports for a specific template"""
        result = report_service.get_template(template_id)
        if not result.get('success'):
            raise TemplateNotFoundError(template_id)
        return render_template('reports/template_reports.html', template=result['template'])
    
    # ================================================
    # API - Templates
    # ================================================
    
    @app.route('/api/templates', methods=['GET'])
    def api_get_templates():
        """Get all templates"""
        category = request.args.get('category')
        templates = report_service.get_all_templates(category)
        return jsonify({'success': True, 'templates': templates})
    
    @app.route('/api/templates', methods=['POST'])
    def api_create_template():
        """Create a new template"""
        data = request.get_json()
        if not data:
            raise ValidationError("لا توجد بيانات")
        
        result = report_service.create_template(
            title=data.get('title'),
            structure=data.get('structure', []),
            description=data.get('description'),
            category=data.get('category', 'general')
        )
        return jsonify(result), 201 if result.get('success') else 400
    
    @app.route('/api/templates/<int:template_id>', methods=['GET'])
    def api_get_template(template_id):
        """Get a single template"""
        result = report_service.get_template(template_id)
        return jsonify(result)
    
    @app.route('/api/templates/<int:template_id>', methods=['PUT'])
    def api_update_template(template_id):
        """Update a template"""
        data = request.get_json()
        if not data:
            raise ValidationError("لا توجد بيانات")
        
        result = report_service.update_template(
            template_id,
            data.get('title'),
            data.get('structure'),
            data.get('description')
        )
        return jsonify(result)
    
    @app.route('/api/templates/<int:template_id>', methods=['DELETE'])
    def api_delete_template(template_id):
        """Delete a template"""
        result = report_service.delete_template(template_id)
        return jsonify(result)
    
    # ================================================
    # API - Reports
    # ================================================
    
    @app.route('/api/templates/<int:template_id>/reports', methods=['GET'])
    def api_get_template_reports(template_id):
        """Get all reports for a template"""
        reports = report_service.get_template_reports(template_id)
        return jsonify({'success': True, 'reports': reports})
    
    @app.route('/api/reports', methods=['POST'])
    def api_create_report():
        """Create a new report"""
        data = request.get_json()
        if not data:
            raise ValidationError("لا توجد بيانات")
        
        result = report_service.create_report(
            template_id=data.get('template_id'),
            form_data=data.get('form_data', {}),
            patient_uid=data.get('patient_uid')
        )
        return jsonify(result), 201 if result.get('success') else 400
    
    @app.route('/api/reports/<int:report_id>', methods=['GET'])
    def api_get_report(report_id):
        """Get a single report"""
        result = report_service.get_report(report_id)
        return jsonify(result)
    
    @app.route('/api/reports/<int:report_id>', methods=['PUT'])
    def api_update_report(report_id):
        """Update an existing report"""
        data = request.get_json()
        if not data:
            raise ValidationError("لا توجد بيانات")
        
        result = report_service.update_report(
            report_id=report_id,
            form_data=data.get('form_data'),
            patient_uid=data.get('patient_uid')
        )
        return jsonify(result)
    
    @app.route('/api/reports/<int:report_id>', methods=['DELETE'])
    def api_delete_report(report_id):
        """Delete a report"""
        result = report_service.delete_report(report_id)
        return jsonify(result)
    
    # ================================================
    #  PDF Generation with improved error handling
    # ================================================
    
    @app.route('/api/reports/<int:report_id>/pdf', methods=['GET'])
    def api_generate_report_pdf(report_id):
        """Generate and download PDF"""
        try:
           
            if report_id is None or report_id <= 0:
                return jsonify({
                    'success': False,
                    'error': 'معرف التقرير غير صحيح'
                }), 400
            
            result = report_service.generate_pdf(report_id)
            
            if result.get('success'):
                pdf_path = result['pdf_path']
                pdf_filename = result['pdf_filename']
                
              
                if not os.path.exists(pdf_path):
                    return jsonify({
                        'success': False,
                        'error': 'ملف PDF غير موجود'
                    }), 404
                
                return send_file(
                    pdf_path,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=pdf_filename
                )
            else:
                error_msg = result.get('error', 'فشل توليد PDF')
                return jsonify({
                    'success': False,
                    'error': error_msg
                }), 400
                
        except ReportNotFoundError as e:
            return jsonify({
                'success': False,
                'error': e.message
            }), 404
        except Exception as e:
            logger.error(f"PDF generation error: {e}")
            return jsonify({
                'success': False,
                'error': 'حدث خطأ داخلي في توليد PDF'
            }), 500
    
    # ================================================
    #  Additional Routes for better UX
    # ================================================
    
    @app.route('/api/patients/<patient_uid>/reports', methods=['GET'])
    def api_get_patient_reports(patient_uid):
        """Get all reports for a specific patient (by UID from CSV)"""
        try:
           
            if not patient_uid or patient_uid == '':
                return jsonify({
                    'success': False,
                    'error': 'معرف المريض غير صحيح'
                }), 400
            
            reports = report_service.get_reports_by_patient(patient_uid)
            return jsonify({
                'success': True,
                'patient_uid': patient_uid,
                'reports': reports,
                'count': len(reports)
            })
        except Exception as e:
            logger.error(f"Error getting reports for patient {patient_uid}: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/reports/stats', methods=['GET'])
    def api_get_report_stats():
        """Get report statistics"""
        try:
            stats = {
                'total_reports': report_service.get_report_count(),
                'total_templates': len(report_service.get_all_templates()),
            }
            return jsonify({
                'success': True,
                'stats': stats
            })
        except Exception as e:
            logger.error(f"Error getting report stats: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500