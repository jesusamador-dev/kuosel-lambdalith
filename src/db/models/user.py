from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from src.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    country = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    subscription_type = Column(String, nullable=True)
    subscription_status = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
