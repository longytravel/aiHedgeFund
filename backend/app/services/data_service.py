from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock_model import Stock
from app.models.signal_model import Signal


class StockService:
    @staticmethod
    async def create_stock(
        db: AsyncSession, ticker: str, name: str, sector: Optional[str] = None, market_cap: Optional[int] = None
    ) -> Stock:
        stock = Stock(ticker=ticker, name=name, sector=sector, market_cap=market_cap)
        db.add(stock)
        await db.commit()
        await db.refresh(stock)
        return stock

    @staticmethod
    async def get_stock_by_ticker(db: AsyncSession, ticker: str) -> Optional[Stock]:
        result = await db.execute(select(Stock).where(Stock.ticker == ticker))
        return result.scalars().first()

    @staticmethod
    async def get_stock_by_id(db: AsyncSession, stock_id: UUID) -> Optional[Stock]:
        result = await db.execute(select(Stock).where(Stock.id == stock_id))
        return result.scalars().first()

    @staticmethod
    async def get_all_stocks(db: AsyncSession) -> List[Stock]:
        result = await db.execute(select(Stock))
        return result.scalars().all()

    @staticmethod
    async def update_stock(
        db: AsyncSession, stock_id: UUID, ticker: Optional[str] = None, name: Optional[str] = None, 
        sector: Optional[str] = None, market_cap: Optional[int] = None
    ) -> Optional[Stock]:
        stock = await StockService.get_stock_by_id(db, stock_id)
        if not stock:
            return None
        
        if ticker:
            stock.ticker = ticker
        if name:
            stock.name = name
        if sector:
            stock.sector = sector
        if market_cap:
            stock.market_cap = market_cap
            
        await db.commit()
        await db.refresh(stock)
        return stock

    @staticmethod
    async def delete_stock(db: AsyncSession, stock_id: UUID) -> bool:
        stock = await StockService.get_stock_by_id(db, stock_id)
        if not stock:
            return False
        
        await db.delete(stock)
        await db.commit()
        return True


class SignalService:
    @staticmethod
    async def create_signal(
        db: AsyncSession, stock_id: UUID, stock_ticker: str, signal_type: str,
        strength: int, agent_id: str, timestamp, data: Optional[dict] = None
    ) -> Signal:
        signal = Signal(
            stock_id=stock_id,
            stock_ticker=stock_ticker,
            type=signal_type,  # Maps to 'type' column in model
            strength=strength,
            agent_id=agent_id,
            timestamp=timestamp,
            data=data
        )
        db.add(signal)
        await db.commit()
        await db.refresh(signal)
        return signal

    @staticmethod
    async def get_signals_for_stock(db: AsyncSession, stock_id: UUID) -> List[Signal]:
        result = await db.execute(select(Signal).where(Signal.stock_id == stock_id))
        return result.scalars().all()
    
    @staticmethod
    async def get_signal_by_id(db: AsyncSession, signal_id: UUID) -> Optional[Signal]:
        result = await db.execute(select(Signal).where(Signal.id == signal_id))
        return result.scalars().first()
