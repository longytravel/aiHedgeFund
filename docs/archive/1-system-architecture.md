# AI Hedge Fund - System Architecture & Multi-Agent Orchestration

**Generated:** 2025-11-16
**Purpose:** Understand how the AI agents work together to make trading decisions

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Multi-Agent Architecture](#multi-agent-architecture)
3. [LangGraph Orchestration](#langgraph-orchestration)
4. [Agent Workflow](#agent-workflow)
5. [State Management](#state-management)
6. [Key Components](#key-components)

---

## System Overview

This is a **multi-agent AI hedge fund** system that simulates the investment strategies of famous investors using LangChain/LangGraph orchestration.

### Architecture Pattern

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│   Visual Workflow Editor + React Flow Visualization     │
└────────────────────┬────────────────────────────────────┘
                     │ REST API
┌────────────────────▼────────────────────────────────────┐
│                Backend (FastAPI)                         │
│  Routes │ Services │ Database │ LangGraph Orchestrator  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         Core AI Agent System (src/)                      │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │  19 Investment Strategy Agents                  │     │
│  │  (Warren Buffett, Charlie Munger, etc.)         │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │  Analysis Agents                                │     │
│  │  • Fundamentals  • Technicals  • Valuation      │     │
│  │  • News Sentiment  • Risk Manager  • Portfolio  │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │  LangGraph State Graph                          │     │
│  │  (Orchestrates agent execution & state flow)    │     │
│  └────────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────────┘
```

---

## Multi-Agent Architecture

### Agent Categories

#### **1. Investment Strategy Agents (19 Total)**

These agents embody famous investor philosophies:

**Value Investors:**
- `warren_buffett` - Long-term value, moats, quality businesses
- `charlie_munger` - Mental models, circle of competence
- `ben_graham` - Deep value, margin of safety
- `mohnish_pabrai` - Cloning, concentrated bets
- `phil_fisher` - Scuttlebutt method, growth at reasonable price

**Growth Investors:**
- `cathie_wood` - Disruptive innovation, tech growth
- `peter_lynch` - PEG ratio, invest in what you know
- `growth_agent` - General growth metrics

**Contrarian/Macro Investors:**
- `michael_burry` - Contrarian deep value, special situations
- `stanley_druckenmiller` - Macro trends, reflexivity
- `bill_ackman` - Activist investing, catalysts

**Regional Specialists:**
- `rakesh_jhunjhunwala` - Indian market strategies

**Academic/Quantitative:**
- `aswath_damodaran` - Valuation, DCF analysis

#### **2. Analysis Agents (6 Total)**

- **`fundamentals`** - Financial statement analysis
- **`technicals`** - Technical indicators (RSI, MACD, moving averages)
- **`valuation`** - DCF, multiples, intrinsic value
- **`sentiment`** - Market sentiment indicators
- **`news_sentiment`** - News article sentiment analysis (LLM-powered)
- **`risk_manager`** - Position sizing, risk limits, exposure management
- **`portfolio_manager`** - Final trading decisions, order generation

---

## LangGraph Orchestration

### How It Works

**File:** `src/main.py`

The system uses **LangGraph** (state machine for agent workflows) to orchestrate agent execution:

```python
def create_workflow(selected_analysts=None):
    """Create the workflow with selected analysts."""
    workflow = StateGraph(AgentState)

    # 1. Start node
    workflow.add_node("start_node", start)

    # 2. Add selected analyst nodes (parallel execution)
    for analyst_key in selected_analysts:
        node_name, node_func = analyst_nodes[analyst_key]
        workflow.add_node(node_name, node_func)
        workflow.add_edge("start_node", node_name)

    # 3. Add risk and portfolio management (sequential)
    workflow.add_node("risk_management_agent", risk_management_agent)
    workflow.add_node("portfolio_manager", portfolio_management_agent)

    # 4. Connect all analysts → risk manager → portfolio manager → END
    for analyst_key in selected_analysts:
        workflow.add_edge(node_name, "risk_management_agent")

    workflow.add_edge("risk_management_agent", "portfolio_manager")
    workflow.add_edge("portfolio_manager", END)

    workflow.set_entry_point("start_node")
    return workflow
```

### Execution Flow

```
                        START
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │   All Selected Analysts (Parallel)   │
        │  ⚬ Warren Buffett                    │
        │  ⚬ Charlie Munger                    │
        │  ⚬ News Sentiment                    │
        │  ⚬ Fundamentals                      │
        │  ⚬ Technicals                        │
        │  ⚬ ... (user selectable)             │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │      Risk Management Agent           │
        │  • Analyzes all analyst signals      │
        │  • Sets position limits              │
        │  • Calculates max exposure           │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │      Portfolio Manager Agent         │
        │  • Makes final trading decisions     │
        │  • Generates buy/sell/short orders   │
        │  • Applies position constraints      │
        └─────────────────┬───────────────────┘
                          │
                          ▼
                         END
              (Returns trading decisions)
```

**Key Insight:** All analyst agents run in **parallel**, then results are aggregated by risk manager, then portfolio manager makes final decisions.

---

## Agent Workflow

### Per-Agent Execution Pattern

Every agent follows this pattern:

```python
def agent_function(state: AgentState, agent_id: str = "agent_name"):
    """
    1. Extract data from state
    2. Fetch required market data (prices, news, financials)
    3. Perform analysis (using LLM or calculations)
    4. Generate signal: "bullish", "bearish", "neutral"
    5. Calculate confidence: 0-100
    6. Create reasoning object
    7. Update state with results
    8. Return updated state
    """
    data = state.get("data", {})
    tickers = data.get("tickers")
    end_date = data.get("end_date")

    analysis_results = {}

    for ticker in tickers:
        # Fetch data (cached automatically)
        prices = get_price_data(ticker, start_date, end_date)
        news = get_company_news(ticker, end_date)
        financials = get_financial_metrics(ticker, end_date)

        # Perform analysis...
        signal = "bullish"  # or "bearish", "neutral"
        confidence = 75.0    # 0-100

        # Create structured output
        analysis_results[ticker] = {
            "signal": signal,
            "confidence": confidence,
            "reasoning": {...}
        }

    # Store in state
    state["data"]["analyst_signals"][agent_id] = analysis_results

    return {
        "messages": [HumanMessage(content=json.dumps(analysis_results), name=agent_id)],
        "data": state["data"],
    }
```

---

## State Management

### AgentState Structure

**File:** `src/graph/state.py`

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    data: Annotated[dict[str, any], merge_dicts]
    metadata: Annotated[dict[str, any], merge_dicts]
```

### State Data Structure

```python
{
    "messages": [
        # LangChain messages from each agent
    ],
    "data": {
        "tickers": ["AAPL", "MSFT", "GOOGL"],  # List of tickers to analyze
        "portfolio": {
            "cash": 100000.0,
            "margin_requirement": 0.5,
            "margin_used": 0.0,
            "positions": {
                "AAPL": {
                    "long": 0,
                    "short": 0,
                    "long_cost_basis": 0.0,
                    "short_cost_basis": 0.0,
                    "short_margin_used": 0.0
                }
            }
        },
        "start_date": "2024-10-01",
        "end_date": "2025-01-15",
        "analyst_signals": {
            # Each agent adds its signals here
            "warren_buffett": {
                "AAPL": {
                    "signal": "bullish",
                    "confidence": 85.0,
                    "reasoning": {...}
                }
            },
            "news_sentiment": {
                "AAPL": {
                    "signal": "bearish",
                    "confidence": 60.0,
                    "reasoning": {...}
                }
            }
            # ... all other agents
        },
        "current_prices": {
            "AAPL": 225.50,
            "MSFT": 415.30
        }
    },
    "metadata": {
        "show_reasoning": false,
        "model_name": "gpt-4o",
        "model_provider": "OpenAI"
    }
}
```

---

## Key Components

### 1. Market Data Tools

**File:** `src/tools/api.py`

Provides cached access to:
- `get_prices()` - Historical OHLCV price data
- `get_financial_metrics()` - Financial ratios, metrics
- `get_company_news()` - News articles with sentiment
- `get_insider_trades()` - Insider buying/selling
- `search_line_items()` - Specific financial statement items

**Data Source:** `financialdatasets.ai` API

### 2. LLM Integration

**File:** `src/llm/models.py`

Supports multiple LLM providers:
- OpenAI (GPT-4o, GPT-4, GPT-3.5)
- Anthropic Claude
- Groq
- DeepSeek
- Google (Gemini)
- xAI (Grok)
- **Ollama (local models)** ⭐

### 3. Progress Tracking

**File:** `src/utils/progress.py`

Real-time status updates for each agent's progress (used in UI and CLI).

### 4. Backtesting Engine

**Dir:** `src/backtesting/`

Complete backtesting framework:
- **engine.py** - Simulation engine
- **portfolio.py** - Portfolio tracking
- **metrics.py** - Performance metrics (Sharpe, drawdown, etc.)
- **benchmarks.py** - Compare against S&P 500, etc.

---

## Critical Insights for UK Adaptation

### What Makes This System Powerful

1. **Modular Agent Design** - Easy to add/modify agents
2. **Parallel Execution** - All analysts run simultaneously (fast)
3. **LangGraph Orchestration** - Clean state management, easy to extend
4. **Cached Data Access** - Reduces API calls and cost
5. **Multi-LLM Support** - Not locked into one provider

### Where to Modify for UK Stocks

1. **Data Source** (`src/tools/api.py`)
   - Replace `financialdatasets.ai` with UK market data provider
   - Options: Financial Modeling Prep, Alpha Vantage, Yahoo Finance (UK), LSE Data

2. **News Sources** (`src/agents/news_sentiment.py`)
   - Add UK-specific news sources (BBC Business, Financial Times, Reuters UK)
   - Filter for LSE/FTSE relevance

3. **Ticker Format** (`src/main.py`, `src/cli/input.py`)
   - Support LSE ticker format (e.g., "VOD.L", "BP.L")
   - Handle FTSE 100, FTSE 250, AIM tickers

4. **Market Hours** (New requirement)
   - UK market hours: 8:00 AM - 4:30 PM GMT
   - Add timezone handling for morning automation

5. **Regulatory Differences**
   - UK uses pence for some stocks (divide by 100)
   - Different insider trading disclosure rules
   - FCA regulations vs SEC

---

## Next Steps

See the other documentation files:
- **[2-news-processing.md](./2-news-processing.md)** - How news sentiment works (critical for morning automation)
- **[3-current-workflow.md](./3-current-workflow.md)** - Manual ticker selection (what to replace)
- **[4-api-integration.md](./4-api-integration.md)** - Where to plug in UK data
- **[5-uk-adaptation-guide.md](./5-uk-adaptation-guide.md)** - Step-by-step UK market setup
