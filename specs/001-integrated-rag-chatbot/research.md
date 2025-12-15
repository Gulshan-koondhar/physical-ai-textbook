# Research Summary: Integrated RAG Chatbot with Selected-Text Override

## Technology Decisions and Rationale

### Frontend Framework and Integration
- **Decision**: Use OpenAI ChatKit React SDK with custom integration for Docusaurus
- **Rationale**: Provides pre-built chat interface components with OpenAI integration, reducing development time while meeting the requirement to use OpenAI's technology stack
- **Alternatives considered**:
  - Custom React chat component (more development time)
  - Third-party chat widgets (less control over integration)

### Backend Framework
- **Decision**: FastAPI for backend API
- **Rationale**: Python-based, async support, excellent documentation, good integration with OpenAI API and other Python libraries for RAG
- **Alternatives considered**:
  - Flask (less modern, no async built-in)
  - Node.js/Express (would require switching to JavaScript ecosystem)

### Vector Database
- **Decision**: Qdrant Cloud Free Tier for vector storage
- **Rationale**: Meets the constraint of using Qdrant Cloud Free Tier, good Python integration, supports metadata storage for source citations
- **Alternatives considered**:
  - Pinecone (would require different constraint compliance)
  - ChromaDB (self-hosted, doesn't meet cloud requirement)

### Database for Session Storage
- **Decision**: Neon Serverless Postgres for session data
- **Rationale**: Meets the constraint of using Neon Serverless Postgres, serverless scales well, good for session storage
- **Alternatives considered**:
  - SQLite (not meeting constraint)
  - Redis (not meeting constraint)

### Text Embedding Model
- **Decision**: OpenAI text-embedding-3-small model
- **Rationale**: Meets the constraint of using OpenAI text-embedding-3-small or -large, good balance of quality and cost
- **Alternatives considered**:
  - text-embedding-3-large (higher cost)
  - Custom embedding models (not allowed per constraints)

### LLM for Responses
- **Decision**: Google Gemini gemini-2.5-flash for responses
- **Rationale**: Meets the constraint of using Google Gemini gemini-2.5-flash, cost-effective while providing quality responses with multimodal capabilities
- **Alternatives considered**:
  - Gemini Pro (higher cost)
  - Other models (not meeting constraint)

### Deployment Strategy
- **Decision**: GitHub Pages for frontend, Render.com free tier for backend
- **Rationale**: Meets the deployment constraints specified in the feature requirements
- **Alternatives considered**:
  - Vercel for frontend (not specified in constraints)
  - Other backend platforms (not specified in constraints)

## Selected Text Functionality Implementation
- **Decision**: Use JavaScript text selection API with custom event handling
- **Rationale**: Native browser API allows reliable text selection capture across all pages, can be implemented as global event listener
- **Implementation approach**: Add global event listener for text selection, provide "Ask about selection" button that sends selected text to backend as exclusive context

## RAG Implementation Approach
- **Decision**: Two-mode RAG system (general knowledge vs. selected text only)
- **Rationale**: Meets both requirements: general textbook Q&A and selected-text-only mode
- **Implementation approach**:
  - General mode: Retrieve from full textbook vector store, pass to LLM
  - Selected text mode: Skip retrieval step, pass only selected text as context to LLM
- **Quality assurance**: Ensure no hallucination by limiting context to either textbook chunks or selected text only

## Source Citation Strategy
- **Decision**: Extract source information from Qdrant metadata and include in responses
- **Rationale**: Qdrant stores metadata with each chunk including file paths, can be retrieved and displayed with responses
- **Implementation approach**: Store relative file paths from /docs/ directory as metadata in Qdrant, retrieve and format as citations in responses

## Architecture Summary
The system will have three main components:
1. Frontend: Docusaurus-integrated React widget using OpenAI ChatKit
2. Backend: FastAPI service handling RAG logic, session management, and Google Gemini API calls (with OpenAI embeddings)
3. Data stores: Qdrant for vector embeddings, Neon Postgres for session data