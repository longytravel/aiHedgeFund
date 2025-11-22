# AIHedgeFund - Product Requirements Document

**Author:** Longy
**Date:** 2025-11-19
**Version:** 1.0

---

## Executive Summary

AIHedgeFund is an autonomous multi-agent AI trading system that replicates institutional hedge fund decision-making at retail cost. Using a breakthrough 20-agent networked architecture with signal convergence, it systematically discovers and analyzes UK stock market opportunities on your schedule (default: overnight), delivering actionable trading decisions when and how you want them (default: morning report).

**The Problem:** Retail traders face systematic disadvantages—they can't monitor entire markets (FTSE All-Share = 600+ stocks), lack multi-perspective institutional analysis, suffer emotional bias, and miss opportunities happening outside their watchlist. Elite hedge funds deploy teams of specialized analysts, systematic processes, and 24/7 resources that cost £60,000-100,000+/year.

**The Solution:** A 20-agent AI system running on your schedule (default: overnight 1am-7am, fully configurable) that:
- **Discovers opportunities** via 7 configurable searcher agents (News Scanner, Insider Trading, Volume Spikes, Fundamental Screener, Earnings Surprises, Analyst Activity, Corporate Actions)
- **Analyzes from multiple perspectives** via 8 customizable expert investor agents (Buffett, Lynch, Burry, Naked Trader, Quality/Moat, Technical, Catalyst Detective, Sentiment)—enable/disable, weight, or add your own
- **Makes decisions** via Risk Manager + Portfolio Manager with adversarial challenge process
- **Delivers reports** at your preferred time/format (default: morning report by 7am via email), plus on-demand analysis anytime
- **Costs £100-200/month** vs. institutional £60k+/year (99.5% cost reduction)

**Three-Phase Path:**
- **Phase 1 (Months 1-3):** Prove profitability with £5-10k capital, 2-3 trades/week, 60%+ win rate
- **Phase 2 (Months 4-9):** Scale to £100k capital, 5-10 trades/week, 40%+ annualized returns
- **Phase 3 (Month 10+):** Launch as hedge fund or signal service

**Current Status:** Working US-focused system with 19 agents. Adapting for UK market with enhanced networked architecture, signal convergence system, and three-tier tracking innovation.

### What Makes This Special

**Core Differentiator:** Networked multi-agent architecture with signal convergence creates emergent intelligence at retail cost.

**Five Breakthrough Innovations:**

1. **Signal Convergence Network** (Industry First)
   - Agents broadcast/listen/react in dynamic network—NOT linear pipeline
   - Example: News Scanner spots catalyst → Industry Specialist confirms significance → Macro Economist identifies trend → Fundamental Screener finds peers → Technical Analyst sees breakout = **CONVERGENCE DETECTED**
   - Multiple independent signals converging on same stock = highest conviction
   - Signal scoring: Weighted by strength + diversity + macro multipliers
   - Filters noise from genuine opportunities

2. **Three-Tier Tracking System** (Watchlist Innovation)
   - **Tier 1 - Active Portfolio:** Current holdings, monitored for SELL signals
   - **Tier 2 - Active Watchlist:** Great stocks waiting for conditions ("Buy if drops to £8", "Buy if insider buying occurs") with **re-validation protocol** (prevents value traps)
   - **Tier 3 - Research Queue:** Stocks under investigation
   - Captures "almost good" opportunities that timing prevents from immediate entry
   - No missed opportunities from timing issues

3. **Adversarial Challenge Protocol** (Risk Management)
   - Before every BUY: Risk Manager + Contrarian Agent **force rigorous thesis defense**
   - Challenge questions: "What could go wrong?", "Why is the market wrong?", "Is this a value trap?"
   - Bull case agents respond to challenges
   - Result: Appropriately sized positions, tight stop-losses, prevents groupthink
   - Matches institutional investment committee processes

4. **Modular Agent Architecture** (Extensibility & Control)
   - Add, remove, or swap agents without code changes—complete plugin system
   - Enable/disable agents based on performance, cost, or strategy preferences
   - Configure agent weights: Emphasize value vs. growth vs. technical analysis
   - Custom agent library: Build your own investor personas
   - Examples:
     - Cost optimization: Disable expensive LLM agents during testing (60% cost reduction)
     - Strategy tuning: Run only value investing agents for dividend portfolio
     - Performance iteration: Remove underperforming agents, boost high-performers
     - Personal preference: "I don't trust technical analysis" → disable Technical Analyst
   - Supports rapid experimentation and continuous improvement
   - Future: Agent marketplace for sharing/selling custom investor personas

5. **Total Flexibility & Control** (User Empowerment)
   - **Schedule:** Morning, afternoon, multiple times daily, weekends, or on-demand anytime—not locked to 7am
   - **Scope:** Analyze entire market, specific sectors, custom ticker lists, or single stocks on demand
   - **Output:** Email, SMS, Slack, PDF, JSON—whatever format, whenever you want it
   - **Strategy:** Run multiple portfolios with different strategies simultaneously (ISA conservative, taxable aggressive)
   - **Execution:** Manual approval, auto-execute within guardrails, or paper trade mode
   - **Agents:** Enable/disable, weight, customize, add your own investor personas
   - **Result:** System adapts to YOUR life, YOUR strategy, YOUR preferences—not the other way around
   - Unlike rigid black-box robo-advisors that force you into their workflow

**Technical Foundation:**
- **LangGraph Orchestration:** Production-grade multi-agent workflow (used by Uber, LinkedIn, Elastic)
- **20-Agent Architecture:** 7 Discovery + 2-3 Macro/Sector + 8 Analysis + 2 Decision agents
- **Batch Processing:** Overnight 1am-7am processing (cost-effective vs. real-time)
- **Existing Codebase:** Working US system with FastAPI backend, React frontend, 19 agents already built

**Competitive Advantages:**
- **UK Market Specialization:** Less competition than US-focused tools, LSE retail data fee waiver (Jan 2025)
- **Research-Validated:** Architecture mirrors elite hedge funds ($400B+ AUM validated practices)
- **Cost-Effective:** £100-200/month vs. £60,000+/year institutional (99.5% cost reduction)
- **Modular & Extensible:** Unlike black-box robo-advisors, users control which agents run, adjust weights, build custom investor personas—complete transparency and customization
- **Total Flexibility:** On-demand analysis, custom schedules, multiple portfolios, any output format—system adapts to user's life and strategy, not vice versa
- **Scalable Path:** Personal use → Hedge fund → Signal service

---

## Project Classification

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

## Success Criteria

Success is measured across three distinct phases with escalating validation thresholds:

**Phase 1: PROVE IT (Months 1-3) - Concept Validation**
- ✅ **Primary Success Metric:** 60%+ win rate with 8-12% average gain per winning trade
- ✅ **Volume Target:** 2-3 actionable trades per week (consistently generating opportunities)
- ✅ **Cost Containment:** Total operating costs ≤ £200/month (LLM + data APIs)
- ✅ **Capital Deployed:** £5,000-10,000 test capital
- ✅ **System Reliability:** Report delivered at configured time 95%+ of scheduled runs (default: 7am trading days)
- ✅ **Quality Gate:** Opportunities align with user judgment 80%+ of time (human validation)

**Phase 2: SCALE IT (Months 4-9) - Performance Validation**
- ✅ **Primary Success Metric:** 40%+ annualized returns (significantly beating FTSE 100)
- ✅ **Volume Target:** 5-10 trades per week with maintained quality
- ✅ **Capital Deployed:** £50,000-100,000
- ✅ **Risk Management:** Max drawdown ≤ 20%, Sharpe ratio > 1.5
- ✅ **Cost Efficiency:** Operating costs < 5% of profits generated
- ✅ **Portfolio Sophistication:** Successfully managing 15-20 concurrent positions

**Phase 3: PRODUCTIZE IT (Month 10+) - Business Validation**
- ✅ **Strategic Decision Point:** Launch hedge fund, signal service, or licensed fund product
- ✅ **Regulatory Compliance:** FCA authorization obtained (if hedge fund path)
- ✅ **Track Record:** 12+ months auditable performance data
- ✅ **Scalability Proven:** System handles £500k+ capital without performance degradation
- ✅ **Automation Maturity:** 90%+ trades executed without manual intervention

### Business Metrics

**Revenue/Value Metrics (Phase-Dependent):**
- **Phase 1:** Personal profit generation, system validation (no revenue target)
- **Phase 2:** £20k-50k personal trading profits demonstrating viability
- **Phase 3:** £100k+ personal profits OR service revenue (signal subscriptions, fund management fees)

**Cost Metrics:**
- **Data APIs:** EODHD All-In-One (~£85/month) + CityFALCON (~£30/month) + IBKR data feed (~£10/month) = ~£125/month
- **LLM Costs:** GPT-4o batch processing for 20 agents analyzing 10-15 stocks/day = ~£40-60/month
- **Infrastructure:** Cloud hosting (AWS/DigitalOcean) = ~£20-40/month
- **Total:** £185-225/month Phase 1, scaling to £300-500/month Phase 2 (still 99% cheaper than institutional £3000+/month)

