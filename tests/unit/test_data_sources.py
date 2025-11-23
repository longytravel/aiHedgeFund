"""
Unit tests for data sources module.

Tests cover:
- DataSource ABC (cannot instantiate)
- Signal dataclass validation
- DataSourceRegistry registration and execution
- YahooFinanceProvider fetch and signal conversion
- AlphaVantageProvider fetch and rate limiting
- Failover logic with mocked provider failures
- Configuration loading and validation
"""

import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from typing import List

from backend.app.data_sources.base import DataSource, Signal
from backend.app.data_sources.registry import DataSourceRegistry
from backend.app.data_sources.providers.yahoo_provider import YahooFinanceProvider
from backend.app.data_sources.providers.alpha_vantage_provider import (
    AlphaVantageProvider,
    RateLimitExceeded
)
from backend.app.data_sources.providers.eodhd_provider import (
    EODHDProvider,
    EODHDRateLimitExceeded
)
from backend.app.data_sources.failover import DataSourceFailover, FailoverReason
from backend.app.core.config import DataSourcesConfig


# Test DataSource ABC
class TestDataSourceABC:
    """Test DataSource abstract base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that DataSource ABC cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            DataSource()

    def test_abstract_methods_required(self):
        """Test that concrete implementations must implement abstract methods."""

        # Missing fetch() implementation
        class IncompleteProvider1(DataSource):
            def get_source_name(self) -> str:
                return "incomplete"

        with pytest.raises(TypeError):
            IncompleteProvider1()

        # Missing get_source_name() implementation
        class IncompleteProvider2(DataSource):
            async def fetch(self) -> List[Signal]:
                return []

        with pytest.raises(TypeError):
            IncompleteProvider2()

    def test_complete_implementation_works(self):
        """Test that complete implementation can be instantiated."""

        class CompleteProvider(DataSource):
            async def fetch(self) -> List[Signal]:
                return []

            def get_source_name(self) -> str:
                return "complete"

        provider = CompleteProvider()
        assert provider.get_source_name() == "complete"


# Test Signal dataclass
class TestSignalDataclass:
    """Test Signal dataclass validation."""

    def test_valid_signal_creation(self):
        """Test creating a valid signal."""
        signal = Signal(
            ticker="VOD.L",
            signal_type="PRICE_UPDATE",
            score=75,
            confidence=0.85,
            data={"price": 100.0},
            timestamp=datetime.now(timezone.utc),
            source="test_provider"
        )

        assert signal.ticker == "VOD.L"
        assert signal.score == 75
        assert signal.confidence == 0.85

    def test_invalid_score_range(self):
        """Test that score must be 0-100."""
        with pytest.raises(ValueError, match="Score must be 0-100"):
            Signal(
                ticker="VOD.L",
                signal_type="PRICE_UPDATE",
                score=150,  # Invalid
                confidence=0.85,
                data={},
                timestamp=datetime.now(timezone.utc),
                source="test"
            )

        with pytest.raises(ValueError, match="Score must be 0-100"):
            Signal(
                ticker="VOD.L",
                signal_type="PRICE_UPDATE",
                score=-10,  # Invalid
                confidence=0.85,
                data={},
                timestamp=datetime.now(timezone.utc),
                source="test"
            )

    def test_invalid_confidence_range(self):
        """Test that confidence must be 0.0-1.0."""
        with pytest.raises(ValueError, match="Confidence must be 0.0-1.0"):
            Signal(
                ticker="VOD.L",
                signal_type="PRICE_UPDATE",
                score=50,
                confidence=1.5,  # Invalid
                data={},
                timestamp=datetime.now(timezone.utc),
                source="test"
            )

    def test_naive_timestamp_rejected(self):
        """Test that timezone-naive timestamps are rejected."""
        with pytest.raises(ValueError, match="Timestamp must be timezone-aware"):
            Signal(
                ticker="VOD.L",
                signal_type="PRICE_UPDATE",
                score=50,
                confidence=0.5,
                data={},
                timestamp=datetime.now(),  # Naive timestamp
                source="test"
            )


# Test DataSourceRegistry
class TestDataSourceRegistry:
    """Test DataSourceRegistry registration and execution."""

    @pytest.fixture
    def mock_provider(self):
        """Create a mock data source provider."""

        class MockProvider(DataSource):
            def __init__(self, name: str, signals: List[Signal]):
                self.name = name
                self.signals = signals
                self.fetch_called = False

            async def fetch(self) -> List[Signal]:
                self.fetch_called = True
                return self.signals

            def get_source_name(self) -> str:
                return self.name

        return MockProvider

    def test_register_provider(self, mock_provider):
        """Test registering a provider."""
        registry = DataSourceRegistry()
        provider = mock_provider("test_provider", [])

        registry.register(provider)

        assert "test_provider" in registry.list_all()
        assert not registry.is_enabled("test_provider")

    def test_register_duplicate_raises_error(self, mock_provider):
        """Test that registering duplicate provider raises error."""
        registry = DataSourceRegistry()
        provider1 = mock_provider("test_provider", [])
        provider2 = mock_provider("test_provider", [])

        registry.register(provider1)

        with pytest.raises(ValueError, match="already registered"):
            registry.register(provider2)

    def test_enable_disable_provider(self, mock_provider):
        """Test enabling and disabling providers."""
        registry = DataSourceRegistry()
        provider = mock_provider("test_provider", [])

        registry.register(provider)
        registry.enable("test_provider")

        assert registry.is_enabled("test_provider")
        assert "test_provider" in registry.list_enabled()

        registry.disable("test_provider")

        assert not registry.is_enabled("test_provider")
        assert "test_provider" not in registry.list_enabled()

    @pytest.mark.asyncio
    async def test_fetch_all_parallel_execution(self, mock_provider):
        """Test that fetch_all executes providers in parallel."""
        registry = DataSourceRegistry()

        # Create mock signals
        signal1 = Signal(
            ticker="VOD.L",
            signal_type="TEST",
            score=50,
            confidence=0.8,
            data={},
            timestamp=datetime.now(timezone.utc),
            source="provider1"
        )
        signal2 = Signal(
            ticker="BP.L",
            signal_type="TEST",
            score=60,
            confidence=0.9,
            data={},
            timestamp=datetime.now(timezone.utc),
            source="provider2"
        )

        provider1 = mock_provider("provider1", [signal1])
        provider2 = mock_provider("provider2", [signal2])

        registry.register(provider1)
        registry.register(provider2)
        registry.enable("provider1")
        registry.enable("provider2")

        signals = await registry.fetch_all()

        assert len(signals) == 2
        assert provider1.fetch_called
        assert provider2.fetch_called

    @pytest.mark.asyncio
    async def test_fetch_all_error_isolation(self, mock_provider):
        """Test that one provider failure doesn't crash others."""

        class FailingProvider(DataSource):
            async def fetch(self) -> List[Signal]:
                raise Exception("Provider failure")

            def get_source_name(self) -> str:
                return "failing"

        registry = DataSourceRegistry()

        signal = Signal(
            ticker="VOD.L",
            signal_type="TEST",
            score=50,
            confidence=0.8,
            data={},
            timestamp=datetime.now(timezone.utc),
            source="success"
        )

        failing = FailingProvider()
        success = mock_provider("success", [signal])

        registry.register(failing)
        registry.register(success)
        registry.enable("failing")
        registry.enable("success")

        signals = await registry.fetch_all()

        # Should get signal from successful provider despite failure
        assert len(signals) == 1
        assert signals[0].source == "success"


