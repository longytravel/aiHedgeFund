# Story 1.3: Abstract Data Source Interface

Status: done

## Story

As a **system architect**,
I want **an abstract DataSource interface that all data providers implement**,
so that **new data sources (APIs, files, webhooks) can be added without changing core logic**.

## Acceptance Criteria

1. **DataSource Abstract Base Class**
   - **Given** the agent system needs data from multiple sources
   - **When** a new data source is added
   - **Then** it implements the `DataSource` abstract base class with required methods:
     - `async def fetch() -> List[Signal]` - Fetch data and return normalized signals
     - `def get_source_name() -> str` - Return unique source identifier
   - **And** All data sources return standardized `Signal` objects with fields:
     - `ticker: str` (e.g., "VOD.L")
     - `signal_type: str` (e.g., "NEWS_CATALYST", "INSIDER_CONVICTION")
     - `score: int` (0-100)
     - `confidence: float` (0.0-1.0)
     - `data: dict` (source-specific metadata)
     - `timestamp: datetime`
     - `source: str` (e.g., "news_scanner", "eodhd_fundamental")

2. **DataSourceRegistry Pattern**
   - **Given** multiple data sources need to be managed
   - **When** the registry is initialized
   - **Then** it provides methods to:
     - Register new data sources
     - Enable/disable sources via configuration
     - List all available sources
     - Execute fetch from all enabled sources
   - **And** Failed sources log errors but don't crash the system
   - **And** Registry executes sources in parallel for performance

3. **Fallback Provider Implementations**
   - **Given** primary data source (EODHD) may fail
   - **When** fallback providers are implemented
   - **Then** the following providers exist (implementing DataSource interface):
     - `YahooFinanceProvider` - Free, basic price/volume data
     - `AlphaVantageProvider` - Free tier (25 calls/day), emergency fallback
   - **And** Automatic failover logic:
     - If EODHD returns 429 (rate limit) → Sleep 60s, retry 3x → Fallback to Yahoo
     - If EODHD returns 5xx (server error) → Fallback to Yahoo immediately
     - Log all failovers to system_logs with severity WARNING
   - **And** Graceful degradation:
     - Yahoo Finance active → Limited fundamental data, price/volume only
     - All providers down → Use cached data (up to 24 hours old), flag staleness
     - No cached data → Skip affected stocks, continue with available data

4. **Configuration-Based Source Management**
   - **Given** sources need to be configurable without code changes
   - **When** configuration is loaded
   - **Then** sources can be enabled/disabled via YAML config:
```yaml
# config/data_sources.yaml
primary_fundamental_provider: eodhd
providers:
  eodhd:
    enabled: true
    api_key: ${EODHD_API_KEY}
    priority: 1
  yahoo:
    enabled: true
    priority: 2
  alpha_vantage:
    enabled: false
    api_key: ${ALPHA_VANTAGE_API_KEY}
    priority: 3
```
   - **And** Priority determines fallback order (1 = primary, 2 = first fallback, etc.)

## Tasks / Subtasks

