# Project Classification

**Technical Type:** AI Platform (Multi-Agent Trading System)
**Domain:** Fintech (UK Stock Trading & Investment)
**Complexity:** HIGH

**Classification Rationale:**
- **Platform:** FastAPI backend + React frontend + LangGraph orchestration + 20-agent system + data processing pipelines
- **High Complexity Domain:** Financial trading, regulatory considerations (FCA), real-time data integration, LLM orchestration at scale
- **Unique Characteristics:** Not standard SaaS or web app—specialized AI agent orchestration platform with financial data integration

### Domain Context

**Fintech Domain - UK Stock Trading:**
- **Regulatory Environment:** Phase 1 (personal use) has minimal regulatory burden. Phase 3 (hedge fund launch) requires FCA authorization, compliance frameworks, and audit trails.
- **Market Characteristics:** London Stock Exchange (LSE), FTSE All-Share (~600 stocks), UK market hours 8:00 AM - 4:30 PM GMT
- **Data Requirements:** Real-time/delayed price data, financial statements, news feeds, insider trading disclosures, corporate actions
- **Cost Structures:** API costs (data + LLM), compute costs (overnight batch processing), trading costs (spreads, commissions)
- **Key Concerns:**
  - Data accuracy and timeliness (bad data = bad trades)
  - Security (API keys, trading credentials, portfolio data)
  - Audit trails (track all decisions for learning + potential regulatory compliance)
  - Risk management (position limits, stop-losses, max exposure controls)
  - Cost containment (LLM costs can spiral analyzing hundreds of stocks daily)

---
