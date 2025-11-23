"""
DataSourceRegistry for managing multiple data providers.

This module implements the Registry pattern to manage data sources,
allowing runtime registration, enabling/disabling, and parallel execution
of multiple providers with error isolation.
"""

import asyncio
import structlog
from typing import List, Dict, Optional
from datetime import datetime, timezone

from backend.app.data_sources.base import DataSource, Signal


logger = structlog.get_logger(__name__)


class DataSourceRegistry:
    """
    Registry for managing and executing multiple data sources.

    The registry provides:
    - Dynamic registration of data sources
    - Enable/disable functionality for sources
    - Parallel execution of all enabled sources
    - Error isolation (one source failure doesn't affect others)
    - Execution timing and logging

    Example:
        >>> registry = DataSourceRegistry()
        >>> registry.register(YahooFinanceProvider())
        >>> registry.register(EODHDProvider())
        >>> registry.enable("yahoo_finance")
        >>> registry.enable("eodhd_fundamental")
        >>>
        >>> # Fetch from all enabled sources in parallel
        >>> signals = await registry.fetch_all()
        >>> print(f"Got {len(signals)} signals from {len(registry.list_enabled())} sources")
    """

    def __init__(self):
        """Initialize empty registry."""
        self._sources: Dict[str, DataSource] = {}
        self._enabled: Dict[str, bool] = {}
        self._execution_stats: Dict[str, Dict] = {}

    def register(self, source: DataSource) -> None:
        """
        Register a new data source.

        The source is registered but NOT automatically enabled.
        Use enable() to activate it.

        Args:
            source: DataSource implementation to register

        Raises:
            ValueError: If source with same name already registered
        """
        source_name = source.get_source_name()

        if source_name in self._sources:
            raise ValueError(f"Source '{source_name}' already registered")

        self._sources[source_name] = source
        self._enabled[source_name] = False

        logger.info(
            "data_source_registered",
            source=source_name,
            total_sources=len(self._sources)
        )

    def unregister(self, source_name: str) -> None:
        """
        Unregister a data source.

        Args:
            source_name: Name of source to remove

        Raises:
            KeyError: If source not found
        """
        if source_name not in self._sources:
            raise KeyError(f"Source '{source_name}' not registered")

        del self._sources[source_name]
        del self._enabled[source_name]

        logger.info(
            "data_source_unregistered",
            source=source_name,
            remaining_sources=len(self._sources)
        )

    def enable(self, source_name: str) -> None:
        """
        Enable a registered source for fetching.

        Args:
            source_name: Name of source to enable

        Raises:
            KeyError: If source not registered
        """
        if source_name not in self._sources:
            raise KeyError(f"Source '{source_name}' not registered")

        self._enabled[source_name] = True
        logger.info("data_source_enabled", source=source_name)

    def disable(self, source_name: str) -> None:
        """
        Disable a source (won't be called during fetch_all).

        Args:
            source_name: Name of source to disable

        Raises:
            KeyError: If source not registered
        """
        if source_name not in self._sources:
            raise KeyError(f"Source '{source_name}' not registered")

        self._enabled[source_name] = False
        logger.info("data_source_disabled", source=source_name)

    def is_enabled(self, source_name: str) -> bool:
        """
        Check if a source is enabled.

        Args:
            source_name: Name of source to check

        Returns:
            True if source is registered and enabled, False otherwise
        """
        return self._enabled.get(source_name, False)

    def list_all(self) -> List[str]:
        """
        List all registered source names.

        Returns:
            List of source names (both enabled and disabled)
        """
        return list(self._sources.keys())

    def list_enabled(self) -> List[str]:
        """
        List all enabled source names.

        Returns:
            List of enabled source names
        """
        return [name for name, enabled in self._enabled.items() if enabled]

    def get_execution_stats(self, source_name: Optional[str] = None) -> Dict:
        """
        Get execution statistics for sources.

        Args:
            source_name: Optional specific source name. If None, returns all.

        Returns:
            Dictionary of execution stats (timing, signal counts, errors)
        """
        if source_name:
            return self._execution_stats.get(source_name, {})
        return self._execution_stats.copy()

    async def fetch_all(self) -> List[Signal]:
        """
        Fetch data from all enabled sources in parallel.

        This method:
        1. Identifies all enabled sources
        2. Executes them in parallel using asyncio.gather()
        3. Isolates errors (one source failure doesn't crash others)
        4. Tracks execution timing and signal counts
        5. Returns aggregated signals from all successful sources

        Returns:
            List of Signal objects from all successful sources.
            Empty list if no sources enabled or all sources failed.

        Example:
            >>> registry = DataSourceRegistry()
            >>> registry.register(source1)
            >>> registry.register(source2)
            >>> registry.enable("source1")
            >>> registry.enable("source2")
            >>>
            >>> signals = await registry.fetch_all()
            >>> # If source1 returns 10 signals and source2 returns 5,
            >>> # signals will contain all 15 signals
        """
        enabled_sources = [
            (name, source)
            for name, source in self._sources.items()
            if self._enabled.get(name, False)
        ]

        if not enabled_sources:
            logger.warning("no_enabled_sources", message="No data sources enabled")
            return []

        logger.info(
            "fetch_all_started",
            enabled_sources=[name for name, _ in enabled_sources],
            count=len(enabled_sources)
        )

        # Execute all sources in parallel with error isolation
        tasks = [
            self._fetch_with_stats(name, source)
            for name, source in enabled_sources
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Aggregate signals from successful sources
        all_signals = []
        successful_count = 0
        failed_count = 0

        for result in results:
            if isinstance(result, Exception):
                # Exception already logged in _fetch_with_stats
                failed_count += 1
            elif isinstance(result, list):
                all_signals.extend(result)
                successful_count += 1

        logger.info(
            "fetch_all_completed",
            total_signals=len(all_signals),
            successful_sources=successful_count,
            failed_sources=failed_count,
            enabled_sources=len(enabled_sources)
        )

        return all_signals

    async def _fetch_with_stats(
        self,
        source_name: str,
        source: DataSource
    ) -> List[Signal]:
        """
        Fetch from a single source with timing and error handling.

        Args:
            source_name: Name of the source (for logging)
            source: DataSource instance to fetch from

        Returns:
            List of Signal objects from this source

        Raises:
            Any exception from source.fetch() (caught by asyncio.gather)
        """
        start_time = datetime.now(timezone.utc)

        try:
            logger.info("source_fetch_started", source=source_name)

            signals = await source.fetch()

            end_time = datetime.now(timezone.utc)
            duration_ms = int((end_time - start_time).total_seconds() * 1000)

            # Update stats
            self._execution_stats[source_name] = {
                "last_execution": end_time.isoformat(),
                "duration_ms": duration_ms,
                "signal_count": len(signals),
                "status": "success",
                "error": None
            }

            logger.info(
                "source_fetch_completed",
                source=source_name,
                signal_count=len(signals),
                duration_ms=duration_ms
            )

            return signals

        except Exception as e:
            end_time = datetime.now(timezone.utc)
            duration_ms = int((end_time - start_time).total_seconds() * 1000)

            # Update stats with error
            self._execution_stats[source_name] = {
                "last_execution": end_time.isoformat(),
                "duration_ms": duration_ms,
                "signal_count": 0,
                "status": "error",
                "error": str(e)
            }

            logger.error(
                "source_fetch_failed",
                source=source_name,
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=duration_ms
            )

            # Re-raise to be caught by asyncio.gather
            raise
