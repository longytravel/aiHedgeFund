# System-Level Test Design - AIHedgeFund

**Project**: AIHedgeFund - Autonomous Multi-Agent AI Trading System
**Phase**: Phase 3 Solutioning - Testability Review
**Generated**: 2025-11-22
**Scope**: Epics 1-2 (Foundation & Discovery layers)
**Mode**: System-Level (pre-implementation-readiness gate check)

---

## Executive Summary

AIHedgeFund's architecture is **TESTABLE** with proper test infrastructure and patterns. The multi-agent distributed system poses interesting testability challenges (signal convergence edge cases, LangGraph state management, time-based decay logic), but the architectural decisions support testability:

- ✅ **Controllability**: Abstract interfaces (DataSource, LLMProvider), dependency injection, mock mode for LLMs
- ✅ **Observability**: Comprehensive structured logging, signal tracing, agent performance metrics
- ✅ **Reliability**: Graceful degradation (data provider fallback), retry logic, error handling per agent

**Recommendation**: **PASS with CONCERNS** - Ready for implementation with testability recommendations below.

---

## 1. Testability Assessment

### 1.1 Controllability: ✅ PASS with CONCERNS

**Can we control system state for testing?**

✅ **PASS**:
- **API Seeding**: FastAPI + SQLAlchemy ORM supports programmatic data seeding (Epic 1.2: database schema)
- **External Dependencies Mockable**:
  - Multi-provider LLM abstraction (Epic 1.8) allows mock LLM mode (£0 testing cost)
  - Abstract DataSource interface (Epic 1.3) allows mock data providers
  - File inbox system (Epic 1.5, 1.6) can use test fixtures instead of real files
- **Database Reset**: PostgreSQL with test schemas for isolation
- **Configuration Injection**: Extensive YAML configuration allows test-specific config files

⚠️ **CONCERNS**:
1. **LangGraph State Management**: 20-agent distributed network needs deterministic state snapshots for testing
   - **Recommendation**: Implement state serialization/deserialization for test fixtures
   - **Owner**: Backend team
   - **Priority**: P1 (required for reliable E2E tests)

2. **Agent Timeout Control**: 120-second timeout per agent mentioned but no test validation pattern
   - **Recommendation**: Configurable timeouts via environment vars for tests (reduce to 5s in tests)
   - **Owner**: Backend team
   - **Priority**: P2 (speeds up test execution)

3. **Time-Based Logic**: Signal decay by days, CRON scheduling, overnight batch processing
   - **Recommendation**: Use `freezegun` library for time mocking, inject clock interface
   - **Owner**: Backend team
   - **Priority**: P1 (critical for testing decay calculations)

---

### 1.2 Observability: ✅ PASS

**Can we inspect system state and validate NFRs?**

✅ **PASS**:
- **Structured Logging**: Epic 1.9 implements comprehensive JSON logging with correlation IDs
- **Signal Tracing**: "Show all signals for VOD.L" query capability enables root cause analysis
- **Agent Performance Metrics**: Execution time, LLM cost, success rate tracked per agent
- **Cost Tracking**: Every LLM call logged with token usage and cost (enables budget validation)
- **Health Check**: `/api/health` endpoint (NFR-R4) for service monitoring
- **Workflow State Persistence**: LangGraph workflow runs stored in database for post-mortem

**Testing Leverage**:
- Tests can assert on log output (e.g., "verify password never appears in logs")
- Signal tracing enables E2E test validation ("why did stock X score 85?")
- Performance metrics enable load test baselines (p95 latency, throughput)

**No Concerns** - Observability exceeds typical standards for greenfield projects.

---

### 1.3 Reliability: ✅ PASS with CONCERNS

**Are tests isolated, failures reproducible, components loosely coupled?**

✅ **PASS**:
- **Graceful Degradation**: EODHD failure → Yahoo Finance fallback (Epic 1.3: DataSource abstraction)
- **Retry Logic**: 3 attempts with exponential backoff for failed API calls (NFR-R2)
- **Error Handling Per Agent**: One agent failure doesn't crash workflow (Epic 1.7: LangGraph error handling)
- **Loose Coupling**: Agents communicate via StateGraph only (Epic 1.7: no direct dependencies)
- **Parallel-Safe**: Discovery agents run in parallel without shared mutable state

