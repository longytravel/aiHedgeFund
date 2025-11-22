# PRD Modularity & Flexibility Additions

**Date:** 2025-11-19
**Issue:** PRD doesn't adequately reflect system modularity and ability to add/remove/configure agents
**Impact:** Critical architectural principle and competitive advantage undersold

---

## Proposed Changes to PRD

### 1. Executive Summary - Add Fourth Innovation

**Location:** After line 54 (Adversarial Challenge Protocol)

**ADD:**

```markdown
4. **Modular Agent Architecture** (Extensibility & Control)
   - Add, remove, or swap agents without code changes
   - Enable/disable agents based on performance, cost, or strategy preferences
   - Configure agent weights: Emphasize value vs. growth vs. technical analysis
   - Custom agent library: Build your own investor personas
   - Examples:
     - Cost optimization: Disable expensive LLM agents during testing
     - Strategy tuning: Run only value investing agents for dividend portfolio
     - Performance iteration: Remove underperforming agents, add specialists
     - Personal preference: "I don't trust technical analysis" → disable Technical Analyst
   - Supports rapid experimentation and continuous improvement
   - Future: Agent marketplace for sharing/selling custom investor personas
```

**Rationale:** Modularity is a core competitive advantage. Users can adapt the system to their strategy, risk tolerance, and preferences.

---

### 2. Product Scope - Update MVP Features

**Location:** Line 180, add new capability to existing description

**CHANGE FROM:**
```markdown
3. **Analysis Layer (8 Agents - Adapted from Existing US System)**
   - Value Investor Agent (Buffett/Graham philosophy: moats, intrinsic value)
   - Growth Investor Agent (Peter Lynch: PEG ratio, sustainable growth)
   ...
```

**CHANGE TO:**
```markdown
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
```

---

### 3. Growth Features - Add Agent Marketplace

**Location:** After line 265 (Enhanced Performance Analytics), add new Growth feature

**ADD:**

```markdown
5. **Agent Configuration & Extensibility**
   - Visual agent builder: Create custom investor personas via UI
   - Agent performance attribution: Track which agents contribute most alpha
   - Strategy templates: Pre-configured agent sets (Value Portfolio, Growth Aggressive, Dividend Income, etc.)
   - Agent versioning: A/B test different agent prompts/logic
   - Export/import agent configurations (share with community)

6. **Agent Marketplace** (Phase 3 Potential)
   - Community-contributed agents (ESG Investor, Biotech Specialist, Small-Cap Hunter)
   - Premium agents: Licensed investor methodologies (e.g., official Joel Greenblatt Magic Formula Agent)
   - Revenue opportunity: 30% commission on agent sales
```

---

### 4. New Functional Requirement - FR-2.7: Agent Management & Configurability

**Location:** After FR-2.6 (if you add Adversarial Challenge FR), or after FR-2.5

**ADD:**

