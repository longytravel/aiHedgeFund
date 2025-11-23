# Story 1.2: Database Schema & Models

Status: review

## Story

As a **system**,
I want **a comprehensive database schema supporting all future features**,
so that **new capabilities can be added without schema migrations breaking existing data**.

## Acceptance Criteria

1.  **Comprehensive Schema with Relationships**
    *   **Given** PostgreSQL database is running
    *   **When** Alembic migrations are applied
    *   **Then** the following tables exist with proper relationships and indexing:
        *   `stocks` - UK company master data (ticker, name, sector, market_cap)
        *   `signals` - Discovery agent signals (ticker, signal_type, score, timestamp, source)
        *   `analysis_results` - Analysis agent outputs (ticker, agent_name, recommendation, confidence, reasoning)
        *   `portfolio_positions` - Current holdings (ticker, entry_date, entry_price, quantity, stop_loss, target)
        *   `watchlist_entries` - Stocks being monitored (ticker, trigger_type, trigger_value, thesis, expiry_date)
        *   `research_queue` - Stocks under investigation (ticker, score, status)
        *   `trades` - Historical trade log (ticker, action, price, quantity, timestamp, outcome)
        *   `reports` - Generated morning reports (date, content, stocks_analyzed, recommendations_count)
        *   `agent_config` - Agent settings (agent_name, enabled, weight, parameters)
        *   `audit_log` - All system decisions (timestamp, action, data, user_id)
    *   **And** All tables have appropriate indexes on frequently queried columns (e.g., `ticker`, `timestamp`, `status`, `agent_id`)
    *   **And** Foreign key constraints maintain referential integrity (e.g., `signals.stock_id` references `stocks.id`)
    *   **And** Timestamps (`created_at`, `updated_at`) use UTC timezone and are automatically managed
    *   **And** Schema supports soft deletes where applicable (e.g., `deleted_at` column in `portfolio_positions`)

2.  **Extensible Data Storage**
    *   **Given** agent-specific data or new metrics need to be stored
    *   **When** data is inserted into `signals`, `analysis_results`, `audit_log`, `watchlist_entries`, `research_queue`
    *   **Then** `JSONB` columns are used (e.g., `signals.data`, `analysis_results.key_metrics`, `audit_log.details`, `agent_config.parameters`)
    *   **And** `agent_config.parameters` uses a `JSONB` column to store flexible agent settings

## Tasks / Subtasks

