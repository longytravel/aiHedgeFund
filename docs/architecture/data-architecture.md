# Data Architecture

### Database Schema (PostgreSQL 18.1)

**Core Tables:**

```sql
-- Stocks master table
CREATE TABLE stocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) UNIQUE NOT NULL,  -- e.g., 'VOD.L'
    name VARCHAR(255) NOT NULL,           -- e.g., 'Vodafone Group PLC'
    sector VARCHAR(100),                  -- e.g., 'Telecommunications'
    market_cap DECIMAL(15, 2),            -- GBP millions
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_stocks_ticker ON stocks(ticker);
CREATE INDEX idx_stocks_sector ON stocks(sector);

-- Signals from discovery agents
CREATE TABLE signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL,            -- 'NEW_CATALYST', 'INSIDER_CONVICTION', etc.
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    strength INTEGER NOT NULL,            -- 0-100 base score
    data JSONB NOT NULL,                  -- Agent-specific details
    agent_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_signals_stock_ticker ON signals(stock_ticker);
CREATE INDEX idx_signals_timestamp ON signals(timestamp DESC);
CREATE INDEX idx_signals_agent_id ON signals(agent_id);

-- Analysis results from analysis agents
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    agent_id VARCHAR(50) NOT NULL,        -- 'value_investor', 'contrarian', etc.
    recommendation VARCHAR(20) NOT NULL,  -- 'BUY', 'SELL', 'HOLD', 'WATCHLIST'
    score INTEGER NOT NULL,               -- 0-100 conviction
    confidence VARCHAR(10) NOT NULL,      -- 'LOW', 'MEDIUM', 'HIGH'
    reasoning TEXT NOT NULL,
    key_metrics JSONB,
    risks JSONB,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_analysis_stock_ticker ON analysis_results(stock_ticker);
CREATE INDEX idx_analysis_timestamp ON analysis_results(timestamp DESC);

-- Tier 1: Active Portfolio
CREATE TABLE portfolio_positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    entry_price DECIMAL(10, 2) NOT NULL,  -- GBP
    entry_date DATE NOT NULL,
    stop_loss DECIMAL(10, 2),             -- GBP
    target_price DECIMAL(10, 2),          -- GBP
    current_price DECIMAL(10, 2),         -- Updated daily
    unrealized_pnl DECIMAL(12, 2),        -- Updated daily
    status VARCHAR(20) DEFAULT 'ACTIVE',  -- 'ACTIVE', 'CLOSED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_portfolio_status ON portfolio_positions(status);

-- Tier 2: Active Watchlist
CREATE TABLE watchlist_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    reason TEXT NOT NULL,                 -- Why added to watchlist
    triggers JSONB NOT NULL,              -- Array of trigger conditions
    added_date DATE NOT NULL,
    last_validated TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'ACTIVE',  -- 'ACTIVE', 'TRIGGERED', 'REMOVED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_watchlist_status ON watchlist_entries(status);

-- Tier 3: Research Queue
CREATE TABLE research_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    convergence_score INTEGER NOT NULL,   -- 31-60 range (below analysis threshold)
    signals JSONB NOT NULL,               -- Array of contributing signals
    added_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING', -- 'PENDING', 'PROMOTED', 'DISCARDED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_research_score ON research_queue(convergence_score DESC);

-- Trades (execution log)
CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_id UUID REFERENCES stocks(id),
    stock_ticker VARCHAR(10) NOT NULL,
    action VARCHAR(10) NOT NULL,          -- 'BUY', 'SELL'
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,        -- GBP
    commission DECIMAL(8, 2),             -- GBP
    trade_date TIMESTAMP WITH TIME ZONE NOT NULL,
    realized_pnl DECIMAL(12, 2),          -- For SELL trades
    notes TEXT,                           -- User notes, lessons learned
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_trades_ticker ON trades(stock_ticker);
CREATE INDEX idx_trades_date ON trades(trade_date DESC);

-- Audit log (full traceability)
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,      -- 'ANALYSIS_RUN', 'SIGNAL_PUBLISHED', 'TRADE_EXECUTED'
    entity_id UUID,                       -- ID of related entity (stock, trade, etc.)
    entity_type VARCHAR(50),              -- 'STOCK', 'TRADE', 'SIGNAL'
    details JSONB NOT NULL,               -- Event-specific details
    user_id UUID,                         -- If user-initiated (future multi-user)
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp DESC);
CREATE INDEX idx_audit_event_type ON audit_log(event_type);
```

### Data Flow

**Overnight Batch Processing (1am-7am):**

```
1:00 AM  → Data Collection
            ├─ EODHD: Pull fundamentals, historical, earnings
            ├─ CityFALCON: Pull RNS feeds, insider dealings
            ├─ IBKR: Update watchlist prices
            └─ Store in signals table

2:00 AM  → Discovery Layer (7 agents run in parallel)
            ├─ News Scanner → NEW_CATALYST signals
            ├─ Insider Trading → INSIDER_CONVICTION signals
            ├─ Volume/Price → UNUSUAL_ACTIVITY signals
            ├─ Fundamental Screener → FUNDAMENTAL_MATCH signals
            └─ Signals published to signal_bus

3:00 AM  → Macro/Sector Context (2 agents, weekly)
            ├─ Macro Economist → MACRO_REGIME_CHANGE signal
            ├─ Sector Rotation → SECTOR_PREFERENCES_UPDATE signal
            └─ Apply sector multipliers to discovery signals

3:30 AM  → Signal Aggregation & Convergence Scoring
            ├─ Group signals by stock ticker
            ├─ Calculate convergence scores (base + multipliers)
            ├─ Route stocks:
            │   ├─ 0-30 points → Monitor (log only)
            │   ├─ 31-60 points → Research Queue (Tier 3)
            │   └─ 61+ points → Deep Analysis (trigger analysis agents)

4:00 AM  → Deep Analysis (8 agents run in parallel, only on 61+ stocks)
            ├─ Value Investor → VALUE_ASSESSMENT
            ├─ Growth Investor → GROWTH_ASSESSMENT
            ├─ Contrarian → CONTRARIAN_OPPORTUNITY/WARNING
            ├─ Quality/Moat → QUALITY_ASSESSMENT
            ├─ Technical Analyst → TECHNICAL_CONFIRMATION/WARNING
            ├─ Catalyst Detective → CATALYST_IDENTIFIED
            ├─ Sentiment Analyst → SENTIMENT_ASSESSMENT
            └─ Results stored in analysis_results table

5:00 AM  → Adversarial Challenge Protocol
            ├─ Risk Manager challenges bullish theses
            ├─ Contrarian Agent provides bear case
            ├─ Portfolio Manager synthesizes all inputs
            └─ Final BUY/SELL/HOLD/WATCHLIST decisions

5:30 AM  → Watchlist Processing
            ├─ Check all watchlist triggers (price, events, macro)
            ├─ Re-validate triggered stocks (run full analysis)
            └─ Update watchlist_entries status

6:00 AM  → Portfolio Review
            ├─ Check stop-losses (current_price vs stop_loss)
            ├─ Check target prices (current_price vs target_price)
            ├─ Re-analyze holdings for fundamental deterioration
            └─ Generate SELL recommendations if needed

6:30 AM  → Report Generation
            ├─ Compile BUY recommendations (from deep analysis)
            ├─ Compile watchlist alerts (triggered + re-validated)
            ├─ Compile portfolio updates (SELL signals, P&L)
            ├─ Aggregate macro/sector context
            └─ Store in reports table

7:00 AM  → Report Delivery
            ├─ Send email notification to user
            └─ Update web dashboard (React frontend pulls via API)
```

---
