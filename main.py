"""
backend/main.py
FastAPI application entry point for MediFind AI.

Run:  uvicorn backend.main:app --reload --port 8000
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from backend.api.hospital_routes import router as hospital_router
from backend.api.recommendation_routes import router as recommendation_router
from backend.api.triage_routes import router as triage_router
from backend.api.report_routes import router as report_router
from backend.api.routing import router as routing_router

app = FastAPI(
    title="MediFind AI",
    description="AI-Powered Emergency Hospital Recommendation System",
    version="1.0.0",
)

# CORS
cors_origin = os.getenv("CORS_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin, "http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hospital_router)
app.include_router(recommendation_router)
app.include_router(triage_router)
app.include_router(report_router)
app.include_router(routing_router)


@app.get("/health")
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "MediFind AI",
        "version": "1.0.0",
        "endpoints": [
            "GET  /health",
            "GET  /hospitals/nearby",
            "GET  /hospitals/ranked",
            "GET  /hospitals/recommendations",
            "POST /triage",
            "GET  /waitingtime",
            "POST /report",
            "GET  /route",
        ],
    }
