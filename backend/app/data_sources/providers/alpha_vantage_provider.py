"""
Alpha Vantage provider implementation.

Emergency fallback provider with free tier (25 calls/day).
Used when both EODHD and Yahoo Finance are unavailable.
"""

import asyncio
import structlog
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict
from alpha_vantage.timeseries import TimeSeries

from backend.app.data_sources.base import DataSource, Signal


logger = structlog.get_logger(__name__)


class RateLimitExceeded(Exception):
    """Raised when Alpha Vantage rate limit is exceeded."""
    pass


class AlphaVantageProvider(DataSource):
    """
    Alpha Vantage data provider for emergency fallback.

    This provider:
    - Has strict rate limits (25 calls/day on free tier)
    - Fetches basic price data for stocks
    - Tracks daily call count to prevent exceeding quota
    - Validates API key before use
    - Should only be used when EODHD and Yahoo Finance both fail

    Rate Limiting:
        Free tier: 25 API calls per day
        Premium tier: 75+ calls per day (requires subscription)

    Example:
        >>> provider = AlphaVantageProvider(api_key="your_key")
        >>> # Check if we have quota remaining
        >>> if provider.get_remaining_calls() > 0:
        ...     signals = await provider.fetch(tickers=["VOD.L"])
        ... else:
        ...     print("Rate limit exceeded for today")
    """

    # Class-level tracking of daily calls (resets at midnight UTC)
    _daily_calls: Dict[str, int] = {}
    _last_reset: Dict[str, datetime] = {}

    # Free tier limit (can be overridden in config)
    DEFAULT_DAILY_LIMIT = 25

    def __init__(
        self,
        api_key: str,
        daily_limit: Optional[int] = None,
        config: Optional[dict] = None
    ):
        """
        Initialize Alpha Vantage provider.

        Args:
            api_key: Alpha Vantage API key (required)
            daily_limit: Maximum API calls per day (default: 25 for free tier)
            config: Optional configuration dictionary

        Raises:
            ValueError: If api_key is empty or None
        """
        if not api_key:
            raise ValueError("Alpha Vantage API key is required")

        self.api_key = api_key
        self.daily_limit = daily_limit if daily_limit is not None else self.DEFAULT_DAILY_LIMIT
        self.config = config or {}
        self.ts = TimeSeries(key=api_key, output_format='pandas')

        # Initialize daily call tracking
        if self.api_key not in self._daily_calls:
            self._daily_calls[self.api_key] = 0
            self._last_reset[self.api_key] = datetime.now(timezone.utc)

    def get_source_name(self) -> str:
        """Return unique identifier for this provider."""
        return "alpha_vantage"

    def _check_and_reset_daily_limit(self) -> None:
        """Check if we need to reset daily call counter (at midnight UTC)."""
        now = datetime.now(timezone.utc)
        last_reset = self._last_reset.get(self.api_key)

        if last_reset:
            # Check if we've crossed midnight UTC
            if now.date() > last_reset.date():
                self._daily_calls[self.api_key] = 0
                self._last_reset[self.api_key] = now
                logger.info(
                    "alpha_vantage_limit_reset",
                    api_key_prefix=self.api_key[:8] + "...",
                    daily_limit=self.daily_limit
                )

    def get_remaining_calls(self) -> int:
        """
        Get number of API calls remaining today.

        Returns:
            Number of calls remaining (0 if limit exceeded)
        """
        self._check_and_reset_daily_limit()
        used = self._daily_calls.get(self.api_key, 0)
        return max(0, self.daily_limit - used)

    def _increment_call_count(self) -> None:
        """Increment daily call counter."""
        self._daily_calls[self.api_key] = self._daily_calls.get(self.api_key, 0) + 1

    async def fetch(
        self,
        tickers: Optional[List[str]] = None
    ) -> List[Signal]:
        """
        Fetch price data from Alpha Vantage.

        Args:
            tickers: List of stock tickers to fetch. If None, returns empty list.

        Returns:
            List of Signal objects with price data.
            Empty list if rate limit exceeded or fetch fails.

        Note:
            Does not raise exceptions. Logs errors and returns empty list.
            Respects rate limits and will return empty if quota exceeded.
        """
        if not tickers:
            logger.warning(
                "alpha_vantage_no_tickers",
                message="No tickers provided to Alpha Vantage provider"
            )
            return []

        # Check rate limit before fetching
        remaining = self.get_remaining_calls()
        if remaining < len(tickers):
            logger.warning(
                "alpha_vantage_rate_limit",
                requested_calls=len(tickers),
                remaining_calls=remaining,
                daily_limit=self.daily_limit,
                message="Insufficient API calls remaining for request"
            )
            # Fetch as many as we can within limit
            tickers = tickers[:remaining]
            if not tickers:
                return []

        logger.info(
            "alpha_vantage_fetch_started",
            ticker_count=len(tickers),
            remaining_calls=remaining
        )

        try:
            # Run synchronous Alpha Vantage calls in thread pool
            signals = await asyncio.to_thread(self._fetch_sync, tickers)
            return signals

        except RateLimitExceeded:
            logger.error(
                "alpha_vantage_rate_limit_exceeded",
                daily_limit=self.daily_limit
            )
            return []

        except Exception as e:
            logger.error(
                "alpha_vantage_fetch_error",
                error=str(e),
                error_type=type(e).__name__
            )
            return []

    def _fetch_sync(self, tickers: List[str]) -> List[Signal]:
        """
        Synchronous fetch from Alpha Vantage (runs in thread pool).

        Args:
            tickers: List of stock tickers to fetch

        Returns:
            List of Signal objects

        Raises:
            RateLimitExceeded: If rate limit is exceeded during fetch
        """
        signals = []
        timestamp = datetime.now(timezone.utc)

        for ticker in tickers:
            # Check if we've hit rate limit
            if self.get_remaining_calls() <= 0:
                logger.warning(
                    "alpha_vantage_mid_fetch_limit",
                    processed=len(signals),
                    remaining_tickers=len(tickers) - len(signals)
                )
                break

            try:
                # Alpha Vantage expects tickers without exchange suffix
                # Convert "VOD.L" -> "VOD" for API call
                av_ticker = ticker.replace(".L", "")

                # Fetch daily data (most efficient for our use case)
                data, meta_data = self.ts.get_daily(symbol=av_ticker)

                # Increment call counter
                self._increment_call_count()

                # Get most recent day's data
                if data.empty:
                    logger.warning(
                        "alpha_vantage_no_data",
                        ticker=ticker,
                        av_ticker=av_ticker
                    )
                    continue

                latest_date = data.index[0]
                latest_data = data.iloc[0]

                current_price = float(latest_data['4. close'])
                open_price = float(latest_data['1. open'])
                high_price = float(latest_data['2. high'])
                low_price = float(latest_data['3. low'])
                volume = int(latest_data['5. volume'])

                # Calculate intraday price change
                price_change_pct = 0
                if open_price > 0:
                    price_change_pct = ((current_price - open_price) / open_price) * 100

                # Generate signal score (basic price movement indicator)
                score = 50
                if abs(price_change_pct) > 3:
                    score += min(abs(price_change_pct) * 3, 25)

                score = max(0, min(100, int(score)))

                # Alpha Vantage confidence (lower than EODHD, higher than Yahoo for LSE)
                confidence = 0.75

                signal = Signal(
                    ticker=ticker,
                    signal_type="PRICE_UPDATE",
                    score=score,
                    confidence=confidence,
                    data={
                        "current_price": current_price,
                        "open_price": open_price,
                        "high_price": high_price,
                        "low_price": low_price,
                        "volume": volume,
                        "price_change_pct": float(price_change_pct),
                        "latest_date": str(latest_date),
                        "provider": "alpha_vantage",
                        "calls_remaining": self.get_remaining_calls()
                    },
                    timestamp=timestamp,
                    source=self.get_source_name()
                )

                signals.append(signal)

                logger.debug(
                    "alpha_vantage_ticker_fetched",
                    ticker=ticker,
                    price=current_price,
                    calls_remaining=self.get_remaining_calls()
                )

            except Exception as e:
                # Check if error is rate limit related
                error_str = str(e).lower()
                if "api call frequency" in error_str or "rate limit" in error_str:
                    logger.error(
                        "alpha_vantage_rate_limit_error",
                        ticker=ticker,
                        error=str(e)
                    )
                    raise RateLimitExceeded(f"Rate limit exceeded for {ticker}")

                logger.warning(
                    "alpha_vantage_ticker_error",
                    ticker=ticker,
                    error=str(e),
                    error_type=type(e).__name__
                )
                continue

        logger.info(
            "alpha_vantage_fetch_completed",
            signals_generated=len(signals),
            calls_used=self._daily_calls.get(self.api_key, 0),
            calls_remaining=self.get_remaining_calls()
        )

        return signals

    def validate_api_key(self) -> bool:
        """
        Validate that the API key works.

        Returns:
            True if API key is valid, False otherwise

        Note:
            This makes an API call and counts against daily limit.
        """
        if self.get_remaining_calls() <= 0:
            logger.warning("alpha_vantage_no_calls_for_validation")
            return False

        try:
            # Test with a known ticker (Microsoft)
            _, _ = self.ts.get_daily(symbol='MSFT')
            self._increment_call_count()
            return True
        except Exception as e:
            logger.error(
                "alpha_vantage_validation_failed",
                error=str(e),
                error_type=type(e).__name__
            )
            return False
