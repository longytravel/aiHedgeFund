# Epic Technical Specification: Foundation & Data Architecture

Date: 2025-11-22
Author: Longy
Epic ID: 1
Status: Draft

---

## Overview

Epic 1 establishes the extensible technical foundation for the AIHedgeFund system - a multi-agent AI trading platform that discovers, analyzes, and recommends UK stock investments through overnight batch processing. This epic delivers the core infrastructure that enables data ingestion from multiple sources (APIs, file drops), agent orchestration via LangGraph, multi-provider LLM abstraction, and comprehensive observability. The foundation is built for modularity, allowing new data sources, agents, and workflows to be added without requiring system rewrites.

The epic transforms a greenfield project into a production-ready platform capable of supporting 20+ AI agents analyzing 600+ UK stocks nightly, with all technical components designed for extensibility, cost-efficiency (target: £200/month), and reliability (95%+ uptime during trading hours).

## Objectives and Scope

**In Scope:**

- Docker-containerized project structure (backend, frontend, agents, data inbox, tests)
- PostgreSQL 18.1 database with comprehensive schema supporting all tiers (portfolio, watchlist, research queue, signals, trades, audit logs)
- Abstract DataSource interface enabling swappable data providers (EODHD primary, Yahoo/Alpha Vantage fallback)
- EODHD API integration for UK fundamentals, historical prices, analyst estimates, macroeconomic indicators
- File inbox system for manual CSV ticker lists and JSON stock additions
- LangGraph agent orchestration foundation supporting parallel discovery and sequential decision-making
- Multi-provider LLM abstraction layer (OpenAI, Anthropic, Google) with cost tracking and mock mode for development
- Observability infrastructure with structured logging, signal tracing, agent performance tracking, and cost monitoring

**Out of Scope (Future Epics):**

- Discovery agents (Epic 2)
- Analysis agents (Epic 3)
- Portfolio management and decision logic (Epic 4)
- Reporting and UI (Epic 5)
- Broker integration and auto-execution (Phase 2-3)

## System Architecture Alignment

The technical foundation aligns directly with the Implementation Architecture document:

**Technology Stack:** Python 3.14 (free-threaded, JIT), FastAPI 0.121.3 (async), LangGraph 1.0.5 (durable agent orchestration), PostgreSQL 18.1 (3× I/O performance), React 19 (frontend), SQLAlchemy 2.x (async ORM).

**Agent Network:** LangGraph StateGraph architecture with parallel fan-out for discovery agents, convergence scoring, conditional routing to analysis agents, and sequential decision pipeline (Risk Manager → Portfolio Manager).

**Data Architecture:** Normalized relational schema (stocks, signals, analysis_results, portfolio_positions, watchlist_entries, research_queue, trades, audit_log) with JSONB columns for flexible metadata storage.

**Integration Points:** EODHD API (fundamentals, prices, earnings), CityFALCON API (RNS feeds, insider dealings - Epic 2), IBKR API (real-time quotes - Phase 2), Multi-provider LLM interface (OpenAI GPT-4o, Anthropic Claude, Google Gemini).

## Detailed Design

### Services and Modules

| Module | Responsibility | Key Components | Dependencies |
|--------|---------------|-----------------|--------------|
| **Backend API** | FastAPI REST API serving frontend and orchestrating workflows | `/api/v1/analysis`, `/api/v1/portfolio`, `/api/v1/signals`, `/api/health` | FastAPI, SQLAlchemy, Pydantic |
| **Database Layer** | PostgreSQL schema and ORM models | SQLAlchemy models: `Stock`, `Signal`, `AnalysisResult`, `PortfolioPosition`, `Trade`, `AuditLog` | PostgreSQL 18.1, Alembic migrations |
| **Data Sources** | Abstract data provider interface with concrete implementations | `DataSource` ABC, `EODHDProvider`, `YahooFinanceProvider`, `AlphaVantageProvider`, `DataSourceRegistry` | httpx (async HTTP), env vars for API keys |
| **File Inbox** | CSV and JSON file processing for manual stock additions | `InboxProcessor`, `CSVTickerListProcessor`, `ManualStockJSONProcessor` | pandas (CSV parsing), pathlib |
| **LangGraph Orchestration** | Agent workflow management and state persistence | `StateGraph`, `AgentState`, discovery nodes, analysis nodes, decision nodes | LangGraph 1.0.5, PostgreSQL (state persistence) |
| **LLM Providers** | Multi-provider abstraction with cost tracking | `LLMProvider` ABC, `OpenAIProvider`, `AnthropicProvider`, `GoogleProvider`, `MockLLMProvider` | openai, anthropic, google-generativeai SDKs |
| **Observability** | Structured logging, metrics, cost tracking | `structlog` (JSON logging), `system_logs` table, `agent_performance` table, debug mode | PostgreSQL, structlog library |

