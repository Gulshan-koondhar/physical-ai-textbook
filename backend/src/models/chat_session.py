from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatSession(BaseModel):
    """
    Represents a user's ongoing conversation with the chatbot
    """
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List['Message'] = []  # Using string annotation to avoid circular import
    metadata: Dict[str, Any] = {}


# Forward reference resolution
from .message import Message  # noqa: E402