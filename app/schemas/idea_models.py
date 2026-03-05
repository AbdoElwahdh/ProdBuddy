from pydantic import BaseModel
from typing import Optional

class IdeaCreate(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
