# AIHedgeFund - Implementation Architecture

**Version:** 1.0
**Date:** 2025-11-22
**Author:** BMad Master (for Longy)
**Status:** Production Ready

---

## Executive Summary

This document defines the complete technical implementation architecture for AIHedgeFund, a 20-agent autonomous UK stock trading system. This architecture serves as the **consistency contract** for all AI development agents—ensuring every agent builds compatible, cohesive code across all 7 MVP epics.

**Core Innovation:** Networked multi-agent architecture with signal convergence, three-tier tracking system, and adversarial challenge protocol delivering institutional-grade analysis at 99.5% cost reduction.

**Technology Foundation:** Python 3.14 + FastAPI 0.121.3 + LangGraph 1.0.5 + React 19 + PostgreSQL 18.1 (all Nov 2025 production versions)

---

## Project Initialization

### First Implementation Story: Initialize Project

```bash
# Backend initialization
mkdir -p ai-hedge-fund && cd ai-hedge-fund
python3.14 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install core dependencies
pip install --upgrade pip
pip install "fastapi[standard]==0.121.3" \
            "langgraph==1.0.5" \
            "langchain==1.0" \
            "langchain-openai" \
            "langchain-anthropic" \
            "langchain-google-genai" \
            "psycopg2-binary" \
            "sqlalchemy" \
            "alembic" \
            "pydantic==2.x" \
            "python-dotenv" \
            "httpx" \
            "schedule" \
            "pytest" \
            "pytest-asyncio"

# Frontend initialization
cd app/frontend
npm create vite@latest . -- --template react-ts
npm install react@19 react-dom@19 @types/react@19 @types/react-dom@19
npm install axios react-router-dom @tanstack/react-query recharts lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

This establishes the base architecture with all decisions below pre-configured.

---

## Decision Summary

| Category | Decision | Version | Affects Epics | Rationale |
|----------|----------|---------|---------------|-----------|
| **Language** | Python | 3.14 (stable Oct 2025) | All | Latest stable, free-threaded mode, JIT compiler, LangGraph 1.0 requires 3.10+ |
| **Backend Framework** | FastAPI | 0.121.3 (Nov 19, 2025) | E1, E5, E6 | Production-ready async, auto OpenAPI docs, excellent performance |
| **Agent Orchestration** | LangGraph | 1.0.5 (Nov 20, 2025) | E2, E3 | Stable 1.0 release, durable state, human-in-loop, no breaking changes until 2.0 |
| **LLM Framework** | LangChain | 1.0 (Oct 2025) | E2, E3 | Multi-provider abstraction (OpenAI, Anthropic, Google), stable 1.0 |
| **Database** | PostgreSQL | 18.1 (Nov 13, 2025) | E1, E4, E6 | 3× I/O performance gains, uuidv7() support, production proven |
| **ORM** | SQLAlchemy | 2.x latest | E1, E4 | Async support, type safety, migration tooling (Alembic) |
| **Frontend Framework** | React | 19 (Dec 2024) | E5 | Latest stable, compiler improvements, concurrent features |
| **Frontend Language** | TypeScript | 5.x latest | E5 | Type safety prevents runtime errors in production |
| **Build Tool** | Vite | 6.x latest | E5 | Fastest HMR, optimized production builds, Node 20.19+ support |
| **API Client** | httpx (Python) | latest | E1, E2 | Async HTTP client, connection pooling, retry logic |
| **Scheduler** | schedule (Python) | latest | E6 | Simple cron-like scheduling for overnight batch processing |
| **Testing** | pytest + pytest-asyncio | latest | All | Async test support, fixtures, comprehensive ecosystem |
| **Data Validation** | Pydantic | 2.x latest | All | FastAPI native, runtime validation, serialization |
| **State Management (FE)** | TanStack Query | latest | E5 | Server state caching, optimistic updates, error handling |
| **LLM Providers** | OpenAI, Anthropic, Google | Multi-provider | E2, E3 | Fallback support, cost optimization, avoid vendor lock-in |
| **Data APIs** | EODHD, CityFALCON, IBKR | - | E1, E2 | 3-tier: fundamentals + intelligence + execution |

**Starter Template:** None - Manual setup required for specialized multi-agent trading architecture

---

## Project Structure

```
AIHedgeFund/
├── .env                           # API keys, secrets (NEVER commit)
├── .env.example                   # Template for environment variables
├── .gitignore                     # Exclude venv, __pycache__, .env, db files
├── README.md                      # Setup instructions, architecture overview
├── requirements.txt               # Python dependencies (pinned versions)
├── pytest.ini                     # Test configuration
├── alembic.ini                    # Database migration config
├── docker-compose.yml             # PostgreSQL + app containerization
│
├── src/                           # Backend Python source (Epic 1-6)
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point, lifespan startup
│   ├── config.py                  # Settings (Pydantic BaseSettings from .env)
│   │
│   ├── agents/                    # EPIC 2, 3: Agent implementations
│   │   ├── __init__.py
│   │   ├── base.py                # Base Agent class with signal broadcast/listen
│   │   │
│   │   ├── discovery/             # EPIC 2: Discovery Layer (7 agents)
│   │   │   ├── __init__.py
│   │   │   ├── news_scanner.py         # News Scanner Agent
│   │   │   ├── insider_trading.py      # Insider Trading Agent
│   │   │   ├── volume_price.py         # Volume & Price Action Agent
│   │   │   ├── fundamental_screener.py # Fundamental Screener Agent
│   │   │   ├── earnings_surprise.py    # Earnings Surprise Agent (Phase 2)
│   │   │   ├── analyst_activity.py     # Analyst Activity Agent (Phase 2)
│   │   │   └── corporate_actions.py    # Corporate Actions Agent (Phase 2)
│   │   │
│   │   ├── macro_sector/          # EPIC 2: Macro/Sector Context (2-3 agents)
│   │   │   ├── __init__.py
│   │   │   ├── macro_economist.py      # Macro Economist Agent (weekly)
│   │   │   ├── sector_rotation.py      # Sector Rotation Agent (weekly)
│   │   │   └── industry_specialist.py  # Industry Specialists (Phase 2)
│   │   │
│   │   ├── analysis/              # EPIC 3: Analysis Layer (8 agents)
│   │   │   ├── __init__.py
│   │   │   ├── value_investor.py       # Value Investor (Buffett/Graham)
│   │   │   ├── growth_investor.py      # Growth Investor (Lynch)
│   │   │   ├── contrarian.py           # Contrarian Agent (Burry)
│   │   │   ├── naked_trader.py         # Naked Trader (Robbie Burns)
│   │   │   ├── quality_moat.py         # Quality/Moat Agent
│   │   │   ├── technical_analyst.py    # Technical Analyst
│   │   │   ├── catalyst_detective.py   # Catalyst Detective
│   │   │   └── sentiment_analyst.py    # Sentiment Analyst
│   │   │
│   │   └── decision/              # EPIC 3: Decision Layer (2 agents)
│   │       ├── __init__.py
│   │       ├── risk_manager.py         # Risk Manager (adversarial challenger)
│   │       └── portfolio_manager.py    # Portfolio Manager (final decisions)
│   │
│   ├── graph/                     # EPIC 3: LangGraph orchestration
│   │   ├── __init__.py
│   │   ├── state.py               # AgentState definition, message history
│   │   ├── workflow.py            # LangGraph StateGraph definition
│   │   ├── nodes.py               # Node implementations (discovery, analysis, decision)
│   │   └── edges.py               # Conditional routing logic
│   │
│   ├── data/                      # EPIC 1: Data integration layer
│   │   ├── __init__.py
│   │   ├── providers/             # API client abstractions
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Abstract base data provider interface
│   │   │   ├── eodhd.py           # EODHD API client (fundamentals, macro)
│   │   │   ├── cityfalcon.py      # CityFALCON API client (RNS, insider, sentiment)
│   │   │   ├── ibkr.py            # IBKR API client (real-time quotes)
│   │   │   └── file_drop.py       # Manual CSV/JSON research inbox
│   │   ├── cache.py               # Caching layer (Redis or in-memory for MVP)
│   │   ├── validator.py           # Data quality checks, outlier detection
│   │   └── mapper.py              # UK company name → LSE ticker mapping
│   │
│   ├── models/                    # EPIC 1, 4: SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py                # Base model with common fields (id, created_at, updated_at)
│   │   ├── signal.py              # Signal model (discovery agent outputs)
│   │   ├── stock.py               # Stock master data (ticker, name, sector)
│   │   ├── analysis.py            # Analysis results (agent assessments)
│   │   ├── portfolio.py           # Tier 1: Active Portfolio positions
│   │   ├── watchlist.py           # Tier 2: Active Watchlist with triggers
│   │   ├── research_queue.py      # Tier 3: Research Queue
│   │   ├── trade.py               # Trade execution records, P&L
│   │   └── audit_log.py           # Full audit trail (decisions, data sources)
│   │
│   ├── schemas/                   # EPIC 1, 5: Pydantic schemas (API contracts)
│   │   ├── __init__.py
│   │   ├── signal.py              # Signal schema (type, stock, data, timestamp)
│   │   ├── analysis.py            # Analysis schema (agent output format)
│   │   ├── recommendation.py      # BUY/SELL/HOLD recommendation format
│   │   ├── portfolio.py           # Portfolio position schema
│   │   ├── watchlist.py           # Watchlist entry schema
│   │   └── report.py              # Daily report schema
│   │
│   ├── services/                  # EPIC 2-6: Business logic services
│   │   ├── __init__.py
│   │   ├── discovery_service.py   # Orchestrates discovery agents
│   │   ├── analysis_service.py    # Orchestrates analysis agents
│   │   ├── signal_aggregator.py   # Signal convergence scoring logic
│   │   ├── watchlist_service.py   # Watchlist trigger monitoring, re-validation
│   │   ├── portfolio_service.py   # Portfolio tracking, P&L calculations
│   │   ├── report_generator.py    # Daily report generation
│   │   └── trade_service.py       # Trade execution, logging
│   │
│   ├── core/                      # EPIC 6: Signal bus, cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── signal_bus.py          # Central message bus (publish/subscribe)
│   │   ├── logging.py             # Structured logging configuration
│   │   ├── errors.py              # Custom exceptions, error handlers
│   │   ├── security.py            # API key validation, auth (future)
│   │   └── monitoring.py          # Cost tracking, performance metrics
│   │
│   ├── automation/                # EPIC 6: Scheduling and automation
│   │   ├── __init__.py
│   │   ├── scheduler.py           # Overnight batch processing (schedule library)
│   │   ├── tasks.py               # Task definitions (discovery, analysis, watchlist)
│   │   └── notifications.py       # Email/SMS delivery (SMTP, future: Twilio)
│   │
│   ├── api/                       # EPIC 5: FastAPI routes
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py        # POST /analysis/run, GET /analysis/{id}
│   │   │   ├── portfolio.py       # GET /portfolio, POST /portfolio/positions
│   │   │   ├── watchlist.py       # GET /watchlist, POST /watchlist, PUT /watchlist/{id}
│   │   │   ├── reports.py         # GET /reports/daily, GET /reports/{date}
│   │   │   ├── trades.py          # POST /trades, GET /trades/history
│   │   │   └── health.py          # GET /health (monitoring endpoint)
│   │   └── dependencies.py        # FastAPI dependencies (DB session, auth)
│   │
│   ├── db/                        # EPIC 1: Database utilities
│   │   ├── __init__.py
│   │   ├── session.py             # Async DB session factory
│   │   └── migrations/            # Alembic migration scripts
│   │       └── versions/
│   │
│   └── utils/                     # Shared utilities
│       ├── __init__.py
│       ├── date_utils.py          # UK market hours, timezone handling
│       ├── formatting.py          # Currency, percentage formatting
│       └── validators.py          # Ticker validation, data quality checks
│
├── app/                           # Frontend application (EPIC 5)
│   └── frontend/
│       ├── package.json
│       ├── tsconfig.json
│       ├── vite.config.ts
│       ├── index.html
│       ├── public/
│       │   └── assets/
│       └── src/
│           ├── main.tsx           # React 19 entry point
│           ├── App.tsx            # Root component, routing
│           ├── vite-env.d.ts
│           │
│           ├── components/        # Reusable UI components
│           │   ├── DailyReport.tsx        # Morning report display
│           │   ├── PortfolioView.tsx      # Tier 1: Holdings + P&L
│           │   ├── WatchlistView.tsx      # Tier 2: Watchlist management
│           │   ├── RecommendationCard.tsx # BUY/SELL/HOLD cards
│           │   ├── AgentInsights.tsx      # Agent analysis breakdown
│           │   └── TradeApprovalModal.tsx # Manual trade approval UI
│           │
│           ├── pages/             # Route pages
│           │   ├── Dashboard.tsx          # Main dashboard
│           │   ├── Analysis.tsx           # On-demand analysis page
│           │   ├── Reports.tsx            # Historical reports
│           │   └── Settings.tsx           # Agent config, scheduling
│           │
│           ├── services/          # API client
│           │   ├── api.ts         # Axios instance, interceptors
│           │   └── queries.ts     # TanStack Query hooks
│           │
│           ├── types/             # TypeScript type definitions
│           │   ├── signal.ts
│           │   ├── analysis.ts
│           │   └── portfolio.ts
│           │
│           └── utils/
│               ├── formatting.ts  # Currency, date formatting
│               └── constants.ts   # API URLs, config
│
├── tests/                         # Test suite (all epics)
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures (DB, mocks)
│   ├── unit/                      # Unit tests for agents, services
│   │   ├── test_agents/
│   │   ├── test_services/
│   │   └── test_signal_bus.py
│   ├── integration/               # API integration tests
│   │   ├── test_api_routes.py
│   │   └── test_workflow.py
│   └── e2e/                       # End-to-end workflow tests
│       └── test_daily_run.py
│
├── docs/                          # Documentation (existing + new)
│   ├── index.md
│   ├── prd.md
│   ├── epics.md
│   ├── architecture.md            # THIS DOCUMENT
│   ├── agent-network-architecture.md  # Conceptual design
│   ├── api-spec.yaml              # OpenAPI spec (auto-generated)
│   └── deployment.md              # Deployment guide
│
└── scripts/                       # Operational scripts
    ├── init_db.py                 # Database initialization
    ├── seed_data.py               # Load UK ticker mapping, test data
    ├── run_discovery.py           # Manual discovery run
    └── backtest.py                # Historical backtesting script
