# Non-Functional Requirements

### Performance

**NFR-P1: Report Delivery Time (Configurable)**
- Report SHALL be delivered at user-configured time 95%+ of scheduled runs (default: 7:00 AM GMT)
- Total batch processing time ≤ 6 hours (adjusts based on configured start time)
- Parallel agent execution: All enabled analysis agents SHALL complete analysis of single stock in < 3 minutes

**NFR-P2: Response Times (Web UI)**
- Page load time ≤ 2 seconds for dashboard views
- On-demand stock analysis results in ≤ 30 seconds (LLM processing time)
- API response time ≤ 500ms for data retrieval endpoints (cached data)

**NFR-P3: Data Freshness**
- Price data: End-of-day prices available by 6:00 PM GMT (LSE closes 4:30 PM)
- News data: Fetched from morning 6:00-9:00 AM window (pre-market)
- Portfolio P&L updates: Real-time during trading hours (8:00 AM - 4:30 PM GMT)

**NFR-P4: Cost Performance**
- Phase 1: Total monthly operating cost ≤ £200 (LLM + data APIs + infrastructure)
- LLM token efficiency: Avg cost per analyzed stock ≤ £0.20 (using GPT-4o)
- API call optimization: 90%+ cache hit rate for repeated data requests

### Security

**NFR-S1: API Key Management**
- All API keys (LLM, data providers, broker) stored in environment variables, NEVER in code
- Secrets encrypted at rest (use system keyring or cloud secret manager)
- API keys rotated quarterly (manual process Phase 1, automated Phase 3)

**NFR-S2: Data Protection**
- Portfolio data, trade history, and agent decisions stored locally or in private cloud
- Database encrypted at rest (AES-256 encryption)
- No sensitive financial data logged in plain text

**NFR-S3: Authentication & Authorization** (Phase 1: Basic, Phase 3: Advanced)
- Web UI: Password-protected (Phase 1), OAuth 2.0 (Phase 3)
- API endpoints: API key authentication for programmatic access
- Role-based access control (RBAC) for multi-user scenarios (Phase 3)

**NFR-S4: Audit Logging**
- All user actions logged with timestamps (trade approvals, rejections, settings changes)
- Logs retained for 2 years minimum
- Logs include: User ID, action type, affected data, timestamp, IP address
- No PII (personally identifiable information) in logs beyond user ID

**NFR-S5: Compliance Readiness**
- Audit trail supports potential FCA regulatory review (Phase 3)
- GDPR compliance: User data deletion capability, data export functionality
- Market Abuse Regulation (MAR): Document that all data sources are public information

### Reliability & Availability

**NFR-R1: System Uptime**
- Target availability: 95%+ during UK trading hours (8:00 AM - 4:30 PM GMT, Monday-Friday)
- Overnight processing: 99%+ success rate (critical for morning report delivery)
- Acceptable downtime: < 2 hours/month for planned maintenance (scheduled outside market hours)

**NFR-R2: Error Handling & Recovery**
- Graceful degradation: If data API unavailable, use cached data and flag in report
- Retry logic: Failed API calls retry 3x with exponential backoff (1s, 3s, 9s delays)
- Email alerts: Notify user immediately if overnight processing fails or morning report not delivered

**NFR-R3: Data Backup**
- Database backed up daily (automated)
- Backup retention: 30 days rolling (local), 90 days (cloud storage)
- Recovery Time Objective (RTO): < 4 hours (restore from backup before next trading day)
- Recovery Point Objective (RPO): < 24 hours (max data loss = 1 day)

**NFR-R4: Monitoring & Alerting**
- Monitor key metrics: API response times, LLM token usage, database size, disk space
- Alerts for: Failed overnight jobs, API quota exhaustion, disk space < 10%, database errors
- Health check endpoint: `/api/health` returns system status

### Scalability

**NFR-SC1: Data Volume Growth**
- System SHALL support analysis of 600+ UK stocks (FTSE All-Share) without performance degradation
- Database SHALL handle 2+ years of trade history (est. 500-1000 trades)
- Audit log storage: Support 100,000+ agent decisions logged

**NFR-SC2: Computational Scalability** (Phase 2-3)
- System SHALL scale to analyze 50+ stocks/day in deep analysis mode (vs. 10-15 in Phase 1)
- Horizontal scaling: Support distributed LLM processing (multiple API keys, load balancing)
- Cache scaling: Redis or distributed cache for multi-instance deployments

**NFR-SC3: User Scalability** (Phase 3 only)
- Support 1-100 concurrent users for signal service platform
- Multi-tenancy: Isolate portfolio data per user
- Rate limiting: Max 10 on-demand analyses per user per day (prevent abuse)

### Maintainability

