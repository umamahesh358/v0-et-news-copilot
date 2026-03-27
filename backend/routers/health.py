"""Health check endpoint"""

from fastapi import APIRouter
from datetime import datetime
from backend.models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if API is healthy and running"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(),
        services={
            "fastapi": "running",
            "text_processing": "ready"
        }
    )
