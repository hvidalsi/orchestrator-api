from pathlib import PurePath

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server
    server_name: str = Field(...)
    server_version: str = Field(...)
    port: int = Field(...)
    environment: str = Field(...)

    # Logging
    log_level: str = Field(...)
    log_to_file: bool = Field(...)

    # openai_api_key: str = Field(...)

    api_prefix: str = Field(...)

    # stt_default_model: str = Field(...)
    # stt_default_language: str = Field(...)
    # stt_default_response_format: str = Field(...)

    # tts_default_model: str = Field(...)
    # tts_default_voice_type: str = Field(...)
    # tts_default_speed: float = Field(...)
    # tts_default_response_format: str = Field(...)
    banking_agent_chat_endpoint: str = Field(...)
    tts_api_endpoint: str = Field(...)
    stt_api_endpoint: str = Field(...)

    root_path: str = str(PurePath(__file__).parents[2])

    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = "utf-8"
