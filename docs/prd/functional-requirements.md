# Functional Requirements

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

**Provider:** EOD Historical Data (https://eodhd.com/)
**Plan:** All-In-One Package
**Cost:** ~£85/month ($99.99/month, or $999/year)

**Delivers:**
- **30-year historical price data:** OHLCV (Open, High, Low, Close, Volume) for 150,000+ tickers globally including comprehensive LSE and FTSE All-Share coverage
- **Deep fundamentals:** Income statements, balance sheets, cash flow statements (quarterly and annual) with 10+ years history
- **Financial ratios & metrics:** P/E, P/B, PEG, ROE, ROA, debt ratios, margins, growth rates—calculated and ready to use
- **Analyst estimates:** Consensus revenue estimates, EPS estimates, earnings trends, surprise data (normally £1000s/month from services like I/B/E/S)
- **Corporate actions:** Dividends, stock splits, buybacks, M&A announcements
- **Earnings calendar:** Upcoming and historical earnings dates with estimate vs. actual data
- **Macroeconomic indicators:** UK GDP, inflation (CPI), interest rates, unemployment—no need for separate macro API
- **Technical indicators:** Pre-calculated RSI, MACD, SMA, Bollinger Bands (optional—can also calculate locally)
- **100,000 API calls/day:** Generous quota eliminates rate limit concerns

**UK-Specific Strengths:**
- Native LSE support (exchange code: 'LSE', MIC: XLON)
- Handles UK quirks: pence vs. pounds pricing, IFRS accounting standards
- Comprehensive FTSE 100/250/All-Share coverage
- UK dividend data specifically validated and maintained

**Why This Replaces 5+ Free APIs:**
✅ Single source of truth for fundamentals—no data aggregation complexity
✅ No rate limit juggling across multiple providers
✅ Analyst estimates included (unique value at this price point)
✅ Consistent data quality—no US-centric bias issues
✅ One API integration to maintain instead of five

**Tier 2: Intelligence Layer - CityFALCON** (~£15-40/month)

**Provider:** CityFALCON (https://www.cityfalcon.ai/)
**Plan:** Personal Silver/Gold or Commercial Starter
**Cost:** ~£15-40/month depending on plan

**Delivers:**
- **UK RNS (Regulatory News Service) feed:** Official regulatory announcements from LSE-listed companies
- **Director dealings:** Properly parsed PDMR (Person Discharging Managerial Responsibilities) shareholding notifications—high-signal insider trading data
- **News sentiment scoring:** NLP-powered sentiment analysis trained specifically on financial text
- **Categorized news:** Automatic tagging (M&A, earnings, director dealings, trading updates, dividends)
- **Real-time alerts:** Push notifications for breaking RNS announcements

**UK-Specific Strengths:**
- Built FOR the UK market (not US-centric like most APIs)
- Understands UK regulatory structure (RNS vs. SEC filings)
- Parses unstructured RNS text into structured data
- Director dealings properly extracted (unlike generic APIs that only handle SEC Form 4)

**Why This Replaces Web Scraping + NewsAPI:**
✅ No fragile web scrapers to maintain (Investegate, LSE.co.uk)
✅ Professionally structured director dealings data—no text parsing required
✅ Sentiment scoring included—no need to build NLP engine
✅ Official RNS feed access—faster and more reliable than scraping
✅ Legal and compliant—no robots.txt or terms-of-service concerns

**Tier 3: Execution Layer - Interactive Brokers API** (~£10/month)

**Provider:** Interactive Brokers (https://www.interactivebrokers.com/)
**Integration:** IBKR API (Python library: `ib_insync`)
**Cost:** ~£10/month for LSE Level 1 market data subscription (standard brokerage account)

**Delivers:**
- **Real-time quotes:** Live bid/ask prices at point of trade execution
- **Order routing:** Direct order placement via API
- **Portfolio tracking:** Real-time position updates, P&L tracking
- **Trade confirmations:** Automated trade logging

**Why This Solves Real-Time Pricing:**
✅ You need a broker anyway—leverage their data feed
✅ Real-time data only required at execution, not for analysis
✅ Eliminates need for expensive standalone real-time API subscription
✅ Seamless execution workflow (analyze → decide → execute all via API)

**Strategic Rationale for 3-Tier Architecture:**

1. **Analysis uses delayed/EOD data** (EODHD): Fundamental strategies don't require real-time prices. Overnight batch processing analyzes valuation, trends, catalysts using historical data.

2. **Intelligence uses specialist UK source** (CityFALCON): RNS and director dealings are UK-specific. Generic global APIs fail here. CityFALCON solves the "UK data gap" problem.

3. **Execution uses broker feed** (IBKR): At the moment of trade, query broker for live quote. This decouples analysis (where 15-min delay is fine) from execution (where real-time matters).

**Total Monthly Cost:** ~£125/month for data (£85 + £30 + £10)
**Remaining budget:** £75/month for LLM API costs (plenty for 20-agent system analyzing 10-15 stocks/day)

---

**FR-5.2: Data Integration Implementation**

**EODHD Integration:**
```python
import requests

class EODHDClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://eodhistoricaldata.com/api"

    def get_fundamentals(self, ticker):
        """Fetch complete fundamental data for UK stock"""
        url = f"{self.base_url}/fundamentals/{ticker}.LSE"
        params = {'api_token': self.api_key, 'fmt': 'json'}
        response = requests.get(url, params=params)
        return response.json()

    def get_prices(self, ticker, start_date, end_date):
        """Fetch historical price data"""
        url = f"{self.base_url}/eod/{ticker}.LSE"
        params = {
            'api_token': self.api_key,
            'from': start_date,  # YYYY-MM-DD
            'to': end_date,
            'fmt': 'json'
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_analyst_estimates(self, ticker):
        """Fetch analyst estimates and earnings data"""
        fundamentals = self.get_fundamentals(ticker)
        return {
            'earnings_trend': fundamentals.get('Earnings', {}).get('Trend'),
            'earnings_annual': fundamentals.get('Earnings', {}).get('Annual'),
            'revenue_estimates': fundamentals.get('Earnings', {}).get('Trend')
        }
```

**CityFALCON Integration:**
```python
class CityFALCONClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.cityfalcon.com/v0.2"

    def get_director_dealings(self, ticker, days=30):
        """Fetch recent director dealing announcements"""
        url = f"{self.base_url}/stories"
        params = {
            'access_token': self.api_key,
            'identifiers': f'{ticker}.LSE',
            'categories': 'dir',  # Director dealings category
            'time_filter': f'd{days}'  # Last N days
        }
        response = requests.get(url, params=params)
        stories = response.json().get('stories', [])

        # Filter for actual director dealings (buy/sell transactions)
        dealings = []
        for story in stories:
            if 'director' in story['title'].lower() or 'pdmr' in story['title'].lower():
                dealings.append({
                    'date': story['publishTime'],
                    'title': story['title'],
                    'url': story['url'],
                    'sentiment': story.get('score', 0)
                })
        return dealings

    def get_news_with_sentiment(self, ticker, days=7):
        """Fetch recent news with sentiment scores"""
        url = f"{self.base_url}/stories"
        params = {
            'access_token': self.api_key,
            'identifiers': f'{ticker}.LSE',
            'time_filter': f'd{days}',
            'languages': 'en'
        }
        response = requests.get(url, params=params)
        stories = response.json().get('stories', [])

        return [{
            'title': story['title'],
            'description': story.get('description', ''),
            'url': story['url'],
            'published': story['publishTime'],
            'sentiment_score': story.get('score', 0),  # CityFALCON proprietary score
            'source': story.get('source', {}).get('name')
        } for story in stories]
```

**IBKR Integration:**
```python
from ib_insync import IB, Stock

class IBKRClient:
    def __init__(self):
        self.ib = IB()

    def connect(self):
        """Connect to IBKR TWS or Gateway"""
        self.ib.connect('127.0.0.1', 7497, clientId=1)  # TWS paper trading

    def get_realtime_quote(self, ticker):
        """Get real-time bid/ask for execution"""
        contract = Stock(ticker, 'LSE', 'GBP')
        self.ib.qualifyContracts(contract)
        ticker_obj = self.ib.reqMktData(contract)
        self.ib.sleep(2)  # Wait for data

        return {
            'bid': ticker_obj.bid,
            'ask': ticker_obj.ask,
            'last': ticker_obj.last,
            'volume': ticker_obj.volume
        }

    def place_order(self, ticker, quantity, action='BUY', order_type='LMT', limit_price=None):
        """Place order via IBKR API"""
        from ib_insync import LimitOrder, MarketOrder

        contract = Stock(ticker, 'LSE', 'GBP')
        self.ib.qualifyContracts(contract)

        if order_type == 'LMT':
            order = LimitOrder(action, quantity, limit_price)
        else:
            order = MarketOrder(action, quantity)

        trade = self.ib.placeOrder(contract, order)
        return trade
```

**Ticker Format Handling:**
- **EODHD format:** `VOD.LSE` (ticker.exchange)
- **CityFALCON format:** `VOD.LSE` (same)
- **IBKR format:** `VOD` with exchange parameter `'LSE'`
- **Pence vs. Pounds:** EODHD returns prices in native format (some UK stocks in pence). System SHALL automatically detect and convert to pounds where needed for consistency.

---

**FR-5.3: Data Caching**

System SHALL implement aggressive caching to minimize API calls and costs.

**Caching Strategy:**

| **Data Type** | **TTL (Time To Live)** | **Refresh Trigger** | **Rationale** |
|---------------|------------------------|---------------------|---------------|
| **EOD Prices** | 24 hours | After market close (4:30 PM GMT) | EOD data doesn't change intraday |
| **Fundamentals** | 7 days | On earnings release | Financial statements update quarterly |
| **Analyst Estimates** | 7 days | On earnings release | Estimates update after earnings |
| **News** | 1 hour | None | News is time-sensitive |
| **Director Dealings** | 24 hours | Daily morning refresh (7 AM) | RNS released overnight |
| **Sentiment Scores** | 1 hour | None | Sentiment evolves intraday |
| **Macro Indicators** | 30 days | On official release dates | Macro data releases monthly/quarterly |
| **Real-time Quotes** | 0 (no cache) | Every request | Must be fresh for execution |

**Cache Implementation:**
- **Storage:** Redis (for production) or local file cache (for development)
- **Key Format:** `{data_type}:{ticker}:{date}:{params_hash}`
- **Example:** `fundamentals:VOD:2025-11-22:full`
- **Eviction Policy:** LRU (Least Recently Used) with max cache size 10 GB

**Cache Warming:**
- On system startup, warm cache with FTSE 100 fundamentals and recent prices
- During overnight batch run, refresh all cached data for watchlist stocks
- Result: Morning analysis runs use almost entirely cached data (fast, cost-effective)

---

**FR-5.4: Data Validation & Quality Checks**

System SHALL validate all incoming data to detect errors before they pollute analysis.

**Validation Rules:**

**Price Data:**
- Reject if price < 0 or price > £10,000 (likely error)
- Reject if single-day price change > 50% (check for stock split/corporate action first)
- Reject if volume < 0
- Flag if volume = 0 for multiple consecutive days (low liquidity warning)

**Fundamental Data:**
- Reject if critical fields missing (market cap, total debt, total equity)
- Flag if debt/equity ratio differs >10% between calculated and reported
- Flag if P/E ratio < 0 (negative earnings—loss-making company)
- Reject if earnings date in future but marked as "actual" (likely error)

**News/Sentiment Data:**
- Reject if timestamp > current time (future date impossible)
- Flag if sentiment score outside expected range (e.g., CityFALCON scores typically -1 to +1)

**Quality Check Workflow:**
1. Fetch data from API
2. Run validation rules
3. If validation fails:
   - Log error with ticker, data type, timestamp, reason
   - Try fallback source (if available)
   - If all sources fail, skip analysis for this stock with warning in report
4. If validation passes, cache and use data

**Audit Logging:**
- Log ALL data quality issues to database table: `data_quality_log`
- Fields: timestamp, ticker, data_type, source, issue_description, resolution
- Review monthly to identify systematic issues with providers

---

**FR-5.5: Audit Trail**

System SHALL maintain comprehensive audit trail of all data access and agent decisions for learning, debugging, and potential regulatory compliance.

**Audit Requirements:**

**Data Access Logging:**
- Log every API call:
  - Timestamp, provider (EODHD/CityFALCON/IBKR), endpoint, ticker(s) requested
  - Response status (success/failure), latency (milliseconds)
  - Cache hit/miss status
  - Cost (if applicable—track API quota usage)

**Agent Decision Logging:**
- Log every agent analysis:
  - Agent name, ticker analyzed, timestamp
  - Input data summary (price range, fundamentals snapshot, news count, sentiment score)
  - Output (signal: BUY/SELL/HOLD, confidence score 0-100, reasoning text)
  - LLM model used (GPT-4o, Claude-3.5, etc.)
  - Token usage (prompt tokens, completion tokens, cost)

**Trade Decision Logging:**
- Log Portfolio Manager decisions:
  - Timestamp, ticker, recommendation (BUY/SELL/HOLD)
  - Position size, entry price target, stop-loss, take-profit levels
  - Contributing signals (which agents voted BUY, signal strength)
  - Risk assessment (Risk Manager input)
  - User action (approved/rejected/modified)

**Execution Logging:**
- Log actual trades executed:
  - Timestamp, ticker, action (BUY/SELL), quantity, price
  - Order type (market/limit), fill status
  - Broker confirmation ID
  - Outcome after 30/60/90 days (profit/loss)

**Retention Policy:**
- **Data access logs:** 90 days
- **Agent decision logs:** 2 years (support learning and performance analysis)
- **Trade logs:** Permanent (regulatory requirement for hedge fund path)

**Storage:**
- Database tables: `api_call_log`, `agent_decision_log`, `trade_recommendation_log`, `execution_log`
- Indexed by: ticker, timestamp, agent_name for fast queries

**Reporting:**
- Weekly summary: Total API calls by provider, cost, success rate
- Monthly summary: Agent performance (win rate by agent), LLM cost breakdown
- Ad-hoc queries: "Show me all BUY recommendations for VOD in last 90 days"

---

**FR-5.6: Ad-Hoc Research Inbox**

System SHALL provide a designated file location for user to manually inject supplemental research not captured by automated data sources, supporting organic discovery of what research types matter before formalizing automation.

**Research Inbox Location:**
- **Path:** `/docs/research-inbox/`
- **Sub-folders:**
  - `/docs/research-inbox/[TICKER]/` — Ticker-specific research (e.g., `/docs/research-inbox/VOD/`)
  - `/docs/research-inbox/macro/` — Macro and sector research
  - `/docs/research-inbox/general/` — Uncategorized insights

**File Naming Convention:**
```
[TICKER]_[YYYYMMDD]_[description].[ext]

Examples:
- VOD_20251122_competitor-analysis.pdf
- BP_20251120_industry-outlook.md
- macro_20251119_BOE-policy-notes.txt
- general_ideas.md
```

**Supported Formats:**
- **Text files:** .txt, .md (plain text research notes, can include markdown formatting and URLs)
- **Documents:** .pdf (industry reports, analyst research, whitepapers)
- **Web content:** .html (saved web pages, archived articles)
- **Data files:** .csv (custom scraped data, comparison tables)

**Agent Integration:**

**When Agents Check Research Inbox:**
- **Portfolio Manager:** Before making final BUY decision, checks `/research-inbox/[TICKER]/` for files dated within last 30 days
- **Deep Analysis (On-Demand):** User can explicitly request: "Analyze VOD including research inbox"
- **Weekly Review:** Portfolio Manager checks `/research-inbox/macro/` during weekly portfolio positioning review

**Agent Behavior (Pseudocode):**
```python
def analyze_stock(ticker):
    # Standard automated data
    fundamentals = eodhd.get_fundamentals(ticker)
    news = cityfalcon.get_news(ticker, days=7)
    sentiment = cityfalcon.get_sentiment(ticker)

    # Check research inbox for supplemental user-provided research
    research_files = scan_research_inbox(ticker, days=30)

    additional_context = []
    if research_files:
        for file in research_files:
            content = read_file(file)  # Read PDF, txt, md, html, csv
            additional_context.append({
                'filename': file.name,
                'date': file.date_modified,
                'content': content[:5000]  # First 5000 chars to fit in LLM context
            })

    # Build LLM prompt with all available data
    prompt = f"""
    Analyze {ticker} using ALL available information:

    **Automated Data:**
    - Fundamentals: {format_fundamentals(fundamentals)}
    - Recent News: {format_news(news)}
    - Sentiment: {sentiment}

    **User-Provided Research (Research Inbox):**
    {format_research_context(additional_context) if additional_context else "No user research files found"}

    Provide BUY/SELL/HOLD recommendation.
    If user research contradicts automated data, explain the discrepancy and use your judgment.
    Cite sources (e.g., "According to user research file VOD_analysis.pdf...")
    """

    return llm.analyze(prompt)
```

**User Workflow Examples:**

**Scenario 1: Found Valuable Industry Report**
1. User discovers McKinsey report on UK telecom sector competitiveness
2. Saves as `/docs/research-inbox/VOD/VOD_20251122_mckinsey-telecom-report.pdf`
3. Next time system analyzes Vodafone (or user triggers on-demand analysis), agent reads PDF
4. Agent includes insight in recommendation: "Based on McKinsey telecom report (user research inbox), Vodafone faces intensifying competition from Three UK merger..."

**Scenario 2: Manual Deep Dive**
1. User spends weekend researching BP, saves notes to `/docs/research-inbox/BP/BP_20251120_energy-transition-thesis.md`
2. Monday morning, user runs: "Analyze BP, include research inbox"
3. Agent synthesizes: BP fundamentals + news + user's energy transition thesis → recommendation
4. Recommendation cites user research: "User's research highlights BP's undervalued offshore wind assets..."

**Scenario 3: Macro Positioning**
1. User reads Bank of England minutes, saves notes to `/docs/research-inbox/macro/BOE_20251119_rate-cut-signals.md`
2. During weekly portfolio review, Portfolio Manager checks macro folder
3. Agent: "User's BOE analysis suggests rate cuts coming Q2 2026 → favor rate-sensitive sectors (REITs, utilities)"

**Non-Goals (Phase 1 - Intentionally Simple):**
- ❌ Automatic URL fetching (user manually saves web pages for now)
- ❌ OCR for scanned images (text-based formats only)
- ❌ Automated categorization/tagging (simple folder structure sufficient)
- ❌ Research expiration/archiving (user manages manually)
- ❌ Integration with Zotero/Notion/etc. (just a file folder)

**Formalization Path (Future):**
After 3-6 months of usage, review research inbox to identify patterns:
- **Pattern:** "I keep adding competitor analysis PDFs" → Build Competitor Tracking Agent
- **Pattern:** "Lots of sector reports from Berenberg" → Integrate Berenberg research feed
- **Pattern:** "Many macro indicators from TradingEconomics" → Add TradingEconomics API
- **Pattern:** "Never used it" → Remove feature

This approach lets **real usage drive automation priorities** rather than speculating upfront about what research matters.

---

**FR-5.7: Fallback & Error Handling**

System SHALL implement graceful degradation when data sources fail, ensuring analysis can continue with partial data rather than complete failure.

**Fallback Strategy:**

**If EODHD Fails (Primary Source):**
1. Use cached data (up to 7 days old acceptable for fundamentals)
2. Alert user: "EODHD unavailable, using cached data from [date]. Recommendations may be stale."
3. Reduce analysis scope: Skip discovery scans, only monitor active portfolio for SELL signals
4. Continue execution: IBKR can still provide real-time quotes for trades

**If CityFALCON Fails (Intelligence Layer):**
1. Use cached news/sentiment (up to 24 hours old)
2. Skip director dealings analysis (no reliable fallback)
3. Alert user: "CityFALCON unavailable, director dealings signals unavailable today"
4. Continue with reduced signals: Fundamental and technical analysis still work

**If IBKR Fails (Execution Layer):**
1. **CRITICAL:** Cannot execute trades without broker connection
2. Alert user immediately: "IBKR connection lost. Manual execution required."
3. Provide manual execution instructions in report: "BUY 500 shares VOD at £0.72 or better"
4. User executes via IBKR web interface or phone

**Partial Data Handling:**
- If one stock's data fetch fails, skip that stock but continue analyzing others
- Report partial failures: "Analyzed 15/20 stocks. Failed: VOD (EODHD timeout), BP (no fundamentals), HSBC (data quality issue)"
- Never fail entire analysis run due to single stock failure

**Circuit Breaker Pattern:**
- If EODHD fails 3 consecutive times (3 days), send urgent alert: "EODHD persistently unavailable. Check API key, account status, service status."
- Temporarily reduce API call frequency if getting rate limit errors (back off)

**Error Logging:**
- Log all failures to `system_error_log` table: timestamp, component, error message, resolution
- Weekly review: Identify patterns (e.g., "CityFALCON timeout every Wednesday 2am" → adjust schedule)

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
