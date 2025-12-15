from pydantic import BaseModel
from typing import List
from datetime import datetime


class Response(BaseModel):
    """
    Represents the AI-generated answer to a user query
    """
    response_id: str
    query_id: str
    session_id: str
    content: str  # The AI-generated response text
    sources: List['Source']  # Sources used to generate the response using forward reference
    timestamp: datetime
    model_used: str  # Which AI model was used to generate the response (e.g., gemini-2.5-flash)


# Forward reference resolution
from .source import Source  # noqa: E402