# AI Hedge Fund - Networked Agent Architecture

**Version:** 1.0
**Date:** 2025-11-16
**Status:** Design Phase - From Brainstorming Session

---

## Executive Summary

This document defines the architecture for a networked multi-agent system designed to discover, analyze, and recommend UK stock investments. The system uses 20+ specialized AI agents that communicate via signals to create emergent intelligence superior to individual agents operating in isolation.

**Key Innovation:** Agents work as a network, not a pipeline - discoveries trigger cascades, signals converge to build conviction, and challenges validate decisions.

---

## System Architecture Overview

### The 20-Agent Network

#### DISCOVERY LAYER (7 Searcher Agents)
**Purpose:** Continuously scan multiple data sources to surface investment opportunities

1. **News Scanner Agent**
   - Sources: BBC, FT, Reuters, LSE announcements
   - Triggers: Major contracts, management changes, regulatory approvals, M&A
   - Output: 5-10 stocks/day with news catalysts
   - Signal: `NEW_CATALYST`

2. **Insider Trading Agent**
   - Source: LSE director dealings
   - Triggers: Significant insider buying (multiple directors, large amounts)
   - Output: 3-5 stocks/week with insider conviction
   - Signal: `INSIDER_CONVICTION`

3. **Volume & Price Action Agent**
   - Source: Market data feeds
   - Triggers: Volume spikes (3x+), breakouts, 52-week highs
   - Output: 5-10 stocks/week with technical triggers
   - Signal: `UNUSUAL_ACTIVITY`

4. **Fundamental Screener Agent**
   - Source: Financial statements, market data
   - Screens: Low P/E + high ROE, high growth, low debt, Naked Trader checklist
   - Output: Top 20 stocks by each screen weekly
   - Signal: `FUNDAMENTAL_MATCH`

5. **Earnings Surprise Agent**
   - Source: Earnings reports, analyst estimates
   - Triggers: Beat by 10%+, guidance raises, margin expansion
   - Output: 3-5 stocks/week post-earnings
   - Signal: `EARNINGS_SURPRISE`

6. **Analyst Activity Agent**
   - Source: Broker research, analyst ratings
   - Triggers: Multiple upgrades, significant target increases
   - Output: 5-10 stocks/week with analyst momentum
   - Signal: `ANALYST_SHIFT`

7. **Corporate Actions Agent**
   - Source: RNS announcements
   - Triggers: Buybacks, special dividends, spinoffs, M&A, activist involvement
   - Output: 2-3 stocks/week in special situations
   - Signal: `SPECIAL_SITUATION`

---

#### MACRO/SECTOR LAYER (2-3 Guide Agents)
**Purpose:** Provide top-down context that filters and weights discovery signals

8. **Macro Economist Agent**
   - Frequency: Weekly analysis
   - Monitors: GDP, inflation, interest rates, unemployment, PMI, BoE policy
   - Output: Current regime (expansion/recession/stagflation) + implications
   - Signal: `MACRO_REGIME_CHANGE`

9. **Sector Rotation Agent**
   - Frequency: Weekly analysis
   - Monitors: Relative sector performance, flows, economic sensitivity
   - Output: Top 3 sectors to overweight, bottom 3 to avoid
   - Signal: `SECTOR_PREFERENCES_UPDATE`

10. **Industry Specialist Agents** (Optional - 3-5 agents for key sectors)
    - Examples: Mining, Financials, Healthcare, Energy, Tech specialists
    - Monitors: Industry-specific metrics, commodity prices, regulations
    - Output: Best-positioned companies within sectors
    - Signal: `INDUSTRY_INSIGHT`

---

#### ANALYSIS LAYER (8 Expert Agents)
**Purpose:** Deep evaluation of stocks surfaced by Discovery Layer

11. **Value Investor Agent** (Buffett/Graham)
    - Analysis: Intrinsic value (DCF, multiples), moat assessment, margin of safety
    - Score: 0-100 + confidence level
    - Signal: `VALUE_ASSESSMENT`

12. **Growth Investor Agent** (Peter Lynch)
    - Analysis: Growth sustainability, market opportunity, competitive dynamics
    - Score: 0-100 + confidence level
    - Signal: `GROWTH_ASSESSMENT`

