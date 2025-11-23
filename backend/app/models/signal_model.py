from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class Signal(BaseModel):
    __tablename__ = "signals"

    # Foreign key to Stock model
    stock_id = Column(PG_UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=False, index=True)
    signal_type = Column(String, nullable=False, index=True)
    score = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    source = Column(String, nullable=True) # Source can be null
    data = Column(JSONB, nullable=True) # JSONB for flexible data storage

    # Relationship to Stock model
    stock = relationship("Stock", back_populates="signals")

    def __repr__(self):
        return f"<Signal(stock_id='{self.stock_id}', signal_type='{self.signal_type}', score={self.score})>"
