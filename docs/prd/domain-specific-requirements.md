# Domain-Specific Requirements

**Fintech (UK Stock Trading) - High Complexity Domain**

1. **UK Market Data Requirements**
   - LSE real-time/delayed price data (FTSE 100, 250, Small Cap, AIM)
   - Ticker format support: VOD.L, BP.L, HSBC.L (Financial Modeling Prep format)
   - UK-specific financial metrics (IFRS accounting standards, not US GAAP)
   - Insider trading data: UK director dealings via Companies House RNS filings
   - Corporate actions: Dividends (pence vs. pounds handling), buybacks, rights issues
   - UK regulatory filings: Annual reports, interim results, trading updates

2. **UK Regulatory Considerations**
   - **Phase 1 (Personal Use):** Minimal regulatory burden, personal investment decisions
   - **Phase 3 (Hedge Fund):** FCA authorization required, MIFID II compliance, audit trail requirements
   - Data Protection: GDPR compliance for any user data storage
   - Market Abuse Regulation (MAR): No insider information usage, audit all data sources
   - Transaction Reporting: Prepare for potential MiFID II/MiFIR requirements if scaling

3. **UK Market Specifics**
   - Market Hours: 8:00 AM - 4:30 PM GMT (earlier close than US)
   - Currency: GBP (pounds sterling), some stocks quoted in pence (divide by 100)
   - Settlement: T+2 (trade date plus 2 business days)
   - Stamp Duty: 0.5% tax on UK stock purchases (factor into cost calculations)
   - ISA/SIPP accounts: Tax-advantaged wrappers (may influence strategy)

4. **Cost Structure Constraints**
   - LLM API costs: GPT-4o at ~$2.50/1M input tokens, $10/1M output tokens
   - Data API costs: Financial Modeling Prep $29-59/month, NewsAPI $449/month
   - Broker costs: Commission + spread + 0.5% stamp duty on buys
   - Target: Keep total operating cost ≤ £200/month Phase 1 (preserve capital for trading)

5. **Risk Management Requirements**
   - Position Sizing: Max 5-10% of portfolio per position (diversification)
   - Stop Losses: Automatic exit triggers (8-12% typical, adjustable per risk level)
   - Max Drawdown: Circuit breaker if portfolio down 20% from peak
   - Exposure Limits: Max total invested 60-80% (maintain cash buffer)
   - Concentration Risk: No more than 20% in single sector

6. **Audit & Compliance Trail**
   - Log all agent decisions with timestamps and reasoning
   - Track data sources for each decision (which news articles, which prices, which reports)
   - Record trade approvals/rejections with user input
   - Store performance history for learning and potential regulatory review
   - Maintain version history of agent prompts and model changes

7. **Data Quality & Accuracy**
   - Price data validation: Reject outliers, check for corporate actions
   - News source verification: Only use reputable UK financial news (BBC, FT, Reuters, City AM)
   - Financial data reconciliation: Cross-check metrics across multiple sources where possible
   - Error handling: Graceful degradation if API unavailable (use cached data, skip analysis, alert user)

This section shapes all functional and non-functional requirements below.

---
