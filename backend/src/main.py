import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .api.health_endpoints import router as health_router
from .api.chat_endpoints import router as chat_router  # Will be created later
from .services.postgres_service import postgres_service
from .services.qdrant_service import qdrant_service
from .middleware.rate_limit import rate_limit_middleware
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Physical AI Textbook RAG Chatbot API",
    description="API for the RAG chatbot integrated with the Physical AI textbook",
    version="1.0.0"
)

# Add security and rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for additional security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # In production, replace with specific hosts
)

# Include routers
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting up services...")
    try:
        # Connect to Postgres
        await postgres_service.connect()
        logger.info("Connected to Postgres")
    except Exception as e:
        logger.error(f"Failed to connect to Postgres: {e}")

    try:
        # Initialize Qdrant collection
        await qdrant_service.create_collection()
        logger.info("Qdrant collection ready")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up services on shutdown"""
    logger.info("Shutting down services...")
    try:
        await postgres_service.disconnect()
        logger.info("Disconnected from Postgres")
    except Exception as e:
        logger.error(f"Error disconnecting from Postgres: {e}")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Physical AI Textbook RAG Chatbot API", "status": "running"}

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)