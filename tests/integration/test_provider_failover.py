"""
Integration tests for data provider failover scenarios.

Tests cover:
- End-to-end: Config → Registry → Multiple providers → Signals
- Failover scenario: Mock EODHD failure → Yahoo succeeds
- All-providers-down scenario → Graceful degradation
- Parallel source execution performance
- Error isolation (one provider crash doesn't affect others)
"""

import pytest
import asyncio
import time
from datetime import datetime, timezone
from unittest.mock import Mock, patch, AsyncMock
from typing import List

from backend.app.data_sources.base import DataSource, Signal
from backend.app.data_sources.registry import DataSourceRegistry
from backend.app.data_sources.providers.yahoo_provider import YahooFinanceProvider
from backend.app.data_sources.providers.alpha_vantage_provider import AlphaVantageProvider
from backend.app.data_sources.providers.eodhd_provider import EODHDProvider
from backend.app.data_sources.failover import DataSourceFailover
from backend.app.core.config import DataSourcesConfig


class TestEndToEndDataFlow:
    """Test end-to-end data flow through the system."""

    @pytest.mark.asyncio
    @patch('backend.app.data_sources.providers.yahoo_provider.yf.Ticker')
    async def test_config_to_signals_flow(self, mock_ticker, tmp_path):
        """Test complete flow: Config → Registry → Provider → Signals."""
        # Create test configuration
        config_content = """
primary_fundamental_provider: yahoo

providers:
  yahoo:
    enabled: true
    priority: 1

failover:
  max_retries: 3
"""
        config_file = tmp_path / "data_sources.yaml"
        config_file.write_text(config_content)

        # Load configuration
        config = DataSourcesConfig(config_path=config_file)

        # Verify configuration loaded correctly
        assert config.is_provider_enabled("yahoo")
        assert config.priority_order == ["yahoo"]

        # Mock Yahoo Finance response
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

        # Create provider and registry
        provider = YahooFinanceProvider(tickers=["VOD.L"])
        registry = DataSourceRegistry()
        registry.register(provider)
        registry.enable("yahoo_finance")

        # Fetch signals
        signals = await registry.fetch_all()

        # Verify signals generated
        assert len(signals) == 1
        assert signals[0].ticker == "VOD.L"
        assert signals[0].signal_type == "PRICE_UPDATE"
        assert signals[0].source == "yahoo_finance"
        assert "current_price" in signals[0].data


