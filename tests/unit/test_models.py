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

    # Create signal with updated schema
    signal = Signal(
        stock_id=stock.id,
        stock_ticker="SIG.L",
        type="BULLISH_CROSSOVER",
        strength=85,  # Changed from score (0.85) to strength (85)
        agent_id="technical_analyst",
        timestamp=datetime.now(),
        data={"ma_50": 100, "ma_200": 95}
    )
    db_session.add(signal)
    await db_session.commit()

    assert signal.id is not None
    assert signal.data["ma_50"] == 100
    assert signal.stock_id == stock.id
    assert signal.stock_ticker == "SIG.L"
    assert signal.type == "BULLISH_CROSSOVER"
    assert signal.strength == 85
    assert signal.agent_id == "technical_analyst"

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


# Additional JSONB field tests (addressing review finding #6)
@pytest.mark.asyncio
async def test_analysis_result_jsonb_fields(db_session):
    """Test AnalysisResult model with JSONB key_metrics and risks fields."""
    from app.models.analysis_result_model import AnalysisResult

    # Create stock first (use unique ticker to avoid conflicts)
    stock = Stock(ticker="ANLYS.L", name="Analysis Test Company")
    db_session.add(stock)
    await db_session.commit()

    # Create analysis result with JSONB fields
    analysis = AnalysisResult(
        stock_id=stock.id,
        stock_ticker="ANLYS.L",
        agent_id="value_investor",
        recommendation="BUY",
        score=85,
        confidence="HIGH",
        reasoning="Strong fundamentals and undervalued",
        key_metrics={"pe_ratio": 12.5, "roe": 0.18, "debt_equity": 0.3},
        risks={"market_risk": "MEDIUM", "sector_risk": "LOW"},
        timestamp=datetime.now()
    )
    db_session.add(analysis)
    await db_session.commit()

    assert analysis.id is not None
    assert analysis.key_metrics["pe_ratio"] == 12.5
    assert analysis.risks["market_risk"] == "MEDIUM"


@pytest.mark.asyncio
async def test_agent_config_jsonb_parameters(db_session):
    """Test AgentConfig model with JSONB parameters field."""
    from app.models.agent_config_model import AgentConfig

    config = AgentConfig(
        agent_name="news_scanner",
        enabled=True,
        weight=1.5,
        parameters={"max_articles": 50, "sentiment_threshold": 0.7, "sources": ["BBC", "FT"]}
    )
    db_session.add(config)
    await db_session.commit()

    assert config.id is not None
    assert config.parameters["max_articles"] == 50
    assert "BBC" in config.parameters["sources"]


@pytest.mark.asyncio
async def test_audit_log_jsonb_details(db_session):
    """Test AuditLog model with JSONB details field."""
    from app.models.audit_log_model import AuditLog

    audit_entry = AuditLog(
        action="TRADE_EXECUTED",
        details={
            "stock_ticker": "VOD.L",
            "action": "BUY",
            "quantity": 1000,
            "price": 72.50,
            "reason": "Strong buy signals from 3 agents"
        },
        user_id="system"
    )
    db_session.add(audit_entry)
    await db_session.commit()

    assert audit_entry.id is not None
    assert audit_entry.details["stock_ticker"] == "VOD.L"
    assert audit_entry.details["quantity"] == 1000