```

---

## Epic to Architecture Mapping

| Epic | Primary Components | Key Files |
|------|-------------------|-----------|
| **Epic 1: Foundation & Data Architecture** | `src/data/`, `src/models/`, `src/db/`, `src/core/` | `data/providers/eodhd.py`, `models/signal.py`, `core/signal_bus.py` |
| **Epic 2: Discovery & Market Intelligence** | `src/agents/discovery/`, `src/agents/macro_sector/`, `src/services/discovery_service.py` | `agents/discovery/news_scanner.py`, `agents/macro_sector/macro_economist.py`, `services/signal_aggregator.py` |
| **Epic 3: Analysis Engine** | `src/agents/analysis/`, `src/agents/decision/`, `src/graph/` | `agents/analysis/value_investor.py`, `agents/decision/risk_manager.py`, `graph/workflow.py` |
| **Epic 4: Portfolio & Tracking** | `src/models/portfolio.py`, `src/models/watchlist.py`, `src/services/portfolio_service.py` | `models/portfolio.py`, `models/watchlist.py`, `services/watchlist_service.py` |
| **Epic 5: Reporting & Execution** | `app/frontend/`, `src/api/routes/`, `src/services/report_generator.py` | `api/routes/reports.py`, `services/report_generator.py`, `frontend/src/components/DailyReport.tsx` |
| **Epic 6: Automation & Reliability** | `src/automation/`, `src/core/monitoring.py` | `automation/scheduler.py`, `automation/tasks.py`, `core/monitoring.py` |
| **Epic 7: Configurability & Enhancement** | `src/api/routes/`, agent plugin system | `agents/base.py` (plugin interface), API routes for agent enable/disable |

---

## Technology Stack Details

### Core Technologies

**Backend Stack:**
- **Python 3.14** - Latest stable (Oct 2025), free-threaded mode, JIT compiler for performance
- **FastAPI 0.121.3** - Async web framework, auto OpenAPI docs, Pydantic integration
- **LangGraph 1.0.5** - Durable agent orchestration, no breaking changes until 2.0
- **LangChain 1.0** - Multi-provider LLM abstraction (OpenAI, Anthropic, Google)
- **PostgreSQL 18.1** - 3× I/O performance gains, uuidv7() for efficient indexing
- **SQLAlchemy 2.x** - Async ORM, type hints, Alembic migrations
- **Pydantic 2.x** - Runtime validation, serialization (FastAPI native)

**Frontend Stack:**
- **React 19** - Latest stable, compiler improvements, concurrent rendering
- **TypeScript 5.x** - Type safety, IntelliSense, catch errors at compile-time
- **Vite 6** - Fastest dev server (HMR), optimized production builds
- **TanStack Query** - Server state management, caching, optimistic updates
- **TailwindCSS** - Utility-first styling (optional, recommended for rapid UI dev)

**Data & Integration:**
- **httpx** - Async HTTP client for API calls (connection pooling, retries)
- **schedule** - Python job scheduling for overnight batch processing
- **EODHD API** - Fundamentals, historical data, earnings, macro indicators
- **CityFALCON API** - UK RNS feeds, director dealings, sentiment
- **IBKR API** - Real-time quotes at point of trade execution

### Integration Points

**LangGraph Agent Network:**
```python
# StateGraph with parallel discovery, sequential decision
from langgraph.graph import StateGraph
from src.graph.state import AgentState

