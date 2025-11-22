# Executive Summary

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
