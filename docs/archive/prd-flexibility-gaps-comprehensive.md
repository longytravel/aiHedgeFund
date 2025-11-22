# PRD Flexibility & Configurability - Comprehensive Gap Analysis

**Date:** 2025-11-19
**Issue:** PRD hardcodes too many assumptions about when/how/what system runs
**Longy's Challenge:** "What about different report times? Ad-hoc analysis? Come on, think about all this stuff."

---

## Current Hardcoded Assumptions (Problems)

### 1. TEMPORAL RIGIDITY

**Hardcoded in PRD:**
- Line 15: "running overnight (1am-7am)"
- Line 19: "Delivers daily report by 7am"
- Line 106: "Morning report delivered by 7am 95%+ of trading days"
- Line 189: "Scheduled nightly execution (Monday-Friday)"
- Line 196: "Daily Morning Report (Delivered by 7am)"
- Line 769: "Morning report SHALL be delivered by 7:00 AM GMT"
- Line 632: "Scheduler runs daily at 1:00 AM GMT (Monday-Friday)"

**Problems:**
- ❌ What if I'm a night owl and want 10am report?
- ❌ What if I want afternoon update (3pm before market close)?
- ❌ What if I'm in a different timezone (US, Asia)?
- ❌ What if I want weekend analysis (prep for Monday)?
- ❌ What if I'm on vacation and want to pause?
- ❌ What if I want multiple runs per day?

**Missing:**
- Custom report delivery time
- Multiple scheduled runs per day
- Timezone configuration
- Weekend/holiday scheduling
- Vacation/pause mode
- Historical backfill ("analyze what I missed last week")

---

### 2. ON-DEMAND / AD-HOC EXECUTION

**Current State:**
- Line 642: "Manual override: User can trigger immediate analysis via web UI" - MENTIONED ONCE, buried in NFR-R2
- Line 581: "On-demand stock analysis" - exists for single stocks only
- No comprehensive ad-hoc workflow

**Problems:**
- ❌ "I just heard Company X announced a buyback - analyze it NOW"
- ❌ "Market crashed 5% today - re-evaluate my entire portfolio NOW"
- ❌ "Quarterly earnings season - run focused scan on reporting companies"
- ❌ "I have 30 minutes free - what opportunities can you find right now?"
- ❌ "Watchlist stock hit my trigger - re-validate immediately, don't wait until tomorrow"

**Missing:**
- Ad-hoc full discovery scan (on-demand morning report)
- Ad-hoc portfolio re-evaluation
- Ad-hoc watchlist re-validation
- Ad-hoc custom ticker list analysis ("analyze these 10 stocks I'm researching")
- Event-driven triggers (market crash, sector rotation, breaking news)
- Real-time alerts with on-demand deep dive

---

### 3. SCOPE & TARGETING FLEXIBILITY

**Current State:**
- Discovery runs across "entire FTSE All-Share" (600+ stocks)
- No ability to focus/filter

**Problems:**
- ❌ "I only want FTSE 100 (large caps), not 600 stocks"
- ❌ "I only want healthcare sector this week"
- ❌ "Analyze only dividend aristocrats (10+ year dividend history)"
- ❌ "I want to research these 5 specific companies my friend mentioned"
- ❌ "Show me only opportunities under £5/share (penny stocks)"
- ❌ "Exclude companies with poor ESG ratings"
- ❌ "I'm bullish on renewable energy - scan only that sector"

**Missing:**
- Market cap filters (FTSE 100 only, small caps only, etc.)
- Sector/industry focus (analyze only tech, only healthcare)
- Custom ticker lists (user-provided watchlist to analyze)
- Price range filters (£2-10, £50+, etc.)
- ESG/ethical filters (exclude tobacco, weapons, fossil fuels)
- Geography expansion (UK + EU, UK + US)
- Asset class expansion (stocks + ETFs + REITs + bonds)
- Fundamental pre-filters (only profitable companies, only low debt, etc.)

---

### 4. OUTPUT & DELIVERY FLEXIBILITY

**Current State:**
- Line 577: "Email: HTML-formatted email to configured address"
- Line 578: "Web Dashboard: React frontend displays same report"
- Single format, single recipient

**Problems:**
- ❌ "I want SMS alert for high-conviction opportunities only"
- ❌ "I want Slack notification, not email"
- ❌ "I want JSON export for my custom Excel dashboard"
- ❌ "I want PDF for my accountant"
- ❌ "I want summary only (1 paragraph), not full report"
- ❌ "I want data-only CSV (no narrative)"
- ❌ "Send to me AND my financial advisor AND my accountant"
- ❌ "I only care about BUY recommendations, skip market context"

**Missing:**
- Multi-channel delivery (email, SMS, Slack, Discord, webhook, API)
- Report format options (HTML, PDF, JSON, CSV, plain text)
- Report detail levels (summary, standard, detailed, data-only)
- Custom report sections (I only want: Opportunities + Portfolio, skip Discovery Summary)
- Multiple recipients (primary user, advisor, accountant, partner)
- Conditional delivery ("only send if 2+ BUY recommendations")
- Report archival (auto-save to Dropbox, Google Drive, OneDrive)

---

### 5. WORKFLOW & EXECUTION MODE FLEXIBILITY

**Current State:**
- Line 203-207: Manual trade execution only (user approves, then places trades)
- Single workflow: Discover → Analyze → Recommend → User Approves → User Executes

**Problems:**
- ❌ "I trust the system - auto-execute within guardrails (max £500/trade, max 5%/position)"
- ❌ "I want multi-stage approval (analyst → me → my advisor → execute)"
- ❌ "I want to paper trade first (track performance without real money)"
- ❌ "I want collaborative mode (me + my partner both review recommendations)"
- ❌ "I want read-only mode (just learn from recommendations, don't trade)"
- ❌ "I want different workflows for different portfolios (ISA auto, SIPP manual)"

**Missing:**
- Auto-execution mode (within user-defined guardrails)
- Multi-stage approval workflow
- Paper trading / simulation mode
- Collaborative / multi-user approval
- Read-only / educational mode
- Portfolio-specific workflows (ISA, SIPP, taxable, speculative)
- Dry-run mode (test config changes without real analysis)

---

### 6. MULTI-PORTFOLIO / MULTI-STRATEGY

**Current State:**
- Single portfolio assumed
- Single strategy at a time

**Problems:**
- ❌ "I have 3 portfolios: ISA (income), SIPP (growth), taxable (speculative)"
- ❌ "I want conservative strategy for ISA, aggressive for taxable"
- ❌ "I want different risk parameters per portfolio"
- ❌ "I want different agents active per portfolio (value for ISA, growth for taxable)"
- ❌ "I want separate morning reports per portfolio"

