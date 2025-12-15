import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.rag_service import RAGService
from src.models.user_query import UserQuery
from datetime import datetime


class TestRAGService:
    """Test suite for RAG Service functionality"""

    @pytest.fixture
    def rag_service(self):
        """Create a RAG service instance for testing"""
        service = RAGService()
        # Mock the dependencies
        service.qdrant_service = MagicMock()
        service.embedding_service = MagicMock()
        service.gemini_service = MagicMock()
        return service

    @pytest.mark.asyncio
    async def test_query_textbook_general_mode(self, rag_service):
        """Test querying textbook in general mode"""
        # Arrange
        query = UserQuery(
            query_id="test_query_1",
            session_id="test_session_1",
            query_text="What is ROS?",
            query_type="general",
            selected_text=None,
            timestamp=datetime.now()
        )

        # Mock embedding service
        rag_service.embedding_service.create_embedding.return_value = [0.1, 0.2, 0.3]

        # Mock Qdrant service
        mock_search_result = [
            MagicMock(payload={'content': 'ROS is a robotics framework', 'metadata': {'file_path': '/docs/ros.md'}}, score=0.9)
        ]
        rag_service.qdrant_service.search_vectors = AsyncMock(return_value=mock_search_result)

        # Mock Gemini service
        mock_response = {
            'content': 'ROS (Robot Operating System) is a flexible framework for writing robot software.',
            'sources': [{'file_path': '/docs/ros.md', 'content_snippet': 'ROS is a robotics framework', 'relevance_score': 0.9}]
        }
        rag_service.gemini_service.generate_response_with_sources = AsyncMock(return_value=mock_response)

        # Act
        result = await rag_service.query_textbook(query)

        # Assert
        assert result.content == 'ROS (Robot Operating System) is a flexible framework for writing robot software.'
        assert len(result.sources) == 1
        assert result.sources[0].file_path == '/docs/ros.md'
        assert result.sources[0].relevance_score == 0.9

    @pytest.mark.asyncio
    async def test_query_textbook_selected_text_mode(self, rag_service):
        """Test querying textbook in selected text mode"""
        # Arrange
        query = UserQuery(
            query_id="test_query_2",
            session_id="test_session_2",
            query_text="Explain this concept?",
            query_type="selected_text",
            selected_text="Gazebo is a 3D simulation environment for robotics",
            timestamp=datetime.now()
        )

        # Mock Gemini service
        mock_response = {
            'content': 'Gazebo provides a realistic 3D simulation environment for testing robotics algorithms.',
            'sources': [{'file_path': 'selected_text', 'content_snippet': 'Gazebo is a 3D simulation environment for robotics', 'relevance_score': 1.0}]
        }
        rag_service.gemini_service.generate_response_with_sources = AsyncMock(return_value=mock_response)

        # Act
        result = await rag_service.query_textbook(query)

        # Assert
        assert result.content == 'Gazebo provides a realistic 3D simulation environment for testing robotics algorithms.'
        assert len(result.sources) == 1
        assert result.sources[0].file_path == 'selected_text'
        assert result.sources[0].content_snippet == 'Gazebo is a 3D simulation environment for robotics'

    @pytest.mark.asyncio
    async def test_query_textbook_invalid_query_type(self, rag_service):
        """Test querying with invalid query type raises error"""
        # Arrange
        query = UserQuery(
            query_id="test_query_3",
            session_id="test_session_3",
            query_text="What is this?",
            query_type="invalid_type",
            selected_text=None,
            timestamp=datetime.now()
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Unknown query type: invalid_type"):
            await rag_service.query_textbook(query)

    @pytest.mark.asyncio
    async def test_index_textbook_content(self, rag_service):
        """Test indexing textbook content"""
        # Arrange
        chunks = [
            {
                'chunk_id': 'chunk_1',
                'content': 'This is the first chunk of content',
                'file_path': '/docs/chapter1.md',
                'metadata': {'section': 'introduction'}
            }
        ]

        # Mock embedding service
        rag_service.embedding_service.create_embeddings.return_value = [[0.1, 0.2, 0.3]]

        # Mock Qdrant service
        rag_service.qdrant_service.upsert_vectors = AsyncMock()

        # Act
        await rag_service.index_textbook_content(chunks)

        # Assert
        rag_service.embedding_service.create_embeddings.assert_called_once()
        rag_service.qdrant_service.upsert_vectors.assert_called_once()