13. **Contrarian Agent** (Michael Burry)
    - Analysis: What's the market missing? What's mispriced? Sentiment extremes
    - Score: 0-100 + confidence level
    - Signal: `CONTRARIAN_OPPORTUNITY` or `CONTRARIAN_WARNING`

14. **Naked Trader Agent** (Robbie Burns)
    - Checklist: Profitable? Growing? Low debt? Clean chart?
    - Score: Pass/Fail on each criterion
    - Signal: `NAKED_TRADER_SCORE`

15. **Quality/Moat Agent**
    - Analysis: Competitive advantages, pricing power, switching costs, network effects
    - Score: 0-100 + confidence level
    - Signal: `QUALITY_ASSESSMENT`

16. **Technical Analyst Agent**
    - Analysis: Chart patterns, support/resistance, momentum indicators
    - Score: 0-100 + confidence level
    - Signal: `TECHNICAL_CONFIRMATION` or `TECHNICAL_WARNING`

17. **Catalyst Detective Agent**
    - Analysis: What specific event will drive this higher in 3-6 months?
    - Output: Identified catalyst + probability + timeline
    - Signal: `CATALYST_IDENTIFIED`

18. **Sentiment Analyst Agent**
    - Analysis: News tone, social sentiment, analyst positioning
    - Score: 0-100 (contrarian indicator - extreme negative = bullish)
    - Signal: `SENTIMENT_ASSESSMENT`

---

#### DECISION LAYER (2 Decider Agents)
**Purpose:** Synthesize all signals and make final decisions

19. **Risk Manager Agent**
    - Role: Challenge every thesis, identify downside
    - Analysis: What could go wrong? Position sizing, stop-loss levels, correlation risk
    - Output: Risk score, position size recommendation, stop-loss
    - Signal: `RISK_ALERT` or `RISK_ACCEPTABLE`

20. **Portfolio Manager Agent**
    - Role: Final synthesis, buy/sell/hold decisions
    - Input: All agent signals, current portfolio state, cash levels
    - Output: BUY / SELL / HOLD / WATCHLIST
    - Signal: `BUY_RECOMMENDATION`, `SELL_RECOMMENDATION`, `WATCHLIST_ADD`

---

#### SUPPORT AGENT

21. **Watchlist Agent**
    - Role: Monitor stocks waiting for conditions to be met
    - Tracks: Price targets, event triggers, macro conditions
    - Output: Alerts when conditions met, triggers re-validation
    - Signal: `WATCHLIST_TRIGGER`

---

## Signal Network Protocol

### Communication Model

**Agents communicate via BROADCAST → LISTEN → REACT pattern:**

1. **BROADCAST:** Agent makes a discovery → publishes signal to message bus
2. **LISTEN:** Other agents subscribe to relevant signal types
3. **REACT:** Receiving agents trigger their own analysis → broadcast new signals

### Signal Types

#### Discovery Signals
- `NEW_CATALYST` - News Scanner (news event detected)
- `INSIDER_CONVICTION` - Insider Trading Agent (director dealings)
- `UNUSUAL_ACTIVITY` - Volume Agent (volume/price action)
- `FUNDAMENTAL_MATCH` - Screener Agent (passed fundamental screen)
- `EARNINGS_SURPRISE` - Earnings Agent (beat/miss)
- `ANALYST_SHIFT` - Analyst Activity (upgrades/downgrades)
- `SPECIAL_SITUATION` - Corporate Actions (buyback, M&A, etc.)

#### Context Signals
- `MACRO_REGIME_CHANGE` - Macro Economist (economic environment shift)
- `SECTOR_PREFERENCES_UPDATE` - Sector Rotation (favored/disfavored sectors)
- `INDUSTRY_INSIGHT` - Industry Specialists (sector-specific intelligence)

#### Validation Signals
- `VALUE_ASSESSMENT` - Value Investor
- `GROWTH_ASSESSMENT` - Growth Investor
- `CONTRARIAN_OPPORTUNITY` / `CONTRARIAN_WARNING` - Contrarian Agent
- `QUALITY_ASSESSMENT` - Quality Agent
- `TECHNICAL_CONFIRMATION` / `TECHNICAL_WARNING` - Technical Analyst
- `CATALYST_IDENTIFIED` - Catalyst Detective
- `SENTIMENT_ASSESSMENT` - Sentiment Analyst

