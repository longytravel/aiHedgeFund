# UK Market Adaptation - Complete Implementation Guide

**Generated:** 2025-11-16
**Purpose:** Step-by-step guide to adapt the AI hedge fund for British stocks with morning automation

---

## Quick Start Checklist

- [ ] Choose UK data provider and get API key
- [ ] Create UK API integration module
- [ ] Build morning news scanner
- [ ] Set up UK company/ticker mapping
- [ ] Test with sample UK stocks
- [ ] Deploy morning automation scheduler
- [ ] Configure notifications/alerts

**Estimated Time:** 2-4 days (depending on experience)

---

## Phase 1: UK Data Integration (Day 1)

### Step 1: Choose and Setup Data Provider

**Recommended: Financial Modeling Prep**

1. Sign up: https://financialmodelingprep.com/register
2. Get API key from dashboard
3. Subscribe to Professional plan ($29/month) or Enterprise ($59/month)

### Step 2: Create UK API Module

**Create:** `src/tools/api_uk.py`

```python
"""UK Market Data Integration - Financial Modeling Prep"""

import requests
import os
from typing import List
from datetime import datetime
from src.data.cache import get_cache
from src.data.models import Price, CompanyNews, FinancialMetrics

FMP_BASE = "https://financialmodelingprep.com/api/v3"
FMP_KEY = os.getenv("FMP_API_KEY")
_cache = get_cache()

def get_uk_prices(ticker: str, start_date: str, end_date: str) -> List[Price]:
    """Fetch LSE stock prices."""
    cache_key = f"UK_PRICES_{ticker}_{start_date}_{end_date}"

    if cached := _cache.get_prices(cache_key):
        return [Price(**p) for p in cached]

    url = f"{FMP_BASE}/historical-price-full/{ticker}"
    params = {"apikey": FMP_KEY, "from": start_date, "to": end_date}

    response = requests.get(url, params=params)
    data = response.json()

    prices = []
    for item in data.get("historical", []):
        prices.append(Price(
            time=item["date"],
            open=item["open"],
            high=item["high"],
            low=item["low"],
            close=item["close"],
            volume=item["volume"]
        ))

    _cache.set_prices(cache_key, [p.model_dump() for p in prices])
    return prices

def get_uk_financial_metrics(ticker: str, end_date: str) -> List[FinancialMetrics]:
    """Fetch UK stock financial ratios and metrics."""
    url = f"{FMP_BASE}/ratios/{ticker}"
    params = {"apikey": FMP_KEY, "limit": 10}

    response = requests.get(url, params=params)
    data = response.json()

    # Convert FMP format to your FinancialMetrics model
    metrics = []
    for item in data:
        metrics.append(FinancialMetrics(
            # Map FMP fields to your model
            ...
        ))
    return metrics

def get_uk_company_news(ticker: str, end_date: str, limit: int = 100) -> List[CompanyNews]:
    """Fetch news for UK ticker."""
    url = f"{FMP_BASE}/stock_news"
    params = {"tickers": ticker, "apikey": FMP_KEY, "limit": limit}

    response = requests.get(url, params=params)
    news_items = response.json()

    return [CompanyNews(**item) for item in news_items]
```

### Step 3: Update Environment Variables

**Add to `.env`:**

```bash
# UK Market Configuration
MARKET=UK
FMP_API_KEY=your_api_key_here
UK_TIMEZONE=Europe/London

# Optional: Fallback to Yahoo Finance for testing
UK_DATA_PROVIDER=FMP  # or YAHOO for free testing
```

### Step 4: Test UK Data Access

**Create:** `scripts/test_uk_data.py`

```python
from src.tools.api_uk import get_uk_prices, get_uk_company_news

# Test major UK stocks
TEST_TICKERS = ["VOD.L", "BP.L", "HSBC.L", "LLOY.L"]

for ticker in TEST_TICKERS:
    print(f"\nTesting {ticker}...")

    prices = get_uk_prices(ticker, "2024-12-01", "2025-01-15")
    print(f"  ✓ Prices: {len(prices)} records")

    news = get_uk_company_news(ticker, "2025-01-15", limit=10)
    print(f"  ✓ News: {len(news)} articles")

print("\n✅ UK data integration working!")
```

Run: `python scripts/test_uk_data.py`

---

## Phase 2: Morning News Scanner (Day 2)

### Step 1: Create UK Company Mapping Database

**Create:** `src/data/uk_companies.json`

