---
id: 1
title: "Integrated RAG Chatbot Specification"
stage: spec
date_iso: 2025-12-12
surface: agent
model: Claude Sonnet 4.5
feature: "001-integrated-rag-chatbot"
branch: "001-integrated-rag-chatbot"
user: "user"
command: "/sp.specify"
labels:
  - "specification"
  - "rag-chatbot"
  - "textbook"
links:
  spec: "specs/001-integrated-rag-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/001-integrated-rag-chatbot/spec.md
  - specs/001-integrated-rag-chatbot/checklists/requirements.md
  - history/prompts/general/001-integrated-rag-chatbot.spec.prompt.md
tests_yaml: |
  - "Specification completeness check"
  - "Quality validation"
prompt_text: |
  Integrated RAG Chatbot with Selected-Text Override for Physical AI Textbook
  Target audience:
  - End users of the live textbook (students, researchers, robotics engineers)
  Focus:
  Fully functional, always-on RAG chatbot embedded in the published Docusaurus book that answers questions exclusively from the textbook content and correctly handles user-selected text as the sole context when provided.
  Success criteria:
  - Chatbot widget is visible and usable on every page of the live GitHub Pages site
  - Answers any question about ROS 2, Gazebo, NVIDIA Isaac Sim, VLA models, etc., accurately and with visible source citations (file paths in /docs/)
  - When user highlights text → clicks "Ask about selection" (or auto-trigger) → response is based 100% on the selected text only (no general retrieval)
  - At least 10 different test questions (general + selected-text) all pass with correct grounding
  - Sources are displayed with every answer (relative Markdown path)
  - No hallucination outside the textbook content (verified by 3 edge-case questions)
  - Backend health endpoint returns 200 OK
  - Qdrant collection `physical-ai-book-v1` contains ≥ 600 chunks with correct metadata
  - Full traceability: every file has /sp.implement header linking back to this spec
  Constraints:
  - Exact stack only:
    → OpenAI ChatKit React SDK (primary) or minimal fallback widget
    → OpenAI Agents / Assistants API or gpt-4o-mini
    → FastAPI backend (Python)
    → Neon Serverless Postgres (session table required even if lightly used)
    → Qdrant Cloud Free Tier
  - All code and content generated exclusively by Claude Code (zero manual edits)
  - Deployment:
    → Frontend = GitHub Pages (already live)
    → Backend = Render.com free tier (or equivalent) with auto-deploy
  - Selected-text capture must work globally across all pages
  - Chatbot must persist (fixed position) and not interfere with page scrolling/reading
  - Must be live and fully functional at submission time
  Not building:
  - Multi-turn memory beyond ChatKit default (not required)
  - User authentication inside the chatbot itself (auth is separate bonus)
  - Personalisation or translation inside the chatbot (separate bonus features)
  - Voice input/output
  - Mobile-specific redesign (desktop-first is acceptable)
  - Custom embedding models (must use OpenAI text-embedding-3-small or -large)
response_text: |
  Created specification for Integrated RAG Chatbot with Selected-Text Override for Physical AI Textbook in branch 001-integrated-rag-chatbot.
  - Created spec file at specs/001-integrated-rag-chatbot/spec.md
  - Created validation checklist at specs/001-integrated-rag-chatbot/checklists/requirements.md
  - All requirements documented with user scenarios, functional requirements, and success criteria
  - Specification validated and ready for planning phase
outcome: |
  Specification successfully created and validated. Ready for planning phase (/sp.plan).
evaluation: |
  The specification meets all quality criteria and is ready for the next phase.
---
