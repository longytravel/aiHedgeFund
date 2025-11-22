# API Integration Points for UK Market Data

**Generated:** 2025-11-22
**Purpose:** Know exactly where to plug in UK market data sources using the simplified 3-tier architecture

---

## Architecture Overview

The system uses a **3-tier simplified architecture** that eliminates multi-source complexity:

1. **Tier 1 - Core Data (EODHD):** Fundamentals, history, estimates, macro
2. **Tier 2 - Intelligence (CityFALCON):** RNS feeds, director dealings, sentiment
3. **Tier 3 - Execution (IBKR):** Real-time quotes for trade execution

**File:** `src/tools/market_data.py` (unified interface)

---

## Tier 1: EODHD All-In-One Integration

### Provider Details

- **Website:** https://eodhd.com/
- **Plan:** All-In-One Package
- **Cost:** ~£85/month ($99.99/month)
- **API Docs:** https://eodhd.com/financial-apis/

### API Integration

**File:** `src/data_sources/eodhd_client.py`

```python
import requests
import os
from datetime import datetime

class EODHDClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("EODHD_API_KEY")
        self.base_url = "https://eodhistoricaldata.com/api"
        self.session = requests.Session()

    # ========================================
    # PRICE DATA
    # ========================================

    def get_prices(self, ticker: str, start_date: str, end_date: str, exchange="LSE"):
        """
        Fetch historical EOD prices.

        Args:
            ticker: Base ticker (e.g., "VOD")
            start_date: YYYY-MM-DD
            end_date: YYYY-MM-DD
            exchange: Default "LSE" for London Stock Exchange

        Returns:
            List of dicts with OHLCV data
        """
        url = f"{self.base_url}/eod/{ticker}.{exchange}"
        params = {
            'api_token': self.api_key,
            'from': start_date,
            'to': end_date,
            'fmt': 'json'
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ========================================
    # FUNDAMENTALS
    # ========================================

    def get_fundamentals(self, ticker: str, exchange="LSE"):
        """
        Fetch complete fundamental data package.

        Returns:
            Dict containing:
            - General: Company info, sector, industry
            - Highlights: Market cap, P/E, dividend yield
            - Valuation: EV, P/B, PEG, ratios
            - Financials: Income, balance sheet, cash flow
            - Earnings: Historical and estimates
            - AnalystRatings: Consensus ratings
        """
        url = f"{self.base_url}/fundamentals/{ticker}.{exchange}"
        params = {
            'api_token': self.api_key,
            'fmt': 'json'
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_financial_ratios(self, ticker: str, exchange="LSE"):
        """Extract just the ratios from fundamentals."""
        fundamentals = self.get_fundamentals(ticker, exchange)
        return {
            'pe_ratio': fundamentals.get('Highlights', {}).get('PERatio'),
            'pb_ratio': fundamentals.get('Highlights', {}).get('PriceToBookMRQ'),
            'peg_ratio': fundamentals.get('Valuation', {}).get('PEGRatio'),
            'roe': fundamentals.get('Highlights', {}).get('ReturnOnEquityTTM'),
            'roa': fundamentals.get('Highlights', {}).get('ReturnOnAssetsTTM'),
            'debt_to_equity': fundamentals.get('Highlights', {}).get('DebtToEquity'),
            'current_ratio': fundamentals.get('Valuation', {}).get('CurrentRatio'),
            'quick_ratio': fundamentals.get('Valuation', {}).get('QuickRatio'),
        }

    # ========================================
    # ANALYST ESTIMATES
    # ========================================

    def get_analyst_estimates(self, ticker: str, exchange="LSE"):
        """
        Fetch analyst estimates and earnings data.
        Includes consensus revenue/EPS estimates.
        """
        fundamentals = self.get_fundamentals(ticker, exchange)
        return {
            'earnings_trend': fundamentals.get('Earnings', {}).get('Trend'),
            'earnings_annual': fundamentals.get('Earnings', {}).get('Annual'),
            'earnings_history': fundamentals.get('Earnings', {}).get('History'),
            'analyst_ratings': fundamentals.get('AnalystRatings'),
        }

    # ========================================
    # CORPORATE ACTIONS
    # ========================================

    def get_dividends(self, ticker: str, start_date: str, end_date: str, exchange="LSE"):
        """Fetch dividend history."""
        url = f"{self.base_url}/div/{ticker}.{exchange}"
        params = {
            'api_token': self.api_key,
            'from': start_date,
            'to': end_date,
            'fmt': 'json'
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_splits(self, ticker: str, start_date: str, end_date: str, exchange="LSE"):
        """Fetch stock split history."""
        url = f"{self.base_url}/splits/{ticker}.{exchange}"
        params = {
            'api_token': self.api_key,
            'from': start_date,
            'to': end_date,
            'fmt': 'json'
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ========================================
    # EARNINGS CALENDAR
    # ========================================

    def get_earnings_calendar(self, start_date: str, end_date: str, ticker=None):
        """
        Fetch upcoming earnings dates.
        Can filter by ticker or get all UK stocks.
        """
        url = f"{self.base_url}/calendar/earnings"
        params = {
            'api_token': self.api_key,
            'from': start_date,
            'to': end_date,
            'fmt': 'json'
        }
        if ticker:
            params['symbols'] = f"{ticker}.LSE"

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ========================================
    # MACROECONOMIC DATA
    # ========================================

    def get_macro_indicator(self, country="GBR", indicator="GDP"):
        """
        Fetch macro indicators for UK.

        Common indicators:
        - GDP: Gross Domestic Product
        - CPI: Consumer Price Index (inflation)
        - interest_rate: Bank of England base rate
        - unemployment_rate
        """
        url = f"{self.base_url}/macro-indicator/{country}"
        params = {
            'api_token': self.api_key,
            'indicator': indicator,
            'fmt': 'json'
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
```

**Environment Variables:**

```bash
# .env file
EODHD_API_KEY=your_eodhd_api_key_here
```

---

## Tier 2: CityFALCON Integration

### Provider Details

- **Website:** https://www.cityfalcon.ai/
- **Plan:** Personal Silver/Gold or Commercial Starter
- **Cost:** ~£15-40/month
- **API Docs:** https://www.cityfalcon.ai/api-documentation

### API Integration

**File:** `src/data_sources/cityfalcon_client.py`

```python
import requests
import os
from datetime import datetime, timedelta

class CityFALCONClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("CITYFALCON_API_KEY")
        self.base_url = "https://api.cityfalcon.com/v0.2"
        self.session = requests.Session()

    # ========================================
    # NEWS & SENTIMENT
    # ========================================

    def get_news(self, ticker: str, days=7, categories=None):
        """
        Fetch recent news for a UK ticker.

        Args:
            ticker: Base ticker (e.g., "VOD")
            days: Number of days to look back
            categories: Filter by category (e.g., ["mp"] for M&A)

        Returns:
            List of news stories with sentiment scores
        """
        url = f"{self.base_url}/stories"
        params = {
            'access_token': self.api_key,
            'identifiers': f'{ticker}.LSE',
            'time_filter': f'd{days}',
            'languages': 'en'
        }

        if categories:
            params['categories'] = ','.join(categories)

        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse and structure
        stories = []
        for story in data.get('stories', []):
            stories.append({
                'title': story['title'],
                'description': story.get('description', ''),
                'url': story['url'],
                'published': story['publishTime'],
                'sentiment_score': story.get('score', 0),  # CityFALCON proprietary score
                'source': story.get('source', {}).get('name'),
                'categories': story.get('categories', [])
            })

        return stories

    # ========================================
    # DIRECTOR DEALINGS (High-Signal Data!)
    # ========================================

    def get_director_dealings(self, ticker: str, days=30):
        """
        Fetch UK director dealing announcements (PDMR notifications).
        This is insider trading data specific to UK market.

        Category code: 'dir' for director dealings
        """
        url = f"{self.base_url}/stories"
        params = {
            'access_token': self.api_key,
            'identifiers': f'{ticker}.LSE',
            'categories': 'dir',  # Director dealings category
            'time_filter': f'd{days}'
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        stories = response.json().get('stories', [])

        # Parse director dealings
        dealings = []
        for story in stories:
            # CityFALCON structures RNS text
            dealings.append({
                'date': story['publishTime'],
                'title': story['title'],
                'description': story.get('description', ''),
                'url': story['url'],
                'sentiment': story.get('score', 0),
                'categories': story.get('categories', [])
            })

        return dealings

    # ========================================
    # RNS ANNOUNCEMENTS
    # ========================================

    def get_rns_announcements(self, ticker: str, days=7, category_filter=None):
        """
        Fetch UK RNS (Regulatory News Service) announcements.

        Common RNS categories:
        - 'dir': Director dealings
        - 'mp': M&A
        - 'res': Results/Earnings
        - 'div': Dividends
        - 'eq': Equity announcements
        """
        url = f"{self.base_url}/stories"
        params = {
            'access_token': self.api_key,
            'identifiers': f'{ticker}.LSE',
            'time_filter': f'd{days}',
            'languages': 'en'
        }

        if category_filter:
            params['categories'] = category_filter

        response = self.session.get(url, params=params)
        response.raise_for_status()

        stories = response.json().get('stories', [])
        return [{
            'date': s['publishTime'],
            'title': s['title'],
            'description': s.get('description', ''),
            'categories': s.get('categories', []),
            'url': s['url'],
            'sentiment': s.get('score', 0)
        } for s in stories]

    # ========================================
    # AGGREGATE SENTIMENT
    # ========================================

    def get_sentiment_summary(self, ticker: str, days=7):
        """
        Calculate aggregate sentiment from recent news.
        Returns average sentiment score and confidence.
        """
        news = self.get_news(ticker, days=days)

        if not news:
            return {'average_sentiment': 0, 'confidence': 0, 'article_count': 0}

        scores = [article['sentiment_score'] for article in news if article.get('sentiment_score')]

        if not scores:
            return {'average_sentiment': 0, 'confidence': 0, 'article_count': len(news)}

        avg_sentiment = sum(scores) / len(scores)

        # Confidence based on article count and score consistency
        import statistics
        score_variance = statistics.variance(scores) if len(scores) > 1 else 0
        confidence = min(1.0, len(scores) / 10) * (1.0 / (1.0 + score_variance))

        return {
            'average_sentiment': avg_sentiment,
            'confidence': confidence,
            'article_count': len(news),
            'score_range': (min(scores), max(scores))
        }
```

**Environment Variables:**

```bash
# .env file
CITYFALCON_API_KEY=your_cityfalcon_api_key_here
```

---

## Tier 3: Interactive Brokers Integration

### Provider Details

- **Website:** https://www.interactivebrokers.com/
- **Python Library:** `ib_insync`
- **Cost:** ~£10/month for LSE Level 1 market data subscription
- **API Docs:** https://ib-insync.readthedocs.io/

### API Integration

**File:** `src/data_sources/ibkr_client.py`

```python
from ib_insync import IB, Stock, LimitOrder, MarketOrder, util
import asyncio

class IBKRClient:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        """
        Initialize IBKR connection.

        Args:
            host: TWS/Gateway host (default localhost)
            port: 7497 for TWS paper trading, 7496 for live
            client_id: Unique client ID
        """
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False

    def connect(self):
        """Connect to IBKR TWS or Gateway."""
        if not self.connected:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            self.connected = True
            print(f"✓ Connected to IBKR at {self.host}:{self.port}")

    def disconnect(self):
        """Disconnect from IBKR."""
        if self.connected:
            self.ib.disconnect()
            self.connected = False

    # ========================================
    # REAL-TIME QUOTES (Execution Layer)
    # ========================================

    def get_realtime_quote(self, ticker: str, exchange='LSE', currency='GBP'):
        """
        Get real-time bid/ask for trade execution.
        This is used ONLY at point of trade, not for analysis.
        """
        if not self.connected:
            self.connect()

        # Create contract
        contract = Stock(ticker, exchange, currency)
        self.ib.qualifyContracts(contract)

        # Request market data
        ticker_obj = self.ib.reqMktData(contract, '', False, False)
        self.ib.sleep(2)  # Wait for data to arrive

        return {
            'ticker': ticker,
            'bid': ticker_obj.bid,
            'ask': ticker_obj.ask,
            'last': ticker_obj.last,
            'volume': ticker_obj.volume,
            'timestamp': ticker_obj.time
        }

    # ========================================
    # ORDER PLACEMENT
    # ========================================

    def place_limit_order(self, ticker: str, quantity: int, limit_price: float,
                          action='BUY', exchange='LSE', currency='GBP'):
        """
        Place limit order.

        Args:
            ticker: Base ticker (e.g., "VOD")
            quantity: Number of shares
            limit_price: Limit price in GBP
            action: 'BUY' or 'SELL'
        """
        if not self.connected:
            self.connect()

        contract = Stock(ticker, exchange, currency)
        self.ib.qualifyContracts(contract)

        order = LimitOrder(action, quantity, limit_price)
        trade = self.ib.placeOrder(contract, order)

        print(f"✓ Order placed: {action} {quantity} {ticker} @ £{limit_price}")
        return {
            'order_id': trade.order.orderId,
            'status': trade.orderStatus.status,
            'filled': trade.orderStatus.filled,
            'remaining': trade.orderStatus.remaining
        }

    def place_market_order(self, ticker: str, quantity: int, action='BUY',
                           exchange='LSE', currency='GBP'):
        """Place market order (immediate execution)."""
        if not self.connected:
            self.connect()

        contract = Stock(ticker, exchange, currency)
        self.ib.qualifyContracts(contract)

        order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(contract, order)

        print(f"✓ Market order placed: {action} {quantity} {ticker}")
        return {
            'order_id': trade.order.orderId,
            'status': trade.orderStatus.status
        }

    # ========================================
    # PORTFOLIO TRACKING
    # ========================================

    def get_portfolio_positions(self):
        """Get current portfolio positions."""
        if not self.connected:
            self.connect()

        positions = []
        for position in self.ib.portfolio():
            positions.append({
                'ticker': position.contract.symbol,
                'quantity': position.position,
                'average_cost': position.averageCost,
                'market_value': position.marketValue,
                'unrealized_pnl': position.unrealizedPNL,
                'realized_pnl': position.realizedPNL
            })

        return positions
```

