# AIHedgeFund - Documentation Index

**Project:** AI-Powered Autonomous UK Stock Trading System
**Current Phase:** Phase 2 - Solutioning (Moving to Phase 3 - Implementation)
**Date:** 2025-11-22
**Owner:** Longy

---

## 📍 Current Status

**Workflow Progress:** Phase 2 Solutioning → Phase 3 Implementation

✅ **Completed:**
- Phase 0: Discovery (brainstorming, research, product brief)
- Phase 1: Planning (PRD complete)
- Phase 2: Architecture (implementation architecture complete)

📋 **Next Steps:**
1. Create final epics and stories (REQUIRED)
2. Test design review (RECOMMENDED)
3. Implementation readiness check (REQUIRED gate check)
4. Sprint planning (BEGIN Phase 3)

---

## 📚 Core Documentation

### 1. **Product Requirements Document (PRD)**
**Location:** [prd/](./prd/) (Sharded document - 9 files)
**Size:** 109KB total
**Status:** Complete & Sharded (2025-11-22)
**Purpose:** Complete product vision, functional requirements, non-functional requirements, success criteria
**Index:** [prd/index.md](./prd/index.md)

**Key Sections:**
- Executive Summary (20-agent networked architecture)
- Product Scope (MVP features, 7 epics)
- Functional Requirements (FR-1 through FR-15)
- Non-Functional Requirements (performance, security, cost)
- Success Criteria (3-phase validation: Prove It → Scale It → Productize It)

**Use this for:** Understanding what to build, validation of implementation, traceability

---

### 2. **Implementation Architecture**
**Location:** [architecture/](./architecture/) (Sharded document - 15 files)
**Size:** 59KB total
**Status:** Complete & Sharded (2025-11-22)
**Purpose:** Technical implementation blueprint - AI agent consistency contract
**Index:** [architecture/index.md](./architecture/index.md)

**Key Sections:**
- **Technology Stack** (2025 production versions)
  - Python 3.14, FastAPI 0.121.3, LangGraph 1.0.5, React 19, PostgreSQL 18.1
- **Complete Project Structure** (300+ line source tree)
- **Epic-to-Architecture Mapping** (all 7 epics mapped to directories/files)
- **Implementation Patterns** (naming conventions, code organization, API formats)
  - Python: `snake_case` files/functions, `PascalCase` classes
  - Database: `snake_case` plural tables
  - API: `/api/v1/resource` pattern
- **Cross-Cutting Concerns** (logging, error handling, signal bus)
- **Data Architecture** (PostgreSQL schema, 10 tables)
- **API Contracts** (complete REST API specification)
- **Architecture Decision Records** (7 ADRs with rationale)

**Use this for:**
- **AI agent consistency** - All agents MUST follow these patterns
- Epic/story creation - Map requirements to actual file paths
- Implementation - Reference for tech stack, conventions, APIs
- Code reviews - Validate against patterns

---

### 3. **Epic Breakdown**
**Location:** [epics/](./epics/) (Sharded document - 7 files)
**Size:** 90KB total
**Status:** Initial version & Sharded (2025-11-22) - will be updated by create-epics-and-stories-final
**Purpose:** Decomposition of PRD into 7 implementable epics
**Index:** [epics/index.md](./epics/index.md)

**Epics:**
1. **Foundation & Data Architecture** - Multi-provider LLM, data ingestion, signal bus
2. **Discovery & Market Intelligence** - 7 discovery agents + macro/sector context
3. **Analysis Engine** - 8 analysis agents + LangGraph orchestration
4. **Portfolio & Tracking** - 3-tier system (portfolio, watchlist, research queue)
5. **Reporting & Execution** - Morning reports, web dashboard, manual trading
6. **Automation & Reliability** - Overnight batch processing, monitoring
7. **Configurability & Enhancement** - Agent management, on-demand analysis

**Note:** This will be replaced by final version from create-epics-and-stories-final workflow (includes architecture mapping)

---

### 4. **Workflow Status**
**File:** [bmm-workflow-status.yaml](./bmm-workflow-status.yaml)
**Purpose:** Track progress through BMM methodology phases
**Updated:** 2025-11-22

**Current Status:**
```yaml
Phase 2 - Solutioning:
  ✅ create-architecture: docs/architecture.md
  📋 create-epics-and-stories-final: required (NEXT)
  📋 test-design: recommended
  📋 validate-architecture: optional
  📋 implementation-readiness: required (gate check)

Phase 3 - Implementation:
  📋 sprint-planning: required
```

**Check status anytime:** Run `/bmad:bmm:workflows:workflow-status`

---

## 🗂️ Folder Structure

```
docs/
├── index.md                     # THIS FILE - Documentation index
├── bmm-workflow-status.yaml     # Workflow progress tracker
│
├── prd/                         # Product Requirements (SHARDED - 9 files)
│   ├── index.md                 # Table of contents
│   ├── executive-summary.md
│   ├── project-classification.md
│   └── ... (6 more sections)
│
├── architecture/                # Implementation Architecture (SHARDED - 15 files)
│   ├── index.md                 # Table of contents
│   ├── executive-summary.md
│   ├── decision-summary.md
│   └── ... (12 more sections)
│
├── epics/                       # Epic Breakdown (SHARDED - 7 files)
│   ├── index.md                 # Table of contents
│   ├── overview.md
│   ├── epic-1-foundation-data-architecture.md
│   └── ... (4 more sections)
│
├── archive/                     # Historical documents (not needed for next phase)
│   ├── prd-whole-2025-11-22.md              # Original whole PRD (archived)
│   ├── epics-whole-2025-11-22.md            # Original whole Epics (archived)
│   ├── architecture-whole-2025-11-22.md     # Original whole Architecture (archived)
│   ├── index-brownfield-2025-11-16.md              # Old brownfield docs index
│   ├── agent-network-architecture-conceptual-2025-11-16.md  # Conceptual design (superseded by architecture.md)
│   ├── product-brief-AIHedgeFund-2025-11-17.md     # Product brief (superseded by PRD)
│   ├── brainstorming-session-results-2025-11-16.md # Brainstorming session
│   ├── research-*.md                                # Research documents
│   ├── 1-system-architecture.md                    # Brownfield system docs
│   ├── 2-news-processing.md
│   ├── 3-current-workflow.md
│   ├── 4-api-integration.md
│   ├── 5-uk-adaptation-guide.md
│   └── ... (other historical documents)
│
└── sprint-artifacts/            # Phase 3 implementation artifacts (future)
```

---

## 🎯 Next Phase Workflows

### Immediate Next Steps

**1. Create Final Epics & Stories** (REQUIRED)
```bash
/bmad:bmm:workflows:create-epics-and-stories
```
- Uses PRD + Architecture to create implementation-ready stories
- Maps stories to actual file paths from architecture.md
- Includes acceptance criteria with technical patterns
- Agent: PM
- Output: Updated epics.md with architecture integration

**2. Test Design** (RECOMMENDED)
```bash
/bmad:bmm:workflows:test-design
```
- System-level testability assessment
- Testing strategies before implementation
- Agent: TEA (Test Engineering Agent)
- Output: Test strategy document

**3. Implementation Readiness** (REQUIRED - Gate Check)
```bash
/bmad:bmm:workflows:implementation-readiness
```
- Validates PRD + Architecture + Epics cohesion
- Ensures no gaps or contradictions
- Final check before Phase 3
- Agent: Architect
- Output: Validation report + go/no-go decision

**4. Sprint Planning** (Phase 3 Begins!)
```bash
/bmad:bmm:workflows:sprint-planning
```
- Creates sprint plan with story breakdown
- Ready to build!
- Agent: SM (Scrum Master)
- Output: Sprint status file, story queue

---

## 🔍 Quick Reference

### Key Decisions (from architecture.md)

**Tech Stack (2025 Versions):**
- Backend: Python 3.14 + FastAPI 0.121.3 + LangGraph 1.0.5
- Frontend: React 19 + TypeScript 5 + Vite 6
- Database: PostgreSQL 18.1
- LLM: Multi-provider (OpenAI/Anthropic/Google with fallback)

**Data Sources:**
- Tier 1: EODHD (fundamentals, £85/month)
- Tier 2: CityFALCON (UK RNS/insider, £30/month)
- Tier 3: IBKR (real-time execution)

**Processing Model:**
- Overnight batch (1am-7am GMT)
- 20-agent networked architecture
- Signal convergence scoring
- Adversarial challenge protocol

**Cost Target:** £200/month MVP

---

## 📖 Reading Order for New Team Members

1. **Start here** - This index (5 min)
2. **PRD Executive Summary** - Understand the vision (10 min)
3. **Architecture Executive Summary + Decision Summary Table** - Tech stack overview (15 min)
4. **Epic Breakdown Overview** - What we're building (15 min)
5. **Deep dive as needed** - Specific sections of PRD/Architecture

**Total onboarding time:** 45 minutes to full context

---

## 🗄️ Archived Documents

All historical documents (brainstorming, research, brownfield analysis, concept designs) have been moved to `archive/` folder.

**Access if needed:**
- Brownfield system documentation: `archive/index-brownfield-2025-11-16.md`
- Conceptual architecture: `archive/agent-network-architecture-conceptual-2025-11-16.md`
- Product brief: `archive/product-brief-AIHedgeFund-2025-11-17.md`
- Research & brainstorming: `archive/research-*.md`, `archive/brainstorming-*.md`

**These are for reference only** - not required for Phase 2→3 progression.

---

## ✅ Document Maintenance

**Last Cleanup:** 2025-11-22
**Next Review:** After create-epics-and-stories-final (replace epics.md)

**Cleanup Policy:**
- Archive documents when superseded by newer versions
- Keep only phase-critical documents in root
- Name archived files with date suffix
- Update this index after major workflow completions

---

**Ready to proceed to Phase 3 Implementation!**

For questions or workflow guidance, run: `/bmad:bmm:workflows:workflow-status`
