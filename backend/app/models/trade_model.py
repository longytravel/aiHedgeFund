from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class Trade(BaseModel):
    __tablename__ = "trades"

    stock_id = Column(PG_UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=False, index=True)
    action = Column(String, nullable=False) # e.g., "BUY", "SELL"
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    outcome = Column(String, nullable=True) # e.g., "PROFIT", "LOSS", "BREAKEVEN"

    # Relationship to Stock model
    stock = relationship("Stock", back_populates="trades")

    def __repr__(self):
        return (
            f"<Trade(stock_id='{self.stock_id}', action='{self.action}', price={self.price}, "
            f"quantity={self.quantity})>"
        )
