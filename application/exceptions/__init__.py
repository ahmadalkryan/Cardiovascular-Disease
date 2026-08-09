# application/exceptions/__init__.py
"""Exceptions Package - Custom exceptions and Flask handlers"""

from .custom_exceptions import *
from .handlers import register_exception_handlers

__all__ = [
    # Base Exception
    'AppException',
    
    # Model Exceptions
    'ModelNotFoundError',
    'ModelLoadError',
    
    # Patient Exceptions
    'PatientNotFoundError',
    'PatientDataValidationError',
    
    # Report Exceptions 
    'ReportNotFoundError',
    'TemplateNotFoundError',
    'PDFGenerationError',
    
    # File Exceptions
    'FileUploadError',
    'FileNotFoundError',
    'InvalidFileTypeError',
    
    # ECG Exceptions
    'ECGModelNotFoundError',
    'ECGProcessingError',
    
    # General Exceptions
    'ValidationError',
    'DatabaseError',
    'ServiceUnavailableError',
    
    # Handlers
    'register_exception_handlers',
]