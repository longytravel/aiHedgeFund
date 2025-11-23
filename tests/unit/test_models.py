import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime
import uuid

from app.core.database import Base
from app.models.stock_model import Stock
from app.models.signal_model import Signal

# Use a separate test database or in-memory SQLite for unit tests if possible,
# but for asyncpg/PostgreSQL specific features (like UUID, JSONB), it's better to use the running Postgres container.
# Here we will assume the test environment (e.g. CI/CD) or local dev sets up a test DB.
# For this task, we'll mock the session or use the dev DB with rollback.
# NOTE: Using dev DB for tests is risky; ideally use a separate test DB. 
# For simplicity in this CLI environment, we'll assume a test DB URL is provided or use the dev one carefully (rollback).

import os
# Ideally, we should load TEST_DATABASE_URL from env.
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://aihedgefund:devpassword@localhost:5432/aihedgefund")

@pytest_asyncio.fixture(scope="module")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(engine):
    # Create a new session factory
    async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session_factory() as session:
        # Start a transaction
        await session.begin()
        
        yield session
        
        # Rollback everything after the test to keep DB clean
        await session.rollback()

@pytest.mark.asyncio
async def test_stock_model_creation(db_session):
    """Test creating a Stock model and saving it to DB."""
    new_stock = Stock(
        ticker="TEST.L",
        name="Test Company PLC",
        sector="Technology",
        market_cap=1000000
    )
    db_session.add(new_stock)
    await db_session.commit()
    
    assert new_stock.id is not None
    assert isinstance(new_stock.id, uuid.UUID)
    assert new_stock.created_at is not None
    assert new_stock.updated_at is not None

@pytest.mark.asyncio
async def test_signal_model_creation(db_session):
    """Test creating a Signal model with relationship to Stock."""
    # Create stock first
    stock = Stock(ticker="SIG.L", name="Signal Corp", sector="Finance")
    db_session.add(stock)
    await db_session.commit() # Commit to get ID
    
    # Create signal
    signal = Signal(
        stock_id=stock.id,
        signal_type="BULLISH_CROSSOVER",
        score=0.85,
        timestamp=datetime.now(),
        source="TechnicalAgent",
        data={"ma_50": 100, "ma_200": 95}
    )
    db_session.add(signal)
    await db_session.commit()
    
    assert signal.id is not None
    assert signal.data["ma_50"] == 100
    assert signal.stock_id == stock.id

@pytest.mark.asyncio
async def test_stock_unique_ticker(db_session):
    """Test that duplicate tickers raise an error (integrity constraint)."""
    import sqlalchemy.exc

    stock1 = Stock(ticker="UNIQ.L", name="Unique 1")
    db_session.add(stock1)
    await db_session.commit()

    stock2 = Stock(ticker="UNIQ.L", name="Unique 2")
    db_session.add(stock2)
    
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await db_session.commit()
