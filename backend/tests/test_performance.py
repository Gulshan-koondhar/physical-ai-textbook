"""
Performance tests for the Physical AI Textbook RAG Chatbot
These tests verify that response times meet the <5s requirement (SC-004)
"""
import pytest
import asyncio
import time
from unittest.mock import AsyncMock, MagicMock
from src.models.user_query import UserQuery
from src.services.rag_service import RAGService
from datetime import datetime


class TestPerformance:
    """Performance tests to ensure <5s response times"""

    @pytest.fixture
    def setup_performance_services(self):
        """Setup services for performance testing"""
        rag_service = RAGService()
        # Mock external dependencies to focus on performance of internal logic
        rag_service.qdrant_service = MagicMock()
        rag_service.embedding_service = MagicMock()
        rag_service.gemini_service = MagicMock()
        return rag_service

    @pytest.mark.asyncio
    async def test_response_time_under_5_seconds_general_query(self, setup_performance_services):
        """
        Test that general queries respond in under 5 seconds
        Success criterion SC-004: At least 95% of user queries receive responses within 5 seconds
        """
        rag_service = setup_performance_services

        # Mock services to simulate realistic response times
        async def mock_create_embedding(text):
            # Simulate embedding service delay
            await asyncio.sleep(0.1)
            return [0.1, 0.2, 0.3, 0.4, 0.5] * 307  # 1536 dimensions like OpenAI

        async def mock_search_vectors(query_vector, limit=10, metadata_filter=None):
            # Simulate Qdrant search delay
            await asyncio.sleep(0.2)
            # Return mock search results
            results = []
            for i in range(limit):
                mock_result = MagicMock()
                mock_result.payload = {
                    'content': f'Relevant content snippet {i} for performance testing',
                    'metadata': {'file_path': f'/docs/performance-test-{i}.md'}
                }
                mock_result.score = 0.9 - (i * 0.05)
                results.append(mock_result)
            return results

        async def mock_generate_response_with_sources(prompt, sources):
            # Simulate Gemini API delay
            await asyncio.sleep(0.5)
            return {
                'content': f'Performance test response to: {prompt}',
                'sources': [
                    {
                        'file_path': source['file_path'],
                        'content_snippet': source['content_snippet'],
                        'relevance_score': source.get('relevance_score', 0.8)
                    } for source in sources
                ] if sources else []
            }

        rag_service.embedding_service.create_embedding = mock_create_embedding
        rag_service.qdrant_service.search_vectors = mock_search_vectors
        rag_service.gemini_service.generate_response_with_sources = mock_generate_response_with_sources

        # Create a test query
        query = UserQuery(
            query_id="perf_test_1",
            session_id="perf_session_1",
            query_text="What is the performance of this system?",
            query_type="general",
            selected_text=None,
            timestamp=datetime.now()
        )

        # Measure response time
        start_time = time.time()
        response = await rag_service.query_textbook(query)
        end_time = time.time()

        response_time = end_time - start_time

        # Verify response time is under 5 seconds
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeded 5 seconds"
        print(f"General query response time: {response_time:.2f}s")

    @pytest.mark.asyncio
    async def test_response_time_under_5_seconds_selected_text_query(self, setup_performance_services):
        """
        Test that selected text queries respond in under 5 seconds
        """
        rag_service = setup_performance_services

        # Mock Gemini service only (selected text doesn't use embedding/Qdrant)
        async def mock_generate_response_with_sources(prompt, sources):
            # Simulate Gemini API delay (faster for selected text since no RAG needed)
            await asyncio.sleep(0.3)
            return {
                'content': f'Performance test response for selected text: {prompt}',
                'sources': [
                    {
                        'file_path': 'selected_text',
                        'content_snippet': 'Performance test selected content',
                        'relevance_score': 1.0
                    }
                ]
            }

        rag_service.gemini_service.generate_response_with_sources = mock_generate_response_with_sources

        # Create a test query with selected text
        query = UserQuery(
            query_id="perf_test_2",
            session_id="perf_session_2",
            query_text="Explain this performance concept?",
            query_type="selected_text",
            selected_text="Performance test selected content",
            timestamp=datetime.now()
        )

        # Measure response time
        start_time = time.time()
        response = await rag_service.query_textbook(query)
        end_time = time.time()

        response_time = end_time - start_time

        # Verify response time is under 5 seconds
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeded 5 seconds"
        print(f"Selected text query response time: {response_time:.2f}s")

    @pytest.mark.asyncio
    async def test_multiple_concurrent_queries_performance(self, setup_performance_services):
        """
        Test performance under concurrent load
        """
        rag_service = setup_performance_services

        # Mock services
        async def mock_create_embedding(text):
            await asyncio.sleep(0.05)  # Faster for this test
            return [0.1, 0.2, 0.3, 0.4, 0.5] * 307

        async def mock_search_vectors(query_vector, limit=10, metadata_filter=None):
            await asyncio.sleep(0.1)  # Faster for this test
            results = []
            for i in range(min(limit, 3)):  # Fewer results for faster test
                mock_result = MagicMock()
                mock_result.payload = {
                    'content': f'Content {i}',
                    'metadata': {'file_path': f'/docs/test-{i}.md'}
                }
                mock_result.score = 0.9 - (i * 0.1)
                results.append(mock_result)
            return results

        async def mock_generate_response_with_sources(prompt, sources):
            await asyncio.sleep(0.2)  # Faster for this test
            return {
                'content': f'Response to: {prompt}',
                'sources': [
                    {
                        'file_path': source['file_path'] if 'file_path' in source else '/docs/default.md',
                        'content_snippet': source.get('content_snippet', 'default content'),
                        'relevance_score': source.get('relevance_score', 0.8)
                    } for source in sources
                ] if sources else []
            }

        rag_service.embedding_service.create_embedding = mock_create_embedding
        rag_service.qdrant_service.search_vectors = mock_search_vectors
        rag_service.gemini_service.generate_response_with_sources = mock_generate_response_with_sources

        # Create multiple concurrent queries
        queries = []
        for i in range(5):  # Test with 5 concurrent queries
            query = UserQuery(
                query_id=f"concurrent_test_{i}",
                session_id=f"session_{i}",
                query_text=f"Concurrent query {i}",
                query_type="general",
                selected_text=None,
                timestamp=datetime.now()
            )
            queries.append(query)

        # Measure time for all queries
        start_time = time.time()

        # Execute queries concurrently
        tasks = [rag_service.query_textbook(query) for query in queries]
        responses = await asyncio.gather(*tasks)

        end_time = time.time()

        total_time = end_time - start_time
        avg_response_time = total_time / len(queries)

        # Verify average response time is under 5 seconds
        assert avg_response_time < 5.0, f"Average response time {avg_response_time:.2f}s exceeded 5 seconds"
        assert total_time < 10.0, f"Total time for {len(queries)} queries ({total_time:.2f}s) seems excessive"

        print(f"Concurrent queries - Total time: {total_time:.2f}s, Average: {avg_response_time:.2f}s")
        print(f"All {len(responses)} queries completed successfully")