#### Decision Signals
- `RISK_ALERT` / `RISK_ACCEPTABLE` - Risk Manager
- `DEEP_ANALYSIS_TRIGGERED` - Portfolio Manager (activates all Analysis Agents)
- `BUY_RECOMMENDATION` - Portfolio Manager
- `SELL_RECOMMENDATION` - Portfolio Manager
- `WATCHLIST_ADD` - Portfolio Manager
- `WATCHLIST_TRIGGER` - Watchlist Agent (condition met)

---

## Signal Convergence & Scoring

### Signal Strength Weights

| Signal Type | Points | Decay Rate |
|-------------|--------|------------|
| Insider buying (significant) | 25 | Slow (3 months) |
| Earnings beat (major) | 20 | Fast (1 week) |
| Corporate action | 20 | Medium (varies) |
| News catalyst (major) | 15 | Medium (2 weeks) |
| Volume spike (5x+) | 15 | Fast (3 days) |
| Fundamental screen match | 15 | Slow (stable) |
| Analyst upgrade | 10 | Medium (1 month) |
| Technical breakout | 10 | Fast (1 week) |

### Macro/Sector Multipliers

| Context | Multiplier |
|---------|------------|
| Macro aligned | 1.5x |
| Sector favored | 1.3x |
| Sector disfavored | 0.7x |
| Macro headwind | 0.5x |

### Convergence Thresholds

**Signal aggregation by stock:**
- **0-30 points:** Low interest → Monitor only
- **31-60 points:** Medium interest → Add to Research Queue
- **61-90 points:** High interest → Trigger Deep Analysis
- **91+ points:** Very high interest → Priority Deep Analysis

**Example Calculation:**
- Company X: Insider buying (25) + News catalyst (15) + Fundamental match (15) = 55 points
- Sector favored multiplier: 55 × 1.3 = 71.5 points
- **Result:** Trigger Deep Analysis (above 61 threshold)

---

## Example Network Flows

### Flow 1: News-Driven Cascade

1. **News Scanner** spots "Company X announces £500M contract win"
   - Broadcasts: `NEW_CATALYST` → Company X, catalyst_type: "major_contract"

2. **Industry Specialist** (listening) → Analyzes sector significance
   - If significant: Broadcasts `SECTOR_IMPACT`

3. **Macro Economist** (listening for SECTOR_IMPACT) → Checks for broader trend
   - If trend detected: Broadcasts `MACRO_THEME` (e.g., infrastructure spending)

4. **Fundamental Screener** (listening for MACRO_THEME) → Finds peer companies
   - Runs screen: All engineering/construction with strong fundamentals
   - Broadcasts `PEER_COMPARISON` with list of 10 companies

5. **Technical Analyst** (listening for NEW_CATALYST on Company X) → Checks chart
   - If breakout: Broadcasts `TECHNICAL_CONFIRMATION`

6. **Portfolio Manager** receives multiple signals on Company X:
   - NEW_CATALYST + TECHNICAL_CONFIRMATION + SECTOR_IMPACT
   - **Convergence detected (3 signals)** → Triggers `DEEP_ANALYSIS`

7. **All 8 Analysis Agents** activate on Company X
   - Each provides detailed assessment

8. **Risk Manager** challenges the thesis
   - "What could go wrong?"

9. **Portfolio Manager** synthesizes all inputs → BUY decision

---

### Flow 2: Insider Trading Cascade

1. **Insider Trading Agent** spots "3 directors of Company Y bought £500k"
   - Broadcasts: `INSIDER_CONVICTION` → Company Y, conviction: "high"

2. **News Scanner** (listening) → Searches for recent news
   - If found: `INSIDER_CATALYST_LINK`
   - If not found: `INSIDER_UNKNOWN_CATALYST` (more interesting!)

3. **Earnings Agent** (listening) → Checks earnings calendar
   - If earnings in 4 weeks: `POTENTIAL_EARNINGS_BEAT` (insiders may know)

4. **Technical Analyst** (listening) → Checks if buying at support/breakout
   - If aligned: `TECHNICAL_CONFIRMATION`

5. **Contrarian Agent** (listening for INSIDER_UNKNOWN_CATALYST) → Checks sentiment
   - If hated by market: `CONTRARIAN_OPPORTUNITY`

6. **Portfolio Manager** receives convergence:
   - Insider conviction + Unknown catalyst + Contrarian setup + Technical confirmation
   - **High conviction setup** → Triggers DEEP_ANALYSIS

