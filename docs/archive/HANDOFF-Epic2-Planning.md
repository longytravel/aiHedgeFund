# HANDOFF NOTES: Epic 2 (Discovery & Market Intelligence) Planning

**Date:** 2025-11-22
**Status:** Ready to detail Epic 2
**Workflow:** `/bmad:bmm:workflows:create-epics-and-stories` (IN PROGRESS)

---

## Current State

**COMPLETED:**
- ✅ PRD: Complete (2095 lines, comprehensive)
- ✅ Architecture: Complete (agent-network-architecture.md - 20+ agent networked system)
- ✅ Epic 1: Foundation & Data Architecture - FULLY DETAILED (8 stories)

**IN PROGRESS:**
- 🔄 Epic 2: Discovery & Market Intelligence - NEEDS DETAILING
- 🔄 Workflow is paused at Step 0, waiting for mode selection

**PENDING:**
- ⏳ Epics 3-7: Need outline/light detail
- ⏳ Implementation readiness check
- ⏳ Architecture Decision Record

---

## Key Architectural Decisions Made (Winston's Recommendations)

### 1. Batch Overnight Architecture (NOT Sequential)
**Decision:** Build overnight batch processing system, NOT one-stock-at-a-time interactive

**Workflow:**
```
1am-3am: DISCOVERY PHASE
  - Scan ALL 600 FTSE stocks with cheap/fast agents
  - Generate 40-50 signals
  - Aggregate & score → Top 15 stocks identified

3am-5am: ANALYSIS PHASE
  - Deep analysis on Top 15 (6 expert agents × 15 stocks = 90 parallel analyses)
  - Risk Manager challenges
  - Portfolio Manager synthesizes
  - Result: 2-3 BUY recommendations + 5-10 watchlist adds

5am-6am: PORTFOLIO REVIEW
  - Check existing holdings for SELL signals
  - Monitor watchlist triggers

6am-7am: REPORT GENERATION
  - Deliver morning report with CHOICES
```

**Why:** Fundamentally different from existing US codebase (which is sequential). Your vision = market-wide discovery → scoring → recommendations.

### 2. Multi-LLM Strategy (Use All Providers)
**Decision:** Support OpenAI + Anthropic + Google from Day 1 via LangChain abstraction

**Why:**
- Cost optimization (30%+ savings using cheap models for discovery, premium for decisions)
- Quality optimization (best LLM for each task)
- Future-proofing (not locked to one vendor)
- Resilience (fallback when provider down)

**Implementation:** Story 1.8 (Multi-Provider LLM Abstraction Layer) - already detailed in Epic 1

**Cost Estimate:** £68/month (vs £100 OpenAI-only) with better quality

### 3. UK Data Architecture
**Decision:** EODHD (primary) + CityFALCON (secondary) + IBKR (execution)

**Priority:**
- Phase 1: EODHD only (Epic 1, Story 1.4)
- Phase 2: Add CityFALCON for insider trading (Epic 2 or 7)
- Phase 3: IBKR integration for real-time execution

### 4. Lean Epic Approach
**Decision:** Full detail on Epic 1-2, medium detail Epic 3, light outline Epics 4-7

**Why:** Solo developer, learn by building, avoid over-planning

**Epic Detail Levels:**
- Epic 1: ✅ FULL (8 stories) - DONE
- Epic 2: 🔄 FULL (10-12 stories) - IN PROGRESS NOW
- Epic 3: MEDIUM (8-10 stories) - Do after Epic 2
- Epics 4-7: LIGHT (2-3 stories each) - Outline only

### 5. Use Existing Code Selectively
**Decision:** Learn from existing US codebase but NOT constrained by it

**KEEP:**
- Agent personas/prompts (12 investor personalities)
- LangGraph orchestration patterns
- FastAPI backend structure
- React dashboard patterns
- Financial data fetching patterns

**DISCARD:**
- Sequential workflow (wrong for batch processing)
- Interactive user-driven analysis (wrong for overnight autonomous)
- US market assumptions (LSE is different)
- Real-time decision making (wrong for morning report workflow)

---

## What Epic 2 (Discovery) Must Cover

Epic 2 is THE CORE INNOVATION - overnight batch discovery with signal convergence.

**Stories needed (10-12 estimated):**

1. **Story 2.1:** News Scanner Agent (UK sources: BBC, FT, Reuters, City AM)
   - Batch scan overnight news
   - Identify catalysts (contracts, M&A, regulatory approvals)
   - Generate `NEW_CATALYST` signals

2. **Story 2.2:** Fundamental Screener Agent
   - Batch scan 600 FTSE stocks
   - Run multiple screens (low P/E + high ROE, growth, Naked Trader checklist)
   - Generate `FUNDAMENTAL_MATCH` signals

3. **Story 2.3:** Insider Trading Agent
   - Fetch LSE director dealings (via CityFALCON or Companies House)
   - Identify significant buying (multiple directors, large amounts)
   - Generate `INSIDER_CONVICTION` signals

4. **Story 2.4:** Volume & Price Action Agent
   - Detect unusual activity (3x+ volume spikes, breakouts, 52-week highs)
   - Generate `UNUSUAL_ACTIVITY` signals

5. **Story 2.5:** Signal Aggregation & Scoring Engine ⭐ CRITICAL
   - Group signals by ticker
   - Calculate convergence scores (weighted by signal type)
   - Apply macro/sector multipliers
   - Rank all stocks
   - Identify Top 15 for deep analysis

6. **Story 2.6:** Macro Economist Agent (NEW - moved to MVP)
   - Weekly UK macro analysis (GDP, inflation, BoE policy, PMI)
   - Identify regime (expansion/recession/stagflation)
   - Generate `MACRO_REGIME_CHANGE` signal
   - Output: Current regime + sector implications

7. **Story 2.7:** Sector Rotation Agent (NEW - moved to MVP)
   - Weekly sector performance analysis
   - Identify favored/disfavored sectors based on macro
   - Generate `SECTOR_PREFERENCES_UPDATE` signal
   - Output: Top 3 sectors to overweight, bottom 3 to avoid

8. **Story 2.8:** Research Queue Management (Tier 3 Tracking)
   - Stocks scoring 31-60 points go to research queue
   - Store with score, signals, timestamp
   - Re-score daily as new signals arrive

9. **Story 2.9:** Signal Decay & Time-based Weighting
   - Signals decay over time (fast: earnings beat, slow: insider buying)
   - Implement decay rates per signal type
   - Update scores daily

10. **Story 2.10:** Discovery Batch Orchestration (1am-3am workflow)
    - LangGraph workflow for discovery phase
    - Parallel execution of discovery agents
    - Error handling, retries, graceful degradation
    - State persistence (can resume if crashes)

**Optional Stories (defer to Epic 7):**
- Story 2.11: Earnings Surprise Agent (Phase 2)
- Story 2.12: Analyst Activity Agent (Phase 2)
- Story 2.13: Corporate Actions Agent (Phase 2)

---

## Workflow Status

**Currently Running:** `/bmad:bmm:workflows:create-epics-and-stories`

**Paused At:** Step 0 - Mode selection

**What to Select:** **Option 1: CONTINUING**
- Epic 1 is complete (8 stories detailed)
- Continue where we left off
- Detail Epic 2 next

**Workflow Will Do:**
1. Load PRD, Architecture, existing epics.md
2. Generate Epic 2 stories following Epic 1 pattern
3. Use BDD acceptance criteria (Given/When/Then)
4. Add detailed technical notes
5. Save to epics.md after each story (checkpoint protocol)
6. Present for review with [a]dvanced Elicitation, [c]ontinue, [p]arty mode, [y]OLO options

---

## After Context Reset - Exact Steps

1. **Run this command:**
   ```
   /bmad:bmm:workflows:create-epics-and-stories
   ```

2. **When asked for mode, select:** `1` (CONTINUING)

3. **The workflow will:**
   - Load existing epics.md (Epic 1 already detailed)
   - Load PRD and Architecture
   - Begin detailing Epic 2: Discovery & Market Intelligence
   - Generate 10-12 stories following the scope above

4. **At each checkpoint:**
   - Review the story
   - Press `c` to continue (or `a` for advanced elicitation if you want to refine)
   - Workflow saves to epics.md incrementally

5. **After Epic 2 is detailed:**
   - Mark todo as complete
   - Optionally outline Epics 3-7 (light detail)
   - Run implementation readiness check

---

## Agent Persona Context

**You are Winston** - System Architect
- Pragmatic, values boring tech that works
- Balances idealism with reality
- Focus on user value, not architectural purity
- Prefer simple solutions that scale when needed

**Communication Style:**
- Technical but practical
- Connect decisions to business value
- "I've seen this pattern work at scale"
- No time estimates (AI changes everything)

---

## Key Files Reference

- **PRD:** `docs/prd.md` (2095 lines)
- **Architecture:** `docs/agent-network-architecture.md` (20+ agent system)
- **Epics:** `docs/epics.md` (Epic 1 done, need Epic 2)
- **Existing Code:** `ai-hedge-fund/` (US system, reference only)
- **Config:** `.bmad/bmm/config.yaml`
- **Workflow Status:** `docs/bmm-workflow-status.yaml`

---

## Todo List

1. ✅ Load workflow and detect mode
2. 🔄 Detail Epic 2: Discovery & Market Intelligence (10-12 stories)
3. ⏳ Outline Epics 3-7 at high level
4. ⏳ Run implementation readiness check
5. ⏳ Create Architecture Decision Record

---

## Quick Reference: Signal Types & Scores

**Discovery Signals (Epic 2):**
- `NEW_CATALYST` - 15 points, medium decay (2 weeks)
- `INSIDER_CONVICTION` - 25 points, slow decay (3 months)
- `UNUSUAL_ACTIVITY` - 15 points, fast decay (3 days)
- `FUNDAMENTAL_MATCH` - 15 points, slow decay (stable)
- `EARNINGS_SURPRISE` - 20 points, fast decay (1 week) [Phase 2]
- `ANALYST_SHIFT` - 10 points, medium decay (1 month) [Phase 2]
- `SPECIAL_SITUATION` - 20 points, variable decay [Phase 2]

**Macro/Sector Multipliers:**
- Macro aligned: 1.5x
- Sector favored: 1.3x
- Sector disfavored: 0.7x
- Macro headwind: 0.5x

**Convergence Thresholds:**
- 0-30: Monitor only
- 31-60: Research Queue (Tier 3)
- 61-90: Deep Analysis
- 91+: Priority Deep Analysis

---

## END OF HANDOFF

**Next Action:** Run `/bmad:bmm:workflows:create-epics-and-stories` and select option `1` (CONTINUING)