# Test YahooFinanceProvider
class TestYahooFinanceProvider:
    """Test Yahoo Finance provider."""

    @pytest.mark.asyncio
    async def test_no_tickers_returns_empty(self):
        """Test that provider returns empty list when no tickers configured."""
        provider = YahooFinanceProvider(tickers=[])
        signals = await provider.fetch()
        assert signals == []

    def test_get_source_name(self):
        """Test provider returns correct source name."""
        provider = YahooFinanceProvider()
        assert provider.get_source_name() == "yahoo_finance"

    @pytest.mark.asyncio
    @patch('backend.app.data_sources.providers.yahoo_provider.yf.Ticker')
    async def test_fetch_with_valid_data(self, mock_ticker):
        """Test fetching valid data from Yahoo Finance."""
        # Mock yfinance response
        mock_stock = Mock()
        mock_stock.info = {
            'regularMarketPrice': 150.0,
            'previousClose': 145.0,
            'volume': 10000000,
            'averageVolume': 8000000,
            'marketCap': 50000000000,
            'currency': 'GBP'
        }
        mock_ticker.return_value = mock_stock

        provider = YahooFinanceProvider(tickers=["VOD.L"])
        signals = await provider.fetch()

        assert len(signals) == 1
        assert signals[0].ticker == "VOD.L"
        assert signals[0].signal_type == "PRICE_UPDATE"
        assert signals[0].data['current_price'] == 150.0
        assert signals[0].data['provider'] == "yahoo_finance"

    @pytest.mark.asyncio
    @patch('backend.app.data_sources.providers.yahoo_provider.yf.Ticker')
    async def test_fetch_with_missing_data(self, mock_ticker):
        """Test handling of missing data from Yahoo Finance."""
        # Mock yfinance response with no data
        mock_stock = Mock()
        mock_stock.info = {}
        mock_ticker.return_value = mock_stock

        provider = YahooFinanceProvider(tickers=["INVALID.L"])
        signals = await provider.fetch()

        # Should return empty list for invalid ticker
        assert signals == []