⚠️ **CONCERNS**:
1. **No Explicit Circuit Breaker**: Architecture mentions error handling but not circuit breaking
   - **Recommendation**: Add circuit breaker for external APIs (EODHD, LLMs) to prevent cascading failures
   - **Owner**: Backend team
   - **Priority**: P2 (nice-to-have, graceful degradation already present)

2. **Partial Agent Failure Isolation**: Workflow continues with other agents, but what if 5/7 discovery agents fail?
   - **Recommendation**: Define minimum viable agent thresholds (e.g., "fail workflow if <3 discovery agents succeed")
   - **Owner**: Backend team
   - **Priority**: P1 (prevents garbage-in-garbage-out scenarios)

3. **Test Data Cleanup**: No explicit cleanup discipline mentioned
   - **Recommendation**: Implement pytest fixtures with auto-cleanup (yield pattern)
   - **Owner**: QA team
   - **Priority**: P1 (prevents test pollution)

---

## 2. Architecturally Significant Requirements (ASRs)

ASRs are quality requirements that drive architecture decisions and pose testability challenges. Scored using **Probability (1-3) × Impact (1-3) = Risk Score (1-9)**.

### High-Risk ASRs (Score ≥6)

| ASR ID | Category | Description | Probability | Impact | Score | Testing Approach |
|--------|----------|-------------|-------------|--------|-------|------------------|
| ASR-01 | PERF | Overnight processing must complete in ≤6 hours (NFR-P1) | 2 | 3 | **6** | Pytest timing markers, k6 load tests for API throughput |
| ASR-02 | OPS | 99%+ overnight processing success rate (NFR-R1) | 2 | 3 | **6** | E2E batch workflow tests with failure injection |

### Medium-Risk ASRs (Score 4-5)

| ASR ID | Category | Description | Probability | Impact | Score | Testing Approach |
|--------|----------|-------------|-------------|--------|-------|------------------|
| ASR-03 | PERF | Total monthly cost ≤ £200 (NFR-P4) | 2 | 2 | **4** | Cost tracking tests, budget circuit breakers |
| ASR-04 | OPS | Configuration changes without code modifications (NFR-M2) | 2 | 2 | **4** | Pydantic schema validation, config integration tests |
| ASR-05 | DATA | Support 600 stocks, 2 years history (NFR-SC1) | 2 | 2 | **4** | Load data volume tests, query performance benchmarks |
| ASR-06 | SEC | API keys stored in env vars, never in code (NFR-S1) | 1 | 3 | **3** | Secret scanning tests, log output validation |

**Testability Impact**: ASR-01 and ASR-02 drive performance testing requirements (k6 load tests, batch timing validation). ASR-04 drives configuration validation testing.

---

## 3. Test Levels Strategy

Based on architecture (Python backend with complex business logic, React frontend, LangGraph multi-agent orchestration, batch processing):

### Recommended Split: **60% Unit / 25% Integration / 15% E2E**

**Rationale**:
- **High complexity** in agent logic, signal scoring algorithms, decay calculations → **Unit tests**
- **Critical data flows** between discovery agents, aggregation, and decision layers → **Integration tests**
- **Batch workflows** and morning report generation → **E2E tests**

### Test Level Breakdown by Component

| Component | Unit | Integration | E2E | Rationale |
|-----------|------|-------------|-----|-----------|
| **Agent Logic** (LLM prompts, response parsing) | 80% | 20% | - | Pure logic + LLM interaction tests |
| **Signal Aggregation** (decay, scoring, convergence) | 70% | 30% | - | Complex math (unit) + data flow (integration) |
| **Database Layer** (models, queries, migrations) | - | 100% | - | Persistence logic requires DB |
| **API Endpoints** (FastAPI routes) | - | 60% | 40% | Contract tests (int) + workflows (E2E) |
| **Configuration System** (YAML validation) | 50% | 50% | - | Schema validation (unit) + loading (integration) |
| **Batch Workflows** (overnight discovery) | - | - | 100% | Full orchestration requires E2E |
| **File Inbox** (CSV/JSON parsing) | 60% | 40% | - | Parse logic (unit) + file I/O (integration) |

### Test Level Selection Examples

**✅ Unit Test**: Signal decay calculation
```python
def test_signal_decay_linear():
    score = calculate_decay(
        base_score=80,
        days_old=30,
        decay_rate="slow",  # 90 days to zero
        formula="linear"
    )
    assert score == 53  # 80 × (1 - 30/90) ≈ 53
```

**✅ Integration Test**: Discovery agent → database signal storage
```python
async def test_news_scanner_stores_signals(db_session):
    agent = NewsScanner(llm_provider=mock_llm)
    await agent.run(ticker="VOD.L")

    signals = db_session.query(Signal).filter_by(ticker="VOD.L").all()
    assert len(signals) == 1
    assert signals[0].signal_type == "NEWS_CATALYST"
```

**✅ E2E Test**: Complete overnight batch workflow
```python
async def test_overnight_discovery_batch(api_client):
    response = await api_client.post("/api/workflows/discovery-batch")
    assert response.status_code == 200

    # Wait for completion (mock time passage)
    await asyncio.sleep(5)  # In real scenario: poll status

    # Validate top stocks identified
    top_stocks = await api_client.get("/api/signals/top-stocks")
    assert len(top_stocks.json()) == 15  # Top 15 for deep analysis
    assert top_stocks.json()[0]["score"] >= 61  # Deep analysis threshold
```

---

## 4. NFR Testing Approach

### 4.1 Security: ⚠️ CONCERNS

**Validation Method**: Playwright E2E + pytest security tests

**Test Coverage**:
- ✅ **Secret Handling**:
  - Test: Verify API keys read from env vars, never hardcoded
  - Test: Verify passwords/API keys never logged (check log output)
  - Test: Verify `.env` excluded from git (`git ls-files .env` returns nothing)
- ✅ **API Authentication**:
  - Test: Unauthenticated requests to `/api/*` endpoints return 401 or redirect
  - (Phase 1 MVP: single-user local, no auth - deferred to Phase 2)
- ✅ **Input Validation**:
  - Test: SQL injection in search endpoint blocked (Pydantic validation)
  - Test: XSS in user input sanitized

**⚠️ Concerns**:
1. **No OWASP Validation Mentioned**: Architecture doesn't explicitly address OWASP Top 10
   - **Recommendation**: Add OWASP dependency check (Bandit for Python, npm audit for frontend)
   - **Owner**: Security team / Backend team
   - **Priority**: P1 (critical for Phase 2 multi-user)

2. **LLM Prompt Injection**: No mention of LLM prompt injection defenses
   - **Recommendation**: Test that user input can't manipulate agent prompts
   - **Owner**: Backend team
   - **Priority**: P2 (risk if user-provided stock tickers contain injection payloads)

**Status**: ⚠️ **CONCERNS** - Good foundation (env vars, input validation), but need OWASP hardening

---

### 4.2 Performance: ⚠️ CONCERNS

**Validation Method**: k6 load testing + pytest timing assertions

**SLO/SLA Targets** (from NFR-P1, NFR-P2):
- Overnight batch: ≤6 hours for 600 stocks
- Parallel agent execution: <3 min per stock
- API response time: ≤500ms for data retrieval endpoints
- Signal aggregation: <2 min for 600 stocks

**Test Approach**:
```javascript
// k6 load test for API endpoints
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    errors: ['rate<0.01'],             // <1% error rate
  },
  stages: [
    { duration: '1m', target: 10 },   // Ramp up
    { duration: '5m', target: 10 },   // Sustained load
  ],
};
```

```python
# pytest timing assertion for batch processing
@pytest.mark.timeout(120)  # 2-hour max for test
async def test_discovery_batch_completes_in_time():
    start = time.time()
    await run_discovery_batch(stock_count=100)  # FTSE 100 subset
    duration = time.time() - start
    assert duration < 600  # <10 min for 100 stocks (scales to <2h for 600)
```

**⚠️ Concerns**:
1. **No Load Testing Baseline**: k6 not mentioned in architecture or Epic 1
   - **Recommendation**: Establish performance baselines before implementation (Sprint 0)
   - **Owner**: QA team
   - **Priority**: P1 (need baselines for regression detection)

2. **LLM API Throughput Unknowns**: OpenAI/Anthropic rate limits not addressed
   - **Recommendation**: Test rate limit handling (429 response → exponential backoff)
   - **Owner**: Backend team
   - **Priority**: P1 (production blocker if rate-limited)

**Status**: ⚠️ **CONCERNS** - Performance targets well-defined, but testing infrastructure missing

---

### 4.3 Reliability: ✅ PASS with CONCERNS

**Validation Method**: Pytest with mocking + E2E failure injection

**Test Coverage**:
- ✅ **Graceful Degradation**:
  - Test: EODHD API failure → Yahoo Finance fallback succeeds
  - Test: All data providers down → system uses cache, flags staleness
- ✅ **Retry Logic**:
  - Test: Failed API call retries 3x with exponential backoff
  - Test: Transient LLM error (503) → retry succeeds