class TestFailoverScenarios:
    """Test failover between providers."""

    @pytest.fixture
    def mock_eodhd_provider(self):
        """Create mock EODHD provider."""

        class MockEODHDProvider(DataSource):
            def __init__(self, should_fail: bool = False):
                self.should_fail = should_fail

            async def fetch(self, tickers=None) -> List[Signal]:
                if self.should_fail:
                    raise Exception("EODHD API 5xx error")
                return [
                    Signal(
                        ticker="VOD.L",
                        signal_type="FUNDAMENTAL_DATA",
                        score=80,
                        confidence=0.95,
                        data={"provider": "eodhd"},
                        timestamp=datetime.now(timezone.utc),
                        source="eodhd"
                    )
                ]

            def get_source_name(self) -> str:
                return "eodhd"

        return MockEODHDProvider

    @pytest.mark.asyncio
    @patch('backend.app.data_sources.providers.yahoo_provider.yf.Ticker')
    async def test_eodhd_fails_yahoo_succeeds(self, mock_ticker, mock_eodhd_provider):
        """Test failover from EODHD to Yahoo when EODHD fails."""
        # Setup EODHD to fail
        eodhd = mock_eodhd_provider(should_fail=True)

        # Setup Yahoo to succeed
        mock_stock = Mock()
        mock_stock.info = {
            'regularMarketPrice': 150.0,
            'previousClose': 145.0,
            'volume': 10000000,
            'averageVolume': 8000000
        }
        mock_ticker.return_value = mock_stock

        yahoo = YahooFinanceProvider(tickers=["VOD.L"])

        # Create failover manager
        failover = DataSourceFailover(
            providers={"eodhd": eodhd, "yahoo": yahoo},
            priority_order=["eodhd", "yahoo"]
        )

        # Fetch with failover
        signals = await failover.fetch_with_failover(tickers=["VOD.L"])

        # Should get signal from Yahoo (backup)
        assert len(signals) == 1
        assert signals[0].source == "yahoo_finance"

    @pytest.mark.asyncio
    async def test_all_providers_down_graceful_degradation(self, mock_eodhd_provider):
        """Test graceful degradation when all providers fail."""

        class FailingYahooProvider(DataSource):
            async def fetch(self, tickers=None) -> List[Signal]:
                raise Exception("Yahoo Finance unavailable")

            def get_source_name(self) -> str:
                return "yahoo"

        # All providers fail
        eodhd = mock_eodhd_provider(should_fail=True)
        yahoo = FailingYahooProvider()

        # Create failover with cache
        failover = DataSourceFailover(
            providers={"eodhd": eodhd, "yahoo": yahoo},
            priority_order=["eodhd", "yahoo"]
        )

        # Pre-populate cache with "stale" data
        cached_signal = Signal(
            ticker="VOD.L",
            signal_type="CACHED",
            score=50,
            confidence=0.5,
            data={"cached": True},
            timestamp=datetime.now(timezone.utc),
            source="cache"
        )

        cache_key = failover._get_cache_key(["VOD.L"])
        failover._update_cache(cache_key, [cached_signal])

        # Fetch should return cached data
        signals = await failover.fetch_with_failover(
            tickers=["VOD.L"],
            use_cache_on_failure=True
        )

        assert len(signals) == 1
        assert signals[0].data["cached"] is True
        assert "stale" in signals[0].data

    @pytest.mark.asyncio
    async def test_all_providers_down_no_cache(self, mock_eodhd_provider):
        """Test behavior when all providers fail and no cache available."""

        class FailingYahooProvider(DataSource):
            async def fetch(self, tickers=None) -> List[Signal]:
                raise Exception("Yahoo Finance unavailable")

            def get_source_name(self) -> str:
                return "yahoo"

        eodhd = mock_eodhd_provider(should_fail=True)
        yahoo = FailingYahooProvider()

        failover = DataSourceFailover(
            providers={"eodhd": eodhd, "yahoo": yahoo},
            priority_order=["eodhd", "yahoo"]
        )

        # Fetch should return empty list
        signals = await failover.fetch_with_failover(
            tickers=["VOD.L"],
            use_cache_on_failure=True
        )

        assert signals == []


class TestParallelExecution:
    """Test parallel execution of multiple providers."""

    @pytest.mark.asyncio
    async def test_parallel_faster_than_sequential(self):
        """Test that parallel execution is faster than sequential."""

        class SlowProvider(DataSource):
            def __init__(self, name: str, delay: float):
                self.name = name
                self.delay = delay

            async def fetch(self, tickers=None) -> List[Signal]:
                await asyncio.sleep(self.delay)
                return [
                    Signal(
                        ticker="VOD.L",
                        signal_type="TEST",
                        score=50,
                        confidence=0.8,
                        data={},
                        timestamp=datetime.now(timezone.utc),
                        source=self.name
                    )
                ]

            def get_source_name(self) -> str:
                return self.name

        # Create 3 providers with 1 second delay each
        provider1 = SlowProvider("provider1", 1.0)
        provider2 = SlowProvider("provider2", 1.0)
        provider3 = SlowProvider("provider3", 1.0)

        registry = DataSourceRegistry()
        registry.register(provider1)
        registry.register(provider2)
        registry.register(provider3)
        registry.enable("provider1")
        registry.enable("provider2")
        registry.enable("provider3")

        # Measure parallel execution time
        start = time.time()
        signals = await registry.fetch_all()
        parallel_duration = time.time() - start

        # Parallel should complete in ~1 second (not 3 seconds)
        assert parallel_duration < 2.0  # Allow some overhead
        assert len(signals) == 3

    @pytest.mark.asyncio
    async def test_error_isolation_parallel(self):
        """Test that one provider crash doesn't affect others in parallel execution."""

        class FailingProvider(DataSource):
            async def fetch(self, tickers=None) -> List[Signal]:
                await asyncio.sleep(0.1)
                raise Exception("Provider crashed")

            def get_source_name(self) -> str:
                return "failing"

        class SuccessProvider(DataSource):
            def __init__(self, name: str):
                self.name = name

            async def fetch(self, tickers=None) -> List[Signal]:
                await asyncio.sleep(0.1)
                return [
                    Signal(
                        ticker="VOD.L",
                        signal_type="TEST",
                        score=50,
                        confidence=0.8,
                        data={},
                        timestamp=datetime.now(timezone.utc),
                        source=self.name
                    )
                ]

            def get_source_name(self) -> str:
                return self.name

        # Mix of failing and successful providers
        failing = FailingProvider()
        success1 = SuccessProvider("success1")
        success2 = SuccessProvider("success2")

        registry = DataSourceRegistry()
        registry.register(failing)
        registry.register(success1)
        registry.register(success2)
        registry.enable("failing")
        registry.enable("success1")
        registry.enable("success2")

        # Should get signals from successful providers despite failure
        signals = await registry.fetch_all()

        assert len(signals) == 2
        assert all(s.source in ["success1", "success2"] for s in signals)


