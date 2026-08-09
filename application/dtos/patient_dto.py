# application/dtos/patient_dto.py
"""Patient DTO"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PatientDTO:
    patient_id: str
    patient_uid: str
    age: int
    sex: int
    prediction: int
    probability: float
    model_used: str
    created_at: Optional[datetime] = None
    date: Optional[str] = None
    time: Optional[str] = None
    
    @classmethod
    def from_model(cls, patient):
        if not patient:
            return None
        return cls(
            patient_id=patient.patient_id,
            patient_uid=patient.patient_uid,
            age=patient.age,
            sex=patient.sex,
            prediction=patient.prediction,
            probability=patient.probability,
            model_used=patient.model_used,
            created_at=patient.created_at,
            date=patient.date,
            time=patient.time
        )
    
    def to_dict(self):
        return {
            'patient_id': self.patient_id,
            'patient_uid': self.patient_uid,
            'age': self.age,
            'sex': self.sex,
            'prediction': self.prediction,
            'result': 'DISEASE' if self.prediction == 1 else 'HEALTHY',
            'result_ar': 'مريض' if self.prediction == 1 else 'سليم',
            'probability': round(self.probability * 100, 1),
            'probability_percent': f"{self.probability * 100:.1f}%",
            'model_used': self.model_used,
            'date': self.date,
            'time': self.time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }