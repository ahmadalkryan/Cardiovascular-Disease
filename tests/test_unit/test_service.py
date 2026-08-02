"""Unit tests for services"""
import pytest
import json
import os
from business.services.report_service import ReportService
from business.services.data_service import DataService
from infrastructure.database import Template, Report, generate_id
from business.config.field_types import FieldTypes

class TestReportTemplateService:
    """Tests for report template service"""
    
    def test_create_template(self, db_session):
        """Test creating a template via service"""
        service = ReportService('temp')
        structure = [{"name": "field1", "label": "حقل 1", "type": "text"}]
        
        result = service.create_template(
            title="قالب جديد",
            description="وصف القالب",
            structure=structure,
            category="test"
        )
        
        assert result['success'] == True
        assert result['template']['title'] == "قالب جديد"
        assert len(result['template']['structure']) == 1
    
    
    def test_get_all_templates_with_data(self, db_session, sample_template):
        """Test getting all templates with data"""
        service = ReportService('temp')
        templates = service.get_all_templates()
        assert len(templates) >= 1
        assert templates[0]['title'] == "قالب فحص القلب"
    
    def test_get_all_templates_by_category(self, db_session, multiple_templates):
        """Test filtering templates by category"""
        service = ReportService('temp')
        
        # اختبار الدالة
        result = service.get_all_templates(category='cardiology')
        assert len(result) >= 1
        # نتحقق أن جميع النتائج من الفئة المطلوبة
        for template in result:
            assert template['category'] == 'cardiology'
    
    def test_get_template(self, db_session, sample_template):
        """Test getting a specific template"""
        service = ReportService('temp')
        result = service.get_template(sample_template.id)
        
        assert result['success'] == True
        assert result['template']['id'] == sample_template.id
        assert result['template']['title'] == sample_template.title
    
    def test_get_template_not_found(self, db_session):
        """Test getting non-existent template"""
        service = ReportService('temp')
        result = service.get_template(99999)
        
        assert result['success'] == False
        assert 'error' in result
    
    def test_update_template(self, db_session, sample_template):
        """Test updating a template"""
        service = ReportService('temp')
        result = service.update_template(
            template_id=sample_template.id,
            title="عنوان محدث",
            description="وصف محدث"
        )
        
        assert result['success'] == True
        assert result['template']['title'] == "عنوان محدث"
        assert result['template']['description'] == "وصف محدث"
    
    def test_update_template_partial(self, db_session, sample_template):
        """Test partial update of template"""
        service = ReportService('temp')
        result = service.update_template(
            template_id=sample_template.id,
            title="عنوان محدث فقط"
        )
        
        assert result['success'] == True
        assert result['template']['title'] == "عنوان محدث فقط"
        assert result['template']['description'] == sample_template.description
    
    def test_update_template_not_found(self, db_session):
        """Test updating non-existent template"""
        service = ReportService('temp')
        result = service.update_template(
            template_id=99999,
            title="عنوان جديد"
        )
        
        assert result['success'] == False
        assert 'error' in result
    
    def test_delete_template(self, db_session, sample_template):
        """Test deleting a template"""
        service = ReportService('temp')
        template_id = sample_template.id
        
        result = service.delete_template(template_id)
        assert result['success'] == True
        
        # نتحقق من الحذف
        template = db_session.query(Template).get(template_id)
        assert template is None
    
    def test_delete_template_not_found(self, db_session):
        """Test deleting non-existent template"""
        service = ReportService('temp')
        result = service.delete_template(99999)
        assert result['success'] == False
        assert 'error' in result

