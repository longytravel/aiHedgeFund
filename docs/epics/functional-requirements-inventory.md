# Functional Requirements Inventory

### FR-1: Discovery & Opportunity Identification
- FR-1.1: Morning News Scanning - UK financial news from configured sources daily
- FR-1.2: Multi-Source Trigger System - Discovery Agents (MVP: 4 agents - News Scanner, Fundamental Screener, Insider Trading, Volume & Price Action; Phase 2: add Earnings Surprise, Analyst Activity, Corporate Actions)
- FR-1.3: Company/Ticker Mapping - Database of 600+ UK companies
- FR-1.4: Signal Aggregation & Ranking - Aggregate signals from all discovery agents per ticker, apply sector multipliers
- FR-1.5: Opportunity Threshold Logic - Score-based routing (0-30 monitor, 31-60 research, 61-90 analyze, 91+ priority)
- FR-1.6: Macro/Sector Intelligence Layer (MVP) - Macro Economist Agent (weekly), Sector Rotation Agent (weekly), sector multipliers for signal scoring

### FR-2: Analysis & Decision Making
- FR-2.1: Multi-Agent LLM Analysis - 8 Analysis Agents (Value, Growth, Contrarian, Naked Trader, Quality/Moat, Technical, Catalyst Detective, Sentiment)
- FR-2.2: Agent Orchestration (LangGraph) - Parallel execution of agents with unified state
- FR-2.3: Risk Management (Risk Manager Agent) - Position sizing, stop-loss, target prices, portfolio constraints
- FR-2.4: Portfolio Management (Portfolio Manager Agent) - Final BUY/SELL/HOLD decisions, order generation
- FR-2.5: Existing Position Monitoring - Daily checks for stop-loss, target reached, fundamental deterioration
- FR-2.6: Adversarial Challenge Protocol - Risk Manager + Contrarian challenge bullish thesis before BUY
- FR-2.7: Agent Management & Configurability - Enable/disable agents, weighting, custom agents, performance tracking

### FR-3: Three-Tier Tracking System
- FR-3.1: Tier 1 - Active Portfolio - Current holdings with P&L tracking and SELL monitoring
- FR-3.2: Tier 2 - Active Watchlist - Conditional triggers (price, event, macro, technical) with re-validation
- FR-3.3: Tier 3 - Research Queue - Stocks under investigation (scored 31-60)

### FR-4: Reporting & Notifications
- FR-4.1: Daily Morning Report - Delivered by 7am GMT with BUY recommendations, portfolio alerts, watchlist triggers
- FR-4.2: Report Delivery Channels - Email, web dashboard, (future) mobile push
- FR-4.3: On-Demand Reporting - Detailed analysis of any stock, historical reports

### FR-5: Data Management & Integration
- FR-5.1: 3-Tier Data Architecture - EODHD (fundamentals), CityFALCON (UK RNS/insider dealings), IBKR (real-time execution)
- FR-5.2: Data Integration Implementation - API clients for each provider
- FR-5.3: Data Caching - Reduce API costs, improve performance
- FR-5.4: Data Validation & Quality Checks - Outlier detection, cross-validation
- FR-5.5: Audit Trail - Log all data sources and decisions
- FR-5.6: Ad-Hoc Research Inbox - Manual stock additions to analysis queue
- FR-5.7: Fallback & Error Handling - Graceful degradation when APIs unavailable

### FR-6: Automation & Scheduling
- FR-6.1: Batch Processing - Default overnight 1am-7am GMT, fully configurable schedule
- FR-6.2: System Reliability - Error handling, retry logic, graceful degradation
- FR-6.3: Cost Monitoring - Track LLM and API costs per analysis
- FR-6.4: Scheduling Flexibility - Custom times, days, timezone, multiple runs, on-demand

### FR-7: User Interface & Trade Execution
- FR-7.1: Web Dashboard (React Frontend) - View reports, manage portfolio, configure agents
- FR-7.2: Manual Trade Execution & Logging - Approve/reject recommendations, log decisions
- FR-7.3: Trade Outcome Tracking - Record actual trades, P&L, lessons learned