```json
{
  "companies": [
    {
      "name": "Vodafone",
      "ticker": "VOD.L",
      "sector": "Telecommunications",
      "index": "FTSE 100",
      "aliases": ["Vodafone Group", "Vodafone plc"]
    },
    {
      "name": "BP",
      "ticker": "BP.L",
      "sector": "Energy",
      "index": "FTSE 100",
      "aliases": ["British Petroleum", "BP plc"]
    }
    // Add all FTSE 100, FTSE 250 companies
  ]
}
```

**Helper Function:**

```python
# src/utils/uk_ticker_mapper.py
import json

class UKTickerMapper:
    def __init__(self):
        with open("src/data/uk_companies.json") as f:
            self.companies = json.load(f)["companies"]

        # Build search index
        self.name_to_ticker = {}
        for company in self.companies:
            name = company["name"].lower()
            self.name_to_ticker[name] = company["ticker"]
            for alias in company.get("aliases", []):
                self.name_to_ticker[alias.lower()] = company["ticker"]

    def find_ticker(self, company_name: str) -> str | None:
        """Find LSE ticker from company name."""
        return self.name_to_ticker.get(company_name.lower())

    def extract_tickers(self, text: str) -> set[str]:
        """Extract all mentioned UK tickers from text."""
        tickers = set()
        text_lower = text.lower()

        for name, ticker in self.name_to_ticker.items():
            if name in text_lower:
                tickers.add(ticker)

        return tickers
```

### Step 2: Implement Morning News Scanner

**Create:** `src/automation/morning_scanner.py`

```python
"""UK Morning News Scanner - Autonomous Opportunity Detection"""

import os
from datetime import datetime, timedelta
import pytz
from typing import Dict, List
import requests
from src.utils.uk_ticker_mapper import UKTickerMapper
from src.agents.news_sentiment import news_sentiment_agent
from src.utils.llm import call_llm

class UKMorningNewsScanner:
    def __init__(self):
        self.ticker_mapper = UKTickerMapper()
        self.news_api_key = os.getenv("NEWS_API_KEY")

    def scan_morning_news(self, date: str = None) -> Dict:
        """
        Main morning scan - runs at 7:00 AM GMT.

        Returns:
            {
                "scan_date": "2025-01-16",
                "opportunities": ["VOD.L", "BP.L"],  # High confidence
                "watch_list": ["HSBC.L"],           # Medium confidence
                "news_summary": {...}
            }
        """
        if not date:
            uk_tz = pytz.timezone("Europe/London")
            date = datetime.now(uk_tz).strftime("%Y-%m-%d")

        print(f"🔍 Scanning UK morning news for {date}...")

        # 1. Fetch UK business news
        news_articles = self._fetch_uk_news(date)
        print(f"  📰 Found {len(news_articles)} news articles")

        # 2. Extract mentioned UK companies/tickers
        mentioned_tickers = self._extract_tickers_from_news(news_articles)
        print(f"  📊 Mentioned tickers: {len(mentioned_tickers)}")

        # 3. Analyze sentiment for each ticker
        ticker_analysis = self._analyze_ticker_sentiments(
            mentioned_tickers, news_articles
        )

        # 4. Rank and categorize
        opportunities, watch_list = self._categorize_opportunities(ticker_analysis)

        print(f"  🎯 High-confidence opportunities: {len(opportunities)}")
        print(f"  👀 Watch list: {len(watch_list)}")

        return {
            "scan_date": date,
            "opportunities": opportunities,
            "watch_list": watch_list,
            "ticker_analysis": ticker_analysis,
            "news_summary": {
                "total_articles": len(news_articles),
                "tickers_mentioned": len(mentioned_tickers),
            }
        }

    def _fetch_uk_news(self, date: str) -> List[Dict]:
        """Fetch UK business news from NewsAPI.org"""
        # Morning window: 6 AM - 9 AM GMT
        from_time = f"{date}T06:00:00"
        to_time = f"{date}T09:00:00"

        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": self.news_api_key,
            "language": "en",
            "domains": "bbc.co.uk,ft.com,reuters.com,telegraph.co.uk,cityam.com,thisismoney.co.uk",
            "q": "(FTSE OR \"stock market\" OR LSE OR shares OR trading OR \"city news\")",
            "from": from_time,
            "to": to_time,
            "sortBy": "publishedAt",
            "pageSize": 100
        }

        response = requests.get(url, params=params)
        data = response.json()

        return data.get("articles", [])

    def _extract_tickers_from_news(self, articles: List[Dict]) -> set[str]:
        """Extract UK tickers mentioned in news."""
        all_tickers = set()

        for article in articles:
            text = article["title"] + " " + article.get("description", "")
            tickers = self.ticker_mapper.extract_tickers(text)
            all_tickers.update(tickers)

        return all_tickers

    def _analyze_ticker_sentiments(
        self, tickers: set[str], articles: List[Dict]
    ) -> Dict:
        """Analyze sentiment for each ticker using LLM."""
        analysis = {}

        for ticker in tickers:
            # Find articles mentioning this ticker
            relevant_articles = self._filter_articles_for_ticker(
                ticker, articles
            )

            if not relevant_articles:
                continue

            # Analyze sentiment
            sentiment_result = self._analyze_sentiment(
                ticker, relevant_articles
            )

            analysis[ticker] = sentiment_result

        return analysis

    def _filter_articles_for_ticker(
        self, ticker: str, articles: List[Dict]
    ) -> List[Dict]:
        """Get articles relevant to specific ticker."""
        # Get company name from ticker
        company = self.ticker_mapper.get_company_name(ticker)

        relevant = []
        for article in articles:
            text = article["title"] + " " + article.get("description", "")
            if company.lower() in text.lower():
                relevant.append(article)

        return relevant

    def _analyze_sentiment(
        self, ticker: str, articles: List[Dict]
    ) -> Dict:
        """Analyze overall sentiment from articles."""
        # Similar to news_sentiment_agent logic
        sentiments = []
        confidences = []

        for article in articles[:5]:  # Analyze top 5
            prompt = f"""
            Analyze sentiment for {ticker}:
            Headline: {article['title']}

            Classify as: positive, negative, or neutral
            Confidence: 0-100
            """

            # Use existing LLM infrastructure
            result = self._classify_sentiment(prompt)
            sentiments.append(result["sentiment"])
            confidences.append(result["confidence"])

        # Aggregate
        bullish_count = sentiments.count("positive")
        bearish_count = sentiments.count("negative")

        overall_signal = "bullish" if bullish_count > bearish_count else (
            "bearish" if bearish_count > bullish_count else "neutral"
        )

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        return {
            "signal": overall_signal,
            "confidence": avg_confidence,
            "article_count": len(articles),
            "bullish_count": bullish_count,
            "bearish_count": bearish_count
        }

    def _categorize_opportunities(
        self, ticker_analysis: Dict
    ) -> tuple[List[str], List[str]]:
        """Separate high-confidence opportunities from watch list."""
        opportunities = []
        watch_list = []

        for ticker, analysis in ticker_analysis.items():
            confidence = analysis["confidence"]
            article_count = analysis["article_count"]
            signal = analysis["signal"]

            # High-confidence criteria
            if (
                confidence > 70 and
                article_count >= 3 and
                signal in ["bullish", "bearish"]
            ):
                opportunities.append(ticker)
            elif confidence > 50 and article_count >= 2:
                watch_list.append(ticker)

        return opportunities, watch_list
```

