# Epic 2: Discovery & Market Intelligence

**Goal:** Build overnight batch discovery system that scans 600+ UK stocks, generates signals from multiple sources, applies macro/sector context, and identifies top opportunities for deep analysis.

**User Value:** Wake up to curated investment opportunities discovered overnight—stocks that multiple signals converge on, filtered by macroeconomic context.

**Prerequisites:** Epic 1 (Foundation & Data Architecture)

**FR Coverage:** FR-1.1, FR-1.2, FR-1.3, FR-1.4, FR-1.5, FR-1.6, FR-3.3

---

### Story 2.1: UK Company & Ticker Master Database

**As a** discovery system,
**I want** a comprehensive database of LSE-listed stocks with sector/industry mappings,
**So that** all discovery agents work from the same company universe and can apply sector filters.

**Acceptance Criteria:**

**Given** the system needs to scan UK stocks
**When** the company database is initialized
**Then** it contains:
- 600+ LSE-listed companies (FTSE 100, FTSE 250, FTSE Small Cap)
- Ticker symbols in LSE format (e.g., "VOD.L", "BP.L", "TSCO.L")
- Company name, sector (GICS level 1), industry (GICS level 2)
- Market capitalization tier (Large Cap, Mid Cap, Small Cap)
- Primary exchange (LSE, AIM)
- Active/delisted status
- Last updated timestamp

**And** The database supports queries:
- Get all stocks in sector (e.g., "Financials", "Healthcare")
- Get all stocks by market cap tier
- Get all stocks on specific exchange (LSE vs AIM)
- Validate ticker exists and is active

**And** Database is updated weekly from EODHD API
**And** New IPOs are automatically added
**And** Delisted companies are marked inactive (not removed)

**Prerequisites:** Story 1.2 (Database Schema), Story 1.4 (EODHD API Integration)

**Technical Notes:**
- `stocks` table already defined in Story 1.2
- EODHD endpoint: `/exchange-symbol-list/LSE` for complete stock list
- GICS sector classification: 11 sectors, 24 industry groups
- Market cap tiers: Large (£10B+), Mid (£2B-10B), Small (<£2B)
- AIM stocks: Higher risk, typically excluded from MVP scans (config flag)
- Initial seed: Manual CSV import of FTSE 350 constituents
- Weekly update: Scheduled task fetches full LSE list, compares, updates

---

### Story 2.2: News Scanner Agent - UK Financial News

**As a** discovery agent,
**I want** to scan overnight UK financial news and identify catalysts,
**So that** stocks with news-driven opportunities are surfaced for analysis.

**Acceptance Criteria:**

**Given** overnight news has been published (6pm-6am window)
**When** the News Scanner Agent runs (configurable schedule, default: 2:00 AM)
**Then** it fetches news from configured sources:
```yaml
# config/discovery_agents.yaml
news_scanner:
  enabled: true
  schedule: "0 2 * * *"  # 2 AM daily
  llm_provider: openai  # From agent_config, user can change
  llm_model: gpt-4o-mini  # Configurable - might be claude-haiku, gemini-flash
  sources:
    - name: bbc_business
      type: rss
      url: "http://feeds.bbci.co.uk/news/business/rss.xml"
      priority: high
    - name: financial_times
      type: news_api
      query: "UK stocks OR London Stock Exchange"
      priority: high
    - name: reuters_uk
      type: news_api
      query: "UK business"
      priority: medium
    - name: city_am
      type: rss
      url: "https://www.cityam.com/feed/"
      priority: medium
    - name: lse_rns
      type: api
      endpoint: "eodhd_calendar"
      priority: critical  # Official announcements
```

**And** For each news article, it:
- Extracts mentioned UK company tickers using configured LLM
- Classifies catalyst type from configurable taxonomy
- Scores significance using catalyst scoring rules (see config below)
- Validates ticker against company database
- Stores in `signals` table with `signal_type = "NEWS_CATALYST"`

**And** Catalyst scoring is configuration-driven:
```yaml
# config/signal_scoring.yaml
NEWS_CATALYST:
  base_score: 50
  decay_rate: medium
  decay_period_days: 14
  catalyst_modifiers:
    major_contract: 1.6        # 50 × 1.6 = 80 points
    m&a_announcement: 1.4      # 70 points
    regulatory_approval: 1.2   # 60 points
    management_change_ceo: 0.8 # 40 points
    product_launch: 0.6        # 30 points
  source_multipliers:
    lse_rns: 1.5  # Official RNS = highest signal
    financial_times: 1.2
    bbc_business: 1.0
```

**And** News is deduplicated (same story from multiple sources = 1 signal)
**And** Signal includes metadata: headline, source, URL, summary, raw_text
**And** Failed API calls retry (attempts configurable, default: 3)
**And** Agent runs in < 5 minutes for 50-100 news articles

**Prerequisites:** Story 1.3 (Abstract Data Source Interface), Story 1.8 (Multi-Provider LLM), Story 2.1 (Company Database)

**Technical Notes:**
- **LLM:** Configured via agent_config table (Story 1.8) - NOT hardcoded
- **Default MVP:** gpt-4o-mini (cheap, fast) but user can switch to claude-haiku, gemini-flash
- Prompt pattern: "Extract UK stock tickers and classify the catalyst type from this news article..."
- News API key: `NEWS_API_KEY` environment variable (or multiple APIs configured)
- RSS parsing: `feedparser` Python library
- **Extensibility:** User can add new news sources via config without code changes
- RNS announcements prioritized (official company news)
- Store raw article text for later agent analysis
- Cost estimate: ~50 articles/day × 500 tokens = $0.01/day (varies by LLM choice)

---

### Story 2.3: Fundamental Screener Agent - Data-Driven Batch Scanning

**As a** discovery agent,
**I want** to run configurable fundamental screens across all UK stocks nightly,
**So that** stocks meeting user-defined value/growth/quality criteria are identified.

**Acceptance Criteria:**

**Given** fundamental data is available from configured provider (default: EODHD)
**When** the Fundamental Screener Agent runs (configurable schedule, default: 2:15 AM)
**Then** it executes screens defined in configuration:

