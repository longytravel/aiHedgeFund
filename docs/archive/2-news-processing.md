# News Processing & Sentiment Analysis

**Generated:** 2025-11-16
**Purpose:** Understand how news is processed - CRITICAL for your morning automation goal

---

## Table of Contents

1. [Current News Processing System](#current-news-processing-system)
2. [News Sentiment Agent Deep Dive](#news-sentiment-agent-deep-dive)
3. [How to Adapt for UK Morning News](#how-to-adapt-for-uk-morning-news)
4. [Automation Strategy](#automation-strategy)

---

## Current News Processing System

### How It Works Now

**File:** `src/agents/news_sentiment.py`

The news sentiment agent:
1. ✅ Fetches company news from API (up to 100 articles)
2. ✅ Analyzes recent headlines using LLM (5 most recent without sentiment)
3. ✅ Classifies sentiment: positive/negative/neutral
4. ✅ Calculates confidence score
5. ✅ Aggregates to overall signal: bullish/bearish/neutral

### Current Workflow

```python
def news_sentiment_agent(state: AgentState):
    tickers = state["data"]["tickers"]  # ⚠️ USER PROVIDES THESE MANUALLY
    end_date = state["data"]["end_date"]

    for ticker in tickers:
        # 1. Fetch news
        company_news = get_company_news(
            ticker=ticker,
            end_date=end_date,
            limit=100,
            api_key=api_key
        )

        # 2. Analyze 10 most recent articles
        recent_articles = company_news[:10]
        articles_without_sentiment = [
            news for news in recent_articles
            if news.sentiment is None
        ]

        # 3. LLM analyzes first 5 articles without sentiment
        articles_to_analyze = articles_without_sentiment[:5]
        for news in articles_to_analyze:
            prompt = f"""
            Analyze the sentiment of: {news.title}
            Stock: {ticker}
            Determine: 'positive', 'negative', or 'neutral'
            Confidence: 0-100
            """
            response = call_llm(prompt, Sentiment, state=state)
            news.sentiment = response.sentiment

        # 4. Aggregate sentiment across all articles
        bullish_count = count("positive")
        bearish_count = count("negative")
        neutral_count = count("neutral")

        # 5. Determine overall signal
        if bullish_count > bearish_count:
            signal = "bullish"
        elif bearish_count > bullish_count:
            signal = "bearish"
        else:
            signal = "neutral"

        # 6. Calculate confidence (weighted by LLM confidence scores)
        confidence = calculate_confidence(...)
```

---

## News Sentiment Agent Deep Dive

### Input Data Structure

**API Response:** `CompanyNews` objects from `financialdatasets.ai`

```python
{
    "title": "Apple Announces Record Q4 Earnings",
    "date": "2025-01-15T09:30:00Z",
    "url": "https://...",
    "source": "Reuters",
    "sentiment": "positive",  # Pre-classified (if available)
    "ticker": "AAPL"
}
```

### LLM Sentiment Classification

**Prompt Template:**

```python
prompt = (
    f"Please analyze the sentiment of the following news headline "
    f"with the following context: "
    f"The stock is {ticker}. "
    f"Determine if sentiment is 'positive', 'negative', or 'neutral' "
    f"for the stock {ticker} only. "
    f"Also provide a confidence score from 0 to 100. "
    f"Respond in JSON format.\n\n"
    f"Headline: {news.title}"
)
```

**Response Model:**

```python
class Sentiment(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: int  # 0-100
```

### Confidence Score Calculation

```python
def _calculate_confidence_score(
    sentiment_confidences: dict,  # LLM confidence scores
    overall_signal: str,
    bullish_signals: int,
    bearish_signals: int,
    total_signals: int
) -> float:
    """
    Weighted confidence:
    - 70% from LLM confidence scores (average of matching articles)
    - 30% from signal proportion (majority strength)
    """
    if sentiment_confidences:
        avg_llm_confidence = sum(llm_confidences) / len(llm_confidences)
        signal_proportion = (max(bullish, bearish) / total) * 100
        return 0.7 * avg_llm_confidence + 0.3 * signal_proportion
    else:
        # Fallback: pure proportion
        return (max(bullish, bearish) / total) * 100
```

### Output Structure

```python
{
    "AAPL": {
        "signal": "bullish",
        "confidence": 75.2,
        "reasoning": {
            "news_sentiment": {
                "signal": "bullish",
                "confidence": 75.2,
                "metrics": {
                    "total_articles": 100,
                    "bullish_articles": 12,
                    "bearish_articles": 3,
                    "neutral_articles": 85,
                    "articles_classified_by_llm": 5
                }
            }
        }
    }
}
```

---

## How to Adapt for UK Morning News

### Your Goal

> "I want it to read all the news in a morning, then work out if opportunities are being created"

### Required Changes

#### 1. **Add UK News Sources**

**Current:** Uses `financialdatasets.ai` (US-focused)

**Needed:** UK-specific news aggregation

**Options:**

**Option A: News API Services**
```python
# NewsAPI.org (supports UK sources)
def get_uk_morning_news(date: str, api_key: str):
    """Fetch UK business news from multiple sources."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": api_key,
        "language": "en",
        "domains": "bbc.co.uk,ft.com,reuters.com,cityam.com",
        "q": "FTSE OR stocks OR LSE OR trading",
        "from": f"{date}T06:00:00",  # UK market open prep
        "to": f"{date}T09:00:00",    # After market open
        "sortBy": "publishedAt"
    }
    response = requests.get(url, params=params)
    return response.json()["articles"]
```

**Option B: RSS Feeds**
```python
import feedparser

UK_NEWS_FEEDS = [
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://www.ft.com/rss/companies/uk",
    "https://www.reuters.com/finance/markets/europe",
    "https://www.cityam.com/feed/",
]

def get_uk_rss_news(feeds: list[str]) -> list[dict]:
    """Aggregate news from UK RSS feeds."""
    all_articles = []
    for feed_url in feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            all_articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "summary": entry.summary
            })
    return all_articles
```

**Option C: Financial Modeling Prep (UK Stock Data)**
```python
# Supports LSE stocks
def get_uk_stock_news(ticker: str, api_key: str):
    """Get news for UK ticker (e.g., 'VOD.L')."""
    url = f"https://financialmodelingprep.com/api/v3/stock_news"
    params = {
        "tickers": ticker,
        "apikey": api_key,
        "limit": 100
    }
    response = requests.get(url, params=params)
    return response.json()
```

#### 2. **Create Morning News Scanner**

**New File:** `src/agents/uk_morning_scanner.py`

```python
from datetime import datetime, timedelta
import pytz

class UKMorningNewsScanner:
    """
    Scans UK news every morning and identifies opportunities.
    Runs at 7:00 AM GMT (before market open at 8:00 AM).
    """

    def scan_morning_news(self, scan_date: str = None):
        """
        Main morning scan function.

        Returns:
            dict: {
                "opportunities": [list of tickers with strong signals],
                "watch_list": [tickers to monitor],
                "news_summary": {...}
            }
        """
        if not scan_date:
            # Default to today (UK timezone)
            uk_tz = pytz.timezone("Europe/London")
            scan_date = datetime.now(uk_tz).strftime("%Y-%m-%d")

        # 1. Fetch UK market news (6-9 AM window)
        morning_news = self._fetch_uk_morning_news(scan_date)

        # 2. Extract mentioned tickers
        mentioned_tickers = self._extract_uk_tickers(morning_news)

        # 3. Analyze sentiment for each ticker
        ticker_sentiments = {}
        for ticker in mentioned_tickers:
            sentiment = self._analyze_ticker_sentiment(
                ticker, morning_news
            )
            ticker_sentiments[ticker] = sentiment

        # 4. Identify opportunities (strong signals)
        opportunities = self._identify_opportunities(ticker_sentiments)

        return {
            "scan_date": scan_date,
            "opportunities": opportunities,
            "watch_list": [
                t for t, s in ticker_sentiments.items()
                if s["confidence"] > 50 and t not in opportunities
            ],
            "news_summary": {
                "total_articles": len(morning_news),
                "tickers_mentioned": len(mentioned_tickers),
                "sentiment_breakdown": self._summarize_sentiment(ticker_sentiments)
            }
        }

    def _fetch_uk_morning_news(self, date: str) -> list[dict]:
        """Fetch news from UK sources for given date morning."""
        # Implement using NewsAPI or RSS feeds
        pass

    def _extract_uk_tickers(self, articles: list[dict]) -> set[str]:
        """
        Extract UK stock tickers from news articles.

        Uses NER (Named Entity Recognition) or keyword matching:
        - Company names → LSE ticker mapping
        - Direct ticker mentions
        """
        tickers = set()

        # Example: Simple keyword matching
        UK_COMPANY_MAP = {
            "Vodafone": "VOD.L",
            "BP": "BP.L",
            "HSBC": "HSBC.L",
            "Unilever": "ULVR.L",
            # ... add all FTSE 100/250 companies
        }

        for article in articles:
            text = article["title"] + " " + article.get("summary", "")
            for company, ticker in UK_COMPANY_MAP.items():
                if company.lower() in text.lower():
                    tickers.add(ticker)

        return tickers

    def _analyze_ticker_sentiment(
        self, ticker: str, news: list[dict]
    ) -> dict:
        """Analyze sentiment for specific ticker from news articles."""
        relevant_articles = [
            article for article in news
            if ticker in article.get("mentioned_tickers", [])
        ]

        # Use same LLM sentiment classification as current system
        # ... (reuse news_sentiment.py logic)

        return {
            "signal": "bullish",  # or bearish/neutral
            "confidence": 75.0,
            "article_count": len(relevant_articles),
            "reasoning": "..."
        }

    def _identify_opportunities(
        self, ticker_sentiments: dict
    ) -> list[str]:
        """
        Identify high-confidence trading opportunities.

        Criteria:
        - Confidence > 70%
        - Strong bullish or bearish signal
        - Multiple article confirmations
        """
        opportunities = []
        for ticker, sentiment in ticker_sentiments.items():
            if (
                sentiment["confidence"] > 70
                and sentiment["signal"] in ["bullish", "bearish"]
                and sentiment["article_count"] >= 3
            ):
                opportunities.append(ticker)
        return opportunities
```

#### 3. **Schedule Morning Automation**

**New File:** `src/automation/morning_scheduler.py`

```python
import schedule
import time
from datetime import datetime
import pytz

def run_morning_scan():
    """Run the morning news scan and identify opportunities."""
    scanner = UKMorningNewsScanner()
    results = scanner.scan_morning_news()

    print(f"\n{'='*50}")
    print(f"UK MORNING MARKET SCAN - {results['scan_date']}")
    print(f"{'='*50}\n")

    print(f"📰 Total Articles Analyzed: {results['news_summary']['total_articles']}")
    print(f"📊 Tickers Mentioned: {results['news_summary']['tickers_mentioned']}\n")

    if results['opportunities']:
        print(f"🎯 HIGH-CONFIDENCE OPPORTUNITIES:")
        for ticker in results['opportunities']:
            print(f"   • {ticker}")
    else:
        print("⚠️  No high-confidence opportunities identified.")

    if results['watch_list']:
        print(f"\n👀 WATCH LIST:")
        for ticker in results['watch_list']:
            print(f"   • {ticker}")

    # Optionally: Run full hedge fund analysis on opportunities
    if results['opportunities']:
        run_hedge_fund_analysis(results['opportunities'])

def run_hedge_fund_analysis(tickers: list[str]):
    """Run full multi-agent analysis on identified tickers."""
    from src.main import run_hedge_fund
    from datetime import datetime

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    portfolio = initialize_portfolio(tickers)

    result = run_hedge_fund(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        portfolio=portfolio,
        selected_analysts=None,  # Use all analysts
        model_name="gpt-4o",
        model_provider="OpenAI"
    )

    # Process and execute trading decisions
    print("\n📈 TRADING DECISIONS:")
    for ticker, decision in result["decisions"].items():
        print(f"{ticker}: {decision}")

# Schedule the morning scan
uk_tz = pytz.timezone("Europe/London")
schedule.every().day.at("07:00", uk_tz).do(run_morning_scan)

print("🤖 UK Morning Scanner Scheduled - Running at 7:00 AM GMT daily")

# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

---

## Automation Strategy

### Recommended Approach

**Phase 1: Morning News Aggregation**
1. Deploy morning scanner (7:00 AM GMT)
2. Fetch news from UK sources
3. Extract mentioned tickers
4. Rank by sentiment + article count

**Phase 2: Automated Analysis**
1. Top opportunities → Full agent analysis
2. Risk management evaluation
3. Generate trading signals

**Phase 3: Execution** (Your Choice)
1. **Manual Review:** Email/notify you of opportunities
2. **Semi-Automated:** Generate orders, await approval
3. **Fully Automated:** Execute trades directly (requires broker API)

### Implementation Checklist

- [ ] Choose UK news data source (NewsAPI, RSS, or FMP)
- [ ] Create UK company → ticker mapping database
- [ ] Implement `UKMorningNewsScanner` class
- [ ] Set up scheduler (schedule library or cron)
- [ ] Add notification system (email, Telegram, etc.)
- [ ] Test with historical UK news data
- [ ] Deploy to always-on server (AWS, DigitalOcean, etc.)

---

## Next Steps

- **[3-current-workflow.md](./3-current-workflow.md)** - See how tickers are currently selected manually
- **[4-api-integration.md](./4-api-integration.md)** - Where to plug in UK data APIs
- **[5-uk-adaptation-guide.md](./5-uk-adaptation-guide.md)** - Complete step-by-step UK setup