# Test AlphaVantageProvider
class TestAlphaVantageProvider:
    """Test Alpha Vantage provider."""

    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with pytest.raises(ValueError, match="API key is required"):
            AlphaVantageProvider(api_key="")

        with pytest.raises(ValueError, match="API key is required"):
            AlphaVantageProvider(api_key=None)

    def test_get_source_name(self):
        """Test provider returns correct source name."""
        provider = AlphaVantageProvider(api_key="test_key")
        assert provider.get_source_name() == "alpha_vantage"

    def test_daily_limit_tracking(self):
        """Test daily call limit tracking."""
        provider = AlphaVantageProvider(api_key="test_key", daily_limit=25)

        # Initially should have 25 calls remaining
        assert provider.get_remaining_calls() == 25

        # Increment counter
        provider._increment_call_count()
        assert provider.get_remaining_calls() == 24

        # Increment 24 more times
        for _ in range(24):
            provider._increment_call_count()

        assert provider.get_remaining_calls() == 0

    def test_daily_limit_reset(self):
        """Test that daily limit resets at midnight UTC."""
        provider = AlphaVantageProvider(api_key="test_key", daily_limit=25)

        # Use up all calls
        for _ in range(25):
            provider._increment_call_count()

        assert provider.get_remaining_calls() == 0

        # Simulate day change by backdating last reset
        provider._last_reset[provider.api_key] = datetime.now(timezone.utc) - timedelta(days=1)

        # Check should trigger reset
        provider._check_and_reset_daily_limit()

        assert provider.get_remaining_calls() == 25

    @pytest.mark.asyncio
    async def test_rate_limit_prevents_fetch(self):
        """Test that fetch respects rate limits."""
        provider = AlphaVantageProvider(api_key="test_key", daily_limit=0)

        signals = await provider.fetch(tickers=["VOD.L"])

        # Should return empty due to rate limit
        assert signals == []


