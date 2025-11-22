# Decision Summary

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
