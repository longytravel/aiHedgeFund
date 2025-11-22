# Product Scope

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
