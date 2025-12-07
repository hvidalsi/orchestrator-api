from ag_ui.core import (
    EventType,
    RunErrorEvent,
)
from ag_ui.encoder import EventEncoder
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from core.config import settings
from core.logger import setup_logger
from models.agent_models import UserQueryRequest
from services.agent_service import AgentService

logger = setup_logger(__name__)
router = APIRouter(prefix=settings.api_prefix)


@router.post("/start/chat/stream")
async def chat_stream(input_data: UserQueryRequest, request: Request):
    """Chat with the ReAct agent using Server-Sent Events (SSE) streaming"""
    # Create an event encoder to properly format SSE events
    accept_header = request.headers.get("accept")
    encoder = EventEncoder(accept=accept_header)




    input_audio = input_data.audio
    thread_id = input_data.thread_id
    resume = input_data.resume
    agent_service = AgentService()
    # logger.info(f"Processing streaming chat request for query: {message[:50]}...")

    async def generate():
        try:
            async for event in agent_service.process_stream(
                input_audio, thread_id, resume
            ):
                yield encoder.encode(event)
        except Exception as error:
            yield encoder.encode(
                RunErrorEvent(type=EventType.RUN_ERROR, message=str(error))
            )

    return StreamingResponse(generate(), media_type=encoder.get_content_type())