**NFR-M1: Code Quality**
- Python code follows PEP 8 style guide
- Type hints for all function signatures (Python 3.10+ typing)
- Unit test coverage: > 70% for core business logic (agent orchestration, signal aggregation)
- Integration tests for critical workflows (morning scan end-to-end)

**NFR-M2: Configuration Management & Modularity**
- All environment-specific settings in config files or environment variables
- No hardcoded values for: API endpoints, thresholds, agent selection, data sources, schedules, timezones
- **Agent configuration externalized:** No code changes required to add/remove/configure agents
- **User-configurable parameters via web UI:**
  - Scheduling (execution times, days, timezone, pause mode)
  - Agent selection (enable/disable, weighting, custom agents)
  - Strategy templates (quick-switch presets)
  - Discovery scope (market cap, sectors, custom lists, ESG filters)
  - Risk settings (position size, stop-loss %, exposure limits)
  - Cost budgets and circuit breakers
  - Report delivery (channels, formats, timing, detail levels)
  - Alert configuration (triggers, channels, urgency, quiet hours)
- **Configuration validation:** System SHALL validate config changes before applying (prevent breaking changes)
- **Configuration versioning:** Track config history, rollback capability, export/import
- **Hot reload where possible:** Config changes take effect without full system restart (exception: structural changes like new agent classes)

**NFR-M3: Logging & Debugging**
- Structured logging (JSON format) for easy parsing
- Log levels: DEBUG (development), INFO (production), ERROR (always)
- Correlation IDs: Track request flow through system (e.g., morning scan ID traces all agents)

**NFR-M4: Documentation**
- README with setup instructions, environment variables, deployment steps
- API documentation: OpenAPI/Swagger spec for all backend endpoints
- Agent design docs: Each agent's philosophy, prompts, example outputs
- Runbooks: Common issues and resolutions (API quota exceeded, LLM errors, etc.)

**NFR-M5: Extensibility & Plugin Architecture**
- **Agent Plugin Interface:** Well-documented interface for adding custom agents
- **Minimal coupling:** Agents SHALL NOT directly depend on each other (communicate via state graph only)
- **Dependency injection:** Core system components (data sources, LLM providers, schedulers) injectable, not hardcoded
- **Versioning support:** Agents SHALL declare version compatibility (prevent breaking changes during upgrades)
- **Sandbox execution:** Custom agents run in controlled environment (resource limits, timeout protection, error isolation)
- **Documentation for extensibility:**
  - Agent developer guide: How to create custom analysis/discovery agents
  - API integration documentation: REST API endpoints, authentication, rate limits
  - Example custom agents: Reference implementations (ESG Investor, Dividend Hunter, Turnaround Specialist)
  - Plugin migration guide: Upgrade path when core system changes, backward compatibility policy
- **Plugin validation:** Automated testing of custom agents before activation (interface compliance, performance benchmarks)

### Usability

**NFR-U1: Morning Report Clarity**
- Report SHALL be scannable in 2-3 minutes (executive summary + key recommendations visible immediately)
- Recommendations SHALL include: Clear BUY/SELL action, quantity, price, stop-loss, target (no ambiguity)
- Visual hierarchy: Most important information (NEW RECOMMENDATIONS, PORTFOLIO ALERTS) at top

**NFR-U2: Trade Execution Workflow**
- User SHALL be able to approve/reject trade with single click
- Confirmation prompts for destructive actions (SELL position)
- Trade logging form: Pre-filled with recommended quantities, minimal user input required

**NFR-U3: On-Demand Analysis**
- Any UK ticker searchable via web UI search bar
- Analysis results displayed in < 30 seconds with progress indicator
- Results organized by agent (expandable sections: Value Investor, Growth Investor, etc.)

**NFR-U4: Mobile Responsiveness** (Phase 1: Basic, Phase 2: Full)
- Morning report email readable on mobile devices (responsive HTML)
- Web dashboard functional on tablets/large phones (Phase 2)
- Native mobile apps (Phase 3)

### Integration

**NFR-I1: Data Provider Integration**
- Primary: Financial Modeling Prep API (REST API, JSON responses)
- Fallback: Yahoo Finance via yfinance Python library
- News: NewsAPI.org (REST API) or RSS feeds (fallback)
- Modular design: Easy to swap data providers without rewriting agent logic

**NFR-I2: LLM Provider Integration**
- Support multiple LLM providers via unified interface (LangChain abstraction)
- Provider selection configurable per agent (cost vs. quality trade-offs)
- Graceful fallback: If primary LLM unavailable, use secondary (e.g., GPT-4o → Claude Sonnet)