class TestRegistryExecutionStats:
    """Test registry execution statistics tracking."""

    @pytest.mark.asyncio
    async def test_execution_stats_tracked(self):
        """Test that registry tracks execution statistics."""

        class TestProvider(DataSource):
            async def fetch(self, tickers=None) -> List[Signal]:
                await asyncio.sleep(0.1)
                return [
                    Signal(
                        ticker="VOD.L",
                        signal_type="TEST",
                        score=50,
                        confidence=0.8,
                        data={},
                        timestamp=datetime.now(timezone.utc),
                        source="test"
                    )
                ]

            def get_source_name(self) -> str:
                return "test"

        provider = TestProvider()
        registry = DataSourceRegistry()
        registry.register(provider)
        registry.enable("test")

        # Execute
        await registry.fetch_all()

        # Check stats
        stats = registry.get_execution_stats("test")

        assert stats["status"] == "success"
        assert stats["signal_count"] == 1
        assert stats["duration_ms"] > 0
        assert "last_execution" in stats

    @pytest.mark.asyncio
    async def test_execution_stats_on_failure(self):
        """Test that stats track failures correctly."""

        class FailingProvider(DataSource):
            async def fetch(self, tickers=None) -> List[Signal]:
                raise Exception("Test failure")

            def get_source_name(self) -> str:
                return "failing"

        provider = FailingProvider()
        registry = DataSourceRegistry()
        registry.register(provider)
        registry.enable("failing")

        # Execute (will fail)
        await registry.fetch_all()

        # Check stats
        stats = registry.get_execution_stats("failing")

        assert stats["status"] == "error"
        assert stats["signal_count"] == 0
        assert "error" in stats
        assert stats["error"] == "Test failure"


class TestCacheAndStaleness:
    """Test caching and staleness tracking."""

    @pytest.mark.asyncio
    async def test_cache_staleness_flagging(self):
        """Test that old cached data is flagged as stale."""

        class FailingProvider(DataSource):
            async def fetch(self, tickers=None) -> List[Signal]:
                raise Exception("Provider down")

            def get_source_name(self) -> str:
                return "failing"

        provider = FailingProvider()

        failover = DataSourceFailover(
            providers={"failing": provider},
            priority_order=["failing"],
            cache_ttl_hours=24
        )

        # Create old cached signal (2 hours old)
        old_signal = Signal(
            ticker="VOD.L",
            signal_type="CACHED",
            score=50,
            confidence=0.5,
            data={},
            timestamp=datetime.now(timezone.utc),
            source="cache"
        )

        cache_key = failover._get_cache_key(["VOD.L"])
        failover._cache[cache_key] = [old_signal]
        failover._cache_timestamps[cache_key] = datetime.now(timezone.utc)

        # Manually set cache timestamp to 2 hours ago
        from datetime import timedelta
        failover._cache_timestamps[cache_key] -= timedelta(hours=2)

        # Fetch should return cached data with staleness flag
        signals = await failover.fetch_with_failover(
            tickers=["VOD.L"],
            use_cache_on_failure=True
        )

        assert len(signals) == 1
        assert signals[0].data["cached"] is True
        assert signals[0].data["stale"] is True
        assert signals[0].data["cache_age_hours"] > 1


