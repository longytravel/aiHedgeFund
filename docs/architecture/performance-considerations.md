# Performance Considerations

**Cost Optimization:**
- ✅ Batch processing overnight (GPT-4o batch API = 50% discount vs. real-time)
- ✅ Signal convergence filtering (only deep-analyze 61+ score stocks = 10-15/day vs. 600+)
- ✅ Agent enable/disable (turn off expensive agents during testing)
- ✅ Data caching (24-hour cache for fundamentals, reducing API calls)
- ✅ LLM provider fallback (use cheapest available provider)

**Performance Targets:**
- Discovery layer: < 30 min for full FTSE scan (7 agents × 600 stocks)
- Deep analysis: < 15 min for 15 stocks (8 agents × 15 stocks in parallel)
- API response time: < 200ms for portfolio/watchlist endpoints
- Report generation: < 2 min (compile all sections)
- Total overnight batch: < 6 hours (1am-7am window)

**Scalability:**
- PostgreSQL 18.1 connection pooling (SQLAlchemy async engine)
- LangGraph parallel agent execution (discovery + analysis layers)
- FastAPI async endpoints (handle concurrent requests)
- Frontend lazy loading (load report sections on-demand)

---