**NFR-I3: Broker Integration** (Phase 2-3)
- Phase 2: Semi-automated via Interactive Brokers API (generate orders, await user approval)
- Phase 3: Full automation with risk-limited auto-execution
- Support multiple brokers: Interactive Brokers, Trading 212, Hargreaves Lansdown (via manual flow)

**NFR-I4: Email Integration**
- SMTP for outbound emails (Gmail, SendGrid, AWS SES)
- HTML email templates for professional formatting
- Attachments: Optional PDF report generation

### Localization & Internationalization

**NFR-L1: Multi-Language & Regional Support**
- **Language Support:** System SHALL support multiple interface languages (Phase 2-3):
  - English (default, MVP)
  - Spanish, French, German (Phase 2 priority)
  - Additional languages via community translations (Phase 3)
- **Timezone Configuration:**
  - All scheduled times SHALL be displayed and configured in user's local timezone
  - System SHALL handle timezone conversions correctly (GMT → user timezone)
  - Daylight saving time transitions handled automatically
- **Currency Preferences:**
  - Primary display currency configurable (GBP default, USD, EUR, etc.)
  - System SHALL display prices, P&L, budgets in selected currency
  - Multi-currency portfolios supported (convert to base currency for reporting)
- **Date/Time Format Localization:**
  - Date format configurable (DD/MM/YYYY for UK/EU, MM/DD/YYYY for US, YYYY-MM-DD for ISO)
  - Time format configurable (24-hour for UK/EU, 12-hour AM/PM for US)
- **News Source Localization:**
  - Support for non-English news sources (French news for French stocks, German for German stocks)
  - Multi-language sentiment analysis (LLMs can analyze news in native language)
- **Number Format Localization:**
  - Thousand separators (1,000 for US/UK, 1.000 for DE, 1 000 for FR)
  - Decimal separators (1.23 for US/UK, 1,23 for DE/FR)

### Compliance & Regulatory Tooling

**NFR-C1: Audit, Explainability & Tax Support**
- **Configurable Audit Detail Levels:**
  - Minimal (Phase 1 MVP): Basic decision logs (what, when, outcome)
  - Standard: Agent reasoning included (why recommendation made)
  - Comprehensive: Full data lineage (which prices, which news articles, which reports informed decision)
  - User SHALL configure audit detail level based on needs (personal use vs. professional trading)
- **Explainability Reports:**
  - System SHALL generate explainability reports on-demand:
    - "Why did system recommend Company X?"
    - "What data sources informed this decision?"
    - "Which agents voted BUY vs. SELL and why?"
  - Explainability reports SHALL be exportable as PDF (for advisors, regulators, personal review)
  - Include data provenance (exact news articles, prices, financial metrics with timestamps)
- **Tax Reporting Exports:**
  - System SHALL generate tax reports for accountant:
    - Capital gains/losses per trade (purchase date, sale date, proceeds, cost basis, gain/loss)
    - Dividend income (if tracking dividends)
    - Wash sale detection and flagging (if applicable to jurisdiction)
  - Export formats: CSV, Excel, PDF
  - Reports SHALL be filterable by tax year, portfolio, asset type
- **Regulatory Compliance Modes:**
  - FCA Mode (UK): Audit trails meet Financial Conduct Authority requirements (Phase 3 if launching hedge fund)
  - SEC Mode (US): If expanding to US market (Phase 3)
  - MiFID II: Transaction reporting compliance for EU markets (Phase 3)
- **Trade Justification Logs:**
  - Required for professional/institutional traders
  - Each trade logged with:
    - Complete decision rationale (all agent votes, confidence scores, challenges raised)
    - Data sources used (which APIs, which news, which prices)
    - User approval timestamp (or auto-execution justification)
    - Outcome tracking (profit/loss realized)
- **Data Privacy & GDPR:**
  - User data SHALL be stored securely (encryption at rest)
  - User SHALL have right to export all data (JSON format)
  - User SHALL have right to delete account and all data
  - System SHALL not store unnecessary PII (minimize data collection)

---

_This PRD captures the complete vision for AIHedgeFund - an autonomous multi-agent AI trading system that brings institutional-quality investment analysis to retail investors at unprecedented cost efficiency (£100-200/month vs. £60k+/year). Through networked signal convergence, adversarial challenge protocols, and systematic opportunity discovery across the entire UK market, it aims to deliver consistent, profitable trading decisions while the user sleeps, waking up to actionable recommendations each morning._

**Next Steps After PRD Approval:**
1. Create epics.md (break PRD into implementable epics and user stories)
2. Create UX Design (wireframes for morning report, web dashboard)
3. Create Technical Architecture Document (system design, agent architecture, data flow, plugin system)
4. Phase 1 MVP Development (8-12 weeks target)

---
