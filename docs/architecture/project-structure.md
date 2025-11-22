# Project Structure

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