workflow = StateGraph(AgentState)

# Discovery Layer (parallel)
workflow.add_node("news_scanner", news_scanner_node)
workflow.add_node("insider_trading", insider_trading_node)
workflow.add_node("volume_price", volume_price_node)
workflow.add_node("fundamental_screener", fundamental_screener_node)

# Macro/Sector Context (parallel)
workflow.add_node("macro_economist", macro_economist_node)
workflow.add_node("sector_rotation", sector_rotation_node)

# Signal Aggregation (sequential after discovery)
workflow.add_node("aggregate_signals", signal_aggregation_node)

# Analysis Layer (parallel, only for high-scoring stocks)
workflow.add_node("value_investor", value_investor_node)
workflow.add_node("growth_investor", growth_investor_node)
# ... 6 more analysis agents

# Decision Layer (sequential)
workflow.add_node("risk_manager", risk_manager_node)
workflow.add_node("portfolio_manager", portfolio_manager_node)

# Edges (parallel fan-out, conditional routing)
workflow.add_edge("start", ["news_scanner", "insider_trading", "volume_price", "fundamental_screener"])
workflow.add_conditional_edges("aggregate_signals", route_to_analysis)  # Only if score > 60
workflow.add_edge("portfolio_manager", "end")
```

**Signal Bus Architecture:**
```python
# Central message bus for agent communication
class SignalBus:
    _subscribers: Dict[str, List[Callable]] = {}

    @classmethod
    def publish(cls, signal: Signal):
        """Broadcast signal to all subscribers"""
        signal_type = signal.type
        for callback in cls._subscribers.get(signal_type, []):
            callback(signal)

    @classmethod
    def subscribe(cls, signal_types: List[str], callback: Callable):
        """Register listener for specific signal types"""
        for signal_type in signal_types:
            cls._subscribers.setdefault(signal_type, []).append(callback)

