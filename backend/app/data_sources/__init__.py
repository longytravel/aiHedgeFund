"""
Data sources package for AIHedgeFund.

This package provides an abstract interface for data providers
and concrete implementations for various data sources (EODHD, Yahoo Finance, Alpha Vantage).
"""

from backend.app.data_sources.base import DataSource, Signal
from backend.app.data_sources.providers.eodhd_provider import EODHDProvider

__all__ = ["DataSource", "Signal", "EODHDProvider"]
