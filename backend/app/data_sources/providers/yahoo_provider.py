"""
Yahoo Finance provider implementation.

Free data source providing basic price and volume data for LSE stocks.
Used as primary fallback when EODHD is unavailable.
"""

import asyncio
import structlog
from datetime import datetime, timezone
from typing import List, Optional
import yfinance as yf

from backend.app.data_sources.base import DataSource, Signal


logger = structlog.get_logger(__name__)


class YahooFinanceProvider(DataSource):
    """
    Yahoo Finance data provider for fallback price/volume data.

    This provider:
    - Fetches basic price and volume data for LSE stocks
    - Converts to standardized Signal format
    - Handles errors gracefully (network issues, missing data)
    - Has no rate limiting (free tier)

    Note: Yahoo Finance provides limited fundamental data compared to EODHD.
    Use primarily for price/volume when EODHD is unavailable.

    Example:
        >>> provider = YahooFinanceProvider(tickers=["VOD.L", "LLOY.L"])
        >>> signals = await provider.fetch()
        >>> for signal in signals:
        ...     print(f"{signal.ticker}: {signal.score}")
    """

    def __init__(
        self,
        tickers: Optional[List[str]] = None,
        config: Optional[dict] = None
    ):
        """
        Initialize Yahoo Finance provider.

        Args:
            tickers: List of LSE tickers to fetch (e.g., ["VOD.L", "BP.L"])
                    If None, uses config or empty list.
            config: Optional configuration dictionary with:
                    - tickers: List of tickers to fetch
                    - enabled: Whether provider is enabled
        """
        self.tickers = tickers or (config.get("tickers", []) if config else [])
        self.config = config or {}

    def get_source_name(self) -> str:
        """Return unique identifier for this provider."""
        return "yahoo_finance"

    async def fetch(self) -> List[Signal]:
        """
        Fetch price/volume data from Yahoo Finance.

        Returns:
            List of Signal objects with price/volume data.
            Empty list if fetch fails or no tickers configured.

        Note:
            Does not raise exceptions. Logs errors and returns empty list.
        """
        if not self.tickers:
            logger.warning(
                "yahoo_no_tickers",
                message="No tickers configured for Yahoo Finance provider"
            )
            return []

        logger.info(
            "yahoo_fetch_started",
            ticker_count=len(self.tickers),
            tickers=self.tickers[:5]  # Log first 5 for brevity
        )

        try:
            # Run yfinance in thread pool (it's synchronous)
            signals = await asyncio.to_thread(self._fetch_sync)
            return signals

        except Exception as e:
            logger.error(
                "yahoo_fetch_error",
                error=str(e),
                error_type=type(e).__name__,
                ticker_count=len(self.tickers)
            )
            return []

    def _fetch_sync(self) -> List[Signal]:
        """
        Synchronous fetch from Yahoo Finance (runs in thread pool).

        Returns:
            List of Signal objects
        """
        signals = []
        timestamp = datetime.now(timezone.utc)

        for ticker in self.tickers:
            try:
                # Fetch stock data
                stock = yf.Ticker(ticker)
                info = stock.info

                # Check if we got valid data
                if not info or info.get("regularMarketPrice") is None:
                    logger.warning(
                        "yahoo_ticker_no_data",
                        ticker=ticker,
                        message="No data available from Yahoo Finance"
                    )
                    continue

                # Extract price and volume data
                current_price = info.get("regularMarketPrice", 0)
                previous_close = info.get("previousClose", current_price)
                volume = info.get("volume", 0)
                avg_volume = info.get("averageVolume", volume)

                # Calculate price change percentage
                price_change_pct = 0
                if previous_close and previous_close > 0:
                    price_change_pct = ((current_price - previous_close) / previous_close) * 100

                # Calculate volume ratio (current vs average)
                volume_ratio = 0
                if avg_volume and avg_volume > 0:
                    volume_ratio = volume / avg_volume

                # Generate signal score based on price change and volume
                # Base score of 50 (neutral), adjusted by price change and volume
                score = 50

                # Adjust for significant price moves
                if abs(price_change_pct) > 5:
                    score += min(abs(price_change_pct) * 2, 20)

                # Adjust for unusual volume
                if volume_ratio > 1.5:
                    score += min((volume_ratio - 1) * 10, 15)

                # Clamp score to 0-100 range
                score = max(0, min(100, int(score)))

                # Determine confidence based on data quality
                confidence = 0.8  # Default for Yahoo Finance
                if info.get("regularMarketPrice") and info.get("volume"):
                    confidence = 0.85

                # Create signal
                signal = Signal(
                    ticker=ticker,
                    signal_type="PRICE_UPDATE",
                    score=score,
                    confidence=confidence,
                    data={
                        "current_price": float(current_price),
                        "previous_close": float(previous_close),
                        "price_change_pct": float(price_change_pct),
                        "volume": int(volume),
                        "average_volume": int(avg_volume),
                        "volume_ratio": float(volume_ratio),
                        "market_cap": info.get("marketCap"),
                        "currency": info.get("currency", "GBP"),
                        "provider": "yahoo_finance"
                    },
                    timestamp=timestamp,
                    source=self.get_source_name()
                )

                signals.append(signal)

                logger.debug(
                    "yahoo_ticker_fetched",
                    ticker=ticker,
                    price=current_price,
                    price_change_pct=price_change_pct,
                    volume_ratio=volume_ratio,
                    score=score
                )

            except Exception as e:
                logger.warning(
                    "yahoo_ticker_error",
                    ticker=ticker,
                    error=str(e),
                    error_type=type(e).__name__
                )
                # Continue with next ticker
                continue

        logger.info(
            "yahoo_fetch_completed",
            signals_generated=len(signals),
            tickers_attempted=len(self.tickers)
        )

        return signals

    async def fetch_single_ticker(self, ticker: str) -> Optional[Signal]:
        """
        Fetch data for a single ticker.

        Utility method for fetching individual stock data.

        Args:
            ticker: LSE ticker (e.g., "VOD.L")

        Returns:
            Signal object if successful, None otherwise
        """
        original_tickers = self.tickers
        self.tickers = [ticker]

        try:
            signals = await self.fetch()
            return signals[0] if signals else None
        finally:
            self.tickers = original_tickers
