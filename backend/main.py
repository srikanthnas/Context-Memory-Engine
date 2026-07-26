from fastapi import FastAPI

from database.connection import engine
from database.base import Base

# Import models so SQLAlchemy knows about them
import database.models

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Context Memory Engine API",
    description="Backend API for the Context Memory Engine (CME)",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Context Memory Engine API",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }