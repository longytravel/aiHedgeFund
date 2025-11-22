"""Integration tests for health check endpoint."""
import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint_returns_200():
    """
    Test that health check endpoint returns 200 OK.

    Acceptance Criteria #3:
    - GET request to /api/health returns 200 OK
    - Response includes status, timestamp, and services
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/health")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


@pytest.mark.asyncio
async def test_health_endpoint_response_structure():
    """
    Test that health check endpoint returns correct JSON structure.

    Acceptance Criteria #3:
    - Response contains: status, timestamp, services.database, services.cache
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/health")

    data = response.json()

    # Verify required keys exist
    assert "status" in data, "Response missing 'status' field"
    assert "timestamp" in data, "Response missing 'timestamp' field"
    assert "services" in data, "Response missing 'services' field"

    # Verify services structure
    services = data["services"]
    assert "database" in services, "Services missing 'database' field"
    assert "cache" in services, "Services missing 'cache' field"

    # Verify cache is not configured (as per AC)
    assert services["cache"] == "not_configured", \
        f"Expected cache='not_configured', got '{services['cache']}'"


@pytest.mark.asyncio
async def test_health_endpoint_timestamp_format():
    """
    Test that health check endpoint returns ISO-8601 timestamp.

    Acceptance Criteria #3:
    - Timestamp is in ISO-8601 format
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/health")

    data = response.json()
    timestamp_str = data["timestamp"]

    # Verify timestamp can be parsed as ISO-8601
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        assert timestamp is not None, "Timestamp parsing failed"
    except ValueError as e:
        pytest.fail(f"Timestamp not in ISO-8601 format: {e}")


@pytest.mark.asyncio
async def test_root_endpoint():
    """
    Test that root endpoint returns API information.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "health" in data
    assert data["health"] == "/api/health"