- ✅ **Error Handling**:
  - Test: One discovery agent failure → workflow continues with others
  - Test: Database connection lost → health check returns 503
- ✅ **Health Checks**:
  - Test: `/api/health` returns 200 with database/cache status

**Test Example**:
```python
@pytest.mark.asyncio
async def test_data_provider_fallback(mock_eodhd_failure):
    # Arrange: Mock EODHD API failure
    mock_eodhd_failure.return_value = None

    # Act: Fetch stock data
    data = await fetch_stock_data(ticker="VOD.L")

    # Assert: Yahoo Finance fallback succeeded
    assert data is not None
    assert data.source == "yahoo_finance"
    assert "Data source: Yahoo Finance (EODHD unavailable)" in logs
```

**⚠️ Concerns**:
1. **No Circuit Breaker Testing**: Architecture mentions retries but not circuit breaking
   - **Recommendation**: Add circuit breaker tests (open after 5 failures, half-open after timeout)
   - **Owner**: Backend team
   - **Priority**: P2 (nice-to-have, graceful degradation already present)

2. **Partial Agent Failure Thresholds Undefined**: What if 5/7 discovery agents fail?
   - **Recommendation**: Define minimum viable agents (e.g., "≥3 discovery agents must succeed")
   - **Owner**: Product team (define business rule)
   - **Priority**: P1 (prevents garbage recommendations)

**Status**: ✅ **PASS with CONCERNS** - Good resilience patterns, need circuit breaker validation

---

### 4.4 Maintainability: ✅ PASS

**Validation Method**: CI tools (pytest-cov, ruff, mypy)

**Test Coverage**:
- ✅ **Code Coverage**: ≥70% target (NFR-M1) validated via pytest-cov
- ✅ **Type Hints**: Python 3.10+ typing enforced via mypy
- ✅ **Code Quality**: PEP 8 via ruff/black, linting in CI
- ✅ **Mock LLM Mode**: Epic 1.8 provides £0-cost testing infrastructure
- ✅ **Structured Logging**: Epic 1.9 enables test log assertions

**CI Pipeline**:
```yaml
# .github/workflows/test.yml
test:
  steps:
    - name: Run tests with coverage
      run: pytest --cov=src --cov-report=term --cov-fail-under=70

    - name: Type checking
      run: mypy src/

    - name: Linting
      run: ruff check src/
```

**No Concerns** - Maintainability is well-addressed in NFR-M1 and Epic 1.

**Status**: ✅ **PASS**

---

## 5. Test Environment Requirements

Based on deployment architecture (Docker Compose for MVP, cloud for Phase 2):

### Local Development Environment
- **Infrastructure**: Docker Compose with PostgreSQL 18.1, FastAPI, React dev server
- **LLMs**: Mock mode (£0 cost) via Epic 1.8 fixtures
- **Data**: Mock data providers (no EODHD API costs)
- **Database**: Test schema with auto-reset between tests
- **Time**: `freezegun` for time mocking (signal decay, CRON tests)

### CI/CD Environment (GitHub Actions)
- **Infrastructure**: PostgreSQL service container, Python 3.14, Node.js for frontend
- **Tests**: pytest with coverage, ruff, mypy, Playwright component tests
- **LLMs**: Mock mode by default, manual trigger for real LLM smoke tests (weekly)
- **Performance**: k6 for weekly performance baselines (not every commit)
- **Cost**: £0 per commit (mocks), ~£5/week for smoke tests with real LLMs

### Staging Environment
- **Infrastructure**: Docker Compose on VPS or cloud (DigitalOcean, AWS)
- **LLMs**: Real API keys with cost alerts (£10/day budget)
- **Data**: Test EODHD API key with limited quota
- **Scope**: 100 FTSE stocks (vs 600 production) for cost control
- **Purpose**: Integration testing, user acceptance testing

---

## 6. Testability Concerns

### 🟡 Concerns (Not Blockers, Require Attention)