```yaml
# config/screens.yaml
screens:
  - name: value_screen
    enabled: true
    description: "Low P/E + High ROE + Low Debt"
    signal_score: 60
    criteria:
      - metric: pe_ratio
        operator: "<"
        value: 15
        weight: 1.0
      - metric: roe
        operator: ">"
        value: 0.15
        weight: 1.0
      - metric: debt_to_equity
        operator: "<"
        value: 0.5
        weight: 0.8
      - metric: market_cap_gbp
        operator: ">"
        value: 500000000  # £500M
        weight: 0.5

  - name: growth_screen
    enabled: true
    description: "High Revenue + EPS Growth"
    signal_score: 65
    criteria:
      - metric: revenue_growth_yoy
        operator: ">"
        value: 0.15
      - metric: eps_growth_yoy
        operator: ">"
        value: 0.20
      - metric: market_cap_gbp
        operator: ">"
        value: 250000000

  - name: naked_trader_checklist
    enabled: true
    description: "Robbie Burns Naked Trader Checklist"
    signal_score: 70
    criteria:
      - metric: net_income_3yr_positive
        operator: "=="
        value: true
      - metric: revenue_growth_3yr
        operator: ">"
        value: 0.0
      - metric: debt_to_equity
        operator: "<"
        value: 0.3
      - metric: pe_ratio_vs_sector
        operator: "<"
        value: 1.0  # Below sector median

  - name: quality_moat
    enabled: true
    description: "High Quality Business with Moat"
    signal_score: 75
    criteria:
      - metric: roe_3yr_avg
        operator: ">"
        value: 0.20
      - metric: gross_margin
        operator: ">"
        value: 0.40
      - metric: operating_margin
        operator: ">"
        value: 0.15
      - metric: free_cash_flow
        operator: ">"
        value: 0

  # User can add custom screens here without code changes
  # - name: my_custom_screen
  #   criteria: [...]
```

**And** Screen execution:
- Load all screen definitions from config/screens.yaml
- For each enabled screen, evaluate all stocks against criteria
- Support operators: `<`, `>`, `<=`, `>=`, `==`, `!=`, `in`, `not_in`
- Support calculated metrics (e.g., `roe_3yr_avg` = average of last 3 years ROE)
- Support derived metrics (e.g., `pe_ratio_vs_sector` = stock PE / sector median PE)

**And** Each stock passing a screen generates `FUNDAMENTAL_MATCH` signal with:
- signal_type: "FUNDAMENTAL_MATCH"
- score: From screen config (60, 65, 70, 75, or user-defined)
- metadata: screen_name, metric_values, percentile_ranks, pass/fail per criterion

