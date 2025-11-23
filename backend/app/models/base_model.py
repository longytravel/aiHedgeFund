import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

# Import the Base from our database.py
from app.core.database import Base


# Define a custom base for all models to inherit common features
# All models will inherit from this BaseModel, which itself inherits from the project's Base
class BaseModel(Base):
    __abstract__ = True  # This tells SQLAlchemy not to create a table for BaseModel itself

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=func.now(), # Use SQL function for timestamp to ensure consistency
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(), # Use SQL function for timestamp to ensure consistency
        onupdate=func.now(),
        nullable=False,
    )