| ID | Concern | Impact | Recommendation | Owner | Priority |
|----|---------|--------|----------------|-------|----------|
| TC-01 | **LangGraph State Management**: 20-agent distributed network needs deterministic state snapshots | Medium | Implement state serialization for test fixtures | Backend | P1 |
| TC-02 | **Signal Convergence Edge Cases**: Complex scoring with decay rates, multipliers, bonuses | Medium | Property-based testing (Hypothesis library) for score calculations | Backend | P1 |
| TC-03 | **Configuration Validation**: Extensive YAML config could cause runtime errors | Medium | Pydantic schema validation + integration tests | Backend | P1 |
| TC-04 | **Cost Control in Tests**: Real LLMs = £50+/day testing cost | High | Mock LLM mode (already planned), weekly smoke tests with real LLMs | QA | P0 |
| TC-05 | **Time-Based Logic**: Signal decay by days, CRON triggers hard to test | Medium | Freezegun for time mocking, configurable clock injection | Backend | P1 |
| TC-06 | **File Inbox Edge Cases**: CSV/JSON parsing with various formats/encodings | Low | Comprehensive file parsing test suite with malformed fixtures | Backend | P2 |
| TC-07 | **Partial Agent Failure Isolation**: Minimum viable agents threshold undefined | Medium | Define business rules (e.g., "≥3 discovery agents must succeed") | Product | P1 |
| TC-08 | **LLM Prompt Injection**: User input could manipulate agent prompts | Medium | Test that ticker input can't inject prompt commands | Backend | P2 |
| TC-09 | **Load Testing Infrastructure**: No k6 or performance baseline mentioned | High | Establish performance baselines in Sprint 0 | QA | P1 |
| TC-10 | **Circuit Breaker Pattern**: Retries present but not circuit breaking | Low | Add circuit breaker tests (open after 5 failures) | Backend | P2 |

### ✅ No Critical Blockers Identified

The architecture is **testable** with proper test infrastructure. All concerns are addressable during Sprint 0 (test framework setup) or early implementation.

---

## 7. Recommendations for Sprint 0

Before beginning Epic 1 development, establish these testing foundations:

### Phase 0: Test Framework Setup (1-2 days)

1. **Pytest Configuration**:
   - Configure `pytest.ini` with markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e`)
   - Set up pytest-cov with 70% threshold
   - Configure pytest-asyncio for async test support

2. **Mock Infrastructure**:
   - Implement Mock LLM Provider (Epic 1.8) with fixtures
   - Create data provider mocks (EODHD, Yahoo Finance)
   - Set up test database fixtures with auto-cleanup

3. **Time Mocking**:
   - Integrate `freezegun` for signal decay tests
   - Create time injection patterns for CRON-triggered workflows

4. **Performance Baselines**:
   - Write k6 scripts for API endpoints
   - Establish baseline: p95 latency, throughput, error rate
   - Run weekly (not per commit) to track regression

5. **CI Pipeline**:
   - GitHub Actions workflow with pytest, ruff, mypy
   - Coverage report publishing (Codecov or similar)
   - Manual trigger for real LLM smoke tests

### Phase 1: Property-Based Testing (Epic 1 stories)

Implement property-based tests for critical algorithms:

```python
from hypothesis import given, strategies as st

@given(
    base_score=st.integers(min_value=0, max_value=100),
    days_old=st.integers(min_value=0, max_value=365),
)
def test_signal_decay_never_negative(base_score, days_old):
    """Property: Decayed score is always ≥0 and ≤ base_score"""
    result = calculate_decay(base_score, days_old, "linear", 90)
    assert 0 <= result <= base_score
```

---

## 8. Quality Gate Criteria

Before **Implementation Readiness** gate (Phase 3 → Phase 4):

- [ ] **Test Framework Complete**: Pytest, mocks, CI pipeline operational
- [ ] **Performance Baselines Established**: k6 scripts with SLO/SLA thresholds
- [ ] **Security Tests Drafted**: Secret handling, input validation, OWASP checks
- [ ] **Reliability Tests Drafted**: Graceful degradation, retry logic, health checks
- [ ] **Mock LLM Mode Validated**: Fixtures match real LLM behavior (spot-check with weekly smoke tests)
- [ ] **Configuration Validation**: Pydantic schemas enforce all config constraints
- [ ] **Time Mocking Patterns**: Freezegun integrated for decay/scheduling tests
- [ ] **Test Coverage Target Met**: ≥70% for Epic 1 stories (unit + integration)

---

## 9. Test Execution Strategy

### Test Pyramid Target Distribution

```
       /\
      /E2\      15% E2E (Batch workflows, critical user journeys)
     /----\
    / INT  \    25% Integration (Data flows, API contracts, DB operations)
   /--------\
  /   UNIT   \  60% Unit (Agent logic, scoring algorithms, pure functions)
 /------------\
