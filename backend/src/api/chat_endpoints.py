from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any, List
import uuid
from datetime import datetime
import logging
from pydantic import BaseModel, field_validator

from ..models.user_query import UserQuery
from ..models.response import Response as ResponseModel
from ..services.rag_service import rag_service
from ..services.postgres_service import postgres_service

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response models for API
class ChatRequest(BaseModel):
    session_id: str
    message: str
    query_type: str = "general"  # 'general' or 'selected_text'
    selected_text: str = None  # Required if query_type is 'selected_text'

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > 10000:  # Max 10k characters
            raise ValueError('Message too long, maximum 10000 characters')
        return v

    @field_validator('query_type')
    @classmethod
    def validate_query_type(cls, v):
        if v not in ['general', 'selected_text']:
            raise ValueError('query_type must be either "general" or "selected_text"')
        return v


class ChatResponse(BaseModel):
    response_id: str
    session_id: str
    message: str
    sources: List[Dict[str, Any]]
    timestamp: datetime


class NewSessionRequest(BaseModel):
    user_id: str = None
    metadata: Dict[str, Any] = {}

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError('user_id too long, maximum 100 characters')
        return v


class NewSessionResponse(BaseModel):
    session_id: str
    created_at: datetime


class SessionHistoryResponse(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message and return a response.
    Supports both general textbook Q&A and selected-text-only modes.
    """
    try:
        # Validate request
        if request.query_type == "selected_text" and not request.selected_text:
            raise HTTPException(
                status_code=400,
                detail="selected_text is required when query_type is 'selected_text'"
            )

        # Validate selected_text if provided
        if request.selected_text and len(request.selected_text) > 5000:
            raise HTTPException(
                status_code=400,
                detail="selected_text is too long, maximum 5000 characters"
            )

        logger.info(f"Processing chat request for session {request.session_id}, query_type: {request.query_type}")

        # Create a UserQuery object
        user_query = UserQuery(
            query_id=str(uuid.uuid4()),
            session_id=request.session_id,
            query_text=request.message,
            query_type=request.query_type,
            selected_text=request.selected_text,
            timestamp=datetime.now()
        )

        # Process the query using RAG service
        response = await rag_service.query_textbook(user_query)

        logger.info(f"Successfully processed chat request for session {request.session_id}")

        # Return the response
        return ChatResponse(
            response_id=response.response_id,
            session_id=response.session_id,
            message=response.content,
            sources=[
                {
                    "file_path": source.file_path,
                    "content_snippet": source.content_snippet,
                    "relevance_score": source.relevance_score
                }
                for source in response.sources
            ],
            timestamp=response.timestamp
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@router.post("/chat/new-session", response_model=NewSessionResponse)
async def create_new_session(request: NewSessionRequest) -> NewSessionResponse:
    """
    Create a new chat session.
    """
    try:
        logger.info("Creating new chat session")

        session_id = str(uuid.uuid4())
        created_at = datetime.now()

        # In a real implementation, you would store session info in the database
        # For now, we just return the session ID
        response = NewSessionResponse(
            session_id=session_id,
            created_at=created_at
        )

        logger.info(f"Created new session with ID: {session_id}")
        return response
    except Exception as e:
        logger.error(f"Error creating new session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error creating new session: {str(e)}")


@router.get("/chat/session/{session_id}", response_model=SessionHistoryResponse)
async def get_session_history(session_id: str) -> SessionHistoryResponse:
    """
    Retrieve the history of a chat session.
    """
    try:
        logger.info(f"Retrieving session history for session {session_id}")

        # Validate session_id format
        if not session_id or len(session_id) > 100:
            raise HTTPException(
                status_code=400,
                detail="Invalid session_id format"
            )

        # In a real implementation, you would fetch session history from the database
        # For now, return an empty history
        response = SessionHistoryResponse(
            session_id=session_id,
            messages=[]  # Placeholder - would come from DB in real implementation
        )

        logger.info(f"Retrieved session history for session {session_id}")
        return response
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error retrieving session history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving session history: {str(e)}")


@router.delete("/session/{session_id}")
async def delete_session(session_id: str) -> Dict[str, str]:
    """
    Delete a chat session.
    """
    try:
        logger.info(f"Deleting session {session_id}")

        # In a real implementation, you would delete session from the database
        # For now, just return success message

        return {"message": f"Session {session_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")