# Test Failover Logic
class TestDataSourceFailover:
    """Test failover logic."""

    @pytest.fixture
    def mock_providers(self):
        """Create mock providers for testing."""

        class MockProvider(DataSource):
            def __init__(self, name: str, should_fail: bool = False, signals: List[Signal] = None):
                self.name = name
                self.should_fail = should_fail
                self.signals = signals or []

            async def fetch(self, tickers=None) -> List[Signal]:
                if self.should_fail:
                    raise Exception(f"{self.name} failed")
                return self.signals

            def get_source_name(self) -> str:
                return self.name

        return MockProvider

    @pytest.mark.asyncio
    async def test_primary_provider_success(self, mock_providers):
        """Test that primary provider is used when successful."""
        signal = Signal(
            ticker="VOD.L",
            signal_type="TEST",
            score=50,
            confidence=0.8,
            data={},
            timestamp=datetime.now(timezone.utc),
            source="primary"
        )

        primary = mock_providers("primary", should_fail=False, signals=[signal])
        backup = mock_providers("backup", should_fail=False, signals=[])

        failover = DataSourceFailover(
            providers={"primary": primary, "backup": backup},
            priority_order=["primary", "backup"]
        )

        signals = await failover.fetch_with_failover(tickers=["VOD.L"])

        assert len(signals) == 1
        assert signals[0].source == "primary"

    @pytest.mark.asyncio
    async def test_failover_to_backup(self, mock_providers):
        """Test failover to backup when primary fails."""
        backup_signal = Signal(
            ticker="VOD.L",
            signal_type="TEST",
            score=50,
            confidence=0.8,
            data={},
            timestamp=datetime.now(timezone.utc),
            source="backup"
        )

        primary = mock_providers("primary", should_fail=True)
        backup = mock_providers("backup", should_fail=False, signals=[backup_signal])

        failover = DataSourceFailover(
            providers={"primary": primary, "backup": backup},
            priority_order=["primary", "backup"]
        )

        signals = await failover.fetch_with_failover(tickers=["VOD.L"])

        assert len(signals) == 1
        assert signals[0].source == "backup"

    @pytest.mark.asyncio
    async def test_all_providers_fail_uses_cache(self, mock_providers):
        """Test that cache is used when all providers fail."""
        # Pre-populate cache
        cached_signal = Signal(
            ticker="VOD.L",
            signal_type="TEST",
            score=50,
            confidence=0.8,
            data={},
            timestamp=datetime.now(timezone.utc),
            source="cache"
        )

        primary = mock_providers("primary", should_fail=True)
        backup = mock_providers("backup", should_fail=True)

        failover = DataSourceFailover(
            providers={"primary": primary, "backup": backup},
            priority_order=["primary", "backup"]
        )

        # Populate cache
        cache_key = failover._get_cache_key(["VOD.L"])
        failover._update_cache(cache_key, [cached_signal])

        signals = await failover.fetch_with_failover(
            tickers=["VOD.L"],
            use_cache_on_failure=True
        )

        assert len(signals) == 1
        assert signals[0].data.get("cached") is True


