from typing import Any, Optional

from pydantic import BaseModel, Field


class SttServiceRequest(BaseModel):
    audio_base64: str = Field(..., description="audio convertido al formato base64")
    mime_type: str = Field(
        "audio/mpeg", description="audio convertido al formato base64"
    )
    thread_id: str = Field(None, description="Session ID for memory continuity")
    resume: Optional[Any] = None


class SttAudioData(BaseModel):
    audio_base64: str = Field(..., description="audio convertido al formato base64")
    mime_type: str = Field(
        "audio/mpeg", description="audio convertido al formato base64"
    )
