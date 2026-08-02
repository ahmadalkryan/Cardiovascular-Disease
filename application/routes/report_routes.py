# application/routes/report_routes.py
"""Report Routes - Template management and report generation"""

from flask import request, jsonify, render_template, send_file


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
        if not result['success']:
            return render_template('404.html'), 404
        return render_template('reports/template_builder.html',
                             field_types=report_service.get_default_field_types(),
                             edit_template=result['template'])
    
    @app.route('/reports/fill/<int:template_id>')
    def fill_report_page(template_id):
        """Page to fill a new report"""
        result = report_service.get_template(template_id)
        if not result['success']:
            return render_template('404.html'), 404
        return render_template('reports/report_form.html', template=result['template'])
    
    @app.route('/reports/edit/<int:report_id>')
    def edit_report_page(report_id):
        """Page to edit an existing report"""
        # Get the report
        report_result = report_service.get_report(report_id)
        if not report_result['success']:
            return render_template('404.html'), 404
        
        report = report_result['report']
        
        # Get the associated template
        template_result = report_service.get_template(report['template_id'])
        if not template_result['success']:
            return render_template('404.html'), 404
        
        return render_template('reports/report_form.html',
                             template=template_result['template'],
                             edit_report=report)
    
    @app.route('/reports/view/<int:template_id>')
    def view_template_reports_page(template_id):
        """View all reports for a specific template"""
        result = report_service.get_template(template_id)
        if not result['success']:
            return render_template('404.html'), 404
        return render_template('reports/template_reports.html', template=result['template'])
    
    # ================================================
    # API - Templates
    # ================================================
    
    @app.route('/api/templates', methods=['GET'])
    def api_get_templates():
        """Get all templates"""
        category = request.args.get('category')
        return jsonify({'success': True, 'templates': report_service.get_all_templates(category)})
    
    @app.route('/api/templates', methods=['POST'])
    def api_create_template():
        """Create a new template"""
        data = request.get_json()
        if not data: return jsonify({'success': False, 'error': 'No data'}), 400
        result = report_service.create_template(
            title=data.get('title'), structure=data.get('structure', []),
            description=data.get('description'), category=data.get('category', 'general')
        )
        return jsonify(result), 201 if result['success'] else 400
    
    @app.route('/api/templates/<int:template_id>', methods=['GET'])
    def api_get_template(template_id):
        """Get a single template"""
        return jsonify(report_service.get_template(template_id))
    
    @app.route('/api/templates/<int:template_id>', methods=['PUT'])
    def api_update_template(template_id):
        """Update a template"""
        data = request.get_json()
        return jsonify(report_service.update_template(
            template_id, data.get('title'), data.get('structure'), data.get('description')
        ))
    
    @app.route('/api/templates/<int:template_id>', methods=['DELETE'])
    def api_delete_template(template_id):
        """Delete a template"""
        return jsonify(report_service.delete_template(template_id))
    
    # ================================================
    # API - Reports
    # ================================================
    
    @app.route('/api/templates/<int:template_id>/reports', methods=['GET'])
    def api_get_template_reports(template_id):
        """Get all reports for a template"""
        return jsonify(report_service.get_template_reports(template_id))
    
    @app.route('/api/reports', methods=['POST'])
    def api_create_report():
        """Create a new report"""
        data = request.get_json()
        result = report_service.create_report(
            template_id=data.get('template_id'),
            form_data=data.get('form_data', {}),
            patient_uid=data.get('patient_uid')
        )
        return jsonify(result), 201 if result['success'] else 400
    
    @app.route('/api/reports/<int:report_id>', methods=['GET'])
    def api_get_report(report_id):
        """Get a single report"""
        return jsonify(report_service.get_report(report_id))
    
    @app.route('/api/reports/<int:report_id>', methods=['PUT'])
    def api_update_report(report_id):
        """Update an existing report"""
        data = request.get_json()
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
    
    @app.route('/api/reports/<int:report_id>/pdf', methods=['GET'])
    def api_generate_report_pdf(report_id):
        """Generate and download PDF"""
        result = report_service.generate_pdf(report_id)
        if result['success']:
            return send_file(result['pdf_path'], mimetype='application/pdf',
                           as_attachment=True, download_name=result['pdf_filename'])
        return jsonify(result), 400