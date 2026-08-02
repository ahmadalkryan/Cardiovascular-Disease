"""Unit tests for database models"""
import pytest
import json
from infrastructure.database import Template, Report, generate_id

class TestGenerateID:
    """Tests for ID generation"""
    
    def test_generate_id_without_prefix(self):
        """Test ID generation without prefix"""
        id1 = generate_id()
        id2 = generate_id()
        assert len(id1) == 8
        assert len(id2) == 8
        assert id1 != id2
    
    def test_generate_id_with_prefix(self):
        """Test ID generation with prefix"""
        prefix = 'REP-'
        id1 = generate_id(prefix)
        id2 = generate_id(prefix)
        assert id1.startswith(prefix)
        assert id2.startswith(prefix)
        assert len(id1) == len(prefix) + 8
        assert id1 != id2
    
    def test_generate_multiple_ids_unique(self):
        """Test that generated IDs are unique"""
        ids = set()
        for _ in range(100):
            new_id = generate_id('TEST-')
            ids.add(new_id)
        assert len(ids) == 100

class TestTemplateModel:
    """Tests for Template model"""
    
    def test_create_template(self, db_session):
        """Test creating a new template"""
        structure = [{"name": "field1", "label": "حقل 1", "type": "text"}]
        template = Template(
            title="قالب جديد",
            description="وصف القالب",
            structure_json=json.dumps(structure),
            category="test",
            is_active=True
        )
        db_session.add(template)
        db_session.commit()
        
        assert template.id is not None
        assert template.title == "قالب جديد"
        assert template.is_active == True
        assert template.category == "test"
    
    def test_template_get_structure(self, sample_template):
        """Test getting structure from template"""
        structure = sample_template.get_structure()
        assert isinstance(structure, list)
        assert len(structure) == 9
        assert structure[0]['name'] == "patient_name"
        assert structure[0]['type'] == "text"
    
    def test_template_field_count(self, sample_template):
        """Test field count property"""
        assert sample_template.field_count == 9
    
    def test_template_report_count_zero(self, sample_template):
        """Test report count when no reports exist"""
        assert sample_template.report_count == 0
    
    def test_template_report_count_with_reports(self, db_session, sample_template, multiple_reports):
        """Test report count when reports exist"""
        # نضمن أن الـ template مرتبط بالـ session
        template = db_session.merge(sample_template)
        assert template.report_count == len(multiple_reports)
    
    def test_template_to_dict(self, sample_template):
        """Test converting template to dict"""
        data = sample_template.to_dict()
        assert 'id' in data
        assert 'title' in data
        assert data['title'] == "قالب فحص القلب"
        assert 'structure' in data
        assert len(data['structure']) == 9
        assert 'category' in data
        assert 'is_active' in data
        assert 'report_count' in data
        assert 'field_count' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_template_to_dict_with_reports(self, db_session, sample_template, multiple_reports):
        """Test template to_dict with reports included"""
        template = db_session.merge(sample_template)
        data = template.to_dict(include_reports=True)
        assert 'reports' in data
        assert len(data['reports']) == len(multiple_reports)
        assert data['reports'][0]['report_uid'] == multiple_reports[0].report_uid
    
    def test_template_str_representation(self, sample_template):
        """Test string representation of template"""
        rep = str(sample_template)
        assert 'Template' in rep
        assert sample_template.title in rep
    
    def test_template_default_values(self, db_session):
        """Test template default values"""
        structure = [{"name": "field1", "label": "Field 1", "type": "text"}]
        template = Template(
            title="Test Template",
            structure_json=json.dumps(structure)
        )
        db_session.add(template)
        db_session.commit()
        
        assert template.is_active == True
        assert template.category == "general"
        assert template.created_at is not None
        assert template.updated_at is not None

