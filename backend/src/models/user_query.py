from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserQuery(BaseModel):
    """
    Represents a query from the user, which may be general or about selected text
    """
    query_id: str
    session_id: str
    query_text: str  # The user's question or query
    query_type: str  # 'general' (RAG from textbook) or 'selected_text' (based only on selected text)
    selected_text: Optional[str] = None  # The text selected by the user (if applicable)
    timestamp: datetime