# Architecture Decision Records (ADRs)

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