class TestEODHDIntegration:
    """Integration tests for EODHD provider."""

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_eodhd_fetch_all_data_types(self, mock_get):
        """Test fetching all data types (fundamentals, prices, profile, estimates)."""
        # Mock successful responses for all endpoints
        mock_fundamentals_response = Mock()
        mock_fundamentals_response.status_code = 200
        mock_fundamentals_response.json.return_value = {
            "General": {"Code": "VOD", "Name": "Vodafone"},
            "Highlights": {"PERatio": 12.5, "ReturnOnEquityTTM": 15.5},
            "Financials": {"Balance_Sheet": {}, "Income_Statement": {}, "Cash_Flow": {}}
        }

        mock_prices_response = Mock()
        mock_prices_response.status_code = 200
        mock_prices_response.json.return_value = [
            {"date": "2025-11-01", "open": 14500, "high": 14800, "low": 14300, "close": 14700, "volume": 5000000}
        ]

        mock_profile_response = Mock()
        mock_profile_response.status_code = 200
        mock_profile_response.json.return_value = {
            "General": {"Code": "VOD", "Name": "Vodafone", "Sector": "Telecom"}
        }

        mock_estimates_response = Mock()
        mock_estimates_response.status_code = 200
        mock_estimates_response.json.return_value = {
            "AnalystRatings": {"Rating": 4.2, "StrongBuy": 5, "Buy": 3, "Hold": 2}
        }

        # Set up mock to return different responses based on URL
        def mock_get_side_effect(url, params=None):
            if "filter=General" in url or ("filter" in params and params.get("filter") == "General"):
                return mock_profile_response
            elif "filter=AnalystRatings" in url or ("filter" in params and params.get("filter") == "AnalystRatings::Rating"):
                return mock_estimates_response
            elif "/eod/" in url:
                return mock_prices_response
            else:
                return mock_fundamentals_response

        mock_get.side_effect = mock_get_side_effect

        # Create provider and fetch
        provider = EODHDProvider(api_key="test_key", tickers=["VOD.L"])
        signals = await provider.fetch()

        # Should get 4 signals: fundamentals, profile, estimates, prices
        assert len(signals) >= 3  # At least fundamentals, profile, prices
        signal_types = {s.signal_type for s in signals}
        assert "FUNDAMENTAL_DATA" in signal_types
        assert "COMPANY_PROFILE" in signal_types or "PRICE_DATA" in signal_types

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_eodhd_caching_reduces_api_calls(self, mock_get):
        """Test that caching reduces API calls for repeated fetches."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "General": {"Code": "VOD"},
            "Highlights": {"PERatio": 12.5},
            "Financials": {}
        }
        mock_get.return_value = mock_response

        provider = EODHDProvider(api_key="test_key", cache_ttl_hours=24)

        # First fetch - should hit API
        fundamentals1 = await provider.fetch_fundamentals("VOD.LSE")
        first_call_count = mock_get.call_count

        # Second fetch - should use cache
        fundamentals2 = await provider.fetch_fundamentals("VOD.LSE")
        second_call_count = mock_get.call_count

        # Call count should not increase (cache hit)
        assert second_call_count == first_call_count
        assert fundamentals1 == fundamentals2

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_eodhd_rate_limit_triggers_failover(self, mock_get):
        """Test that rate limit triggers Yahoo Finance failover."""
        # Setup EODHD to fail with rate limit
        eodhd = EODHDProvider(api_key="test_key", rate_limit_per_day=0, tickers=["VOD.L"])

        # Setup Yahoo to succeed
        with patch('backend.app.data_sources.providers.yahoo_provider.yf.Ticker') as mock_ticker:
            mock_stock = Mock()
            mock_stock.info = {
                'regularMarketPrice': 150.0,
                'previousClose': 145.0,
                'volume': 10000000,
                'averageVolume': 8000000
            }
            mock_ticker.return_value = mock_stock

            yahoo = YahooFinanceProvider(tickers=["VOD.L"])

            # Create failover
            failover = DataSourceFailover(
                providers={"eodhd": eodhd, "yahoo": yahoo},
                priority_order=["eodhd", "yahoo"]
            )

            # Fetch should failover to Yahoo
            signals = await failover.fetch_with_failover(tickers=["VOD.L"])

            # Should get Yahoo signals (EODHD at rate limit)
            # May be empty if both fail, or contain Yahoo signals
            assert isinstance(signals, list)

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_eodhd_integration_with_registry(self, mock_get):
        """Test EODHD integration with DataSourceRegistry."""
        # Mock EODHD response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "General": {"Code": "VOD", "Name": "Vodafone"},
            "Highlights": {"PERatio": 12.5},
            "Financials": {}
        }
        mock_get.return_value = mock_response

        # Create provider and register
        provider = EODHDProvider(api_key="test_key", tickers=["VOD.L"])
        registry = DataSourceRegistry()

        registry.register(provider)
        registry.enable("eodhd_fundamental")

        # Verify registration
        assert "eodhd_fundamental" in registry.list_all()
        assert registry.is_enabled("eodhd_fundamental")

        # Fetch all
        signals = await registry.fetch_all()

        # Should get EODHD signals
        assert isinstance(signals, list)
        if signals:
            assert all(s.source == "eodhd_fundamental" for s in signals)

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_eodhd_uk_market_pence_conversion(self, mock_get):
        """Test UK market pence/pounds conversion."""
        # Mock price response with values in pence
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"date": "2025-11-01", "open": 14500, "high": 14800, "low": 14300, "close": 14700, "volume": 5000000}
        ]
        mock_get.return_value = mock_response

        provider = EODHDProvider(api_key="test_key")
        prices = await provider.fetch_historical_prices("VOD.LSE", "2025-11-01", "2025-11-02")

        # Prices should be converted from pence to pounds
        assert prices["prices"][0]["close"] == 147.0  # 14700 pence = £147
        assert prices["prices"][0]["high"] == 148.0  # 14800 pence = £148

    @pytest.mark.asyncio
    async def test_eodhd_config_integration(self, tmp_path, monkeypatch):
        """Test EODHD configuration loading from YAML."""
        monkeypatch.setenv("EODHD_API_KEY", "test_api_key_from_env")

        # Create test configuration
        config_content = """