**Module Interaction Flow:**
```
User/Scheduler → FastAPI Backend → LangGraph Orchestrator
                                    ↓
                  [Data Sources (EODHD/Yahoo/Files)]
                                    ↓
                  [Agent Nodes (Discovery/Analysis/Decision)]
                                    ↓
                  [Database Layer (PostgreSQL)]
                                    ↓
                  [Observability Logs & Metrics]
```

### Data Models and Contracts

**Core Data Entities:**

```python
# SQLAlchemy ORM Models

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String(10), unique=True, nullable=False)  # e.g., "VOD.L"
    name = Column(String(255), nullable=False)
    sector = Column(String(100))  # GICS Level 1
    industry = Column(String(100))  # GICS Level 2
    market_cap = Column(Numeric(15, 2))  # GBP millions
    exchange = Column(String(10))  # "LSE", "AIM"
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Signal(Base):
    __tablename__ = "signals"
    id = Column(UUID(as_uuid=True), primary_key=True)
    type = Column(String(50), nullable=False)  # "NEWS_CATALYST", "INSIDER_CONVICTION"
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id"))
    stock_ticker = Column(String(10), nullable=False)
    strength = Column(Integer, nullable=False)  # 0-100 base score
    data = Column(JSONB, nullable=False)  # Agent-specific metadata
    agent_id = Column(String(50), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"
    id = Column(UUID(as_uuid=True), primary_key=True)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id"))
    stock_ticker = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    entry_price = Column(Numeric(10, 2), nullable=False)
    entry_date = Column(Date, nullable=False)
    stop_loss = Column(Numeric(10, 2))
    target_price = Column(Numeric(10, 2))
    current_price = Column(Numeric(10, 2))
    unrealized_pnl = Column(Numeric(12, 2))
    status = Column(String(20), default="ACTIVE")  # "ACTIVE", "CLOSED"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Data Validation Contracts (Pydantic):**

```python
from pydantic import BaseModel, Field, field_validator

