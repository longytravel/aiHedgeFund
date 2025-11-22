# AIHedgeFund

**AI-Powered Autonomous UK Stock Trading System**

A multi-agent AI system for analyzing UK stocks using discovery agents, signal convergence, and adversarial challenge protocols. Built with Python 3.14, FastAPI, LangGraph, and PostgreSQL 18.1.

---

## 🎯 Project Status

**Phase:** Sprint 0 Complete ✅ - Ready for Epic 1-2 Implementation
**Track:** BMad Method (Brownfield)
**Budget:** £195-230/month (within £200 target)
**Documentation:** [docs/index.md](docs/index.md)

**Quick Links:**
- [Implementation Readiness Report](docs/implementation-readiness-report-2025-11-22.md)
- [Product Requirements (PRD)](docs/prd/index.md)
- [Architecture](docs/architecture/index.md)
- [Epic 1-2 Stories](docs/epics/index.md)

---

## ⚡ Quick Start (<30 Minutes)

### Prerequisites

- **Python 3.14+** ([Download](https://www.python.org/downloads/))
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))
- **Git** ([Download](https://git-scm.com/downloads))

### Setup Steps

```bash
# 1. Clone the repository (or navigate to existing directory)
cd AIHedgeFund

# 2. Configure environment variables
cp .env.example .env
# Edit .env and add your API keys (see API Key Setup section below)

# 3. Build and start all containers (backend, frontend, postgres)
docker-compose build
docker-compose up

# 4. Verify health check endpoint
curl http://localhost:8000/api/health

# 5. Access the frontend
# Open browser to http://localhost:5173

# 6. Access the backend API docs
# Open browser to http://localhost:8000/docs
```

**Setup Time:** ~20-25 minutes (excluding API key registration wait times)

---

## 🔑 API Key Setup (HP-03)

### Required for Development

**Mock Mode (Zero Cost):**
```bash
# In .env
USE_MOCK_LLM=true
```
- Start development immediately with zero costs
- Perfect for Epic 1-2 implementation
- No API keys needed for LLMs

### Required for Production

**1. Data Providers (£125/month total):**

- **EODHD** (£85/month) - Fundamentals, macro data
  - Register: https://eodhd.com/pricing
  - Add `EODHD_API_KEY` to `.env`

- **CityFALCON** (£30/month) - UK RNS, insider trading, sentiment
  - Register: https://www.cityfalcon.com/pricing
  - Add `CITYFALCON_API_KEY` to `.env`

- **IBKR** (£10/month) - Real-time quotes, paper trading
  - Register: https://www.interactivebrokers.com/
  - Add `IBKR_USERNAME`, `IBKR_PASSWORD`, `IBKR_ACCOUNT` to `.env`

**2. LLM Providers (£70-105/month total):**

Start with **free tiers** during development:

- **OpenAI** - https://platform.openai.com/api-keys
  - Add `OPENAI_API_KEY` to `.env`

- **Anthropic** - https://console.anthropic.com/
  - Add `ANTHROPIC_API_KEY` to `.env`

- **Google AI** - https://makersuite.google.com/app/apikey
  - Add `GOOGLE_API_KEY` to `.env`

**Multi-Provider Fallback:**
```bash
# In .env
LLM_PROVIDER=openai
LLM_FALLBACK_PROVIDERS=anthropic,google
```

---

## 🏗️ Architecture Overview

### Technology Stack (2025 Production Versions)

- **Backend:** Python 3.14, FastAPI 0.121.3
- **AI Framework:** LangGraph 1.0.5, LangChain 0.3.13
- **Database:** PostgreSQL 18.1 (3× I/O performance, uuidv7 support)
- **Frontend:** React 19, TypeScript 5, Vite 6 (Epic 5)
- **Cache/Queue:** Redis 7.4
- **Testing:** pytest 8.3.4 with async support

### 20-Agent Network Architecture

**Discovery Layer (Epic 2):**
- 7 Discovery Agents (News Scanner, Insider Trading, Volume/Price, etc.)
- 2-3 Macro/Sector Context Agents

**Analysis Layer (Epic 3):**
- 8 Analysis Agents (Value Investor, Growth Investor, Contrarian, etc.)

**Decision Layer (Epic 3):**
- Risk Manager (adversarial challenger)
- Portfolio Manager (final decisions)

**Processing Model:**
- Overnight batch (1am-7am GMT)
- Signal convergence scoring
- Adversarial challenge protocol

---

## 📁 Project Structure

```
AIHedgeFund/
├── backend/                # Backend Python application
│   ├── app/                # FastAPI application code
│   │   ├── api/            # API endpoints (health check, etc.)
│   │   ├── models/         # SQLAlchemy ORM models (Epic 1)
│   │   ├── services/       # Business logic services (Epic 2-6)
│   │   ├── core/           # Core configuration and database
│   │   └── main.py         # FastAPI entry point
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container definition
├── frontend/               # React 19 frontend application
│   ├── src/                # React source code
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page-level components
│   │   ├── services/       # API client services
│   │   └── main.tsx        # React entry point
│   ├── package.json        # Node dependencies
│   ├── vite.config.ts      # Vite configuration
│   ├── tsconfig.json       # TypeScript configuration
│   ├── index.html          # HTML entry point
│   └── Dockerfile          # Frontend container definition
├── agents/                 # Agent implementations (Epic 2-3)
│   ├── discovery/          # Discovery agents
│   ├── analysis/           # Analysis agents
│   ├── decision/           # Decision agents
│   └── shared/             # Shared agent utilities
├── data/                   # Data folders
│   ├── inbox/              # File drop folders
│   │   ├── ticker-lists/   # CSV ticker uploads
│   │   ├── research-reports/ # PDF/markdown research
│   │   └── manual-stocks/  # JSON stock additions
│   └── processed/          # Processed files archive
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test data fixtures
├── docs/                   # Documentation (PRD, Architecture, Epics)
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── docker-compose.yml      # Multi-container orchestration
└── README.md               # This file
```

---

## 🧪 Testing (HP-01)

### Test Strategy (60/25/15 Split)

```bash
# Run all tests
pytest

# Run unit tests only (fast)
pytest tests/unit/ -m unit

# Run with coverage
pytest --cov=src --cov-report=html

# Run Sprint 0 validation
pytest tests/test_sprint0_validation.py -v

# Run specific test
pytest tests/unit/test_agents/test_news_scanner.py::test_signal_generation
```

### Mock LLM Provider (Zero-Cost Testing)

```python
# tests/conftest.py provides Mock LLM fixtures
async def test_analysis_agent(mock_llm_bullish):
    """Test with bullish mock responses - zero API cost."""
    response = await mock_llm_bullish.generate("Analyze BARC.LSE")
    assert "BULLISH" in response.content
```

**Coverage Target:** 60% minimum (configured in pyproject.toml)

---

## 🚀 Development Workflow

### Epic 1-2 Implementation (Current Phase)

**Epic 1: Foundation & Data Architecture (9 stories)**
- Story 1.1: Project Initialization
- Story 1.2: Database Models
- Story 1.3: EODHD Integration
- Story 1.4: CityFALCON Integration
- Story 1.5: Error Handling & Logging
- Story 1.6: Observability & Monitoring
- Story 1.7: Signal Bus
- Story 1.8: Multi-Provider LLM Abstraction
- Story 1.9: Configuration System

**Epic 2: Discovery & Market Intelligence (12 stories)**
- Story 2.1-2.6: Discovery Agents
- Story 2.7: Agent Orchestration Engine
- Story 2.8: Signal Aggregation
- Story 2.9: Macro Economist Agent
- Story 2.10: Sector Rotation Agent
- Story 2.11: Configuration UI (CLI)
- Story 2.12: Integration Testing

### Story Development Flow

```bash
# 1. Create story context
/bmad:bmm:workflows:story-context

# 2. Implement story
# ... write code, tests, documentation ...

# 3. Mark story as ready for review
/bmad:bmm:workflows:story-ready

# 4. Mark story as done (DoD complete)
/bmad:bmm:workflows:story-done
```

---

## 🔧 Configuration (Epic 2 Story 2.11)

### Configuration-First Design

All agents, thresholds, and schedules are configurable via YAML (no code changes):

```yaml
# config/agents.yaml (Story 2.11)
discovery_agents:
  news_scanner:
    enabled: true
    schedule: "0 * * * *"  # Every hour
    confidence_threshold: 0.7

  insider_trading:
    enabled: true
    schedule: "0 8 * * *"  # 8am daily
    confidence_threshold: 0.9
```

**Benefits:**
- Hot-swap agents without code changes
- A/B test different configurations
- Easy disable/enable for debugging

---

## 📊 Database Management

### Using Docker PostgreSQL 18.1

```bash
# Start database
docker-compose up -d postgres

# View logs
docker-compose logs -f postgres

# Access PostgreSQL CLI
docker exec -it aihedgefund-postgres psql -U aihedgefund

# Stop database
docker-compose down
```

### Using pgAdmin (Optional)

```bash
# Start with pgAdmin UI
docker-compose --profile tools up -d

# Access at: http://localhost:5050
# Email: admin@aihedgefund.local
# Password: devpassword
```

### Database Migrations (Story 1.2)

```bash
# Create migration
alembic revision --autogenerate -m "Add signals table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 📈 Cost Monitoring (Epic 1 Story 1.6)

### Monthly Budget: £200

**Breakdown:**
- Data Providers: £125/month (EODHD £85 + CityFALCON £30 + IBKR £10)
- LLM APIs: £70-105/month (varies by usage)

**Cost Control:**
```bash
# In .env
MONTHLY_BUDGET_GBP=200
LLM_BUDGET_WARNING_THRESHOLD=0.8  # Warn at 80%
ENABLE_COST_TRACKING=true
```

**Development Mode (£0 LLM Cost):**
```bash
USE_MOCK_LLM=true  # Zero-cost testing
```

---

## 🐛 Troubleshooting

### Common Issues

**1. PostgreSQL won't start**
```bash
# Check if port 5432 is in use
docker-compose down
docker-compose up -d
```

**2. Import errors**
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**3. Tests fail**
```bash
# Run Sprint 0 validation
pytest tests/test_sprint0_validation.py -v

# Check if Mock LLM provider works
pytest tests/test_sprint0_validation.py::TestMockLLMProvider -v
```

**4. API keys not working**
```bash
# Verify .env file exists (not .env.template)
# Check for typos in API keys
# Ensure no spaces around = in .env
```

---

## 📚 Documentation

- **[Documentation Index](docs/index.md)** - Central hub for all docs
- **[PRD](docs/prd/index.md)** - Product Requirements Document (9 files, 109KB)
- **[Architecture](docs/architecture/index.md)** - Implementation Architecture (15 files, 59KB)
- **[Epic Breakdown](docs/epics/index.md)** - Epic 1-7 Stories (7 files, 90KB)
- **[Test Design](docs/test-design-system.md)** - Testability assessment
- **[Implementation Readiness](docs/implementation-readiness-report-2025-11-22.md)** - Phase 3 gate check

---

## 🤝 Contributing

### Code Quality Standards

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Run all checks
pre-commit run --all-files
```

### Git Workflow

```bash
# Create feature branch
git checkout -b story/1.1-project-initialization

# Commit changes
git add .
git commit -m "feat: Story 1.1 - Project initialization complete"

# Push branch
git push origin story/1.1-project-initialization
```

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🆘 Support

- **Documentation:** [docs/index.md](docs/index.md)
- **Workflow Status:** Run `/bmad:bmm:workflows:workflow-status`
- **Issues:** Create GitHub issue with error details

---

## ✅ Sprint 0 Completion Checklist

- [x] Project directory structure created
- [x] Python 3.14 environment configured
- [x] Dependencies installed (requirements.txt)
- [x] PostgreSQL 18.1 Docker setup
- [x] Redis cache/queue setup
- [x] pytest framework configured
- [x] Mock LLM provider implemented
- [x] .env.template created
- [x] .gitignore configured (secrets protected)
- [x] README.md with <30 minute setup guide

**Run validation:** `pytest tests/test_sprint0_validation.py -v`

**If all tests pass:** Sprint 0 COMPLETE ✅ - Ready for `/bmad:bmm:workflows:sprint-planning`

---

**Next Steps:**
1. Complete Sprint 0 checklist above
2. Run `/bmad:bmm:workflows:sprint-planning` to create sprint status file
3. Begin Story 1.1: Project Initialization & Structure

---

**Built with BMad Method v6 - AI-Powered Software Development**
