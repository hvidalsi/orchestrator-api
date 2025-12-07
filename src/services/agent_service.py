import base64
import json
import mimetypes
import os
import uuid
from typing import Dict

import httpx
from ag_ui.core import (
    CustomEvent,
    EventType,
    RunErrorEvent,
    RunFinishedEvent,
    RunStartedEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
    TextMessageStartEvent,
    ToolCallArgsEvent,
    ToolCallEndEvent,
    ToolCallResultEvent,
    ToolCallStartEvent,
)

from core.config import settings
from core.logger import setup_logger
from models.stt_models import SttAudioData
from models.tts_models import TtsAudioData, TtsAudioEventData
from services.stt_service import SttService
from services.tts_tervice import TtsService

logger = setup_logger(__name__)

MIME_EXTENSION_MAP = {
    "audio/webm": ".webm",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/ogg": ".ogg",
    "audio/flac": ".flac",
}


class AgentService:
    def __init__(self):
        self.api_url = settings.banking_agent_chat_endpoint

    def base64_to_audio(self, data_base64: str, mime_type: str):
        # 1. Decodificar Base64 a bytes
        audio_bytes = base64.b64decode(data_base64)
        # 2. Obtener extensión a partir del mime_type
        #    ej: "audio/wav" → ".wav"
        ext = MIME_EXTENSION_MAP.get(mime_type)
        if not ext:
            ext = mimetypes.guess_extension(mime_type) or ".bin"
        generated_filename = f"{str(uuid.uuid4())}{ext}"
        output_file = os.path.join(
            settings.root_path,
            "files",
            "generated",
            generated_filename,
        )
        with open(output_file, "wb") as f:
            f.write(audio_bytes)
        return output_file

    def audio_to_base64(self, path):
        with open(path, "rb") as f:
            audio_bytes = f.read()
            return base64.b64encode(audio_bytes).decode("utf-8")

    async def process_stream(
        self,
        input_audio: SttAudioData,
        thread_id: str,
        resume: Dict[str, str] = None,
    ):
        output_file = self.base64_to_audio(
            input_audio.audio_base64, input_audio.mime_type
        )
        # Pasando el audio a texto:
        user_input = SttService().transcribe_audio(output_file)
        # Enviamos al cliente el texto
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                }

                payload = {
                    "query": user_input,
                    "thread_id": thread_id,
                    "resume": resume,
                }

                async with client.stream(
                    "POST", self.api_url, json=payload, headers=headers
                ) as response:
                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue

                        json_data = line.replace("data:", "").strip()
                        event_dict = json.loads(json_data)

                        event_type = event_dict.get("type")
                        # --- Reconocimiento de eventos ---
                        if event_type == "RUN_STARTED":
                            yield RunStartedEvent(**event_dict)
                        elif event_type == "TEXT_MESSAGE_START":
                            yield TextMessageStartEvent(**event_dict)
                            # Enviamos un evento TEXT_MESSAGE_CONTENT con el contenido en
                            # texto del mensaje de usuario
                            yield TextMessageContentEvent(
                                type=EventType.TEXT_MESSAGE_CONTENT,
                                message_id=event_dict.get("messageId"),
                                delta=f"Transcription: {user_input}",
                            )
                        elif event_type == "TEXT_MESSAGE_CONTENT":
                            event = TextMessageContentEvent(**event_dict)
                            yield event
                            data: TtsAudioData = TtsService().synthesize_speech(
                                event.delta
                            )
                            data_value = TtsAudioEventData(
                                audio_base64=self.audio_to_base64(data.file_path),
                                mime_type=data.mime_type,
                            )
                            yield CustomEvent(
                                name="AUDIO_MESSAGE_CONTENT", value=data_value
                            )
                        elif event_type == "TEXT_MESSAGE_END":
                            yield TextMessageEndEvent(**event_dict)
                        elif event_type == "TOOL_CALL_START":
                            yield ToolCallStartEvent(**event_dict)
                        elif event_type == "TOOL_CALL_ARGS":
                            yield ToolCallArgsEvent(**event_dict)
                        elif event_type == "TOOL_CALL_END":
                            yield ToolCallEndEvent(**event_dict)
                        elif event_type == "TOOL_CALL_RESULT":
                            yield ToolCallResultEvent(**event_dict)
                        elif event_type == "RUN_ERROR":
                            yield RunErrorEvent(**event_dict)
                        elif event_type == "RUN_FINISHED":
                            yield RunFinishedEvent(**event_dict)
                        elif event_type == "CUSTOM":
                            yield CustomEvent(**event_dict)
                        else:
                            print("[UNKNOWN EVENT]", event_dict)

        except Exception as e:
            logger.error(f"Error durante la invocacion del agente:{e}")
            yield RunErrorEvent(
                type=EventType.RUN_ERROR,
                message=str(e),
                thread_id=thread_id,
                run_id="unknown",
            )