class TestReportModel:
    """Tests for Report model"""
    
    def test_create_report(self, db_session, sample_template):
        """Test creating a new report"""
        template = db_session.merge(sample_template)
        report = Report(
            report_uid=generate_id('REP-'),
            template_id=template.id,
            patient_uid=generate_id('PAT-'),
            data_json=json.dumps({"field1": "value1"})
        )
        db_session.add(report)
        db_session.commit()
        
        assert report.id is not None
        assert report.report_uid.startswith('REP-')
        assert report.patient_uid.startswith('PAT-')
        assert report.has_pdf == False
    
    def test_report_get_data(self, sample_report):
        """Test getting data from report"""
        data = sample_report.get_data()
        assert isinstance(data, dict)
        assert 'patient_name' in data
        assert data['patient_name'] == "أحمد محمد"
    
    def test_report_get_field_value(self, sample_report):
        """Test getting field values"""
        value = sample_report.get_field_value('age')
        assert value == 55
        
        value = sample_report.get_field_value('diagnosis')
        assert value == "ارتفاع ضغط الدم"
        
        # حقل غير موجود
        value = sample_report.get_field_value('nonexistent')
        assert value == '-'  # القيمة الافتراضية
    
    def test_report_get_field_value_with_custom_default(self, sample_report):
        """Test getting field with custom default value"""
        value = sample_report.get_field_value('nonexistent', 'N/A')
        assert value == 'N/A'
    
    def test_report_template_title(self, db_session, sample_report):
        """Test template title property"""
        report = db_session.merge(sample_report)
        assert report.template_title == "قالب فحص القلب"
    
    def test_report_has_pdf_false(self, sample_report):
        """Test has_pdf property when no PDF exists"""
        assert sample_report.has_pdf == False
    
    def test_report_to_dict(self, sample_report):
        """Test converting report to dict"""
        data = sample_report.to_dict()
        assert 'id' in data
        assert 'report_uid' in data
        assert data['report_uid'].startswith('REP-')
        assert 'template_id' in data
        assert 'template_title' in data
        assert 'patient_uid' in data
        assert 'data' in data
        assert 'has_pdf' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_report_to_dict_with_template(self, db_session, sample_report):
        """Test report to_dict with template included"""
        report = db_session.merge(sample_report)
        data = report.to_dict(include_template=True)
        assert 'template' in data
        assert data['template']['id'] == report.template_id
        assert data['template']['title'] == "قالب فحص القلب"
    
    def test_report_str_representation(self, sample_report):
        """Test string representation of report"""
        rep = str(sample_report)
        assert 'Report' in rep
        assert sample_report.report_uid in rep
    
    def test_report_default_values(self, db_session, sample_template):
        """Test report default values"""
        template = db_session.merge(sample_template)
        report = Report(
            report_uid=generate_id('REP-'),
            template_id=template.id,
            data_json=json.dumps({})
        )
        db_session.add(report)
        db_session.commit()
        
        assert report.patient_uid is None
        assert report.pdf_path is None
        assert report.created_at is not None
        assert report.updated_at is not None

# tests/test_unit/test_database.py (تعديل الجزء الخاص بـ cascade delete)

class TestModelRelationships:
    """Tests for model relationships"""
    
    def test_template_reports_relationship(self, db_session, sample_template, multiple_reports):
        """Test relationship between template and reports"""
        template = db_session.merge(sample_template)
        assert len(template.reports) == len(multiple_reports)
        for report in template.reports:
            assert report.template_id == template.id
    
    def test_report_template_relationship(self, db_session, sample_report):
        """Test relationship between report and template"""
        report = db_session.merge(sample_report)
        assert report.template is not None
        assert report.template.id == report.template_id
    
    def test_cascade_delete(self, db_session, sample_template, multiple_reports):
        """Test cascade delete when template is deleted"""
        # نضمن أن الـ template مرتبط بالـ session
        template = db_session.merge(sample_template)
        template_id = template.id
        
        # نتحقق من وجود التقارير أولاً
        reports_before = db_session.query(Report).filter_by(template_id=template_id).all()
        assert len(reports_before) == len(multiple_reports)
        
        # حذف القالب
        db_session.delete(template)
        db_session.commit()
        
        # نتحقق أن جميع التقارير حُذفت
        reports_after = db_session.query(Report).filter_by(template_id=template_id).all()
        assert len(reports_after) == 0
        
        # نتحقق أيضاً أن القالب نفسه حُذف
        template_after = db_session.query(Template).filter_by(id=template_id).first()
        assert template_after is None
    
    def test_cascade_delete_with_orphan(self, db_session, sample_template, sample_report):
        """Test cascade delete removes orphan reports"""
        template = db_session.merge(sample_template)
        template_id = template.id
        
        # نتحقق من وجود التقرير
        report = db_session.merge(sample_report)
        assert report.template_id == template_id
        
        # حذف القالب
        db_session.delete(template)
        db_session.commit()
        
        # نتحقق أن التقرير حُذف
        report_after = db_session.query(Report).filter_by(id=report.id).first()
        assert report_after is None