---

### Flow 3: Macro-Down Cascade

1. **Macro Economist** (weekly analysis) identifies "UK entering recession"
   - Broadcasts: `MACRO_REGIME_CHANGE` → regime: "early_recession", favor: "defensives"

2. **Sector Rotation Agent** (listening) → Updates sector rankings
   - Defensives (Healthcare, Utilities, Staples) → TOP
   - Cyclicals (Mining, Housebuilders) → BOTTOM
   - Broadcasts: `SECTOR_PREFERENCES_UPDATE`

3. **ALL Discovery Agents** (listening) → Adjust scoring
   - Weight defensive sectors 2x higher
   - Downweight or filter cyclical triggers

4. **Fundamental Screener** (listening) → Runs defensive screens
   - High dividend + low beta + stable earnings
   - Broadcasts: `DEFENSIVE_OPPORTUNITIES` with list

5. **Discovery Agents** find Company Z (healthcare):
   - News Scanner: FDA approval
   - Fundamental Screen: Appears in defensive list
   - Analyst Activity: 2 upgrades
   - **3 signals converge!**

6. **Portfolio Manager**:
   - Company Z = right sector + multiple signals + macro tailwind
   - Priority analysis triggered

---

## Adversarial Challenge System

### Devil's Advocate Protocol

**Before any BUY recommendation:**

**Step 1: Portfolio Manager broadcasts proposed thesis**
```
THESIS_PROPOSED:
Stock: Company X
Recommendation: BUY
Bull Case: [reasons]
Price: £8.50
Target: £12
Stop: £7.50
```

**Step 2: Challenge Round**

**Risk Manager (mandatory challenger):**
- "What could go wrong?"
- Identifies risks: customer concentration, high debt, market headwinds
- Challenge Score: 0-10 risk rating

**Contrarian Agent (mandatory challenger):**
- "Why is the market wrong?"
- "If this is so obvious, why hasn't it been priced in?"
- Identifies: value traps, falling knives, sector downtrends

**Technical Analyst:**
- Checks for false breakouts, weak volume, resistance levels

**Sentiment Analyst:**
- "Is this one positive in a sea of negatives?"

**Step 3: Response Round**

Bull case agents respond to specific challenges

**Step 4: Portfolio Manager Synthesis**

| Factor | Bull Case | Bear Case | Weight | Score |
|--------|-----------|-----------|--------|-------|
| Valuation | Cheap P/E | Value trap | High | +2 |
| Catalyst | Major contract | One-off | High | +1 |
| Insider | Heavy buying | Maybe selling later | Med | +2 |
| Technical | Breakout | Weak volume | Med | 0 |
| Risk | Manageable | Concentration | High | -1 |

**Net Score determines:**
- Position size (high conviction = 5%, low = 2%)
- Stop-loss tightness
- Monitoring intensity

---

## Three-Tier Tracking System

### TIER 1: Active Portfolio
- Stocks currently owned
- Monitored daily for SELL signals
- Stop-losses and target prices tracked
- Re-analyzed weekly

### TIER 2: Active Watchlist (Critical Innovation)
**Purpose:** Track stocks that are interesting but waiting for conditions

**Entry reasons:**
- Good company, wrong price: "Buy if drops to £8"
- Right setup, wrong macro: "Buy when recession risk decreases"
- Needs validation: "Buy if next earnings beat"
- Event-dependent: "Buy if insider buying occurs"

**Trigger types:**
- **Price-based:** "Alert when price ≤ £X" or "Alert when P/E ≤ X"
- **Event-based:** "Alert on insider buying" or "Alert on earnings"
- **Macro-based:** "Alert when sector rotation favors"
- **Technical:** "Alert on breakout above resistance"

**Re-validation process:**
When trigger fires:
1. ALL Analysis Agents re-run (is thesis still valid?)
2. News Scanner checks (why did price drop?)
3. Risk Manager evaluates (what changed?)
4. Insider Trading checks (are they buying or selling?)

**Outcomes:**
- **Validated** → BUY (watchlist worked!)
- **Invalidated** → REMOVE (saved from value trap!)
- **Unclear** → ADJUST (new price target or conditions)

### TIER 3: Research Queue
- Stocks currently being investigated
- Triggered by discovery agents
- Not yet BUY or WATCHLIST

---

## Daily Workflow