### FR-8: System Architecture & Technical Requirements
- FR-8.1: Backend (FastAPI) - REST API, async task processing, database access
- FR-8.2: Agent Orchestration (LangGraph) - Multi-agent workflow with state management
- FR-8.3: LLM Integration - GPT-4o integration with structured outputs
- FR-8.4: Database & Persistence - PostgreSQL for structured data, audit logs
- FR-8.5: Deployment - Docker containerization, cloud hosting

### FR-9: System Extensibility & Modularity
- FR-9.1: Plugin Architecture - Add custom agents without code changes
- FR-9.2: Data Source Modularity - Swap data providers via configuration
- FR-9.3: Strategy Framework - Pre-configured agent sets for different goals
- FR-9.4: API for External Integrations - Webhook support for third-party tools

### FR-10: Ad-Hoc & On-Demand Execution
- FR-10.1: Manual Full Discovery Scan - User-triggered market-wide analysis
- FR-10.2: Custom Ticker List Analysis - Analyze specific stocks on-demand
- FR-10.3: Portfolio Re-Evaluation On-Demand - Re-run all agents on current holdings
- FR-10.4: Event-Driven Triggers - React to breaking news, RNS announcements
- FR-10.5: Historical Backfill Analysis - Analyze how system would have performed on past data

### FR-11: Discovery Scope & Targeting
- FR-11.1: Market Cap Filters - Configure minimum market cap, focus FTSE 100/250/Small Cap
- FR-11.2: Sector & Industry Focus - Whitelist/blacklist sectors
- FR-11.3: Custom Ticker Lists - User-defined stock universe
- FR-11.4: ESG & Ethical Filters - Exclude sin stocks, ESG scoring
- FR-11.5: Price Range & Liquidity Filters - Min/max price, min volume
- FR-11.6: Geography & Asset Class Expansion - Future: US, EU, crypto, forex

### FR-12: Workflow & Execution Modes
- FR-12.1: Manual Approval Workflow (MVP Default) - Review and approve trades manually
- FR-12.2: Paper Trading / Simulation Mode - Track hypothetical performance
- FR-12.3: Read-Only / Educational Mode - View recommendations without trading
- FR-12.4: Auto-Execution Mode (Phase 2) - Execute within guardrails
- FR-12.5: Collaborative / Multi-User Approval (Phase 2-3) - Team decision-making
- FR-12.6: Dry-Run / Test Mode - Test configuration changes

### FR-13: Multi-Portfolio Management
- FR-13.1: Multiple Portfolio Support - ISA, SIPP, taxable, joint accounts
- FR-13.2: Portfolio-Specific Strategies - Different agent configurations per portfolio
- FR-13.3: Portfolio-Specific Risk Parameters - Custom risk limits per portfolio
- FR-13.4: Cross-Portfolio Tax Optimization (Phase 2-3) - Harvest losses, rebalance
- FR-13.5: Consolidated & Individual Reporting - Aggregate and per-portfolio reports

### FR-14: Alerting & Notification System
- FR-14.1: Custom Alert Triggers - User-defined conditions for notifications
- FR-14.2: Multi-Channel Alert Delivery - Email, SMS, Slack, webhook
- FR-14.3: Alert Urgency Levels & Frequency - Critical/warning/info, immediate/digest
- FR-14.4: Alert Filters & Quiet Hours - Suppress during configured times
- FR-14.5: Alert Grouping & Digest - Batch multiple alerts

### FR-15: Historical Analysis & Backtesting
- FR-15.1: Historical Backtesting - Walk-forward optimization on past data
- FR-15.2: Point-In-Time Analysis - How would system have decided on specific date
- FR-15.3: Configuration A/B Testing - Compare different agent configurations
- FR-15.4: Stress Testing - Test performance during crashes, recessions
- FR-15.5: Performance Attribution Historical - Which agents contributed most
- FR-15.6: Walk-Forward Validation - Prevent overfitting in agent tuning

---
