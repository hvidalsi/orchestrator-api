from typing import Any, Optional

from pydantic import BaseModel, Field
from models.stt_models import SttAudioData


class UserQueryRequest(BaseModel):
    """Request to process a query with the ReAct agent"""

    audio: SttAudioData = Field(..., description="audio convertido al formato base64")
    thread_id: str = Field(None, description="Session ID for memory continuity")
    resume: Optional[Any] = None