# Agent usage
class NewsScanner(BaseAgent):
    def analyze(self, data):
        # Perform news analysis
        catalyst = detect_catalyst(data)

        # Broadcast discovery
        SignalBus.publish(Signal(
            type="NEW_CATALYST",
            stock="VOD.L",
            data=catalyst,
            strength=15,
            timestamp=datetime.now(UTC)
        ))
```

**API Response Structure (Standardized):**
```typescript
// Success response
{
  "success": true,
  "data": { ... },
  "timestamp": "2025-11-22T07:00:00Z"
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid ticker format",
    "details": { "ticker": "Must match pattern: [A-Z]{2,4}\\.L" }
  },
  "timestamp": "2025-11-22T07:00:05Z"
}
```

---

## Implementation Patterns

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

## Data Architecture

### Database Schema (PostgreSQL 18.1)

**Core Tables:**

```sql
-- Stocks master table
CREATE TABLE stocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) UNIQUE NOT NULL,  -- e.g., 'VOD.L'
    name VARCHAR(255) NOT NULL,           -- e.g., 'Vodafone Group PLC'
    sector VARCHAR(100),                  -- e.g., 'Telecommunications'
    market_cap DECIMAL(15, 2),            -- GBP millions
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_stocks_ticker ON stocks(ticker);
CREATE INDEX idx_stocks_sector ON stocks(sector);

-- Signals from discovery agents
CREATE TABLE signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL,            -- 'NEW_CATALYST', 'INSIDER_CONVICTION', etc.
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    strength INTEGER NOT NULL,            -- 0-100 base score
    data JSONB NOT NULL,                  -- Agent-specific details
    agent_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_signals_stock_ticker ON signals(stock_ticker);
CREATE INDEX idx_signals_timestamp ON signals(timestamp DESC);
CREATE INDEX idx_signals_agent_id ON signals(agent_id);

-- Analysis results from analysis agents
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    agent_id VARCHAR(50) NOT NULL,        -- 'value_investor', 'contrarian', etc.
    recommendation VARCHAR(20) NOT NULL,  -- 'BUY', 'SELL', 'HOLD', 'WATCHLIST'
    score INTEGER NOT NULL,               -- 0-100 conviction
    confidence VARCHAR(10) NOT NULL,      -- 'LOW', 'MEDIUM', 'HIGH'
    reasoning TEXT NOT NULL,
    key_metrics JSONB,
    risks JSONB,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_analysis_stock_ticker ON analysis_results(stock_ticker);
CREATE INDEX idx_analysis_timestamp ON analysis_results(timestamp DESC);

