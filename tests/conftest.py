"""
Pytest configuration and fixtures for AIHedgeFund test suite.

Sprint 0 Setup: Mock LLM Provider for zero-cost testing
"""

import asyncio
from typing import Any, AsyncIterator, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# ============================================================================
# Pytest Configuration
# ============================================================================


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Mock LLM Provider (HP-01: Zero-Cost Testing)
# ============================================================================


class MockLLMResponse:
    """Mock LLM response for testing."""

    def __init__(self, content: str, model: str = "mock-gpt-4"):
        self.content = content
        self.model = model
        self.usage = {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}


class MockLLMProvider:
    """
    Mock LLM provider for zero-cost testing.

    Usage:
        mock_llm = MockLLMProvider()
        response = await mock_llm.generate("What is the stock price?")
        assert "bullish" in response.content.lower()

    Features:
    - Zero API costs (no real LLM calls)
    - Deterministic responses for reproducible tests
    - Configurable responses per test case
    - Token usage tracking
    """

    def __init__(self, default_response: str = "MOCK LLM RESPONSE"):
        self.default_response = default_response
        self.call_history: List[Dict[str, Any]] = []
        self._custom_responses: Dict[str, str] = {}

    async def generate(
        self,
        prompt: str,
        model: str = "mock-gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> MockLLMResponse:
        """Generate a mock LLM response."""
        # Record call for assertions
        self.call_history.append(
            {
                "prompt": prompt,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
        )

        # Return custom response if configured
        for keyword, response in self._custom_responses.items():
            if keyword.lower() in prompt.lower():
                return MockLLMResponse(response, model)

        # Return default response
        return MockLLMResponse(self.default_response, model)

    def set_response(self, keyword: str, response: str):
        """Configure custom response for prompts containing keyword."""
        self._custom_responses[keyword] = response

    def reset(self):
        """Reset call history and custom responses."""
        self.call_history = []
        self._custom_responses = {}


@pytest.fixture
def mock_llm():
    """Provide a fresh Mock LLM provider for each test."""
    provider = MockLLMProvider()
    yield provider
    provider.reset()


@pytest.fixture
def mock_llm_bullish(mock_llm):
    """Mock LLM configured for bullish analysis responses."""
    mock_llm.set_response(
        "analyze",
        """
        **Analysis: BULLISH**

        - Strong revenue growth (+25% YoY)
        - P/E ratio attractive at 12x vs sector 18x
        - Insider buying activity detected
        - Technical breakout above 200-day MA

        **Recommendation:** BUY
        **Confidence:** 8/10
        """,
    )
    return mock_llm


@pytest.fixture
def mock_llm_bearish(mock_llm):
    """Mock LLM configured for bearish analysis responses."""
    mock_llm.set_response(
        "analyze",
        """
        **Analysis: BEARISH**

        - Declining revenue (-10% YoY)
        - High debt-to-equity ratio (2.5x)
        - Insider selling detected
        - Technical breakdown below support

        **Recommendation:** SELL
        **Confidence:** 7/10
        """,
    )
    return mock_llm


# ============================================================================
# Database Fixtures (Epic 1)
# ============================================================================


@pytest.fixture(scope="session")
async def test_db_engine():
    """Create test database engine (SQLite in-memory for speed)."""
    # Use SQLite for fast testing (PostgreSQL for integration tests)
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    # Import models and create tables
    # from src.models.base import Base
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def db_session(test_db_engine) -> AsyncIterator[AsyncSession]:
    """Provide a clean database session for each test."""
    async_session = sessionmaker(
        test_db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()  # Rollback after each test


# ============================================================================
# API Client Fixtures (Epic 1-2)
# ============================================================================


@pytest.fixture
def mock_eodhd_client():
    """Mock EODHD API client."""
    client = MagicMock()
    client.get_fundamentals = AsyncMock(
        return_value={
            "General": {
                "Code": "BARC",
                "Name": "Barclays PLC",
                "Exchange": "LSE",
                "Sector": "Financial Services",
            },
            "Highlights": {
                "MarketCapitalization": 25000000000,
                "PERatio": 8.5,
                "DividendYield": 0.045,
            },
        }
    )
    return client


@pytest.fixture
def mock_cityfalcon_client():
    """Mock CityFALCON API client."""
    client = MagicMock()
    client.get_news = AsyncMock(
        return_value=[
            {
                "title": "Barclays reports strong Q3 earnings",
                "url": "https://example.com/news1",
                "published_at": "2025-11-22T09:00:00Z",
                "sentiment": "positive",
            }
        ]
    )
    return client


# ============================================================================
# Signal Bus Fixtures (Epic 1)
# ============================================================================


@pytest.fixture
def mock_signal_bus():
    """Mock signal bus for testing agent communication."""
    bus = MagicMock()
    bus.publish = AsyncMock()
    bus.subscribe = MagicMock()
    return bus


# ============================================================================
# Test Data Factories
# ============================================================================


@pytest.fixture
def sample_signal():
    """Factory for creating sample signals."""

    def _create_signal(
        ticker: str = "BARC.LSE",
        signal_type: str = "NEWS_ALERT",
        confidence: float = 0.8,
        data: Optional[Dict] = None,
    ):
        return {
            "ticker": ticker,
            "signal_type": signal_type,
            "confidence": confidence,
            "data": data or {"title": "Sample news", "sentiment": "positive"},
            "timestamp": "2025-11-22T10:00:00Z",
        }

    return _create_signal


@pytest.fixture
def sample_stock():
    """Factory for creating sample stock data."""

    def _create_stock(
        ticker: str = "BARC.LSE",
        name: str = "Barclays PLC",
        sector: str = "Financial Services",
    ):
        return {
            "ticker": ticker,
            "name": name,
            "sector": sector,
            "exchange": "LSE",
            "currency": "GBP",
        }

    return _create_stock