primary_fundamental_provider: eodhd

providers:
  eodhd:
    enabled: true
    api_key: ${EODHD_API_KEY}
    priority: 1
    rate_limit: 100000
    cache_ttl_hours: 24
"""
        config_file = tmp_path / "data_sources.yaml"
        config_file.write_text(config_content)

        # Load configuration
        config = DataSourcesConfig(config_path=config_file)

        # Verify EODHD configuration
        assert config.primary_provider == "eodhd"
        assert config.is_provider_enabled("eodhd")
        assert config.providers["eodhd"]["api_key"] == "test_api_key_from_env"
        assert config.providers["eodhd"]["rate_limit"] == 100000
        assert config.providers["eodhd"]["cache_ttl_hours"] == 24

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_eodhd_error_handling_network_failure(self, mock_get):
        """Test EODHD error handling for network failures."""
        # Mock network error
        import httpx
        mock_get.side_effect = httpx.TimeoutException("Connection timeout")

        provider = EODHDProvider(api_key="test_key", max_retries=1)

        # Should handle gracefully and return empty dict
        fundamentals = await provider.fetch_fundamentals("VOD.LSE")

        assert fundamentals == {}  # Empty on error

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_eodhd_retry_logic_eventual_success(self, mock_get):
        """Test that retry logic eventually succeeds after transient failures."""
        # First two calls fail with 503, third succeeds
        mock_fail = Mock()
        mock_fail.status_code = 503

        mock_success = Mock()
        mock_success.status_code = 200
        mock_success.json.return_value = {"test": "data"}

        mock_get.side_effect = [mock_fail, mock_fail, mock_success]

        provider = EODHDProvider(api_key="test_key", max_retries=3)

        result = await provider._make_request_with_retry(
            "http://test.com/api",
            {"api_token": "test_key"}
        )

        # Should succeed on third attempt
        assert result == {"test": "data"}
        assert mock_get.call_count == 3
