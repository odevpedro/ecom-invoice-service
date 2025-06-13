# infrastructure/persistence/db.py
"""
Database configuration and session factory using SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Use environment variable or default URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:password@localhost:5432/invoice_db")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
