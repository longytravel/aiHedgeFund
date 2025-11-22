# Development Environment

### Prerequisites

**Required:**
- Python 3.14+ (latest stable)
- Node.js 20.19+ (for Vite 6)
- PostgreSQL 18.1+ (local or Docker)
- Git

**API Keys Needed:**
- EODHD All-In-One (£85/month) - https://eodhd.com/
- CityFALCON (£30/month) - https://www.cityfalcon.com/
- IBKR API (free with account) - https://www.interactivebrokers.com/
- OpenAI API (GPT-4o) - https://platform.openai.com/
- Anthropic API (Claude, optional fallback) - https://www.anthropic.com/
- Google AI API (Gemini, optional fallback) - https://ai.google.dev/

### Setup Commands

```bash
# 1. Clone repository
git clone <repo-url>
cd AIHedgeFund

# 2. Backend setup
cd ai-hedge-fund
python3.14 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Database setup
createdb aihedgefund  # Or use Docker: docker-compose up -d db
alembic upgrade head  # Run migrations
python scripts/seed_data.py  # Load UK ticker mapping

# 4. Environment configuration
cp .env.example .env
# Edit .env with your API keys

# 5. Frontend setup
cd app/frontend
npm install

# 6. Run development servers
# Terminal 1: Backend
cd ai-hedge-fund
fastapi dev src/main.py

# Terminal 2: Frontend
cd app/frontend
npm run dev

# Terminal 3: Scheduler (optional, for testing overnight batch)
cd ai-hedge-fund
python src/automation/scheduler.py
```

### Testing Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/agents/test_news_scanner.py

# Run integration tests only
pytest tests/integration/

# Run with debug output
pytest -vv -s
```

---
