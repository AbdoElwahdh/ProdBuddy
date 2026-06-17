import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from ...schemas.chat_models import ChatMessageRequest, ChatMessageResponse, VoiceMessageRequest, TranscribeResponse
from ...services.bot import get_chat_response, transcribe_audio, TEMP_AUDIO_DIR

router = APIRouter()

@router.post("/chat/", response_model=ChatMessageResponse)
def chat_with_bot(request: ChatMessageRequest):
    # Running this synchronously prevents event loop deadlock when GeminiWrapper 
    # makes a local HTTP request back to this same FastAPI server to fetch media.
    reply = get_chat_response(
        message=request.message,
        user_id=request.user_id
    )
    return ChatMessageResponse(reply=reply)

@router.post("/chat/transcribe/", response_model=TranscribeResponse)
def chat_transcribe(request: VoiceMessageRequest):
    # Dedicated endpoint for transcribing voice messages
    text = transcribe_audio(
        audio_base64=request.audio_base64
    )
    return TranscribeResponse(text=text)

@router.get("/chat/media/{filename}")
def get_chat_media(filename: str):
    """
    Serves temporary audio files so GeminiWrapper can download them via HTTP.
    """
    filepath = os.path.join(TEMP_AUDIO_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="audio/webm")
    return {"error": "File not found"}, 404
