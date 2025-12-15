# Implementation Plan: Integrated RAG Chatbot with Selected-Text Override for Physical AI Textbook

**Branch**: `001-integrated-rag-chatbot` | **Date**: 2025-12-12 | **Spec**: [specs/001-integrated-rag-chatbot/spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-integrated-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a RAG (Retrieval Augmented Generation) chatbot integrated into the Docusaurus-based Physical AI textbook website. The system will allow users to ask questions about textbook content with source citations, and provide a special mode where selected text becomes the exclusive context for answers. The architecture includes a React-based frontend widget using OpenAI ChatKit, a FastAPI backend with Google Gemini integration for responses (while using OpenAI embeddings), and vector storage in Qdrant for textbook content retrieval.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript/TypeScript (frontend)
**Primary Dependencies**: OpenAI ChatKit React SDK, FastAPI, Google Gemini API, Qdrant, Neon Postgres
**Storage**: Qdrant vector database (textbook content embeddings), Neon Serverless Postgres (session data)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web (GitHub Pages frontend, Render.com backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5 second response time for 95% of queries, handle concurrent users without degradation
**Constraints**: Must use OpenAI text-embedding-3-small/large for embeddings, Google Gemini gemini-2.5-flash for responses, deployed on free tiers (Qdrant Cloud Free, Render.com free, Neon free)
**Scale/Scope**: Support textbook content (≥600 chunks), handle student/researcher usage patterns

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Spec-driven development compliance**: ✅ Feature starts with comprehensive specification
**Clarity and accessibility**: ✅ System designed to be accessible to students and researchers
**Maintainability through versioned documentation**: ✅ Architecture follows Docusaurus standards with proper documentation
**Ethical and accurate use of AI-generated content**: ✅ System prevents hallucination by grounding responses in textbook content only
**Docusaurus Standards Compliance**: ✅ Frontend widget integrates with Docusaurus framework
**Workflow Consistency**: ✅ All development follows Spec-Kit Plus workflows

*Re-evaluation after Phase 1 design:*
**Architecture alignment**: ✅ Design aligns with constitutional principles and feature requirements
**Technology stack compliance**: ✅ Selected technologies match constraints specified in feature requirements
**Documentation completeness**: ✅ All required documentation artifacts created (data model, API contracts, quickstart guide)

## Project Structure

### Documentation (this feature)

```text
specs/001-integrated-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── chat_session.py
│   │   ├── knowledge_chunk.py
│   │   └── query_response.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── embedding_service.py
│   │   ├── qdrant_service.py
│   │   ├── postgres_service.py
│   │   └── gemini_service.py
│   ├── api/
│   │   ├── chat_endpoints.py
│   │   ├── health_endpoints.py
│   │   └── session_endpoints.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   ├── ChatWidget.jsx
│   │   ├── ChatInterface.jsx
│   │   ├── MessageDisplay.jsx
│   │   └── SourceCitation.jsx
│   ├── services/
│   │   ├── apiClient.js
│   │   └── textSelection.js
│   └── utils/
│       └── chatUtils.js
├── tests/
│   ├── unit/
│   └── integration/
└── package.json
```

**Structure Decision**: Web application structure chosen to separate frontend (Docusaurus integration) from backend (API and RAG services). Backend uses FastAPI for Python-based API with async capabilities. Frontend uses React components that integrate with Docusaurus via custom plugins.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