- [x] **Task 1: Define SQLAlchemy ORM Models** (AC: #1, #2)
  - [x] Create SQLAlchemy ORM models for all specified tables: `Stock`, `Signal`, `AnalysisResult`, `PortfolioPosition`, `WatchlistEntry`, `ResearchQueue`, `Trade`, `Report`, `AgentConfig`, `AuditLog`.
  - [x] Ensure `id` fields are `UUID` type and default to `uuid.uuid4()` (or `uuidv7()` if implemented).
  - [x] Include `created_at` and `updated_at` (UTC timezone, automatically managed) for all models.
  - [x] Define `JSONB` columns for flexible data storage in `Signal.data`, `AnalysisResult.key_metrics`, `AuditLog.details`, `AgentConfig.parameters`.
  - [x] Establish foreign key relationships between models (e.g., `Signal.stock_id` to `Stock.id`).
  - [x] Implement appropriate indexing for frequently queried columns in each model (e.g., `ticker`, `timestamp`, `agent_id`, `status`).

- [x] **Task 2: Initialize & Configure Alembic** (AC: #1)
  - [x] Initialize Alembic environment for database migrations (`alembic init -t async backend/alembic`).
  - [x] Configure `alembic.ini` and `env.py` to connect to the PostgreSQL database using `asyncpg` and SQLAlchemy's async engine.
  - [x] Ensure Alembic can correctly detect changes in SQLAlchemy models.

- [x] **Task 3: Create Initial Migration** (AC: #1, #2)
  - [x] Generate a new Alembic migration script to create all defined tables with their columns, data types, indexes, and foreign key constraints.
  - [x] Verify the migration script accurately reflects the desired schema.
  - [x] Apply the migration to a local PostgreSQL database to confirm successful schema creation.

- [x] **Task 4: Implement Basic CRUD Operations for Key Models**
  - [x] Implement asynchronous create, read, update, and delete functions for `Stock` and `Signal` models.
  - [x] Ensure data can be successfully inserted, retrieved, modified, and deleted, respecting `JSONB` fields and relationships.

- [x] **Task 5: Develop Unit Tests for Models** (AC: #1, #2)
  - [x] Write unit tests for each SQLAlchemy model to verify correct column definitions, data types, relationships, and default values.
  - [x] Test `created_at`/`updated_at` functionality and `JSONB` field handling.

- [x] **Task 6: Develop Integration Tests for Migrations & Connectivity** (AC: #1)
  - [x] Write integration tests to run Alembic migrations (upgrade and downgrade) and verify the schema state before and after.
  - [x] **[PRIORITY]** Implement integration tests for database connectivity, including scenarios that simulate connection failures and graceful handling, as recommended from learnings in Story 1.1.

- [x] **Task 7: Update Dependencies and Project Configuration**
  - [x] Add `alembic` to `backend/requirements.txt` and `pyproject.toml`.
  - [x] Update `docker-compose.yml` to:
    - Include `alembic` as a dependency for the backend service (e.g., run `alembic upgrade head` on backend startup).
    - Ensure the backend service has necessary environment variables for database connection.


### Dev Notes

### Architecture Patterns and Constraints

**From ADRs & Implementation Architecture:**

*   **Database Choice:** PostgreSQL 18.1 for its I/O performance gains and `uuidv7()` support.
*   **ORM:** SQLAlchemy 2.x for Python models, ensuring type safety and async capabilities.
*   **Migrations:** Alembic for managing schema changes in a controlled and versioned manner.
*   **Data Types:** Utilize `JSONB` for flexible, schema-less data storage where agent-specific data or evolving metrics are required (e.g., `signals.data`, `analysis_results.key_metrics`, `audit_log.details`, `agent_config.parameters`).
*   **UUIDs:** Use `uuidv7()` for primary keys where applicable, enabling efficient time-ordered indexing.
*   **Timestamps:** All `created_at` and `updated_at` fields should be timezone-aware (UTC) and managed automatically by the ORM.
*   **Schema Evolution:** Design the schema to be forward-compatible, minimizing breaking changes for future features.

**Specific to this Story:**

*   **Database Connectivity:** Leverage the existing database connection and session management established in Story 1.1 (`backend/app/core/database.py`).
*   **Table Naming:** Adhere to `snake_case` for table and column names (e.g., `portfolio_positions`).
*   **Relationships:** Define explicit foreign key relationships between tables (`signals.stock_id` to `stocks.id`).

### Learnings from Previous Story (1.1: Project Setup & Repository Structure)

*   **New Services Established:** The previous story successfully set up the FastAPI backend and integrated async SQLAlchemy for database session management. This provides the foundational services needed for interacting with the database schema defined in this story.
*   **Architectural Alignment Confirmed:** The core tech stack (Python 3.14, FastAPI, PostgreSQL 18.1, Docker) and backend structure (separation into `api/`, `models/`, `services/`, `core/`) were validated and approved. All database schema components should adhere strictly to this established pattern, particularly models residing in `backend/app/models/`.
*   **Recommendation for Current Story (1.2):** Explicitly add health check tests for database failure scenarios. This will build upon the existing health check endpoint to ensure robustness in database connectivity.
*   **Files Created in Previous Story (1.1):**
    - `backend/app/__init__.py`
    - `backend/app/main.py`
    - `backend/app/api/__init__.py`
    - `backend/app/api/health.py`
    - `backend/app/core/__init__.py`
    - `backend/app/core/database.py`
    - `backend/app/models/__init__.py`
    - `backend/app/services/__init__.py`
    - `backend/requirements.txt`
    - `backend/Dockerfile`
    - `frontend/src/main.tsx`
    - `frontend/src/components/`
    - `frontend/src/pages/`
    - `frontend/src/services/`
    - `frontend/package.json`
    - `frontend/tsconfig.json`
    - `frontend/vite.config.ts`
    - `frontend/index.html`
    - `frontend/Dockerfile`
    - `tests/integration/test_health.py`
    - `.env.example`
    - `CONTRIBUTING.md`
    - `LICENSE`
    - `data/inbox/ticker-lists/.gitkeep`
    - `data/inbox/research-reports/.gitkeep`
    - `data/inbox/manual-stocks/.gitkeep`
    - `data/processed/.gitkeep`

### Source Tree Components to Touch

**New Files Created:**

*   `backend/app/models/stock_model.py` (or similar, one file per model or grouped)
*   `backend/app/models/signal_model.py`
*   `backend/app/models/analysis_result_model.py`
*   `backend/app/models/portfolio_position_model.py`
*   `backend/app/models/watchlist_entry_model.py`
*   `backend/app/models/research_queue_model.py`
*   `backend/app/models/trade_model.py`
*   `backend/app/models/report_model.py`
*   `backend/app/models/agent_config_model.py`
*   `backend/app/models/audit_log_model.py`
*   `alembic/env.py` (or initial setup files)
*   `alembic/script.py.mako` (or initial setup files)
*   `alembic/versions/initial_schema.py` (or migration file for this story)
*   `tests/unit/test_models.py` (or similar for model tests)
*   `tests/integration/test_migrations.py` (or similar for migration tests)

**Modified Files:**

*   `backend/app/models/__init__.py` (to import new models)
*   `backend/requirements.txt` (add `alembic`, `psycopg2-binary` if not using asyncpg directly for ORM)
*   `pyproject.toml` (if managing dependencies here)
*   `docker-compose.yml` (if alembic needs its own service for running migrations, or new entrypoint for backend service)
*   `backend/app/main.py` (if database initialization logic changes)

### Project Structure Notes

*   **Model Organization:** Models will be organized under `backend/app/models/`, potentially with one file per major entity or grouped logically.
*   **Migrations:** Alembic scripts will reside in a dedicated `alembic/` directory at the project root or within the `backend/` directory, following standard Alembic conventions.

### References

*   **Epic Tech Spec:** [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Detailed-Design]
*   **Epic 1 Details:** [Source: docs/epics/epic-1-foundation-data-architecture.md]
*   **Data Architecture:** [Source: docs/architecture/data-architecture.md]
*   **ADR-003:** Use PostgreSQL 18.1 Over SQLite [Source: docs/architecture/architecture-decision-records-adrs.md]

## Dev Agent Record

### Context Reference

<!-- Placeholder for dynamic XML context generation -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

- Fixed Docker build context issue by changing context to root `.` and updating `backend/Dockerfile`.
- Fixed `ModuleNotFoundError` in Alembic `env.py` by correctly adjusting `sys.path`.
- Fixed database connection in unit tests by using `DATABASE_URL` environment variable to point to `postgres` service.

### Completion Notes List

- Defined SQLAlchemy ORM models for all entities in `backend/app/models/`.
- Configured Alembic for async migrations in `backend/alembic/`.
- Generated and verified initial migration script.
- Implemented basic CRUD services in `backend/app/services/data_service.py`.
- Created unit tests in `tests/unit/test_models.py` and integration tests in `tests/integration/test_db_connectivity.py`.
- Updated `docker-compose.yml` to run migrations on backend startup and fixed build context to include tests.
- Updated `backend/Dockerfile` to support new build context.
- Successfully ran tests in Docker container.

### File List

- backend/app/models/base_model.py
- backend/app/models/stock_model.py
- backend/app/models/signal_model.py
- backend/app/models/analysis_result_model.py
- backend/app/models/portfolio_position_model.py
- backend/app/models/watchlist_entry_model.py
- backend/app/models/research_queue_model.py
- backend/app/models/trade_model.py
- backend/app/models/report_model.py
- backend/app/models/agent_config_model.py
- backend/app/models/audit_log_model.py
- backend/app/models/__init__.py
- backend/alembic/env.py
- backend/alembic/versions/*.py
- backend/app/services/data_service.py
- tests/unit/test_models.py
- tests/integration/test_db_connectivity.py
- docker-compose.yml
- backend/Dockerfile
