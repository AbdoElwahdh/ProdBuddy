from pydantic import BaseModel
from typing import Optional

class ChatMessageRequest(BaseModel):
    message: str
    user_id: str = "default_user"

class VoiceMessageRequest(BaseModel):
    audio_base64: str
    user_id: str = "default_user"

class ChatMessageResponse(BaseModel):
    reply: str

class TranscribeResponse(BaseModel):
    text: str
