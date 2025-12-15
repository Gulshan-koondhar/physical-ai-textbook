"""
Tests to verify source citations are displayed with every answer (SC-002, SC-003)
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from src.models.user_query import UserQuery
from src.services.rag_service import RAGService
from datetime import datetime


class TestSourceCitations:
    """Tests to verify source citations are displayed with every answer"""

    @pytest.fixture
    def setup_citation_services(self):
        """Setup services for citation testing"""
        rag_service = RAGService()
        rag_service.qdrant_service = MagicMock()
        rag_service.embedding_service = MagicMock()
        rag_service.gemini_service = MagicMock()
        return rag_service

    @pytest.mark.asyncio
    async def test_general_query_returns_source_citations(self, setup_citation_services):
        """
        Test that general queries return source citations (SC-002)
        Success criterion: Answers to at least 10 different test questions about textbook content
        are accurate and include proper source citations
        """
        rag_service = setup_citation_services

        # Mock embedding service
        async def mock_create_embedding(text):
            return [0.1, 0.2, 0.3, 0.4, 0.5] * 307  # 1536 dimensions

        # Mock Qdrant service to return search results with metadata
        async def mock_search_vectors(query_vector, limit=10, metadata_filter=None):
            results = []
            for i in range(2):  # Return 2 sources
                mock_result = MagicMock()
                mock_result.payload = {
                    'content': f'Relevant content snippet {i} about the topic',
                    'metadata': {
                        'file_path': f'/docs/chapter-{i+1}/section-{i+1}.md',
                        'title': f'Section {i+1}'
                    }
                }
                mock_result.score = 0.9 - (i * 0.1)
                results.append(mock_result)
            return results

        # Mock Gemini service to return response with sources
        async def mock_generate_response_with_sources(prompt, sources):
            return {
                'content': f'Answer based on the provided sources: {prompt}',
                'sources': [
                    {
                        'file_path': f'/docs/chapter-{i+1}/section-{i+1}.md',
                        'content_snippet': f'Relevant content snippet {i} about the topic',
                        'relevance_score': 0.9 - (i * 0.1)
                    } for i in range(len(sources)) if sources
                ] or [
                    {
                        'file_path': '/docs/chapter-1/introduction.md',
                        'content_snippet': 'Default relevant content',
                        'relevance_score': 0.8
                    }
                ]
            }

        rag_service.embedding_service.create_embedding = mock_create_embedding
        rag_service.qdrant_service.search_vectors = mock_search_vectors
        rag_service.gemini_service.generate_response_with_sources = mock_generate_response_with_sources

        # Test multiple general queries
        test_queries = [
            "What is ROS?",
            "Explain Gazebo simulation",
            "Describe VLA models",
            "How does NVIDIA Isaac Sim work?",
            "What are the key concepts in robotics?"
        ]

        for query_text in test_queries:
            query = UserQuery(
                query_id=f"citation_test_{hash(query_text) % 10000}",
                session_id="citation_session_1",
                query_text=query_text,
                query_type="general",
                selected_text=None,
                timestamp=datetime.now()
            )

            response = await rag_service.query_textbook(query)

            # Verify that the response has content
            assert response.content is not None and len(response.content) > 0

            # Verify that sources are included (SC-002, SC-003)
            assert response.sources is not None, f"No sources found for query: {query_text}"
            assert len(response.sources) > 0, f"No source citations found for query: {query_text}"

            # Verify each source has required fields
            for source in response.sources:
                assert source.file_path is not None, f"Missing file_path in source for query: {query_text}"
                assert source.content_snippet is not None, f"Missing content_snippet in source for query: {query_text}"
                assert source.relevance_score is not None, f"Missing relevance_score in source for query: {query_text}"
                # Verify file path is relative to /docs/ as specified in data model
                assert source.file_path.startswith('/docs/') or source.file_path == 'selected_text', \
                    f"Invalid file path format: {source.file_path} for query: {query_text}"

    @pytest.mark.asyncio
    async def test_selected_text_query_handles_sources_properly(self, setup_citation_services):
        """
        Test that selected text queries handle sources properly (SC-003)
        Success criterion: When users select text and ask about it, 100% of responses
        are based solely on the selected text without retrieving from broader knowledge base
        """
        rag_service = setup_citation_services

        # Mock Gemini service for selected text mode
        async def mock_generate_response_with_sources(prompt, sources):
            return {
                'content': f'Answer based on selected text: {prompt}',
                'sources': [
                    {
                        'file_path': 'selected_text',
                        'content_snippet': 'The selected text content for testing',
                        'relevance_score': 1.0
                    }
                ]
            }

        rag_service.gemini_service.generate_response_with_sources = mock_generate_response_with_sources

        # Create a selected text query
        query = UserQuery(
            query_id="citation_test_selected_1",
            session_id="citation_session_2",
            query_text="Explain this concept?",
            query_type="selected_text",
            selected_text="The selected text content for testing",
            timestamp=datetime.now()
        )

        response = await rag_service.query_textbook(query)

        # Verify response has content
        assert response.content is not None and len(response.content) > 0

        # Verify sources are included and properly marked as selected text
        assert response.sources is not None
        assert len(response.sources) > 0

        # For selected text mode, the source should be marked appropriately
        source = response.sources[0]
        assert source.file_path == 'selected_text', "Selected text query should have 'selected_text' as file_path"
        assert source.content_snippet == 'The selected text content for testing'
        assert source.relevance_score == 1.0

    @pytest.mark.asyncio
    async def test_multiple_source_citations_format(self, setup_citation_services):
        """
        Test that multiple source citations follow proper format
        """
        rag_service = setup_citation_services

        # Mock services to return multiple sources
        async def mock_create_embedding(text):
            return [0.1, 0.2, 0.3, 0.4, 0.5] * 307

        async def mock_search_vectors(query_vector, limit=10, metadata_filter=None):
            results = []
            # Return 3 different sources to test multiple citations
            for i in range(3):
                mock_result = MagicMock()
                mock_result.payload = {
                    'content': f'Comprehensive content about the topic, part {i+1}',
                    'metadata': {
                        'file_path': f'/docs/module-{i+1}/topic-{i+1}.md',
                        'section': f'Section {i+1}',
                        'chapter': f'Chapter {i+1}'
                    }
                }
                mock_result.score = 0.95 - (i * 0.05)  # Decreasing relevance
                results.append(mock_result)
            return results

        async def mock_generate_response_with_sources(prompt, sources):
            return {
                'content': 'Comprehensive answer incorporating information from multiple sources',
                'sources': [
                    {
                        'file_path': f'/docs/module-{i+1}/topic-{i+1}.md',
                        'content_snippet': f'Comprehensive content about the topic, part {i+1}',
                        'relevance_score': 0.95 - (i * 0.05)
                    } for i in range(3)
                ]
            }

        rag_service.embedding_service.create_embedding = mock_create_embedding
        rag_service.qdrant_service.search_vectors = mock_search_vectors
        rag_service.gemini_service.generate_response_with_sources = mock_generate_response_with_sources

        query = UserQuery(
            query_id="citation_test_multiple",
            session_id="citation_session_3",
            query_text="Give a comprehensive overview",
            query_type="general",
            selected_text=None,
            timestamp=datetime.now()
        )

        response = await rag_service.query_textbook(query)

        # Verify multiple sources are included
        assert len(response.sources) == 3, f"Expected 3 sources, got {len(response.sources)}"

        # Verify all sources have proper format and decreasing relevance scores
        for i, source in enumerate(response.sources):
            assert source.file_path == f'/docs/module-{i+1}/topic-{i+1}.md'
            assert f'part {i+1}' in source.content_snippet
            expected_score = 0.95 - (i * 0.05)
            assert abs(source.relevance_score - expected_score) < 0.01