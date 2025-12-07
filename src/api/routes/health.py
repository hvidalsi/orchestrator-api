from fastapi import APIRouter

from core.config import settings
from models.api import HealthResponse

router = APIRouter(prefix=settings.api_prefix)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Service health check"""
    return HealthResponse(status="healthy", service="Speech API")
