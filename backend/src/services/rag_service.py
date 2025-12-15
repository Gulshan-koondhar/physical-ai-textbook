from typing import List, Dict, Any, Optional
import logging
from ..models.user_query import UserQuery
from ..models.response import Response as ResponseModel
from ..models.source import Source
from .embedding_service import embedding_service
from .qdrant_service import qdrant_service
from .gemini_service import gemini_service

logger = logging.getLogger(__name__)

class RAGService:
    """
    Service for implementing Retrieval Augmented Generation functionality
    Supports two modes: general textbook Q&A and selected-text-only mode
    """

    def __init__(self):
        self.qdrant_service = qdrant_service
        self.embedding_service = embedding_service
        self.gemini_service = gemini_service

    async def query_textbook(self, query: UserQuery) -> ResponseModel:
        """
        Process a query based on the query type:
        - 'general': Use RAG to retrieve from textbook and generate response
        - 'selected_text': Use only the selected text as context for response
        """
        if query.query_type == 'selected_text':
            return await self._query_selected_text(query)
        elif query.query_type == 'general':
            return await self._query_general_textbook(query)
        else:
            raise ValueError(f"Unknown query type: {query.query_type}")

    async def _query_selected_text(self, query: UserQuery) -> ResponseModel:
        """
        Handle query where response should be based only on selected text
        """
        if not query.selected_text:
            raise ValueError("Selected text is required for selected_text query type")

        # Generate response using only the selected text as context
        result = await self.gemini_service.generate_response_with_sources(
            prompt=query.query_text,
            sources=[{
                'file_path': 'selected_text',
                'content_snippet': query.selected_text,
                'relevance_score': 1.0
            }]
        )

        # Create response object
        response = ResponseModel(
            response_id=f"resp_{query.query_id}",
            query_id=query.query_id,
            session_id=query.session_id,
            content=result['content'],
            sources=[
                Source(
                    source_id=f"src_{query.query_id}_0",
                    file_path='selected_text',
                    content_snippet=query.selected_text,
                    relevance_score=1.0
                )
            ],
            timestamp=query.timestamp,
            model_used='gemini-2.5-flash'
        )

        return response

    async def _query_general_textbook(self, query: UserQuery) -> ResponseModel:
        """
        Handle general query using RAG to retrieve from textbook
        """
        # Create embedding for the query
        query_embedding = await self.embedding_service.create_embedding(query.query_text)

        # Search for relevant chunks in Qdrant
        search_results = await self.qdrant_service.search_vectors(
            query_vector=query_embedding,
            limit=5,  # Retrieve top 5 most relevant chunks
            metadata_filter=None  # No specific filters for general queries
        )

        # Extract sources from search results
        sources = []
        for result in search_results:
            if result.payload and 'metadata' in result.payload:
                metadata = result.payload['metadata']
                sources.append({
                    'file_path': metadata.get('file_path', 'unknown'),
                    'content_snippet': result.payload.get('content', ''),
                    'relevance_score': result.score
                })

        # Generate response using retrieved sources
        result = await self.gemini_service.generate_response_with_sources(
            prompt=query.query_text,
            sources=sources
        )

        # Create response object with proper Source models
        response_sources = []
        for i, source in enumerate(result['sources']):
            response_sources.append(
                Source(
                    source_id=f"src_{query.query_id}_{i}",
                    file_path=source['file_path'],
                    content_snippet=source['content_snippet'],
                    relevance_score=source['relevance_score']
                )
            )

        response = ResponseModel(
            response_id=f"resp_{query.query_id}",
            query_id=query.query_id,
            session_id=query.session_id,
            content=result['content'],
            sources=response_sources,
            timestamp=query.timestamp,
            model_used='gemini-2.5-flash'
        )

        return response

    async def index_textbook_content(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Index textbook content for RAG retrieval
        """
        # Extract texts for embedding
        texts = [chunk['content'] for chunk in chunks]

        # Create embeddings
        embeddings = await self.embedding_service.create_embeddings(texts)

        # Prepare points for Qdrant
        points = []
        for i, chunk in enumerate(chunks):
            points.append({
                'id': chunk['chunk_id'],
                'vector': embeddings[i],
                'payload': {
                    'content': chunk['content'],
                    'metadata': {
                        'file_path': chunk['file_path'],
                        'chunk_id': chunk['chunk_id'],
                        **chunk.get('metadata', {})
                    }
                }
            })

        # Upsert vectors to Qdrant
        await self.qdrant_service.upsert_vectors(points)

# Global instance
rag_service = RAGService()