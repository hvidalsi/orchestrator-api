import os
import uuid

import requests

from core.config import settings
from core.logger import setup_logger
from models.tts_models import TtsAudioData

logger = setup_logger(__name__)


class TtsService:
    def __init__(self):
        self.api_url = settings.tts_api_endpoint

    def synthesize_speech(self, input_text: str, file_name: str = None):
        payload = {"message": input_text}

        response = requests.post(self.api_url, json=payload)
        mime_type = response.headers.get("Content-Type")

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        if not file_name:
            # Se genera un nombre automatico
            file_name = f"{str(uuid.uuid4())}.mp3"
        output_file = os.path.join(
            settings.root_path,
            "files",
            "generated",
            file_name,
        )
        with open(output_file, "wb") as f:
            f.write(response.content)
        logger.info(f"Audio guardado en: {output_file}")
        return TtsAudioData(file_path=output_file, mime_type=mime_type)