class TestReportService:
    """Tests for report operations"""
    
    def test_create_report(self, db_session, sample_template):
        """Test creating a report"""
        service = ReportService('temp')
        form_data = {"patient_name": "مريض جديد", "age": 30}
        
        result = service.create_report(
            template_id=sample_template.id,
            form_data=form_data,
            patient_uid=generate_id('PAT-')
        )
        
        assert result['success'] == True
        assert result['report']['template_id'] == sample_template.id
        assert result['report']['data']['patient_name'] == "مريض جديد"
    
    def test_create_report_without_patient_uid(self, db_session, sample_template):
        """Test creating report without patient_uid (auto-generate)"""
        service = ReportService('temp')
        form_data = {"patient_name": "مريض جديد"}
        
        result = service.create_report(
            template_id=sample_template.id,
            form_data=form_data
        )
        
        assert result['success'] == True
        assert result['report']['patient_uid'] is not None
        assert result['report']['patient_uid'].startswith('PAT-')
    
    def test_create_report_template_not_found(self, db_session):
        """Test creating report with non-existent template"""
        service = ReportService('temp')
        result = service.create_report(
            template_id=99999,
            form_data={}
        )
        
        assert result['success'] == False
        assert 'error' in result
    
    def test_get_report(self, db_session, sample_report):
        """Test getting a report"""
        service = ReportService('temp')
        result = service.get_report(sample_report.id)
        
        assert result['success'] == True
        assert result['report']['id'] == sample_report.id
        assert result['report']['report_uid'] == sample_report.report_uid
    
    def test_get_report_not_found(self, db_session):
        """Test getting non-existent report"""
        service = ReportService('temp')
        result = service.get_report(99999)
        
        assert result['success'] == False
    
    def test_get_template_reports(self, db_session, sample_template, multiple_reports):
        """Test getting all reports for a template"""
        service = ReportService('temp')
        result = service.get_template_reports(sample_template.id)
        
        assert result['success'] == True
        assert len(result['reports']) == len(multiple_reports)
        assert result['template']['id'] == sample_template.id
    
    def test_get_template_reports_not_found(self, db_session):
        """Test getting reports for non-existent template"""
        service = ReportService('temp')
        result = service.get_template_reports(99999)
        
        assert result['success'] == False
        assert 'error' in result
    
    def test_update_report(self, db_session, sample_report):
        """Test updating a report"""
        service = ReportService('temp')
        new_data = {"patient_name": "مريض محدث", "age": 35}
        
        result = service.update_report(
            report_id=sample_report.id,
            form_data=new_data,
            patient_uid=generate_id('PAT-')
        )
        
        assert result['success'] == True
        assert result['report']['data']['patient_name'] == "مريض محدث"
        assert result['report']['data']['age'] == 35
    
    def test_update_report_partial(self, db_session, sample_report):
        """Test partial update of report"""
        service = ReportService('temp')
        
        # نأخذ البيانات الحالية
        current_data = sample_report.get_data()
        
        # نعدل البيانات الحالية بإضافة/تحديث العمر
        updated_data = current_data.copy()
        updated_data['age'] = 40
        
        # نحدث التقرير بالبيانات الجديدة
        result = service.update_report(
            report_id=sample_report.id,
            form_data=updated_data
        )
        
        assert result['success'] == True
        # نتحقق أن العمر تم تحديثه
        assert result['report']['data']['age'] == 40
        # نتحقق أن البيانات الأخرى بقيت كما هي (إذا كانت موجودة)
        if 'patient_name' in current_data:
            assert result['report']['data']['patient_name'] == current_data['patient_name']
    
    def test_delete_report(self, db_session, sample_report):
        """Test deleting a report"""
        service = ReportService('temp')
        report_id = sample_report.id
        
        result = service.delete_report(report_id)
        assert result['success'] == True
        
        # نتحقق من الحذف
        report = db_session.query(Report).get(report_id)
        assert report is None
    
    def test_get_default_field_types(self):
        """Test getting default field types"""
        service = ReportService('temp')
        field_types = service.get_default_field_types()
        
        assert isinstance(field_types, list)
        assert len(field_types) > 0
        
        # نتحقق من هيكل البيانات الصحيح
        first_field = field_types[0]
        assert 'type' in first_field
        assert 'label' in first_field
        assert first_field['type'] == 'text'