### Overnight Batch Processing (1am - 6am)

**1:00 AM - Data Collection**
- Pull UK market data: prices, volumes, news, filings, insider trades
- Update watchlist stock prices
- Pull macro data: interest rates, economic indicators

**2:00 AM - Discovery Layer**
- All 7 Discovery Agents scan their domains
- Generate signals for yesterday's events
- Score all signals

**3:00 AM - Signal Aggregation**
- Group signals by stock
- Calculate convergence scores
- Identify stocks above threshold (60+ points)

**4:00 AM - Deep Analysis**
- Run all 8 Analysis Agents on high-scoring stocks
- Run adversarial challenge process
- Generate detailed reports

**5:00 AM - Watchlist Processing**
- Check all watchlist triggers
- Re-validate any triggered watchlist stocks
- Update watchlist status

**6:00 AM - Portfolio Review**
- Review all current holdings
- Check stop-losses, target prices
- Identify SELL signals

**7:00 AM - Report Delivered**

---

### Daily Report Format

**SECTION 1: NEW OPPORTUNITIES** (0-3 stocks)
- BUY recommendations with full analysis
- Signal strength, convergence score
- Bull case, bear case, risks
- Price targets, position sizing, stop-losses

**SECTION 2: WATCHLIST ALERTS** (0-5 stocks)
- Watchlist stocks that triggered
- Re-validation results
- Recommendation: BUY / REMOVE / ADJUST

**SECTION 3: PORTFOLIO UPDATES**
- Current holdings status
- Any SELL recommendations
- Performance vs. benchmarks

**SECTION 4: MARKET CONTEXT** (weekly)
- Macro update
- Sector preferences
- Key themes

**SECTION 5: DISCOVERY SUMMARY**
- What Discovery Agents found
- Interesting stocks below threshold (monitoring)
- Suggested watchlist additions

---

### Weekly Deep Dive (Sunday Evening)

**More thorough analysis:**
- Macro Economist full report
- Sector Rotation detailed update
- Industry Specialists insights
- Portfolio rebalancing recommendations
- Watchlist cleanup (remove stale entries)
- Performance attribution (what worked/didn't)

---

## Technical Implementation

### Message Bus Architecture

**Central communication hub:**
```python
class SignalBus:
    def publish(signal: Signal):
        # Broadcast to all subscribers

    def subscribe(signal_types: List[str], callback: Callable):
        # Register listener
```

**Agent pattern:**
```python
class Agent:
    def analyze(data):
        # Run agent logic
        result = ...

        # Broadcast findings
        signal_bus.publish(Signal(
            type="SIGNAL_TYPE",
            stock="ticker",
            data=result
        ))

    @signal_bus.subscribe(["RELEVANT_SIGNAL"])
    def on_signal(signal):
        # React to other agents
```

### Data Sources

**Market Data:**
- Financial Modeling Prep API
- Alpha Vantage
- Yahoo Finance
- LSE RNS feed

**News:**
- News API
- RSS feeds (BBC, FT, Reuters)

**Insider Trading:**
- LSE director dealings feed

**Fundamentals:**
- Company financial statements APIs
- Screening APIs

---

## Cost Estimation

**Discovery Layer:** ~£30-50/month (mostly API calls, simple prompts)
**Macro/Sector Layer:** ~£10-20/month (weekly, lightweight)
**Analysis Layer:** ~£100-150/month (expensive, but only 10 stocks/day × 8 agents)
**Decision Layer:** ~£20-30/month (synthesis prompts)
**Watchlist:** ~£10-20/month (monitoring, re-validation)

**Total Estimated Cost:** £200-300/month

**Cost per analyzed stock:** ~£1.50-3.00
**Cost per BUY recommendation:** ~£10-20 (including all research)

---

## Success Metrics

**Phase 1 (Months 1-3): Proof of Concept**
- Win rate: 60%+ trades profitable
- Average winner: +10-15%
- Average loser: -5% or less (tight stops)
- Total return: 15-25% over 3 months
- User engagement: Actually enjoys using it

**If successful → Phase 2 Scale-up**

---

## Next Steps

1. Define detailed prompts for each of the 20 agents
2. Build signal bus infrastructure
3. Integrate data APIs
4. Implement watchlist system
5. Create daily report generator
6. Backtest on historical data
7. Paper trade for validation
8. Small real-money test

---

**Document End**