```markdown
### FR-2.7: Agent Management & Configurability

**FR-2.7.1: Agent Enable/Disable**
- System SHALL allow users to enable/disable any analysis agent via configuration
- Disabled agents SHALL NOT run during analysis (cost savings, performance optimization)
- At least 3 agents MUST remain enabled (minimum for multi-perspective analysis)
- Agent status changes SHALL take effect on next overnight run
- UI SHALL show which agents are active in current configuration

**FR-2.7.2: Agent Weighting & Influence**
- System SHALL allow users to configure agent voting weights (default: 1.0 for all)
- Weight range: 0.1 (minimal influence) to 3.0 (3x influence)
- Example: User running dividend portfolio can set Value Investor weight = 2.0, Growth Investor weight = 0.5
- Weighted voting SHALL be reflected in Portfolio Manager decision logic:
  - BUY threshold adjusted: (Weighted bullish votes / Total weighted votes) > 65%
- UI SHALL provide preset strategy templates:
  - "Conservative Value" (Value 2.0x, Quality 1.5x, Growth 0.5x, Technical 0.5x)
  - "Aggressive Growth" (Growth 2.0x, Catalyst 1.5x, Value 0.5x, Quality 0.5x)
  - "Balanced" (All agents 1.0x)
  - "Technical Momentum" (Technical 2.0x, Sentiment 1.5x, fundamentals 0.5x)

**FR-2.7.3: Custom Agent Integration**
- System SHALL provide agent interface specification (input schema, output schema)
- Users SHALL be able to add custom agents via:
  - Python class implementing `AnalysisAgent` interface
  - Custom LLM prompt with structured output format
  - External API integration (call third-party analysis service)
- Custom agents SHALL participate in voting alongside built-in agents
- Custom agents SHALL be validated before activation (schema compliance check)

**FR-2.7.4: Agent Performance Tracking**
- System SHALL track performance attribution per agent:
  - Win rate when agent voted BUY
  - Average gain when agent voted BUY
  - False positive rate (agent voted BUY, stock declined)
- UI SHALL display agent performance dashboard:
  - Ranking by contribution to overall returns
  - Individual agent win rates
  - Cost per agent (LLM token usage)
  - ROI per agent (returns generated vs. cost)
- Users SHALL be able to disable underperforming agents based on data

**FR-2.7.5: Agent Configuration Persistence**
- System SHALL store agent configurations:
  - Active/inactive status per agent
  - Agent weights
  - Custom agent definitions
  - Strategy template selections
- Configurations SHALL be versioned (track changes over time)
- Users SHALL be able to export/import configurations (backup, sharing)
- System SHALL log all configuration changes in audit trail

**FR-2.7.6: Discovery Agent Configurability**
- System SHALL allow users to enable/disable any discovery agent
- Users SHALL be able to configure discovery agent parameters:
  - News Scanner: Customize news sources, keywords
  - Fundamental Screener: Define custom screens (P/E < 10, Debt/Equity < 0.3, etc.)
  - Volume Spike: Adjust threshold (2x vs. 3x average volume)
  - Analyst Activity: Filter by broker credibility score
- Configuration changes SHALL preserve signal convergence logic
```

---

### 5. New Functional Requirement - FR-9: System Extensibility

**Location:** After FR-8 (System Architecture)

**ADD:**

```markdown
### FR-9: System Extensibility & Modularity

**FR-9.1: Plugin Architecture**
- System SHALL implement plugin architecture for agents:
  - Discovery agents as plugins
  - Analysis agents as plugins
  - Decision agents (Risk Manager, Portfolio Manager) extendable
- Plugins SHALL be hot-swappable (add/remove without system restart where feasible)
- Plugin registry SHALL validate compatibility before loading

**FR-9.2: Data Source Modularity**
- System SHALL abstract data provider interface:
  - Easy to swap primary data source (EODHD → Finnhub → Yahoo Finance)
  - Multi-source redundancy (automatic fallback if primary unavailable)
- Data adapters SHALL normalize data to common format (agent logic agnostic to source)

**FR-9.3: Strategy Framework**
- System SHALL support multiple strategy configurations:
  - Save/load named strategies (e.g., "Conservative Dividend", "Aggressive Growth")
  - Quick-switch between strategies via UI dropdown
  - Backtest different strategies against historical data
- Each strategy configuration includes:
  - Active agents + weights
  - Discovery agent parameters
  - Risk parameters (position sizing, stop-loss %)
  - Watchlist triggers customization

**FR-9.4: API for External Integrations**
- System SHALL expose agent orchestration API:
  - POST /api/analyze-stock: Run analysis on arbitrary ticker with custom agent set
  - GET /api/agents/available: List all registered agents (built-in + custom)
  - POST /api/agents/configure: Update agent configuration programmatically
  - GET /api/agents/performance: Retrieve agent performance metrics
- API SHALL support third-party tools integration (Excel plugins, TradingView scripts, etc.)
```

---

### 6. Non-Functional Requirements - Update NFR-M2

**Location:** Lines 865-868 (NFR-M2: Configuration Management)

**ENHANCE:**

```markdown
**NFR-M2: Configuration Management & Modularity**
- All environment-specific settings in config files or environment variables
- No hardcoded values for: API endpoints, thresholds, agent selection, data sources
- **Agent configuration externalized:** No code changes required to add/remove/configure agents
- **User-configurable parameters via web UI:**
  - Risk settings (position size, stop-loss %)
  - Agent selection (enable/disable, weighting)
  - Strategy templates (quick-switch presets)
  - Discovery agent parameters (news sources, screening criteria)
  - Cost budgets and alerts
  - Email notification preferences
- **Configuration validation:** System SHALL validate config changes before applying (prevent breaking changes)
- **Configuration versioning:** Track config history, rollback capability
- **Hot reload where possible:** Config changes take effect without full system restart (exception: structural changes like new agent classes)
```

---

### 7. Non-Functional Requirements - Add NFR-M5: Extensibility

**Location:** After NFR-M4 (Documentation)

**ADD:**

```markdown
**NFR-M5: Extensibility & Plugin Architecture**
- **Agent Plugin Interface:** Well-documented interface for adding custom agents
- **Minimal coupling:** Agents SHALL NOT directly depend on each other (communicate via state graph)
- **Dependency injection:** Core system components (data sources, LLM providers) injectable, not hardcoded
- **Versioning support:** Agents SHALL declare version compatibility (prevent breaking changes)
- **Sandbox execution:** Custom agents run in controlled environment (resource limits, timeout protection)
- **Documentation for extensibility:**
  - Agent developer guide: How to create custom agents
  - API documentation: Integration endpoints
  - Example custom agents: Reference implementations (ESG Investor, Dividend Hunter)
  - Plugin migration guide: Upgrade path when core system changes
```

---

### 8. Product Differentiators - Add Modularity

**Location:** Lines 62-67 (Competitive Advantages), add new bullet

**ADD:**

```markdown
- **Modular & Extensible:** Unlike black-box robo-advisors, users control which agents run, adjust weights, and build custom investor personas. Supports continuous improvement and personalization.
```

---

### 9. Vision Features - Add Agent Marketplace

**Location:** Line 305-309 (Community & Learning section), enhance

**CHANGE FROM:**
```markdown
7. **Community & Learning**
   - User forums for strategy sharing
   - Agent marketplace (custom investor personas)
   - Performance leaderboards
   - Educational content (how each agent thinks)
```

**CHANGE TO:**
```markdown
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
```

---

### 10. New Section (Optional) - Agent Configuration Examples

**Location:** Could add after FR-9 or as appendix

**ADD:**

```markdown
## Agent Configuration Use Cases

**Use Case 1: Cost Optimization During Testing**
- **Scenario:** User testing system with small capital, wants to minimize LLM costs
- **Configuration:**
  - Disable expensive agents: Contrarian (complex reasoning), Sentiment (multi-source analysis)
  - Enable lightweight agents: Naked Trader (checklist-based), Technical Analyst (local calculations)
  - Fundamental Screener: Use cached data, run filters locally
- **Result:** 60% cost reduction while validating core workflow

**Use Case 2: Dividend Income Portfolio**
- **Scenario:** User wants consistent dividend income, not growth
- **Configuration:**
  - Value Investor weight: 2.5x (prioritize stable, undervalued dividend payers)
  - Quality/Moat weight: 2.0x (strong businesses with pricing power)
  - Growth Investor weight: 0.3x (low growth acceptable)
  - Catalyst Detective weight: 0.5x (short-term catalysts less relevant)
  - Custom screen in Fundamental Screener: Dividend yield > 4%, payout ratio < 70%, 10+ year dividend history
- **Result:** System recommends high-quality dividend stocks matching user goals

**Use Case 3: Turnaround Specialist Strategy**
- **Scenario:** Experienced trader focuses on distressed/turnaround opportunities
- **Configuration:**
  - Add custom "Turnaround Specialist" agent (analyzes management changes, restructuring plans, balance sheet repair)
  - Contrarian Agent weight: 2.5x (identify mispriced beaten-down stocks)
  - Quality/Moat weight: 0.5x (willingly accept temporarily impaired businesses)
  - Technical Analyst weight: 1.5x (entry timing critical in volatile turnarounds)
  - Risk Manager: Tighter stop-losses (5-7% vs. default 8-12%), smaller position sizes
- **Result:** Specialized system for high-risk, high-reward turnaround investing

**Use Case 4: Performance-Based Agent Pruning**
- **Scenario:** After 6 months, user analyzes agent performance data
- **Findings:**
  - Sentiment Analyst: 45% win rate (underperforming, noisy signals)
  - Catalyst Detective: 72% win rate (strong contributor)
  - Technical Analyst: 68% win rate but expensive (high token usage)
- **Configuration Changes:**
  - Disable Sentiment Analyst (poor performance)
  - Increase Catalyst Detective weight to 1.5x (reward performance)
  - Optimize Technical Analyst prompt (reduce tokens, maintain accuracy)
- **Result:** Improved overall system performance, 20% cost reduction

**Use Case 5: Multi-Market Expansion**
- **Scenario:** User wants to analyze both UK and US markets
- **Configuration:**
  - Clone agent configuration for US market
  - UK Configuration: Enable "UK Naked Trader" agent (specialized in UK market dynamics)
  - US Configuration: Disable UK Naked Trader, enable US-specific agents (e.g., Buffett Clone focuses on US companies)
  - Data sources: UK uses EODHD UK data, US uses EODHD US data
  - Run parallel overnight jobs (UK 1am-4am, US 4am-7am)
- **Result:** Dual-market coverage with specialized agent sets per market
```

---

## Summary of Changes

### What Gets Added/Enhanced:

1. **Executive Summary:** 4th innovation - Modular Agent Architecture
2. **Product Scope (MVP):** Clarify agents are configurable, weighted, extensible
3. **Growth Features:** Agent configuration UI, performance attribution
4. **Vision Features:** Agent marketplace, strategy templates library
5. **New FR-2.7:** Agent Management & Configurability (6 sub-requirements)
6. **New FR-9:** System Extensibility & Modularity (4 sub-requirements)
7. **NFR-M2:** Enhanced with agent configurability specifics
8. **New NFR-M5:** Extensibility & Plugin Architecture
9. **Competitive Advantages:** Add modularity bullet point
10. **Use Case Examples:** 5 real-world configuration scenarios (optional section)

### Why This Matters:

**For Development:**
- Drives architectural decisions (plugin system, dependency injection)
- Ensures testability (can test agents in isolation)
- Supports iterative development (add agents incrementally)

**For Users:**
- Control and transparency (not a black box)
- Personalization (adapt to strategy, risk tolerance, preferences)
- Cost optimization (disable expensive features during testing)
- Continuous improvement (remove underperformers, add specialists)

**For Business (Phase 3):**
- Agent marketplace revenue opportunity (£20k+/month potential)
- Differentiation vs. competitors (black-box robo-advisors)
- Community building (users contribute and share agents)
- Licensing opportunity (official investor methodology agents)

---

## Validation Impact

**This addresses a CRITICAL validation gap:**
- Current PRD: Mentions configurability in passing (lines 682, 867-868)
- Updated PRD: Elevates modularity to core architectural principle and competitive advantage
- New validation items:
  - ✅ Modularity documented as key differentiator
  - ✅ Explicit FRs for agent management
  - ✅ Extensibility architecture specified
  - ✅ Configuration management comprehensive

**Recommendation:** Integrate these changes into PRD before creating epics.md, so epic breakdown reflects modular architecture.
