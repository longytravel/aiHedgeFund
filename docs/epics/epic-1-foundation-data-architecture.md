# Epic 1: Foundation & Data Architecture

**Goal:** Establish extensible technical foundation that supports APIs, file drops, agent plugins, and future data sources without requiring rewrites.

**User Value:** Infrastructure ready to ingest data from multiple sources and run AI agents in a modular, extensible way.

**Prerequisites:** None (greenfield project)

### Story 1.1: Project Setup & Repository Structure

**As a** developer,
**I want** a well-organized project structure with Docker containerization,
**So that** the system is deployable and maintainable from day 1.

**Acceptance Criteria:**

**Given** a new greenfield project
**When** the repository is initialized
**Then** the following structure exists:
- `/backend` - FastAPI application
- `/frontend` - React application
- `/agents` - Agent plugin directory
- `/data/inbox` - File drop folders (ticker-lists, research-reports, manual-stocks)
- `/data/processed` - Processed files archive
- `/tests` - Test suites
- `docker-compose.yml` - Multi-container setup
- `.env.example` - Environment variable template
- `README.md` - Setup instructions

**And** Docker containers build successfully
**And** Basic health check endpoint returns 200 OK

**Prerequisites:** None

**Technical Notes:**
- Use Python 3.14 for backend (stable Oct 2025, free-threaded mode, JIT compiler)
- FastAPI 0.121.3 with async support
- React 19 with TypeScript 5.x for frontend
- PostgreSQL 18.1 for database (3× I/O performance gains, uuidv7() support)
- Redis for caching (optional Phase 2)
- Environment variables for all secrets (API keys, database credentials)

**Code Reuse from Reference System:**

