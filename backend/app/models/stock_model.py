from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class Stock(BaseModel):
    __tablename__ = "stocks"

    ticker = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    sector = Column(String, nullable=True) # Sector can be null if not available
    market_cap = Column(BigInteger, nullable=True) # Market cap can be null, using BigInteger for large values

    # Define relationships (assuming other models will be defined later)
    # These relationships will be fully established once the other models are created
    signals = relationship("Signal", back_populates="stock", cascade="all, delete-orphan")
    analysis_results = relationship("AnalysisResult", back_populates="stock", cascade="all, delete-orphan")
    portfolio_positions = relationship("PortfolioPosition", back_populates="stock", cascade="all, delete-orphan")
    watchlist_entries = relationship("WatchlistEntry", back_populates="stock", cascade="all, delete-orphan")
    research_queue_entries = relationship("ResearchQueue", back_populates="stock", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="stock", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Stock(ticker='{self.ticker}', name='{self.name}')>"
