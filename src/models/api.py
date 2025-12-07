from typing import List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for health check"""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