-- Tier 1: Active Portfolio
CREATE TABLE portfolio_positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    entry_price DECIMAL(10, 2) NOT NULL,  -- GBP
    entry_date DATE NOT NULL,
    stop_loss DECIMAL(10, 2),             -- GBP
    target_price DECIMAL(10, 2),          -- GBP
    current_price DECIMAL(10, 2),         -- Updated daily
    unrealized_pnl DECIMAL(12, 2),        -- Updated daily
    status VARCHAR(20) DEFAULT 'ACTIVE',  -- 'ACTIVE', 'CLOSED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_portfolio_status ON portfolio_positions(status);

-- Tier 2: Active Watchlist
CREATE TABLE watchlist_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    reason TEXT NOT NULL,                 -- Why added to watchlist
    triggers JSONB NOT NULL,              -- Array of trigger conditions
    added_date DATE NOT NULL,
    last_validated TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'ACTIVE',  -- 'ACTIVE', 'TRIGGERED', 'REMOVED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_watchlist_status ON watchlist_entries(status);

-- Tier 3: Research Queue
CREATE TABLE research_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    convergence_score INTEGER NOT NULL,   -- 31-60 range (below analysis threshold)
    signals JSONB NOT NULL,               -- Array of contributing signals
    added_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING', -- 'PENDING', 'PROMOTED', 'DISCARDED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_research_score ON research_queue(convergence_score DESC);

-- Trades (execution log)
CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    action VARCHAR(10) NOT NULL,          -- 'BUY', 'SELL'
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,        -- GBP
    commission DECIMAL(8, 2),             -- GBP
    trade_date TIMESTAMP WITH TIME ZONE NOT NULL,
    realized_pnl DECIMAL(12, 2),          -- For SELL trades
    notes TEXT,                           -- User notes, lessons learned
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_trades_ticker ON trades(stock_ticker);
CREATE INDEX idx_trades_date ON trades(trade_date DESC);

-- Audit log (full traceability)
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,      -- 'ANALYSIS_RUN', 'SIGNAL_PUBLISHED', 'TRADE_EXECUTED'
    entity_id UUID,                       -- ID of related entity (stock, trade, etc.)
    entity_type VARCHAR(50),              -- 'STOCK', 'TRADE', 'SIGNAL'
    details JSONB NOT NULL,               -- Event-specific details
    user_id UUID,                         -- If user-initiated (future multi-user)
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp DESC);
CREATE INDEX idx_audit_event_type ON audit_log(event_type);
```

### Data Flow

**Overnight Batch Processing (1am-7am):**

```
1:00 AM  → Data Collection
            ├─ EODHD: Pull fundamentals, historical, earnings
            ├─ CityFALCON: Pull RNS feeds, insider dealings
            ├─ IBKR: Update watchlist prices
            └─ Store in signals table

2:00 AM  → Discovery Layer (7 agents run in parallel)
            ├─ News Scanner → NEW_CATALYST signals
            ├─ Insider Trading → INSIDER_CONVICTION signals
            ├─ Volume/Price → UNUSUAL_ACTIVITY signals
            ├─ Fundamental Screener → FUNDAMENTAL_MATCH signals
            └─ Signals published to signal_bus

3:00 AM  → Macro/Sector Context (2 agents, weekly)
            ├─ Macro Economist → MACRO_REGIME_CHANGE signal
            ├─ Sector Rotation → SECTOR_PREFERENCES_UPDATE signal
            └─ Apply sector multipliers to discovery signals

3:30 AM  → Signal Aggregation & Convergence Scoring
            ├─ Group signals by stock ticker
            ├─ Calculate convergence scores (base + multipliers)
            ├─ Route stocks:
            │   ├─ 0-30 points → Monitor (log only)
            │   ├─ 31-60 points → Research Queue (Tier 3)
            │   └─ 61+ points → Deep Analysis (trigger analysis agents)

4:00 AM  → Deep Analysis (8 agents run in parallel, only on 61+ stocks)
            ├─ Value Investor → VALUE_ASSESSMENT
            ├─ Growth Investor → GROWTH_ASSESSMENT
            ├─ Contrarian → CONTRARIAN_OPPORTUNITY/WARNING
            ├─ Quality/Moat → QUALITY_ASSESSMENT
            ├─ Technical Analyst → TECHNICAL_CONFIRMATION/WARNING
            ├─ Catalyst Detective → CATALYST_IDENTIFIED
            ├─ Sentiment Analyst → SENTIMENT_ASSESSMENT
            └─ Results stored in analysis_results table

5:00 AM  → Adversarial Challenge Protocol
            ├─ Risk Manager challenges bullish theses
            ├─ Contrarian Agent provides bear case
            ├─ Portfolio Manager synthesizes all inputs
            └─ Final BUY/SELL/HOLD/WATCHLIST decisions

5:30 AM  → Watchlist Processing
            ├─ Check all watchlist triggers (price, events, macro)
            ├─ Re-validate triggered stocks (run full analysis)
            └─ Update watchlist_entries status

6:00 AM  → Portfolio Review
            ├─ Check stop-losses (current_price vs stop_loss)
            ├─ Check target prices (current_price vs target_price)
            ├─ Re-analyze holdings for fundamental deterioration
            └─ Generate SELL recommendations if needed

6:30 AM  → Report Generation
            ├─ Compile BUY recommendations (from deep analysis)
            ├─ Compile watchlist alerts (triggered + re-validated)
            ├─ Compile portfolio updates (SELL signals, P&L)
            ├─ Aggregate macro/sector context
            └─ Store in reports table

7:00 AM  → Report Delivery
            ├─ Send email notification to user
            └─ Update web dashboard (React frontend pulls via API)
```

---

## API Contracts

### Core API Endpoints

**Base URL:** `http://localhost:8000/api/v1`

**Authentication:** None for MVP (future: JWT tokens in `Authorization: Bearer {token}` header)