```

### Execution Frequency

| Level | When | Duration | Cost | Coverage |
|-------|------|----------|------|----------|
| **Unit** | Every commit | <30s | £0 (mocks) | 60% codebase |
| **Integration** | Every commit | <2min | £0 (mocks) | 25% codebase |
| **E2E** | PR to main | <10min | £0 (mocks) | 15% codebase |
| **Performance (k6)** | Weekly | <5min | £0 (local) | SLO/SLA validation |
| **Smoke (Real LLMs)** | Weekly (manual) | <15min | ~£5 | Critical paths only |

### Selective Execution (Epic 2+)

Use pytest markers for selective execution:

```bash
# Run only fast tests (unit + integration)
pytest -m "unit or integration"

# Run only E2E tests
pytest -m e2e

# Run only tests for Epic 1
pytest -m epic1

# Run tests affected by signal scoring changes
pytest tests/unit/signal_scoring/ tests/integration/aggregation/
```

---

## 10. Next Steps

### Immediate Actions (Before Epic 1 Implementation)

1. **Backend Team**:
   - [ ] Set up pytest with coverage, asyncio, mocking
   - [ ] Implement Mock LLM Provider with fixtures (Epic 1.8 guidance)
   - [ ] Create `freezegun` integration for time-based tests
   - [ ] Add Pydantic schema validation for all config files

2. **QA Team**:
   - [ ] Write k6 scripts for API performance baselines
   - [ ] Create test data factories for database seeding
   - [ ] Draft security test suite (secret handling, input validation)
   - [ ] Set up CI pipeline (GitHub Actions with pytest, coverage reporting)

3. **Product Team**:
   - [ ] Define minimum viable agent thresholds (TC-07)
   - [ ] Clarify performance targets for load testing (NFR-P1 specifics)

### Phase 2 Enhancements (Post-MVP)

- Add Playwright E2E tests for React frontend (Phase 2 when UI delivered)
- Implement chaos engineering for distributed agent resilience
- Add mutation testing (mutmut) to validate test quality
- Performance monitoring dashboard (Grafana + Prometheus)

---

## Appendix A: Tool Selection Summary

| NFR Category | Tool | Purpose | When |
|--------------|------|---------|------|
| **Security** | pytest | Secret handling, input validation tests | Every commit |
| **Security** | Bandit | Static analysis for Python security issues | Every commit |
| **Security** | OWASP ZAP | API security scanning | Weekly (Phase 2) |
| **Performance** | k6 | Load testing, SLO/SLA validation | Weekly |
| **Performance** | pytest-benchmark | Micro-benchmarks for algorithms | On-demand |
| **Reliability** | pytest | Error handling, retry logic, graceful degradation | Every commit |
| **Reliability** | Chaos Toolkit | Distributed system resilience (Phase 2) | On-demand |
| **Maintainability** | pytest-cov | Code coverage reporting | Every commit |
| **Maintainability** | mypy | Type checking | Every commit |
| **Maintainability** | ruff | Linting, code quality | Every commit |

---

## Appendix B: Risk Summary

### High-Risk Areas Requiring Test Focus

1. **Signal Convergence Logic** (Epic 2.6, 2.10):
   - Complex math: decay × macro × sector × convergence bonuses
   - **Test Approach**: Property-based testing, edge case fixtures

2. **LangGraph Agent Orchestration** (Epic 1.7, 2.12):
   - 20-agent parallel execution with state management
   - **Test Approach**: Deterministic state snapshots, partial failure injection

3. **Overnight Batch Performance** (Epic 2.12):
   - 6-hour window for 600 stocks × 7 discovery agents
   - **Test Approach**: Scaled-down tests (100 stocks), k6 load baselines, timing assertions

4. **Configuration Management** (Epic 2.11):
   - Extensive YAML config with enable/disable, thresholds, schedules
   - **Test Approach**: Pydantic validation, malformed config fixtures, integration tests

5. **Cost Control** (Epic 1.8):
   - £200/month budget with 20 agents × 15 stocks/day × real LLMs
   - **Test Approach**: Mock LLM mode (£0), cost tracking assertions, budget circuit breakers

---

**Document Status**: Ready for implementation-readiness gate review
**Next Workflow**: *create-epics-and-stories-final* (PM agent) → *implementation-readiness* (Architect agent)
**Test Framework Readiness**: Recommendations complete, Sprint 0 tasks defined

---

_Generated by: Murat (Master Test Architect)_
_Framework: System-Level Testability Review (Phase 3 - Solutioning)_
