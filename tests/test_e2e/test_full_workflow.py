"""End-to-End tests for full system workflow"""
import pytest
import json
import os
from datetime import datetime
from infrastructure.database import db, Template, Report, generate_id  # <-- إضافة generate_id
from business.services.report_service import ReportService
from business.services.data_service import DataService

class TestEndToEndWorkflow:
    """Complete end-to-end tests"""
    
    def test_full_doctor_workflow(self, db_session, report_service, data_service):
        """Test complete doctor workflow: template → report → PDF → statistics"""
        
        # === STEP 1: Create a new template ===
        print("\n📋 Step 1: Creating template...")
        structure = [
            {"name": "patient_name", "label": "اسم المريض", "type": "text", "required": True},
            {"name": "age", "label": "العمر", "type": "number", "required": True},
            {"name": "gender", "label": "الجنس", "type": "select", "options": ["ذكر", "أنثى"]},
            {"name": "diagnosis", "label": "التشخيص", "type": "text", "required": True},
            {"name": "blood_pressure", "label": "ضغط الدم", "type": "text"},
            {"name": "heart_rate", "label": "معدل ضربات القلب", "type": "number"},
            {"name": "symptoms", "label": "الأعراض", "type": "textarea"},
            {"name": "medications", "label": "الأدوية الموصوفة", "type": "text"},
            {"name": "follow_up", "label": "موعد المتابعة", "type": "date"},
            {"name": "notes", "label": "ملاحظات إضافية", "type": "textarea"}
        ]
        
        template_result = report_service.create_template(
            title="قالب الفحص السريري",
            description="قالب شامل للفحص السريري للمرضى",
            structure=structure,
            category="clinical"
        )
        assert template_result['success'] == True
        template_id = template_result['template']['id']
        print(f"✅ Template created: ID={template_id}")
        
        # === STEP 2: Create multiple reports ===
        print("\n📋 Step 2: Creating patient reports...")
        patients_data = [
            {
                "patient_name": "أحمد محمد",
                "age": 55,
                "gender": "ذكر",
                "diagnosis": "ارتفاع ضغط الدم",
                "blood_pressure": "140/90",
                "heart_rate": 85,
                "symptoms": "صداع، دوخة",
                "medications": "Captopril 25mg",
                "follow_up": "2026-08-15",
                "notes": "يحتاج متابعة شهرية"
            },
            {
                "patient_name": "سارة أحمد",
                "age": 42,
                "gender": "أنثى",
                "diagnosis": "السكري من النوع الثاني",
                "blood_pressure": "130/85",
                "heart_rate": 78,
                "symptoms": "عطش شديد، كثرة التبول",
                "medications": "Metformin 500mg",
                "follow_up": "2026-07-30",
                "notes": "تحتاج فحص سكر صائم"
            },
            {
                "patient_name": "خالد علي",
                "age": 65,
                "gender": "ذكر",
                "diagnosis": "مرض القلب التاجي",
                "blood_pressure": "150/95",
                "heart_rate": 92,
                "symptoms": "ألم في الصدر، ضيق تنفس",
                "medications": "Aspirin, Atorvastatin",
                "follow_up": "2026-08-01",
                "notes": "يحتاج تخطيط قلب"
            }
        ]
        
        report_ids = []
        for patient in patients_data:
            result = report_service.create_report(
                template_id=template_id,
                form_data=patient,
                patient_uid=f"PAT-{patient['patient_name'][:3]}{patient['age']}"
            )
            assert result['success'] == True
            report_ids.append(result['report']['id'])
            print(f"✅ Report created for: {patient['patient_name']}")
        
        # === STEP 3: Get all reports for template ===
        print("\n📋 Step 3: Retrieving all reports...")
        reports_result = report_service.get_template_reports(template_id)
        assert reports_result['success'] == True
        assert len(reports_result['reports']) == 3
        print(f"✅ Retrieved {len(reports_result['reports'])} reports")
        
        # === STEP 4: Update a report ===
        print("\n📋 Step 4: Updating a report...")
        update_data = {
            "patient_name": "أحمد محمد",
            "age": 56,
            "gender": "ذكر",
            "diagnosis": "ارتفاع ضغط الدم - درجة 2",
            "blood_pressure": "145/92",
            "heart_rate": 88,
            "symptoms": "صداع، دوخة، عدم وضوح الرؤية",
            "medications": "Captopril 50mg",
            "follow_up": "2026-08-20",
            "notes": "زيادة الجرعة، متابعة الضغط أسبوعياً"
        }
        update_result = report_service.update_report(
            report_id=report_ids[0],
            form_data=update_data
        )
        assert update_result['success'] == True
        print(f"✅ Report updated for: {update_data['patient_name']}")
        
        # === STEP 5: Generate PDF for each report ===
        print("\n📋 Step 5: Generating PDFs...")
        pdf_paths = []
        for report_id in report_ids:
            pdf_result = report_service.generate_pdf(report_id)
            if pdf_result['success']:
                pdf_paths.append(pdf_result['pdf_path'])
                print(f"✅ PDF generated: {os.path.basename(pdf_result['pdf_path'])}")
        
        assert len(pdf_paths) > 0
        
        # === STEP 6: Save patient data for statistics ===
        print("\n📋 Step 6: Saving patient data...")
        for i, patient in enumerate(patients_data):
            patient_data = {
                'age': patient['age'],
                'sex': 1 if patient['gender'] == 'ذكر' else 0,
                'chest_pain_type': 2 if i == 2 else 1,
                'resting_bp': int(patient['blood_pressure'].split('/')[0]) if '/' in patient['blood_pressure'] else 130,
                'cholesterol': 180 + i * 20,
                'max_heart_rate': 150 - patient['age'] + i * 5,
                'ST_slope': 1 + i,
                'exercise_angina': 1 if i == 2 else 0,
                'oldpeak': 1.0 + i * 0.5
            }
            
            data_service.save_patient_data(
                patient_data=patient_data,
                prediction=1 if i % 2 == 0 else 0,
                probability=0.6 + i * 0.1,
                model_name='minimal',
                model_features=['age', 'sex']
            )
        print("✅ Patient data saved")
        
        # === STEP 7: Get statistics ===
        print("\n📋 Step 7: Calculating statistics...")
        stats = data_service.get_statistics()
        assert stats['total'] >= 3
        print(f"✅ Statistics calculated: Total={stats['total']}, Disease={stats['disease']}, Healthy={stats['healthy']}")
        
        # === STEP 8: Cleanup ===
        print("\n📋 Step 8: Cleaning up...")
        # Delete reports
        for report_id in report_ids:
            report_service.delete_report(report_id)
        
        # Delete template
        report_service.delete_template(template_id)
        
        # Delete PDF files
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                print(f"✅ Deleted PDF: {os.path.basename(pdf_path)}")
        
        print("✅ All cleaned up!")
    
    def test_error_handling_workflow(self, db_session, report_service):
        """Test error handling in various scenarios"""
        
        # 1. Create template with invalid structure - 
        print("\n🔴 Testing invalid structure...")
        
        # Test: structure is not a list (string)
        result = report_service.create_template(
            title="قالب خاطئ",
            structure="invalid_string",  
            description="هذا القالب سيفشل"
        )
       
        
        # Test: structure contains unserializable object
        class NonSerializable:
            pass
        
        result = report_service.create_template(
            title="قالب خاطئ",
            structure=[NonSerializable()],  
            description="هذا القالب سيفشل"
        )
        # هذا يجب أن يفشل
        assert result['success'] == False
        assert 'error' in result
        print("✅ Invalid structure handled correctly")
        
        # 2. Create report with non-existent template
        print("\n🔴 Testing non-existent template...")
        result = report_service.create_report(
            template_id=99999,
            form_data={"patient_name": "test"}
        )
        assert result['success'] == False
        assert 'error' in result
        print("✅ Non-existent template handled correctly")
        
        # 3. Update non-existent report
        print("\n🔴 Testing non-existent report...")
        result = report_service.update_report(
            report_id=99999,
            form_data={"test": "data"}
        )
        assert result['success'] == False
        assert 'error' in result
        print("✅ Non-existent report handled correctly")
        
        # 4. Delete non-existent template
        print("\n🔴 Testing delete non-existent template...")
        result = report_service.delete_template(99999)
        assert result['success'] == False
        assert 'error' in result
        print("✅ Delete non-existent handled correctly")
        
        # 5. Generate PDF for non-existent report
        print("\n🔴 Testing PDF generation for non-existent report...")
        result = report_service.generate_pdf(99999)
        assert result['success'] == False
        assert 'error' in result
        print("✅ PDF generation for non-existent handled correctly")
    
    def test_data_integrity_workflow(self, db_session, sample_template, report_service):
        """Test data integrity across operations"""
        
        # 1. Create multiple reports
        reports_data = [
            {"patient_name": "مريض A", "age": 30, "diagnosis": "تشخيص A"},
            {"patient_name": "مريض B", "age": 40, "diagnosis": "تشخيص B"},
            {"patient_name": "مريض C", "age": 50, "diagnosis": "تشخيص C"}
        ]
        
        report_ids = []
        for data in reports_data:
            result = report_service.create_report(
                template_id=sample_template.id,
                form_data=data,
                patient_uid=generate_id('PAT-')  # الآن generate_id معرف
            )
            assert result['success'] == True
            report_ids.append(result['report']['id'])
        
        # 2. Verify all reports exist
        for report_id in report_ids:
            result = report_service.get_report(report_id)
            assert result['success'] == True
            assert result['report']['id'] == report_id
        
        # 3. Delete one report
        report_service.delete_report(report_ids[0])
        
        # 4. Verify only 2 reports remain
        result = report_service.get_template_reports(sample_template.id)
        assert result['success'] == True
        assert len(result['reports']) == 2
        
        # 5. Delete template (cascade delete)
        report_service.delete_template(sample_template.id)
        
        # 6. Verify all reports are deleted
        for report_id in report_ids[1:]:
            result = report_service.get_report(report_id)
            assert result['success'] == False
    
    def test_concurrent_operations_workflow(self, db_session, sample_template, report_service):
        """Test concurrent operations (sequential simulation)"""
        
        # Create multiple templates
        templates = []
        for i in range(3):
            structure = [{"name": f"field_{i}", "label": f"حقل {i}", "type": "text"}]
            result = report_service.create_template(
                title=f"قالب متزامن {i+1}",
                description=f"وصف القالب {i+1}",
                structure=structure,
                category="concurrent"
            )
            assert result['success'] == True
            templates.append(result['template']['id'])
        
        # Create reports for each template
        all_report_ids = []
        for template_id in templates:
            for j in range(2):
                result = report_service.create_report(
                    template_id=template_id,
                    form_data={"field": f"value_{j}"},
                    patient_uid=generate_id('PAT-')
                )
                assert result['success'] == True
                all_report_ids.append(result['report']['id'])
        
        # Verify total reports count
        total_reports = 0
        for template_id in templates:
            result = report_service.get_template_reports(template_id)
            assert result['success'] == True
            total_reports += len(result['reports'])
        
        assert total_reports == 6  # 3 templates * 2 reports each
        
        # Cleanup
        for report_id in all_report_ids:
            report_service.delete_report(report_id)
        
        for template_id in templates:
            report_service.delete_template(template_id)
    
    def test_pdf_generation_with_special_characters(self, db_session, sample_template, report_service):
        """Test PDF generation with special characters and Arabic text"""
        
        # Create report with special characters
        special_data = {
            "patient_name": "محمد أحمد علي",
            "age": 45,
            "diagnosis": "مرض القلب التاجي ⚡",
            "blood_pressure": "140/90 mmHg",
            "heart_rate": "85 bpm",
            "symptoms": "ألم صدر، ضيق تنفس، تعب 🏥",
            "medications": "Aspirin 75mg + Atorvastatin 20mg",
            "follow_up": "2026-09-01",
            "notes": "ملاحظات: يحتاج متابعة ❤️"
        }
        
        result = report_service.create_report(
            template_id=sample_template.id,
            form_data=special_data,
            patient_uid=generate_id('PAT-')
        )
        assert result['success'] == True
        report_id = result['report']['id']
        
        # Generate PDF
        pdf_result = report_service.generate_pdf(report_id)
        assert pdf_result['success'] == True
        assert os.path.exists(pdf_result['pdf_path'])
        
        # Cleanup
        if os.path.exists(pdf_result['pdf_path']):
            os.remove(pdf_result['pdf_path'])
        
        report_service.delete_report(report_id)