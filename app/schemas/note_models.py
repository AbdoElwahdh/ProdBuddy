from pydantic import BaseModel
from typing import Optional

class NoteCreate(BaseModel):
    user_id: str
    content: str
    summary: Optional[str] = None

class NoteUpdate(BaseModel):
    content: Optional[str] = None
    summary: Optional[str] = None
