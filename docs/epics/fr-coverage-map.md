# FR Coverage Map

### Phase 1 MVP Coverage

**Epic 1: Foundation & Data Architecture**
- FR-8.1: Backend (FastAPI)
- FR-8.2: Agent Orchestration (LangGraph foundation)
- FR-8.3: LLM Integration (Multi-provider: OpenAI, Anthropic, Google)
- FR-8.4: Database & Persistence
- FR-8.5: Deployment
- FR-5.1: 3-Tier Data Architecture (EODHD initially)
- FR-5.2: Data Integration Implementation (EODHD client)
- FR-5.6: Ad-Hoc Research Inbox (file drop architecture)
- FR-9.1: Plugin Architecture (agent framework)
- FR-9.2: Data Source Modularity (abstract interfaces)
- **NEW:** Multi-Provider LLM Abstraction (OpenAI, Anthropic, Google with fallback)

**Epic 2: Discovery & Market Intelligence**
- FR-1.1: Morning News Scanning
- FR-1.2: Multi-Source Trigger System (4 discovery agents: News, Fundamentals, Insider, Volume)
- FR-1.3: Company/Ticker Mapping
- FR-1.4: Signal Aggregation & Ranking (with sector multipliers)
- FR-1.5: Opportunity Threshold Logic
- FR-3.3: Tier 3 - Research Queue
- **NEW - Macro/Sector Intelligence (moved to MVP):**
  - Macro Economist Agent (weekly UK economic analysis)
  - Sector Rotation Agent (identify favored/disfavored sectors based on macro)
  - Sector multipliers applied to signal scoring (boost favored sectors, penalize risky ones)
  - Track upcoming macro events (budget, BoE meetings, inflation releases)

**Epic 3: Analysis Engine**
- FR-2.1: Multi-Agent LLM Analysis (6 agents: Value, Growth, Quality, Technical, Risk Manager, Portfolio Manager)
- FR-2.2: Agent Orchestration (LangGraph)
- FR-2.3: Risk Management (Risk Manager Agent)
- FR-2.4: Portfolio Management (Portfolio Manager Agent)
- FR-2.5: Existing Position Monitoring
- FR-2.6: Adversarial Challenge Protocol

**Epic 4: Portfolio & Tracking**
- FR-3.1: Tier 1 - Active Portfolio
- FR-3.2: Tier 2 - Active Watchlist (basic manual version)
- FR-7.3: Trade Outcome Tracking

**Epic 5: Reporting & Execution**
- FR-4.1: Daily Morning Report
- FR-4.2: Report Delivery Channels (email + web)
- FR-4.3: On-Demand Reporting (basic)
- FR-7.1: Web Dashboard (React Frontend - basic)
- FR-7.2: Manual Trade Execution & Logging
- FR-12.1: Manual Approval Workflow

**Epic 6: Automation & Reliability**
- FR-6.1: Batch Processing (overnight scheduling)
- FR-6.2: System Reliability (error handling, retry logic)
- FR-6.3: Cost Monitoring
- FR-6.4: Scheduling Flexibility (configurable schedule)
- FR-5.3: Data Caching (basic)
- FR-5.4: Data Validation & Quality Checks (basic)
- FR-5.5: Audit Trail
- FR-5.7: Fallback & Error Handling

**Epic 7: Configurability & Enhancement**
- FR-2.7.1: Agent Enable/Disable (via config file)
- FR-2.7.2: Agent Weighting & Influence (via config file)
- FR-2.7.5: Agent Configuration Persistence
- FR-2.7.6: Discovery Agent Configurability
- FR-5.2: Data Integration Implementation (add CityFALCON for insider trading)
- FR-9.3: Strategy Framework (config templates)
- FR-9.4: API for External Integrations (basic)
- FR-10.1: Manual Full Discovery Scan
- FR-10.2: Custom Ticker List Analysis
- FR-10.3: Portfolio Re-Evaluation On-Demand
- FR-11.1: Market Cap Filters
- FR-11.2: Sector & Industry Focus
- FR-11.3: Custom Ticker Lists
- FR-11.5: Price Range & Liquidity Filters
- FR-12.2: Paper Trading / Simulation Mode
- FR-12.6: Dry-Run / Test Mode

### Phase 2+ Coverage (Deferred)

**Epic 8: Advanced Tracking**
- FR-3.2: Tier 2 - Active Watchlist (automated triggers & re-validation)
- FR-10.4: Event-Driven Triggers

**Epic 9: Multi-Portfolio Management**
- FR-13.1: Multiple Portfolio Support
- FR-13.2: Portfolio-Specific Strategies
- FR-13.3: Portfolio-Specific Risk Parameters
- FR-13.5: Consolidated & Individual Reporting

**Epic 10: Advanced Alerting**
- FR-14.1: Custom Alert Triggers
- FR-14.2: Multi-Channel Alert Delivery
- FR-14.3: Alert Urgency Levels & Frequency
- FR-14.4: Alert Filters & Quiet Hours
- FR-14.5: Alert Grouping & Digest

**Epic 11: Historical Backtesting**
- FR-15.1: Historical Backtesting
- FR-15.2: Point-In-Time Analysis
- FR-15.3: Configuration A/B Testing
- FR-15.4: Stress Testing
- FR-15.5: Performance Attribution Historical
- FR-15.6: Walk-Forward Validation
- FR-10.5: Historical Backfill Analysis

**Advanced Features (Phase 2+)**
- FR-2.7.3: Custom Agent Integration (UI for custom agents)
- FR-2.7.4: Agent Performance Tracking (dashboard)
- FR-9.1: Plugin Architecture (UI and marketplace)
- FR-11.4: ESG & Ethical Filters
- FR-11.6: Geography & Asset Class Expansion
- FR-12.3: Read-Only / Educational Mode
- FR-12.4: Auto-Execution Mode
- FR-12.5: Collaborative / Multi-User Approval
- FR-13.4: Cross-Portfolio Tax Optimization

### Non-Functional Requirements Coverage

All epics incorporate relevant NFRs:
- **Security** (NFR-S*): API key management, data protection, audit logging
- **Performance** (NFR-P*): Response times, data freshness, cost optimization
- **Reliability** (NFR-R*): Error handling, backup, monitoring
- **Maintainability** (NFR-M*): Code quality, configuration management, documentation
- **Usability** (NFR-U*): Report clarity, intuitive workflows

---
