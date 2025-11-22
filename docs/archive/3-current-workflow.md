# Current Workflow & Manual Ticker Selection

**Generated:** 2025-11-16
**Purpose:** Understand what needs to be replaced for automation

---

## Current Manual Workflow

### How the System Runs Now

**Entry Point:** `src/main.py` (CLI) or Backend API

#### CLI Workflow

```bash
# User runs the system with manual inputs:
python src/main.py \
  --tickers AAPL,MSFT,GOOGL \  # ⚠️ MANUAL INPUT
  --start-date 2024-10-01 \
  --end-date 2025-01-15 \
  --analysts warren_buffett,charlie_munger,news_sentiment \
  --model gpt-4o \
  --initial-cash 100000
```

**Interactive Mode:**
```bash
python src/main.py
# System prompts:
# 1. "Enter tickers (comma-separated): " → User types AAPL,MSFT
# 2. "Select analysts: " → User checks boxes
# 3. "Select LLM model: " → User chooses GPT-4o
# Then runs analysis...
```

### The Problem: Manual Ticker Selection

**File:** `src/cli/input.py`

```python
def parse_cli_inputs(require_tickers=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tickers",
        type=str,
        required=True,  # ⚠️ USER MUST PROVIDE
        help="Comma-separated list of stock ticker symbols"
    )
    args = parser.parse_args()
    tickers = parse_tickers(args.tickers)  # Split by comma
    return tickers
```

**This is what you want to eliminate!**

---

## What Needs to Change

### Goal: Autonomous Morning Workflow

```
OLD (Manual):
User → Picks tickers → System analyzes → Returns signals

NEW (Autonomous):
System → Scans morning news → Finds tickers → Analyzes → Notifies user
```

### Replacement Strategy

#### Option 1: Replace CLI Input with News Scanner

**Before:**
```python
# src/main.py (line 133-141)
if __name__ == "__main__":
    inputs = parse_cli_inputs(require_tickers=True)  # ← REMOVE THIS
    tickers = inputs.tickers  # ← Manual input
    run_hedge_fund(tickers=tickers, ...)
```

**After:**
```python
# src/main.py (modified)
from src.automation.morning_scanner import UKMorningNewsScanner

if __name__ == "__main__":
    # 1. Scan morning news
    scanner = UKMorningNewsScanner()
    scan_results = scanner.scan_morning_news()

    # 2. Get tickers from opportunities
    tickers = scan_results["opportunities"]

    if not tickers:
        print("No opportunities identified today.")
        sys.exit(0)

    print(f"Analyzing {len(tickers)} opportunities: {tickers}")

    # 3. Run analysis automatically
    inputs = parse_cli_inputs(require_tickers=False)  # No manual tickers
    run_hedge_fund(
        tickers=tickers,  # ← From news scanner!
        start_date=inputs.start_date,
        end_date=inputs.end_date,
        ...
    )
```

#### Option 2: Backend API Automation

**New Endpoint:** `app/backend/routes/automation.py`

```python
from fastapi import APIRouter
from src.automation.morning_scanner import UKMorningNewsScanner
from src.main import run_hedge_fund

router = APIRouter(prefix="/automation", tags=["Automation"])

@router.post("/morning-scan")
async def run_morning_scan():
    """
    Automated morning news scan and analysis.
    No manual ticker input required.
    """
    # 1. Scan news
    scanner = UKMorningNewsScanner()
    scan_results = scanner.scan_morning_news()

    if not scan_results["opportunities"]:
        return {
            "status": "no_opportunities",
            "message": "No high-confidence opportunities found",
            "scan_summary": scan_results["news_summary"]
        }

    # 2. Run analysis on opportunities
    tickers = scan_results["opportunities"]
    hedge_fund_result = run_hedge_fund(
        tickers=tickers,
        start_date=...,
        end_date=...,
        ...
    )

    return {
        "status": "success",
        "opportunities": tickers,
        "trading_decisions": hedge_fund_result["decisions"],
        "scan_summary": scan_results["news_summary"]
    }

@router.get("/schedule-status")
async def get_schedule_status():
    """Check if morning scan is scheduled and last run time."""
    return {
        "scheduled": True,
        "next_run": "2025-01-16 07:00:00 GMT",
        "last_run": "2025-01-15 07:00:00 GMT",
        "last_opportunities_count": 3
    }
```

#### Option 3: Scheduled Cron Job

**File:** `scripts/morning_automation.sh`

```bash
#!/bin/bash
# Run every weekday at 7:00 AM GMT

cd /path/to/ai-hedge-fund

# Activate Python environment
source venv/bin/activate

# Run morning scan (no manual input)
python -c "
from src.automation.morning_scanner import UKMorningNewsScanner
from src.main import run_hedge_fund
import json

scanner = UKMorningNewsScanner()
results = scanner.scan_morning_news()

if results['opportunities']:
    print('Opportunities found:', results['opportunities'])
    # Run analysis and save results
    hedge_fund_result = run_hedge_fund(
        tickers=results['opportunities'],
        ...
    )
    # Email/notify user
    send_notification(hedge_fund_result)
else:
    print('No opportunities today.')
"
```

**Crontab Entry:**
```bash
# Run Monday-Friday at 7:00 AM GMT
0 7 * * 1-5 /path/to/scripts/morning_automation.sh
```

---

## Current Data Flow

```
┌─────────────────────────────────────────────────────┐
│         User Provides Tickers Manually              │
│              (AAPL, MSFT, GOOGL)                    │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              Create Workflow                         │
│   • Add selected analyst nodes                      │
│   • Initialize agent state with tickers             │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│          Run Agents (Parallel)                       │
│   For each ticker in [AAPL, MSFT, GOOGL]:          │
│   • Fetch prices                                    │
│   • Fetch news                                      │
│   • Fetch financials                                │
│   • Analyze & generate signal                       │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│        Risk Management → Portfolio Manager           │
│   • Aggregate signals                               │
│   • Calculate position limits                       │
│   • Generate trading decisions                      │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              Return Results                          │
│   { AAPL: {action: "buy", ...},                    │
│     MSFT: {action: "hold", ...},                   │
│     GOOGL: {action: "sell", ...} }                 │
└─────────────────────────────────────────────────────┘
```

---

## Automated Data Flow (Your Goal)

```
┌─────────────────────────────────────────────────────┐
│      7:00 AM GMT - Scheduled Trigger                │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│         UK Morning News Scanner                      │
│   • Fetch UK news (BBC, FT, Reuters, etc.)         │
│   • Extract mentioned companies                     │
│   • Map companies → LSE tickers                     │
│   • Analyze sentiment for each ticker              │
│   • Rank by confidence                             │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│      Identify High-Confidence Opportunities          │
│   Filters:                                          │
│   • Confidence > 70%                                │
│   • Multiple article confirmations (≥3)             │
│   • Strong bullish/bearish signal                   │
│                                                     │
│   Output: [VOD.L, BP.L, HSBC.L]                    │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│       Run Full Hedge Fund Analysis                   │
│   (Same as current system, but automatic)           │
│   • Create workflow with all analysts               │
│   • Analyze [VOD.L, BP.L, HSBC.L]                  │
│   • Generate trading decisions                      │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│           Notify User or Auto-Execute                │
│   Option A: Email/SMS notification                  │
│   Option B: Display in web UI                      │
│   Option C: Auto-execute trades (broker API)       │
└─────────────────────────────────────────────────────┘
```

---

## Key Files to Modify

### 1. Remove Manual Input Requirement

**File:** `src/main.py`

```python
# BEFORE
if __name__ == "__main__":
    inputs = parse_cli_inputs(require_tickers=True)  # ← CHANGE THIS
    tickers = inputs.tickers

# AFTER
if __name__ == "__main__":
    # Check if running in automated mode
    if os.getenv("AUTOMATED_MODE") == "true":
        from src.automation.morning_scanner import get_morning_opportunities
        tickers = get_morning_opportunities()
    else:
        # Interactive mode (keep for manual testing)
        inputs = parse_cli_inputs(require_tickers=True)
        tickers = inputs.tickers
```

### 2. Create News Scanner Module

**New File:** `src/automation/morning_scanner.py`

(See detailed implementation in `2-news-processing.md`)

### 3. Add Automation Routes

**New File:** `app/backend/routes/automation.py`

```python
@router.post("/morning-scan")
async def run_morning_scan():
    # Implementation above
    pass

@router.get("/opportunities")
async def get_current_opportunities():
    """Get latest identified opportunities without re-scanning."""
    # Read from cache/database
    pass
```

### 4. Frontend Automation Dashboard

**New Component:** `app/frontend/src/components/AutomationDashboard.tsx`

```typescript
function AutomationDashboard() {
  const [opportunities, setOpportunities] = useState([]);

  useEffect(() => {
    // Poll for new opportunities every 5 minutes
    const interval = setInterval(() => {
      fetch("/api/automation/opportunities")
        .then(res => res.json())
        .then(data => setOpportunities(data.opportunities));
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>This Morning's Opportunities</h2>
      {opportunities.map(opp => (
        <OpportunityCard key={opp.ticker} {...opp} />
      ))}
    </div>
  );
}
```

---

## Testing the Automation

### Manual Test

```bash
# Test the morning scanner without scheduling
python -c "
from src.automation.morning_scanner import UKMorningNewsScanner

scanner = UKMorningNewsScanner()
results = scanner.scan_morning_news()

print('Opportunities:', results['opportunities'])
print('Watch List:', results['watch_list'])
"
```

### API Test

```bash
curl -X POST http://localhost:8000/api/automation/morning-scan
```

---

## Next Steps

- **[4-api-integration.md](./4-api-integration.md)** - Where to plug in UK market data
- **[5-uk-adaptation-guide.md](./5-uk-adaptation-guide.md)** - Complete setup instructions