#### Analysis Endpoints

```yaml
POST /analysis/run
Description: Trigger on-demand analysis for specific stocks
Request Body:
  {
    "tickers": ["VOD.L", "BP.L"],    # Array of LSE tickers
    "agents": ["all"] | ["value_investor", "technical_analyst"],  # Optional: specific agents
    "priority": "normal" | "high"     # Optional: queue priority
  }
Response (202 Accepted):
  {
    "success": true,
    "data": {
      "job_id": "uuid-here",
      "status": "queued",
      "estimated_completion": "2025-11-22T07:15:00Z"
    },
    "timestamp": "2025-11-22T07:00:00Z"
  }

GET /analysis/{job_id}
Description: Get analysis job status and results
Response (200 OK):
  {
    "success": true,
    "data": {
      "job_id": "uuid-here",
      "status": "completed",  # "queued" | "running" | "completed" | "failed"
      "results": [
        {
          "stock_ticker": "VOD.L",
          "recommendation": "BUY",
          "convergence_score": 75,
          "agent_results": [
            {
              "agent_id": "value_investor",
              "score": 85,
              "confidence": "HIGH",
              "reasoning": "Trading at 0.6× book value with strong FCF..."
            }
          ]
        }
      ],
      "completed_at": "2025-11-22T07:10:00Z"
    },
    "timestamp": "2025-11-22T07:10:05Z"
  }
```

#### Portfolio Endpoints

```yaml
GET /portfolio
Description: Get current portfolio positions (Tier 1)
Response (200 OK):
  {
    "success": true,
    "data": {
      "positions": [
        {
          "id": "uuid",
          "stock_ticker": "VOD.L",
          "stock_name": "Vodafone Group PLC",
          "quantity": 1000,
          "entry_price": 0.85,
          "current_price": 0.92,
          "unrealized_pnl": 70.00,
          "unrealized_pnl_pct": 8.24,
          "stop_loss": 0.75,
          "target_price": 1.10,
          "entry_date": "2025-11-10"
        }
      ],
      "total_value": 15420.00,
      "total_pnl": 1240.00,
      "total_pnl_pct": 8.74
    },
    "timestamp": "2025-11-22T07:00:00Z"
  }

POST /portfolio/positions
Description: Add new position (after trade execution)
Request Body:
  {
    "stock_ticker": "BP.L",
    "quantity": 500,
    "entry_price": 4.50,
    "stop_loss": 4.00,
    "target_price": 5.50
  }
Response (201 Created):
  {
    "success": true,
    "data": {
      "id": "uuid",
      "stock_ticker": "BP.L",
      ...
    }
  }
```

#### Watchlist Endpoints

```yaml
GET /watchlist
Description: Get active watchlist (Tier 2)
Response (200 OK):
  {
    "success": true,
    "data": {
      "entries": [
        {
          "id": "uuid",
          "stock_ticker": "LLOY.L",
          "stock_name": "Lloyds Banking Group",
          "reason": "Good value but waiting for sector rotation to favor financials",
          "triggers": [
            {"type": "sector", "condition": "sector_favored"},
            {"type": "price", "condition": "<=", "value": 0.50}
          ],
          "current_price": 0.55,
          "added_date": "2025-11-15",
          "status": "ACTIVE"
        }
      ]
    }
  }

POST /watchlist
Description: Add stock to watchlist
Request Body:
  {
    "stock_ticker": "HSBC.L",
    "reason": "Strong fundamentals but needs macro tailwind",
    "triggers": [
      {"type": "macro", "condition": "regime_change", "value": "expansion"},
      {"type": "price", "condition": "<=", "value": 6.00}
    ]
  }
Response (201 Created): { ... }

PUT /watchlist/{id}/triggers
Description: Update watchlist triggers
Request Body:
  {
    "triggers": [
      {"type": "price", "condition": "<=", "value": 5.50}
    ]
  }
Response (200 OK): { ... }

DELETE /watchlist/{id}
Description: Remove from watchlist
Response (204 No Content)
```

#### Report Endpoints

```yaml
GET /reports/daily
Description: Get latest daily report
Response (200 OK):
  {
    "success": true,
    "data": {
      "report_date": "2025-11-22",
      "generated_at": "2025-11-22T06:30:00Z",
      "sections": {
        "new_opportunities": [
          {
            "stock_ticker": "VOD.L",
            "stock_name": "Vodafone Group PLC",
            "recommendation": "BUY",
            "convergence_score": 75,
            "target_price": 1.10,
            "stop_loss": 0.75,
            "position_size_pct": 5,
            "bull_case": "Trading at deep discount, new contract wins...",
            "bear_case": "High debt, competitive pressure...",
            "signals": ["NEW_CATALYST", "INSIDER_CONVICTION", "VALUE_ASSESSMENT"]
          }
        ],
        "watchlist_alerts": [
          {
            "stock_ticker": "BP.L",
            "trigger_type": "price",
            "revalidation_result": "BUY",
            "reason": "Hit target price of £4.50, fundamentals still strong"
          }
        ],
        "portfolio_updates": [
          {
            "stock_ticker": "LLOY.L",
            "action": "SELL",
            "reason": "Hit target price, take profits"
          }
        ],
        "market_context": {
          "macro_regime": "expansion",
          "favored_sectors": ["Technology", "Industrials"],
          "disfavored_sectors": ["Utilities", "REITs"]
        }
      }
    }
  }

GET /reports/{date}
Description: Get historical report by date (YYYY-MM-DD)
Response (200 OK): { ... }
```

#### Trade Endpoints

