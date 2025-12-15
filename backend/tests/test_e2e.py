"""
End-to-end tests for the Physical AI Textbook RAG Chatbot
These tests verify the integration between components and user story functionality
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.models.user_query import UserQuery
from src.services.rag_service import RAGService
from datetime import datetime


class TestEndToEnd:
    """End-to-end tests for user story functionality"""

    @pytest.fixture
    def setup_services(self):
        """Setup services for end-to-end testing"""
        rag_service = RAGService()
        # Mock external dependencies for testing
        rag_service.qdrant_service = MagicMock()
        rag_service.embedding_service = MagicMock()
        rag_service.gemini_service = MagicMock()
        return rag_service

    @pytest.mark.asyncio
    async def test_user_story_1_general_qa_flow(self, setup_services):
        """
        Test User Story 1: General textbook Q&A with source citations
        As a student, I want to ask questions about textbook content and get answers with source citations
        """
        rag_service = setup_services

        # Mock embedding service to return a test embedding
        rag_service.embedding_service.create_embedding.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]

        # Mock Qdrant service to return relevant search results
        mock_search_results = [
            MagicMock(
                payload={
                    'content': 'ROS (Robot Operating System) is a flexible framework for writing robot software',
                    'metadata': {'file_path': '/docs/ros/introduction.md'}
                },
                score=0.95
            ),
            MagicMock(
                payload={
                    'content': 'ROS provides services like hardware abstraction, device drivers, libraries, and more',
                    'metadata': {'file_path': '/docs/ros/architecture.md'}
                },
                score=0.87
            )
        ]
        rag_service.qdrant_service.search_vectors = AsyncMock(return_value=mock_search_results)

        # Mock Gemini service to return a response with sources
        mock_gemini_response = {
            'content': 'ROS is a flexible framework for writing robot software that provides hardware abstraction, device drivers, libraries, and more.',
            'sources': [
                {
                    'file_path': '/docs/ros/introduction.md',
                    'content_snippet': 'ROS (Robot Operating System) is a flexible framework for writing robot software',
                    'relevance_score': 0.95
                },
                {
                    'file_path': '/docs/ros/architecture.md',
                    'content_snippet': 'ROS provides services like hardware abstraction, device drivers, libraries, and more',
                    'relevance_score': 0.87
                }
            ]
        }
        rag_service.gemini_service.generate_response_with_sources = AsyncMock(return_value=mock_gemini_response)

        # Create a test query
        query = UserQuery(
            query_id="test_e2e_1",
            session_id="session_1",
            query_text="What is ROS?",
            query_type="general",
            selected_text=None,
            timestamp=datetime.now()
        )

        # Execute the query
        response = await rag_service.query_textbook(query)

        # Verify the response
        assert "ROS" in response.content
        assert len(response.sources) == 2
        assert any("introduction.md" in source.file_path for source in response.sources)
        assert any("architecture.md" in source.file_path for source in response.sources)

    @pytest.mark.asyncio
    async def test_user_story_2_selected_text_flow(self, setup_services):
        """
        Test User Story 2: Query selected text only
        As a researcher, I want to ask about selected text and get answers based only on that text
        """
        rag_service = setup_services

        # Mock Gemini service for selected text mode
        mock_gemini_response = {
            'content': 'Gazebo provides a realistic 3D simulation environment that is widely used in robotics research.',
            'sources': [
                {
                    'file_path': 'selected_text',
                    'content_snippet': 'Gazebo is a 3D simulation environment for robotics',
                    'relevance_score': 1.0
                }
            ]
        }
        rag_service.gemini_service.generate_response_with_sources = AsyncMock(return_value=mock_gemini_response)

        # Create a test query with selected text
        query = UserQuery(
            query_id="test_e2e_2",
            session_id="session_2",
            query_text="Explain this concept?",
            query_type="selected_text",
            selected_text="Gazebo is a 3D simulation environment for robotics",
            timestamp=datetime.now()
        )

        # Execute the query
        response = await rag_service.query_textbook(query)

        # Verify the response is based only on the selected text
        assert "Gazebo" in response.content
        assert len(response.sources) == 1
        assert response.sources[0].file_path == 'selected_text'
        assert "3D simulation environment" in response.sources[0].content_snippet

    @pytest.mark.asyncio
    async def test_user_story_3_persistent_interface_simulation(self):
        """
        Test User Story 3: Persistent chat interface (simulated)
        As a user, I want the chat interface to remain accessible across pages
        """
        # This test simulates the persistence by verifying the service can handle
        # multiple requests from different "sessions" (simulating different pages)
        rag_service = RAGService()
        rag_service.qdrant_service = MagicMock()
        rag_service.embedding_service = MagicMock()
        rag_service.gemini_service = MagicMock()

        # Mock responses for multiple queries
        def mock_generate_response_with_sources(prompt, sources):
            return {
                'content': f"Response to: {prompt}",
                'sources': sources if sources else []
            }

        rag_service.gemini_service.generate_response_with_sources = AsyncMock(
            side_effect=mock_generate_response_with_sources
        )

        # Simulate multiple queries from different "pages" (different session IDs)
        sessions = ["session_page_1", "session_page_2", "session_page_3"]
        responses = []

        for i, session_id in enumerate(sessions):
            query = UserQuery(
                query_id=f"query_{i}",
                session_id=session_id,
                query_text=f"Question from page {i+1}",
                query_type="general",
                selected_text=None,
                timestamp=datetime.now()
            )

            # Mock embedding
            rag_service.embedding_service.create_embedding.return_value = [float(i+1) * 0.1] * 5

            # Mock search results
            mock_search_results = [
                MagicMock(
                    payload={
                        'content': f'Content for page {i+1}',
                        'metadata': {'file_path': f'/docs/page{i+1}.md'}
                    },
                    score=0.9
                )
            ]
            rag_service.qdrant_service.search_vectors = AsyncMock(return_value=mock_search_results)

            response = await rag_service.query_textbook(query)
            responses.append(response)

        # Verify that all sessions received responses
        assert len(responses) == 3
        for i, response in enumerate(responses):
            assert f"Question from page {i+1}" in response.content or f"Response to:" in response.content
            assert response.session_id == sessions[i]