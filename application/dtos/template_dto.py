# application/dtos/template_dto.py
"""Template DTO"""

from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class TemplateDTO:
    id: int
    title: str
    description: Optional[str]
    structure: List[Dict]
    category: str
    is_active: bool
    report_count: int = 0
    field_count: int = 0
    
    @classmethod
    def from_model(cls, template):
        if not template:
            return None
        return cls(
            id=template.id,
            title=template.title,
            description=template.description,
            structure=template.get_structure(),
            category=template.category,
            is_active=template.is_active,
            report_count=template.report_count,
            field_count=template.field_count
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'structure': self.structure,
            'category': self.category,
            'is_active': self.is_active,
            'report_count': self.report_count,
            'field_count': self.field_count
        }