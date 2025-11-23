import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

# Use the same DB URL for testing connectivity
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://aihedgefund:devpassword@localhost:5432/aihedgefund")

@pytest.mark.asyncio
async def test_database_connectivity():
    """
    Test that the application can successfully connect to the PostgreSQL database
    and execute a simple query.
    """
    try:
        # Create an async engine
        engine = create_async_engine(TEST_DATABASE_URL, future=True)
        
        async with engine.connect() as connection:
            # Execute a simple query (SELECT 1)
            result = await connection.execute(text("SELECT 1"))
            value = result.scalar()
            
            # Verify the result
            assert value == 1
            
        await engine.dispose()
        
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

@pytest.mark.asyncio
async def test_database_connection_failure_handling():
    """
    Test handling of database connection failures.
    We simulate this by using an invalid database URL.
    """
    INVALID_DATABASE_URL = "postgresql+asyncpg://invalid_user:wrong_pass@localhost:5432/nonexistent_db"
    
    try:
        engine = create_async_engine(INVALID_DATABASE_URL, future=True)
        
        # Attempt to connect - expecting an exception
        with pytest.raises(Exception): # Catching generic Exception as asyncpg might raise different specific errors
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
                
        await engine.dispose()
        
    except Exception as e:
        # If create_async_engine raises immediately (unlikely for lazy connect), that's also a pass
        pass