### Step 3: Test Morning Scanner

```python
# scripts/test_morning_scanner.py
from src.automation.morning_scanner import UKMorningNewsScanner

scanner = UKMorningNewsScanner()
results = scanner.scan_morning_news("2025-01-15")

print("\n" + "="*60)
print(f"UK MORNING SCAN RESULTS - {results['scan_date']}")
print("="*60)

print(f"\n📰 News Summary:")
print(f"   Total articles: {results['news_summary']['total_articles']}")
print(f"   Tickers mentioned: {results['news_summary']['tickers_mentioned']}")

if results["opportunities"]:
    print(f"\n🎯 HIGH-CONFIDENCE OPPORTUNITIES:")
    for ticker in results["opportunities"]:
        analysis = results["ticker_analysis"][ticker]
        print(f"   {ticker}: {analysis['signal']} ({analysis['confidence']:.1f}% confidence)")

if results["watch_list"]:
    print(f"\n👀 WATCH LIST:")
    for ticker in results["watch_list"]:
        print(f"   {ticker}")
```

---

## Phase 3: Automation Integration (Day 3)

### Step 1: Modify Main Entry Point

**Update:** `src/main.py`

```python
import os
from src.automation.morning_scanner import UKMorningNewsScanner

def main():
    """Main entry point - supports both manual and automated modes."""

    # Check for automation mode
    if os.getenv("AUTOMATED_MODE") == "true":
        print("🤖 Running in AUTOMATED MODE")
        return run_automated_morning_scan()
    else:
        print("👤 Running in MANUAL MODE")
        return run_manual_mode()

def run_automated_morning_scan():
    """Automated morning workflow - no user input required."""
    # 1. Scan news
    scanner = UKMorningNewsScanner()
    scan_results = scanner.scan_morning_news()

    # 2. Get opportunities
    tickers = scan_results["opportunities"]

    if not tickers:
        print("ℹ️  No opportunities identified today.")
        send_notification("No UK market opportunities today")
        return None

    print(f"📊 Analyzing {len(tickers)} opportunities: {tickers}")

    # 3. Run full hedge fund analysis
    result = run_hedge_fund(
        tickers=tickers,
        start_date=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        end_date=datetime.now().strftime("%Y-%m-%d"),
        portfolio=initialize_portfolio(tickers),
        selected_analysts=None,  # Use all analysts
        model_name="gpt-4o",
        model_provider="OpenAI"
    )

    # 4. Notify user
    send_notification(result)

    return result

def run_manual_mode():
    """Original manual mode with user input."""
    inputs = parse_cli_inputs(require_tickers=True)
    tickers = inputs.tickers
    # ... rest of original code

if __name__ == "__main__":
    main()
```

