from pydantic import BaseModel, Field


class TtsAudioEventData(BaseModel):
    audio_base64: str = Field(..., description="audio convertido al formato base64")
    mime_type: str = Field(
        "audio/mpeg", description="audio convertido al formato base64"
    )


class TtsAudioData(BaseModel):
    file_path: str = Field(
        ..., description="Ruta local en el server del archivo de audio"
    )
    mime_type: str = Field(
        "audio/mpeg", description="audio convertido al formato base64"
    )
