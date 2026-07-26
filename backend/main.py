from fastapi import FastAPI

from database.base import Base
from database.connection import engine

# Import models so SQLAlchemy creates the tables
import database.models

# Import routers
from api.routes import (
    users,
    conversations,
    messages,
    documents,
    memory,
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Context Memory Engine API",
    description="Backend API for the Context Memory Engine (CME)",
    version="1.0.0",
)

# Register routers
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(messages.router)
app.include_router(documents.router)
app.include_router(memory.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Context Memory Engine API",
        "status": "Running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy",
    }