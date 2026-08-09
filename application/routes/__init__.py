

# application/routes/__init__.py
"""Routes Package - Centralized route registration"""

from .page_routes import register_page_routes
from .prediction_routes import register_prediction_routes
from .ecg_routes import register_ecg_routes
from .batch_routes import register_batch_routes
from .patient_routes import register_patient_routes
from .report_routes import register_report_routes


def register_routes(app, data_service, prediction_service, config, ecg_service):
    """Register all route groups with the Flask application"""
    
    register_page_routes(app, config)
    register_prediction_routes(app, data_service, prediction_service, config)
    register_ecg_routes(app, ecg_service, config)
    register_batch_routes(app, prediction_service, data_service, config)
    register_patient_routes(app, data_service, prediction_service, config)


__all__ = ['register_routes']