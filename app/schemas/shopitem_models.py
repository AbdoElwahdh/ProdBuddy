from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShopItemCreate(BaseModel):
    user_id: str
    item_name: str
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None

class ShopItemUpdate(BaseModel):
    item_name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
