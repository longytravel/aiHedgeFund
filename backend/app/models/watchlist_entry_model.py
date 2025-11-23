from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class WatchlistEntry(BaseModel):
    __tablename__ = "watchlist_entries"

    stock_id = Column(PG_UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=False, index=True)
    trigger_type = Column(String, nullable=True)
    trigger_value = Column(Float, nullable=True)
    thesis = Column(Text, nullable=True) # Text for detailed thesis
    expiry_date = Column(DateTime(timezone=True), nullable=True)

    # Relationship to Stock model
    stock = relationship("Stock", back_populates="watchlist_entries")

    def __repr__(self):
        return (
            f"<WatchlistEntry(stock_id='{self.stock_id}', trigger_type='{self.trigger_type}', "
            f"expiry_date='{self.expiry_date}')>"
        )
