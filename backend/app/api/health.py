"""Health check endpoint for monitoring system status."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime, timezone

from app.core.database import get_db

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint that returns system status.

    Returns:
        dict: System health status including:
            - status: "healthy" if all systems operational
            - timestamp: ISO-8601 formatted current time
            - services: Status of each service (database, cache)

    Example Response:
        {
            "status": "healthy",
            "timestamp": "2025-11-22T20:45:00.123456+00:00",
            "services": {
                "database": "connected",
                "cache": "not_configured"
            }
        }
    """
    # Test database connectivity
    db_status = "disconnected"
    try:
        # Execute a simple query to test database connection
        result = await db.execute(text("SELECT 1"))
        if result:
            db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "database": db_status,
            "cache": "not_configured"  # Redis will be configured in Epic 6
        }
    }