**Environment Variables:**

```bash
# .env file
IBKR_HOST=127.0.0.1
IBKR_PORT=7497  # Paper trading, use 7496 for live
IBKR_CLIENT_ID=1
```

---

## Unified Market Data Interface

**File:** `src/data_sources/market_data.py`

This provides a single unified interface to all three tiers:

```python
"""
Unified market data interface.
Simplifies agent code - agents just call get_prices(), get_news(), etc.
"""

import os
from datetime import datetime, timedelta
from src.data_sources.eodhd_client import EODHDClient
from src.data_sources.cityfalcon_client import CityFALCONClient
from src.data_sources.ibkr_client import IBKRClient
from src.data.cache import CacheLayer

# Initialize clients (singleton pattern)
_eodhd = EODHDClient()
_cityfalcon = CityFALCONClient()
_ibkr = IBKRClient()
_cache = CacheLayer()

# ========================================
# PRICE DATA (Tier 1: EODHD)
# ========================================

def get_prices(ticker: str, start_date: str, end_date: str):
    """Fetch EOD prices with caching."""
    cache_key = f"prices:{ticker}:{start_date}:{end_date}"

    if cached := _cache.get(cache_key):
        return cached

    prices = _eodhd.get_prices(ticker, start_date, end_date)
    _cache.set(cache_key, prices, ttl=86400)  # Cache 24 hours
    return prices

# ========================================
# FUNDAMENTALS (Tier 1: EODHD)
# ========================================

def get_fundamentals(ticker: str):
    """Fetch fundamental data with caching."""
    cache_key = f"fundamentals:{ticker}"

    if cached := _cache.get(cache_key):
        return cached

    fundamentals = _eodhd.get_fundamentals(ticker)
    _cache.set(cache_key, fundamentals, ttl=604800)  # Cache 7 days
    return fundamentals

def get_financial_ratios(ticker: str):
    """Get just the key ratios."""
    return _eodhd.get_financial_ratios(ticker)

# ========================================
# NEWS & SENTIMENT (Tier 2: CityFALCON)
# ========================================

def get_news(ticker: str, days=7):
    """Fetch recent news with sentiment."""
    cache_key = f"news:{ticker}:{days}"

    if cached := _cache.get(cache_key):
        return cached

    news = _cityfalcon.get_news(ticker, days=days)
    _cache.set(cache_key, news, ttl=3600)  # Cache 1 hour
    return news

def get_sentiment(ticker: str, days=7):
    """Get aggregate sentiment summary."""
    return _cityfalcon.get_sentiment_summary(ticker, days=days)

# ========================================
# DIRECTOR DEALINGS (Tier 2: CityFALCON)
# ========================================

def get_director_dealings(ticker: str, days=30):
    """Fetch UK director dealing announcements."""
    cache_key = f"director_dealings:{ticker}:{days}"

    if cached := _cache.get(cache_key):
        return cached

    dealings = _cityfalcon.get_director_dealings(ticker, days=days)
    _cache.set(cache_key, dealings, ttl=86400)  # Cache 24 hours
    return dealings

# ========================================
# REAL-TIME QUOTES (Tier 3: IBKR)
# ========================================

def get_realtime_quote(ticker: str):
    """
    Get real-time bid/ask for execution.
    NO CACHING - must be fresh for trades.
    """
    return _ibkr.get_realtime_quote(ticker)

# ========================================
# ORDER EXECUTION (Tier 3: IBKR)
# ========================================

def place_order(ticker: str, quantity: int, action='BUY', order_type='LIMIT', limit_price=None):
    """Place order via IBKR."""
    if order_type == 'LIMIT' and limit_price:
        return _ibkr.place_limit_order(ticker, quantity, limit_price, action)
    else:
        return _ibkr.place_market_order(ticker, quantity, action)
```

