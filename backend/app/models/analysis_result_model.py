from sqlalchemy import Column, String, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class AnalysisResult(BaseModel):
    __tablename__ = "analysis_results"

    stock_id = Column(PG_UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=False, index=True)
    agent_name = Column(String, nullable=False, index=True)
    recommendation = Column(String, nullable=True) # e.g., "BUY", "SELL", "HOLD"
    confidence = Column(Float, nullable=True)
    reasoning = Column(Text, nullable=True) # Text for potentially long reasoning
    key_metrics = Column(JSONB, nullable=True) # JSONB for flexible storage of metrics

    # Relationship to Stock model
    stock = relationship("Stock", back_populates="analysis_results")

    def __repr__(self):
        return (
            f"<AnalysisResult(stock_id='{self.stock_id}', agent_name='{self.agent_name}', "
            f"recommendation='{self.recommendation}')>"
        )
