from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class Signal(BaseModel):
    __tablename__ = "signals"

    # Foreign key to Stock model
    stock_id = Column(PG_UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=False, index=True)
    stock_ticker = Column(String(10), nullable=False, index=True)  # Added per architecture spec
    type = Column(String(50), nullable=False, index=True)  # Renamed from signal_type per architecture
    strength = Column(Integer, nullable=False)  # Renamed from score, changed to Integer (0-100)
    agent_id = Column(String(50), nullable=False, index=True)  # Added per architecture spec
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    data = Column(JSONB, nullable=True) # JSONB for flexible data storage

    # Relationship to Stock model
    stock = relationship("Stock", back_populates="signals")

    def __repr__(self):
        return f"<Signal(stock_ticker='{self.stock_ticker}', type='{self.type}', strength={self.strength})>"