```yaml
POST /trades
Description: Log executed trade
Request Body:
  {
    "stock_ticker": "VOD.L",
    "action": "BUY",
    "quantity": 1000,
    "price": 0.85,
    "commission": 9.99,
    "notes": "Morning report recommendation, strong value setup"
  }
Response (201 Created): { ... }

GET /trades/history
Description: Get trade history with P&L
Query Params: ?start_date=2025-11-01&end_date=2025-11-22
Response (200 OK):
  {
    "success": true,
    "data": {
      "trades": [ ... ],
      "summary": {
        "total_trades": 15,
        "winning_trades": 9,
        "losing_trades": 6,
        "win_rate": 60.0,
        "total_pnl": 1240.00,
        "avg_winner": 182.50,
        "avg_loser": -45.20
      }
    }
  }
```

---

## Security Architecture

**MVP Security (Phase 1):**
- ✅ Environment variable-based secrets (`.env` file, never committed)
- ✅ HTTPS in production (Cloudflare/nginx reverse proxy)
- ✅ CORS configuration (restrict frontend origin)
- ✅ Input validation (Pydantic schemas on all API endpoints)
- ❌ Authentication: None (single-user local deployment)
- ❌ Rate limiting: None (trusted local environment)

**Phase 2 Security (Multi-User):**
- JWT token-based authentication
- Role-based access control (admin, trader, viewer)
- API rate limiting (per-user quotas)
- Audit logging for all trades and config changes
- Encrypted database fields (API keys, trade credentials)

**Data Protection:**
- Database backups (daily automated exports)
- API key rotation (manual for MVP, automated in Phase 2)
- No sensitive data in logs (mask API keys, trade amounts)

---

## Performance Considerations

**Cost Optimization:**
- ✅ Batch processing overnight (GPT-4o batch API = 50% discount vs. real-time)
- ✅ Signal convergence filtering (only deep-analyze 61+ score stocks = 10-15/day vs. 600+)
- ✅ Agent enable/disable (turn off expensive agents during testing)
- ✅ Data caching (24-hour cache for fundamentals, reducing API calls)
- ✅ LLM provider fallback (use cheapest available provider)

**Performance Targets:**
- Discovery layer: < 30 min for full FTSE scan (7 agents × 600 stocks)
- Deep analysis: < 15 min for 15 stocks (8 agents × 15 stocks in parallel)
- API response time: < 200ms for portfolio/watchlist endpoints
- Report generation: < 2 min (compile all sections)
- Total overnight batch: < 6 hours (1am-7am window)

**Scalability:**
- PostgreSQL 18.1 connection pooling (SQLAlchemy async engine)
- LangGraph parallel agent execution (discovery + analysis layers)
- FastAPI async endpoints (handle concurrent requests)
- Frontend lazy loading (load report sections on-demand)

---

## Deployment Architecture

**MVP Deployment (Local/Single VPS):**

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:18.1
    environment:
      POSTGRES_DB: aihedgefund
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: .
    command: fastapi run src/main.py --host 0.0.0.0 --port 8000
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@db:5432/aihedgefund
      - EODHD_API_KEY=${EODHD_API_KEY}
      # ... all other env vars
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./src:/app/src  # Hot reload in dev

  scheduler:
    build: .
    command: python src/automation/scheduler.py
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@db:5432/aihedgefund
      # ... all other env vars
    depends_on:
      - db

  frontend:
    build: ./app/frontend
    command: npm run dev -- --host 0.0.0.0 --port 5173
    ports:
      - "5173:5173"
    volumes:
      - ./app/frontend/src:/app/src  # Hot reload in dev

volumes:
  pgdata:
```

**Production Deployment (Cloud):**
- Backend: AWS ECS/Fargate or DigitalOcean App Platform
- Database: AWS RDS PostgreSQL 18.1 or managed DigitalOcean Postgres
- Frontend: Vercel or Cloudflare Pages (static build)
- Scheduler: AWS EventBridge + Lambda or DigitalOcean Functions
- Monitoring: AWS CloudWatch or Datadog

---

## Development Environment

### Prerequisites

**Required:**
- Python 3.14+ (latest stable)
- Node.js 20.19+ (for Vite 6)
- PostgreSQL 18.1+ (local or Docker)
- Git

**API Keys Needed:**
- EODHD All-In-One (£85/month) - https://eodhd.com/
- CityFALCON (£30/month) - https://www.cityfalcon.com/
- IBKR API (free with account) - https://www.interactivebrokers.com/
- OpenAI API (GPT-4o) - https://platform.openai.com/
- Anthropic API (Claude, optional fallback) - https://www.anthropic.com/
- Google AI API (Gemini, optional fallback) - https://ai.google.dev/

### Setup Commands

```bash
# 1. Clone repository
git clone <repo-url>
cd AIHedgeFund

# 2. Backend setup
cd ai-hedge-fund
python3.14 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Database setup
createdb aihedgefund  # Or use Docker: docker-compose up -d db
alembic upgrade head  # Run migrations
python scripts/seed_data.py  # Load UK ticker mapping

# 4. Environment configuration
cp .env.example .env
# Edit .env with your API keys

# 5. Frontend setup
cd app/frontend
npm install

# 6. Run development servers
# Terminal 1: Backend
cd ai-hedge-fund
fastapi dev src/main.py

# Terminal 2: Frontend
cd app/frontend
npm run dev

# Terminal 3: Scheduler (optional, for testing overnight batch)
cd ai-hedge-fund
python src/automation/scheduler.py
```

### Testing Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/agents/test_news_scanner.py

# Run integration tests only
pytest tests/integration/

# Run with debug output
pytest -vv -s
```

---

## Architecture Decision Records (ADRs)

### ADR-001: Use Python 3.14 (Latest Stable)

