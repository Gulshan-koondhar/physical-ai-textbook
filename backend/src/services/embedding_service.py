import google.generativeai as genai
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class EmbeddingService:
    """
    Service for generating embeddings using Google Gemini API
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        self.model = "embedding-001"  # Gemini embedding model
        self.dimensions = 768  # Dimensions for Gemini embedding model

    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text"""
        response = await genai.embed_content_async(
            model=self.model,
            content=text,
            task_type="RETRIEVAL_QUERY"  # Appropriate task type for RAG queries
        )
        return response['embedding']

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts"""
        if not texts:
            return []

        # Process embeddings for all texts at once using Gemini API
        # Gemini API can handle multiple texts in one call
        response = await genai.embed_content_async(
            model=self.model,
            content=texts,
            task_type="RETRIEVAL_DOCUMENT"  # Appropriate task type for document embeddings
        )

        return response['embeddings']

# Global instance
embedding_service = EmbeddingService()