**Location:** `C:\Users\User\Desktop\AIHedgeFund\ai-hedge-fund\`

This is a working US-focused AI hedge fund system. Reuse proven components:

1. **Backend Structure (FastAPI):**
   - Reference: `/app/backend/` folder structure
   - Copy: Route patterns (`/api/v1/analysis`, `/api/v1/portfolio`)
   - Adapt: `routes/`, `services/`, `models/` organization

2. **LangGraph Patterns:**
   - Reference: `services/graph.py` for agent orchestration examples
   - Copy: State management, error handling, parallel execution patterns
   - Saves weeks of debugging distributed agent workflows

3. **Docker Configuration:**
   - Reference: `docker/docker-compose.yml` structure
   - Copy: Service definitions, container orchestration
   - Adapt: UK system-specific services

4. **React Components (Partial):**
   - Reference: `/app/frontend/src/` for dashboard layouts
   - Copy: Portfolio view, signal display, report components
   - Adapt: UK market terminology, GBP currency

5. **Investor Persona Prompts:**
   - Copy: Agent prompts for Buffett, Lynch, Burry, Munger, etc.
   - Adapt: Add Naked Trader (UK-focused), adjust for UK market context

**Do NOT Copy:**
- Sequential workflow logic (we're building batch overnight)
- US market assumptions (tickers, exchanges, data sources)
- Financial Datasets API integration (we use EODHD)
- Interactive CLI approach (we're building autonomous batch)

---

### Story 1.2: Database Schema & Models

**As a** system,
**I want** a comprehensive database schema supporting all future features,
**So that** new capabilities can be added without schema migrations breaking existing data.

**Acceptance Criteria:**

**Given** PostgreSQL database is running
**When** migrations are applied
**Then** the following tables exist with proper relationships:

**Core Tables:**
- `stocks` - UK company master data (ticker, name, sector, market_cap)
- `signals` - Discovery agent signals (ticker, signal_type, score, timestamp, source)
- `analyses` - Analysis agent outputs (ticker, agent_name, recommendation, confidence, reasoning)
- `portfolio` - Current holdings (ticker, entry_date, entry_price, quantity, stop_loss, target)
- `watchlist` - Stocks being monitored (ticker, trigger_type, trigger_value, thesis, expiry_date)
- `research_queue` - Stocks under investigation (ticker, score, status)
- `trades` - Historical trade log (ticker, action, price, quantity, timestamp, outcome)
- `reports` - Generated morning reports (date, content, stocks_analyzed, recommendations_count)
- `agent_config` - Agent settings (agent_name, enabled, weight, parameters)
- `audit_log` - All system decisions (timestamp, action, data, user_id)

**And** All tables have proper indexes on frequently queried columns
**And** Foreign key constraints maintain referential integrity
**And** Timestamps use UTC timezone
**And** Schema supports soft deletes (deleted_at column where needed)

**Prerequisites:** Story 1.1

**Technical Notes:**
- Use SQLAlchemy ORM models
- Alembic for migrations
- Include created_at, updated_at timestamps on all tables
- watchlist table supports multiple trigger types (price, event, macro, technical) - enables Phase 2 features
- agent_config table supports JSON parameters field for extensibility

---

### Story 1.3: Abstract Data Source Interface

**As a** system architect,
**I want** an abstract DataSource interface that all data providers implement,
**So that** new data sources (APIs, files, webhooks) can be added without changing core logic.

**Acceptance Criteria:**

**Given** the agent system needs data from multiple sources
**When** a new data source is added
**Then** it implements the `DataSource` abstract base class:

```python
class DataSource(ABC):
    @abstractmethod
    async def fetch(self) -> List[Signal]:
        """Fetch data and return normalized signals"""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Return unique source identifier"""
        pass
```

**And** All data sources return standardized `Signal` objects:
- ticker: str (e.g., "VOD.L")
- signal_type: str (e.g., "NEWS_CATALYST", "INSIDER_CONVICTION")
- score: int (0-100)
- confidence: float (0.0-1.0)
- data: dict (source-specific metadata)
- timestamp: datetime
- source: str (e.g., "news_scanner", "eodhd_fundamental")

**And** DataSourceRegistry manages all registered sources
**And** Sources can be enabled/disabled via configuration
**And** Failed sources log errors but don't crash the system

**And** Fallback data sources are implemented:

**Primary:** EODHD API (£80/month)

**Fallback Options (Implement Interface, Don't Activate by Default):**

1. **Yahoo Finance (Free):**
   - Use for: Basic price data, historical OHLCV
   - Limitations: No fundamentals, unreliable UK data quality
   - Implementation: `YahooFinanceProvider` class (implements `DataSource` interface)
   - Activation: Manual fallback when EODHD unavailable

2. **Alpha Vantage (Free tier: 25 calls/day):**
   - Use for: Emergency price data if EODHD + Yahoo both fail
   - Limitations: Rate limits too strict for production use
   - Implementation: `AlphaVantageProvider` class (implements `DataSource` interface)
   - Activation: Last resort only

**Automatic Failover Logic:**
- If EODHD returns 429 (rate limit) → Sleep 60s, retry 3x → Fallback to Yahoo
- If EODHD returns 5xx (server error) → Fallback to Yahoo immediately
- Log all failovers to `system_logs` table with severity: WARNING
- Morning report includes notice: "Data source: Yahoo Finance (EODHD unavailable)"

**Graceful Degradation:**
- Yahoo Finance active → Limited fundamental data, price/volume only
- All providers down → Use cached data (up to 24 hours old), flag staleness
- No cached data → Skip affected stocks, continue with available data

**Testing:**
- Mock EODHD failure → System continues using Yahoo (degraded mode)
- Mock all providers down → System uses cache, flags data age
- Integration test: Verify automatic failover works end-to-end

**Prerequisites:** Story 1.1, 1.2

**Technical Notes:**
- Use Python ABC (Abstract Base Class)
- Async/await pattern for all data fetching
- Pydantic models for Signal validation
- Registry pattern for managing data sources
- Dependency injection for testability

---

### Story 1.4: EODHD API Integration (MVP Financial Data Provider)

**As a** discovery system,
**I want** to fetch UK stock data from a financial data provider (EODHD for MVP),
**So that** I have fundamental data, prices, and company information for analysis.

**Acceptance Criteria:**

**Given** valid EODHD API key in environment variables
**When** the EODHD data source implementation is triggered
**Then** it successfully fetches:
- Historical prices (OHLCV) for LSE-listed stocks
- Fundamental data (income statement, balance sheet, cash flow)
- Financial ratios (P/E, P/B, ROE, ROA, debt ratios, custom metrics)
- Company profile (sector, industry, market cap, description)
- Analyst estimates (EPS, revenue consensus)
- ANY available metrics from EODHD API (store all, filter later)

**And** All fetched data is stored in flexible JSON structure for extensibility
**And** Data is cached for configurable duration (default: 24 hours)
**And** Rate limits are respected (100k calls/day, configurable)
**And** Failed API calls retry with exponential backoff (attempts configurable)
**And** Pence vs pounds conversion handled correctly (divide by 100 where needed)
**And** LSE exchange code ('.LSE' suffix) properly formatted

**And** Implementation follows DataSource interface from Story 1.3
**And** Provider is swappable via config without code changes:
```yaml
# config/data_sources.yaml
primary_fundamental_provider: eodhd  # Or: alpha_vantage, financial_modeling_prep
providers:
  eodhd:
    api_key: ${EODHD_API_KEY}
    cache_duration_hours: 24
    rate_limit_per_day: 100000
  # Future providers added here
```

**Prerequisites:** Story 1.3 (Abstract Data Source Interface)

**Technical Notes:**
- **MVP Choice:** EODHD (cost-effective, UK coverage)
- **Swappability:** Implements DataSource interface - can replace with Alpha Vantage, FMP, Bloomberg API
- EODHD Python client wrapper
- Base URL: https://eodhistoricaldata.com/api
- Endpoint examples:
  - `/fundamentals/{ticker}.LSE` - Company fundamentals
  - `/eod/{ticker}.LSE` - Historical prices
  - `/calendar/earnings` - Upcoming earnings
- **Store ALL metrics:** Don't filter at ingestion - store everything EODHD provides
- Flexible schema: Use JSONB columns for metric storage (supports adding new metrics)
- Handle API errors gracefully (503 Service Unavailable, 429 Rate Limit)
- Store API key in environment variable `EODHD_API_KEY`
- Log all API calls for cost tracking
- **Future:** User might want Bloomberg, Refinitiv, or custom data sources - architecture supports it

---

### Story 1.5: File Inbox System - CSV Ticker Lists

**As a** user,
**I want** to drop CSV files with ticker lists into a folder,
**So that** the system analyzes stocks I manually select.

**Acceptance Criteria:**

**Given** a CSV file exists in `/data/inbox/ticker-lists/`
**When** the file inbox processor runs
**Then** it reads the CSV file with columns: ticker, reason (optional)

**And** Each ticker is validated (exists in LSE, proper format)
**And** A `MANUAL_SELECTION` signal is created for each ticker with score 20
**And** Invalid tickers are logged to error log
**And** Processed files are moved to `/data/processed/ticker-lists/{date}/`
**And** CSV parsing handles common formats (comma, semicolon delimiters)
**And** Empty rows and header rows are skipped
**And** Duplicate tickers in same file are de-duplicated

**Example CSV:**
```
ticker,reason
VOD.L,Saw insider buying
BP.L,Strong dividend yield
TSCO.L,Undervalued on P/E
```

**Prerequisites:** Story 1.3

**Technical Notes:**
- Use pandas for CSV parsing
- Support .csv and .txt extensions
- Handle encoding issues (UTF-8, Windows-1252)
- File monitoring: scan folder every batch run (not real-time for MVP)
- Error file: Move malformed CSVs to `/data/errors/` with error report

---

### Story 1.6: File Inbox System - Manual Stock JSON

**As a** user,
**I want** to drop simple JSON files to manually add stocks to research queue,
**So that** I can quickly add stocks I hear about (podcasts, tweets, conversations).

**Acceptance Criteria:**

**Given** a JSON file exists in `/data/inbox/manual-stocks/`
**When** the file inbox processor runs
**Then** it parses JSON with schema:
```json
{
  "ticker": "XYZ.L",
  "reason": "CEO bought £500k shares",
  "source": "LSE RNS",
  "urgency": "normal"
}
```

**And** Ticker is validated against LSE stock database
**And** A `MANUAL_ADDITION` signal is created with score 25
**And** Reason is stored in signal metadata for agent context
**And** Invalid JSON files are moved to `/data/errors/` with error details
**And** Processed files are moved to `/data/processed/manual-stocks/`
**And** Multiple JSON files can be processed in one run

**Prerequisites:** Story 1.3

**Technical Notes:**
- Use Python json library
- Schema validation with Pydantic
- Support both .json extension
- Optional fields: source, urgency (defaults: "manual", "normal")
- Future enhancement: Web UI creates these JSON files automatically

---

### Story 1.7: LangGraph Agent Orchestration Foundation

**As a** system architect,
**I want** LangGraph set up for multi-agent workflows,
**So that** agents can run in parallel, maintain state, and communicate.

**Acceptance Criteria:**

**Given** multiple AI agents need orchestration
**When** LangGraph is configured
**Then** it supports:
- Parallel agent execution (multiple agents analyze same stock simultaneously)
- Shared state management (all agents access same stock data)
- Conditional routing (route to different agents based on signals)
- Error handling per agent (one agent failure doesn't crash workflow)
- State persistence (save workflow state to database)

**And** Agent workflow graph is defined:
```
START → [Discovery Agents] → Signal Aggregation →
[Analysis Agents (parallel)] → Risk Manager → Portfolio Manager → END
```

**And** State object contains:
- ticker: str
- signals: List[Signal]
- analyses: List[AgentAnalysis]
- decision: Decision (BUY/SELL/HOLD)
- metadata: dict

**And** Workflow execution time is logged for performance monitoring
**And** Failed workflows are retried once before marking as failed

**Prerequisites:** Story 1.1, 1.2

**Technical Notes:**
- LangGraph library from LangChain
- State graph pattern for workflow management
- Async agent execution for performance
- PostgreSQL for state persistence
- Timeout per agent: 120 seconds (prevent hanging)
- Cost tracking: Log LLM token usage per agent

---

### Story 1.8: Multi-Provider LLM Abstraction Layer

**As a** system architect,
**I want** to support multiple LLM providers (OpenAI, Anthropic, Google) interchangeably,
**So that** each agent can use the optimal model for cost, performance, or availability.

**Acceptance Criteria:**

**Given** the system needs to call various LLM providers
**When** an agent requests LLM completion
**Then** it uses an abstract `LLMProvider` interface:

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
```

**And** Concrete implementations exist for:
- **OpenAIProvider** - GPT-4o, GPT-4o-mini, GPT-4-turbo, o1-preview
- **AnthropicProvider** - Claude 3.5 Sonnet, Claude 3 Haiku, Claude 3 Opus
- **GoogleProvider** - Gemini 1.5 Pro, Gemini 1.5 Flash

**And** Each agent specifies preferred model via configuration:
```yaml
agents:
  macro_economist:
    provider: anthropic
    model: claude-3-5-sonnet-20241022  # Deep reasoning needed

  news_scanner:
    provider: openai
    model: gpt-4o-mini  # Cheap, fast, good enough

  value_investor:
    provider: anthropic
    model: claude-3-5-sonnet-20241022  # Nuanced analysis

  fundamental_screener:
    provider: google
    model: gemini-1.5-flash  # High volume, need speed
```

**And** LLMProvider handles:
- API key management (different env vars per provider)
- Rate limiting per provider
- Automatic retry with exponential backoff
- Error handling (provider outage → log and fail gracefully)
- Token counting for cost tracking
- Response caching (optional, same prompt = cached response for 1 hour)

**And** Cost tracking logs every call:
```
{
  "agent": "value_investor",
  "provider": "anthropic",
  "model": "claude-3-5-sonnet-20241022",
  "input_tokens": 2500,
  "output_tokens": 800,
  "cost_usd": 0.0145,
  "timestamp": "2024-11-22T14:30:00Z"
}
```

**And** Fallback mechanism:
- If primary provider fails (API down, rate limited)
- Try secondary provider from config
- Example: Primary=Anthropic, Fallback=OpenAI

**And** All LLM calls are async (non-blocking)
**And** Provider switching doesn't require code changes (config only)

**And** Mock LLM mode for development/testing:

**Purpose:** Avoid burning £50+/day in LLM costs during development and testing

**Mock Implementation:**
```python
class MockLLMProvider(LLMProvider):
    """Mock provider that returns predefined responses from fixture files"""

    def __init__(self, fixtures_path: str = "tests/fixtures/llm_responses/"):
        self.fixtures_path = fixtures_path

    async def complete(self, messages, model, **kwargs) -> LLMResponse:
        # Load mock response from fixture file based on agent/context
        agent_name = kwargs.get("agent_name", "default")
        fixture_file = f"{self.fixtures_path}/{agent_name}_response.json"

        # Return predefined response (zero cost, instant)
        return LLMResponse(
            content=mock_content,
            provider="mock",
            model="mock",
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
            latency_ms=10,
            cached=False
        )
```

**Mock Response Fixtures:**
```
/tests/fixtures/llm_responses/
  ├── value_investor_bullish.json
  ├── value_investor_bearish.json
  ├── contrarian_bullish.json
  ├── contrarian_bearish.json
  ├── news_scanner_catalyst.json
  ├── macro_economist_expansion.json
  └── risk_manager_high_risk.json
```

**Configuration:**
```yaml
# config/llm_providers.yaml
llm:
  mock_mode: false  # Set to true for testing
  mock_fixtures_path: "tests/fixtures/llm_responses/"

  # When mock_mode=true, all agents use MockLLMProvider
  # When mock_mode=false, agents use real providers
```

**Usage:**
```bash
# Development mode with mock LLMs (zero cost)
python main.py --dev --mock-llm

# Test full pipeline without LLM costs
pytest tests/ --mock-llm

# Production mode (real LLMs)
python main.py
```

**Benefits:**
- **Cost savings:** £0 for development testing vs £50+/day with real LLMs
- **Speed:** Instant responses vs 2-5 second LLM latency
- **Reproducibility:** Same fixtures = consistent test results
- **Offline development:** Work without internet/API access

**Testing Strategy:**
- Unit tests: ALWAYS use mock LLMs
- Integration tests: Mix of mock + real (configurable)
- End-to-end tests: Real LLMs (run sparingly, e.g., pre-release)
- Development iterations: Mock LLMs until logic validated, then test with real LLMs

**Fixture Management:**
- Create fixtures by running agents once with real LLMs, saving responses
- Update fixtures when prompts change significantly
- Version control fixtures (committed to git)

**Prerequisites:** Story 1.1, 1.2

**Technical Notes:**

**Libraries:**
- OpenAI: `openai` Python SDK
- Anthropic: `anthropic` Python SDK
- Google: `google-generativeai` Python SDK
- Or use LangChain/LiteLLM for unified interface

**Environment Variables:**
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...

# Default provider (can be overridden per agent)
DEFAULT_LLM_PROVIDER=anthropic
DEFAULT_LLM_MODEL=claude-3-5-sonnet-20241022
```

**Cost Optimization Strategy:**
- **Cheap models** (< $0.10 per 1M input tokens): News scanning, fundamental screening, ticker extraction
- **Mid-tier models** ($0.50-1.00 per 1M): General analysis, sentiment, technical analysis
- **Premium models** ($3-15 per 1M): Macro economist, risk manager, portfolio manager (critical decisions)

**Example Routing:**
```yaml
# Cost-optimized configuration
agents:
  # CHEAP - High Volume Tasks
  news_scanner:
    provider: openai
    model: gpt-4o-mini  # $0.15/1M input

  fundamental_screener:
    provider: google
    model: gemini-1.5-flash  # $0.075/1M input

  # MID-TIER - Standard Analysis
  technical_analyst:
    provider: openai
    model: gpt-4o  # $2.50/1M input

  sentiment_analyst:
    provider: google
    model: gemini-1.5-pro  # $1.25/1M input

  # PREMIUM - Critical Decisions
  value_investor:
    provider: anthropic
    model: claude-3-5-sonnet-20241022  # $3/1M input

  macro_economist:
    provider: anthropic
    model: claude-3-5-sonnet-20241022  # Deep reasoning

  risk_manager:
    provider: anthropic
    model: claude-3-5-sonnet-20241022  # Critical risk assessment

  portfolio_manager:
    provider: anthropic
    model: claude-3-5-sonnet-20241022  # Final decision maker
```

**Estimated Monthly Cost (10-15 stocks/day analyzed):**
- News/Discovery: ~$10-15/month (high volume, cheap models)
- Analysis Agents: ~$40-60/month (GPT-4o, Gemini Pro)
- Decision Agents: ~$20-30/month (Claude Sonnet, lower volume but premium)
- **Total: ~$70-105/month** (well under £200 budget with £125 data costs)

**Response Format Standardization:**
```python
@dataclass
class LLMResponse:
    content: str  # Main response text
    provider: str  # Which provider used
    model: str  # Which model used
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_ms: int
    cached: bool  # Was this from cache?
```

**Future Enhancement (Phase 2):**
- A/B testing: Run same agent with different models, compare performance
- Automatic model selection based on agent performance history
- Cost vs quality optimization (use cheaper model if accuracy acceptable)

---

### Story 1.9: Observability & Logging Infrastructure

**As a** developer and operator,
**I want** comprehensive logging and monitoring of all agent executions, signals, and convergence calculations,
**So that** I can debug issues, track performance, understand why stocks were recommended, and optimize the system.

**Acceptance Criteria:**

**Given** the system has 20+ agents running in a distributed network
**When** agents execute and generate signals
**Then** all activity is logged with structured data:

**1. Structured Logging:**

All logs use structured JSON format for queryability:
```json
{
  "timestamp": "2025-11-22T02:15:30Z",
  "log_level": "INFO",
  "component": "news_scanner",
  "event_type": "agent_execution",
  "ticker": "VOD.L",
  "execution_time_ms": 1250,
  "llm_cost_usd": 0.0015,
  "output_summary": "Generated 1 NEWS_CATALYST signal"
}
```

**And** Agent executions logged with:
- timestamp, agent_name, ticker, execution_time_ms, llm_provider, llm_model, llm_cost_usd, input_tokens, output_tokens, success/failure, error_message (if failed)

**And** Signals logged with:
- timestamp, ticker, signal_type, strength, source_agent, decay_applied, current_score, metadata

**And** Convergence calculations logged with:
- timestamp, ticker, total_score, contributing_signals[], base_score_sum, macro_multiplier, sector_multiplier, convergence_bonus, final_score, routing_decision

**2. Signal Trace Capability:**

**Given** I want to understand why a stock scored high
**When** I query: "Show all signals for VOD.L from last 7 days"
**Then** system returns table:

| Date | Signal Type | Source | Base Score | Decay Applied | Current Score | Metadata |
|------|-------------|--------|------------|---------------|---------------|----------|
| 2025-11-20 | INSIDER_CONVICTION | insider_trading | 80 | 0 days | 80 | CEO bought £100k |
| 2025-11-21 | NEWS_CATALYST | news_scanner | 50 | 1 day | 48 | Major contract win |
| 2025-11-22 | FUNDAMENTAL_MATCH | fundamental_screener | 60 | 0 days | 60 | Value screen passed |

**And** Convergence calculation breakdown:
```
Total Score for VOD.L on 2025-11-22:
Base signals: 80 + 48 + 60 = 188 points
Macro multiplier: 1.3x (expansion regime)
Sector multiplier: 1.1x (Telecoms favored)
Convergence bonus: 1.25x (3 signals)
Final score: 188 × 1.3 × 1.1 × 1.25 = 336 points
Routing: PRIORITY_ANALYSIS (score > 91)
```

**3. Agent Performance Dashboard Data:**

**And** System tracks metrics per agent:
- Avg execution time (ms)
- LLM cost per run (USD)
- Signals generated per run
- Success rate (% of successful executions)
- Last 7 days, last 30 days views

**And** Metrics stored in database:
```sql
CREATE TABLE agent_performance (
  agent_name VARCHAR(50),
  date DATE,
  execution_count INT,
  avg_execution_time_ms INT,
  total_llm_cost_usd DECIMAL,
  signals_generated INT,
  success_rate DECIMAL,
  error_count INT
);
```

**4. Debug Mode:**

**And** `--debug` flag enables verbose logging:
- Every signal broadcast logged
- Every convergence calculation step logged
- Every LLM prompt and response logged
- Every API call logged (URL, params, response time)

**And** Debug output written to: `logs/debug-{timestamp}.log`
**And** Debug mode does NOT run in production (performance overhead)

**5. Cost Tracking:**

**And** Every LLM API call logged:
```json
{
  "timestamp": "2025-11-22T02:15:30Z",
  "agent": "value_investor",
  "provider": "anthropic",
  "model": "claude-3-5-sonnet-20241022",
  "input_tokens": 2500,
  "output_tokens": 800,
  "cost_usd": 0.0145,
  "ticker": "VOD.L"
}
```

**And** Daily cost summary generated:
- Total cost: £2.50
- Cost by agent: news_scanner (£0.30), value_investor (£0.80), etc.
- Cost by LLM provider: OpenAI (£1.20), Anthropic (£1.00), Google (£0.30)

**And** Alert if daily cost exceeds configurable threshold (default: £10)

**6. System Logs Table:**

**And** Central logging table in PostgreSQL:
```sql
CREATE TABLE system_logs (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  log_level VARCHAR(10),  -- DEBUG, INFO, WARNING, ERROR, CRITICAL
  component VARCHAR(50),  -- agent_name, workflow_name, or system component
  event_type VARCHAR(50),  -- agent_execution, signal_generated, convergence_calculated, etc.
  ticker VARCHAR(10),
  data JSONB,  -- Flexible structured data
  message TEXT
);
CREATE INDEX idx_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX idx_logs_ticker ON system_logs(ticker);
CREATE INDEX idx_logs_component ON system_logs(component);
```

**And** Logs queryable via SQL or API
**And** Old logs archived after configurable period (default: 90 days)

**7. Execution Example:**

**Given** I run discovery batch and VOD.L scores 85 points
**When** I query: "Why did VOD.L score 85 on 2025-11-22?"
**Then** System returns:
```
VOD.L scored 85 points on 2025-11-22

Contributing Signals:
1. INSIDER_CONVICTION (80 pts) - CEO bought £100k on 2025-11-20
   Source: insider_trading agent
   Decay: 0 days old, no decay applied

2. NEWS_CATALYST (48 pts) - Major contract announcement
   Source: news_scanner agent
   Decay: 1 day old, base 50 pts × 0.96 = 48 pts

3. FUNDAMENTAL_MATCH (60 pts) - Passed value_screen
   Source: fundamental_screener agent
   Decay: Stable, no decay

Base total: 188 points
Macro multiplier: 1.0x (neutral regime)
Sector multiplier: 0.7x (Telecoms disfavored this week)
Convergence bonus: 1.25x (3 signals converged)
Final calculation: 188 × 1.0 × 0.7 × 1.25 = 164 points

Wait, that's not 85... recalculating based on actual logs...
[System shows actual calculation from logs]
```

**Prerequisites:** Story 1.1 (Database), Story 1.2 (Database Schema), Story 1.7 (LangGraph)

**Technical Notes:**
- **Library:** Python `structlog` for structured JSON logging
- **Storage:** PostgreSQL `system_logs` table (searchable, persistent)
- **Rotation:** Archive old logs to S3/file storage after 90 days
- **Performance:** Async logging (don't block agent execution)
- **Grafana (Phase 2):** Dashboards showing agent performance, costs, signal trends
- **Prometheus (Phase 2):** Metrics export for monitoring
- **Query Interface:** SQL queries, Python API, future web UI
- **Cost:** ~50MB/day logs for 600 stocks = negligible storage cost
- **Critical for complex systems:** Without logging, debugging distributed agent networks is impossible

---
