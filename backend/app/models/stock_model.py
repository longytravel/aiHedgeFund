from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class Stock(BaseModel):
    __tablename__ = "stocks"

    ticker = Column(String(10), unique=True, index=True, nullable=False)  # Added length constraint
    name = Column(String(255), nullable=False)  # Added length constraint per architecture
    sector = Column(String(100), nullable=True)  # Added length constraint per architecture
    market_cap = Column(Numeric(15, 2), nullable=True)  # Changed to Numeric per architecture (GBP millions with decimals)

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
