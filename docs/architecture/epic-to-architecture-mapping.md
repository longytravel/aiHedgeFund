# Epic to Architecture Mapping

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
