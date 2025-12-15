from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class KnowledgeChunk(BaseModel):
    """
    Represents a segment of textbook content stored in the vector database
    """
    chunk_id: str
    content: str  # The text content of the chunk
    file_path: str  # Relative path to the original document in /docs/
    embedding: List[float]  # Vector embedding of the content
    metadata: Dict[str, Any]  # Additional information about the chunk (section, chapter, etc.)
    created_at: datetime