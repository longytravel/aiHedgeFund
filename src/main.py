"""
AIHedgeFund - FastAPI Application Entry Point

Sprint 0: Minimal application for validation
Story 1.1: Will expand with full initialization
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events (startup/shutdown)."""
    # Startup
    print("🚀 AIHedgeFund starting up...")
    print("   Phase: Sprint 0 Complete")
    print("   Next: Story 1.1 - Project Initialization")

    yield

    # Shutdown
    print("👋 AIHedgeFund shutting down...")


# Create FastAPI application
app = FastAPI(
    title="AIHedgeFund",
    description="AI-Powered Autonomous UK Stock Trading System",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS (for frontend in Epic 5)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health Check Endpoint (Sprint 0)
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint - basic health check."""
    return {
        "status": "online",
        "service": "AIHedgeFund",
        "version": "0.1.0",
        "phase": "Sprint 0 Complete",
        "next_story": "Story 1.1 - Project Initialization",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.

    Story 1.6 will expand this with:
    - Database connectivity check
    - Redis connectivity check
    - API provider status
    - LLM provider status
    """
    return {
        "status": "healthy",
        "database": "not_configured",  # Story 1.2
        "redis": "not_configured",  # Story 1.7
        "llm_provider": "not_configured",  # Story 1.8
    }


@app.get("/api/v1/info")
async def api_info():
    """API information endpoint."""
    return {
        "api_version": "v1",
        "python_version": "3.14+",
        "framework": "FastAPI 0.121.3",
        "ai_framework": "LangGraph 1.0.5",
        "database": "PostgreSQL 18.1",
        "architecture": "20-agent multi-agent system",
        "budget": "£200/month",
    }


# ============================================================================
# Story 1.1 onwards will add:
# - Database session management
# - Settings from config.py
# - API route imports (analysis, portfolio, watchlist, etc.)
# - Error handlers
# - Logging configuration
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
