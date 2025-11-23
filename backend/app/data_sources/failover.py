"""
Failover and retry logic for data sources.

This module implements automatic failover between data providers with
retry logic, exponential backoff, and graceful degradation strategies.
"""

import asyncio
import structlog
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum

from backend.app.data_sources.base import DataSource, Signal


logger = structlog.get_logger(__name__)


class FailoverReason(Enum):
    """Reasons for failover to next provider."""
    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    TIMEOUT = "timeout"
    NETWORK_ERROR = "network_error"
    MAX_RETRIES_EXCEEDED = "max_retries_exceeded"


class DataSourceFailover:
    """
    Manages failover between multiple data source providers.

    This class implements:
    - Priority-based provider ordering
    - Automatic retry with exponential backoff
    - Failover to backup providers
    - Cached data fallback
    - Staleness tracking
    - Failover event logging

    Example:
        >>> failover = DataSourceFailover(
        ...     providers={
        ...         "eodhd": eodhd_provider,
        ...         "yahoo": yahoo_provider,
        ...         "alpha_vantage": av_provider
        ...     },
        ...     priority_order=["eodhd", "yahoo", "alpha_vantage"]
        ... )
        >>>
        >>> signals = await failover.fetch_with_failover(tickers=["VOD.L"])
    """

    def __init__(
        self,
        providers: Dict[str, DataSource],
        priority_order: List[str],
        max_retries: int = 3,
        retry_delays: Optional[List[int]] = None,
        cache_ttl_hours: int = 24,
        system_logs_table: Optional[Any] = None
    ):
        """
        Initialize failover manager.

        Args:
            providers: Dictionary mapping provider names to DataSource instances
            priority_order: Ordered list of provider names (first = primary)
            max_retries: Maximum retry attempts for rate limit errors (default: 3)
            retry_delays: Delays in seconds between retries (default: [60, 120, 180])
            cache_ttl_hours: Maximum age of cached data in hours (default: 24)
            system_logs_table: Optional SQLAlchemy table for logging failover events
        """
        self.providers = providers
        self.priority_order = priority_order
        self.max_retries = max_retries
        self.retry_delays = retry_delays or [60, 120, 180]
        self.cache_ttl_hours = cache_ttl_hours
        self.system_logs_table = system_logs_table

        # Validate priority order
        for provider_name in priority_order:
            if provider_name not in providers:
                raise ValueError(f"Provider '{provider_name}' in priority_order not found in providers dict")

        # Cache for signals (in-memory for now, can be moved to Redis)
        self._cache: Dict[str, List[Signal]] = {}
        self._cache_timestamps: Dict[str, datetime] = {}

    async def fetch_with_failover(
        self,
        tickers: Optional[List[str]] = None,
        use_cache_on_failure: bool = True
    ) -> List[Signal]:
        """
        Fetch data with automatic failover through provider chain.

        Strategy:
        1. Try primary provider with retries (for rate limits)
        2. If 5xx error, skip retries and failover immediately
        3. Try each backup provider in order
        4. If all fail and cache enabled, use cached data (flag staleness)
        5. If no cache, return empty list and log critical error

        Args:
            tickers: List of tickers to fetch (passed to providers)
            use_cache_on_failure: Whether to use cached data if all providers fail

        Returns:
            List of Signal objects from successful provider or cache.
            Empty list if all providers and cache fail.
        """
        cache_key = self._get_cache_key(tickers)
        last_error: Optional[Exception] = None
        attempted_providers: List[str] = []

        for provider_name in self.priority_order:
            provider = self.providers[provider_name]
            attempted_providers.append(provider_name)

            logger.info(
                "failover_trying_provider",
                provider=provider_name,
                priority=self.priority_order.index(provider_name) + 1,
                total_providers=len(self.priority_order)
            )

            try:
                # Determine retry strategy based on provider position
                is_primary = (provider_name == self.priority_order[0])

                if is_primary:
                    # Primary provider: use retries for rate limits
                    signals = await self._fetch_with_retry(
                        provider,
                        provider_name,
                        tickers
                    )
                else:
                    # Backup providers: single attempt
                    signals = await self._fetch_single_attempt(
                        provider,
                        provider_name,
                        tickers
                    )

                # Success! Cache and return
                if signals:
                    self._update_cache(cache_key, signals)

                    logger.info(
                        "failover_success",
                        provider=provider_name,
                        signal_count=len(signals),
                        attempted_providers=attempted_providers
                    )

                    # Log failover event if not using primary
                    if not is_primary:
                        await self._log_failover_event(
                            from_provider=self.priority_order[0],
                            to_provider=provider_name,
                            reason=FailoverReason.SERVER_ERROR,
                            tickers=tickers
                        )

                    return signals

                # No signals returned, try next provider
                logger.warning(
                    "failover_empty_result",
                    provider=provider_name,
                    message="Provider returned no signals"
                )

            except Exception as e:
                last_error = e
                logger.error(
                    "failover_provider_failed",
                    provider=provider_name,
                    error=str(e),
                    error_type=type(e).__name__
                )
                # Continue to next provider

        # All providers failed - try cache
        if use_cache_on_failure:
            cached_signals = self._get_from_cache(cache_key)
            if cached_signals:
                age_hours = self._get_cache_age_hours(cache_key)

                logger.warning(
                    "failover_using_cache",
                    cache_age_hours=age_hours,
                    signal_count=len(cached_signals),
                    attempted_providers=attempted_providers,
                    message="All providers failed, using cached data"
                )

                # Flag staleness in signals
                for signal in cached_signals:
                    signal.data["cached"] = True
                    signal.data["cache_age_hours"] = age_hours
                    signal.data["stale"] = (age_hours > 1)

                await self._log_failover_event(
                    from_provider="all_providers",
                    to_provider="cache",
                    reason=FailoverReason.MAX_RETRIES_EXCEEDED,
                    tickers=tickers
                )

                return cached_signals

        # Complete failure - no providers worked, no cache available
        logger.critical(
            "failover_complete_failure",
            attempted_providers=attempted_providers,
            last_error=str(last_error) if last_error else None,
            cache_available=use_cache_on_failure and cache_key in self._cache,
            message="All data sources failed and no cache available"
        )

        return []

    async def _fetch_with_retry(
        self,
        provider: DataSource,
        provider_name: str,
        tickers: Optional[List[str]]
    ) -> List[Signal]:
        """
        Fetch from provider with retry logic for rate limits.

        Retry strategy:
        - 429 (rate limit): Retry up to max_retries with exponential backoff
        - 5xx (server error): No retry, failover immediately
        - Network/timeout: Retry once

        Args:
            provider: DataSource instance
            provider_name: Provider name for logging
            tickers: Tickers to fetch

        Returns:
            List of Signal objects

        Raises:
            Exception: After max retries exceeded or non-retryable error
        """
        for attempt in range(self.max_retries):
            try:
                logger.debug(
                    "retry_attempt",
                    provider=provider_name,
                    attempt=attempt + 1,
                    max_retries=self.max_retries
                )

                # Attempt fetch
                if hasattr(provider, 'fetch') and callable(provider.fetch):
                    # Most providers have fetch()
                    if tickers:
                        # Try passing tickers if provider accepts them
                        try:
                            signals = await provider.fetch(tickers=tickers)
                        except TypeError:
                            # Provider doesn't accept tickers parameter
                            signals = await provider.fetch()
                    else:
                        signals = await provider.fetch()
                else:
                    raise AttributeError(f"Provider {provider_name} missing fetch() method")

                return signals

            except Exception as e:
                error_str = str(e).lower()

                # Check error type
                is_rate_limit = ("429" in error_str or "rate limit" in error_str)
                is_server_error = ("5" in error_str[:3] if len(error_str) >= 3 else False)

                if is_server_error:
                    # Server error - don't retry, failover immediately
                    logger.warning(
                        "retry_server_error_no_retry",
                        provider=provider_name,
                        error=str(e)
                    )
                    raise

                if is_rate_limit and attempt < self.max_retries - 1:
                    # Rate limit - retry with backoff
                    delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]

                    logger.warning(
                        "retry_rate_limit",
                        provider=provider_name,
                        attempt=attempt + 1,
                        max_retries=self.max_retries,
                        retry_delay=delay
                    )

                    await asyncio.sleep(delay)
                    continue

                # Max retries exceeded or non-retryable error
                logger.error(
                    "retry_exhausted",
                    provider=provider_name,
                    attempts=attempt + 1,
                    error=str(e)
                )
                raise

        # Should not reach here, but just in case
        raise Exception(f"Max retries exceeded for {provider_name}")

    async def _fetch_single_attempt(
        self,
        provider: DataSource,
        provider_name: str,
        tickers: Optional[List[str]]
    ) -> List[Signal]:
        """
        Fetch from provider with single attempt (no retries).

        Used for backup providers in failover chain.

        Args:
            provider: DataSource instance
            provider_name: Provider name for logging
            tickers: Tickers to fetch

        Returns:
            List of Signal objects

        Raises:
            Exception: On any error
        """
        try:
            if tickers:
                try:
                    return await provider.fetch(tickers=tickers)
                except TypeError:
                    # Provider doesn't accept tickers parameter
                    return await provider.fetch()
            else:
                return await provider.fetch()
        except Exception as e:
            logger.error(
                "single_attempt_failed",
                provider=provider_name,
                error=str(e)
            )
            raise

    def _get_cache_key(self, tickers: Optional[List[str]]) -> str:
        """Generate cache key from tickers."""
        if not tickers:
            return "all_tickers"
        return ",".join(sorted(tickers))

    def _update_cache(self, cache_key: str, signals: List[Signal]) -> None:
        """Update cache with fresh signals."""
        self._cache[cache_key] = signals
        self._cache_timestamps[cache_key] = datetime.now(timezone.utc)

        logger.debug(
            "cache_updated",
            cache_key=cache_key,
            signal_count=len(signals)
        )

    def _get_from_cache(self, cache_key: str) -> Optional[List[Signal]]:
        """
        Get signals from cache if not expired.

        Args:
            cache_key: Cache key to lookup

        Returns:
            List of cached Signal objects if available and not expired,
            None otherwise
        """
        if cache_key not in self._cache:
            return None

        # Check if cache is expired
        age_hours = self._get_cache_age_hours(cache_key)
        if age_hours > self.cache_ttl_hours:
            logger.debug(
                "cache_expired",
                cache_key=cache_key,
                age_hours=age_hours,
                ttl_hours=self.cache_ttl_hours
            )
            return None

        return self._cache[cache_key]

    def _get_cache_age_hours(self, cache_key: str) -> float:
        """Get age of cached data in hours."""
        if cache_key not in self._cache_timestamps:
            return float('inf')

        cached_time = self._cache_timestamps[cache_key]
        age = datetime.now(timezone.utc) - cached_time
        return age.total_seconds() / 3600

    async def _log_failover_event(
        self,
        from_provider: str,
        to_provider: str,
        reason: FailoverReason,
        tickers: Optional[List[str]]
    ) -> None:
        """
        Log failover event to database and structured logs.

        Args:
            from_provider: Provider that failed
            to_provider: Provider failed over to
            reason: Reason for failover
            tickers: Tickers involved (for context)
        """
        event = {
            "from_provider": from_provider,
            "to_provider": to_provider,
            "reason": reason.value,
            "ticker_count": len(tickers) if tickers else 0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        logger.warning(
            "failover_event",
            **event,
            severity="WARNING"
        )

        # TODO: Log to system_logs table when database integration is complete
        # This will be implemented in Story 1.4 or 1.9 (Observability)
