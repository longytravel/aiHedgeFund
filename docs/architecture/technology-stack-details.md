# Technology Stack Details

### Core Technologies

**Backend Stack:**
- **Python 3.14** - Latest stable (Oct 2025), free-threaded mode, JIT compiler for performance
- **FastAPI 0.121.3** - Async web framework, auto OpenAPI docs, Pydantic integration
- **LangGraph 1.0.5** - Durable agent orchestration, no breaking changes until 2.0
- **LangChain 1.0** - Multi-provider LLM abstraction (OpenAI, Anthropic, Google)
- **PostgreSQL 18.1** - 3× I/O performance gains, uuidv7() for efficient indexing
- **SQLAlchemy 2.x** - Async ORM, type hints, Alembic migrations
- **Pydantic 2.x** - Runtime validation, serialization (FastAPI native)

**Frontend Stack:**
- **React 19** - Latest stable, compiler improvements, concurrent rendering
- **TypeScript 5.x** - Type safety, IntelliSense, catch errors at compile-time
- **Vite 6** - Fastest dev server (HMR), optimized production builds
- **TanStack Query** - Server state management, caching, optimistic updates
- **TailwindCSS** - Utility-first styling (optional, recommended for rapid UI dev)

**Data & Integration:**
- **httpx** - Async HTTP client for API calls (connection pooling, retries)
- **schedule** - Python job scheduling for overnight batch processing
- **EODHD API** - Fundamentals, historical data, earnings, macro indicators
- **CityFALCON API** - UK RNS feeds, director dealings, sentiment
- **IBKR API** - Real-time quotes at point of trade execution

### Integration Points

**LangGraph Agent Network:**
```python
# StateGraph with parallel discovery, sequential decision
from langgraph.graph import StateGraph
from src.graph.state import AgentState

workflow = StateGraph(AgentState)

# Discovery Layer (parallel)
workflow.add_node("news_scanner", news_scanner_node)
workflow.add_node("insider_trading", insider_trading_node)
workflow.add_node("volume_price", volume_price_node)
workflow.add_node("fundamental_screener", fundamental_screener_node)

# Macro/Sector Context (parallel)
workflow.add_node("macro_economist", macro_economist_node)
workflow.add_node("sector_rotation", sector_rotation_node)

# Signal Aggregation (sequential after discovery)
workflow.add_node("aggregate_signals", signal_aggregation_node)

# Analysis Layer (parallel, only for high-scoring stocks)
workflow.add_node("value_investor", value_investor_node)
workflow.add_node("growth_investor", growth_investor_node)
# ... 6 more analysis agents

# Decision Layer (sequential)
workflow.add_node("risk_manager", risk_manager_node)
workflow.add_node("portfolio_manager", portfolio_manager_node)

# Edges (parallel fan-out, conditional routing)
workflow.add_edge("start", ["news_scanner", "insider_trading", "volume_price", "fundamental_screener"])
workflow.add_conditional_edges("aggregate_signals", route_to_analysis)  # Only if score > 60
workflow.add_edge("portfolio_manager", "end")
```

**Signal Bus Architecture:**
```python
# Central message bus for agent communication
class SignalBus:
    _subscribers: Dict[str, List[Callable]] = {}

    @classmethod
    def publish(cls, signal: Signal):
        """Broadcast signal to all subscribers"""
        signal_type = signal.type
        for callback in cls._subscribers.get(signal_type, []):
            callback(signal)

    @classmethod
    def subscribe(cls, signal_types: List[str], callback: Callable):
        """Register listener for specific signal types"""
        for signal_type in signal_types:
            cls._subscribers.setdefault(signal_type, []).append(callback)

# Agent usage
class NewsScanner(BaseAgent):
    def analyze(self, data):
        # Perform news analysis
        catalyst = detect_catalyst(data)

        # Broadcast discovery
        SignalBus.publish(Signal(
            type="NEW_CATALYST",
            stock="VOD.L",
            data=catalyst,
            strength=15,
            timestamp=datetime.now(UTC)
        ))
```

**API Response Structure (Standardized):**
```typescript
// Success response
{
  "success": true,
  "data": { ... },
  "timestamp": "2025-11-22T07:00:00Z"
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid ticker format",
    "details": { "ticker": "Must match pattern: [A-Z]{2,4}\\.L" }
  },
  "timestamp": "2025-11-22T07:00:05Z"
}
```

---
