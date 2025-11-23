from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class ResearchQueue(BaseModel):
    __tablename__ = "research_queue"

    stock_id = Column(PG_UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=False, index=True)
    score = Column(Float, nullable=True) # Score can be null if not yet determined
    status = Column(String, nullable=False, index=True) # e.g., PENDING, IN_PROGRESS, COMPLETED

    # Relationship to Stock model
    stock = relationship("Stock", back_populates="research_queue_entries")

    def __repr__(self):
        return (
            f"<ResearchQueue(stock_id='{self.stock_id}', status='{self.status}', "
            f"score={self.score})>"
        )
