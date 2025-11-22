# Implementation Patterns

### CRITICAL: These patterns ensure AI agent consistency across all 7 epics

### Naming Conventions

**Python Backend:**
- **Files:** `snake_case.py` (e.g., `news_scanner.py`, `signal_bus.py`)
- **Classes:** `PascalCase` (e.g., `NewsScanner`, `SignalBus`, `AgentState`)
- **Functions/Methods:** `snake_case` (e.g., `def aggregate_signals()`, `def publish_signal()`)
- **Variables:** `snake_case` (e.g., `signal_strength`, `portfolio_value`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_POSITION_SIZE`, `API_TIMEOUT`)
- **Private methods:** `_leading_underscore` (e.g., `def _validate_ticker()`)

**Database (PostgreSQL):**
- **Tables:** `snake_case` plural (e.g., `signals`, `watchlist_entries`, `portfolio_positions`)
- **Columns:** `snake_case` (e.g., `created_at`, `stock_ticker`, `signal_strength`)
- **Foreign keys:** `{table}_id` (e.g., `stock_id`, `portfolio_id`)
- **Indexes:** `idx_{table}_{columns}` (e.g., `idx_signals_stock_ticker`, `idx_trades_created_at`)

**REST API Endpoints:**
- **Pattern:** `/resource` or `/resource/{id}` (plural resources, lowercase, hyphens for multi-word)
- **Examples:**
  - `GET /api/v1/portfolio` - Get current portfolio
  - `POST /api/v1/analysis/run` - Trigger analysis
  - `GET /api/v1/watchlist/{id}` - Get watchlist entry
  - `PUT /api/v1/watchlist/{id}/triggers` - Update triggers
- **Versioning:** `/api/v1/` prefix (prepare for future v2)

**TypeScript Frontend:**
- **Components:** `PascalCase.tsx` (e.g., `DailyReport.tsx`, `PortfolioView.tsx`)
- **Interfaces/Types:** `PascalCase` (e.g., `interface Signal {}`, `type AnalysisResult`)
- **Functions:** `camelCase` (e.g., `const fetchReports = () => {}`)
- **Files (non-components):** `camelCase.ts` (e.g., `api.ts`, `formatting.ts`)

### Code Organization Patterns

**Test File Placement:**
- **Unit tests:** `tests/unit/test_{module}.py` (e.g., `tests/unit/test_signal_bus.py`)
- **Integration tests:** `tests/integration/test_{feature}.py`
- **Test files mirror source structure:** `src/agents/news_scanner.py` → `tests/unit/agents/test_news_scanner.py`

**Import Order (enforced by linters):**
```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party
from fastapi import FastAPI
from sqlalchemy import select

# 3. Local application
from src.models.signal import Signal
from src.core.signal_bus import SignalBus
```

**Component Organization (React):**
```typescript
// 1. Imports (React, libraries, local)
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchPortfolio } from '../services/api';

// 2. Type definitions
interface PortfolioViewProps {
  userId: string;
}

// 3. Component
export const PortfolioView: React.FC<PortfolioViewProps> = ({ userId }) => {
  // Hooks first
  const { data, isLoading } = useQuery(['portfolio', userId], fetchPortfolio);

  // Render
  return <div>{/* ... */}</div>;
};
```

### Format Patterns (Data Exchange)

**Date/Time Handling:**
- **Storage (DB):** UTC timestamps (`TIMESTAMP WITH TIME ZONE`)
- **API responses:** ISO 8601 strings (`"2025-11-22T07:00:00Z"`)
- **Frontend display:** Convert to UK timezone (`Europe/London`) for user
- **Market hours:** Store as UTC, compare against LSE hours (8:00-16:30 GMT/BST)

```python
from datetime import datetime, timezone

# Always use timezone-aware datetimes
now = datetime.now(timezone.utc)  # ✅ CORRECT
now = datetime.now()              # ❌ WRONG (naive datetime)

# API serialization
def serialize_datetime(dt: datetime) -> str:
    return dt.isoformat()  # "2025-11-22T07:00:00+00:00"
```

**Currency Formatting:**
- **Storage:** Decimal type (e.g., `DECIMAL(12, 2)` for GBP amounts)
- **API:** Float/number (JSON limitation)
- **Display:** `£1,234.56` (UK locale, 2 decimals)

```python
from decimal import Decimal

# Storage/calculations
price = Decimal("123.45")  # ✅ CORRECT (no float precision errors)
price = 123.45             # ❌ WRONG (float precision issues)
```

**Ticker Format:**
- **LSE tickers:** `{SYMBOL}.L` (e.g., `VOD.L`, `LLOY.L`, `BP.L`)
- **Validation regex:** `^[A-Z]{2,4}\.L$`
- **Company names:** Store separately in `stocks.name`, never use for lookups

### Error Handling Patterns

**API Error Responses (Standardized):**
```python
from fastapi import HTTPException

# Custom exception classes
class DataProviderError(Exception):
    """Raised when external API fails"""
    pass

class ValidationError(Exception):
    """Raised when input validation fails"""
    pass

# FastAPI exception handlers
@app.exception_handler(DataProviderError)
async def data_provider_error_handler(request, exc):
    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error": {
                "code": "DATA_PROVIDER_UNAVAILABLE",
                "message": str(exc),
                "details": {"provider": exc.provider_name}
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

# Graceful degradation example
async def fetch_stock_data(ticker: str) -> StockData:
    try:
        # Try primary provider (EODHD)
        return await eodhd_client.get_stock_data(ticker)
    except DataProviderError:
        logger.warning(f"EODHD unavailable for {ticker}, trying IBKR fallback")
        try:
            # Fallback to IBKR
            return await ibkr_client.get_stock_data(ticker)
        except DataProviderError:
            # Both failed - return cached data if available
            cached = cache.get(f"stock:{ticker}")
            if cached:
                logger.info(f"Using cached data for {ticker}")
                return cached
            # No cache - raise error
            raise DataProviderError(f"All providers failed for {ticker}")
```

**Retry Logic (with exponential backoff):**
```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def fetch_with_retry(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return response.json()
```

### Logging Strategy

**Structured Logging (JSON format for production):**
```python
import logging
import json
from datetime import datetime, timezone

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(handler)

    def info(self, message: str, **kwargs):
        self.logger.info(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": "INFO",
            "message": message,
            **kwargs
        }))

# Usage in agents
logger = StructuredLogger("news_scanner")
logger.info("Catalyst detected", ticker="VOD.L", catalyst_type="major_contract", strength=15)

# Output:
# {"timestamp": "2025-11-22T02:15:00Z", "level": "INFO", "message": "Catalyst detected", "ticker": "VOD.L", "catalyst_type": "major_contract", "strength": 15}
```

**Log Levels:**
- **DEBUG:** Detailed agent reasoning, signal details (development only)
- **INFO:** Agent actions, signals published, analysis started/completed
- **WARNING:** Fallback data source used, API quota approaching, missing data
- **ERROR:** API failures, validation errors, unexpected exceptions
- **CRITICAL:** System failures, database connection lost, scheduler crash

### Consistency Patterns (Cross-Cutting)

**Signal Schema (ALL agents must use):**
```python
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class Signal(BaseModel):
    type: str               # e.g., "NEW_CATALYST", "INSIDER_CONVICTION"
    stock_ticker: str       # e.g., "VOD.L"
    strength: int           # 0-100 (base score before multipliers)
    data: dict              # Agent-specific details
    timestamp: datetime     # UTC timezone-aware
    agent_id: str           # e.g., "news_scanner", "macro_economist"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
```

**Analysis Result Schema (ALL analysis agents must use):**
```python
class AnalysisResult(BaseModel):
    agent_id: str           # e.g., "value_investor", "contrarian"
    stock_ticker: str
    recommendation: str     # "BUY" | "SELL" | "HOLD" | "WATCHLIST"
    score: int              # 0-100 conviction
    confidence: str         # "LOW" | "MEDIUM" | "HIGH"
    reasoning: str          # Human-readable explanation
    key_metrics: dict       # Agent-specific metrics
    risks: list[str]        # Identified risks
    timestamp: datetime     # UTC
```

**Environment Variables (consistent naming):**
```bash
# .env format (all UPPER_SNAKE_CASE)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/aihedgefund
EODHD_API_KEY=your_key_here
CITYFALCON_API_KEY=your_key_here
IBKR_API_KEY=your_key_here

OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# LLM provider preference (comma-separated, fallback order)
LLM_PROVIDERS=openai,anthropic,google

# Batch processing schedule (cron format)
BATCH_SCHEDULE="0 1 * * 1-5"  # 1 AM Mon-Fri

# Email notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
NOTIFICATION_EMAIL=your_email@gmail.com

# Cost controls
MAX_DAILY_LLM_COST=50.00  # GBP
MAX_STOCKS_PER_RUN=15
```

---
