"""Pytest configuration and fixtures"""
import pytest
import os
import tempfile
import json
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from infrastructure.database import db, Template, Report, generate_id
from business.services.report_service import ReportService
from business.services.data_service import DataService

# ========== إعداد Flask App للاختبار ==========
@pytest.fixture(scope='session')
def app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    return app

@pytest.fixture(scope='function')
def app_context(app):
    """Provide Flask app context for each test"""
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def db_session(app):
    """Provide database session for each test"""
    with app.app_context():
        db.session.begin_nested()
        
        yield db.session
        
        db.session.rollback()
        db.session.remove()

# ========== Fixtures للبيانات ==========
@pytest.fixture(scope='function')
def sample_structure():
    """Sample template structure"""
    return [
        {"name": "patient_name", "label": "اسم المريض", "type": "text", "required": True},
        {"name": "age", "label": "العمر", "type": "number", "required": True},
        {"name": "diagnosis", "label": "التشخيص", "type": "text", "required": True},
        {"name": "blood_pressure", "label": "ضغط الدم", "type": "text"},
        {"name": "heart_rate", "label": "معدل ضربات القلب", "type": "number"},
        {"name": "symptoms", "label": "الأعراض", "type": "textarea"},
        {"name": "medications", "label": "الأدوية", "type": "text"},
        {"name": "follow_up", "label": "موعد المتابعة", "type": "date"},
        {"name": "notes", "label": "ملاحظات", "type": "textarea"}
    ]

@pytest.fixture(scope='function')
def sample_template(db_session, sample_structure):
    """Create a sample template"""
    template = Template(
        title="قالب فحص القلب",
        description="قالب شامل لفحص أمراض القلب",
        structure_json=json.dumps(sample_structure, ensure_ascii=False),
        category="cardiology",
        is_active=True
    )
    db_session.add(template)
    db_session.commit()
    db_session.refresh(template)
    return template

@pytest.fixture(scope='function')
def sample_report_data():
    """Sample report data"""
    return {
        "patient_name": "أحمد محمد",
        "age": 55,
        "diagnosis": "ارتفاع ضغط الدم",
        "blood_pressure": "140/90",
        "heart_rate": 85,
        "symptoms": "صداع، دوخة",
        "medications": "Captopril 25mg",
        "follow_up": "2026-08-01",
        "notes": "يحتاج متابعة شهرية"
    }

@pytest.fixture(scope='function')
def sample_report(db_session, sample_template, sample_report_data):
    """Create a sample report"""
    report = Report(
        report_uid=generate_id('REP-'),
        template_id=sample_template.id,
        patient_uid=generate_id('PAT-'),
        data_json=json.dumps(sample_report_data, ensure_ascii=False)
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    return report

@pytest.fixture(scope='function')
def report_service():
    """Create ReportService instance for testing"""
    reports_folder = tempfile.mkdtemp()
    return ReportService(reports_folder)

@pytest.fixture(scope='function')
def data_service():
    """Create DataService instance for testing"""
    data_folder = tempfile.mkdtemp()
    patient_files = {
        'minimal': os.path.join(data_folder, 'minimal_patients.csv'),
        'top8': os.path.join(data_folder, 'top8_patients.csv'),
        'all11': os.path.join(data_folder, 'all11_patients.csv')
    }
    return DataService(data_folder, patient_files)

# ========== Fixtures للبيانات الإضافية ==========
@pytest.fixture(scope='function')
def multiple_templates(db_session, sample_structure):
    """Create multiple templates for testing"""
    templates = []
    categories = ['cardiology', 'neurology', 'general']
    titles = ['قالب القلب', 'قالب الأعصاب', 'قالب عام']
    
    for category, title in zip(categories, titles):
        template = Template(
            title=title,
            description=f"وصف {title}",
            structure_json=json.dumps(sample_structure, ensure_ascii=False),
            category=category,
            is_active=True
        )
        db_session.add(template)
        templates.append(template)
    
    db_session.commit()
    for template in templates:
        db_session.refresh(template)
    
    return templates

@pytest.fixture(scope='function')
def multiple_reports(db_session, sample_template):
    """Create multiple reports for testing"""
    reports = []
    patients = ["مريض 1", "مريض 2", "مريض 3"]
    
    for i, patient in enumerate(patients):
        report = Report(
            report_uid=generate_id('REP-'),
            template_id=sample_template.id,
            patient_uid=generate_id('PAT-'),
            data_json=json.dumps({
                "patient_name": patient,
                "age": 40 + i * 5,
                "diagnosis": f"تشخيص {i+1}",
                "notes": f"ملاحظات {i+1}"
            }, ensure_ascii=False)
        )
        db_session.add(report)
        reports.append(report)
    
    db_session.commit()
    for report in reports:
        db_session.refresh(report)
    
    return reports