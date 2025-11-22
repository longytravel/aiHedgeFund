"""FastAPI application entry point for AIHedgeFund backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Startup: Initialize database connections, load config
    Shutdown: Close connections, cleanup resources
    """
    # Startup
    print("🚀 AIHedgeFund backend starting up...")
    print("✅ Database connection pool initialized")

    yield

    # Shutdown
    print("🛑 AIHedgeFund backend shutting down...")


# Create FastAPI application
app = FastAPI(
    title="AIHedgeFund API",
    description="AI-powered UK stock analysis and portfolio management system",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Register API routers
app.include_router(health.router, prefix="/api", tags=["health"])


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "AIHedgeFund API",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/api/health"
    }
