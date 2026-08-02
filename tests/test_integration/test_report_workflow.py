"""Integration tests for report workflow"""
import pytest
import json
import os
from datetime import datetime
from infrastructure.database import db, Template, Report, generate_id
from business.services.report_service import ReportService
from business.services.data_service import DataService

class TestReportWorkflow:
    """Integration tests for complete report workflow"""
    
    def test_complete_report_workflow(self, db_session, report_service):
        """Test complete workflow: create template → create report → update → delete"""
        
        # 1. Create template
        structure = [
            {"name": "patient_name", "label": "اسم المريض", "type": "text"},
            {"name": "age", "label": "العمر", "type": "number"},
            {"name": "diagnosis", "label": "التشخيص", "type": "text"}
        ]
        
        create_result = report_service.create_template(
            title="قالب اختبار التكامل",
            description="قالب لاختبار التكامل",
            structure=structure,
            category="test"
        )
        
        assert create_result['success'] == True
        template_id = create_result['template']['id']
        
        # 2. Create report
        form_data = {
            "patient_name": "مريض تكامل",
            "age": 45,
            "diagnosis": "اختبار تشخيص"
        }
        
        report_result = report_service.create_report(
            template_id=template_id,
            form_data=form_data,
            patient_uid=generate_id('PAT-')
        )
        
        assert report_result['success'] == True
        report_id = report_result['report']['id']
        
        # 3. Get report and verify
        get_result = report_service.get_report(report_id)
        assert get_result['success'] == True
        assert get_result['report']['data']['patient_name'] == "مريض تكامل"
        
        # 4. Update report
        updated_data = {
            "patient_name": "مريض تكامل محدث",
            "age": 50,
            "diagnosis": "تشخيص محدث"
        }
        
        update_result = report_service.update_report(
            report_id=report_id,
            form_data=updated_data
        )
        
        assert update_result['success'] == True
        assert update_result['report']['data']['patient_name'] == "مريض تكامل محدث"
        
        # 5. Delete report
        delete_result = report_service.delete_report(report_id)
        assert delete_result['success'] == True
        
        # Verify report is deleted
        get_deleted = report_service.get_report(report_id)
        assert get_deleted['success'] == False
    
    def test_template_with_multiple_reports(self, db_session, sample_template, report_service):
        """Test creating multiple reports for same template"""
        template_id = sample_template.id
        
        reports_data = [
            {"patient_name": "مريض 1", "age": 30, "diagnosis": "تشخيص 1"},
            {"patient_name": "مريض 2", "age": 40, "diagnosis": "تشخيص 2"},
            {"patient_name": "مريض 3", "age": 50, "diagnosis": "تشخيص 3"}
        ]
        
        report_ids = []
        for data in reports_data:
            result = report_service.create_report(
                template_id=template_id,
                form_data=data,
                patient_uid=generate_id('PAT-')
            )
            assert result['success'] == True
            report_ids.append(result['report']['id'])
        
        # Get all reports for template
        result = report_service.get_template_reports(template_id)
        assert result['success'] == True
        assert len(result['reports']) == len(reports_data)
        
        # Delete all reports
        for report_id in report_ids:
            result = report_service.delete_report(report_id)
            assert result['success'] == True
    
    def test_pdf_generation_workflow(self, db_session, sample_template, sample_report_data, report_service):
        """Test PDF generation workflow"""
        # Create report
        result = report_service.create_report(
            template_id=sample_template.id,
            form_data=sample_report_data,
            patient_uid=generate_id('PAT-')
        )
        assert result['success'] == True
        report_id = result['report']['id']
        
        # Generate PDF
        pdf_result = report_service.generate_pdf(report_id)
        assert pdf_result['success'] == True
        assert 'pdf_path' in pdf_result
        assert os.path.exists(pdf_result['pdf_path'])
        
        # Verify report has PDF
        report = db_session.query(Report).get(report_id)
        assert report.pdf_path is not None
        assert report.has_pdf == True
        
        # Cleanup
        if os.path.exists(pdf_result['pdf_path']):
            os.remove(pdf_result['pdf_path'])
    
    def test_template_crud_workflow(self, db_session, report_service):
        """Test complete CRUD workflow for templates"""
        
        # 1. Create template
        structure = [{"name": "field1", "label": "حقل 1", "type": "text"}]
        create_result = report_service.create_template(
            title="قالب CRUD",
            description="قالب اختبار CRUD",
            structure=structure,
            category="test"
        )
        assert create_result['success'] == True
        template_id = create_result['template']['id']
        
        # 2. Get template
        get_result = report_service.get_template(template_id)
        assert get_result['success'] == True
        assert get_result['template']['title'] == "قالب CRUD"
        
        # 3. Update template
        update_result = report_service.update_template(
            template_id=template_id,
            title="قالب CRUD محدث",
            description="وصف محدث"
        )
        assert update_result['success'] == True
        assert update_result['template']['title'] == "قالب CRUD محدث"
        
        # 4. Get all templates
        all_templates = report_service.get_all_templates()
        assert len(all_templates) >= 1
        
        # 5. Delete template
        delete_result = report_service.delete_template(template_id)
        assert delete_result['success'] == True
        
        # Verify deletion
        get_deleted = report_service.get_template(template_id)
        assert get_deleted['success'] == False

class TestDataServiceIntegration:
    """Integration tests for DataService"""
    
    def test_data_save_and_retrieve(self, data_service):
        """Test saving and retrieving patient data"""
        patient_data = {
            'age': 55,
            'sex': 1,
            'chest_pain_type': 2,
            'resting_bp': 140,
            'cholesterol': 200,
            'max_heart_rate': 150,
            'ST_slope': 2,
            'exercise_angina': 1,
            'oldpeak': 1.5
        }
        
        patient_id = data_service.save_patient_data(
            patient_data=patient_data,
            prediction=1,
            probability=0.85,
            model_name='minimal',
            model_features=['age', 'sex']
        )
        
        assert patient_id is not None
        
        # Retrieve data
        df = data_service.get_patients_data('minimal')
        assert not df.empty
        assert len(df) >= 1
        
        # Verify data
        record = df.iloc[0]
        assert record['age'] == 55
        assert record['prediction'] == 1
        assert record['probability'] == 0.85
    
    def test_multiple_model_data(self, data_service):
        """Test saving data for multiple models"""
        models = ['minimal', 'top8', 'all11']
        
        for model in models:
            data_service.save_patient_data(
                patient_data={'age': 50, 'sex': 1},
                prediction=0,
                probability=0.3,
                model_name=model,
                model_features=['age']
            )
        
        # Get all data
        all_data = data_service.get_patients_data()
        assert not all_data.empty
        assert len(all_data) >= 3
        
        # Get data for specific model
        minimal_data = data_service.get_patients_data('minimal')
        assert not minimal_data.empty
        assert all(minimal_data['model_used'] == 'minimal')
    
    def test_statistics_calculation(self, data_service):
        """Test statistics calculation with multiple records"""
        # Add multiple records
        for i in range(10):
            data_service.save_patient_data(
                patient_data={'age': 40 + i * 5},
                prediction=1 if i % 2 == 0 else 0,
                probability=0.5 + i * 0.05,
                model_name='minimal',
                model_features=['age']
            )
        
        stats = data_service.get_statistics()
        
        assert stats['total'] == 10
        assert stats['disease'] == 5
        assert stats['healthy'] == 5
        assert stats['avg_probability'] > 0
        assert len(stats['recent']) > 0
        assert 'by_model' in stats
        assert stats['by_model']['minimal'] == 10