---

## Agent Integration

Agents now use the unified interface:

```python
# src/agents/fundamental_screener.py

from src.data_sources.market_data import (
    get_prices,
    get_fundamentals,
    get_financial_ratios
)

def fundamental_screener_agent(state):
    ticker = state["ticker"]

    # Fetch data using unified interface
    fundamentals = get_fundamentals(ticker)
    ratios = get_financial_ratios(ticker)
    prices = get_prices(ticker, "2024-01-01", "2025-11-22")

    # Agent logic...
    if ratios['pe_ratio'] < 15 and ratios['debt_to_equity'] < 0.5:
        return {"signal": "BUY", "confidence": 85}

    return {"signal": "HOLD", "confidence": 50}
```

**Agents don't know or care which provider the data comes from!** The unified interface handles routing to EODHD, CityFALCON, or IBKR automatically.

---

## Environment Setup

**Complete `.env` file:**

```bash
# ========================================
# DATA PROVIDERS
# ========================================

# Tier 1: EODHD (Core Data)
EODHD_API_KEY=your_eodhd_api_key_here

# Tier 2: CityFALCON (Intelligence)
CITYFALCON_API_KEY=your_cityfalcon_api_key_here

# Tier 3: IBKR (Execution)
IBKR_HOST=127.0.0.1
IBKR_PORT=7497  # 7497 for paper trading, 7496 for live
IBKR_CLIENT_ID=1

# ========================================
# MARKET CONFIGURATION
# ========================================

MARKET=UK
EXCHANGE=LSE
TIMEZONE=Europe/London
MARKET_OPEN=08:00
MARKET_CLOSE=16:30
CURRENCY=GBP
```

---

## Testing

**Test script:** `test_uk_data_integration.py`

```python
from src.data_sources.market_data import (
    get_prices,
    get_fundamentals,
    get_news,
    get_director_dealings,
    get_realtime_quote
)

# Test Tier 1: EODHD
print("Testing EODHD (Tier 1)...")
prices = get_prices("VOD", "2025-01-01", "2025-11-22")
print(f"✓ Fetched {len(prices)} price records")

fundamentals = get_fundamentals("VOD")
print(f"✓ Fetched fundamentals: Market Cap = £{fundamentals['Highlights']['MarketCapitalization']:,.0f}")

# Test Tier 2: CityFALCON
print("\nTesting CityFALCON (Tier 2)...")
news = get_news("VOD", days=7)
print(f"✓ Fetched {len(news)} news articles")

dealings = get_director_dealings("VOD", days=30)
print(f"✓ Fetched {len(dealings)} director dealing announcements")

# Test Tier 3: IBKR (requires TWS/Gateway running)
print("\nTesting IBKR (Tier 3)...")
try:
    quote = get_realtime_quote("VOD")
    print(f"✓ Real-time quote: Bid=£{quote['bid']}, Ask=£{quote['ask']}")
except Exception as e:
    print(f"⚠️ IBKR not connected (TWS/Gateway must be running): {e}")

print("\n✅ All integration tests passed!")
```

---

## Migration from Old System

If migrating from the old multi-source system:

1. **Remove old API integrations:**
   - Delete `src/tools/api.py` (US-focused financialdatasets.ai)
   - Remove FMP, Alpha Vantage, yfinance code

2. **Update agent imports:**
   ```python
   # OLD
   from src.tools.api import get_prices, get_company_news

   # NEW
   from src.data_sources.market_data import get_prices, get_news
   ```

3. **Update ticker format:**
   - Agents now use base ticker: "VOD" (not "VOD.L" or "VOD.LSE")
   - Market data module handles exchange suffix internally

4. **Remove rate limit logic:**
   - No more juggling Finnhub (800/day), Alpha Vantage (25/day), FMP (250/day)
   - EODHD has 100,000 calls/day - no limits to worry about

---

## Next Steps

- **[prd.md](./prd.md)** - Full Product Requirements Document with detailed FR-5 data integration specs
- **[5-uk-adaptation-guide.md](./5-uk-adaptation-guide.md)** - Complete step-by-step implementation guide
- **[index.md](./index.md)** - Master index of all documentation
