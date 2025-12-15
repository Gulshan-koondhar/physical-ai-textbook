from fastapi import APIRouter
from typing import Dict, Any
import time
import logging

from ..services.qdrant_service import qdrant_service
from ..services.postgres_service import postgres_service

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Checks the health status of the backend service.
    """
    start_time = time.time()
    logger.info("Health check initiated")

    # Check dependencies
    dependencies_status = {}

    # Check Qdrant connection
    try:
        # Try to get collection info to verify connection
        collection_info = qdrant_service.client.get_collection(qdrant_service.collection_name)
        dependencies_status["qdrant"] = "connected"
        logger.info("Qdrant connection: OK")
    except Exception as e:
        dependencies_status["qdrant"] = f"error: {str(e)}"
        logger.error(f"Qdrant connection failed: {str(e)}")

    # Check Postgres connection
    try:
        pool = await postgres_service.get_pool()
        connection = await pool.acquire()
        await connection.fetchval("SELECT 1")
        await pool.release(connection)
        dependencies_status["postgres"] = "connected"
        logger.info("Postgres connection: OK")
    except Exception as e:
        dependencies_status["postgres"] = f"error: {str(e)}"
        logger.error(f"Postgres connection failed: {str(e)}")

    # Check if we can access the embedding service (just check if env var is set)
    import os
    if os.getenv("OPENAI_API_KEY"):
        dependencies_status["openai"] = "configured"  # Embedding service
        logger.info("OpenAI API (embeddings) configured")
    else:
        dependencies_status["openai"] = "not configured"
        logger.warning("OpenAI API (embeddings) not configured")

    # Check if we can access the Gemini service (just check if env var is set)
    if os.getenv("GEMINI_API_KEY"):
        dependencies_status["gemini"] = "configured"
        logger.info("Gemini API configured")
    else:
        dependencies_status["gemini"] = "not configured"
        logger.warning("Gemini API not configured")

    # Calculate response time
    response_time = round((time.time() - start_time) * 1000, 2)  # in milliseconds

    # Determine overall status
    overall_status = "healthy" if all("connected" in status or "configured" in status
                                      for status in dependencies_status.values()) else "degraded"

    logger.info(f"Health check completed with status: {overall_status}, response time: {response_time}ms")

    return {
        "status": overall_status,
        "timestamp": time.time(),
        "response_time_ms": response_time,
        "dependencies": dependencies_status
    }