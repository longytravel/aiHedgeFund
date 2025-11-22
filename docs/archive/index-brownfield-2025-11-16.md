# AI Hedge Fund - Documentation Index

**Generated:** 2025-11-16
**Project:** Multi-Agent AI Hedge Fund System
**Goal:** Adapt for UK stocks with autonomous morning news automation

---

## 🎯 Your Mission, Longy

Transform this US-focused AI hedge fund into an **autonomous UK stock trading system** that:

1. ✅ **Scans UK morning news automatically** (7:00 AM GMT daily)
2. ✅ **Identifies trading opportunities** from news sentiment
3. ✅ **Analyzes using 19 AI investment agents** (Warren Buffett, Charlie Munger, etc.)
4. ✅ **Generates trading decisions** without manual ticker selection
5. ✅ **Notifies you of opportunities** via email/UI

---

## 📚 Documentation Structure

This documentation set is organized into two main sections:

### **Phase 0: Strategic Planning Documents** ✨ NEW

**Discovery & Planning artifacts created through BMad Method:**

- **[Product Brief](./product-brief-AIHedgeFund-2025-11-17.md)** - Comprehensive product vision and strategy
- **[Brainstorming Session Results](./brainstorming-session-results-2025-11-16.md)** - Networked agent architecture breakthrough (20-agent system, signal convergence, three-tier tracking)
- **[Research: Data Sources](./research-data-sources-2025-11-16.md)** - UK market data providers analysis
- **[Product Requirements Document (PRD)](./prd.md)** ⭐ **NEW** - Complete functional & non-functional requirements (938 lines)

**Read these to understand the strategic vision and complete requirements.**

---

### **Technical Implementation Documents**

**Brownfield system analysis - how the current system works:**

### **1. [System Architecture & AI Agent Orchestration](./1-system-architecture.md)** ⭐ START HERE

**Read this first to understand how everything works.**

**What You'll Learn:**
- How 19 AI agents work together using LangGraph
- Parallel agent execution → Risk management → Portfolio decisions
- Agent workflow patterns (all agents follow same structure)
- State management and data flow
- Where to modify for UK stocks

**Key Sections:**
- Multi-Agent Architecture
- LangGraph Orchestration
- Agent Workflow Patterns
- Critical Insights for UK Adaptation

**Time:** 15-20 minutes

---

### **2. [News Processing & Sentiment Analysis](./2-news-processing.md)** 🔥 CRITICAL

**How news sentiment works - this is the foundation of your morning automation.**

**What You'll Learn:**
- Current news sentiment agent implementation
- LLM-powered headline analysis
- Confidence score calculation
- How to add UK news sources (BBC, FT, Reuters)
- Morning scanner implementation strategy

**Key Sections:**
- News Sentiment Agent Deep Dive
- UK Morning News Scanner (complete code)
- Automation Strategy (3-phase approach)

**Implementation Code:**
- `UKMorningNewsScanner` class
- News aggregation from UK sources
- Ticker extraction from articles
- Opportunity identification logic

**Time:** 20-25 minutes

---

### **3. [Current Workflow & Manual Ticker Selection](./3-current-workflow.md)** 🎯 WHAT TO REPLACE

**Understand what needs to change for automation.**

**What You'll Learn:**
- How users currently provide tickers manually (CLI/API)
- Where ticker input happens in code
- Replacement strategies (3 options)
- New automated data flow diagram

**Key Files:**
- `src/main.py` - Entry point to modify
- `src/cli/input.py` - Manual input to replace
- `app/backend/routes/automation.py` - New automation endpoint

**Before/After Code Examples:**
- Manual: User types tickers → System analyzes
- Automated: News scanner finds tickers → Auto-analyzes → Notifies

**Time:** 10-15 minutes

---

### **4. [API Integration Points for UK Market Data](./4-api-integration.md)** 🔌 TECHNICAL

**Where to plug in UK stock data sources.**

**What You'll Learn:**
- Current US data API (`financialdatasets.ai`)
- 3 UK data provider options:
  - **Financial Modeling Prep** (Recommended - $29/month)
  - Alpha Vantage (Free tier available)
  - Yahoo Finance (Free, good for testing)
- LSE ticker format handling (`.L` vs `.LON`)
- Integration patterns (conditional imports, abstraction layer)

**Implementation Files:**
- `src/tools/api_uk.py` (new module)
- `src/tools/market_data.py` (unified interface)
- Environment configuration

**Ready-to-use Code:**
- FMP integration functions
- Yahoo Finance fallback
- Ticker normalization
- Caching strategy

**Time:** 15 minutes

---

### **5. [UK Adaptation Guide - Complete Implementation](./5-uk-adaptation-guide.md)** 📋 ACTION PLAN

**Step-by-step implementation from start to finish.**

**What You'll Learn:**
- 4-phase implementation plan (4 days estimated)
- Phase 1: UK Data Integration
- Phase 2: Morning News Scanner
- Phase 3: Automation Integration
- Phase 4: Deployment

**Complete Code Included:**
- UK API module (`api_uk.py`)
- Morning scanner (`morning_scanner.py`)
- Scheduler (`scheduler.py`)
- Notification system (`notifications.py`)
- UK company/ticker mapping database
- Testing scripts

**Deployment Options:**
- Local machine (nohup)
- Cloud (AWS/DigitalOcean)
- Systemd service setup

**Time:** Reference guide - implement over 2-4 days

---

## 🚀 Quick Start Path

**If you want to dive in right now:**

1. **Read:** [1-system-architecture.md](./1-system-architecture.md) (understand the foundation)
2. **Study:** [2-news-processing.md](./2-news-processing.md) (your core automation)
3. **Implement:** Follow [5-uk-adaptation-guide.md](./5-uk-adaptation-guide.md) phase-by-phase

**If you want to learn the whole system first:**

Read all 5 docs in order (90 minutes total), then implement.

---

## 🎯 Key Technologies Used

### Current System

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Orchestration** | LangGraph + LangChain | Multi-agent workflow management |
| **LLM Providers** | OpenAI, Anthropic, Groq, Ollama | AI analysis engines |
| **Backend** | FastAPI (Python 3.11+) | REST API server |
| **Frontend** | React + TypeScript + Vite | Web UI |
| **Visualization** | React Flow | Agent workflow visualization |
| **Database** | SQLite + SQLAlchemy | Data persistence |
| **Data Source** | financialdatasets.ai | US market data |

### Your UK Additions

| Component | Technology | Purpose |
|-----------|------------|---------|
| **UK Data** | Financial Modeling Prep | LSE stock data |
| **News Aggregation** | NewsAPI.org | UK morning news |
| **Scheduling** | Python `schedule` library | Daily automation |
| **Notifications** | Email (SMTP) | Opportunity alerts |
| **Ticker Mapping** | JSON database | Company → LSE ticker |

---

## 📊 Project Structure

```
AIHedgeFund/
├── ai-hedge-fund/                  # Main project
│   ├── src/                        # Core AI system
│   │   ├── agents/                 # 19 investment strategy agents
│   │   │   ├── warren_buffett.py
│   │   │   ├── charlie_munger.py
│   │   │   ├── news_sentiment.py   ← Study this
│   │   │   └── ... (16 more)
│   │   ├── graph/                  # LangGraph orchestration
│   │   │   └── state.py            ← Agent state management
│   │   ├── tools/
│   │   │   ├── api.py              ← Current US data API
│   │   │   └── api_uk.py           ← ADD THIS (UK data)
│   │   ├── automation/             ← ADD THIS FOLDER
│   │   │   ├── morning_scanner.py  ← UK news scanner
│   │   │   ├── scheduler.py        ← Daily automation
│   │   │   └── notifications.py    ← Email alerts
│   │   ├── backtesting/            # Backtesting engine
│   │   ├── llm/                    # LLM configurations
│   │   ├── utils/                  # Helper functions
│   │   └── main.py                 ← Entry point (MODIFY)
│   │
│   ├── app/                        # Web application
│   │   ├── backend/                # FastAPI server
│   │   │   ├── routes/
│   │   │   │   └── automation.py   ← ADD THIS (automation endpoints)
│   │   │   └── services/
│   │   └── frontend/               # React UI
│   │       └── src/
│   │           └── components/
│   │               └── AutomationDashboard.tsx  ← ADD THIS
│   │
│   └── .env                        ← Add UK API keys here
│
└── docs/                           # THIS DOCUMENTATION
    ├── index.md                    ← YOU ARE HERE
    ├── 1-system-architecture.md
    ├── 2-news-processing.md
    ├── 3-current-workflow.md
    ├── 4-api-integration.md
    └── 5-uk-adaptation-guide.md
```

---

## 🔧 Prerequisites

**To implement the UK adaptation, you'll need:**

1. ✅ **API Keys:**
   - Financial Modeling Prep (or Yahoo Finance for free)
   - NewsAPI.org (for UK news aggregation)
   - OpenAI/Anthropic (for LLM analysis)

2. ✅ **Python Skills:**
   - Intermediate Python (functions, classes, async)
   - Familiarity with APIs and JSON
   - Basic understanding of LangChain (helpful but not required)

3. ✅ **Infrastructure:**
   - Server/VPS for 24/7 operation (or just run on your PC)
   - Email account for notifications (Gmail works)

4. ✅ **Time:**
   - Day 1: UK data integration (3-4 hours)
   - Day 2: Morning news scanner (4-5 hours)
   - Day 3: Automation integration (3-4 hours)
   - Day 4: Testing & deployment (2-3 hours)

**Total:** 2-4 days for full implementation

---

## 💡 What Makes This System Powerful

### Multi-Agent Architecture

**19 AI agents** modeling famous investors:
- Value: Buffett, Munger, Graham, Pabrai
- Growth: Cathie Wood, Peter Lynch
- Contrarian: Michael Burry, Druckenmiller
- + Analysis agents: Fundamentals, Technicals, News Sentiment, Risk, Portfolio

**Each agent:**
1. Fetches relevant market data
2. Performs specialized analysis
3. Generates signal (bullish/bearish/neutral) + confidence
4. Provides structured reasoning

**All run in parallel** → Aggregated by Risk Manager → Final decisions by Portfolio Manager

### LangGraph Orchestration

**Clean state machine** for agent coordination:
- Parallel execution of analysts (fast)
- Sequential risk → portfolio stages
- Shared state (AgentState) with message history
- Easy to extend (add new agents by just adding nodes)

### Flexible & Modular

- **Swap LLM providers** easily (OpenAI, Claude, local Ollama)
- **Add new agents** without changing core workflow
- **Replace data sources** (US → UK)
- **Customize analysis logic** per agent

---

## 🎓 Learning the System

### If You're New to LangChain/LangGraph

1. **Start simple:** Read the architecture doc to understand the flow
2. **Study one agent:** Look at `news_sentiment.py` - it's well-commented
3. **Trace the execution:** Run the system manually and watch agent outputs
4. **Modify gradually:** Start by changing news sources, then add UK data

### If You're Experienced

You can jump straight to implementation:
1. Skim architecture doc for context
2. Read news processing doc for automation strategy
3. Follow the UK adaptation guide to build

---

## 📞 Support & Resources

### External Documentation

- **LangChain Docs:** https://python.langchain.com/docs/
- **LangGraph Guide:** https://langchain-ai.github.io/langgraph/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Flow:** https://reactflow.dev/

### Recommended Reading Order

For this project specifically:

1. This index (overview)
2. System architecture (understand foundations)
3. News processing (your core feature)
4. UK adaptation guide (implementation)
5. API integration + Current workflow (as needed during implementation)

---

## ✅ Success Checklist

Track your progress:

**Understanding Phase:**
- [ ] Read system architecture document
- [ ] Understand LangGraph workflow
- [ ] Study news sentiment agent
- [ ] Review agent execution patterns

**Implementation Phase:**
- [ ] Choose UK data provider (FMP recommended)
- [ ] Create `api_uk.py` module
- [ ] Test UK data access
- [ ] Build UK company/ticker mapping
- [ ] Implement morning news scanner
- [ ] Test news aggregation
- [ ] Integrate with main workflow
- [ ] Add automation scheduler
- [ ] Set up notifications
- [ ] Deploy to server

**Testing Phase:**
- [ ] Test UK data APIs
- [ ] Test morning scanner
- [ ] Test full automated workflow
- [ ] Verify notifications work
- [ ] Run for 1 week in test mode

**Production Phase:**
- [ ] Go live with automation
- [ ] Monitor daily scans
- [ ] Refine opportunity filters
- [ ] Track trading performance

---

## 🎯 Expected Outcomes

**After completing the UK adaptation:**

### Every Weekday Morning at 7:00 AM GMT:

1. ✅ System automatically scans UK business news
2. ✅ Identifies companies mentioned with strong sentiment
3. ✅ Maps company names to LSE tickers
4. ✅ Ranks by confidence and article count
5. ✅ Runs full 19-agent analysis on top opportunities
6. ✅ Generates trading decisions
7. ✅ Emails you the opportunities

### You Wake Up To:

📧 **Email:** "3 UK Market Opportunities Identified"
- VOD.L: BUY 1000 shares (85% confidence)
- BP.L: HOLD (neutral signals)
- HSBC.L: SELL 500 shares (70% confidence, bearish)

**No manual work required!**

---

## 🚀 Let's Get Started

**Ready to build your autonomous UK trading system?**

👉 **Start here:** [1. System Architecture & AI Agent Orchestration](./1-system-architecture.md)

**Questions as you build?**
- Re-read relevant sections
- Study the code examples
- Test incrementally

**Good luck, Longy! You've got this.** 🎯