**Context:** Need to choose Python version for 5+ year project lifespan.

**Decision:** Use Python 3.14 (latest stable, Oct 2025)

**Rationale:**
- LangGraph 1.0 requires Python 3.10+ (dropped 3.9 support in Oct 2025)
- Python 3.14 free-threaded mode enables true parallelism for agent execution
- JIT compiler improves performance for long-running batch processing
- 5 years of security support (until Oct 2030)
- Latest stable = best library compatibility going forward

**Alternatives Considered:**
- Python 3.12 (conservative choice, but already 2 years old by 2025)
- Python 3.10 (minimum for LangGraph 1.0, but nearing EOL in 2026)

**Status:** Accepted

---

### ADR-002: Use LangGraph 1.0 for Agent Orchestration

**Context:** Need durable, production-grade multi-agent orchestration framework.

**Decision:** Use LangGraph 1.0.5 (stable release, Nov 2025)

**Rationale:**
- First stable 1.0 release (no breaking changes until 2.0)
- Durable state persistence (resume workflows after interruptions)
- Human-in-the-loop patterns (manual trade approval)
- StateGraph abstraction enables parallel discovery + sequential decision layers
- Production-proven (Klarna, Replit, Elastic use in production)
- Better than building custom orchestration from scratch

**Alternatives Considered:**
- CrewAI (less mature, no durable state, limited to sequential workflows)
- Custom LangChain implementation (reinventing wheel, high maintenance)
- Raw LangChain (no orchestration, manual state management)

**Status:** Accepted

---

### ADR-003: Use PostgreSQL 18.1 Over SQLite

**Context:** Need database for production trading system with audit trails.

**Decision:** Use PostgreSQL 18.1 (latest stable, Nov 2025)

**Rationale:**
- 3× I/O performance gains (new I/O subsystem in Postgres 18)
- uuidv7() function for efficient time-ordered UUIDs (better indexing)
- JSONB for flexible signal/analysis storage (agent-specific data)
- Production-grade concurrency (multiple processes reading/writing)
- Proper transaction support for trade execution
- SQLite insufficient for concurrent writes (scheduler + API + manual trades)

**Alternatives Considered:**
- SQLite (simple, but no concurrent writes, not production-grade for trading)
- MySQL (less advanced JSON support, weaker for analytics queries)

**Status:** Accepted

---

### ADR-004: React 19 + Vite 6 for Frontend

**Context:** Need modern, fast frontend for trading dashboard.

**Decision:** Use React 19 + TypeScript 5 + Vite 6

**Rationale:**
- React 19 latest stable (compiler improvements, concurrent features)
- TypeScript prevents runtime errors (critical for financial data display)
- Vite 6 fastest dev server (instant HMR, better DX than Create React App)
- TanStack Query simplifies server state (caching, optimistic updates)
- No complex state management needed (TanStack Query handles server state)

**Alternatives Considered:**
- Vue 3 (smaller ecosystem for financial charting libraries)
- Svelte (too niche, fewer TypeScript resources)
- Next.js (overkill for SPA, unnecessary SSR complexity for dashboard)

**Status:** Accepted

---

### ADR-005: Multi-Provider LLM Abstraction

**Context:** Avoid vendor lock-in, enable cost optimization and fallback.

**Decision:** Use LangChain 1.0 multi-provider abstraction (OpenAI, Anthropic, Google)

**Rationale:**
- Cost optimization (use cheapest provider for each agent type)
- Fallback support (if OpenAI down, switch to Anthropic automatically)
- Future-proof (easily add new providers as they emerge)
- LangChain 1.0 provides unified interface across providers
- Agent-specific provider selection (use GPT-4o for discovery, Claude for analysis)

**Alternatives Considered:**
- Single provider (OpenAI only) - vendor lock-in, no fallback
- Direct API calls - reinventing wheel, no fallback logic

**Status:** Accepted

---

### ADR-006: Batch Processing Over Real-Time

**Context:** Balance between responsiveness and cost.

**Decision:** Overnight batch processing (1am-7am) as default, with on-demand option

**Rationale:**
- GPT-4o batch API = 50% cost savings vs. real-time
- UK market closed overnight (no urgency for real-time during US hours)
- Morning report delivery aligns with trader workflow (review before market open)
- On-demand analysis still available for breaking news events
- Cost containment critical for MVP profitability (£200/month target)

**Alternatives Considered:**
- Real-time continuous monitoring (2× cost, minimal benefit for overnight strategy)
- Intraday batch (4× daily) - higher cost, unnecessary for swing trading

**Status:** Accepted

---

### ADR-007: Three-Tier Data Architecture

**Context:** Balance cost, data quality, and execution needs.

**Decision:** 3-tier data architecture
- Tier 1: EODHD (fundamentals, history, macro)
- Tier 2: CityFALCON (UK-specific RNS, insider, sentiment)
- Tier 3: IBKR (real-time quotes only at execution)

**Rationale:**
- Cost optimization (EODHD All-In-One replaces 3-4 separate APIs)
- UK market specialization (CityFALCON = best UK RNS coverage)
- Execution efficiency (IBKR real-time only when needed, not 24/7 streaming)
- Total: £125/month vs. £300+ for premium real-time feeds
- Sufficient for overnight batch + manual execution workflow

**Alternatives Considered:**
- Bloomberg Terminal (£2,000/month - too expensive for MVP)
- All-IBKR (lacks UK RNS feeds, insider data)
- Free Yahoo Finance (unreliable, no insider/RNS data)

**Status:** Accepted

---

_Generated by BMAD Decision Architecture Workflow v1.0_
_Date: 2025-11-22_
_For: Longy_
_By: BMad Master_
