
# application/exceptions/custom_exceptions.py
"""Custom Exception Classes for the Application"""


class AppException(Exception):
    """Base exception for the application"""
    def __init__(self, message, status_code=500, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)


# ================================================
# Model Exceptions
# ================================================
class ModelNotFoundError(AppException):
    def __init__(self, model_name):
        super().__init__(
            message=f"النموذج '{model_name}' غير موجود",
            status_code=404,
            error_code="MODEL_NOT_FOUND"
        )


class ModelLoadError(AppException):
    def __init__(self, model_name, reason):
        super().__init__(
            message=f"فشل تحميل النموذج '{model_name}': {reason}",
            status_code=500,
            error_code="MODEL_LOAD_ERROR"
        )


# ================================================
# Patient Exceptions
# ================================================
class PatientNotFoundError(AppException):
    def __init__(self, patient_id):
        super().__init__(
            message=f"المريض برقم '{patient_id}' غير موجود",
            status_code=404,
            error_code="PATIENT_NOT_FOUND"
        )


class PatientDataValidationError(AppException):
    def __init__(self, errors):
        if isinstance(errors, list):
            message = f"بيانات المريض غير صالحة: {', '.join(errors)}"
        else:
            message = f"بيانات المريض غير صالحة: {errors}"
        super().__init__(
            message=message,
            status_code=400,
            error_code="PATIENT_VALIDATION_ERROR"
        )


# ================================================
# Report Exceptions 
# ================================================
class ReportNotFoundError(AppException):
    def __init__(self, report_id):
        super().__init__(
            message=f"التقرير برقم '{report_id}' غير موجود",
            status_code=404,
            error_code="REPORT_NOT_FOUND"
        )


class TemplateNotFoundError(AppException):
    def __init__(self, template_id):
        super().__init__(
            message=f"القالب برقم '{template_id}' غير موجود",
            status_code=404,
            error_code="TEMPLATE_NOT_FOUND"
        )


class PDFGenerationError(AppException):
    def __init__(self, reason):
        super().__init__(
            message=f"فشل توليد PDF: {reason}",
            status_code=500,
            error_code="PDF_GENERATION_ERROR"
        )


# ================================================
# File Exceptions
# ================================================
class FileUploadError(AppException):
    def __init__(self, reason):
        super().__init__(
            message=f"فشل رفع الملف: {reason}",
            status_code=400,
            error_code="FILE_UPLOAD_ERROR"
        )


class FileNotFoundError(AppException):
    def __init__(self, filename):
        super().__init__(
            message=f"الملف '{filename}' غير موجود",
            status_code=404,
            error_code="FILE_NOT_FOUND"
        )


class InvalidFileTypeError(AppException):
    def __init__(self, file_type, allowed_types):
        super().__init__(
            message=f"نوع الملف '{file_type}' غير مسموح. الأنواع المسموحة: {', '.join(allowed_types)}",
            status_code=400,
            error_code="INVALID_FILE_TYPE"
        )


# ================================================
# ECG Exceptions
# ================================================
class ECGModelNotFoundError(AppException):
    def __init__(self, model_key):
        super().__init__(
            message=f"نموذج ECG '{model_key}' غير موجود",
            status_code=404,
            error_code="ECG_MODEL_NOT_FOUND"
        )


class ECGProcessingError(AppException):
    def __init__(self, reason):
        super().__init__(
            message=f"فشل معالجة صورة ECG: {reason}",
            status_code=500,
            error_code="ECG_PROCESSING_ERROR"
        )


# ================================================
# General Exceptions
# ================================================
class ValidationError(AppException):
    def __init__(self, errors):
        if isinstance(errors, list):
            message = f"خطأ في التحقق من البيانات: {', '.join(errors)}"
        else:
            message = f"خطأ في التحقق من البيانات: {errors}"
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR"
        )


class DatabaseError(AppException):
    def __init__(self, reason):
        super().__init__(
            message=f"خطأ في قاعدة البيانات: {reason}",
            status_code=500,
            error_code="DATABASE_ERROR"
        )


# ================================================
# Service Exceptions
# ================================================
class ServiceUnavailableError(AppException):
    def __init__(self, service_name):
        super().__init__(
            message=f"الخدمة '{service_name}' غير متوفرة حالياً",
            status_code=503,
            error_code="SERVICE_UNAVAILABLE"
        )