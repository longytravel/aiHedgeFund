"""
EODHD data provider implementation.

Primary data source for UK stock fundamentals, historical prices, company profiles,
and analyst estimates. Implements caching, rate limiting, and retry logic.
"""

import asyncio
import structlog
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
import httpx

from backend.app.data_sources.base import DataSource, Signal


logger = structlog.get_logger(__name__)


class EODHDRateLimitExceeded(Exception):
    """Raised when EODHD API rate limit is exceeded."""
    pass


class EODHDProvider(DataSource):
    """
    EODHD API provider for comprehensive UK stock data.

    This provider fetches:
    - Historical prices (OHLCV data)
    - Fundamental data (income statement, balance sheet, cash flow)
    - Financial ratios (P/E, P/B, ROE, ROA, debt ratios)
    - Company profile (sector, industry, market cap)
    - Analyst estimates (EPS, revenue consensus)

    Features:
    - Caching with configurable TTL (default: 24 hours)
    - Rate limiting (100k calls/day, configurable)
    - Retry with exponential backoff (1s, 3s, 9s)
    - UK market-specific handling (pence/pounds conversion)
    - Graceful error handling and fallback to cached data

    Example:
        >>> provider = EODHDProvider(
        ...     api_key="your_api_key",
        ...     cache_ttl_hours=24,
        ...     rate_limit_per_day=100000
        ... )
        >>> signals = await provider.fetch()
        >>> for signal in signals:
        ...     print(f"{signal.ticker}: {signal.signal_type}")
    """

    BASE_URL = "https://eodhistoricaldata.com/api"
    EXCHANGE_CODE = "LSE"  # London Stock Exchange

    def __init__(
        self,
        api_key: str,
        tickers: Optional[List[str]] = None,
        cache_ttl_hours: int = 24,
        rate_limit_per_day: int = 100000,
        max_retries: int = 3,
        config: Optional[dict] = None
    ):
        """
        Initialize EODHD provider.

        Args:
            api_key: EODHD API key (required)
            tickers: List of LSE tickers to fetch (e.g., ["VOD.L", "BP.L"])
            cache_ttl_hours: Cache time-to-live in hours (default: 24)
            rate_limit_per_day: Maximum API calls per day (default: 100000)
            max_retries: Maximum retry attempts for failed requests (default: 3)
            config: Optional configuration dictionary
        """
        if not api_key:
            raise ValueError("EODHD API key is required")

        self.api_key = api_key
        self.tickers = tickers or (config.get("tickers", []) if config else [])
        self.cache_ttl_hours = cache_ttl_hours
        self.rate_limit_per_day = rate_limit_per_day
        self.max_retries = max_retries
        self.config = config or {}

        # Rate limiting tracking
        self._api_call_count = 0
        self._rate_limit_reset_time = datetime.now(timezone.utc) + timedelta(days=1)

        # Cache storage
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, datetime] = {}

        # HTTP client
        self._client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True
        )

    def get_source_name(self) -> str:
        """Return unique identifier for this provider."""
        return "eodhd_fundamental"

    async def fetch(self) -> List[Signal]:
        """
        Fetch data from EODHD for all configured tickers.

        Returns:
            List of Signal objects with fundamental data, prices, and estimates.
            Empty list if fetch fails or no tickers configured.

        Note:
            Does not raise exceptions. Logs errors and returns empty list.
        """
        if not self.tickers:
            logger.warning(
                "eodhd_no_tickers",
                message="No tickers configured for EODHD provider"
            )
            return []

        logger.info(
            "eodhd_fetch_started",
            ticker_count=len(self.tickers),
            tickers=self.tickers[:5]  # Log first 5 for brevity
        )

        all_signals = []

        for ticker in self.tickers:
            try:
                # Fetch all data types for this ticker
                signals = await self._fetch_ticker_data(ticker)
                all_signals.extend(signals)

            except EODHDRateLimitExceeded:
                logger.warning(
                    "eodhd_rate_limit_exceeded",
                    ticker=ticker,
                    message="Rate limit exceeded, using cached data for remaining tickers"
                )
                # Try to get cached data for remaining tickers
                cached_signals = self._get_cached_signals(ticker)
                if cached_signals:
                    all_signals.extend(cached_signals)

            except Exception as e:
                logger.error(
                    "eodhd_ticker_error",
                    ticker=ticker,
                    error=str(e),
                    error_type=type(e).__name__
                )
                # Try to get cached data
                cached_signals = self._get_cached_signals(ticker)
                if cached_signals:
                    all_signals.extend(cached_signals)
                continue

        logger.info(
            "eodhd_fetch_completed",
            signals_generated=len(all_signals),
            tickers_attempted=len(self.tickers),
            api_calls_made=self._api_call_count
        )

        return all_signals

    async def _fetch_ticker_data(self, ticker: str) -> List[Signal]:
        """
        Fetch all data types for a single ticker.

        Args:
            ticker: Stock ticker (e.g., "VOD.L")

        Returns:
            List of Signal objects for this ticker
        """
        signals = []
        timestamp = datetime.now(timezone.utc)

        # Format ticker for EODHD API (remove .L, add .LSE)
        eodhd_ticker = self._format_ticker_for_api(ticker)

        # Fetch fundamental data (includes financials, ratios, profile)
        fundamentals = await self.fetch_fundamentals(eodhd_ticker)
        if fundamentals:
            signal = Signal(
                ticker=ticker,
                signal_type="FUNDAMENTAL_DATA",
                score=self._calculate_fundamental_score(fundamentals),
                confidence=0.9,  # EODHD is high quality
                data=fundamentals,
                timestamp=timestamp,
                source=self.get_source_name()
            )
            signals.append(signal)

        # Fetch company profile
        profile = await self.fetch_company_profile(eodhd_ticker)
        if profile:
            signal = Signal(
                ticker=ticker,
                signal_type="COMPANY_PROFILE",
                score=50,  # Neutral score for profile data
                confidence=0.95,
                data=profile,
                timestamp=timestamp,
                source=self.get_source_name()
            )
            signals.append(signal)

        # Fetch analyst estimates
        estimates = await self.fetch_analyst_estimates(eodhd_ticker)
        if estimates:
            signal = Signal(
                ticker=ticker,
                signal_type="ANALYST_ESTIMATES",
                score=self._calculate_analyst_score(estimates),
                confidence=0.85,
                data=estimates,
                timestamp=timestamp,
                source=self.get_source_name()
            )
            signals.append(signal)

        # Fetch recent historical prices (last 30 days)
        to_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        from_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
        prices = await self.fetch_historical_prices(eodhd_ticker, from_date, to_date)
        if prices:
            signal = Signal(
                ticker=ticker,
                signal_type="PRICE_DATA",
                score=self._calculate_price_score(prices),
                confidence=0.95,
                data=prices,
                timestamp=timestamp,
                source=self.get_source_name()
            )
            signals.append(signal)

        return signals

    async def fetch_historical_prices(
        self,
        ticker: str,
        from_date: str,
        to_date: str
    ) -> Dict[str, Any]:
        """
        Fetch historical OHLCV data for a ticker.

        Args:
            ticker: EODHD ticker (e.g., "VOD.LSE")
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            Dictionary with price data or empty dict if fetch fails
        """
        cache_key = f"{ticker}:prices:{from_date}:{to_date}"

        # Check cache first
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            logger.debug("eodhd_cache_hit", cache_key=cache_key, data_type="prices")
            return cached_data

        # Check rate limit
        if not self._check_rate_limit():
            raise EODHDRateLimitExceeded("Daily rate limit exceeded")

        url = f"{self.BASE_URL}/eod/{ticker}"
        params = {
            "api_token": self.api_key,
            "from": from_date,
            "to": to_date,
            "fmt": "json"
        }

        try:
            response = await self._make_request_with_retry(url, params)
            if not response:
                return {}

            # Parse OHLCV data
            price_data = {
                "from_date": from_date,
                "to_date": to_date,
                "data_points": len(response),
                "prices": []
            }

            for item in response:
                # Handle pence/pounds conversion for UK stocks
                price_data["prices"].append({
                    "date": item.get("date"),
                    "open": self._convert_pence_to_pounds(item.get("open", 0)),
                    "high": self._convert_pence_to_pounds(item.get("high", 0)),
                    "low": self._convert_pence_to_pounds(item.get("low", 0)),
                    "close": self._convert_pence_to_pounds(item.get("close", 0)),
                    "adjusted_close": self._convert_pence_to_pounds(item.get("adjusted_close", 0)),
                    "volume": item.get("volume", 0)
                })

            # Calculate summary statistics
            if price_data["prices"]:
                closes = [p["close"] for p in price_data["prices"]]
                price_data["latest_price"] = closes[-1]
                price_data["price_change_30d"] = ((closes[-1] - closes[0]) / closes[0] * 100) if closes[0] > 0 else 0
                price_data["avg_volume_30d"] = sum(p["volume"] for p in price_data["prices"]) / len(price_data["prices"])

            # Cache the result
            self._add_to_cache(cache_key, price_data)

            logger.info(
                "eodhd_prices_fetched",
                ticker=ticker,
                data_points=len(response),
                from_date=from_date,
                to_date=to_date
            )

            return price_data

        except Exception as e:
            logger.error(
                "eodhd_fetch_prices_error",
                ticker=ticker,
                error=str(e),
                error_type=type(e).__name__
            )
            return {}

    async def fetch_fundamentals(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch fundamental data (income statement, balance sheet, cash flow, ratios).

        Args:
            ticker: EODHD ticker (e.g., "VOD.LSE")

        Returns:
            Dictionary with fundamental data or empty dict if fetch fails
        """
        cache_key = f"{ticker}:fundamentals"

        # Check cache first
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            logger.debug("eodhd_cache_hit", cache_key=cache_key, data_type="fundamentals")
            return cached_data

        # Check rate limit
        if not self._check_rate_limit():
            raise EODHDRateLimitExceeded("Daily rate limit exceeded")

        url = f"{self.BASE_URL}/fundamentals/{ticker}"
        params = {
            "api_token": self.api_key,
            "fmt": "json"
        }

        try:
            response = await self._make_request_with_retry(url, params)
            if not response:
                return {}

            # Extract all available fundamental data
            # Store ALL metrics as per AC #1 - don't filter
            fundamentals = {
                "general": response.get("General", {}),
                "highlights": response.get("Highlights", {}),
                "valuation": response.get("Valuation", {}),
                "financials": {
                    "balance_sheet": response.get("Financials", {}).get("Balance_Sheet", {}),
                    "income_statement": response.get("Financials", {}).get("Income_Statement", {}),
                    "cash_flow": response.get("Financials", {}).get("Cash_Flow", {})
                },
                "earnings": response.get("Earnings", {}),
                "technicals": response.get("Technicals", {}),
                "analyst_ratings": response.get("AnalystRatings", {}),
                "holders": response.get("Holders", {}),
                "esg_scores": response.get("ESGScores", {}),
                "outstanding_shares": response.get("outstandingShares", {}),
                "raw_response": response  # Store complete raw response for future use
            }

            # Extract key financial ratios for easy access
            highlights = response.get("Highlights", {})
            fundamentals["key_metrics"] = {
                "pe_ratio": highlights.get("PERatio"),
                "pb_ratio": highlights.get("PriceBookMRQ"),
                "dividend_yield": highlights.get("DividendYield"),
                "eps": highlights.get("EarningsShare"),
                "market_cap": highlights.get("MarketCapitalization"),
                "roe": highlights.get("ReturnOnEquityTTM"),
                "roa": highlights.get("ReturnOnAssetsTTM"),
                "debt_to_equity": highlights.get("DebtToEquity"),
                "current_ratio": highlights.get("CurrentRatio"),
                "profit_margin": highlights.get("ProfitMargin"),
                "operating_margin": highlights.get("OperatingMarginTTM"),
                "revenue_per_share": highlights.get("RevenuePerShareTTM"),
                "quarterly_earnings_growth": highlights.get("QuarterlyEarningsGrowthYOY"),
                "quarterly_revenue_growth": highlights.get("QuarterlyRevenueGrowthYOY")
            }

            # Cache the result
            self._add_to_cache(cache_key, fundamentals)

            logger.info(
                "eodhd_fundamentals_fetched",
                ticker=ticker,
                has_financials=bool(fundamentals.get("financials")),
                has_ratios=bool(fundamentals.get("key_metrics"))
            )

            return fundamentals

        except Exception as e:
            logger.error(
                "eodhd_fetch_fundamentals_error",
                ticker=ticker,
                error=str(e),
                error_type=type(e).__name__
            )
            return {}

    async def fetch_company_profile(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch company profile (sector, industry, market cap, description).

        Args:
            ticker: EODHD ticker (e.g., "VOD.LSE")

        Returns:
            Dictionary with company profile or empty dict if fetch fails
        """
        cache_key = f"{ticker}:profile"

        # Check cache first
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            logger.debug("eodhd_cache_hit", cache_key=cache_key, data_type="profile")
            return cached_data

        # Check rate limit
        if not self._check_rate_limit():
            raise EODHDRateLimitExceeded("Daily rate limit exceeded")

        url = f"{self.BASE_URL}/fundamentals/{ticker}"
        params = {
            "api_token": self.api_key,
            "fmt": "json"
        }

        try:
            response = await self._make_request_with_retry(url, params)
            if not response:
                return {}

            # Extract General section
            general = response.get("General", {})
            if not general:
                logger.warning(
                    "eodhd_no_general_data",
                    ticker=ticker,
                    message="No General section in fundamentals response"
                )
                return {}

            # Extract company profile information
            profile = {
                "code": general.get("Code"),
                "name": general.get("Name"),
                "exchange": general.get("Exchange"),
                "currency": general.get("CurrencyCode"),
                "country": general.get("CountryName"),
                "sector": general.get("Sector"),
                "industry": general.get("Industry"),
                "description": general.get("Description"),
                "address": general.get("Address"),
                "phone": general.get("Phone"),
                "website": general.get("WebURL"),
                "employees": general.get("FullTimeEmployees"),
                "ipo_date": general.get("IPODate"),
                "fiscal_year_end": general.get("FiscalYearEnd"),
                "updated_at": general.get("UpdatedAt")
            }

            # Handle market cap conversion (often in millions)
            if general.get("MarketCapitalization"):
                profile["market_cap_gbp"] = float(general.get("MarketCapitalization", 0))

            # Cache the result
            self._add_to_cache(cache_key, profile)

            logger.info(
                "eodhd_profile_fetched",
                ticker=ticker,
                sector=profile.get("sector"),
                industry=profile.get("industry")
            )

            return profile

        except Exception as e:
            logger.error(
                "eodhd_fetch_profile_error",
                ticker=ticker,
                error=str(e),
                error_type=type(e).__name__
            )
            return {}

    async def fetch_analyst_estimates(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch analyst estimates (EPS, revenue consensus, number of analysts).

        Args:
            ticker: EODHD ticker (e.g., "VOD.LSE")

        Returns:
            Dictionary with analyst estimates or empty dict if fetch fails
        """
        cache_key = f"{ticker}:estimates"

        # Check cache first
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            logger.debug("eodhd_cache_hit", cache_key=cache_key, data_type="estimates")
            return cached_data

        # Check rate limit
        if not self._check_rate_limit():
            raise EODHDRateLimitExceeded("Daily rate limit exceeded")

        # Try to get analyst ratings from fundamentals endpoint
        url = f"{self.BASE_URL}/fundamentals/{ticker}"
        params = {
            "api_token": self.api_key,
            "filter": "AnalystRatings::Rating",
            "fmt": "json"
        }

        try:
            response = await self._make_request_with_retry(url, params)
            if not response:
                logger.info(
                    "eodhd_no_analyst_coverage",
                    ticker=ticker,
                    message="No analyst coverage available"
                )
                return {}

            # Handle different response formats
            # Sometimes EODHD returns just a value when using filter, not a dict
            if not isinstance(response, dict):
                logger.info(
                    "eodhd_simple_rating_response",
                    ticker=ticker,
                    response_type=type(response).__name__,
                    message="Analyst data returned as simple value, not detailed object"
                )
                # If it's just a number, create minimal estimates
                if isinstance(response, (int, float)):
                    return {
                        "rating": response,
                        "total_analysts": 0,
                        "consensus": "UNKNOWN"
                    }
                return {}

            analyst_data = response.get("AnalystRatings", {})

            # Handle case where AnalystRatings might be a simple value or empty
            if not analyst_data or not isinstance(analyst_data, dict):
                logger.info(
                    "eodhd_no_analyst_coverage",
                    ticker=ticker,
                    analyst_data_type=type(analyst_data).__name__,
                    message="No analyst coverage available or unexpected format"
                )
                return {}

            # Extract analyst estimates
            estimates = {
                "rating": analyst_data.get("Rating"),
                "target_price": analyst_data.get("TargetPrice"),
                "strong_buy": analyst_data.get("StrongBuy", 0),
                "buy": analyst_data.get("Buy", 0),
                "hold": analyst_data.get("Hold", 0),
                "sell": analyst_data.get("Sell", 0),
                "strong_sell": analyst_data.get("StrongSell", 0),
                "raw_response": analyst_data
            }

            # Calculate total number of analysts
            estimates["total_analysts"] = sum([
                estimates.get("strong_buy", 0),
                estimates.get("buy", 0),
                estimates.get("hold", 0),
                estimates.get("sell", 0),
                estimates.get("strong_sell", 0)
            ])

            # Calculate consensus sentiment
            if estimates["total_analysts"] > 0:
                bullish = estimates.get("strong_buy", 0) + estimates.get("buy", 0)
                bearish = estimates.get("sell", 0) + estimates.get("strong_sell", 0)
                if bullish > bearish:
                    estimates["consensus"] = "BULLISH"
                elif bearish > bullish:
                    estimates["consensus"] = "BEARISH"
                else:
                    estimates["consensus"] = "NEUTRAL"
            else:
                estimates["consensus"] = "NO_COVERAGE"

            # Cache the result
            self._add_to_cache(cache_key, estimates)

            logger.info(
                "eodhd_estimates_fetched",
                ticker=ticker,
                total_analysts=estimates["total_analysts"],
                consensus=estimates.get("consensus")
            )

            return estimates

        except Exception as e:
            logger.error(
                "eodhd_fetch_estimates_error",
                ticker=ticker,
                error=str(e),
                error_type=type(e).__name__
            )
            return {}

    async def _make_request_with_retry(
        self,
        url: str,
        params: Dict[str, Any]
    ) -> Optional[Any]:
        """
        Make HTTP request with exponential backoff retry logic.

        Retries on:
        - 429 (rate limit)
        - 5xx (server errors)

        Does NOT retry on:
        - 4xx (except 429) - client errors

        Args:
            url: Request URL
            params: Query parameters

        Returns:
            JSON response or None if all retries fail
        """
        retry_delays = [1, 3, 9]  # Exponential backoff: 1s, 3s, 9s

        for attempt in range(self.max_retries):
            try:
                response = await self._client.get(url, params=params)

                # Track API call
                self._api_call_count += 1

                # Success
                if response.status_code == 200:
                    return response.json()

                # Rate limit - retry
                if response.status_code == 429:
                    logger.warning(
                        "eodhd_rate_limit",
                        url=url,
                        attempt=attempt + 1,
                        max_retries=self.max_retries
                    )
                    if attempt < self.max_retries - 1:
                        delay = retry_delays[attempt]
                        await asyncio.sleep(delay)
                        continue
                    raise EODHDRateLimitExceeded("Rate limit exceeded after retries")

                # Server error - retry
                if response.status_code >= 500:
                    logger.warning(
                        "eodhd_server_error",
                        status_code=response.status_code,
                        url=url,
                        attempt=attempt + 1,
                        max_retries=self.max_retries
                    )
                    if attempt < self.max_retries - 1:
                        delay = retry_delays[attempt]
                        await asyncio.sleep(delay)
                        continue
                    return None

                # Client error (4xx) - don't retry
                logger.error(
                    "eodhd_client_error",
                    status_code=response.status_code,
                    url=url,
                    response=response.text[:200]
                )
                return None

            except httpx.TimeoutException:
                logger.warning(
                    "eodhd_timeout",
                    url=url,
                    attempt=attempt + 1,
                    max_retries=self.max_retries
                )
                if attempt < self.max_retries - 1:
                    delay = retry_delays[attempt]
                    await asyncio.sleep(delay)
                    continue
                return None

            except EODHDRateLimitExceeded:
                # Re-raise rate limit exception
                raise

            except Exception as e:
                logger.error(
                    "eodhd_request_error",
                    error=str(e),
                    error_type=type(e).__name__,
                    url=url,
                    attempt=attempt + 1
                )
                if attempt < self.max_retries - 1:
                    delay = retry_delays[attempt]
                    await asyncio.sleep(delay)
                    continue
                return None

        return None

    def _check_rate_limit(self) -> bool:
        """
        Check if rate limit allows more API calls.

        Returns:
            True if call is allowed, False if rate limit exceeded
        """
        # Reset counter if it's a new day
        if datetime.now(timezone.utc) > self._rate_limit_reset_time:
            self._api_call_count = 0
            self._rate_limit_reset_time = datetime.now(timezone.utc) + timedelta(days=1)
            logger.info(
                "eodhd_rate_limit_reset",
                reset_time=self._rate_limit_reset_time.isoformat()
            )

        # Check if we're at 95% of limit (early warning)
        if self._api_call_count >= self.rate_limit_per_day * 0.95:
            logger.warning(
                "eodhd_rate_limit_approaching",
                current_calls=self._api_call_count,
                limit=self.rate_limit_per_day,
                percentage=round((self._api_call_count / self.rate_limit_per_day) * 100, 1)
            )

        # Check if limit exceeded
        if self._api_call_count >= self.rate_limit_per_day:
            logger.error(
                "eodhd_rate_limit_exceeded",
                current_calls=self._api_call_count,
                limit=self.rate_limit_per_day
            )
            return False

        return True

    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get data from cache if not expired."""
        if key not in self._cache:
            return None

        # Check if cache entry is still valid
        cached_time = self._cache_timestamps.get(key)
        if cached_time is None:
            return None

        age = datetime.now(timezone.utc) - cached_time
        if age.total_seconds() > self.cache_ttl_hours * 3600:
            # Cache expired
            logger.debug(
                "eodhd_cache_expired",
                cache_key=key,
                age_hours=age.total_seconds() / 3600
            )
            del self._cache[key]
            del self._cache_timestamps[key]
            return None

        return self._cache[key]

    def _add_to_cache(self, key: str, data: Any) -> None:
        """Add data to cache with timestamp."""
        self._cache[key] = data
        self._cache_timestamps[key] = datetime.now(timezone.utc)
        logger.debug(
            "eodhd_cache_add",
            cache_key=key,
            ttl_hours=self.cache_ttl_hours
        )

    def _get_cached_signals(self, ticker: str) -> List[Signal]:
        """Get all cached signals for a ticker."""
        cached_signals = []
        timestamp = datetime.now(timezone.utc)

        # Try to get cached data for each data type
        eodhd_ticker = self._format_ticker_for_api(ticker)

        fundamentals = self._get_from_cache(f"{eodhd_ticker}:fundamentals")
        if fundamentals:
            signal = Signal(
                ticker=ticker,
                signal_type="FUNDAMENTAL_DATA",
                score=self._calculate_fundamental_score(fundamentals),
                confidence=0.7,  # Lower confidence for cached data
                data={**fundamentals, "cached": True},
                timestamp=timestamp,
                source=self.get_source_name()
            )
            cached_signals.append(signal)

        return cached_signals

    def _format_ticker_for_api(self, ticker: str) -> str:
        """
        Format ticker for EODHD API.

        Converts UK tickers: "VOD.L" → "VOD.LSE"
        Leaves other tickers unchanged: "AAPL.US" → "AAPL.US"

        Args:
            ticker: Ticker with exchange suffix (e.g., "VOD.L", "AAPL.US")

        Returns:
            Ticker in EODHD format (e.g., "VOD.LSE", "AAPL.US")
        """
        # Convert UK tickers from .L to .LSE
        if ticker.endswith(".L"):
            return ticker.replace(".L", f".{self.EXCHANGE_CODE}")

        # Already in LSE format, keep as-is
        if ticker.endswith(".LSE"):
            return ticker

        # For all other tickers (US, etc.), return as-is
        # E.g., "AAPL.US" stays "AAPL.US", not "AAPL.US.LSE"
        return ticker

    def _convert_pence_to_pounds(self, value: float) -> float:
        """
        Convert pence to pounds for UK stocks.

        EODHD returns prices in the trading currency. UK stocks trade in pence
        but report financials in pounds. This method handles conversion when needed.

        Args:
            value: Price value (may be in pence or pounds)

        Returns:
            Value in pounds
        """
        # Threshold of 1000: UK stocks rarely trade above £1000/share, so values
        # >1000 are likely in pence (e.g., 14700 pence = £147). This heuristic
        # works for typical LSE stocks (FTSE 100/250 range £1-£100/share).
        if value > 1000:
            return round(value / 100, 2)
        return value

    def _calculate_fundamental_score(self, fundamentals: Dict[str, Any]) -> int:
        """
        Calculate signal score based on fundamental data.

        Uses key metrics like P/E ratio, ROE, debt levels, earnings growth.

        Args:
            fundamentals: Fundamental data dictionary

        Returns:
            Score from 0-100
        """
        score = 50  # Start neutral

        key_metrics = fundamentals.get("key_metrics", {})

        # P/E ratio scoring (lower is better for value)
        pe_ratio = key_metrics.get("pe_ratio")
        if pe_ratio:
            if 0 < pe_ratio < 15:
                score += 15  # Undervalued
            elif 15 <= pe_ratio < 25:
                score += 5  # Fair value

        # ROE scoring (higher is better)
        roe = key_metrics.get("roe")
        if roe:
            if roe > 15:
                score += 10
            elif roe > 10:
                score += 5

        # Debt to equity (lower is better)
        debt_to_equity = key_metrics.get("debt_to_equity")
        if debt_to_equity is not None:
            if debt_to_equity < 0.5:
                score += 10
            elif debt_to_equity < 1.0:
                score += 5

        # Earnings growth
        earnings_growth = key_metrics.get("quarterly_earnings_growth")
        if earnings_growth:
            if earnings_growth > 20:
                score += 10
            elif earnings_growth > 10:
                score += 5

        return max(0, min(100, int(score)))

    def _calculate_price_score(self, prices: Dict[str, Any]) -> int:
        """
        Calculate signal score based on price data.

        Uses momentum, volume trends.

        Args:
            prices: Price data dictionary

        Returns:
            Score from 0-100
        """
        score = 50  # Start neutral

        # Price momentum
        price_change = prices.get("price_change_30d", 0)
        if price_change > 10:
            score += 15
        elif price_change > 5:
            score += 10
        elif price_change < -10:
            score -= 15
        elif price_change < -5:
            score -= 10

        return max(0, min(100, int(score)))

    def _calculate_analyst_score(self, estimates: Dict[str, Any]) -> int:
        """
        Calculate signal score based on analyst estimates.

        Uses consensus ratings and number of analysts.

        Args:
            estimates: Analyst estimates dictionary

        Returns:
            Score from 0-100
        """
        score = 50  # Start neutral

        total_analysts = estimates.get("total_analysts", 0)
        if total_analysts == 0:
            return score  # No coverage, neutral score

        # Score based on consensus
        consensus = estimates.get("consensus", "NEUTRAL")
        if consensus == "BULLISH":
            score += 20
        elif consensus == "BEARISH":
            score -= 20

        # Adjust based on strength of consensus
        strong_buy = estimates.get("strong_buy", 0)
        strong_sell = estimates.get("strong_sell", 0)

        if total_analysts > 0:
            strong_buy_pct = (strong_buy / total_analysts) * 100
            strong_sell_pct = (strong_sell / total_analysts) * 100

            if strong_buy_pct > 50:
                score += 15
            elif strong_sell_pct > 50:
                score -= 15

        return max(0, min(100, int(score)))

    async def close(self):
        """Close HTTP client connection."""
        await self._client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