**Missing:**
- Multi-portfolio support (ISA, SIPP, taxable, joint account, kids' accounts)
- Portfolio-specific strategies (conservative, balanced, aggressive, income, growth, speculative)
- Portfolio-specific agent configurations
- Portfolio-specific risk parameters
- Portfolio-specific reporting
- Portfolio rebalancing recommendations
- Tax-loss harvesting across portfolios

---

### 7. NOTIFICATION & ALERT FLEXIBILITY

**Current State:**
- Line 236-239: Watchlist triggers mentioned but implementation vague
- Line 561: "Stop-loss alerts" mentioned
- No comprehensive alerting system

**Problems:**
- ❌ "Alert me immediately if any holding drops 5%"
- ❌ "Alert me if insider buying detected in watchlist stock"
- ❌ "Alert me if analyst upgrades any FTSE 100 stock to Strong Buy"
- ❌ "Alert me real-time for high-conviction opportunities (don't wait until 7am)"
- ❌ "Alert me on my phone (push), not email"
- ❌ "Alert me hourly during market hours, digest after close"
- ❌ "Alert me only for opportunities >£10k position size (filter noise)"

**Missing:**
- Custom alert triggers (price %, insider buying, analyst upgrades, news catalysts, technical breakouts)
- Alert channels (email, SMS, push notification, Slack, Discord, webhook)
- Alert urgency levels (critical, high, medium, low)
- Alert frequency (real-time, hourly, daily, weekly)
- Alert filters (only high-conviction, only BUYs, only SELLs, only >£X position)
- Alert grouping (single digest vs. individual notifications)
- Alert quiet hours (don't disturb 10pm-7am)

---

### 8. HISTORICAL & BACKTESTING FLEXIBILITY

**Current State:**
- No backtesting mentioned in MVP
- Line 299: "Walk-forward optimization" in Vision (Phase 3)
- No historical analysis

**Problems:**
- ❌ "How would the system have performed during COVID crash (March 2020)?"
- ❌ "Backtest my current agent configuration vs. last 2 years"
- ❌ "What if I had run this system in 2022 bear market?"
- ❌ "Show me what the system would have recommended on [specific past date]"
- ❌ "Replay last week's analysis with different agent weights"

**Missing:**
- Historical backtesting (run system on past data)
- Point-in-time analysis ("what would system recommend on 2020-03-15?")
- Configuration A/B testing (compare different agent setups historically)
- Stress testing (2008 crisis, COVID crash, specific bear markets)
- Walk-forward validation (train on 2020-2022, test on 2023-2024)
- Performance attribution historical (which agents would have contributed most?)

---

### 9. DATA SOURCE & INTEGRATION FLEXIBILITY

**Current State:**
- Line 586-591: Primary = Financial Modeling Prep, Fallback = Yahoo Finance
- Prescriptive data sources

**Problems:**
- ❌ "I have Bloomberg Terminal subscription - use that instead"
- ❌ "I want to add my own proprietary data (web scraping, alternative data)"
- ❌ "I want to use Interactive Brokers data (I'm already paying for it)"
- ❌ "I want to add Twitter sentiment for specific stocks"
- ❌ "I want to integrate with my broker's API for live positions"
- ❌ "I want to sync portfolio from Google Sheets"

**Missing:**
- Data source priority/selection (user picks primary, fallback, tertiary)
- Custom data integration (user uploads CSV, connects API)
- Alternative data support (satellite imagery, web traffic, app downloads, social sentiment)
- Multi-broker support (aggregate positions from HL, IBKR, Trading 212)
- Portfolio sync (import from external trackers)
- Custom fundamental metrics (user-defined calculations)

---

### 10. LANGUAGE & LOCALIZATION

**Current State:**
- Hardcoded English, UK-centric

**Problems:**
- ❌ "I'm in Spain - I want reports in Spanish"
- ❌ "I'm analyzing French stocks - need French news sources"
- ❌ "I'm in Hong Kong timezone - adjust schedules"
- ❌ "I want currency in EUR, not GBP"
- ❌ "I want dates in DD/MM/YYYY (UK), not MM/DD/YYYY (US)"

**Missing:**
- Multi-language support (English, Spanish, French, German, Chinese)
- Timezone configuration
- Currency preference (GBP, USD, EUR)
- Date/time format localization
- News source localization (French news for French stocks)

---

### 11. COST & RESOURCE MANAGEMENT

**Current State:**
- Line 653: "Alert user if monthly cost exceeds configured budget (default £200 Phase 1)"
- Basic cost monitoring

**Problems:**
- ❌ "I have £100/month budget this month, £300 next month (bonus coming)"
- ❌ "Pause system if I hit £150 this month (hard stop)"
- ❌ "Prioritize high-conviction opportunities if approaching budget limit"
- ❌ "I want daily cost breakdown (how much did yesterday's run cost?)"
- ❌ "I want cost per opportunity (was that recommendation worth £5 in LLM costs?)"
- ❌ "I want to allocate budget: 60% discovery, 30% analysis, 10% reporting"

**Missing:**
- Dynamic budget allocation (per month, per week, per run)
- Cost circuit breakers (hard stop at £X)
- Cost prioritization (focus budget on highest-value activities)
- Cost attribution (cost per opportunity, per agent, per data source)
- Budget forecasting ("at current rate, you'll hit £200 by day 20")
- Cost optimization recommendations ("disable Sentiment Agent to save £30/month")

---

### 12. REGULATORY & COMPLIANCE FLEXIBILITY

**Current State:**
- Phase 1: Personal use, minimal regulation
- Phase 3: FCA authorization

**Problems:**
- ❌ "I want audit trail for every decision (tax preparation)"
- ❌ "I need explainability reports (show me why system recommended X)"
- ❌ "I need to export all trades for accountant (CSV format)"
- ❌ "I need to comply with pattern day trader rules (US users)"
- ❌ "I need to track wash sales (tax optimization)"

**Missing:**
- Configurable audit detail level (minimal, standard, comprehensive)
- Explainability reports (agent reasoning, data sources, decision path)
- Tax reporting exports (capital gains, dividends, wash sales)
- Regulatory compliance modes (FCA, SEC, MiFID II)
- Trade justification logs (required for professional traders)

---

## Summary: What's Missing from PRD

### CRITICAL GAPS (Must Add to PRD)

1. **Scheduling Flexibility (FR-6 Enhancement)**
   - Custom report delivery time (not hardcoded 7am)
   - Multiple runs per day (morning + afternoon)
   - Timezone configuration
   - Weekend/holiday scheduling
   - Pause/vacation mode

2. **Ad-Hoc Execution (New FR-10)**
   - On-demand full discovery scan
   - On-demand portfolio re-evaluation
   - On-demand custom ticker list analysis
   - Event-driven triggers (market crash, breaking news)
   - Real-time alerts with immediate deep dive

3. **Scope & Targeting (New FR-11)**
   - Market cap filters (FTSE 100 only, small caps only)
   - Sector/industry focus
   - Custom ticker lists
   - ESG/ethical filters
   - Price range filters
   - Asset class expansion

4. **Output & Delivery (FR-4 Enhancement)**
   - Multi-channel delivery (email, SMS, Slack, webhook)
   - Report format options (HTML, PDF, JSON, CSV)
   - Report detail levels (summary, standard, detailed)
   - Custom report sections
   - Multiple recipients
   - Conditional delivery

5. **Workflow Modes (New FR-12)**
   - Auto-execution mode (within guardrails)
   - Multi-stage approval
   - Paper trading / simulation
   - Collaborative / multi-user
   - Read-only / educational

6. **Multi-Portfolio (New FR-13)**
   - Multiple portfolio support (ISA, SIPP, taxable)
   - Portfolio-specific strategies
   - Portfolio-specific agent configurations
   - Portfolio-specific risk parameters
   - Tax-loss harvesting

7. **Alerting System (New FR-14)**
   - Custom alert triggers
   - Multi-channel alerts
   - Alert frequency and grouping
   - Alert filters
   - Quiet hours

### IMPORTANT GAPS (Should Add to PRD)

8. **Historical & Backtesting (New FR-15)**
   - Historical backtesting
   - Point-in-time analysis
   - Configuration A/B testing
   - Stress testing
   - Performance attribution historical

9. **Data Source Flexibility (FR-5 Enhancement)**
   - Custom data integration
   - Alternative data support
   - Multi-broker sync
   - Portfolio import/export

10. **Cost Management (NFR-P4 Enhancement)**
    - Dynamic budget allocation
    - Cost circuit breakers
    - Cost attribution and forecasting
    - Cost optimization recommendations

### NICE-TO-HAVE GAPS (Consider for Phase 2-3)

11. **Language & Localization (New NFR-L1)**
    - Multi-language support
    - Timezone configuration
    - Currency and format preferences

12. **Compliance Tooling (New NFR-C1)**
    - Configurable audit detail
    - Explainability reports
    - Tax reporting exports
    - Regulatory compliance modes

---

## Proposed PRD Changes

### 1. Remove ALL Hardcoded Times

**CHANGE FROM:**
- "running overnight (1am-7am)"
- "Delivers daily report by 7am"
- "Scheduler runs daily at 1:00 AM GMT"

**CHANGE TO:**
- "running on user-defined schedule (default: 1am-7am)"
- "Delivers report at configured time (default: 7am)"
- "Scheduler runs at user-configured times (default: daily at 1:00 AM GMT)"

**ADD EVERYWHERE:** "User-configurable" or "Default: [value], configurable"

### 2. New Functional Requirements (7 Major Additions)

**FR-6.4: Scheduling Flexibility**
- Custom report delivery time (user sets preferred time)
- Multiple scheduled runs per day
- Timezone configuration
- Day-of-week selection (Mon-Fri default, weekends optional)
- Pause mode (vacation, testing, temporary disable)
- One-time scheduled runs (analyze on specific future date)

**FR-10: Ad-Hoc & On-Demand Execution**
- Manual full discovery scan (trigger complete overnight workflow anytime)
- Manual portfolio re-evaluation (check all holdings now)
- Custom ticker list analysis (user provides 5-50 tickers, system analyzes immediately)
- Event-driven triggers (market crash detection, breaking news alerts)
- Scheduled historical analysis (backfill missed days)

**FR-11: Discovery Scope & Targeting**
- Market cap filters (FTSE 100, FTSE 250, Small Cap, AIM, custom market cap range)
- Sector/industry focus (analyze only healthcare, only tech, etc.)
- Custom ticker lists (user-provided watchlist to analyze)
- ESG/ethical filters (exclude sectors, minimum ESG score)
- Price range filters (£2-10, £50+, etc.)
- Geography expansion (UK only, UK + EU, UK + US)
- Asset class filters (stocks, ETFs, REITs, bonds)

**FR-12: Workflow & Execution Modes**
- Manual approval (default): User reviews and executes trades
- Auto-execution mode: System executes within guardrails (max position size, daily trade limit)
- Paper trading mode: Track hypothetical performance without real trades
- Collaborative mode: Multiple users review recommendations
- Read-only mode: View recommendations without trade capability
- Dry-run mode: Test configuration changes without live analysis

**FR-13: Multi-Portfolio Management**
- Multiple portfolio support (ISA, SIPP, taxable, joint, etc.)
- Portfolio-specific strategies (conservative for ISA, aggressive for taxable)
- Portfolio-specific agent configurations (value agents for ISA, growth for taxable)
- Portfolio-specific risk parameters (different stop-losses, position sizes)
- Cross-portfolio tax optimization (harvest losses, rebalance)
- Consolidated reporting (all portfolios) and individual reporting (per portfolio)

**FR-14: Alerting & Notification System**
- Custom alert triggers (price %, volume spike, insider buying, analyst upgrade, news catalyst)
- Multi-channel alerts (email, SMS, push, Slack, Discord, webhook)
- Alert urgency levels (critical, high, medium, low)
- Alert frequency (real-time, hourly, daily digest, weekly summary)
- Alert filters (only high-conviction, only BUYs, only >£X position, etc.)
- Quiet hours (don't disturb 10pm-7am, user-configurable)
- Alert grouping (single digest vs. individual notifications)

**FR-15: Historical Analysis & Backtesting**
- Historical backtesting: Run system on past data (2020-2024)
- Point-in-time analysis: "What would system recommend on 2020-03-15?"
- Configuration A/B testing: Compare different agent setups historically
- Stress testing: Simulate performance during 2008 crisis, COVID crash
- Performance attribution: Which agents/strategies performed best historically?
- Walk-forward validation: Train on historical, validate on recent data

### 3. Enhanced Functional Requirements

**FR-4.2 Enhancement: Report Delivery Channels & Formats**
- ADD: Multi-channel delivery (email, SMS, Slack, Discord, webhook, API)
- ADD: Format options (HTML, PDF, JSON, CSV, plain text)
- ADD: Detail levels (summary, standard, detailed, data-only)
- ADD: Custom sections (user selects which sections to include)
- ADD: Multiple recipients (primary, advisor, accountant, partner)
- ADD: Conditional delivery (only send if X recommendations, or cost < £Y)

**FR-5 Enhancement: Data Source Flexibility**
- ADD: FR-5.6: Custom Data Integration
  - User can upload CSV data (custom fundamental metrics, proprietary signals)
  - User can connect custom APIs (alternative data providers)
  - User can integrate broker feeds (IBKR, HL, Trading 212 live positions)
  - User can add custom news sources (industry blogs, niche publications)

**NFR-P4 Enhancement: Cost Management & Optimization**
- ADD: Dynamic budget allocation (per month, per week, per run)
- ADD: Cost circuit breakers (pause system if approaching hard limit)
- ADD: Cost attribution (cost per opportunity, per agent, per data source)
- ADD: Budget forecasting ("at current rate, £200 budget reached by day 20")
- ADD: Cost optimization recommendations ("disable X agent to save £Y/month")

### 4. New Non-Functional Requirements

**NFR-L1: Localization & Internationalization**
- Multi-language support (English, Spanish, French, German priority)
- Timezone configuration (all times in user's local timezone)
- Currency preference (GBP, USD, EUR, etc.)
- Date/time format localization (DD/MM/YYYY vs MM/DD/YYYY)
- News source localization (French news for French stocks)

**NFR-C1: Compliance & Regulatory Tooling**
- Configurable audit detail level (minimal, standard, comprehensive)
- Explainability reports (agent reasoning, data sources, decision path exportable as PDF)
- Tax reporting exports (capital gains, dividends, wash sales in CSV/PDF)
- Regulatory compliance modes (FCA, SEC, MiFID II specific requirements)
- Trade justification logs (required for professional/institutional users)

### 5. Update Executive Summary

**CHANGE FROM:**
"A 20-agent AI system running overnight (1am-7am) that delivers daily report by 7am"

**CHANGE TO:**
"A 20-agent AI system running on your schedule (default overnight 1am-7am, fully configurable) that delivers reports when and how you want them - morning email, afternoon Slack update, real-time alerts, or on-demand analysis anytime."

**ADD to "What Makes This Special":**
```markdown
5. **Total Flexibility & Control** (User Empowerment)
   - Schedule: Morning, afternoon, multiple times daily, weekends, or on-demand anytime
   - Scope: Analyze entire market, specific sectors, custom ticker lists, or single stocks
   - Output: Email, SMS, Slack, PDF, JSON - whatever format, whenever you want
   - Strategy: Run multiple portfolios with different strategies simultaneously
   - Execution: Manual approval, auto-execute within guardrails, or paper trade
   - Agents: Enable/disable, weight, customize, add your own investor personas
   - **Result:** System adapts to YOUR life, YOUR strategy, YOUR preferences - not the other way around
```

---

## Why This All Matters

**Development:**
- Drives configuration architecture (everything externalized)
- Ensures testability (can test different schedules, scopes, modes)
- Future-proofs system (easy to add new channels, modes, features)

**Users:**
- **Adaptability:** "I work night shifts, want 10pm report" - DONE
- **Control:** "I only trust value investing, disable growth agents" - DONE
- **Experimentation:** "Try conservative strategy for a month, then aggressive" - DONE
- **Life events:** "Going on vacation, pause for 2 weeks" - DONE
- **Crisis response:** "Market crashed, analyze everything NOW" - DONE

**Business (Phase 3):**
- Professional traders need this flexibility (regulatory, multi-portfolio, custom strategies)
- International expansion requires localization
- Institutional clients need compliance tooling
- Differentiation: "We're flexible, competitors are rigid black boxes"

---

## Bottom Line

**Current PRD treats system as:**
- Single-user, single-portfolio, single-strategy
- Fixed schedule (1am-7am, 7am delivery, Monday-Friday)
- Fixed scope (entire FTSE All-Share)
- Fixed workflow (discover → analyze → recommend → user executes)
- Fixed output (email at 7am)

**Reality of users like Longy:**
- Multiple portfolios (ISA, SIPP, taxable, speculative)
- Variable schedule (sometimes want afternoon update, sometimes on-demand)
- Focused analysis (sector rotation, specific watchlist, custom screens)
- Different workflows (sometimes manual, sometimes want auto-execution within limits)
- Multi-channel needs (email summary, Slack alerts, JSON for Excel dashboard)

**The PRD needs to reflect a FLEXIBLE SYSTEM, not a rigid automation.**

---

## Next Steps

1. **Review this comprehensive gap analysis**
2. **Prioritize which flexibility dimensions are MVP vs. Growth vs. Vision**
3. **Integrate critical gaps into PRD (scheduling, ad-hoc, scope, output, workflow)**
4. **Update all hardcoded references to "default: X, user-configurable"**
5. **Add 7 new FRs (FR-10 through FR-15, plus FR-6.4)**
6. **Enhance existing FRs (FR-4.2, FR-5, NFR-P4)**
7. **Add 2 new NFRs (NFR-L1, NFR-C1)**
8. **Update Executive Summary to highlight flexibility as differentiator**

**Then proceed to epics.md creation with flexibility baked into every epic.**