- [x] **Task 1: Define DataSource Abstract Base Class** (AC: #1)
  - [x] Create `backend/app/data_sources/base.py` with `DataSource` ABC
  - [x] Define abstract methods: `fetch()` and `get_source_name()`
  - [x] Create `Signal` dataclass for standardized return type
  - [x] Add comprehensive docstrings with usage examples

- [x] **Task 2: Implement DataSourceRegistry** (AC: #2)
  - [x] Create `backend/app/data_sources/registry.py`
  - [x] Implement registry pattern with register/enable/disable methods
  - [x] Add parallel execution of enabled sources using asyncio.gather()
  - [x] Implement error isolation (one source failure doesn't crash others)
  - [x] Add logging for source execution status and timing

- [x] **Task 3: Implement YahooFinanceProvider** (AC: #3)
  - [x] Create `backend/app/data_sources/providers/yahoo_provider.py`
  - [x] Implement DataSource interface
  - [x] Fetch basic price/volume data for LSE stocks
  - [x] Convert to standardized Signal format
  - [x] Handle errors gracefully (network issues, missing data)
  - [x] Add rate limiting if needed

- [x] **Task 4: Implement AlphaVantageProvider** (AC: #3)
  - [x] Create `backend/app/data_sources/providers/alpha_vantage_provider.py`
  - [x] Implement DataSource interface
  - [x] Fetch emergency price data
  - [x] Respect rate limits (25 calls/day)
  - [x] Convert to standardized Signal format
  - [x] Add API key validation

- [x] **Task 5: Implement Failover Logic** (AC: #3)
  - [x] Create `backend/app/data_sources/failover.py`
  - [x] Implement automatic retry with exponential backoff
  - [x] Add provider failover sequence (EODHD → Yahoo → Alpha Vantage)
  - [x] Log all failover events to system_logs table
  - [x] Add staleness flagging for cached data

- [x] **Task 6: Create Configuration System** (AC: #4)
  - [x] Create `config/data_sources.yaml` template
  - [x] Implement config loading in `backend/app/core/config.py`
  - [x] Add environment variable substitution (${EODHD_API_KEY})
  - [x] Validate config schema at startup
  - [x] Support priority-based failover ordering

- [x] **Task 7: Write Unit Tests**
  - [x] Test DataSource ABC (cannot instantiate directly)
  - [x] Test Signal dataclass validation
  - [x] Test DataSourceRegistry registration and execution
  - [x] Test YahooFinanceProvider fetch and signal conversion
  - [x] Test AlphaVantageProvider fetch and rate limiting
  - [x] Test failover logic (mock provider failures)
  - [x] Test configuration loading and validation

- [x] **Task 8: Write Integration Tests**
  - [x] Test end-to-end: Config → Registry → Multiple providers → Signals
  - [x] Test failover scenario: Mock EODHD failure → Yahoo succeeds
  - [x] Test all-providers-down scenario → Graceful degradation
  - [x] Test parallel source execution performance
  - [x] Verify error isolation (one provider crash doesn't affect others)

## Dev Notes

### Architecture Patterns and Constraints

**From ADRs & Implementation Architecture:**

- **Abstract Base Classes:** Use Python ABC module for interface definition
- **Async/Await:** All data fetching uses async patterns for non-blocking I/O
- **Dependency Injection:** Registry pattern allows runtime provider swapping
- **Fail-Safe Design:** System continues with degraded data rather than crashing
- **Observability:** All provider calls logged with timing and status

**From Tech Spec (Epic 1):**

- DataSource interface enables swappable providers (EODHD, Yahoo, Alpha Vantage, future Bloomberg)
- Priority-based failover with configurable retry logic
- Graceful degradation: cached data → partial data → skip affected stocks
- All providers return standardized Signal objects for downstream processing

### Learnings from Previous Story (1.2: Database Schema & Models)

**From Story 1.2 (Status: DONE)**

**New Services/Components Available:**
- SQLAlchemy ORM models in `backend/app/models/` (Stock, Signal, AnalysisResult, etc.)
- Database session management via `backend/app/core/database.py`
- Basic CRUD services in `backend/app/services/data_service.py`
- Signal model with JSONB `data` field for flexible metadata storage

**Architectural Decisions Validated:**
- JSONB columns proven effective for extensible data (Signal.data, AnalysisResult.key_metrics)
- Async SQLAlchemy patterns working well with FastAPI
- Docker build context fixed (root `.` context with proper Dockerfile paths)
- Alembic migrations integrated into backend startup

**Technical Recommendations:**
- Use async database sessions from `database.py` when storing signals
- Leverage Signal model's JSONB `data` field for provider-specific metadata
- Follow established patterns for async service methods (see `data_service.py`)
- Ensure integration tests handle database connectivity failures (pattern established in Story 1.2)

**Files to Reuse/Extend:**
- `backend/app/models/signal_model.py` - Signal ORM model (store fetched signals)
- `backend/app/models/stock_model.py` - Stock ORM model (validate tickers)
- `backend/app/services/data_service.py` - Add methods for signal creation from providers
- `backend/app/core/database.py` - Async session management for signal persistence

**Integration Points:**
- DataSource.fetch() returns Signal dataclass → Convert to Signal ORM model → Store in database
- Use Stock model to validate tickers before creating signals
- Store provider-specific metadata in Signal.data JSONB field (already supports flexible schema)

**Pending Review Items from Story 1.2:**
- None - Story 1.2 fully approved and completed

### Source Tree Components to Touch

**New Files Created:**

- `backend/app/data_sources/__init__.py`
- `backend/app/data_sources/base.py` - DataSource ABC and Signal dataclass
- `backend/app/data_sources/registry.py` - DataSourceRegistry implementation
- `backend/app/data_sources/failover.py` - Failover and retry logic
- `backend/app/data_sources/providers/__init__.py`
- `backend/app/data_sources/providers/yahoo_provider.py` - Yahoo Finance implementation
- `backend/app/data_sources/providers/alpha_vantage_provider.py` - Alpha Vantage implementation
- `config/data_sources.yaml` - Provider configuration template
- `tests/unit/test_data_sources.py` - Unit tests for DataSource components
- `tests/integration/test_provider_failover.py` - Integration tests for failover

**Modified Files:**

- `backend/app/core/config.py` - Add data source configuration loading
- `backend/app/services/data_service.py` - Add signal creation from provider signals
- `backend/requirements.txt` - Add provider dependencies (yfinance, alpha_vantage, pyyaml)
- `pyproject.toml` - Update dependencies if managing there
- `.env.example` - Add ALPHA_VANTAGE_API_KEY template

### Project Structure Notes

**Module Organization:**
- All data source code under `backend/app/data_sources/`
- Providers in `backend/app/data_sources/providers/` subdirectory
- Configuration in `config/` directory at project root
- Tests mirror source structure in `tests/unit/` and `tests/integration/`

**Design Pattern:**
- **Abstract Factory Pattern:** DataSource ABC as factory interface
- **Registry Pattern:** DataSourceRegistry manages concrete implementations
- **Strategy Pattern:** Swappable providers based on configuration
- **Chain of Responsibility:** Failover sequence through providers

### Testing Standards Summary

**Unit Tests (Story-Level):**
- Test DataSource ABC cannot be instantiated
- Test Signal dataclass validation (required fields, type checking)
- Test registry registration, enable/disable, list methods
- Test each provider's fetch() method with mocked API responses
- Test failover logic with mocked provider failures
- Test configuration loading and validation

**Integration Tests:**
- Test full pipeline: Config → Registry → Providers → Database
- Test failover: EODHD mock failure → Yahoo success → Signals stored
- Test parallel execution: Multiple providers fetch simultaneously
- Test error isolation: One provider crash, others succeed
- Test graceful degradation: All providers down → Uses cached data

**Coverage Target:**
- 90%+ for DataSource interface and registry (critical infrastructure)
- 80%+ for provider implementations
- 100% for failover logic (critical for reliability)

### References

- **Epic Tech Spec:** [Source: docs/sprint-artifacts/tech-spec-epic-1.md#APIs-and-Interfaces]
- **Epic 1 Story 1.3:** [Source: docs/epics/epic-1-foundation-data-architecture.md#Story-1.3]
- **Data Architecture:** [Source: docs/architecture/data-architecture.md]
- **ADR-007:** Three-Tier Data Architecture [Source: docs/architecture/architecture-decision-records-adrs.md]
- **Previous Story:** [Source: docs/sprint-artifacts/1-2-database-schema-models.md]

## Dev Agent Record

### Context Reference

- [Story Context XML](1-3-abstract-data-source-interface.context.xml)

### Agent Model Used

claude-sonnet-4-5-20250929 (Sonnet 4.5)

### Debug Log References

No critical issues encountered during implementation recovery.

### Completion Notes List

**Implementation Recovery (Session after crash):**

1. **Missing Dependencies Fixed**
   - Installed yfinance, alpha-vantage, pyyaml packages
   - Already present in requirements.txt but not installed in environment

2. **Config Validation Issue Fixed** (backend/app/core/config.py:69)
   - Added `extra = "ignore"` to Settings.Config class
   - Allows docker-compose env vars (POSTGRES_USER, REDIS_PASSWORD, etc.) in .env without validation errors

3. **AlphaVantageProvider Rate Limit Bug Fixed** (backend/app/data_sources/providers/alpha_vantage_provider.py:77)
   - Changed `self.daily_limit = daily_limit or self.DEFAULT_DAILY_LIMIT` to `self.daily_limit = daily_limit if daily_limit is not None else self.DEFAULT_DAILY_LIMIT`
   - Previously treated `daily_limit=0` as falsy, incorrectly defaulting to 25
   - Now properly respects `0` as a valid limit for testing

4. **Unit Test Bug Fixed** (tests/unit/test_data_sources.py:267)
   - Removed extra `()` call on mock_provider instantiation
   - Was calling `mock_provider("success", [signal])()` instead of `mock_provider("success", [signal])`

5. **Coverage Configuration Fixed** (pyproject.toml:107, 123)
   - Updated coverage paths from `src` to `backend/app`
   - Added `*/alembic/*` to omit patterns

**Test Results:**
- ✅ Unit Tests: 28/28 passing
- ✅ Integration Tests: 9/9 passing
- ✅ Total: 37/37 passing
- 📊 Coverage: 51% overall (core data sources: 79-96%)

**All Acceptance Criteria Met:**
- AC#1: DataSource ABC with fetch() and get_source_name() ✓
- AC#2: DataSourceRegistry with parallel execution and error isolation ✓
- AC#3: Yahoo & Alpha Vantage providers with failover logic ✓
- AC#4: YAML configuration with env var substitution ✓

### File List

**Files Created:**
- backend/app/data_sources/__init__.py
- backend/app/data_sources/base.py
- backend/app/data_sources/registry.py
- backend/app/data_sources/failover.py
- backend/app/data_sources/providers/__init__.py
- backend/app/data_sources/providers/yahoo_provider.py
- backend/app/data_sources/providers/alpha_vantage_provider.py
- config/data_sources.yaml
- tests/unit/test_data_sources.py
- tests/integration/test_provider_failover.py

**Files Modified:**
- backend/app/core/config.py (added DataSourcesConfig class, fixed validation)
- backend/requirements.txt (added yfinance, alpha-vantage, pyyaml)
- pyproject.toml (fixed coverage paths)
