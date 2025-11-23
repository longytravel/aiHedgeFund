"""
Abstract base class for data sources and standardized Signal dataclass.

This module defines the interface that all data providers must implement,
ensuring consistent data fetching and signal generation across the system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class Signal:
    """
    Standardized signal dataclass returned by all data sources.

    All data providers must return signals in this format to ensure
    consistent processing by the agent system.

    Attributes:
        ticker: Stock ticker in LSE format (e.g., "VOD.L")
        signal_type: Type of signal (e.g., "NEWS_CATALYST", "INSIDER_CONVICTION")
        score: Base signal strength (0-100, before multipliers)
        confidence: Provider confidence in signal accuracy (0.0-1.0)
        data: Provider-specific metadata (stored in Signal.data JSONB field)
        timestamp: When the signal was generated (UTC timezone-aware)
        source: Source identifier (e.g., "news_scanner", "eodhd_fundamental")

    Example:
        >>> signal = Signal(
        ...     ticker="VOD.L",
        ...     signal_type="INSIDER_CONVICTION",
        ...     score=80,
        ...     confidence=0.9,
        ...     data={"director": "CEO", "shares_bought": 100000},
        ...     timestamp=datetime.now(timezone.utc),
        ...     source="insider_trading"
        ... )
    """
    ticker: str
    signal_type: str
    score: int  # 0-100
    confidence: float  # 0.0-1.0
    data: Dict[str, Any]
    timestamp: datetime
    source: str

    def __post_init__(self):
        """Validate signal fields after initialization."""
        # Validate ticker format
        if not isinstance(self.ticker, str) or len(self.ticker) < 3:
            raise ValueError(f"Invalid ticker: {self.ticker}")

        # Validate score range
        if not 0 <= self.score <= 100:
            raise ValueError(f"Score must be 0-100, got {self.score}")

        # Validate confidence range
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be 0.0-1.0, got {self.confidence}")

        # Ensure timestamp is timezone-aware
        if self.timestamp.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware")


class DataSource(ABC):
    """
    Abstract base class for all data providers.

    All data sources (EODHD, Yahoo Finance, Alpha Vantage, file inbox, etc.)
    must implement this interface to ensure they can be used interchangeably
    by the DataSourceRegistry.

    The interface enforces two key requirements:
    1. Async data fetching (non-blocking I/O for performance)
    2. Standardized signal return format (Signal dataclass)

    Example Implementation:
        >>> class YahooFinanceProvider(DataSource):
        ...     def __init__(self, config: dict):
        ...         self.config = config
        ...
        ...     async def fetch(self) -> List[Signal]:
        ...         # Fetch data from Yahoo Finance
        ...         data = await self._fetch_yahoo_data()
        ...
        ...         # Convert to standardized signals
        ...         signals = []
        ...         for ticker, price_data in data.items():
        ...             signal = Signal(
        ...                 ticker=ticker,
        ...                 signal_type="PRICE_UPDATE",
        ...                 score=50,
        ...                 confidence=0.8,
        ...                 data=price_data,
        ...                 timestamp=datetime.now(timezone.utc),
        ...                 source="yahoo_finance"
        ...             )
        ...             signals.append(signal)
        ...
        ...         return signals
        ...
        ...     def get_source_name(self) -> str:
        ...         return "yahoo_finance"
    """

    @abstractmethod
    async def fetch(self) -> List[Signal]:
        """
        Fetch data from the provider and return normalized signals.

        This method should:
        1. Connect to the data source (API, file, database, etc.)
        2. Retrieve relevant data
        3. Transform data into standardized Signal objects
        4. Handle errors gracefully (log but don't crash)

        Returns:
            List of Signal objects. Empty list if no data available.

        Raises:
            Should NOT raise exceptions for normal failures (network errors,
            API quota exceeded, etc.). Instead, log the error and return
            empty list. Only raise for programming errors (config issues, etc.).
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """
        Return unique identifier for this data source.

        This name is used for:
        - Logging and observability
        - Configuration management (enable/disable sources)
        - Signal source tracking

        Returns:
            Lowercase snake_case identifier (e.g., "eodhd_fundamental",
            "yahoo_finance", "manual_csv_inbox")

        Example:
            >>> provider = EODHDProvider(api_key="...")
            >>> provider.get_source_name()
            "eodhd_fundamental"
        """
        pass
