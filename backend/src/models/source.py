from pydantic import BaseModel
from typing import Optional


class Source(BaseModel):
    """
    Represents a source document referenced in a response
    """
    source_id: str
    file_path: str  # Relative path to the source file in /docs/
    content_snippet: str  # Excerpt from the source that was referenced
    relevance_score: float  # How relevant this source was to the response (0-1)