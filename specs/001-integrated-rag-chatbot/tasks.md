# Implementation Tasks: Integrated RAG Chatbot with Selected-Text Override for Physical AI Textbook

**Feature**: Integrated RAG Chatbot with Selected-Text Override for Physical AI Textbook
**Branch**: `001-integrated-rag-chatbot`
**Generated**: 2025-12-12
**Input**: Feature specification from `/specs/001-integrated-rag-chatbot/spec.md`

## Implementation Strategy

Build the RAG chatbot in phases, starting with the core infrastructure and API, then implementing the three user stories in priority order. The approach will be MVP-first, with User Story 1 (P1) as the minimum viable product, followed by User Story 2 (P2) and User Story 3 (P3). Each user story will be independently testable.

## Phase 1: Setup Tasks

- [X] T001 Create backend directory structure per plan: `backend/src/models`, `backend/src/services`, `backend/src/api`, `backend/tests`
- [X] T002 Create frontend directory structure per plan: `frontend/src/components`, `frontend/src/services`, `frontend/src/utils`, `frontend/tests`
- [X] T003 [P] Initialize backend requirements.txt with FastAPI, pydantic, qdrant-client, asyncpg, psycopg[binary], google-generativeai, python-dotenv
- [X] T004 [P] Initialize frontend package.json with react, react-dom, openai-chat-widget, axios, @docusaurus/core, @docusaurus/module-type-aliases
- [X] T005 Set up environment configuration files (.env.example) for both backend and frontend

## Phase 2: Foundational Tasks

- [X] T006 [P] Create ChatSession model in backend/src/models/chat_session.py with all required fields per data model
- [X] T007 [P] Create Message model in backend/src/models/message.py with all required fields per data model
- [X] T008 [P] Create Source model in backend/src/models/source.py with all required fields per data model
- [X] T009 [P] Create KnowledgeChunk model in backend/src/models/knowledge_chunk.py with all required fields per data model
- [X] T010 [P] Create UserQuery model in backend/src/models/user_query.py with all required fields per data model
- [X] T011 [P] Create Response model in backend/src/models/response.py with all required fields per data model
- [X] T012 Create database connection service in backend/src/services/postgres_service.py
- [X] T013 Create Qdrant vector database service in backend/src/services/qdrant_service.py
- [X] T014 Create embedding service in backend/src/services/embedding_service.py using OpenAI text-embedding-3-small
- [X] T015 Create Gemini service in backend/src/services/gemini_service.py using Google Gemini API
- [X] T016 Create RAG service in backend/src/services/rag_service.py implementing two-mode functionality
- [X] T017 Create API health endpoint in backend/src/api/health_endpoints.py with dependencies check
- [X] T018 Create basic FastAPI main application in backend/src/main.py with CORS and health endpoints
- [X] T019 [P] Create API client service in frontend/src/services/apiClient.js
- [X] T020 [P] Create text selection utility in frontend/src/services/textSelection.js

## Phase 3: [US1] Chat with Textbook Content

**User Story Goal**: As a student reading the Physical AI textbook online, I want to ask questions about the content I'm reading so that I can get immediate answers from the textbook itself without having to search through pages or external resources.

**Independent Test Criteria**: Can be fully tested by asking various questions about the textbook content and verifying that the answers come from the textbook with proper source citations.

- [X] T021 [US1] Implement chat endpoint in backend/src/api/chat_endpoints.py for general textbook Q&A
- [X] T022 [US1] Create session creation endpoint in backend/src/api/chat_endpoints.py (POST /api/chat/new-session)
- [X] T023 [US1] Create session history endpoint in backend/src/api/chat_endpoints.py (GET /api/chat/session/{session_id})
- [X] T024 [US1] Implement RAG service logic for general textbook queries with source citations
- [X] T025 [US1] Create ChatWidget component in frontend/src/components/ChatWidget.jsx with OpenAI ChatKit integration
- [X] T026 [US1] Create ChatInterface component in frontend/src/components/ChatInterface.jsx
- [X] T027 [US1] Create MessageDisplay component in frontend/src/components/MessageDisplay.jsx
- [X] T028 [US1] Create SourceCitation component in frontend/src/components/SourceCitation.jsx
- [X] T029 [US1] Integrate chat widget with backend API calls
- [X] T030 [US1] Test User Story 1 functionality with sample textbook questions