### Step 2: Create Scheduler

**Create:** `src/automation/scheduler.py`

```python
"""UK Morning Market Scheduler"""

import schedule
import time
import pytz
from datetime import datetime
from src.main import run_automated_morning_scan

def morning_scan_job():
    """Job to run every weekday morning at 7:00 AM GMT."""
    uk_tz = pytz.timezone("Europe/London")
    current_time = datetime.now(uk_tz)

    # Only run on weekdays
    if current_time.weekday() >= 5:  # Saturday = 5, Sunday = 6
        print(f"⏭️  Skipping - Weekend")
        return

    print(f"⏰ Running morning scan at {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    run_automated_morning_scan()

# Schedule for 7:00 AM GMT (before UK market opens at 8:00 AM)
schedule.every().day.at("07:00").do(morning_scan_job)

print("🚀 UK Morning Scanner Scheduled")
print("   ⏰ Runs: Every weekday at 7:00 AM GMT")
print("   🎯 Action: Scans news → Identifies opportunities → Analyzes")

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
```

Run with: `python -m src.automation.scheduler`

### Step 3: Add Notification System

**Create:** `src/automation/notifications.py`

```python
"""Notification system for trading opportunities."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(subject: str, body: str):
    """Send email notification."""
    sender = os.getenv("NOTIFICATION_EMAIL")
    recipient = os.getenv("USER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

def send_notification(results: dict):
    """Format and send trading opportunity notification."""
    if not results:
        send_email_notification(
            "UK Morning Scan - No Opportunities",
            "<p>No high-confidence opportunities identified today.</p>"
        )
        return

    # Build HTML email
    html = f"""
    <h2>🎯 UK Morning Market Opportunities</h2>
    <p><strong>Date:</strong> {datetime.now().strftime("%Y-%m-%d")}</p>

    <h3>Trading Decisions:</h3>
    <table border="1">
        <tr>
            <th>Ticker</th>
            <th>Action</th>
            <th>Quantity</th>
            <th>Confidence</th>
        </tr>
    """

    for ticker, decision in results["decisions"].items():
        html += f"""
        <tr>
            <td>{ticker}</td>
            <td>{decision['action']}</td>
            <td>{decision['quantity']}</td>
            <td>{decision['confidence']}%</td>
        </tr>
        """

    html += "</table>"

    send_email_notification("UK Market Opportunities", html)
```

---

## Phase 4: Deployment (Day 4)

### Option 1: Run on Local Machine

```bash
# Keep running 24/7
nohup python -m src.automation.scheduler > scheduler.log 2>&1 &
```

### Option 2: Deploy to Cloud

**AWS EC2 / DigitalOcean Droplet:**

1. Create Ubuntu server
2. Install Python dependencies
3. Set up systemd service
4. Configure environment variables

**Systemd Service** (`/etc/systemd/system/uk-hedge-fund.service`):

```ini
[Unit]
Description=UK Morning Hedge Fund Scanner
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-hedge-fund
ExecStart=/home/ubuntu/ai-hedge-fund/venv/bin/python -m src.automation.scheduler
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable uk-hedge-fund
sudo systemctl start uk-hedge-fund
```

---

## Testing & Validation

### Full Integration Test

```python
# scripts/full_uk_test.py

# Test complete flow
from src.automation.morning_scanner import UKMorningNewsScanner
from src.main import run_hedge_fund

# 1. Scan news
scanner = UKMorningNewsScanner()
results = scanner.scan_morning_news()

# 2. Run analysis
if results["opportunities"]:
    hedge_fund_result = run_hedge_fund(
        tickers=results["opportunities"],
        ...
    )

    print("✅ Full UK integration test passed!")
    print(f"   Opportunities: {results['opportunities']}")
    print(f"   Decisions: {hedge_fund_result['decisions']}")
```

---

## Next Steps

You're now ready to run an autonomous UK stock trading system!

- Monitor `scheduler.log` for daily scans
- Review opportunities via email/notifications
- Refine ticker mapping as needed
- Add more UK news sources over time

**See:** [index.md](./index.md) for full documentation index
