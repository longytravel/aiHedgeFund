# Project Initialization

### First Implementation Story: Initialize Project

```bash
# Backend initialization
mkdir -p ai-hedge-fund && cd ai-hedge-fund
python3.14 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install core dependencies
pip install --upgrade pip
pip install "fastapi[standard]==0.121.3" \
            "langgraph==1.0.5" \
            "langchain==1.0" \
            "langchain-openai" \
            "langchain-anthropic" \
            "langchain-google-genai" \
            "psycopg2-binary" \
            "sqlalchemy" \
            "alembic" \
            "pydantic==2.x" \
            "python-dotenv" \
            "httpx" \
            "schedule" \
            "pytest" \
            "pytest-asyncio"

# Frontend initialization
cd app/frontend
npm create vite@latest . -- --template react-ts
npm install react@19 react-dom@19 @types/react@19 @types/react-dom@19
npm install axios react-router-dom @tanstack/react-query recharts lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

This establishes the base architecture with all decisions below pre-configured.

---
