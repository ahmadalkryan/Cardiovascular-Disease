# infrastructure/models/setting.py
"""Settings Model - Store application settings"""

from infrastructure.database import db
from datetime import datetime
import json


class Setting(db.Model):
    """Application settings model"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='general')
    data_type = db.Column(db.String(20), default='string')
    description = db.Column(db.String(255))
    is_editable = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def get_value(self):
        """Get value with proper type conversion"""
        if self.value is None:
            return None
        
        if self.data_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.data_type == 'integer':
            return int(self.value) if self.value else 0
        elif self.data_type == 'float':
            return float(self.value) if self.value else 0.0
        elif self.data_type == 'json':
            return json.loads(self.value) if self.value else {}
        elif self.data_type == 'list':
            return [x.strip() for x in self.value.split(',') if x.strip()]
        else:
            return self.value
    
    def set_value(self, value):
        """Set value with proper type conversion"""
        if self.data_type == 'json' and not isinstance(value, str):
            self.value = json.dumps(value)
        elif self.data_type == 'list' and isinstance(value, list):
            self.value = ','.join(value)
        elif self.data_type == 'boolean':
            self.value = str(bool(value)).lower()
        else:
            self.value = str(value)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'key': self.key,
            'value': self.get_value(),
            'category': self.category,
            'data_type': self.data_type,
            'description': self.description,
            'is_editable': self.is_editable,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }