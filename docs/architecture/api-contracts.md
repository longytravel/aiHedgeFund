# API Contracts

### Core API Endpoints

**Base URL:** `http://localhost:8000/api/v1`

**Authentication:** None for MVP (future: JWT tokens in `Authorization: Bearer {token}` header)

#### Analysis Endpoints

```yaml
POST /analysis/run
Description: Trigger on-demand analysis for specific stocks
Request Body:
  {
    "tickers": ["VOD.L", "BP.L"],    # Array of LSE tickers
    "agents": ["all"] | ["value_investor", "technical_analyst"],  # Optional: specific agents
    "priority": "normal" | "high"     # Optional: queue priority
  }
Response (202 Accepted):
  {
    "success": true,
    "data": {
      "job_id": "uuid-here",
      "status": "queued",
      "estimated_completion": "2025-11-22T07:15:00Z"
    },
    "timestamp": "2025-11-22T07:00:00Z"
  }

GET /analysis/{job_id}
Description: Get analysis job status and results
Response (200 OK):
  {
    "success": true,
    "data": {
      "job_id": "uuid-here",
      "status": "completed",  # "queued" | "running" | "completed" | "failed"
      "results": [
        {
          "stock_ticker": "VOD.L",
          "recommendation": "BUY",
          "convergence_score": 75,
          "agent_results": [
            {
              "agent_id": "value_investor",
              "score": 85,
              "confidence": "HIGH",
              "reasoning": "Trading at 0.6× book value with strong FCF..."
            }
          ]
        }
      ],
      "completed_at": "2025-11-22T07:10:00Z"
    },
    "timestamp": "2025-11-22T07:10:05Z"
  }
```

#### Portfolio Endpoints

```yaml
GET /portfolio
Description: Get current portfolio positions (Tier 1)
Response (200 OK):
  {
    "success": true,
    "data": {
      "positions": [
        {
          "id": "uuid",
          "stock_ticker": "VOD.L",
          "stock_name": "Vodafone Group PLC",
          "quantity": 1000,
          "entry_price": 0.85,
          "current_price": 0.92,
          "unrealized_pnl": 70.00,
          "unrealized_pnl_pct": 8.24,
          "stop_loss": 0.75,
          "target_price": 1.10,
          "entry_date": "2025-11-10"
        }
      ],
      "total_value": 15420.00,
      "total_pnl": 1240.00,
      "total_pnl_pct": 8.74
    },
    "timestamp": "2025-11-22T07:00:00Z"
  }

POST /portfolio/positions
Description: Add new position (after trade execution)
Request Body:
  {
    "stock_ticker": "BP.L",
    "quantity": 500,
    "entry_price": 4.50,
    "stop_loss": 4.00,
    "target_price": 5.50
  }
Response (201 Created):
  {
    "success": true,
    "data": {
      "id": "uuid",
      "stock_ticker": "BP.L",
      ...
    }
  }
```

#### Watchlist Endpoints

```yaml
GET /watchlist
Description: Get active watchlist (Tier 2)
Response (200 OK):
  {
    "success": true,
    "data": {
      "entries": [
        {
          "id": "uuid",
          "stock_ticker": "LLOY.L",
          "stock_name": "Lloyds Banking Group",
          "reason": "Good value but waiting for sector rotation to favor financials",
          "triggers": [
            {"type": "sector", "condition": "sector_favored"},
            {"type": "price", "condition": "<=", "value": 0.50}
          ],
          "current_price": 0.55,
          "added_date": "2025-11-15",
          "status": "ACTIVE"
        }
      ]
    }
  }

POST /watchlist
Description: Add stock to watchlist
Request Body:
  {
    "stock_ticker": "HSBC.L",
    "reason": "Strong fundamentals but needs macro tailwind",
    "triggers": [
      {"type": "macro", "condition": "regime_change", "value": "expansion"},
      {"type": "price", "condition": "<=", "value": 6.00}
    ]
  }
Response (201 Created): { ... }

PUT /watchlist/{id}/triggers
Description: Update watchlist triggers
Request Body:
  {
    "triggers": [
      {"type": "price", "condition": "<=", "value": 5.50}
    ]
  }
Response (200 OK): { ... }

DELETE /watchlist/{id}
Description: Remove from watchlist
Response (204 No Content)
```

#### Report Endpoints

```yaml
GET /reports/daily
Description: Get latest daily report
Response (200 OK):
  {
    "success": true,
    "data": {
      "report_date": "2025-11-22",
      "generated_at": "2025-11-22T06:30:00Z",
      "sections": {
        "new_opportunities": [
          {
            "stock_ticker": "VOD.L",
            "stock_name": "Vodafone Group PLC",
            "recommendation": "BUY",
            "convergence_score": 75,
            "target_price": 1.10,
            "stop_loss": 0.75,
            "position_size_pct": 5,
            "bull_case": "Trading at deep discount, new contract wins...",
            "bear_case": "High debt, competitive pressure...",
            "signals": ["NEW_CATALYST", "INSIDER_CONVICTION", "VALUE_ASSESSMENT"]
          }
        ],
        "watchlist_alerts": [
          {
            "stock_ticker": "BP.L",
            "trigger_type": "price",
            "revalidation_result": "BUY",
            "reason": "Hit target price of £4.50, fundamentals still strong"
          }
        ],
        "portfolio_updates": [
          {
            "stock_ticker": "LLOY.L",
            "action": "SELL",
            "reason": "Hit target price, take profits"
          }
        ],
        "market_context": {
          "macro_regime": "expansion",
          "favored_sectors": ["Technology", "Industrials"],
          "disfavored_sectors": ["Utilities", "REITs"]
        }
      }
    }
  }

GET /reports/{date}
Description: Get historical report by date (YYYY-MM-DD)
Response (200 OK): { ... }
```

#### Trade Endpoints

```yaml
POST /trades
Description: Log executed trade
Request Body:
  {
    "stock_ticker": "VOD.L",
    "action": "BUY",
    "quantity": 1000,
    "price": 0.85,
    "commission": 9.99,
    "notes": "Morning report recommendation, strong value setup"
  }
Response (201 Created): { ... }

GET /trades/history
Description: Get trade history with P&L
Query Params: ?start_date=2025-11-01&end_date=2025-11-22
Response (200 OK):
  {
    "success": true,
    "data": {
      "trades": [ ... ],
      "summary": {
        "total_trades": 15,
        "winning_trades": 9,
        "losing_trades": 6,
        "win_rate": 60.0,
        "total_pnl": 1240.00,
        "avg_winner": 182.50,
        "avg_loser": -45.20
      }
    }
  }
```

---
