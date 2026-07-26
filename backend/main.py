from fastapi import FastAPI

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