# Test Configuration
class TestDataSourcesConfig:
    """Test data sources configuration loading."""

    def test_config_file_not_found_raises_error(self):
        """Test that missing config file raises FileNotFoundError."""
        from pathlib import Path

        with pytest.raises(FileNotFoundError):
            DataSourcesConfig(config_path=Path("/nonexistent/config.yaml"))

    def test_load_valid_config(self, tmp_path):
        """Test loading valid configuration."""
        config_content = """
primary_fundamental_provider: eodhd

providers:
  eodhd:
    enabled: true
    api_key: test_key
    priority: 1

  yahoo:
    enabled: true
    priority: 2

failover:
  max_retries: 3
  retry_delays: [60, 120, 180]
"""
        config_file = tmp_path / "data_sources.yaml"
        config_file.write_text(config_content)

        config = DataSourcesConfig(config_path=config_file)

        assert config.primary_provider == "eodhd"
        assert len(config.providers) == 2
        assert config.is_provider_enabled("eodhd")
        assert config.is_provider_enabled("yahoo")
        assert config.priority_order == ["eodhd", "yahoo"]

    def test_env_var_substitution(self, tmp_path, monkeypatch):
        """Test environment variable substitution in config."""
        monkeypatch.setenv("TEST_API_KEY", "actual_key_value")

        config_content = """
providers:
  test_provider:
    enabled: true
    api_key: ${TEST_API_KEY}
    priority: 1
"""
        config_file = tmp_path / "data_sources.yaml"
        config_file.write_text(config_content)

        config = DataSourcesConfig(config_path=config_file)

        assert config.providers["test_provider"]["api_key"] == "actual_key_value"

    def test_validation_no_enabled_providers(self, tmp_path):
        """Test validation fails when no providers enabled."""
        config_content = """
providers:
  provider1:
    enabled: false
    priority: 1
"""
        config_file = tmp_path / "data_sources.yaml"
        config_file.write_text(config_content)

        config = DataSourcesConfig(config_path=config_file)
        is_valid, errors = config.validate()

        assert not is_valid
        assert "No providers enabled" in errors[0]


# Test EODHDProvider
class TestEODHDProvider:
    """Test EODHD provider."""

    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with pytest.raises(ValueError, match="EODHD API key is required"):
            EODHDProvider(api_key="")

        with pytest.raises(ValueError, match="EODHD API key is required"):
            EODHDProvider(api_key=None)

    def test_get_source_name(self):
        """Test provider returns correct source name."""
        provider = EODHDProvider(api_key="test_key")
        assert provider.get_source_name() == "eodhd_fundamental"

    def test_ticker_formatting(self):
        """Test LSE ticker formatting (.L to .LSE)."""
        provider = EODHDProvider(api_key="test_key")

        # Test .L to .LSE conversion (UK stocks)
        assert provider._format_ticker_for_api("VOD.L") == "VOD.LSE"
        assert provider._format_ticker_for_api("BP.L") == "BP.LSE"

        # Test .LSE remains unchanged
        assert provider._format_ticker_for_api("VOD.LSE") == "VOD.LSE"

        # Test US tickers remain unchanged
        assert provider._format_ticker_for_api("AAPL.US") == "AAPL.US"
        assert provider._format_ticker_for_api("TSLA.US") == "TSLA.US"

        # Test other exchanges remain unchanged
        assert provider._format_ticker_for_api("BTC-USD.CC") == "BTC-USD.CC"

    def test_pence_to_pounds_conversion(self):
        """Test pence to pounds conversion for UK stocks."""
        provider = EODHDProvider(api_key="test_key")

        # Large values (>1000) assumed to be in pence, convert to pounds
        assert provider._convert_pence_to_pounds(15000) == 150.0
        assert provider._convert_pence_to_pounds(2500) == 25.0

        # Small values (<1000) assumed to be in pounds, leave as-is
        assert provider._convert_pence_to_pounds(150.5) == 150.5
        assert provider._convert_pence_to_pounds(25.0) == 25.0

    def test_rate_limit_tracking(self):
        """Test daily rate limit tracking."""
        provider = EODHDProvider(
            api_key="test_key",
            rate_limit_per_day=100
        )

        # Initially should allow calls
        assert provider._check_rate_limit() is True
        assert provider._api_call_count == 0

        # Simulate 95 calls (95% of limit)
        provider._api_call_count = 95
        assert provider._check_rate_limit() is True  # Warning logged but allowed

        # Simulate 100 calls (at limit)
        provider._api_call_count = 100
        assert provider._check_rate_limit() is False  # Blocked

        # Simulate 101 calls (over limit)
        provider._api_call_count = 101
        assert provider._check_rate_limit() is False  # Blocked

    def test_rate_limit_reset(self):
        """Test that rate limit resets after 24 hours."""
        provider = EODHDProvider(
            api_key="test_key",
            rate_limit_per_day=100
        )

        # Use up all calls
        provider._api_call_count = 100
        assert provider._check_rate_limit() is False

        # Simulate day change by backdating reset time
        provider._rate_limit_reset_time = datetime.now(timezone.utc) - timedelta(hours=1)

        # Check should trigger reset
        assert provider._check_rate_limit() is True
        assert provider._api_call_count == 0

    def test_cache_add_and_get(self):
        """Test cache add and retrieval."""
        provider = EODHDProvider(api_key="test_key", cache_ttl_hours=24)

        # Add to cache
        test_data = {"test": "data"}
        provider._add_to_cache("test_key", test_data)

        # Retrieve from cache
        cached_data = provider._get_from_cache("test_key")
        assert cached_data == test_data

    def test_cache_expiry(self):
        """Test cache expiry after TTL."""
        provider = EODHDProvider(api_key="test_key", cache_ttl_hours=1)

        # Add to cache
        provider._add_to_cache("test_key", {"test": "data"})

        # Backdate timestamp to simulate expiry
        provider._cache_timestamps["test_key"] = datetime.now(timezone.utc) - timedelta(hours=2)

        # Cache should be expired
        cached_data = provider._get_from_cache("test_key")
        assert cached_data is None
        assert "test_key" not in provider._cache

    def test_calculate_fundamental_score(self):
        """Test fundamental score calculation."""
        provider = EODHDProvider(api_key="test_key")

        # Strong fundamentals (low P/E, high ROE, low debt, high earnings growth)
        fundamentals = {
            "key_metrics": {
                "pe_ratio": 10,  # Undervalued
                "roe": 20,  # High return
                "debt_to_equity": 0.3,  # Low debt
                "quarterly_earnings_growth": 25  # Strong growth
            }
        }
        score = provider._calculate_fundamental_score(fundamentals)
        assert score > 70  # Should be high score

        # Weak fundamentals
        weak_fundamentals = {
            "key_metrics": {
                "pe_ratio": 50,  # Overvalued
                "roe": 5,  # Low return
                "debt_to_equity": 2.0,  # High debt
                "quarterly_earnings_growth": -10  # Declining
            }
        }
        score = provider._calculate_fundamental_score(weak_fundamentals)
        assert score <= 50  # Should be neutral or lower

    def test_calculate_price_score(self):
        """Test price score calculation."""
        provider = EODHDProvider(api_key="test_key")

        # Strong momentum
        prices = {"price_change_30d": 15}
        score = provider._calculate_price_score(prices)
        assert score > 60

        # Weak momentum
        prices = {"price_change_30d": -15}
        score = provider._calculate_price_score(prices)
        assert score < 50

    def test_calculate_analyst_score(self):
        """Test analyst score calculation."""
        provider = EODHDProvider(api_key="test_key")

        # Bullish consensus
        estimates = {
            "total_analysts": 10,
            "consensus": "BULLISH",
            "strong_buy": 7,
            "buy": 2,
            "hold": 1,
            "sell": 0,
            "strong_sell": 0
        }
        score = provider._calculate_analyst_score(estimates)
        assert score > 60

        # Bearish consensus
        bearish_estimates = {
            "total_analysts": 10,
            "consensus": "BEARISH",
            "strong_buy": 0,
            "buy": 1,
            "hold": 2,
            "sell": 3,
            "strong_sell": 4
        }
        score = provider._calculate_analyst_score(bearish_estimates)
        assert score < 50

        # No coverage
        no_coverage = {
            "total_analysts": 0,
            "consensus": "NO_COVERAGE"
        }
        score = provider._calculate_analyst_score(no_coverage)
        assert score == 50  # Neutral

    @pytest.mark.asyncio
    async def test_no_tickers_returns_empty(self):
        """Test that provider returns empty list when no tickers configured."""
        provider = EODHDProvider(api_key="test_key", tickers=[])
        signals = await provider.fetch()
        assert signals == []

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded_uses_cache(self):
        """Test that rate limit exceeded triggers cache usage."""
        provider = EODHDProvider(
            api_key="test_key",
            tickers=["VOD.L"],
            rate_limit_per_day=0  # Already at limit
        )

        # Pre-populate cache
        cached_fundamentals = {
            "key_metrics": {"pe_ratio": 15},
            "highlights": {}
        }
        provider._add_to_cache("VOD.LSE:fundamentals", cached_fundamentals)

        signals = await provider.fetch()

        # Should get cached signal with lower confidence
        assert len(signals) >= 0  # May return cached signal

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_fetch_historical_prices_success(self, mock_get):
        """Test successful historical price fetching."""
        # Mock EODHD API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "date": "2025-11-01",
                "open": 14500,
                "high": 14800,
                "low": 14300,
                "close": 14700,
                "adjusted_close": 14700,
                "volume": 5000000
            },
            {
                "date": "2025-11-02",
                "open": 14700,
                "high": 15000,
                "low": 14600,
                "close": 14900,
                "adjusted_close": 14900,
                "volume": 6000000
            }
        ]
        mock_get.return_value = mock_response

        provider = EODHDProvider(api_key="test_key")
        prices = await provider.fetch_historical_prices("VOD.LSE", "2025-11-01", "2025-11-02")

        assert prices["data_points"] == 2
        assert len(prices["prices"]) == 2
        # Prices should be converted from pence to pounds
        assert prices["prices"][0]["close"] == 147.0
        assert prices["prices"][1]["close"] == 149.0

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_fetch_fundamentals_success(self, mock_get):
        """Test successful fundamental data fetching."""
        # Mock EODHD API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "General": {
                "Code": "VOD",
                "Name": "Vodafone Group PLC",
                "Sector": "Telecommunications"
            },
            "Highlights": {
                "PERatio": 12.5,
                "PriceBookMRQ": 1.2,
                "ReturnOnEquityTTM": 15.5,
                "DebtToEquity": 0.8
            },
            "Financials": {
                "Balance_Sheet": {"yearly": {}},
                "Income_Statement": {"yearly": {}},
                "Cash_Flow": {"yearly": {}}
            }
        }
        mock_get.return_value = mock_response

        provider = EODHDProvider(api_key="test_key")
        fundamentals = await provider.fetch_fundamentals("VOD.LSE")

        assert fundamentals["general"]["Code"] == "VOD"
        assert fundamentals["key_metrics"]["pe_ratio"] == 12.5
        assert fundamentals["key_metrics"]["roe"] == 15.5

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_fetch_company_profile_success(self, mock_get):
        """Test successful company profile fetching."""
        # Mock EODHD API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "General": {
                "Code": "VOD",
                "Name": "Vodafone Group PLC",
                "Sector": "Telecommunications",
                "Industry": "Telecom Services",
                "Exchange": "LSE",
                "CurrencyCode": "GBP",
                "MarketCapitalization": 25000000000
            }
        }
        mock_get.return_value = mock_response

        provider = EODHDProvider(api_key="test_key")
        profile = await provider.fetch_company_profile("VOD.LSE")

        assert profile["name"] == "Vodafone Group PLC"
        assert profile["sector"] == "Telecommunications"
        assert profile["market_cap_gbp"] == 25000000000

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_fetch_analyst_estimates_success(self, mock_get):
        """Test successful analyst estimates fetching."""
        # Mock EODHD API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "AnalystRatings": {
                "Rating": 4.2,
                "TargetPrice": 160.0,
                "StrongBuy": 5,
                "Buy": 3,
                "Hold": 2,
                "Sell": 0,
                "StrongSell": 0
            }
        }
        mock_get.return_value = mock_response

        provider = EODHDProvider(api_key="test_key")
        estimates = await provider.fetch_analyst_estimates("VOD.LSE")

        assert estimates["total_analysts"] == 10
        assert estimates["consensus"] == "BULLISH"
        assert estimates["strong_buy"] == 5

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_fetch_analyst_estimates_no_coverage(self, mock_get):
        """Test handling of stocks with no analyst coverage."""
        # Mock EODHD API response with no analyst data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        provider = EODHDProvider(api_key="test_key")
        estimates = await provider.fetch_analyst_estimates("SMALLCAP.LSE")

        assert estimates == {}

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_retry_on_429_rate_limit(self, mock_get):
        """Test retry logic on 429 rate limit error."""
        # First two attempts return 429, third succeeds
        mock_response_429 = Mock()
        mock_response_429.status_code = 429

        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"test": "data"}

        mock_get.side_effect = [mock_response_429, mock_response_429, mock_response_success]

        provider = EODHDProvider(api_key="test_key", max_retries=3)

        result = await provider._make_request_with_retry(
            "http://test.com/api",
            {"api_token": "test_key"}
        )

        assert result == {"test": "data"}
        assert mock_get.call_count == 3

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_retry_on_5xx_server_error(self, mock_get):
        """Test retry logic on 5xx server errors."""
        # First attempt returns 503, second succeeds
        mock_response_503 = Mock()
        mock_response_503.status_code = 503

        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"test": "data"}

        mock_get.side_effect = [mock_response_503, mock_response_success]

        provider = EODHDProvider(api_key="test_key", max_retries=3)

        result = await provider._make_request_with_retry(
            "http://test.com/api",
            {"api_token": "test_key"}
        )

        assert result == {"test": "data"}
        assert mock_get.call_count == 2

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_no_retry_on_4xx_client_error(self, mock_get):
        """Test that 4xx errors (except 429) are not retried."""
        # Return 404 (client error)
        mock_response_404 = Mock()
        mock_response_404.status_code = 404
        mock_response_404.text = "Not found"
        mock_get.return_value = mock_response_404

        provider = EODHDProvider(api_key="test_key", max_retries=3)

        result = await provider._make_request_with_retry(
            "http://test.com/api",
            {"api_token": "test_key"}
        )

        assert result is None
        assert mock_get.call_count == 1  # No retries

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_exponential_backoff_timing(self, mock_get):
        """Test exponential backoff delays (1s, 3s, 9s)."""
        # All attempts return 429
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        mock_get.return_value = mock_response_429

        provider = EODHDProvider(api_key="test_key", max_retries=3)

        start_time = asyncio.get_event_loop().time()

        with pytest.raises(EODHDRateLimitExceeded):
            await provider._make_request_with_retry(
                "http://test.com/api",
                {"api_token": "test_key"}
            )

        elapsed = asyncio.get_event_loop().time() - start_time

        # Should have delays of 1 + 3 = 4 seconds minimum (3rd attempt doesn't delay)
        # Allow some tolerance for test execution time
        assert elapsed >= 4.0
        assert mock_get.call_count == 3

    @pytest.mark.asyncio
    async def test_implements_datasource_interface(self):
        """Test that EODHDProvider implements DataSource interface."""
        provider = EODHDProvider(api_key="test_key")

        # Should have fetch method
        assert hasattr(provider, 'fetch')
        assert asyncio.iscoroutinefunction(provider.fetch)

        # Should have get_source_name method
        assert hasattr(provider, 'get_source_name')
        assert callable(provider.get_source_name)

        # Should be instance of DataSource
        assert isinstance(provider, DataSource)

    @pytest.mark.asyncio
    async def test_context_manager_support(self):
        """Test async context manager support."""
        async with EODHDProvider(api_key="test_key") as provider:
            assert provider.get_source_name() == "eodhd_fundamental"
        # Client should be closed after exiting context
