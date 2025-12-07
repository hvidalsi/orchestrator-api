import requests

from core.config import settings
from core.logger import setup_logger

logger = setup_logger(__name__)


class SttService:
    def __init__(self):
        self.api_url = settings.stt_api_endpoint

    def transcribe_audio(self, file_path: str) -> str:
        # audio_file = open(file_path, "rb")
        with open(file_path, "rb") as f:
            files = {
                "audioFile": (
                    file_path,
                    f,
                    "audio/webm",
                )  # O audio/mp3 según corresponda
            }
            response = requests.post(self.api_url, files=files)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} -> {response.text}")

        resp_json = response.json()

        return resp_json.get("transcription", "")
