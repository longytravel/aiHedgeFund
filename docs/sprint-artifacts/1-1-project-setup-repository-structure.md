# Story 1.1: Project Setup & Repository Structure

Status: ready-for-dev

## Story

As a **developer**,
I want **a well-organized project structure with Docker containerization**,
so that **the system is deployable and maintainable from day 1**.

## Acceptance Criteria

1. **Repository Structure Exists**
   - **Given** a new greenfield project
   - **When** the repository is initialized
   - **Then** the following directory structure exists:
     - `/backend` - FastAPI application with proper module organization
     - `/frontend` - React 19 application with TypeScript 5.x
     - `/agents` - Agent plugin directory for discovery/analysis/decision agents
     - `/data/inbox` - File drop folders:
       - `/data/inbox/ticker-lists` - CSV ticker list uploads
       - `/data/inbox/research-reports` - PDF/markdown research files (future)
       - `/data/inbox/manual-stocks` - JSON stock additions
     - `/data/processed` - Processed files archive with date-stamped folders
     - `/tests` - Test suites (unit, integration, end-to-end)
     - `docker-compose.yml` - Multi-container setup (backend, frontend, postgres)
     - `.env.example` - Environment variable template with all required keys
     - `README.md` - Setup instructions with quickstart guide

2. **Docker Containers Build Successfully**
   - **Given** the docker-compose.yml is configured
   - **When** `docker-compose build` is executed
   - **Then** all containers (backend, frontend, postgres) build without errors
   - **And** containers start successfully with `docker-compose up`
   - **And** no port conflicts occur (backend: 8000, frontend: 5173, postgres: 5432)

3. **Health Check Endpoint Returns 200 OK**
   - **Given** the backend container is running
   - **When** a GET request is made to `http://localhost:8000/api/health`
   - **Then** the response status code is 200 OK
   - **And** the response body contains:
     ```json
     {
       "status": "healthy",
       "timestamp": "<ISO-8601 timestamp>",
       "services": {
         "database": "connected",
         "cache": "not_configured"
       }
     }
     ```

## Tasks / Subtasks