class SignalCreate(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    stock_ticker: str = Field(..., pattern=r"^[A-Z]{2,4}\.L$")
    strength: int = Field(..., ge=0, le=100)
    data: dict
    agent_id: str

    @field_validator("type")
    def validate_signal_type(cls, v):
        valid_types = ["NEWS_CATALYST", "INSIDER_CONVICTION", "FUNDAMENTAL_MATCH", "UNUSUAL_ACTIVITY"]
        if v not in valid_types:
            raise ValueError(f"Signal type must be one of {valid_types}")
        return v

class LLMResponse(BaseModel):
    content: str
    provider: str  # "openai", "anthropic", "google", "mock"
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_ms: int
    cached: bool = False
```

### APIs and Interfaces

**Abstract DataSource Interface:**

```python
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

@dataclass
class Signal:
    ticker: str
    signal_type: str
    score: int  # 0-100
    confidence: float  # 0.0-1.0
    data: dict
    timestamp: datetime
    source: str

class DataSource(ABC):
    @abstractmethod
    async def fetch(self) -> List[Signal]:
        """Fetch data and return normalized signals"""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Return unique source identifier"""
        pass

# Concrete Implementation Example
class EODHDProvider(DataSource):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://eodhistoricaldata.com/api"

    async def fetch(self) -> List[Signal]:
        # Implementation fetches fundamentals, prices
        # Returns standardized Signal objects
        pass

    def get_source_name(self) -> str:
        return "eodhd_fundamental"
```

**Abstract LLMProvider Interface:**

```python
class LLMProvider(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Get completion from LLM"""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider name (openai, anthropic, google)"""
        pass

    @abstractmethod
    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Estimate cost in USD for this call"""
        pass

# Concrete Implementation Example
class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    async def complete(self, messages, model, **kwargs) -> LLMResponse:
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return LLMResponse(
            content=response.choices[0].message.content,
            provider="openai",
            model=model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            cost_usd=self.estimate_cost(...)
        )

    def estimate_cost(self, input_tokens, output_tokens, model) -> float:
        # Pricing table for OpenAI models
        pricing = {
            "gpt-4o": {"input": 2.50, "output": 10.00},  # per 1M tokens
            "gpt-4o-mini": {"input": 0.15, "output": 0.60}
        }
        input_cost = (input_tokens / 1_000_000) * pricing[model]["input"]
        output_cost = (output_tokens / 1_000_000) * pricing[model]["output"]
        return input_cost + output_cost
```

**FastAPI Endpoints:**

```python
# /api/v1/stocks
GET /api/v1/stocks  # List all stocks
GET /api/v1/stocks/{ticker}  # Get single stock details
POST /api/v1/stocks  # Add new stock (admin)

# /api/v1/signals
GET /api/v1/signals  # List signals (filterable by ticker, type, date)
POST /api/v1/signals  # Create new signal (agents only)

# /api/v1/portfolio
GET /api/v1/portfolio/positions  # List active positions
POST /api/v1/portfolio/positions  # Add position (manual trade logging)
PATCH /api/v1/portfolio/positions/{id}  # Update position (price, P&L)

# /api/health
GET /api/health  # System health check
```

**Response Formats:**

```json
{
  "success": true,
  "data": {
    "ticker": "VOD.L",
    "name": "Vodafone Group PLC",
    "sector": "Telecommunications",
    "market_cap": 18500.00,
    "signals": [
      {
        "type": "INSIDER_CONVICTION",
        "strength": 80,
        "agent": "insider_trading",
        "timestamp": "2025-11-22T02:30:00Z"
      }
    ]
  },
  "timestamp": "2025-11-22T07:00:00Z"
}
```

### Workflows and Sequencing

**LangGraph Agent Orchestration (Epic 1 Foundation):**

```python
from langgraph.graph import StateGraph
from typing import TypedDict, List

class AgentState(TypedDict):
    ticker: str
    signals: List[Signal]
    analyses: List[AgentAnalysis]
    decision: str  # "BUY", "SELL", "HOLD"
    metadata: dict

# Create StateGraph
workflow = StateGraph(AgentState)

# Placeholder nodes (Epic 1 foundation, agents implemented in Epic 2-3)
workflow.add_node("initialize", initialize_state)
workflow.add_node("data_collection", collect_data_sources)

# Future agent nodes (structure defined now, implemented later)
workflow.add_node("discovery_agents", discovery_placeholder)
workflow.add_node("analysis_agents", analysis_placeholder)
workflow.add_node("decision_agents", decision_placeholder)

# Sequential workflow (basic structure)
workflow.add_edge("initialize", "data_collection")
workflow.add_edge("data_collection", "discovery_agents")
workflow.add_conditional_edges("discovery_agents", route_to_analysis)
workflow.add_edge("analysis_agents", "decision_agents")

# Compile
app = workflow.compile()
```

**File Inbox Processing Sequence:**

```
1. Scanner checks /data/inbox/ folders every batch run (1:00 AM)
2. Process CSV ticker lists:
   - Read CSV with pandas
   - Validate tickers against stocks table
   - Generate MANUAL_SELECTION signals (score: 20)
   - Move processed file to /data/processed/ticker-lists/{date}/
3. Process JSON stock additions:
   - Parse JSON, validate schema
   - Generate MANUAL_ADDITION signals (score: 25)
   - Move processed file to /data/processed/manual-stocks/
4. Handle errors:
   - Malformed files → /data/errors/ with error report
   - Invalid tickers → Log to error log, skip
```

## Non-Functional Requirements

### Performance

- **Database Query Performance:** Stock lookup by ticker < 10ms (indexed), signal aggregation for 600 stocks < 2 minutes (vectorized Pandas operations)
- **API Response Times:** Health check < 100ms, portfolio list < 500ms, stock details < 200ms
- **LLM Call Efficiency:** Mock mode for development (0 cost, instant response), production mode < 5 seconds per agent call
- **File Inbox Processing:** 100 CSV rows/second, JSON parsing < 50ms per file

### Security

- **API Key Storage:** All keys (EODHD, OpenAI, Anthropic, Google) in environment variables, never committed to git
- **Database Encryption:** Passwords encrypted at rest using bcrypt (Phase 2 multi-user), connection strings in .env file
- **Input Validation:** Pydantic models validate all API inputs, SQL injection prevented by SQLAlchemy ORM parameterized queries
- **Docker Isolation:** Services run in separate containers with minimal privileges

### Reliability

- **Failover Strategy:** EODHD API failure → use cached data (up to 7 days for fundamentals), log warning in system_logs table
- **Retry Logic:** API calls retry 3x with exponential backoff (1s, 3s, 9s), circuit breaker after 3 consecutive failures
- **Data Validation:** Reject prices < 0 or > £10,000, reject missing critical fundamentals (market cap, debt, equity), flag staleness
- **State Persistence:** LangGraph workflow state saved to PostgreSQL, can resume after crash

### Observability

- **Structured Logging:** All logs JSON format with correlation IDs, log levels (DEBUG dev, INFO prod, ERROR always)
- **Agent Execution Tracking:** Every agent call logged with timestamp, model, input/output tokens, cost, execution time
- **Signal Traceability:** Query "Why did VOD score 85?" returns breakdown: signals contributing, decay applied, multipliers, final score
- **Cost Monitoring:** Daily LLM cost summary by agent and provider, alert if exceeds configurable budget (default: £10/day)

## Dependencies and Integrations

**Python Dependencies (pyproject.toml):**

```toml
[project]
name = "aihedgefund"
version = "0.1.0"
requires-python = ">=3.14"

dependencies = [
    "fastapi==0.121.3",
    "uvicorn[standard]==0.34.0",
    "sqlalchemy[asyncio]==2.0.36",
    "alembic==1.14.0",
    "asyncpg==0.30.0",  # PostgreSQL async driver
    "pydantic==2.10.4",
    "pydantic-settings==2.7.0",
    "langgraph==1.0.5",
    "langchain==1.0.0",
    "openai==1.59.6",
    "anthropic==0.42.0",
    "google-generativeai==0.8.3",
    "httpx==0.28.1",
    "pandas==2.2.3",
    "structlog==24.4.0",
    "python-dotenv==1.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest==8.3.4",
    "pytest-asyncio==0.24.0",
    "black==24.10.0",
    "ruff==0.8.4",
]
```

**External Integrations:**

- **EODHD API:** Endpoint `https://eodhistoricaldata.com/api`, requires API key (env: `EODHD_API_KEY`), 100k calls/day quota
- **OpenAI API:** Models `gpt-4o`, `gpt-4o-mini`, requires API key (env: `OPENAI_API_KEY`), rate limit 10k requests/day
- **Anthropic API:** Models `claude-3-5-sonnet-20241022`, `claude-3-haiku-20240307`, requires API key (env: `ANTHROPIC_API_KEY`)
- **Google Gemini API:** Models `gemini-1.5-pro`, `gemini-1.5-flash`, requires API key (env: `GOOGLE_API_KEY`)

**Container Dependencies (docker-compose.yml):**

```yaml
services:
  postgres:
    image: postgres:18.1
    environment:
      POSTGRES_DB: aihedgefund
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/aihedgefund
      EODHD_API_KEY: ${EODHD_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"

volumes:
  postgres_data:
```

## Acceptance Criteria (Authoritative)

1. **Project Structure:** Docker containers build successfully, health check endpoint returns 200 OK, `/backend`, `/frontend`, `/agents`, `/data/inbox` folders exist
2. **Database Schema:** All tables created via Alembic migrations, indexes on frequently queried columns (ticker, timestamp), foreign key constraints enforced
3. **DataSource Interface:** `DataSource` ABC defined, `EODHDProvider` implemented and functional, `YahooFinanceProvider` fallback works, failed sources log errors but don't crash system
4. **EODHD Integration:** Fetches fundamentals for LSE stocks, handles pence/pounds conversion, respects rate limits, caches data 24 hours, retry logic on failures
5. **File Inbox System:** CSV processor reads ticker lists, validates tickers, generates MANUAL_SELECTION signals (score: 20), moves processed files to archive
6. **LangGraph Foundation:** StateGraph defined with placeholder nodes for discovery/analysis/decision, state persistence to PostgreSQL, workflow executes without error
7. **Multi-Provider LLM:** `LLMProvider` ABC defined, OpenAI/Anthropic/Google providers work, cost tracking logs input/output tokens, MockLLMProvider for development (zero cost)
8. **Observability:** Structured JSON logs, `system_logs` table stores all events, agent execution time tracked, daily cost summary generated, debug mode enables verbose logging

## Traceability Mapping

| AC# | PRD Requirement | Spec Section | Component/API | Test Idea |
|-----|-----------------|--------------|---------------|-----------|
| 1 | FR-8.1 (Project Structure) | Detailed Design → Services | Docker containers, health endpoint | Test: `docker-compose up`, curl `/api/health` returns 200 |
| 2 | FR-1.3 (Company/Ticker DB) | Data Models → Stock table | SQLAlchemy `Stock` model, Alembic migration | Test: Insert 600 FTSE stocks, query by ticker < 10ms |
| 3 | FR-5.1 (Data Architecture) | APIs → DataSource interface | `DataSource` ABC, `EODHDProvider` | Test: Mock API failure → fallback to Yahoo |
| 4 | FR-5.2 (EODHD Integration) | APIs → EODHDProvider | `get_fundamentals()`, `get_prices()` | Test: Fetch VOD.L fundamentals, verify P/E ratio |
| 5 | FR-5.6 (File Inbox) | Workflows → File Inbox Processing | `CSVTickerListProcessor`, `ManualStockJSONProcessor` | Test: Drop CSV with 10 tickers, verify 10 signals created |
| 6 | FR-2.2 (LangGraph Orchestration) | Detailed Design → LangGraph | `StateGraph`, agent nodes | Test: Execute workflow, verify state transitions |
| 7 | NFR-M5 (Multi-Provider LLM) | APIs → LLMProvider interface | `OpenAIProvider`, `AnthropicProvider`, `GoogleProvider` | Test: Call each provider, verify cost calculation |
| 8 | FR-5.5 (Observability) | Observability section | `structlog`, `system_logs` table | Test: Trigger error, verify JSON log entry created |

## Risks, Assumptions, Open Questions

**Risks:**

- **R1 (High):** EODHD API downtime during overnight batch → **Mitigation:** Implement aggressive caching (7-day TTL for fundamentals), Yahoo Finance fallback, alert user if stale data used
- **R2 (Medium):** PostgreSQL 18.1 too new, compatibility issues → **Mitigation:** Use Docker official image (tested), fallback to PostgreSQL 17.x if needed
- **R3 (Medium):** LLM costs exceed budget during development → **Mitigation:** MockLLMProvider for 90% of testing, strict rate limiting, cost tracking with circuit breaker
- **R4 (Low):** LangGraph breaking changes in v1.x → **Mitigation:** Pin to 1.0.5, monitor changelogs before upgrading

**Assumptions:**

- **A1:** User has EODHD API subscription (£85/month), OpenAI API key, Anthropic API key, Google API key
- **A2:** Docker and Docker Compose installed on deployment machine
- **A3:** PostgreSQL 18.1 is stable enough for production use (released Oct 2024)
- **A4:** File inbox folder `/data/inbox/` is accessible and writable by backend container

**Open Questions:**

- **Q1:** Should we use Redis for caching instead of in-memory cache? → **Decision:** Start with in-memory (simpler), migrate to Redis in Epic 2 if needed
- **Q2:** How to handle UK stock tickers with special characters (e.g., "III.L" for 3i Group)? → **Decision:** Store as-is, validate with regex pattern `^[A-Z0-9]{2,4}\.L$`
- **Q3:** Should MockLLMProvider return random data or fixed fixtures? → **Decision:** Fixed fixtures from `tests/fixtures/llm_responses/` for reproducibility

## Test Strategy Summary

**Unit Tests (Story-Level):**

- **Story 1.1 (Project Setup):** Test Docker containers build, health endpoint returns 200, folder structure exists
- **Story 1.2 (Database Schema):** Test all tables created, indexes exist, foreign keys enforced, migrations reversible
- **Story 1.3 (DataSource Interface):** Test abstract interface, mock implementations, registry pattern, enable/disable sources
- **Story 1.4 (EODHD Integration):** Test fundamentals fetch, price fetch, analyst estimates, error handling, retry logic
- **Story 1.5-1.6 (File Inbox):** Test CSV parsing, JSON parsing, ticker validation, signal generation, file archiving
- **Story 1.7 (LangGraph):** Test state transitions, parallel execution, conditional routing, state persistence
- **Story 1.8 (LLM Providers):** Test each provider, cost estimation, fallback logic, MockLLMProvider
- **Story 1.9 (Observability):** Test structured logging, signal tracing, cost tracking, debug mode

**Integration Tests (Epic-Level):**

- **End-to-End Data Flow:** Drop CSV file → inbox processor → signals created → database updated → logs written
- **LangGraph Workflow:** Initialize state → collect data → execute placeholder agents → persist state → verify completion
- **API Integration:** Call EODHD API → parse response → normalize to Signal objects → cache → verify cached retrieval
- **LLM Integration:** Call OpenAI/Anthropic/Google → verify response format → calculate cost → log to database

**Performance Tests:**

- **Database:** Insert 600 stocks, query by ticker (target: < 10ms), aggregate 1000 signals (target: < 2 min)
- **API:** 100 concurrent health check requests (target: 95%+ < 100ms)
- **File Inbox:** Process CSV with 1000 rows (target: < 10 seconds)

**Coverage Target:** 70%+ for core business logic (DataSource, LLMProvider, LangGraph nodes), 90%+ for critical paths (database models, API validation)