**Engagement Metrics:**
- Daily morning report open rate (user engagement with recommendations)
- Trade approval rate (% of AI recommendations user agrees with)
- Watchlist utilization (how often watchlist triggers lead to trades)
- Signal convergence accuracy (when 4+ agents agree, what's the success rate?)

**Learning Metrics:**
- Win rate by signal strength threshold (optimize confidence scoring)
- Performance by agent combination (which agent groups most valuable?)
- Cost per analyzed stock (optimize funnel efficiency)
- Time saved vs. manual research (ROI calculation)

---

## Product Scope

### MVP - Minimum Viable Product

**Goal:** Prove the autonomous UK trading concept works with £5-10k capital in 3 months.

**Core MVP Features:**

1. **UK Market Data Integration (3-Tier Simplified Architecture)**
   - **Tier 1 - Core Data:** EODHD All-In-One for fundamentals, history, estimates, macro
   - **Tier 2 - Intelligence:** CityFALCON for UK RNS feeds, director dealings, sentiment
   - **Tier 3 - Execution:** IBKR API for real-time quotes at point of trade
   - FTSE 100/250/All-Share ticker support (600+ stocks)
   - UK company → ticker mapping database

2. **Discovery Layer (7 Configurable Agents)**
   - **Modular Design:** Enable/disable any discovery agent, configure parameters
   - **Custom Scope:** Analyze entire FTSE, specific sectors, custom ticker lists, or single stocks on-demand
   - **Agent Library:**
     - News Scanner Agent (UK-specific sources: BBC, FT, Reuters, City AM—customizable sources)
     - Insider Trading Agent (UK director dealings via Companies House/RNS)
     - Volume & Price Action Agent (unusual trading activity detection—adjustable thresholds)
     - Fundamental Screener Agent (quantitative filters: P/E, growth, debt—user-configurable custom screens)
     - Earnings Surprise Agent (vs. analyst expectations)
     - Analyst Activity Agent (broker upgrades/downgrades, target changes)
     - Corporate Actions Agent (buybacks, dividends, M&A monitoring)

3. **Analysis Layer (8 Configurable Agents - Adapted from Existing US System)**
   - **Modular Design:** Enable/disable any agent via configuration
   - **Weighted Voting:** Adjust agent influence (e.g., 2x weight for Value Investor if running dividend strategy)
   - **Agent Library:**
     - Value Investor Agent (Buffett/Graham philosophy: moats, intrinsic value)
     - Growth Investor Agent (Peter Lynch: PEG ratio, sustainable growth)
     - Contrarian Agent (Michael Burry: mispricing, contrarian opportunities)
     - Naked Trader Agent (Robbie Burns UK methodology: profitable + growing + low debt checklist)
     - Quality/Moat Agent (competitive advantages, pricing power)
     - Technical Analyst Agent (charts, patterns, momentum indicators)
     - Catalyst Detective Agent (what specific event drives upside?)
     - Sentiment Analyst Agent (news tone, positioning, social sentiment)
   - **Custom Agents:** Framework supports adding new investor personas (e.g., ESG Investor, Dividend Hunter, Turnaround Specialist)

4. **Decision Layer (2 Agents)**
   - Risk Manager Agent (position sizing, stop-losses, exposure limits)
   - Portfolio Manager Agent (final BUY/SELL/HOLD decisions, aggregates all signals)

5. **Flexible Batch Processing (Default: Overnight 1am-7am GMT, Fully Configurable)**
   - **Custom Scheduling:** User sets execution time(s), days, timezone (default: nightly Monday-Friday)
   - **Multiple Runs:** Support morning + afternoon updates, weekend analysis, or pause mode
   - **On-Demand Execution:** User can trigger full analysis anytime via web UI or API
   - **Execution Workflow:**
     - Data collection (prices, news, filings, insider trades)
     - Discovery agents run and generate signals (configurable scope: entire market, sectors, or custom ticker lists)
     - High-scoring stocks → deep analysis by enabled analysis agents
     - Risk + portfolio management decisions
     - Report generation in configured format(s)

6. **Flexible Report Delivery (Default: Morning Report by 7am, Fully Configurable)**
   - **Custom Timing:** User sets preferred delivery time(s) and timezone (default: 7am GMT)
   - **Report Content:**
     - 0-3 NEW BUY recommendations with full rationale
     - Current portfolio status (holdings, P&L, stop-loss alerts)
     - Watchlist summary (stocks being monitored)
     - Market context (weekly macro/sector updates)
   - **Multi-Channel Delivery:** Email (default), web dashboard, SMS, Slack, webhook, API (user-configurable)
   - **Format Options:** HTML email (default), PDF, JSON, CSV—user selects preferred format(s)
   - **Detail Levels:** Summary, standard, detailed, or data-only (user-configurable sections)

7. **Flexible Trade Execution & Workflows**
   - **Manual Approval (Default MVP):** User reviews recommendations, approves/rejects, executes via broker
   - **Paper Trading Mode:** Track hypothetical performance without real money (testing/learning)
   - **Read-Only Mode:** View recommendations without trade capability (educational use)
   - **Future (Phase 2):** Auto-execution within guardrails, collaborative approval, broker API integration
   - All workflows log decisions for system learning and performance attribution

8. **Configurable Watchlist**
   - Track stocks identified as interesting but timing not right
   - Customizable triggers (price-based, event-based, technical, macro)
   - Manual monitoring (MVP) with future re-validation protocol (Phase 2)

**Out of Scope for MVP (Deferred to Phase 2-3):**
- ❌ Automated trade execution (broker API integration)
- ❌ Advanced signal convergence scoring (basic scoring in MVP)
- ❌ Three-tier tracking with re-validation protocol (basic watchlist in MVP)
- ❌ Adversarial challenge protocol (manual risk review in MVP)
- ❌ Macro/Sector rotation agents (analysis agents only in MVP)
- ❌ Mobile app (web dashboard in MVP)
- ❌ Multi-user / multi-portfolio support (single user/portfolio in MVP)
- ❌ Real-time intraday monitoring (end-of-day analysis in MVP)
- ❌ Historical backtesting UI (manual validation in MVP)
- ❌ Agent marketplace (custom agents supported, marketplace Phase 3)

### Growth Features (Post-MVP)

**Phase 2 (Months 4-9) - Enhanced Intelligence & Automation:**

1. **Networked Signal Convergence System**
   - Agents broadcast/listen/react in dynamic network
   - Signal strength scoring with weighted factors
   - Convergence detection: Multiple independent agents spotting same stock = high conviction
   - Macro/sector multipliers (favored sectors get 1.3-1.5x boost)
   - Threshold-based triggers: 0-30 points (monitor), 31-60 (queue), 61-90 (analyze), 91+ (priority)

2. **Three-Tier Tracking System with Re-Validation**
   - **Tier 1:** Active Portfolio (current holdings, SELL monitoring)
   - **Tier 2:** Active Watchlist with conditional triggers:
     - Price-based: "Alert when drops to £8.50"
     - Event-based: "Alert when insider buying occurs"
     - Macro-based: "Alert when sector rotation favors this sector"
     - Technical: "Alert when breaks above resistance at £12"
   - **Tier 3:** Research Queue (under investigation)
   - **Re-validation Protocol:** When watchlist trigger fires, ALL agents re-run analysis to confirm thesis still valid (prevents value traps)

3. **Adversarial Challenge Protocol**
   - Before BUY: Risk Manager + Contrarian force devil's advocate questions
   - Challenge round: "What could go wrong?", "Why is market wrong?", "Value trap risk?"
   - Bull agents respond to challenges
   - Outcomes: Adjusted position size, tighter stops, or kill trade
   - Prevents groupthink, mimics institutional investment committees

4. **Macro/Sector Rotation Agents (3 agents)**
   - Macro Economist Agent (UK economic environment assessment)
   - Sector Rotation Agent (identify favored/disfavored sectors in current conditions)
   - Industry Specialist Agents (deep sector expertise, optional)
   - Top-down hierarchy: Macro → Sector → Stock selection

5. **Enhanced Performance Analytics**
   - Win rate by confidence threshold (optimize scoring)
   - Agent contribution analysis (which agents most valuable?)
   - Cost-per-stock analysis (optimize funnel efficiency)
   - Backtest comparisons (how would system have performed historically?)

6. **Semi-Automated Execution**
   - Broker API integration (Interactive Brokers, Trading 212)
   - Auto-generate orders, await user approval via mobile
   - One-click trade execution

7. **Agent Configuration & Extensibility**
   - Visual agent builder: Create custom investor personas via UI
   - Agent performance attribution: Track which agents contribute most alpha
   - Strategy templates: Pre-configured agent sets (Value Portfolio, Growth Aggressive, Dividend Income, etc.)
   - Agent versioning: A/B test different agent prompts/logic
   - Export/import agent configurations (share with community)

8. **Multi-Portfolio Management**
   - Multiple portfolio support (ISA, SIPP, taxable, joint accounts)
   - Portfolio-specific strategies (conservative for ISA, aggressive for taxable)
   - Portfolio-specific agent configurations and risk parameters
   - Cross-portfolio tax optimization (harvest losses, rebalance)
   - Consolidated and individual portfolio reporting

### Vision (Future)

**Phase 3 (Month 10+) - Productization & Scale:**

1. **Full Automation**
   - Hands-free operation: System trades autonomously within predefined risk parameters
   - User sets weekly/monthly approval thresholds
   - Morning report becomes FYI vs. action required

2. **Hedge Fund Infrastructure**
   - FCA authorization and compliance framework
   - Multi-investor accounts and capital tracking
   - Professional reporting (monthly tear sheets, quarterly investor letters)
   - Auditable decision trail for regulatory compliance

3. **Signal Service Platform**
   - Subscription tiers (Basic: morning report only, Pro: full agent analysis, Premium: custom portfolios)
   - £99-499/month subscription revenue
   - White-label partnerships with wealth managers

4. **Strategy Customization Engine**
   - User risk profiles (conservative, balanced, aggressive)
   - Sector preferences/exclusions (e.g., no tobacco, overweight tech)
   - Custom agent weighting (emphasize value vs. growth)
   - Multiple portfolio strategies (income, growth, speculative)

5. **Mobile-First Experience**
   - Native iOS/Android apps
   - Push notifications for opportunities and alerts
   - Quick approval/reject interface
   - Portfolio tracking and P&L visualization

6. **Advanced Backtesting Framework**
   - Walk-forward optimization
   - Monte Carlo simulation
   - Stress testing (2008 crisis, COVID crash scenarios)
   - Compare strategies and agent combinations

7. **Community, Marketplace & Learning**
   - **Agent Marketplace:**
     - Browse/purchase community-contributed agents (ESG Investor, Biotech Specialist, Small-Cap Hunter)
     - Licensed premium agents (Joel Greenblatt Magic Formula, Mohnish Pabrai Clone Investing)
     - Revenue model: 30% platform fee on agent sales (£5-50 per agent)
     - Agent ratings and reviews (5-star system, performance stats)
     - Version control: Agent updates delivered to buyers
   - **Strategy Templates Library:**
     - Pre-configured agent sets for common goals (Income, Growth, Value, Momentum)
     - User-contributed strategies with backtest results
     - One-click strategy import
   - **User Community:**
     - Forums for strategy discussion
     - Performance leaderboards (opt-in, privacy-preserved)
     - Educational content: How each agent thinks, when to use each
   - **Revenue Opportunity:** 1,000 users × £20/month marketplace spend = £20k/month platform revenue

---

## Domain-Specific Requirements

**Fintech (UK Stock Trading) - High Complexity Domain**

1. **UK Market Data Requirements**
   - LSE real-time/delayed price data (FTSE 100, 250, Small Cap, AIM)
   - Ticker format support: VOD.L, BP.L, HSBC.L (Financial Modeling Prep format)
   - UK-specific financial metrics (IFRS accounting standards, not US GAAP)
   - Insider trading data: UK director dealings via Companies House RNS filings
   - Corporate actions: Dividends (pence vs. pounds handling), buybacks, rights issues
   - UK regulatory filings: Annual reports, interim results, trading updates

2. **UK Regulatory Considerations**
   - **Phase 1 (Personal Use):** Minimal regulatory burden, personal investment decisions
   - **Phase 3 (Hedge Fund):** FCA authorization required, MIFID II compliance, audit trail requirements
   - Data Protection: GDPR compliance for any user data storage
   - Market Abuse Regulation (MAR): No insider information usage, audit all data sources
   - Transaction Reporting: Prepare for potential MiFID II/MiFIR requirements if scaling

3. **UK Market Specifics**
   - Market Hours: 8:00 AM - 4:30 PM GMT (earlier close than US)
   - Currency: GBP (pounds sterling), some stocks quoted in pence (divide by 100)
   - Settlement: T+2 (trade date plus 2 business days)
   - Stamp Duty: 0.5% tax on UK stock purchases (factor into cost calculations)
   - ISA/SIPP accounts: Tax-advantaged wrappers (may influence strategy)

4. **Cost Structure Constraints**
   - LLM API costs: GPT-4o at ~$2.50/1M input tokens, $10/1M output tokens
   - Data API costs: Financial Modeling Prep $29-59/month, NewsAPI $449/month
   - Broker costs: Commission + spread + 0.5% stamp duty on buys
   - Target: Keep total operating cost ≤ £200/month Phase 1 (preserve capital for trading)

5. **Risk Management Requirements**
   - Position Sizing: Max 5-10% of portfolio per position (diversification)
   - Stop Losses: Automatic exit triggers (8-12% typical, adjustable per risk level)
   - Max Drawdown: Circuit breaker if portfolio down 20% from peak
   - Exposure Limits: Max total invested 60-80% (maintain cash buffer)
   - Concentration Risk: No more than 20% in single sector

6. **Audit & Compliance Trail**
   - Log all agent decisions with timestamps and reasoning
   - Track data sources for each decision (which news articles, which prices, which reports)
   - Record trade approvals/rejections with user input
   - Store performance history for learning and potential regulatory review
   - Maintain version history of agent prompts and model changes

7. **Data Quality & Accuracy**
   - Price data validation: Reject outliers, check for corporate actions
   - News source verification: Only use reputable UK financial news (BBC, FT, Reuters, City AM)
   - Financial data reconciliation: Cross-check metrics across multiple sources where possible
   - Error handling: Graceful degradation if API unavailable (use cached data, skip analysis, alert user)

This section shapes all functional and non-functional requirements below.

---

## Functional Requirements

### FR-1: Discovery & Opportunity Identification

**FR-1.1: Morning News Scanning**
- System SHALL fetch UK financial news from configured sources daily (BBC Business, Financial Times, Reuters UK, City AM, This Is Money)
- News fetch window: 6:00 AM - 9:00 AM GMT (before market open)
- System SHALL extract mentioned UK companies from headlines and article summaries using company name → ticker mapping database
- Minimum 100 articles per scan to ensure coverage
- System SHALL filter news for relevance (FTSE mentions, stock market keywords, LSE activity)

**FR-1.2: Multi-Source Trigger System** (7 Discovery Agents)
- **News Scanner:** Monitor UK news sources for company-specific catalysts (earnings, partnerships, regulatory approval, management changes)
- **Insider Trading:** Fetch UK director dealings from Companies House RNS filings, flag significant purchases/sales
- **Volume & Price Action:** Detect unusual trading activity (volume spikes 2x+ avg, price moves 5%+ on high volume)
- **Fundamental Screener:** Run quantitative filters across FTSE All-Share daily:
  - P/E < market average AND revenue growth > 10% (value + growth combo)
  - Debt/Equity < 0.5 AND ROCE > 15% (financial strength)
  - User-configurable custom screens
- **Earnings Surprise:** Track earnings releases vs. analyst expectations, flag beats/misses
- **Analyst Activity:** Monitor broker upgrades/downgrades, target price changes from major UK brokers (Barclays, Peel Hunt, Liberum, etc.)
- **Corporate Actions:** Track buybacks, dividend increases, M&A activity, spinoffs

**FR-1.3: Company/Ticker Mapping**
- System SHALL maintain database of 600+ UK companies (FTSE 100, FTSE 250, liquid small caps)
- Database SHALL include: Company name, aliases, LSE ticker, sector, index membership
- Support fuzzy matching for name variations (e.g., "Vodafone", "Vodafone Group", "Vodafone plc" all → VOD.L)
- Monthly updates to reflect index changes and new listings

**FR-1.4: Signal Aggregation & Ranking**
- System SHALL aggregate signals from all discovery agents per ticker
- Calculate signal strength score (0-100) based on:
  - Number of independent signals (more signals = higher score)
  - Signal quality (insider buying weighted higher than general news mention)
  - Recency (signals from last 24 hours weighted higher)
  - Confidence from sentiment analysis
- Apply macro/sector multipliers (favored sectors get boost)
- Rank all mentioned tickers by total score

**FR-1.5: Opportunity Threshold Logic**
- Score 0-30: Monitor only (add to background tracking)
- Score 31-60: Research queue (investigate further)
- Score 61-90: Trigger deep analysis (all 8 analysis agents)
- Score 91+: Priority analysis (highest conviction, fast-track to portfolio manager)

### FR-2: Analysis & Decision Making

**FR-2.1: Multi-Agent LLM Analysis** (8 Analysis Agents)
- System SHALL run 8 specialized analysis agents for each opportunity exceeding threshold
- **Value Investor Agent:**
  - Assess intrinsic value using DCF, comparable company analysis
  - Evaluate moat (competitive advantages, pricing power)
  - Calculate margin of safety (intrinsic value vs. current price)
  - Output: BUY (undervalued), SELL (overvalued), HOLD (fair value)
- **Growth Investor Agent:**
  - Calculate PEG ratio (P/E to earnings growth rate)
  - Assess revenue/earnings growth sustainability
  - Evaluate TAM (total addressable market) expansion potential
  - Output: BUY/SELL/HOLD + confidence
- **Contrarian Agent:**
  - Identify mispricing due to negative sentiment
  - Look for turnaround catalysts
  - Assess value trap risk
  - Output: BUY (contrarian opportunity) or AVOID (value trap)
- **Naked Trader Agent:** (Robbie Burns UK methodology)
  - Checklist: Profitable? Growing? Low debt? Positive momentum?
  - All YES = BUY, any NO = investigate reason
  - Emphasize common-sense, checklist-based approach
- **Quality/Moat Agent:**
  - Assess competitive advantages: network effects, switching costs, brand, regulatory barriers
  - Evaluate management quality and capital allocation
  - Output: Quality score (A-F) + recommendation
- **Technical Analyst Agent:**
  - Chart patterns (support/resistance, breakouts, trend channels)
  - Momentum indicators (RSI, MACD, moving averages)
  - Volume confirmation
  - Output: BUY (bullish setup), SELL (bearish), NEUTRAL
- **Catalyst Detective Agent:**
  - Identify specific near-term catalysts (earnings in 2 weeks, product launch, regulatory decision)
  - Assess catalyst magnitude and probability
  - Output: Expected catalyst impact + timeline
- **Sentiment Analyst Agent:**
  - Aggregate sentiment from news, social media, analyst reports
  - Detect sentiment shifts (improving vs. deteriorating)
  - Identify contrarian signals (extreme pessimism = opportunity)
  - Output: Sentiment score (-100 to +100) + trend direction

**FR-2.2: Agent Orchestration (LangGraph)**
- All 8 analysis agents SHALL run in parallel for efficiency
- Each agent outputs: Signal (BUY/SELL/HOLD), Confidence (0-100), Reasoning (structured JSON)
- System SHALL aggregate all agent outputs into unified state object
- Total analysis time target: < 3 minutes per stock (parallel execution + caching)

**FR-2.3: Risk Management (Risk Manager Agent)**
- Input: All analyst signals + current portfolio state
- Calculate recommended position size per stock:
  - Base: 5-10% of portfolio value
  - Adjust for confidence: High conviction (7+ bullish agents) = 10%, Medium (5-6) = 7%, Low (3-4) = 5%
  - Adjust for volatility: High beta stocks get smaller size
  - Respect concentration limits: No more than 20% in single sector
- Set stop-loss levels:
  - Default: 8-12% below entry price
  - Tighter stops (5-8%) for low-conviction trades
  - Wider stops (12-15%) for high-conviction long-term plays
- Set target prices:
  - Calculate upside from valuation agent analysis
  - Set initial target at 50% of estimated upside (secure partial gains)
- Check portfolio constraints:
  - Total exposure ≤ 80% of capital (maintain cash buffer)
  - No single position > 10% of portfolio
  - Sector exposure ≤ 20% per sector
- Output: Approved/rejected recommendations with position sizing and risk parameters

**FR-2.4: Portfolio Management (Portfolio Manager Agent)**
- Input: Risk-approved recommendations
- Make final BUY/SELL/HOLD decisions:
  - BUY: 6+ agents bullish AND confidence > 65% AND passes risk checks
  - SELL: 6+ agents bearish OR stop-loss triggered OR target reached
  - HOLD: Mixed signals or insufficient conviction
- Generate trading orders:
  - Ticker symbol
  - Action (BUY/SELL)
  - Quantity (shares)
  - Order type (market, limit)
  - Stop-loss price
  - Target price
- Prioritize opportunities: Highest conviction stocks first if capital limited
- Output: Daily trading recommendations (0-3 new BUY orders typical)

**FR-2.5: Existing Position Monitoring**
- Check all current holdings daily:
  - Stop-loss breached? → Generate SELL order
  - Target price reached? → Generate partial SELL (50% of position)
  - Fundamental deterioration? → Re-run all agents, may trigger SELL
- Monitor watchlist stocks:
  - Price triggers reached? → Re-validate thesis, may trigger BUY
  - Event triggers occurred? (insider buying, earnings beat) → Re-analyze

**FR-2.6: Adversarial Challenge Protocol**
- Before any BUY recommendation reaches user, Risk Manager and Contrarian agents SHALL challenge the bullish thesis
- Challenge questions SHALL include:
  - "What could go wrong with this investment?"
  - "Why is the market pricing this incorrectly?"
  - "Is this a value trap? What evidence contradicts our thesis?"
  - "What's our downside scenario and probability?"
  - "What catalysts could fail to materialize?"
- Bull case agents (Value, Growth, Quality, Catalyst Detective) SHALL respond to challenges with evidence-based rebuttals
- Portfolio Manager SHALL incorporate challenge outcomes into final decision:
  - Adjust position sizing based on identified risks
  - Set tighter stop-losses if downside risks significant
  - Reject trade if challenges expose fatal flaws in thesis
- Final recommendation SHALL document:
  - Key risks identified in challenge process
  - How position sizing/stop-loss accounts for risks
  - Why bullish thesis withstands scrutiny despite challenges
- All challenge rounds logged in audit trail for learning and compliance

**FR-2.7: Agent Management & Configurability**

**FR-2.7.1: Agent Enable/Disable**
- System SHALL allow users to enable/disable any analysis agent via configuration (web UI or config file)
- Disabled agents SHALL NOT run during analysis (cost savings, performance optimization)
- Minimum 3 agents MUST remain enabled (ensures multi-perspective analysis)
- Agent status changes SHALL take effect on next scheduled run (or immediately for on-demand analysis)
- UI SHALL clearly show which agents are active in current configuration

**FR-2.7.2: Agent Weighting & Influence**
- System SHALL allow users to configure agent voting weights (range: 0.1 to 3.0, default: 1.0 for all)
- Weight examples:
  - Value-focused strategy: Value Investor 2.5x, Quality 2.0x, Growth 0.3x, Technical 0.5x
  - Growth-focused strategy: Growth 2.5x, Catalyst 2.0x, Value 0.5x, Quality 0.8x
  - Balanced strategy: All agents 1.0x
- Weighted voting SHALL be reflected in Portfolio Manager decision logic:
  - BUY threshold: (Weighted bullish votes / Total weighted votes) ≥ 65%
  - Higher-weighted agents have proportionally more influence on decisions
- UI SHALL provide preset strategy templates:
  - "Conservative Value" (Value 2.0x, Quality 1.5x, Growth 0.5x, Technical 0.5x)
  - "Aggressive Growth" (Growth 2.0x, Catalyst 1.5x, Value 0.5x, Quality 0.5x)
  - "Balanced" (All agents 1.0x)
  - "Technical Momentum" (Technical 2.0x, Sentiment 1.5x, fundamentals 0.5x)
  - "Dividend Income" (Value 2.5x, Quality 2.0x, Growth 0.3x, Catalyst 0.5x)

**FR-2.7.3: Custom Agent Integration**
- System SHALL provide documented agent interface specification (input schema, output schema, reasoning format)
- Users SHALL be able to add custom agents via:
  - Python class implementing `AnalysisAgent` interface
  - Custom LLM prompt with structured output format (Pydantic models)
  - External API integration (call third-party analysis service, return standardized format)
- Custom agents SHALL participate in weighted voting alongside built-in agents
- Custom agents SHALL be validated before activation (schema compliance check, test run)
- System SHALL sandbox custom agents (resource limits, timeout protection, error handling)

**FR-2.7.4: Agent Performance Tracking**
- System SHALL track performance attribution per agent:
  - Win rate when agent voted BUY (% of profitable trades)
  - Average gain when agent voted BUY
  - False positive rate (agent voted BUY, stock declined)
  - Cost per agent (LLM token usage, API calls)
- UI SHALL display agent performance dashboard:
  - Ranking by contribution to overall returns (ROI per agent)
  - Individual agent win rates over time
  - Cost-benefit analysis (returns generated vs. operating cost)
  - Agent agreement patterns (which agents correlate, which provide unique signals)
- Users SHALL be able to disable underperforming agents based on historical data
- System SHALL recommend agent configuration optimizations ("Sentiment Agent 45% win rate, consider disabling")

**FR-2.7.5: Agent Configuration Persistence**
- System SHALL store agent configurations in database:
  - Active/inactive status per agent
  - Agent weights per strategy template
  - Custom agent definitions (code, prompts, API integrations)
  - Strategy template selections
- Configurations SHALL be versioned (track changes over time, rollback capability)
- Users SHALL be able to export/import configurations (JSON format for backup, sharing)
- System SHALL log all configuration changes in audit trail (who, what, when, why)
- Configuration changes SHALL validate before saving (minimum 3 agents enabled, weights in valid range)

**FR-2.7.6: Discovery Agent Configurability**
- System SHALL allow users to enable/disable any discovery agent independently
- Users SHALL be able to configure discovery agent parameters:
  - **News Scanner:** Customize news sources (add/remove domains), keywords, languages
  - **Fundamental Screener:** Define custom screens (e.g., "P/E < 10 AND Debt/Equity < 0.3 AND ROE > 15%")
  - **Volume Spike Agent:** Adjust threshold (2x vs. 3x vs. 5x average volume)
  - **Analyst Activity:** Filter by broker credibility score, upgrade strength
  - **Insider Trading:** Minimum transaction size threshold (£50k, £100k, £500k)
- Discovery agent configuration changes SHALL preserve signal convergence logic
- System SHALL validate custom fundamental screens for syntax errors before activation

### FR-3: Three-Tier Tracking System

**FR-3.1: Tier 1 - Active Portfolio**
- Track all current holdings:
  - Entry date, entry price, current price
  - P&L (absolute £ and %)
  - Stop-loss level, target price
  - Days held, original thesis
- Daily monitoring for SELL signals:
  - Stop-loss breach
  - Target price reached
  - Fundamental deterioration
  - Better opportunity requires capital (opportunity cost)
- Update user daily in morning report

**FR-3.2: Tier 2 - Active Watchlist** (MVP: Basic, Growth: Advanced)
- Store stocks with conditional triggers:
  - **Price-based:** "BUY if price drops to £8.50" (value emerged at lower price)
  - **Event-based:** "BUY if insider buying occurs" (management confidence signal)
  - **Macro-based:** "BUY if sector rotation favors healthcare" (timing macro environment)
  - **Technical:** "BUY if breaks above resistance at £12" (momentum confirmation)
- Each watchlist entry includes:
  - Ticker, current price, trigger condition(s)
  - Original analysis thesis
  - Trigger expiry date (stale after 30-60 days)
- Monitor daily for trigger conditions
- **Re-validation Protocol** (Growth feature):
  - When trigger fires, re-run ALL 8 analysis agents
  - Compare new analysis to original thesis
  - Outcomes:
    - **Thesis validated:** Proceed with BUY
    - **Thesis invalidated:** Remove from watchlist (avoided value trap!)
    - **Thesis uncertain:** Adjust trigger or extend monitoring

**FR-3.3: Tier 3 - Research Queue**
- Stocks currently being investigated (scored 31-60, not yet actionable)
- Background monitoring for additional signals
- Auto-promote to deep analysis if score increases to 61+
- Auto-remove if no new signals after 7 days (stale)

### FR-4: Reporting & Notifications

**FR-4.1: Daily Morning Report**
- Deliver by 7:00 AM GMT every trading day (Monday-Friday)
- Report sections:
  1. **Executive Summary:** Quick snapshot (# of opportunities, portfolio status)
  2. **NEW BUY RECOMMENDATIONS:** (0-3 typical)
     - Ticker, company name, current price
     - Recommended action (BUY), quantity, stop-loss, target
     - Conviction level (high/medium/low)
     - Analyst consensus (e.g., "8/8 agents bullish, avg confidence 78%")
     - Key reasons (top 3 bullet points)
     - Risks (top 2-3 concerns from risk manager)
  3. **PORTFOLIO ALERTS:**
     - Stop-loss alerts (approaching or breached)
     - Target price reached
     - SELL recommendations
     - Performance summary (daily P&L, total P&L)
  4. **WATCHLIST TRIGGERS:**
     - Which watchlist stocks triggered conditions
     - Re-validation results (BUY now or remove)
  5. **MARKET CONTEXT:** (weekly, not daily)
     - Macro environment summary (UK economy, interest rates, recession risk)
     - Sector rotation analysis (favored/disfavored sectors)
  6. **DISCOVERY SUMMARY:**
     - How many stocks scanned
     - Top signals by source (news, insiders, fundamentals, etc.)
     - Interesting but not actionable (background trends)

**FR-4.2: Report Delivery Channels**
- Email: HTML-formatted email to configured address
- Web Dashboard: React frontend displays same report with interactive charts
- (Future) Mobile push notifications for urgent alerts

**FR-4.3: On-Demand Reporting**
- User can request detailed analysis of any UK stock via web UI
- User can view full agent reasoning (show all 8 agents' detailed analysis)
- User can access historical reports (last 90 days)

### FR-5: Data Management & Integration

**Philosophy:** Simplicity over complexity. Three specialized providers deliver institutional-grade UK data without the fragmentation, rate limit juggling, and maintenance overhead of multi-source aggregation.

**FR-5.1: 3-Tier Data Architecture**

System SHALL use a simplified three-tier data architecture optimized for UK market coverage, eliminating the complexity of managing multiple free APIs with inconsistent data quality and rate limits.

**Tier 1: Core Data Engine - EODHD All-In-One** (~£85/month)
  - Historical EOD prices (OHLCV) for 150,000+ tickers including LSE, FTSE All-Share
  - 30+ years historical data coverage
  - Financial metrics (P/E, P/B, ROE, debt ratios, growth rates, margins)
  - Company fundamentals (income statements, balance sheets, cash flow - quarterly & annual)
  - Corporate actions (dividends, splits, buybacks)
  - Earnings calendar
  - 100,000 API calls/day limit (generous allowance for Phase 1)
- **Free Tier Supplements:**
  - **Finnhub Free** (60/min, 800/day): Real-time data, news, sentiment, fundamentals cross-validation
  - **Alpha Vantage Free** (25/day): News sentiment, backup price data
  - **Financial Modeling Prep Free** (250/day): Social sentiment, backup fundamentals
  - **LSE Official 15-min delayed** (FREE since Jan 2025 retail fee waiver): Official LSE data
  - **yfinance** (FREE): Emergency fallback only if all paid APIs unavailable
- Handle LSE ticker format: VOD.L, BP.L, HSBC.L (EODHD uses exchange code 'LSE', MIC: XLON)
- Support pence vs. pounds conversion (some UK stocks quoted in pence, divide by 100)
- Currency handling: GBP primary, support multi-currency for international holdings

**FR-5.2: News API Integration**
- Integrate NewsAPI.org for UK financial news:
  - Configured domains: bbc.co.uk, ft.com, reuters.com, telegraph.co.uk, cityam.com, thisismoney.co.uk
  - Keywords: FTSE, LSE, "stock market", shares, trading
  - Fetch 100+ articles per morning scan
- Alternative: RSS feeds from UK news sources (free fallback)

**FR-5.3: Data Caching**
- Cache price data to reduce API calls (existing system has caching)
- Cache news articles (valid for 24 hours)
- Cache financial metrics (valid for 7 days, refresh on earnings releases)
- Cache key format: UK_{ticker}_{datatype}_{date}

**FR-5.4: Data Validation & Quality Checks**
- Reject price data with >20% single-day moves (likely error, check for corporate actions)
- Verify financial data consistency (e.g., debt/equity ratio matches balance sheet)
- Flag missing data and use fallback sources or skip analysis
- Log all data quality issues for review

**FR-5.5: Audit Trail**
- Log every agent decision with:
  - Timestamp, ticker, agent name, model used (GPT-4o, Claude, etc.)
  - Input data (prices, news, financials)
  - Output (signal, confidence, reasoning)
  - LLM token usage and cost
- Store trade decisions:
  - Recommended trades (with full rationale)
  - User approvals/rejections
  - Actual trades executed
  - Outcome (profit/loss)
- Retention: 2 years minimum (support learning + potential regulatory review)

**FR-5.6: Web Scraping Architecture**

System SHALL support ethical web scraping for data sources without official APIs (director dealings, RNS announcements, supplemental news).

**Scraping Requirements:**
- **Target Sources:**
  - **Investegate** (investegate.co.uk): Director dealings, RNS announcements, corporate actions
  - **LSE Director Deals** (lse.co.uk/share-prices/recent-directors-deals.html): Backup director dealings
  - **UK News Sites** (optional): BBC Business, Financial Times, Reuters UK (if API limits exhausted)
- **Ethical & Legal Compliance (2025 Standards):**
  - MUST check and respect robots.txt BEFORE scraping any domain (legally significant under GDPR)
  - MUST use real User-Agent string identifying bot: "AIHedgeFund/1.0 (Trading Bot; contact@example.com)"
  - MUST implement rate limiting: Minimum 10-15 seconds between requests per domain
  - MUST cache aggressively to minimize requests (store scraped data, never re-scrape same content)
  - ONLY scrape public data (no paywalls, no authentication-required content, no terms-of-service violations)
  - MUST implement retry logic with exponential backoff (respect server load)
  - MUST monitor for HTTP 429 (Too Many Requests) and back off immediately
  - MUST log all scraping activity (URL, timestamp, success/failure) for compliance audit
- **Implementation Stack:**
  - **Python libraries:** BeautifulSoup4 (HTML parsing), Requests (HTTP), Scrapy (optional for advanced scraping)
  - **Rate limiting:** Custom rate limiter class enforcing minimum interval between requests
  - **robots.txt parser:** urllib.robotparser or reppy library
  - **Error handling:** Graceful failures, log errors, fallback to cached data

**Director Dealings Scraping (Investegate):**
- **Schedule:** Daily at 7:00 AM GMT (after overnight RNS releases)
- **Target URL:** https://www.investegate.co.uk/category/directors-dealings
- **Data Extracted:**
  - Company name and ticker
  - Director name and role
  - Transaction type (Purchase/Sale)
  - Number of shares
  - Price per share
  - Transaction date
  - Total value
- **Storage:** Store in `director_dealings` database table with deduplication (don't store same transaction twice)
- **Alerting:** High-value purchases (>£100k) trigger immediate notification to Insider Trading Agent

**RNS Announcements Scraping:**
- **Schedule:** Every 2 hours during market hours (8 AM - 5 PM GMT)
- **Categories to monitor:**
  - Mergers & Acquisitions
  - Share Buyback Programs
  - Dividend Declarations
  - Trading Updates
  - Results/Earnings
- **NLP Processing:** Use LLM (GPT-4o or Claude) to extract key facts from announcement text
- **Storage:** Store in `rns_announcements` table with full text + extracted summary

**Scraping Code Example (Conceptual):**
```python
import time
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

class EthicalScraper:
    def __init__(self, base_url, rate_limit_seconds=15):
        self.base_url = base_url
        self.rate_limit = rate_limit_seconds
        self.last_request_time = 0
        self.user_agent = "AIHedgeFund/1.0 (Trading Bot; longy@example.com)"
        self.robots_parser = RobotFileParser()
        self.check_robots_txt()

    def check_robots_txt(self):
        """Check robots.txt before scraping (MANDATORY)"""
        robots_url = f"{self.base_url}/robots.txt"
        self.robots_parser.set_url(robots_url)
        self.robots_parser.read()

    def can_fetch(self, url):
        """Check if scraping is allowed per robots.txt"""
        return self.robots_parser.can_fetch(self.user_agent, url)

    def rate_limited_get(self, url):
        """Enforce rate limiting between requests"""
        if not self.can_fetch(url):
            raise PermissionError(f"robots.txt disallows scraping: {url}")

        # Enforce rate limit
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            time.sleep(sleep_time)

        headers = {'User-Agent': self.user_agent}
        response = requests.get(url, headers=headers, timeout=30)
        self.last_request_time = time.time()

        # Check for rate limiting response
        if response.status_code == 429:
            raise Exception("Rate limited by server - back off")

        return response

    def scrape_director_dealings(self, max_pages=3):
        """Scrape Investegate director dealings"""
        dealings = []
        url = f"{self.base_url}/category/directors-dealings"

        for page in range(1, max_pages + 1):
            response = self.rate_limited_get(f"{url}?page={page}")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Parse announcements (implementation-specific)
            # Extract: company, director, type, shares, price, date
            # ... parsing logic ...

        return dealings
```

**Fallback Strategy:**
- If web scraping fails (site structure changed, blocked, robots.txt disallows):
  - Use cached data from last successful scrape (up to 7 days old acceptable)
  - Alert user that director dealings data is stale
  - Consider paid alternative: Smart Insider API (~£50/month) if scraping consistently fails

**FR-5.7: Multi-Source Data Aggregation Strategy**

System SHALL combine data from multiple sources to maximize coverage, ensure redundancy, and enable cross-validation.

**Aggregation Patterns:**

**1. Primary + Cross-Validation Pattern** (Fundamentals):
- **Use Case:** Financial metrics where accuracy is critical
- **Strategy:**
  - Fetch from primary source (EODHD fundamentals)
  - Cross-validate key metrics with secondary source (Finnhub fundamentals)
  - If discrepancy >10%, flag for manual review
  - Log which source was used for each metric (data lineage)
- **Example:** P/E ratio from EODHD = 15.2, Finnhub = 15.4 → Accept (within tolerance)
- **Example:** Debt/Equity from EODHD = 0.8, Finnhub = 1.5 → Flag (>10% diff, investigate)

**2. Priority Fallback Pattern** (Price Data):
- **Use Case:** Real-time/EOD prices where availability matters more than perfect accuracy
- **Strategy:**
  - Try sources in priority order until success
  - Cache successful result
  - Log which source provided data
- **Priority Order:**
  1. EODHD (primary paid, 100k/day limit) → historical EOD prices
  2. LSE Official (free 15-min delay) → recent prices
  3. Finnhub Free (60/min, 800/day) → real-time fallback
  4. Alpha Vantage Free (25/day) → backup EOD
  5. yfinance (fragile) → emergency only

**3. Aggregation + Weighting Pattern** (Sentiment):
- **Use Case:** Sentiment scores where multiple perspectives improve accuracy
- **Strategy:**
  - Fetch sentiment from ALL available sources
  - Aggregate using weighted average
  - Weight by source credibility/historical accuracy
- **Sources & Weights:**
  - Finnhub Social Sentiment (Reddit, Twitter): Weight 1.0
  - FMP Social Sentiment (Reddit, Yahoo Finance, StockTwits): Weight 1.0
  - Alpha Vantage News Sentiment: Weight 1.2 (news > social for UK stocks)
  - EODHD News Sentiment (if available): Weight 1.5 (proprietary algorithm)
- **Calculation:**
  ```python
  weighted_sentiment = (
      (finnhub_score * 1.0) +
      (fmp_score * 1.0) +
      (av_score * 1.2) +
      (eodhd_score * 1.5)
  ) / (1.0 + 1.0 + 1.2 + 1.5)
  ```
- **Output:** Single aggregated sentiment score (-100 to +100) with confidence level based on source agreement

**4. First-Available Pattern** (News):
- **Use Case:** News articles where coverage breadth matters
- **Strategy:**
  - Fetch from ALL free sources in parallel (no priority, maximize coverage)
  - Deduplicate by article title similarity (>80% match = duplicate)
  - Combine into unified news feed
- **Sources:**
  - Finnhub News API (800/day)
  - Alpha Vantage News (25/day)
  - Investegate RNS scraping (unlimited, rate-limited)
  - EODHD News (if using higher tier)
- **Deduplication:** Use fuzzy string matching (difflib, Levenshtein distance) to remove duplicate articles from different sources

**5. Specialized Source Pattern** (Director Dealings):
- **Use Case:** Data only available from specific source
- **Strategy:**
  - Primary: Investegate scraping (most comprehensive UK director dealings)
  - Backup: LSE.co.uk scraping
  - Validation: Cross-check high-value transactions (>£500k) against both sources
- **No fallback to generic APIs** (director dealings not available in free price APIs)

**Data Aggregator Architecture:**
```python
class DataAggregator:
    def __init__(self):
        self.sources = {
            'eodhd': EODHDClient(api_key=config.EODHD_KEY),
            'finnhub': FinnhubClient(api_key=config.FINNHUB_KEY),
            'alphavantage': AlphaVantageClient(api_key=config.AV_KEY),
            'fmp': FMPClient(api_key=config.FMP_KEY),
            'lse_official': LSEClient(),
            'investegate': InvestegateScraper(),
            'yfinance': YFinanceClient()
        }
        self.cache = CacheLayer(redis_client)

    def get_price_data(self, ticker, start_date, end_date):
        """Priority fallback pattern for price data"""
        cache_key = f"price:{ticker}:{start_date}:{end_date}"

        if cached := self.cache.get(cache_key):
            return cached

        # Try sources in priority order
        for source_name in ['eodhd', 'lse_official', 'finnhub', 'alphavantage', 'yfinance']:
            try:
                data = self.sources[source_name].get_prices(ticker, start_date, end_date)
                self.cache.set(cache_key, data, ttl=3600)  # Cache 1 hour
                logger.info(f"Price data from {source_name}")
                return data
            except Exception as e:
                logger.warning(f"{source_name} failed: {e}, trying next source")

        raise Exception("All price data sources failed")

    def get_aggregated_sentiment(self, ticker):
        """Aggregation + weighting pattern for sentiment"""
        sentiments = []

        # Fetch from all sources (parallel)
        try:
            finnhub_sentiment = self.sources['finnhub'].get_sentiment(ticker)
            sentiments.append(('finnhub', finnhub_sentiment, 1.0))
        except Exception as e:
            logger.warning(f"Finnhub sentiment failed: {e}")

        try:
            fmp_sentiment = self.sources['fmp'].get_social_sentiment(ticker)
            sentiments.append(('fmp', fmp_sentiment, 1.0))
        except Exception as e:
            logger.warning(f"FMP sentiment failed: {e}")

        try:
            av_sentiment = self.sources['alphavantage'].get_news_sentiment(ticker)
            sentiments.append(('av', av_sentiment, 1.2))
        except Exception as e:
            logger.warning(f"Alpha Vantage sentiment failed: {e}")

        # Weighted aggregation
        if not sentiments:
            return None

        weighted_sum = sum(score * weight for (_, score, weight) in sentiments)
        total_weight = sum(weight for (_, _, weight) in sentiments)
        aggregated_score = weighted_sum / total_weight

        # Confidence based on source agreement
        variance = np.var([score for (_, score, _) in sentiments])
        confidence = 1.0 / (1.0 + variance)  # Lower variance = higher confidence

        return {
            'score': aggregated_score,
            'confidence': confidence,
            'sources': [name for (name, _, _) in sentiments]
        }
```

**FR-5.8: Data Source Priority & Fallback Logic**

System SHALL implement intelligent fallback logic to ensure data availability even when primary sources fail.

**Fallback Hierarchy by Data Type:**

| **Data Type** | **Priority 1** | **Priority 2** | **Priority 3** | **Priority 4** | **Priority 5** |
|---------------|----------------|----------------|----------------|----------------|----------------|
| **EOD Prices** | EODHD (paid) | LSE Official (free) | Finnhub Free | Alpha Vantage Free | yfinance (emergency) |
| **Real-time Prices** | LSE Official 15-min | Finnhub Free | EODHD intraday (if upgraded) | - | - |
| **Fundamentals** | EODHD | Finnhub Free | FMP Free | - | - |
| **News** | Finnhub Free | Alpha Vantage Free | Investegate RNS | EODHD (if tier 3) | - |
| **Sentiment** | Aggregate All | (Finnhub + FMP + AV) | - | - | - |
| **Director Dealings** | Investegate scrape | LSE.co.uk scrape | MarketBeat (manual) | - | - |
| **Earnings Calendar** | EODHD | Finnhub Free | FMP Free | - | - |
| **Corporate Actions** | EODHD | Investegate RNS | - | - | - |
| **Technical Indicators** | TA-Lib local | Alpha Vantage API | - | - | - |

**Fallback Trigger Conditions:**
- **Source Unavailable:** HTTP 5xx errors, timeouts (>30s), connection refused
- **Rate Limit Hit:** HTTP 429, or daily quota exhausted (tracked internally)
- **Data Quality Issues:** Missing critical fields, impossible values (price < 0, volume < 0)
- **Stale Data:** Data timestamp older than acceptable threshold (e.g., prices >24 hours old for EOD)

**Fallback Behavior:**
- **Automatic:** System tries next source automatically without user intervention
- **Logged:** All fallback events logged with reason, timestamp, affected tickers
- **Alerted:** If ALL sources fail for critical data type, alert user via configured channel
- **Cached:** Use cached data up to 7 days old if all live sources fail (mark as stale in report)

**Retry Logic:**
- **Transient Failures:** Retry 3x with exponential backoff (1s, 3s, 9s delays)
- **Rate Limit Failures:** Do NOT retry immediately, wait until next scheduled run or quota resets
- **Permanent Failures:** Skip retries, move to next fallback source immediately

**Circuit Breaker Pattern:**
- If source fails 5 consecutive times, temporarily disable for 1 hour (prevent wasting time on dead source)
- After 1 hour, re-enable and retry (source may have recovered)
- Alert user if primary source (EODHD) circuit broken (indicates serious issue)

**FR-5.9: Adding New Data Sources (Developer Process)**

System SHALL provide clear process for developers to add new data sources without modifying core system logic.

**Step-by-Step Process to Add New Source:**

**Step 1: Create Data Source Adapter Class**
- Create new Python file: `src/data_sources/adapters/new_source_adapter.py`
- Implement `DataSourceAdapter` interface (abstract base class)
- Required methods:
  ```python
  class NewSourceAdapter(DataSourceAdapter):
      def __init__(self, api_key=None, **config):
          self.api_key = api_key
          self.base_url = "https://api.newsource.com"
          self.rate_limiter = RateLimiter(calls_per_minute=60)

      def get_prices(self, ticker, start_date, end_date):
          """Fetch price data and return in standard format"""
          # Implementation-specific API calls
          raw_data = self._api_call(f"/prices/{ticker}")
          # Normalize to standard format (see FR-5.10)
          return self._normalize_prices(raw_data)

      def get_fundamentals(self, ticker):
          """Fetch fundamentals and return in standard format"""
          raw_data = self._api_call(f"/fundamentals/{ticker}")
          return self._normalize_fundamentals(raw_data)

      def _api_call(self, endpoint, params=None):
          """Internal helper for API calls with rate limiting"""
          self.rate_limiter.wait()  # Enforce rate limit
          response = requests.get(
              f"{self.base_url}{endpoint}",
              headers={'Authorization': f'Bearer {self.api_key}'},
              params=params,
              timeout=30
          )
          response.raise_for_status()
          return response.json()

      def _normalize_prices(self, raw_data):
          """Convert source-specific format to standard format"""
          return {
              'ticker': raw_data['symbol'],
              'date': raw_data['date'],
              'open': float(raw_data['o']),
              'high': float(raw_data['h']),
              'low': float(raw_data['l']),
              'close': float(raw_data['c']),
              'volume': int(raw_data['v']),
              'source': 'new_source'
          }
  ```

**Step 2: Register Adapter in Configuration**
- Add source to `config/data_sources.yaml`:
  ```yaml
  data_sources:
    new_source:
      adapter_class: "data_sources.adapters.new_source_adapter.NewSourceAdapter"
      api_key: "${NEW_SOURCE_API_KEY}"  # Read from environment variable
      enabled: true
      priority: 3  # Priority in fallback hierarchy (1 = highest)
      rate_limit:
        calls_per_minute: 60
        calls_per_day: 800
      cost:
        per_call: 0.001  # For cost tracking
        monthly_quota: 800  # For budget alerts
      capabilities:
        - prices
        - fundamentals
        - news
  ```

**Step 3: Add API Credentials**
- Add API key to `.env` file (NEVER commit to git):
  ```
  NEW_SOURCE_API_KEY=your_api_key_here
  ```

**Step 4: Write Unit Tests**
- Create test file: `tests/data_sources/test_new_source_adapter.py`
- Test cases:
  - Successful data fetch
  - Rate limiting enforcement
  - Error handling (404, 500, timeout)
  - Data normalization correctness
  - Fallback behavior
- Run tests: `pytest tests/data_sources/test_new_source_adapter.py`

**Step 5: Update Fallback Priorities**
- Modify `src/data_aggregator.py` to include new source in fallback hierarchy
- Add to priority list for relevant data types:
  ```python
  PRICE_DATA_PRIORITY = ['eodhd', 'lse_official', 'new_source', 'finnhub', 'alphavantage', 'yfinance']
  ```

**Step 6: Document the Source**
- Add documentation to `docs/data-sources.md`:
  - Source name, URL, pricing
  - API rate limits
  - Data coverage (markets, tickers)
  - Data quality notes (UK coverage, accuracy, latency)
  - Example API calls
  - Known issues or limitations

**Step 7: Deploy and Monitor**
- Deploy updated code
- Monitor logs for new source usage
- Track cost vs. value (API calls used, data quality contribution)
- If source proves valuable, consider upgrading priority
- If source unreliable, consider disabling or removing

**Adding New News Source (Web Scraping):**

If adding news source WITHOUT API (requires scraping):

**Step 1: Check Legal/Ethical Feasibility**
- Check robots.txt: `curl https://newssite.com/robots.txt`
- Check terms of service: Ensure scraping is allowed
- Verify no authentication/paywall required
- Only proceed if scraping is legal and ethical

**Step 2: Create Scraper Class**
- Create `src/data_sources/scrapers/newssite_scraper.py`
- Inherit from `EthicalScraper` base class (enforces rate limiting, robots.txt checks)
- Implement parsing logic:
  ```python
  class NewsSiteScraper(EthicalScraper):
      def __init__(self):
          super().__init__(
              base_url="https://newssite.com",
              rate_limit_seconds=15  # 15 seconds between requests
          )

      def scrape_uk_stock_news(self, max_articles=50):
          """Scrape UK stock news from news site"""
          articles = []
          url = f"{self.base_url}/markets/uk-stocks"

          response = self.rate_limited_get(url)
          soup = BeautifulSoup(response.text, 'html.parser')

          # Parse articles (site-specific selectors)
          article_elements = soup.find_all('article', class_='stock-news')

          for elem in article_elements[:max_articles]:
              article = {
                  'title': elem.find('h2').text.strip(),
                  'url': elem.find('a')['href'],
                  'published_date': elem.find('time')['datetime'],
                  'summary': elem.find('p', class_='summary').text.strip(),
                  'source': 'newssite',
                  'tickers': self._extract_tickers(elem.text)
              }
              articles.append(article)

          return articles

      def _extract_tickers(self, text):
          """Extract mentioned tickers from article text"""
          # Use regex to find LSE ticker patterns (e.g., VOD.L, BP.L)
          import re
          ticker_pattern = r'\b([A-Z]{2,5}\.L)\b'
          return re.findall(ticker_pattern, text)
  ```

**Step 3: Schedule Scraping**
- Add scraper to scheduled tasks in `src/scheduler/tasks.py`:
  ```python
  @scheduler.scheduled_job('cron', hour=6, minute=0)
  def scrape_newssite_morning():
      scraper = NewsSiteScraper()
      articles = scraper.scrape_uk_stock_news(max_articles=50)
      store_articles_in_db(articles)
      logger.info(f"Scraped {len(articles)} articles from newssite")
  ```

**Step 4: Monitor for Changes**
- Set up alerts if scraping fails (site structure changed)
- Implement automatic retry with fallback to other news sources
- Document CSS selectors used (for future maintenance)

**FR-5.10: Data Normalization Pipeline**

System SHALL normalize data from different sources into common internal format to ensure agent logic is source-agnostic.

**Why Normalization Matters:**
- Different APIs return data in different formats (JSON structure, field names, data types, units)
- Agents should NOT know which source data came from (separation of concerns)
- Makes adding new sources easy (just implement normalization logic)
- Enables cross-validation (compare same data from different sources)

**Standard Internal Schemas:**

**1. Price Data Schema (OHLCV):**
```python
{
    'ticker': 'VOD.L',             # Standardized format: {symbol}.{exchange}
    'date': '2025-11-19',          # ISO 8601 date format
    'open': 75.50,                 # Float, GBP
    'high': 76.20,                 # Float, GBP
    'low': 75.10,                  # Float, GBP
    'close': 75.80,                # Float, GBP
    'adjusted_close': 75.80,       # Adjusted for splits/dividends
    'volume': 12500000,            # Integer
    'currency': 'GBP',             # ISO 4217 currency code
    'source': 'eodhd',             # Which API provided this data
    'fetched_at': '2025-11-19T14:30:00Z'  # ISO 8601 timestamp
}
```

**2. Fundamentals Schema:**
```python
{
    'ticker': 'VOD.L',
    'fiscal_period': '2024-Q2',    # YYYY-QN or YYYY for annual
    'report_date': '2024-06-30',
    'currency': 'GBP',
    'financials': {
        'revenue': 10500000000,     # In currency units
        'net_income': 1200000000,
        'total_assets': 50000000000,
        'total_liabilities': 30000000000,
        'shareholders_equity': 20000000000,
        'operating_cash_flow': 3000000000,
        'free_cash_flow': 2500000000
    },
    'metrics': {
        'market_cap': 25000000000,
        'pe_ratio': 15.2,
        'pb_ratio': 1.8,
        'debt_to_equity': 0.65,
        'roe': 0.18,               # Return on Equity (18%)
        'roa': 0.08,               # Return on Assets (8%)
        'current_ratio': 1.5,
        'profit_margin': 0.11      # 11%
    },
    'source': 'eodhd',
    'fetched_at': '2025-11-19T14:30:00Z'
}
```

**3. News Article Schema:**
```python
{
    'article_id': 'uuid-or-hash',
    'title': 'Vodafone Reports Strong Q2 Earnings',
    'url': 'https://newssite.com/article/12345',
    'published_date': '2025-11-19T09:30:00Z',  # ISO 8601
    'source': 'finnhub',           # Or 'investegate', 'alphavantage', etc.
    'summary': 'Brief article summary text...',
    'full_text': 'Complete article text...' (optional),
    'tickers_mentioned': ['VOD.L', 'BT.L'],
    'sentiment': {
        'score': 0.75,             # -1.0 (negative) to +1.0 (positive)
        'label': 'positive',       # 'positive', 'negative', 'neutral'
        'confidence': 0.82         # 0.0 to 1.0
    },
    'categories': ['earnings', 'telecommunications'],
    'language': 'en',
    'fetched_at': '2025-11-19T10:00:00Z'
}
```

**4. Director Dealing Schema:**
```python
{
    'dealing_id': 'unique-hash',
    'ticker': 'VOD.L',
    'company_name': 'Vodafone Group plc',
    'director_name': 'John Smith',
    'director_role': 'Chief Executive Officer',
    'transaction_type': 'Purchase',  # 'Purchase' or 'Sale'
    'transaction_date': '2025-11-15',
    'shares': 50000,               # Number of shares
    'price_per_share': 75.50,      # GBP
    'total_value': 3775000,        # GBP (shares * price)
    'currency': 'GBP',
    'shares_held_after': 150000,   # Total shares held after transaction
    'source': 'investegate',
    'announcement_url': 'https://investegate.co.uk/...',
    'fetched_at': '2025-11-19T07:00:00Z'
}
```

**5. Sentiment Schema (Aggregated):**
```python
{
    'ticker': 'VOD.L',
    'date': '2025-11-19',
    'social_sentiment': {
        'score': 0.65,             # -1.0 to +1.0
        'sources': ['finnhub', 'fmp'],
        'confidence': 0.78,
        'sample_size': 150         # Number of social mentions analyzed
    },
    'news_sentiment': {
        'score': 0.72,
        'sources': ['alphavantage', 'eodhd'],
        'confidence': 0.85,
        'articles_analyzed': 12
    },
    'aggregated_sentiment': {
        'score': 0.69,             # Weighted average of social + news
        'confidence': 0.82,
        'trend': 'improving'       # 'improving', 'deteriorating', 'stable'
    },
    'calculated_at': '2025-11-19T14:00:00Z'
}
```

**Normalization Implementation:**

Each data source adapter implements `_normalize_*()` methods:

```python
# Example: EODHD adapter normalizing price data
class EODHDAdapter(DataSourceAdapter):
    def get_prices(self, ticker, start_date, end_date):
        raw_data = self._api_call(f"/eod/{ticker}", {'from': start_date, 'to': end_date})
        return [self._normalize_price(ticker, record) for record in raw_data]

    def _normalize_price(self, ticker, raw):
        """Convert EODHD format to standard schema"""
        return {
            'ticker': ticker,
            'date': raw['date'],             # Already ISO format
            'open': float(raw['open']),
            'high': float(raw['high']),
            'low': float(raw['low']),
            'close': float(raw['close']),
            'adjusted_close': float(raw['adjusted_close']),
            'volume': int(raw['volume']),
            'currency': 'GBP',               # Assume GBP for .L tickers
            'source': 'eodhd',
            'fetched_at': datetime.utcnow().isoformat() + 'Z'
        }

# Example: Finnhub adapter normalizing price data (different API format)
class FinnhubAdapter(DataSourceAdapter):
    def get_prices(self, ticker, start_date, end_date):
        raw_data = self._api_call(f"/stock/candle", {
            'symbol': ticker,
            'resolution': 'D',
            'from': int(start_date.timestamp()),
            'to': int(end_date.timestamp())
        })

        # Finnhub returns arrays, not list of dicts
        prices = []
        for i in range(len(raw_data['t'])):
            prices.append(self._normalize_price(ticker, raw_data, i))
        return prices

    def _normalize_price(self, ticker, raw, index):
        """Convert Finnhub format to standard schema"""
        return {
            'ticker': ticker,
            'date': datetime.fromtimestamp(raw['t'][index]).strftime('%Y-%m-%d'),
            'open': float(raw['o'][index]),
            'high': float(raw['h'][index]),
            'low': float(raw['l'][index]),
            'close': float(raw['c'][index]),
            'adjusted_close': float(raw['c'][index]),  # Finnhub doesn't provide adjusted
            'volume': int(raw['v'][index]),
            'currency': 'GBP',
            'source': 'finnhub',
            'fetched_at': datetime.utcnow().isoformat() + 'Z'
        }
```

**Benefits of Normalization:**
- ✅ Agents receive consistent data format regardless of source
- ✅ Easy to swap data sources without changing agent code
- ✅ Cross-validation possible (compare normalized data from different sources)
- ✅ Source attribution maintained (can trace back to origin)
- ✅ Adding new source = implement normalization, rest of system works automatically

### FR-6: Automation & Scheduling

**FR-6.1: Batch Processing (Default: Overnight, Fully Configurable)**
- Scheduler runs at user-configured time(s) (default: daily at 1:00 AM GMT Monday-Friday)
- Execution stages (6-hour window, times adjust based on configured start time):
  1. **Hour 1:** Data collection (prices, volumes, news, insider trades, corporate actions)
  2. **Hour 2:** Discovery agents run, generate signals, score tickers (scope: configured universe or custom list)
  3. **Hour 3:** Deep analysis for high-scoring stocks (enabled analysis agents only)
  4. **Hour 4:** Risk management, portfolio decisions, adversarial challenge protocol
  5. **Hour 5:** Watchlist processing, re-validation (if configured)
  6. **Hour 6:** Report generation and delivery in configured format(s) and channel(s)
- User-configurable execution days (default: Monday-Friday, can include/exclude weekends, holidays)
- Support for multiple scheduled runs per day (e.g., morning + afternoon market update)
- Error handling: Alert user via configured channels if any stage fails

**FR-6.2: System Reliability**
- Target uptime: 95%+ during trading days
- Graceful degradation: If API unavailable, use cached data and flag in report
- Retry logic: Failed API calls retry 3x with exponential backoff
- Manual override: User can trigger immediate analysis via web UI

**FR-6.3: Cost Monitoring**
- Track daily LLM token usage and cost
- Track API call counts (stay within rate limits)
- Alert user if monthly cost exceeds configured budget (default £200 Phase 1)
- Optimize costs:
  - Use batch processing during off-peak hours
  - Cache aggressively
  - Only run deep analysis on high-scoring opportunities (funnel approach)

**FR-6.4: Scheduling Flexibility & Configuration**
- System SHALL allow users to configure execution schedule via web UI or config file:
  - **Start Time:** Any time in user's timezone (default: 1:00 AM GMT)
  - **Days of Week:** Select any combination (default: Monday-Friday, can add Saturday/Sunday)
  - **Timezone:** User's local timezone for all schedule times (default: GMT)
  - **Frequency:** Daily, multiple times per day, specific days only, or one-time future run
  - **Pause Mode:** Temporarily disable scheduled runs (vacation mode)
- Multiple scheduled runs per day:
  - Example 1: Morning scan 6am + Afternoon update 3pm
  - Example 2: Pre-market 7am + Mid-day 12pm + Pre-close 3pm
  - Each run can have different scope/configuration (e.g., morning = full market, afternoon = portfolio + watchlist only)
- One-time scheduled runs:
  - User can schedule analysis for specific future date/time ("Run full scan on 2025-12-01 at 9am")
  - Useful for earnings season, known catalyst dates, testing
- Pause mode configuration:
  - User can pause all scheduled runs (vacation, system changes, testing)
  - Specify pause duration (pause for 2 weeks, pause until specific date)
  - On-demand execution still available during pause
- Schedule SHALL be persisted in database and survive system restarts
- Schedule changes SHALL take effect immediately (next scheduled run uses new schedule)
- UI SHALL display next scheduled run time prominently

### FR-7: User Interface & Trade Execution

**FR-7.1: Web Dashboard (React Frontend)**
- **Home/Morning Report View:**
  - Display latest morning report
  - Show NEW recommendations with BUY buttons
  - Portfolio performance chart (daily P&L)
  - Watchlist summary with trigger status
- **Portfolio View:**
  - Table of all holdings with current P&L
  - Click any position to see detailed agent analysis
  - Quick SELL button with confirmation
- **Opportunities View:**
  - Today's recommended trades
  - Historical recommendations with outcomes
  - Filter by conviction level
- **Stock Analysis View:**
  - Search any UK ticker
  - Run on-demand analysis (all 8 agents)
  - View detailed agent reasoning
  - Add to watchlist with custom triggers
- **Settings:**
  - Configure risk parameters (position size, stop-loss %)
  - Select active agents (enable/disable specific agents)
  - Set cost budgets and alerts
  - Email notification preferences

**FR-7.2: Manual Trade Execution & Logging**
- User reviews morning recommendations
- For each recommended trade:
  - **APPROVE:** User clicks "Execute Trade" → Logs approval, provides trade confirmation form
  - **REJECT:** User clicks "Reject" → Logs rejection with optional reason
  - **MODIFY:** User adjusts quantity or price → Logs modification
- User manually executes trade via broker (Interactive Brokers, Hargreaves Lansdown, etc.)
- User returns to system and logs actual trade:
  - Ticker, action (BUY/SELL), quantity, price, commission, timestamp
  - System automatically calculates cost basis, stop-loss, target price
  - Adds position to Active Portfolio tracking

**FR-7.3: Trade Outcome Tracking**
- For every trade, track:
  - Entry: Date, price, quantity, total cost (including stamp duty + commission)
  - Exit: Date, price, quantity, total proceeds
  - Holding period (days)
  - Profit/Loss (£ and %)
  - Which agents recommended it (attribution)
  - Why exited (stop-loss, target, user decision, fundamental change)
- Aggregate performance metrics:
  - Win rate overall and by confidence level
  - Average gain on winners, average loss on losers
  - Risk/reward ratio
  - Best/worst performers by agent recommendation

### FR-8: System Architecture & Technical Requirements

**FR-8.1: Backend (FastAPI)**
- Existing FastAPI backend to be extended:
  - New routes for UK market data, automation status, morning reports
  - API endpoint: `POST /api/automation/morning-scan` (trigger manual scan)
  - API endpoint: `GET /api/opportunities` (retrieve latest recommendations)
  - API endpoint: `POST /api/watchlist/add` (add stock to watchlist with trigger)
  - API endpoint: `GET /api/portfolio/status` (current holdings and P&L)

**FR-8.2: Agent Orchestration (LangGraph)**
- Extend existing LangGraph workflow:
  - Add 7 new discovery agent nodes
  - Modify state graph to support signal aggregation before analysis
  - Implement conditional logic: Only run analysis agents on high-scoring stocks
  - Add watchlist re-validation workflow
- State management:
  - Existing `AgentState` TypedDict extended with:
    - `discovery_signals`: Aggregated signals from all discovery agents
    - `signal_scores`: Ticker → score mapping
    - `watchlist_triggers`: Stocks that triggered conditions today
    - `re_validation_results`: Re-analysis outcomes for watchlist stocks

**FR-8.3: LLM Integration**
- Support multiple LLM providers (existing):
  - OpenAI (GPT-4o primary, GPT-3.5 for cheap operations)
  - Anthropic Claude (Sonnet for reasoning-heavy tasks)
  - Groq (fast inference for real-time queries)
  - Ollama (local models for development/testing)
- Prompt engineering:
  - Each agent has specialized system prompt encoding investor philosophy
  - Prompts include UK-specific context (IFRS accounting, LSE market structure, UK economic indicators)
  - Use structured output (Pydantic models) for reliable signal extraction

**FR-8.4: Database & Persistence**
- Store in database:
  - Company/ticker mapping (600+ UK companies)
  - Watchlist (stocks with triggers)
  - Portfolio positions (current holdings)
  - Trade history (all executed trades)
  - Agent decisions (audit trail)
  - Morning reports (last 90 days)
- Use existing database setup (likely PostgreSQL or SQLite)

**FR-8.5: Deployment**
- Phase 1: Run locally on user's machine or VPS (DigitalOcean, AWS EC2)
- Scheduler: Python `schedule` library or cron job
- Process management: systemd service or supervisor
- Environment: Ubuntu Linux, Python 3.10+, virtual environment
- Dependencies: LangChain, LangGraph, FastAPI, React, requests, pandas, yfinance (fallback)

### FR-9: System Extensibility & Modularity

**FR-9.1: Plugin Architecture**
- System SHALL implement plugin architecture for all agent types:
  - Discovery agents as loadable plugins
  - Analysis agents as loadable plugins
  - Decision agents (Risk Manager, Portfolio Manager) extendable
- Plugins SHALL be hot-swappable where feasible (add/remove without system restart for config-only changes)
- Plugin registry SHALL validate compatibility before loading (interface compliance, dependencies satisfied)
- Plugin API SHALL be versioned (backward compatibility maintained across minor versions)

**FR-9.2: Data Source Modularity**
- System SHALL abstract data provider interface:
  - Easy to swap primary data source (EODHD → Finnhub → Yahoo Finance via configuration)
  - Multi-source redundancy (automatic fallback if primary unavailable)
  - Priority-based data sourcing (try source A, fallback to B, then C)
- Data adapters SHALL normalize data to common internal format (agent logic agnostic to source)
- System SHALL support custom data sources (user-provided CSV, custom API integration)

**FR-9.3: Strategy Framework**
- System SHALL support multiple named strategy configurations:
  - Save/load strategies (e.g., "Conservative Dividend", "Aggressive Growth", "Turnaround Specialist")
  - Quick-switch between strategies via UI dropdown
  - Each strategy includes: active agents + weights, discovery parameters, risk parameters, watchlist triggers
- Strategy configurations SHALL be exportable/importable (JSON format, shareable across users)
- System SHALL provide strategy templates library (built-in + user-contributed)

**FR-9.4: API for External Integrations**
- System SHALL expose comprehensive REST API:
  - `POST /api/analyze-stock`: Run analysis on arbitrary ticker with custom agent set
  - `GET /api/agents/available`: List all registered agents (built-in + custom)
  - `POST /api/agents/configure`: Update agent configuration programmatically
  - `GET /api/agents/performance`: Retrieve agent performance metrics
  - `POST /api/execution/trigger`: Trigger on-demand full system run
  - `GET /api/reports/latest`: Retrieve latest report in JSON format
- API SHALL support authentication (API key, OAuth 2.0)
- API SHALL enable third-party tool integrations (Excel plugins, TradingView scripts, Zapier workflows)

### FR-10: Ad-Hoc & On-Demand Execution

**FR-10.1: Manual Full Discovery Scan**
- User SHALL be able to trigger complete discovery + analysis workflow anytime via web UI or API
- On-demand run SHALL execute same workflow as scheduled batch (all enabled agents, full data collection)
- On-demand run SHALL use current agent configuration and strategy settings
- System SHALL queue on-demand requests (prevent concurrent executions, execute sequentially)
- Results SHALL be delivered via configured channels same as scheduled runs
- On-demand runs SHALL be logged and counted toward cost budgets

**FR-10.2: Custom Ticker List Analysis**
- User SHALL be able to provide custom ticker list for immediate analysis (5-50 tickers)
- System SHALL run enabled analysis agents on provided tickers (skip discovery layer)
- Use cases:
  - "I heard about Companies X, Y, Z - analyze them NOW"
  - "Friend recommended these 10 stocks - what do your agents think?"
  - "Re-analyze my watchlist immediately"
- Custom list analysis SHALL complete faster than full discovery (focus on specific stocks)
- Results SHALL be delivered in lightweight format (summary report, not full morning report)

**FR-10.3: Portfolio Re-Evaluation On-Demand**
- User SHALL be able to trigger immediate re-evaluation of all current holdings
- System SHALL run all enabled analysis agents on each holding
- System SHALL flag positions where thesis has deteriorated (SELL candidates)
- Use cases:
  - "Market crashed 5% today - check my portfolio NOW"
  - "Major news just broke - re-evaluate everything"
  - "Want to know if I should hold over weekend"
- Portfolio re-evaluation SHALL include stop-loss breach check, target price check, fundamental deterioration check

**FR-10.4: Event-Driven Triggers**
- System SHALL support event-driven analysis triggers:
  - Market crash detection: If FTSE 100 drops >3% in single day, automatically run portfolio re-evaluation
  - Breaking news alerts: If major news detected (configurable keywords), trigger focused analysis
  - Insider trading alerts: If large insider buy detected in watchlist stock, trigger immediate re-validation
  - Technical breakout alerts: If watchlist stock breaks resistance, trigger analysis
- User SHALL be able to enable/disable event triggers
- Event triggers SHALL respect cost budgets (circuit breaker if approaching limit)

**FR-10.5: Historical Backfill Analysis**
- User SHALL be able to request historical analysis ("what would system have recommended on 2024-11-01?")
- System SHALL retrieve historical data (prices, news, filings from specified date)
- System SHALL run current agent configuration on historical data
- Use cases:
  - "I was on vacation last week - what did I miss?"
  - "System was down on Monday - backfill that day's analysis"
  - "Test my new agent configuration on last week's data"
- Historical analysis SHALL be clearly marked as retrospective (not real-time)

### FR-11: Discovery Scope & Targeting

**FR-11.1: Market Cap Filters**
- User SHALL be able to filter discovery scope by market cap:
  - FTSE 100 only (large caps, ~100 stocks)
  - FTSE 250 only (mid caps, ~250 stocks)
  - Small Cap only (FTSE SmallCap index)
  - AIM (Alternative Investment Market, high-growth small companies)
  - Custom market cap range (e.g., £500M-5B)
  - All stocks (default: FTSE All-Share ~600 stocks)
- Market cap filters SHALL reduce discovery costs (fewer stocks to analyze)

**FR-11.2: Sector & Industry Focus**
- User SHALL be able to limit discovery to specific sectors or industries:
  - Single sector (e.g., Healthcare only, Technology only, Energy only)
  - Multiple sectors (e.g., Healthcare + Technology)
  - Exclude sectors (e.g., All except Financials)
  - GICS classification support (11 sectors, 24 industry groups)
- Sector focus use cases:
  - "I'm bullish on renewable energy this month"
  - "Only analyze defensive sectors (Healthcare, Utilities, Consumer Staples)"
  - "Avoid cyclicals during recession risk"

**FR-11.3: Custom Ticker Lists**
- User SHALL be able to provide custom ticker list as discovery scope:
  - Replace broad market scan with specific list (10-100 tickers)
  - Useful for focused research, friend recommendations, sector deep-dives
  - Custom list SHALL be saved and reusable (named lists: "Tech Watchlist", "Dividend Aristocrats")
- System SHALL support importing ticker lists (CSV, Excel, text file)

**FR-11.4: ESG & Ethical Filters**
- User SHALL be able to apply ethical/ESG filters to discovery scope:
  - Exclude sectors: Tobacco, Weapons, Fossil Fuels, Gambling, Alcohol
  - Minimum ESG score (if ESG data available)
  - Include-only filters (e.g., only renewable energy, only B-Corps)
- ESG filters SHALL be saved per strategy configuration
- System SHALL clearly indicate when ESG filters reduce opportunity set

**FR-11.5: Price Range & Liquidity Filters**
- User SHALL be able to filter by stock price and liquidity:
  - Price range (e.g., £2-10, £50+, under £5 "penny stocks")
  - Minimum average daily volume (ensure liquidity, avoid illiquid stocks)
  - Maximum bid-ask spread (avoid stocks with poor execution costs)
- Liquidity filters SHALL protect user from stocks difficult to trade

**FR-11.6: Geography & Asset Class Expansion**
- System SHALL support expanding scope beyond UK stocks (Phase 2-3):
  - UK + European stocks (LSE + Euronext + XETRA)
  - UK + US stocks (dual market coverage)
  - Asset class expansion: Stocks, ETFs, REITs, Investment Trusts
- Geographic expansion SHALL require additional data sources
- Each market SHALL support same agent framework (localized where needed)

### FR-12: Workflow & Execution Modes

**FR-12.1: Manual Approval Workflow (MVP Default)**
- User reviews recommendations in morning report
- User approves or rejects each recommendation via web UI
- User executes approved trades manually via broker
- User logs actual trades executed (ticker, quantity, price, commission)
- System updates portfolio tracking with executed positions
- All decisions logged for performance attribution

**FR-12.2: Paper Trading / Simulation Mode**
- User SHALL be able to enable paper trading mode (no real money)
- System executes all logic normally but tracks hypothetical positions
- Paper trading use cases:
  - Test system with zero risk before committing real capital
  - Test new agent configuration or strategy
  - Learn how system works without financial exposure
  - Compare paper performance vs. real portfolio performance
- Paper trading SHALL maintain separate portfolio (no mixing with real positions)
- Paper trading results SHALL clearly indicate "SIMULATED" in all reports

**FR-12.3: Read-Only / Educational Mode**
- User SHALL be able to enable read-only mode (view recommendations without trade capability)
- Read-only use cases:
  - Learn from system recommendations without trading
  - Educational use for students/researchers
  - Sharing access with advisor/partner without execution risk
- Read-only mode SHALL hide all trade execution buttons
- Read-only mode SHALL still track recommendation outcomes for learning

**FR-12.4: Auto-Execution Mode (Phase 2)**
- System SHALL support auto-execution within user-defined guardrails:
  - Max position size per trade (e.g., £500, 5% of portfolio)
  - Max trades per day/week (e.g., 2 trades/day max)
  - Auto-execute only high-conviction signals (e.g., 8/8 agents bullish, confidence >80%)
  - Require manual approval if position size exceeds threshold
- Auto-execution SHALL integrate with broker API (Interactive Brokers, Trading 212)
- Auto-execution SHALL require explicit user opt-in (disabled by default for safety)
- All auto-executed trades logged and notified to user immediately

**FR-12.5: Collaborative / Multi-User Approval (Phase 2-3)**
- System SHALL support multi-stage approval workflow:
  - Stage 1: AI recommends → Stage 2: User reviews → Stage 3: Advisor approves → Execute
  - Use cases: Joint accounts, managed accounts, advisory relationships
- Each approver SHALL have configurable permissions (view-only, approve, execute)
- Approval workflows SHALL be configurable per portfolio

**FR-12.6: Dry-Run / Test Mode**
- User SHALL be able to run configuration changes in dry-run mode (test without affecting live system)
- Dry-run use cases:
  - Test new agent configuration before activating
  - Test new discovery scope filters
  - Test new strategy template
- Dry-run SHALL execute full workflow but not save results or update portfolio
- Dry-run results SHALL be clearly marked "TEST RUN"

### FR-13: Multi-Portfolio Management

**FR-13.1: Multiple Portfolio Support**
- System SHALL support managing multiple portfolios simultaneously:
  - ISA (tax-advantaged UK Individual Savings Account)
  - SIPP (Self-Invested Personal Pension)
  - Taxable general investment account
  - Joint account (shared with partner)
  - Speculative/experimental portfolio
- Each portfolio SHALL have independent tracking (positions, P&L, cost basis)
- User SHALL be able to create unlimited portfolios (within reasonable system limits)

**FR-13.2: Portfolio-Specific Strategies**
- Each portfolio SHALL support independent strategy configuration:
  - Portfolio A (ISA): Conservative dividend strategy (Value 2.5x, Quality 2.0x, Growth 0.3x)
  - Portfolio B (Taxable): Aggressive growth strategy (Growth 2.5x, Catalyst 2.0x, Value 0.5x)
  - Portfolio C (SIPP): Balanced long-term (All agents 1.0x)
- Strategy settings SHALL include: active agents, agent weights, discovery scope, risk parameters

**FR-13.3: Portfolio-Specific Risk Parameters**
- Each portfolio SHALL have independent risk configuration:
  - Position sizing (ISA: 5% max, Taxable: 10% max, Speculative: 15% max)
  - Stop-loss percentages (ISA: 5%, Taxable: 8%, Speculative: 12%)
  - Max exposure (ISA: 60%, Taxable: 80%, Speculative: 90%)
  - Sector concentration limits
- Risk parameters SHALL match portfolio objectives (conservative vs. aggressive)

**FR-13.4: Cross-Portfolio Tax Optimization (Phase 2-3)**
- System SHALL support tax-loss harvesting across portfolios:
  - Identify losing positions in taxable account
  - Offset gains with losses for tax efficiency
  - Rebalance across portfolios to maintain overall allocation
- Tax optimization SHALL respect wash sale rules (if applicable)
- System SHALL generate tax reports (capital gains, dividends for accountant)

**FR-13.5: Consolidated & Individual Reporting**
- System SHALL provide consolidated reporting (all portfolios aggregated):
  - Total portfolio value, total P&L, overall win rate
  - Aggregate performance metrics
- System SHALL provide individual portfolio reporting:
  - Per-portfolio morning reports (separate email for ISA, SIPP, Taxable)
  - Per-portfolio performance dashboards
- User SHALL configure reporting preferences (consolidated only, individual only, or both)

### FR-14: Alerting & Notification System

**FR-14.1: Custom Alert Triggers**
- User SHALL be able to define custom alert triggers:
  - **Price Alerts:** Alert when holding drops/rises X% (e.g., "Alert if AAPL drops 5%")
  - **Volume Spikes:** Alert when stock volume exceeds X× average
  - **Insider Trading:** Alert when insider buying detected in watchlist stock
  - **Analyst Upgrades:** Alert when any analyst upgrades stock to Strong Buy
  - **News Catalysts:** Alert when significant news detected (user-defined keywords)
  - **Technical Breakouts:** Alert when stock breaks above resistance or below support
  - **Earnings Surprises:** Alert when earnings beat/miss expectations by X%
- Each alert SHALL include trigger condition, affected ticker, current value, threshold

**FR-14.2: Multi-Channel Alert Delivery**
- System SHALL support multiple alert delivery channels (user-configurable):
  - Email (default)
  - SMS (via Twilio, SNS, or similar)
  - Push notifications (web push, mobile app Phase 3)
  - Slack (webhook integration)
  - Discord (webhook integration)
  - Webhook (generic HTTP POST for custom integrations)
- User SHALL configure preferred channel per alert type (critical = SMS, informational = email)

**FR-14.3: Alert Urgency Levels & Frequency**
- Alerts SHALL be categorized by urgency:
  - **Critical:** Stop-loss breached, portfolio down >10%, market crash detected (immediate delivery)
  - **High:** High-conviction opportunity, insider buying in watchlist (deliver within 15 min)
  - **Medium:** Watchlist trigger fired, analyst upgrade (hourly digest)
  - **Low:** General opportunities, market context updates (daily digest)
- User SHALL configure alert frequency per urgency level:
  - Critical: Real-time (immediate)
  - High: Real-time or 15-min batches
  - Medium: Hourly digest
  - Low: Daily digest or weekly summary

**FR-14.4: Alert Filters & Quiet Hours**
- User SHALL be able to filter alerts:
  - Only high-conviction opportunities (confidence >75%, 7+ agents agree)
  - Only BUYs (suppress SELLs), or only SELLs (suppress BUYs)
  - Only positions >£X (filter small trades)
  - Only specific portfolios (ISA alerts, but not Speculative)
- User SHALL configure quiet hours (no alerts during sleep):
  - Default: No alerts 10pm-7am
  - Configurable start/end times
  - Exception: Critical alerts always delivered (stop-loss breach, market crash)

**FR-14.5: Alert Grouping & Digest**
- System SHALL support alert grouping to prevent notification fatigue:
  - Single digest email with multiple alerts (vs. individual emails per alert)
  - Grouped by urgency level
  - Grouped by portfolio
  - Grouped by alert type (all price alerts together, all insider alerts together)
- User SHALL configure digest frequency (real-time, hourly, daily)

### FR-15: Historical Analysis & Backtesting

**FR-15.1: Historical Backtesting**
- User SHALL be able to run system on historical data (e.g., 2020-2024)
- Backtesting SHALL use current agent configuration on past data
- Backtesting SHALL simulate trading decisions (what would system have recommended?)
- Backtesting SHALL calculate performance metrics:
  - Win rate, average gain/loss, total return, Sharpe ratio
  - Max drawdown, recovery time
  - Comparison vs. benchmark (FTSE 100 buy-and-hold)
- Backtesting use cases:
  - Validate new agent configuration before going live
  - Compare different strategies historically
  - Build confidence in system before committing capital

**FR-15.2: Point-In-Time Analysis**
- User SHALL be able to request "what would system recommend on [specific past date]?"
- System SHALL retrieve historical data as of that date (prices, news, filings)
- System SHALL run current agent configuration on that historical snapshot
- Point-in-time use cases:
  - "What would system have said about GameStop on 2021-01-15?" (meme stock event)
  - "How would system have handled COVID crash (March 2020)?"
  - "Test if system would have caught opportunity I missed"

**FR-15.3: Configuration A/B Testing**
- User SHALL be able to compare different agent configurations historically:
  - Configuration A (all agents 1.0x) vs. Configuration B (value-focused)
  - Agent set 1 (8 agents) vs. Agent set 2 (5 agents, disabled expensive ones)
- A/B testing SHALL run both configurations on same historical data
- Results SHALL show comparative performance (which config would have performed better?)
- A/B testing use cases:
  - Optimize agent weights for best historical performance
  - Determine which agents add value vs. just cost

**FR-15.4: Stress Testing**
- System SHALL support stress testing against historical crisis periods:
  - 2008 Financial Crisis
  - COVID Crash (March 2020)
  - 2022 Bear Market
  - Brexit Referendum (2016)
  - User-defined custom periods
- Stress testing SHALL show how portfolio/strategy would have performed during crisis
- Stress testing use cases:
  - Validate risk management (would stop-losses have protected?)
  - Assess strategy resilience (which strategies weather storms best?)
  - Build confidence in downside protection

**FR-15.5: Performance Attribution Historical**
- System SHALL analyze historical performance by agent contribution:
  - Which agents voted for winning trades most often?
  - Which agents had highest ROI (returns generated vs. cost)?
  - Which agent combinations most valuable?
  - Which agents add unique signal vs. redundant?
- Performance attribution use cases:
  - Optimize agent selection (keep high-performers, disable low-performers)
  - Justify agent costs ("Value Investor generated £5k profit vs. £20 cost")
  - Continuous improvement (data-driven agent configuration)

**FR-15.6: Walk-Forward Validation**
- System SHALL support walk-forward optimization:
  - Train on Period A (2020-2022), test on Period B (2023-2024)
  - Optimize agent configuration on training period
  - Validate optimized config on out-of-sample test period
- Walk-forward validation prevents overfitting (config works on new data, not just historical)
- Walk-forward use cases:
  - Scientifically validate strategy before live trading
  - Avoid curve-fitting (config that worked in past but fails going forward)

---

## Non-Functional Requirements

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

## References

### Source Documents

**Product Planning:**
- `docs/product-brief-AIHedgeFund-2025-11-17.md` - Product vision, innovations, target users, success metrics
- `docs/brainstorming-session-results-2025-11-16.md` - Initial ideation and problem/solution discovery

**Research & Validation:**
- `docs/research-multi-agent-architecture-2025-11-17.md` - Multi-agent system architecture patterns, institutional validation
- `docs/research-domain-2025-11-16.md` - UK fintech domain analysis, regulatory considerations
- `docs/research-data-sources-2025-11-16.md` - UK market data source evaluation and cost analysis

**Technical Documentation:**
- `docs/1-system-architecture.md` - Existing US system architecture baseline
- `docs/2-news-processing.md` - News ingestion and processing patterns
- `docs/3-current-workflow.md` - Current LangGraph workflow structure
- `docs/4-api-integration.md` - API integration patterns and examples
- `docs/5-uk-adaptation-guide.md` - UK market adaptation requirements
- `docs/agent-network-architecture.md` - Agent communication and signal convergence design

### External References

**Market Data & APIs:**
- Financial Modeling Prep API Documentation (https://financialmodelingprep.com/developer/docs/)
- London Stock Exchange Market Data Guidelines
- Companies House RNS Filings API
- NewsAPI.org Documentation

**Frameworks & Tools:**
- LangGraph Documentation (https://langchain-ai.github.io/langgraph/)
- LangChain Production Best Practices
- FastAPI Documentation (https://fastapi.tiangolo.com/)
- React + TypeScript + Vite Best Practices

**Regulatory & Compliance:**
- FCA Regulatory Framework for AI in Finance
- UK ISA and SIPP Rules and Regulations
- GDPR Data Protection Requirements
- Market Abuse Regulation (MAR) Guidelines

**Investment Methodologies:**
- Warren Buffett / Benjamin Graham: Value Investing Principles
- Peter Lynch: One Up on Wall Street Methodology
- Michael Burry: Contrarian Value Investing
- Robbie Burns: The Naked Trader (UK-Specific Approach)

---

_This PRD captures the complete vision for AIHedgeFund - an autonomous, modular, flexible multi-agent AI trading system that brings institutional-quality investment analysis to retail investors at unprecedented cost efficiency (£100-200/month vs. £60k+/year). Through networked signal convergence, adversarial challenge protocols, total user control and configurability, and systematic opportunity discovery across the entire UK market, it aims to deliver consistent, profitable trading decisions on the user's schedule and terms._

**Key Innovations:** Signal Convergence Network, Three-Tier Tracking, Adversarial Challenge Protocol, Modular Agent Architecture, Total Flexibility & Control

_Created through collaborative discovery between Longy and AI Product Manager._
_Version 1.1 | Date: 2025-11-19 | Status: Modularity & Flexibility Integrated_