- [ ] **Task 1: Initialize Repository Structure** (AC: #1)
  - [ ] Create root project folder: `aihedgefund/`
  - [ ] Create `/backend` folder with Python package structure:
    - `backend/app/` - FastAPI application code
    - `backend/app/api/` - API route definitions
    - `backend/app/models/` - SQLAlchemy database models
    - `backend/app/services/` - Business logic services
    - `backend/app/core/` - Core configuration and dependencies
    - `backend/requirements.txt` - Python dependencies
    - `backend/Dockerfile` - Backend container definition
  - [ ] Create `/frontend` folder with React/Vite structure:
    - `frontend/src/` - React source code
    - `frontend/src/components/` - Reusable React components
    - `frontend/src/pages/` - Page-level components
    - `frontend/src/services/` - API client services
    - `frontend/package.json` - Node dependencies
    - `frontend/Dockerfile` - Frontend container definition
  - [ ] Create `/agents` folder structure:
    - `agents/discovery/` - Discovery agent implementations (future)
    - `agents/analysis/` - Analysis agent implementations (future)
    - `agents/decision/` - Decision agent implementations (future)
    - `agents/shared/` - Shared agent utilities
  - [ ] Create `/data/inbox` folder structure:
    - `data/inbox/ticker-lists/` - CSV uploads
    - `data/inbox/research-reports/` - Research PDFs/markdown
    - `data/inbox/manual-stocks/` - JSON stock additions
  - [ ] Create `/data/processed` folder for archiving processed files
  - [ ] Create `/tests` folder structure:
    - `tests/unit/` - Unit tests
    - `tests/integration/` - Integration tests
    - `tests/fixtures/` - Test data fixtures

- [ ] **Task 2: Configure Docker Multi-Container Setup** (AC: #2)
  - [ ] Create `docker-compose.yml` with services:
    - `postgres` service (image: postgres:18.1)
    - `backend` service (build: ./backend, depends_on: postgres)
    - `frontend` service (build: ./frontend)
  - [ ] Define volume mappings:
    - `postgres_data` volume for database persistence
    - `data/inbox` mounted to backend container
    - `data/processed` mounted to backend container
  - [ ] Configure environment variables:
    - `DATABASE_URL` for backend → postgres connection
    - `EODHD_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` (from .env)
  - [ ] Set up networking:
    - Internal network for service communication
    - Expose ports: backend (8000), frontend (5173), postgres (5432)
  - [ ] Create `.env.example` with template values:
    ```
    POSTGRES_USER=aihedgefund
    POSTGRES_PASSWORD=<changeme>
    POSTGRES_DB=aihedgefund
    EODHD_API_KEY=<your_key>
    OPENAI_API_KEY=<your_key>
    ANTHROPIC_API_KEY=<your_key>
    GOOGLE_API_KEY=<your_key>
    ```
  - [ ] Add `.gitignore` to exclude:
    - `.env` (actual secrets)
    - `node_modules/`, `__pycache__/`, `*.pyc`
    - `data/inbox/*`, `data/processed/*` (user data)
    - `postgres_data/` (database files)

- [ ] **Task 3: Implement Backend Health Check Endpoint** (AC: #3)
  - [ ] Create FastAPI application in `backend/app/main.py`:
    - Initialize FastAPI app
    - Configure CORS middleware
    - Import and register API routers
  - [ ] Implement health check endpoint in `backend/app/api/health.py`:
    ```python
    from fastapi import APIRouter, Depends
    from datetime import datetime, timezone
    from app.core.database import get_db

    router = APIRouter()

    @router.get("/health")
    async def health_check(db = Depends(get_db)):
        db_status = "connected" if db else "disconnected"
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {
                "database": db_status,
                "cache": "not_configured"
            }
        }
    ```
  - [ ] Register health router in `main.py`:
    ```python
    from app.api import health
    app.include_router(health.router, prefix="/api", tags=["health"])
    ```
  - [ ] Create minimal `backend/Dockerfile`:
    - Use Python 3.14 base image
    - Install dependencies from requirements.txt
    - Expose port 8000
    - Run `uvicorn app.main:app --host 0.0.0.0 --port 8000`

- [ ] **Task 4: Create Documentation** (AC: #1)
  - [ ] Write `README.md` with sections:
    - Project overview (AI hedge fund system)
    - Architecture diagram (ASCII or reference to docs)
    - Prerequisites (Docker, Docker Compose, API keys)
    - Quickstart instructions:
      1. Clone repository
      2. Copy `.env.example` to `.env` and fill in API keys
      3. Run `docker-compose build`
      4. Run `docker-compose up`
      5. Access health check: `curl http://localhost:8000/api/health`
    - Development workflow (how to run tests, add new agents)
    - Environment variables reference
    - Troubleshooting common issues
  - [ ] Create `CONTRIBUTING.md` with contribution guidelines
  - [ ] Create `LICENSE` file (choose appropriate license, e.g., MIT)

- [ ] **Task 5: Testing & Validation** (AC: #1, #2, #3)
  - [ ] Write integration test for health check endpoint:
    - Test file: `tests/integration/test_health.py`
    - Test case: `test_health_endpoint_returns_200()`
    - Verify response status code = 200
    - Verify response JSON structure matches spec
  - [ ] Manual verification checklist:
    - [ ] Run `docker-compose build` → all services build successfully
    - [ ] Run `docker-compose up` → all containers start without errors
    - [ ] Check container logs → no critical errors
    - [ ] Test health endpoint: `curl http://localhost:8000/api/health` → 200 OK
    - [ ] Verify folder structure exists and matches spec
    - [ ] Verify `.env.example` contains all required keys
    - [ ] Verify `README.md` quickstart works from clean state

## Dev Notes

### Architecture Patterns and Constraints

**From Epic Tech Spec (tech-spec-epic-1.md):**

- **Technology Stack:** Python 3.14 (free-threaded, JIT), FastAPI 0.121.3, React 19, TypeScript 5.x, PostgreSQL 18.1, Docker
- **Backend Structure:** Follow `/backend/app/` organization with clear separation: `api/`, `models/`, `services/`, `core/`
- **Container Strategy:** Multi-container Docker Compose with services: postgres (18.1), backend (FastAPI), frontend (React/Vite)
- **Environment Variables:** ALL secrets in .env (never committed), use python-dotenv for loading
- **Health Check Pattern:** Implement `/api/health` endpoint with database connectivity check

**From Architecture Document:**

- **Project Structure:** Align with Reference System structure (`C:\Users\User\Desktop\AIHedgeFund\ai-hedge-fund\`) where applicable:
  - Backend: Reuse route patterns (`/api/v1/analysis`, `/api/v1/portfolio`)
  - Frontend: Reuse dashboard layout concepts
  - Docker: Adapt service definitions from reference
- **DO NOT COPY from Reference:**
  - Sequential workflow logic (we're building batch overnight)
  - US market assumptions
  - Financial Datasets API integration (we use EODHD)

**Testing Standards:**

- Unit test coverage target: 70%+ for core logic
- Integration tests for critical workflows
- Follow pytest conventions for test structure
- Test file naming: `test_<module>.py`

### Source Tree Components to Touch

**New Files Created:**

- Root level:
  - `docker-compose.yml` - Multi-container orchestration
  - `.env.example` - Environment variable template
  - `.gitignore` - Git ignore rules
  - `README.md` - Project documentation
  - `CONTRIBUTING.md`, `LICENSE` - Project governance

- Backend structure:
  - `backend/app/main.py` - FastAPI application entry point
  - `backend/app/api/health.py` - Health check endpoint
  - `backend/app/core/config.py` - Configuration management (future)
  - `backend/app/core/database.py` - Database session management (future)
  - `backend/requirements.txt` - Python dependencies
  - `backend/Dockerfile` - Backend container definition

- Frontend structure:
  - `frontend/src/main.tsx` - React application entry point
  - `frontend/package.json` - Node dependencies
  - `frontend/vite.config.ts` - Vite configuration
  - `frontend/Dockerfile` - Frontend container definition

- Data folders:
  - `data/inbox/ticker-lists/.gitkeep` - Preserve folder in git
  - `data/inbox/research-reports/.gitkeep`
  - `data/inbox/manual-stocks/.gitkeep`
  - `data/processed/.gitkeep`

- Test structure:
  - `tests/integration/test_health.py` - Health check test

**Modified Files:** None (greenfield project)

### Project Structure Notes

**Alignment with Unified Project Structure:**

This is the foundational story establishing the project structure. Future stories will align with this structure:

- **Backend modules:** All agent logic goes in `/agents/`, API routes in `/backend/app/api/`, database models in `/backend/app/models/`
- **Data flow:** Manual files dropped in `/data/inbox/`, processed files archived in `/data/processed/`
- **Testing:** All tests in `/tests/` with clear separation of unit vs integration tests

**Naming Conventions:**

- **Files:** snake_case for Python (e.g., `health_check.py`), kebab-case for frontend (e.g., `api-client.ts`)
- **Folders:** kebab-case throughout (e.g., `ticker-lists`, `research-reports`)
- **Docker services:** lowercase with underscores (e.g., `postgres`, `backend`, `frontend`)

### References

- **Epic Tech Spec:** [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Detailed-Design]
- **PRD Requirements:** [Source: docs/prd/functional-requirements.md#FR-8.1]
- **Architecture Stack:** [Source: docs/architecture/technology-stack-details.md#Core-Technologies]
- **PRD Project Structure:** [Source: docs/prd/functional-requirements.md#FR-8.1-Backend]
- **Code Reuse Guidance:** [Source: docs/epics/epic-1-foundation-data-architecture.md#Story-1.1-Technical-Notes]

## Dev Agent Record

### Context Reference

- [Story Context](1-1-project-setup-repository-structure.context.xml) - Generated 2025-11-22

### Agent Model Used

_To be filled by dev agent_

### Debug Log References

_To be filled by dev agent during implementation_

### Completion Notes List

_To be filled by dev agent upon story completion_

### File List

_To be filled by dev agent with NEW/MODIFIED/DELETED file paths_
