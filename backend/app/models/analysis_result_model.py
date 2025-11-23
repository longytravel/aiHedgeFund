from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class AnalysisResult(BaseModel):
    __tablename__ = "analysis_results"

    stock_id = Column(PG_UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=False, index=True)
    stock_ticker = Column(String(10), nullable=False, index=True)  # Added per architecture spec
    agent_id = Column(String(50), nullable=False, index=True)  # Renamed from agent_name per architecture
    recommendation = Column(String(20), nullable=False)  # Made non-nullable per architecture
    score = Column(Integer, nullable=False)  # Added per architecture (0-100 conviction)
    confidence = Column(String(10), nullable=False)  # Changed to String per architecture (LOW/MEDIUM/HIGH)
    reasoning = Column(Text, nullable=False)  # Made non-nullable per architecture
    key_metrics = Column(JSONB, nullable=True) # JSONB for flexible storage of metrics
    risks = Column(JSONB, nullable=True)  # Added per architecture spec
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)  # Added per architecture spec

    # Relationship to Stock model
    stock = relationship("Stock", back_populates="analysis_results")

    def __repr__(self):
        return (
            f"<AnalysisResult(stock_ticker='{self.stock_ticker}', agent_id='{self.agent_id}', "
            f"recommendation='{self.recommendation}', score={self.score})>"
        )