## Phase 4: [US2] Query Selected Text Only

**User Story Goal**: As a researcher studying specific sections of the textbook, I want to highlight text and ask questions specifically about that selected text so that I can get contextually relevant answers without interference from the broader knowledge base.

**Independent Test Criteria**: Can be fully tested by selecting text on a page, triggering the chat function, and verifying that responses are based only on the selected text rather than general textbook knowledge.

- [X] T031 [US2] Enhance RAG service to support selected-text-only mode
- [X] T032 [US2] Update chat endpoint to handle query_type='selected_text' and selected_text parameter
- [X] T033 [US2] Implement text selection capture mechanism in frontend/src/services/textSelection.js
- [X] T034 [US2] Add "Ask about selection" functionality to ChatWidget component
- [X] T035 [US2] Ensure selected-text mode bypasses RAG retrieval and uses only provided text as context
- [X] T036 [US2] Test User Story 2 functionality with selected text scenarios

## Phase 5: [US3] Persistent Chat Interface

**User Story Goal**: As a user reading through the textbook, I want the chatbot interface to remain accessible and not interfere with my reading experience so that I can seamlessly switch between reading and asking questions.

**Independent Test Criteria**: Can be fully tested by navigating through different pages while keeping the chat interface visible and functional without interfering with page scrolling or content readability.

- [X] T037 [US3] Create persistent chat interface that works across Docusaurus pages
- [X] T038 [US3] Implement fixed positioning for chat widget that doesn't interfere with page scrolling
- [X] T039 [US3] Add Docusaurus plugin integration to embed chat widget on all pages
- [X] T040 [US3] Ensure chat widget remains accessible when navigating between textbook pages
- [X] T041 [US3] Test User Story 3 functionality with page navigation and scrolling

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T042 Implement proper error handling and validation for all API endpoints
- [X] T043 Add comprehensive logging for debugging and monitoring
- [X] T044 Implement rate limiting and security measures
- [X] T045 Add proper loading states and user feedback in frontend components
- [X] T046 Create comprehensive test suite for backend services
- [X] T047 Create comprehensive test suite for frontend components
- [X] T048 Set up deployment configuration for Render.com backend
- [X] T049 Set up Docusaurus integration for GitHub Pages frontend deployment
- [X] T050 Conduct end-to-end testing of all user stories
- [X] T051 Performance testing to ensure <5s response times (SC-004)
- [X] T052 Verify source citations are displayed with every answer (SC-002, SC-003)
- [X] T053 Verify no hallucination occurs (SC-007)
- [X] T054 Document deployment process and update quickstart guide

## Dependencies

- **User Story 2** depends on foundational tasks from Phase 2 (services and models)
- **User Story 3** depends on User Story 1 (basic chat functionality)
- **User Story 3** depends on User Story 2 (full functionality available)

## Parallel Execution Examples

**User Story 1 Tasks that can run in parallel:**
- T021, T022, T023 (API endpoints)
- T025, T026, T027, T028 (Frontend components)

**User Story 2 Tasks that can run in parallel:**
- T031, T032 (Backend enhancements)
- T033, T034 (Frontend enhancements)

**User Story 3 Tasks that can run in parallel:**
- T037, T038 (UI/UX enhancements)
- T039, T040 (Integration tasks)

## Task Breakdown Summary

- **Setup Tasks**: 5 tasks
- **Foundational Tasks**: 18 tasks
- **User Story 1 (P1)**: 10 tasks
- **User Story 2 (P2)**: 6 tasks
- **User Story 3 (P3)**: 5 tasks
- **Polish & Cross-Cutting**: 21 tasks
- **Total**: 65 tasks

**MVP Scope (User Story 1)**: Tasks T001-T025 (25 tasks) - Basic chat functionality with textbook Q&A and source citations