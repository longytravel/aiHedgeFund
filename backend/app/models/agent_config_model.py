from sqlalchemy import Column, String, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base_model import BaseModel

class AgentConfig(BaseModel):
    __tablename__ = "agent_config"

    agent_name = Column(String, unique=True, nullable=False, index=True)
    enabled = Column(Boolean, default=True, nullable=False)
    weight = Column(Float, default=1.0, nullable=False)
    parameters = Column(JSONB, nullable=True) # JSONB for flexible agent parameters

    def __repr__(self):
        return (
            f"<AgentConfig(agent_name='{self.agent_name}', enabled={self.enabled}, "
            f"weight={self.weight})>"
        )
