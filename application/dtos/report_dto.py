# application/dtos/report_dto.py
"""Report DTO"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class ReportDTO:
    id: int
    report_uid: str
    template_id: int
    patient_uid: str
    data: Dict
    pdf_path: Optional[str] = None
    has_pdf: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    template_title: Optional[str] = None
    
    @classmethod
    def from_model(cls, report):
        if not report:
            return None
        return cls(
            id=report.id,
            report_uid=report.report_uid,
            template_id=report.template_id,
            patient_uid=report.patient_uid or '',
            data=report.get_data(),
            pdf_path=report.pdf_path,
            has_pdf=report.has_pdf,
            created_at=report.created_at.strftime('%Y-%m-%d %H:%M') if report.created_at else None,
            updated_at=report.updated_at.strftime('%Y-%m-%d %H:%M') if report.updated_at else None,
            template_title=report.template_title
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'report_uid': self.report_uid,
            'template_id': self.template_id,
            'template_title': self.template_title,
            'patient_uid': self.patient_uid,
            'data': self.data,
            'pdf_path': self.pdf_path,
            'has_pdf': self.has_pdf,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }