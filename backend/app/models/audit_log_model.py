from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base_model import BaseModel

class AuditLog(BaseModel):
    __tablename__ = "audit_log"

    action = Column(String, nullable=False, index=True)
    details = Column(JSONB, nullable=True) # JSONB for detailed audit information
    user_id = Column(String, nullable=True) # Can be null for system-initiated actions

    def __repr__(self):
        return f"<AuditLog(action='{self.action}', user_id='{self.user_id}')>"
