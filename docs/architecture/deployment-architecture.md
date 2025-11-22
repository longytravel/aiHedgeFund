# Deployment Architecture

**MVP Deployment (Local/Single VPS):**

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:18.1
    environment:
      POSTGRES_DB: aihedgefund
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: .
    command: fastapi run src/main.py --host 0.0.0.0 --port 8000
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@db:5432/aihedgefund
      - EODHD_API_KEY=${EODHD_API_KEY}
      # ... all other env vars
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./src:/app/src  # Hot reload in dev

  scheduler:
    build: .
    command: python src/automation/scheduler.py
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@db:5432/aihedgefund
      # ... all other env vars
    depends_on:
      - db

  frontend:
    build: ./app/frontend
    command: npm run dev -- --host 0.0.0.0 --port 5173
    ports:
      - "5173:5173"
    volumes:
      - ./app/frontend/src:/app/src  # Hot reload in dev

volumes:
  pgdata:
```

**Production Deployment (Cloud):**
- Backend: AWS ECS/Fargate or DigitalOcean App Platform
- Database: AWS RDS PostgreSQL 18.1 or managed DigitalOcean Postgres
- Frontend: Vercel or Cloudflare Pages (static build)
- Scheduler: AWS EventBridge + Lambda or DigitalOcean Functions
- Monitoring: AWS CloudWatch or Datadog

---