**And** Stocks can pass multiple screens (generates multiple signals)
**And** Screen results are cached for configurable duration (default: 24 hours)
**And** Agent runs in < 10 minutes for 600 stocks
**And** Missing metrics handled gracefully (stock fails that criterion, doesn't crash)

**Prerequisites:** Story 1.4 (EODHD API Integration), Story 2.1 (Company Database)

**Technical Notes:**
- **Data-Driven:** All screens defined in YAML - user can add new screens without code changes
- **Metric Extensibility:**
  - Fetch ALL available metrics from data provider (don't hardcode which metrics exist)
  - Store in flexible JSON/JSONB structure
  - Screen config references ANY metric - if it exists in data, it can be screened
- **Calculated Metrics:** Support formulas like `roic_3yr_avg`, `fcf_yield`, `price_to_book`
- Fundamental data source: Configurable (EODHD for MVP, swappable to Alpha Vantage, FMP)
- Batch fetch: Request 50 stocks per API call (reduce latency)
- Pandas DataFrame for efficient vectorized filtering
- Store screen results in `signal_metadata` JSON field
- **No LLM needed:** Pure numerical filtering (cost = $0)
- **Phase 2 Enhancement:**
  - UI to create/edit screens
  - Backtest screen performance
  - Screen optimization (which screens find best stocks?)

---

### Story 2.4: Insider Trading Agent - Director Dealings

**As a** discovery agent,
**I want** to detect significant LSE director dealings (insider buying),
**So that** stocks with insider conviction are surfaced.

**Acceptance Criteria:**

**Given** LSE director dealings data is available from configured source
**When** the Insider Trading Agent runs (configurable schedule, default: 2:30 AM)
**Then** it fetches director dealings based on configuration:

```yaml
# config/discovery_agents.yaml
insider_trading:
  enabled: true
  schedule: "30 2 * * *"  # 2:30 AM daily
  data_source: companies_house  # Or: cityfalcon, manual_file_drop
  lookback_days: 7  # Fetch last 7 days of transactions
  cluster_window_days: 30  # Group transactions within 30 days

  # Significance thresholds (user configurable)
  significance_rules:
    single_director:
      min_amount_gbp: 50000
      min_percent_market_cap: 0.001  # 0.1%
      base_score: 80

    multiple_directors:
      min_directors: 2
      cluster_window_days: 30
      base_score: 90
      multiplier_per_additional_director: 1.05

    executive_purchase:  # CEO, CFO, Chairman
      min_amount_gbp: 25000
      base_score: 85
      role_multipliers:
        ceo: 1.2
        cfo: 1.1
        chairman: 1.15

    combined_signal:  # Multiple directors + executive
      base_score: 100

  # Transaction types to track
  transaction_types:
    purchase: true  # Generate signals
    sale: false  # Track but don't signal (tax planning)
    options_exercised: false
```

**And** Significance evaluation logic:
- Check each transaction against configurable rules
- Apply role multipliers for executives
- Apply market cap percentage check
- Cluster transactions within configurable window
- Calculate final score using config formulas

**And** For each significant purchase:
- Generate `INSIDER_CONVICTION` signal
- Score calculated from config (default: 80-100 range, user can adjust)
- Metadata: director_names, director_roles, total_amount_gbp, number_of_insiders, transaction_dates, percent_of_market_cap

**And** Signal scoring configuration:
```yaml
# config/signal_scoring.yaml
INSIDER_CONVICTION:
  base_score: 80  # User configurable
  decay_rate: slow
  decay_period_days: 90  # Insiders have long-term view
  adjustments:
    large_purchase_100k_plus: 1.0  # No additional boost
    multiple_directors_2_plus: 1.125  # 90 points
    ceo_involved: 1.0625  # 85 points
    combined_multiple_and_ceo: 1.25  # 100 points
```

**And** SALES are tracked but don't generate signals by default (configurable)
**And** Cluster transactions within configurable window (default: 30 days) as single signal
**And** Validate tickers against company database
**And** Agent runs in < 3 minutes

**Prerequisites:** Story 1.3 (Abstract Data Source Interface), Story 2.1 (Company Database)

**Technical Notes:**
- **Data Source Flexibility:**
  - **Phase 1 (MVP):** Companies House API (free, slower)
    - Endpoint: `/company/{company_number}/filing-history`
    - Filter for "SH01" forms (director dealings)
  - **Phase 2:** CityFALCON Insider Trading API (£25/month, faster, cleaner data)
  - **Alternative:** Manual file drop (CSV of insider transactions)
- **Configuration-Driven:** All thresholds (£50k, 0.1%, etc.) in config - user can tune
- Parse insider transactions, extract ticker, director role, amount
- Handle pence vs pounds conversion (LSE reports in pence)
- Insider signals decay slowly (90 days default, configurable)
- Store raw transaction details for agent analysis
- **Future:** User might want to track options grants, RSU vesting - config supports adding new transaction types

---

### Story 2.5: Volume & Price Action Agent - Technical Signals

**As a** discovery agent,
**I want** to detect unusual volume and price movements in UK stocks,
**So that** technical breakouts and momentum opportunities are surfaced.

**Acceptance Criteria:**

**Given** historical price and volume data is available
**When** the Volume & Price Action Agent runs (configurable schedule, default: 2:45 AM)
**Then** it analyzes all UK stocks for technical triggers defined in configuration:

```yaml
# config/discovery_agents.yaml
volume_price_action:
  enabled: true
  schedule: "45 2 * * *"
  lookback_days: 30  # Compare to 30-day average

  # Triggers (user configurable)
  triggers:
    volume_spike:
      enabled: true
      min_multiplier: 3.0  # 3x average volume
      signal_score: 60
      decay_days: 3  # Fast decay

    breakout_52week_high:
      enabled: true
      proximity_percent: 0.02  # Within 2% of 52-week high
      volume_confirmation: true  # Requires above-average volume
      signal_score: 70
      decay_days: 7

    price_surge:
      enabled: true
      min_gain_percent_1day: 0.10  # 10%+ gain in single day
      min_gain_percent_1week: 0.20  # 20%+ gain in week
      signal_score: 65
      decay_days: 5

    consolidation_breakout:
      enabled: false  # Advanced - Phase 2
      consolidation_days: 20
      breakout_multiplier: 1.5
      signal_score: 75

  # Filters
  filters:
    min_market_cap_gbp: 100000000  # £100M (avoid penny stocks)
    min_avg_daily_volume: 50000  # Minimum liquidity
```

**And** For each detected trigger:
- Generate `UNUSUAL_ACTIVITY` signal
- Score from config (60-75 range based on trigger type)
- Metadata: trigger_type, volume_ratio, price_change_percent, 52week_high_distance

**And** Volume calculations:
- Compare today's volume to configurable average (default: 30-day)
- Support different volume periods (10-day, 20-day, 50-day) via config

**And** Price analysis:
- Detect breakouts using configurable thresholds
- Support multiple timeframes (1-day, 1-week, 1-month)
- Calculate distance to 52-week high/low

**And** Filter out noise:
- Minimum market cap (avoid penny stocks manipulation)
- Minimum liquidity (avoid illiquid stocks with false signals)
- Thresholds configurable via filters section

**And** Agent runs in < 5 minutes for 600 stocks

**Prerequisites:** Story 1.4 (EODHD API - price/volume data), Story 2.1 (Company Database)

**Technical Notes:**
- **No LLM needed:** Pure price/volume math (cost = $0)
- Price/volume data from EODHD `/eod/{ticker}.LSE` endpoint
- Pandas for vectorized calculations (fast)
- Technical signals decay fast (3-7 days) - momentum is short-lived
- Store OHLCV data in database or cache for quick access
- **Phase 2 triggers:** RSI, MACD, Bollinger Bands, consolidation patterns
- User can add custom technical triggers via config

---

### Story 2.6: Signal Aggregation & Scoring Engine (CRITICAL)

**As a** discovery orchestrator,
**I want** to aggregate signals from all discovery agents and calculate convergence scores,
**So that** the highest-probability opportunities rise to the top for deep analysis.

**Acceptance Criteria:**

**Given** discovery agents have generated signals (NEWS_CATALYST, INSIDER_CONVICTION, FUNDAMENTAL_MATCH, UNUSUAL_ACTIVITY)
**When** the Signal Aggregation Engine runs (after all discovery agents complete, ~3:00 AM)
**Then** it aggregates signals by ticker and calculates total score:

```yaml
# config/signal_aggregation.yaml
aggregation:
  # Base scores by signal type (referenced from signal_scoring.yaml)
  signal_types:
    NEWS_CATALYST:
      base_score: 50
      decay_rate: medium
      decay_period_days: 14

    INSIDER_CONVICTION:
      base_score: 80
      decay_rate: slow
      decay_period_days: 90

    FUNDAMENTAL_MATCH:
      base_score: 60
      decay_rate: stable  # Fundamentals don't decay
      decay_period_days: null

    UNUSUAL_ACTIVITY:
      base_score: 60
      decay_rate: fast
      decay_period_days: 3

  # Macro/Sector multipliers (applied after base scoring)
  macro_sector_multipliers:
    macro_aligned: 1.5
    macro_neutral: 1.0
    macro_headwind: 0.5

    sector_favored: 1.3
    sector_neutral: 1.0
    sector_disfavored: 0.7

  # Convergence bonuses (multiple signals = higher conviction)
  convergence_bonuses:
    2_signals: 1.1   # 10% bonus
    3_signals: 1.25  # 25% bonus
    4_plus_signals: 1.4  # 40% bonus

  # Thresholds for routing decisions
  thresholds:
    monitor_only: 0      # 0-30 points
    research_queue: 31   # 31-60 points (Tier 3)
    deep_analysis: 61    # 61-90 points
    priority_analysis: 91  # 91+ points
```

**And** Aggregation algorithm:
1. **Collect all signals for each ticker** (from past N days, configurable)
2. **Apply time decay** to older signals (fast/medium/slow/stable rates)
3. **Sum base scores** for all active signals
4. **Apply macro multiplier** (from Macro Economist Agent output)
5. **Apply sector multiplier** (from Sector Rotation Agent output)
6. **Apply convergence bonus** (2+ signals = boosted confidence)
7. **Calculate final score** = (sum of decayed signals) × macro_mult × sector_mult × convergence_bonus

**And** Output ranking:
- Top 15 stocks above deep_analysis threshold (61+) → Route to Epic 3 (Analysis Agents)
- Stocks scoring 31-60 → Route to Research Queue (Story 2.9)
- Stocks scoring 0-30 → Monitor only (no action)

**And** Store aggregated scores in database:
```sql
CREATE TABLE aggregated_signals (
  ticker VARCHAR(10),
  date DATE,
  total_score DECIMAL,
  signal_count INT,
  signal_breakdown JSONB,  -- Which signals contributed
  macro_multiplier DECIMAL,
  sector_multiplier DECIMAL,
  convergence_bonus DECIMAL,
  routing_decision VARCHAR(20)  -- monitor, research_queue, deep_analysis, priority
);
```

**And** Deduplication logic:
- Same signal type from same source = keep most recent
- Different signal types = add all
- Expired signals (beyond decay period) = remove

**And** Execution time < 2 minutes for 600 stocks × avg 50 signals = 30,000 calculations

**Prerequisites:** All discovery agents (Stories 2.2-2.5), Story 2.7-2.8 (Macro/Sector context)

**Technical Notes:**
- **This is the CORE of the discovery system** - everything feeds into this
- Pandas DataFrame for vectorized calculations (fast)
- Signal decay formulas:
  - Fast: `score × (1 - days_old / decay_period)`
  - Medium: `score × exp(-days_old / decay_period)`
  - Slow: `score × (1 - days_old / (2 × decay_period))`
  - Stable: No decay
- Store calculation details for transparency (why did this stock score 85?)
- **Configuration-driven:** User can tune all thresholds, multipliers, decay rates
- **Future enhancement:** Machine learning to optimize scoring weights

---

### Story 2.7: Macro Economist Agent - UK Economic Context

**As a** discovery system,
**I want** weekly UK macroeconomic analysis to provide top-down context,
**So that** discovery signals are weighted by economic regime (expansion, recession, etc.).

**Acceptance Criteria:**

**Given** UK macroeconomic data is available
**When** the Macro Economist Agent runs (configurable schedule, default: Sunday 8 PM weekly)
**Then** it analyzes UK economic indicators:

**Data inputs:**
- GDP growth (quarterly, YoY)
- Inflation (CPI, RPI)
- Interest rates (Bank of England base rate)
- Unemployment rate
- PMI (Manufacturing, Services)
- Consumer confidence
- Housing market indicators
- FTSE 100 index trend

**And** Uses configured LLM (default: Claude Sonnet for deep reasoning) to:
- Classify current regime: expansion, late_cycle, early_recession, deep_recession, recovery, stagflation
- Identify key risks: inflation, recession, policy tightening, geopolitical
- Recommend sector positioning: which sectors to favor/avoid in this regime
- Predict regime changes: "Expansion likely to continue" vs "Recession risk rising"

```yaml
# config/analysis_agents.yaml
macro_economist:
  enabled: true
  schedule: "0 20 * * 0"  # Sunday 8 PM weekly
  llm_provider: anthropic
  llm_model: claude-3-5-sonnet-20241022  # Deep reasoning needed

  data_sources:
    - ons_uk  # Office for National Statistics
    - boe  # Bank of England
    - pmi_markit
    - trading_economics

  # Output structure
  output_schema:
    regime: enum  # expansion, recession, etc.
    confidence: float  # 0.0-1.0
    key_risks: list[str]
    sector_recommendations:
      favor: list[str]  # Healthcare, Utilities, etc.
      avoid: list[str]  # Mining, Housebuilders, etc.
    narrative: str  # 2-3 paragraph summary
```

**And** Generates `MACRO_REGIME_CHANGE` signal when regime shifts
**And** Output stored in `macro_context` table with weekly snapshots
**And** Signal Aggregation Engine (Story 2.6) applies macro multipliers:
- Aligned with macro regime: 1.5x
- Neutral: 1.0x
- Against macro regime: 0.5x

**And** Agent runs in < 5 minutes (LLM call is expensive but infrequent - weekly)

**Prerequisites:** Story 1.8 (Multi-Provider LLM), Story 2.1 (Company Database for sector mapping)

**Technical Notes:**
- **LLM:** Configured via agent_config - user can switch models
- **Default:** Claude Sonnet (best reasoning for macro analysis)
- **Cost:** ~£0.20-0.30 per run × 4 runs/month = £1/month
- Prompt includes: all economic indicators + historical context + current positioning
- Output format: Structured JSON for easy parsing
- **Data sources:** Free UK economic data (ONS, BoE publish free APIs)
- **Phase 2:** Backtest macro regime classifications against historical returns
- User can customize regime definitions and sector mappings via config

---

### Story 2.8: Sector Rotation Agent - Identify Favored Sectors

**As a** discovery system,
**I want** weekly sector performance analysis,
**So that** stocks in favored sectors get boosted scores and disfavored sectors get penalized.

**Acceptance Criteria:**

**Given** sector performance data is available
**When** the Sector Rotation Agent runs (configurable schedule, default: Sunday 9 PM weekly)
**Then** it analyzes UK sector performance:

**Analysis inputs:**
- Relative sector performance (vs FTSE 100): 1-month, 3-month, 6-month
- Sector fund flows (money moving in/out)
- Sector earnings trends
- Macro context (from Macro Economist Agent Story 2.7)
- Sector valuations (P/E relative to historical averages)

**And** Uses configured LLM to identify:
- **Top 3 sectors to overweight** (favored): Strong performance + positive outlook
- **Bottom 3 sectors to underweight** (disfavored): Weak performance + negative outlook
- Rationale for each (economic sensitivity, valuation, momentum)

```yaml
# config/analysis_agents.yaml
sector_rotation:
  enabled: true
  schedule: "0 21 * * 0"  # Sunday 9 PM weekly (after macro_economist)
  llm_provider: google
  llm_model: gemini-1.5-pro  # Good for comparative analysis

  sectors:  # GICS Level 1
    - Financials
    - Healthcare
    - Industrials
    - Consumer Discretionary
    - Consumer Staples
    - Energy
    - Materials
    - Real Estate
    - Technology
    - Communication Services
    - Utilities

  output_schema:
    favored_sectors: list[str]  # Top 3
    disfavored_sectors: list[str]  # Bottom 3
    sector_rankings: dict  # All 11 sectors ranked
    narrative: str
```

**And** Generates `SECTOR_PREFERENCES_UPDATE` signal weekly
**And** Output stored in `sector_context` table
**And** Signal Aggregation Engine (Story 2.6) applies sector multipliers:
- Favored sectors: 1.3x
- Neutral: 1.0x
- Disfavored sectors: 0.7x

**And** Agent runs in < 5 minutes

**Prerequisites:** Story 1.8 (Multi-Provider LLM), Story 2.1 (Company Database with sector mapping), Story 2.7 (Macro context)

**Technical Notes:**
- **LLM:** Configured via agent_config
- **Default:** Gemini Pro (cost-effective for comparative analysis)
- **Cost:** ~£0.10-0.15 per run × 4 runs/month = £0.50/month
- Sector performance data: EODHD sector indices or calculate from stock universe
- Integrates with Macro Economist output (e.g., recession → favor defensives)
- **Phase 2:** Machine learning to predict sector rotation
- User can customize sector definitions and multipliers via config

---

### Story 2.9: Research Queue Management (Tier 3 Tracking)

**As a** portfolio manager,
**I want** a research queue for stocks scoring 31-60 points,
**So that** medium-interest stocks are tracked and re-scored daily without expensive deep analysis.

**Acceptance Criteria:**

**Given** Signal Aggregation Engine (Story 2.6) has identified stocks scoring 31-60 points
**When** the Research Queue Manager runs (after aggregation, ~3:15 AM)
**Then** it manages the research queue:

**Add to Queue:**
- Stocks crossing 31-point threshold → Add with current score, signals, timestamp
- Store: ticker, score, signal_breakdown, added_date, last_updated

**Daily Re-Scoring:**
- Re-run Signal Aggregation for all queued stocks
- Update scores based on new signals + decay
- Detect score changes:
  - **Promoted (61+):** Move to Deep Analysis queue
  - **Demoted (< 31):** Remove from queue (interest faded)
  - **Stable (31-60):** Keep in queue

**Queue Management:**
```yaml
# config/research_queue.yaml
research_queue:
  max_queue_size: 100  # Configurable limit
  max_age_days: 60  # Auto-remove stocks older than 60 days
  re_score_frequency: daily

  promotion_threshold: 61  # Move to deep analysis
  demotion_threshold: 30   # Remove from queue
```

**And** Database table:
```sql
CREATE TABLE research_queue (
  ticker VARCHAR(10),
  score DECIMAL,
  signal_breakdown JSONB,
  added_date DATE,
  last_updated TIMESTAMP,
  days_in_queue INT,
  status VARCHAR(20)  -- queued, promoted, demoted, expired
);
```

**And** Notifications:
- Daily summary: "5 stocks promoted to deep analysis, 3 removed, 42 still in queue"
- Included in morning report (Epic 5)

**And** Queue limits enforced:
- If queue exceeds max_size (default: 100), remove lowest-scoring stocks
- If stock exceeds max_age_days (default: 60), auto-remove

**And** Execution time < 1 minute

**Prerequisites:** Story 2.6 (Signal Aggregation Engine), Story 1.2 (Database Schema)

**Technical Notes:**
- **Purpose:** Avoid expensive LLM analysis on every signal - only deep-dive when conviction builds
- Research queue is "warm leads" - tracking without committing resources
- Re-scoring is cheap (no LLM, just math from Story 2.6)
- **Phase 2:** User can manually add stocks to research queue via UI
- **Phase 2:** Set custom alerts ("Notify me if stock X enters research queue")

---

### Story 2.10: Signal Decay & Time-Based Weighting

**As a** signal aggregation system,
**I want** older signals to decay over time at configurable rates,
**So that** scoring reflects signal freshness and relevance.

**Acceptance Criteria:**

**Given** signals have been generated with timestamps
**When** Signal Aggregation Engine (Story 2.6) calculates scores
**Then** it applies time decay to each signal based on configuration:

```yaml
# config/signal_decay.yaml
decay_algorithms:
  # Fast decay - momentum signals lose relevance quickly
  fast:
    formula: linear  # Or: exponential, step
    half_life_days: 3
    zero_after_days: 7
    example_signals: [UNUSUAL_ACTIVITY, EARNINGS_SURPRISE]

  # Medium decay - news relevance fades moderately
  medium:
    formula: exponential
    half_life_days: 7
    zero_after_days: 30
    example_signals: [NEWS_CATALYST, ANALYST_SHIFT]

  # Slow decay - insider conviction has long horizon
  slow:
    formula: linear
    half_life_days: 30
    zero_after_days: 90
    example_signals: [INSIDER_CONVICTION]

  # Stable - fundamentals don't decay (until data refresh)
  stable:
    formula: none
    example_signals: [FUNDAMENTAL_MATCH]

# Decay formulas
formulas:
  linear:
    # score × (1 - days_old / zero_after_days)
    description: "Linear decline to zero"

  exponential:
    # score × exp(-days_old / half_life_days)
    description: "Exponential decay, slower at first"

  step:
    # Full score until cutoff, then zero
    description: "No decay until expiry"
```

**And** Decay calculation per signal:
- Determine days_old = current_date - signal_date
- Lookup decay_rate for signal_type
- Apply formula with configured parameters
- Return decayed_score

**And** Example calculations:
```
Signal: INSIDER_CONVICTION (base_score = 80, slow decay, 90 days)
- Day 0: 80 points (fresh)
- Day 30: 53 points (1/3 through decay period)
- Day 60: 27 points (2/3 through)
- Day 90: 0 points (expired)

Signal: UNUSUAL_ACTIVITY (base_score = 60, fast decay, 7 days)
- Day 0: 60 points
- Day 3: 34 points (half-life)
- Day 7: 0 points (expired)
```

**And** Expired signals (beyond zero_after_days):
- Removed from aggregation calculations
- Archived in database for historical analysis
- Not deleted (useful for backtesting)

**And** Database tracking:
```sql
ALTER TABLE signals ADD COLUMN:
  created_at TIMESTAMP,
  decay_rate VARCHAR(10),  -- fast, medium, slow, stable
  expired_at TIMESTAMP,  -- Calculated: created_at + zero_after_days
  current_score DECIMAL  -- Recalculated daily with decay
```

**And** Execution: Decay calculations done in-memory during aggregation (fast)

**Prerequisites:** Story 2.6 (Signal Aggregation Engine)

**Technical Notes:**
- **Configuration-driven:** User can tune decay rates, formulas, half-lives
- Default decay rates set per signal type, but user can override
- Decay is continuous (recalculated daily), not stepped
- **Phase 2:** Optimize decay rates via backtesting (which decay curves maximize returns?)
- Mathematical formulas:
  - Linear: `score × max(0, 1 - days_old / zero_after_days)`
  - Exponential: `score × exp(-days_old × ln(2) / half_life_days)`
  - Step: `score if days_old < zero_after_days else 0`

---

### Story 2.11: Configuration Management System

**As a** developer and user,
**I want** a centralized configuration system with validation and documentation,
**So that** all scoring rules, thresholds, and agent parameters can be easily changed without code modifications.

**Acceptance Criteria:**

**Given** the system uses extensive configuration files
**When** the Configuration Manager initializes on startup
**Then** it loads and validates all configuration files:

**Configuration file structure:**
```
/config
  ├── agents/
  │   ├── discovery_agents.yaml      # News, Insider, Screener, Volume configs
  │   ├── analysis_agents.yaml       # Macro, Sector, Value, Growth, etc.
  │   └── decision_agents.yaml       # Risk Manager, Portfolio Manager
  │
  ├── scoring/
  │   ├── signal_scoring.yaml        # Base scores, multipliers per signal type
  │   ├── signal_decay.yaml          # Decay rates and formulas
  │   └── aggregation.yaml           # Convergence bonuses, thresholds
  │
  ├── data/
  │   ├── data_sources.yaml          # EODHD, CityFALCON, etc.
  │   └── screens.yaml               # Fundamental screen definitions
  │
  ├── scheduling/
  │   └── workflows.yaml             # Cron schedules for all agents
  │
  └── system/
      ├── database.yaml              # Connection settings
      ├── llm_providers.yaml         # API keys, rate limits
      └── limits.yaml                # Max queue sizes, timeouts, etc.
```

**And** Agent feature flags for easy enable/disable during development:

**Agent Configuration with Feature Flags:**
```yaml
# config/agents/discovery_agents.yaml
agents:
  discovery:
    news_scanner:
      enabled: true  # Set to false to disable during testing
      llm_provider: openai
      llm_model: gpt-4o-mini
      schedule: "0 2 * * *"
      # [other config...]

    insider_trading:
      enabled: true  # Disable if Companies House API down
      data_source: companies_house
      schedule: "30 2 * * *"
      # [other config...]

    fundamental_screener:
      enabled: true
      schedule: "15 2 * * *"
      # [other config...]

    volume_price_action:
      enabled: false  # Example: Disabled during testing
      schedule: "45 2 * * *"
      # [other config...]

# config/agents/analysis_agents.yaml
agents:
  analysis:
    value_investor:
      enabled: true
      llm_provider: anthropic
      llm_model: claude-3-5-sonnet-20241022
      weight: 1.0  # Influence on final decision

    contrarian:
      enabled: false  # Example: Too expensive in dev, disable temporarily
      llm_provider: anthropic
      llm_model: claude-3-5-sonnet-20241022
      weight: 0.8

    growth_investor:
      enabled: true
      llm_provider: openai
      llm_model: gpt-4o
      weight: 1.0

    naked_trader:
      enabled: true  # UK-specific agent
      llm_provider: google
      llm_model: gemini-1.5-pro
      weight: 1.2  # Higher weight for UK specialist

    macro_economist:
      enabled: true
      schedule: "0 20 * * 0"  # Weekly
      llm_provider: anthropic
      llm_model: claude-3-5-sonnet-20241022

    sector_rotation:
      enabled: true
      schedule: "0 21 * * 0"  # Weekly
      llm_provider: google
      llm_model: gemini-1.5-pro
```

**Workflow Behavior with Disabled Agents:**
- Disabled agents: Skipped during workflow execution
- Workflow logs: "news_scanner: SKIPPED (disabled in config)"
- Signal aggregation: Works with partial agent set
- Morning report: Notes which agents were active

**Use Cases for Feature Flags:**
1. **Development Testing:** Disable expensive agents (Contrarian using Claude Opus)
2. **Debugging:** Isolate single agent to test changes
3. **Cost Control:** Disable non-critical agents to stay under budget
4. **Gradual Rollout:** Enable new agents one at a time
5. **A/B Testing:** Run with/without specific agents, compare performance
6. **API Outages:** Disable agent if data source unavailable

**Configuration Validation:**
- Warn if ALL discovery agents disabled (no signals generated)
- Warn if Portfolio Manager disabled (no decisions made)
- Allow partial agent sets (system degrades gracefully)

**Example Development Workflow:**
```bash
# Day 1: Test just news scanner
# Set: news_scanner.enabled=true, all others=false
python main.py --dev

# Day 2: Add fundamental screener
# Set: news_scanner.enabled=true, fundamental_screener.enabled=true
python main.py --dev

# Day 3: Full discovery layer
# Set: all discovery agents enabled=true
python main.py --dev
```

**And** Configuration validation on load:
- Schema validation (YAML structure matches expected format)
- Type checking (scores are numbers, dates are dates)
- Range validation (scores 0-100, probabilities 0-1)
- Dependency checks (referenced agents exist, LLM models valid)
- Circular dependency detection

**And** Validation errors:
- Clear error messages: "signal_scoring.yaml line 12: base_score must be 0-100, got 150"
- Fail fast: Don't start system with invalid config
- Suggest fixes: "Did you mean 'fast' instead of 'fats'?"

**And** Configuration documentation:
```yaml
# Example: config/scoring/signal_scoring.yaml
# DOCUMENTATION: Signal Scoring Configuration
# Purpose: Define base scores and modifiers for all signal types
# Updated: 2025-11-22
# Owner: System Architect

NEWS_CATALYST:
  base_score: 50  # Range: 0-100. Default: 50
  # Description: Base score for news-driven catalysts
  # Higher = more weight in signal aggregation
  # Recommendation: 40-60 for medium-strength signals

  decay_rate: medium  # Options: fast, medium, slow, stable
  decay_period_days: 14  # Range: 1-365

  catalyst_modifiers:
    major_contract: 1.6  # Multiplier: base_score × 1.6 = 80 points
    # [Additional modifiers...]
```

**And** Configuration hot-reload (Phase 2):
- Detect config file changes
- Reload without restart
- Validate before applying
- Rollback on errors

**And** Configuration versioning:
```sql
CREATE TABLE config_versions (
  id SERIAL,
  config_file VARCHAR(100),
  version INT,
  content TEXT,  -- Full YAML content
  changed_by VARCHAR(50),
  changed_at TIMESTAMP,
  change_reason TEXT
);
```

**And** API for config queries (Phase 2):
```python
# Code can query config dynamically
config = ConfigManager()
news_score = config.get("signal_scoring.NEWS_CATALYST.base_score")
decay_rate = config.get("signal_decay.fast.half_life_days")
```

**Prerequisites:** Story 1.1 (Project Setup)

**Technical Notes:**
- **Libraries:** PyYAML for parsing, Pydantic for validation
- **Default configs:** Shipped with sensible defaults (system works out-of-box)
- **User overrides:** User can override any default in local config files
- **Environment variables:** Support `${EODHD_API_KEY}` substitution
- **Documentation:** Inline comments in YAML + separate docs/configuration.md
- **Phase 2:** Web UI for config editing with real-time validation
- **Security:** Sensitive configs (API keys) in environment vars, not committed to git
- **.gitignore:** Local config overrides, API keys
- **Config testing:** Unit tests validate all example configs load successfully

---

### Story 2.12: Discovery Batch Orchestration (LangGraph Workflow)

**As a** system orchestrator,
**I want** a LangGraph workflow that runs all discovery agents in parallel overnight,
**So that** the discovery phase completes reliably in the 1am-3am window.

**Acceptance Criteria:**

**Given** all discovery agents are configured and enabled
**When** the Discovery Batch Orchestrator triggers (configurable, default: 1:00 AM)
**Then** it supports multiple execution modes for different use cases:

**EXECUTION MODES:**

**1. Production Mode (Default):**
```yaml
# Scheduled overnight batch
mode: production
schedule: "0 1 * * *"  # 1 AM daily
scope: full  # All 600 FTSE stocks
agents: all_enabled  # All agents with enabled=true run
llm_mode: real  # Real LLM API calls
```

**Characteristics:**
- Runs automatically at 1 AM GMT daily
- Analyzes full stock universe (600 FTSE stocks)
- All enabled discovery agents execute in parallel
- Uses real LLM providers (OpenAI, Anthropic, Google)
- Generates morning report by 7 AM
- Cost: ~£2-5/day for discovery phase

**2. Dev Mode (--dev flag):**
```bash
python main.py --dev
# OR
python main.py --mode=dev --scope=ftse100 --mock-llm
```

```yaml
# Fast iteration for development
mode: dev
schedule: on_demand  # Run immediately when triggered
scope: limited  # FTSE 100 only (100 stocks)
agents: configurable_subset  # Test specific agents
llm_mode: cheap_models  # Use GPT-4o-mini, Gemini Flash for all
timeout: 10_minutes  # Fail fast if hanging
```

**Characteristics:**
- Runs immediately (on-demand, not scheduled)
- Limited scope: FTSE 100 only (100 stocks vs 600)
- Configurable agent subset: Test 2-3 agents at a time
- Uses cheap LLM models for all agents (override config)
- Target runtime: <10 minutes (vs 2 hours production)
- Cost: ~£0.10-0.30 per run (vs £2-5 production)
- Output: Dev console + logs (not morning report)

**Configuration:**
```yaml
# config/workflows.yaml
discovery_batch:
  modes:
    dev:
      scope: ftse_100  # 100 stocks
      timeout_minutes: 10
      llm_override:
        all_agents: gpt-4o-mini  # Cheap model for all
      agents_subset:
        - news_scanner  # Only test these agents
        - fundamental_screener
      parallel_limit: 5  # Don't overwhelm APIs
```

**Usage:**
```bash
# Quick dev test: News scanner + Fundamentals only, 100 stocks
python main.py --dev

# Custom dev run: Specific agents
python main.py --dev --agents=news_scanner,insider_trading

# Dev with specific scope
python main.py --dev --scope=ftse250 --limit=50  # First 50 FTSE 250
```

**3. Dry Run Mode (--dry-run flag):**
```bash
python main.py --dry-run
# OR
python main.py --mode=dry-run --mock-llm
```

```yaml
# Test workflow logic without LLM calls
mode: dry_run
scope: full  # 600 stocks (or configurable)
agents: all_enabled
llm_mode: mock  # Mock LLM responses from fixtures
data_mode: cached  # Use cached data, don't fetch new
```

**Characteristics:**
- Tests full workflow logic without API costs
- Uses mock LLM responses (fixtures from tests/fixtures/)
- Uses cached data (no EODHD API calls)
- Target runtime: <2 minutes for 600 stocks
- Cost: £0 (zero LLM costs, zero data costs)
- Output: Signal counts, convergence scores, routing decisions

**Use Cases:**
- Test signal convergence logic changes
- Test decay calculations
- Test workflow orchestration (parallel execution, error handling)
- CI/CD integration tests

**4. On-Demand Mode (Manual Trigger):**
```bash
# Full production run, triggered manually
python main.py --run-now

# On-demand for specific tickers
python main.py --tickers=VOD.L,BP.L,TSCO.L

# On-demand for specific sector
python main.py --sector=Healthcare --scope=all
```

```yaml
# User-triggered production run
mode: on_demand
schedule: immediate
scope: configurable  # Full, sector, or ticker list
agents: all_enabled
llm_mode: real
```

**Characteristics:**
- Runs immediately (not scheduled)
- Full production mode (real LLMs, real data)
- Configurable scope: All stocks, specific sector, or ticker list
- Generates full report (same as overnight batch)
- Cost: Same as production (£2-5 for full run)

**Use Cases:**
- Breaking news: Re-run discovery after major market event
- User curiosity: "What does the system think about Healthcare sector today?"
- Manual override: "Analyze these 5 tickers right now"

**WORKFLOW EXECUTION (All Modes):**

**Then** the workflow executes using LangGraph:

**Workflow Graph:**
```
START (1:00 AM)
  ↓
[Initialize] - Load configs, check system health
  ↓
[Parallel Discovery Phase] (1:00-2:45 AM)
  ├─→ Company Database Sync (Story 2.1) - Weekly
  ├─→ News Scanner Agent (Story 2.2)
  ├─→ Fundamental Screener Agent (Story 2.3)
  ├─→ Insider Trading Agent (Story 2.4)
  └─→ Volume & Price Action Agent (Story 2.5)
  ↓ (All parallel agents complete)
[Signal Aggregation & Scoring] (Story 2.6) (2:45-3:00 AM)
  ↓
[Research Queue Update] (Story 2.9) (3:00-3:05 AM)
  ↓
[Context Agents - Weekly Only] (3:05-3:15 AM)
  ├─→ Macro Economist Agent (Story 2.7) - Sundays only
  └─→ Sector Rotation Agent (Story 2.8) - Sundays only
  ↓
[Export Top 15 for Analysis] → Trigger Epic 3 (Analysis Phase)
  ↓
END (3:15 AM latest)
```

**And** Workflow configuration:
```yaml
# config/workflows.yaml
discovery_batch:
  enabled: true
  schedule: "0 1 * * *"  # 1 AM daily
  timeout_minutes: 135  # 2h 15min (fail if exceeds)
  retry_policy:
    max_retries: 1
    retry_failed_agents: true
    continue_on_agent_failure: true  # Don't fail entire workflow if one agent fails

  stages:
    - name: initialization
      timeout_minutes: 5

    - name: discovery_parallel
      timeout_minutes: 105  # 1h 45min for all agents
      agents:
        - company_database_sync  # Runs weekly only
        - news_scanner
        - fundamental_screener
        - insider_trading
        - volume_price_action
      parallelism: all  # Run all simultaneously

    - name: aggregation
      timeout_minutes: 15
      depends_on: [discovery_parallel]

    - name: research_queue
      timeout_minutes: 5
      depends_on: [aggregation]

    - name: context_agents
      timeout_minutes: 10
      depends_on: [aggregation]
      schedule_override: "0 20 * * 0"  # Weekly on Sunday
      agents:
        - macro_economist
        - sector_rotation

    - name: export_results
      timeout_minutes: 5
      depends_on: [aggregation, research_queue]
```

**And** State management:
```python
class DiscoveryState:
    workflow_id: str
    start_time: datetime
    current_stage: str
    agent_results: Dict[str, Any]
    signal_count: int
    top_stocks: List[Tuple[str, float]]  # (ticker, score)
    errors: List[str]
    status: str  # running, completed, failed
```

**And** Error handling:
- Agent failure → Log error, continue with other agents
- Timeout → Fail agent, continue workflow
- Critical failure (database down) → Abort workflow, alert user
- Partial success → Complete workflow, flag missing agent data

**And** Monitoring & Logging:
- Log start/end time of each agent
- Track execution duration
- Count signals generated per agent
- Store workflow state in database:
```sql
CREATE TABLE workflow_runs (
  workflow_id UUID,
  workflow_name VARCHAR(50),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  status VARCHAR(20),
  agent_results JSONB,
  error_log TEXT
);
```

**And** Graceful degradation:
- If News Scanner fails → Continue with other agents, note "News unavailable"
- If EODHD API down → Use cached data, flag staleness
- If LLM rate-limited → Queue for retry, don't block workflow

**And** Success metrics:
- Workflow completes in < 2 hours for 600 stocks
- 95%+ agent success rate
- Logs accessible for debugging

**Prerequisites:** Story 1.7 (LangGraph Foundation), All Epic 2 stories (2.1-2.11)

**Technical Notes:**
- **LangGraph:** State graph for workflow orchestration
- **Parallel execution:** asyncio for concurrent agent execution
- **State persistence:** PostgreSQL stores workflow state (can resume if crashes)
- **Scheduling:** APScheduler or cron for daily 1 AM trigger
- **Monitoring:** Prometheus metrics, Grafana dashboards (Phase 2)
- **Alerting:** Email/Slack if workflow fails (Phase 2)
- **Dry-run mode:** Test workflow without generating signals (useful for debugging)
- **Manual trigger:** API endpoint to run discovery on-demand (FR-10.1)
- **Cost tracking:** Sum LLM costs from all agents, log total daily cost

---


