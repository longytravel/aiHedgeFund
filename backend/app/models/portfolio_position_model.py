from sqlalchemy import Column, DateTime, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class PortfolioPosition(BaseModel):
    __tablename__ = "portfolio_positions"

    stock_id = Column(PG_UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=False, index=True)
    entry_date = Column(DateTime(timezone=True), nullable=False)
    entry_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    stop_loss = Column(Float, nullable=True)
    target = Column(Float, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True) # For soft delete

    # Relationship to Stock model
    stock = relationship("Stock", back_populates="portfolio_positions")

    def __repr__(self):
        return (
            f"<PortfolioPosition(stock_id='{self.stock_id}', quantity={self.quantity}, "
            f"entry_price={self.entry_price})>"
        )
