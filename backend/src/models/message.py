from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    """
    Represents a single message in the conversation
    """
    message_id: str
    session_id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    sources: Optional[List['Source']] = None  # Using string annotation to avoid circular import


# Forward reference resolution
from .source import Source  # noqa: E402