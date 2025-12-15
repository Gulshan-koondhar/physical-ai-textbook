# Feature Specification: Integrated RAG Chatbot with Selected-Text Override for Physical AI Textbook

**Feature Branch**: `001-integrated-rag-chatbot`
**Created**: 2025-12-12
**Status**: Draft
**Input**: User description: "Integrated RAG Chatbot with Selected-Text Override for Physical AI Textbook
Target audience:
- End users of the live textbook (students, researchers, robotics engineers)
Focus:
Fully functional, always-on RAG chatbot embedded in the published Docusaurus book that answers questions exclusively from the textbook content and correctly handles user-selected text as the sole context when provided.
Success criteria:
- Chatbot widget is visible and usable on every page of the live GitHub Pages site
- Answers any question about ROS 2, Gazebo, NVIDIA Isaac Sim, VLA models, etc., accurately and with visible source citations (file paths in /docs/)
- When user highlights text → clicks “Ask about selection” (or auto-trigger) → response is based 100% on the selected text only (no general retrieval)
- At least 10 different test questions (general + selected-text) all pass with correct grounding
- Sources are displayed with every answer (relative Markdown path)
- No hallucination outside the textbook content (verified by 3 edge-case questions)
- Backend health endpoint returns 200 OK
- Qdrant collection `physical-ai-book-v1` contains ≥ 600 chunks with correct metadata
- Full traceability: every file has /sp.implement header linking back to this spec
Constraints:
- Exact stack only:
  → OpenAI ChatKit React SDK (primary) or minimal fallback widget
  → Google Gemini API or gemini-2.5-flash
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
- Custom embedding models (must use OpenAI text-embedding-3-small or -large)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chat with Textbook Content (Priority: P1)

As a student reading the Physical AI textbook online, I want to ask questions about the content I'm reading so that I can get immediate answers from the textbook itself without having to search through pages or external resources. I should see the chatbot widget on every page and be able to ask questions about ROS 2, Gazebo, NVIDIA Isaac Sim, VLA models, etc.

**Why this priority**: This is the core value proposition of the feature - providing instant access to textbook knowledge through natural language interaction.

**Independent Test**: Can be fully tested by asking various questions about the textbook content and verifying that the answers come from the textbook with proper source citations.

**Acceptance Scenarios**:

1. **Given** I am viewing any page of the Physical AI textbook, **When** I type a question about the textbook content into the chatbot, **Then** I receive an accurate answer based on the textbook content with source citations showing the document path.
2. **Given** I have asked a question about textbook content, **When** I receive the response, **Then** the response includes specific source citations with file paths from the /docs/ directory.

---

### User Story 2 - Query Selected Text Only (Priority: P2)

As a researcher studying specific sections of the textbook, I want to highlight text and ask questions specifically about that selected text so that I can get contextually relevant answers without interference from the broader knowledge base.

**Why this priority**: This provides a more precise querying mechanism that allows users to focus on specific content they've selected, enhancing the utility for deep study.

**Independent Test**: Can be fully tested by selecting text on a page, triggering the chat function, and verifying that responses are based only on the selected text rather than general textbook knowledge.

**Acceptance Scenarios**:

1. **Given** I have highlighted specific text on a textbook page, **When** I trigger the "Ask about selection" functionality, **Then** the chatbot responds based only on the selected text content.
2. **Given** I have selected text and asked a question about it, **When** I receive the response, **Then** the answer is grounded solely in the selected text without pulling from other parts of the textbook.

---

### User Story 3 - Persistent Chat Interface (Priority: P3)

As a user reading through the textbook, I want the chatbot interface to remain accessible and not interfere with my reading experience so that I can seamlessly switch between reading and asking questions.

**Why this priority**: Essential for user experience - the chatbot should enhance rather than disrupt the reading experience.

**Independent Test**: Can be fully tested by navigating through different pages while keeping the chat interface visible and functional without interfering with page scrolling or content readability.

**Acceptance Scenarios**:

1. **Given** I am browsing different pages of the textbook, **When** I continue to use the chatbot, **Then** the chat interface remains consistently available and positioned without reloading or disappearing.
2. **Given** the chatbot interface is active, **When** I scroll through the textbook content, **Then** the chat interface does not interfere with page scrolling or reading experience.

---

### Edge Cases

- What happens when the selected text is very short or contains only punctuation?
- How does the system handle network connectivity issues during chat requests?
- What occurs when the RAG system cannot find relevant content to answer a question?
- How does the system behave when users submit extremely long questions or queries?
- What happens if the backend service is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a chatbot interface that is visible and accessible on every page of the Docusaurus-based textbook website
- **FR-002**: System MUST answer questions based on the Physical AI textbook content using RAG (Retrieval Augmented Generation) methodology
- **FR-003**: System MUST display source citations with relative file paths from the /docs/ directory for every answer provided
- **FR-004**: Users MUST be able to select text on any page and ask questions specifically about that selected text, with responses based 100% on the selected content
- **FR-005**: System MUST integrate with Qdrant vector database containing textbook content embeddings for retrieval
- **FR-006**: System MUST prevent hallucination by ensuring all responses are grounded in the textbook content only
- **FR-007**: System MUST provide a health endpoint that returns 200 OK status when operational
- **FR-008**: System MUST maintain session state using Neon Serverless Postgres database
- **FR-009**: System MUST handle concurrent users without degradation in response quality or speed

### Key Entities

- **Chat Session**: Represents a user's ongoing conversation with the chatbot, including message history and session metadata stored in Neon Postgres
- **Knowledge Chunk**: Represents segments of textbook content stored in Qdrant vector database with embedding vectors and source file path metadata
- **User Query**: Represents a text input from the user, which may be a general question or specifically about selected text
- **Response**: Represents the AI-generated answer with source citations pointing to specific textbook content

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chatbot widget is visible and functional on 100% of textbook pages deployed to GitHub Pages
- **SC-002**: Answers to at least 10 different test questions about textbook content are accurate and include proper source citations
- **SC-003**: When users select text and ask about it, 100% of responses are based solely on the selected text without retrieving from broader knowledge base
- **SC-004**: At least 95% of user queries receive responses within 5 seconds
- **SC-005**: Backend health endpoint returns 200 OK status with 99% uptime during testing period
- **SC-006**: Qdrant collection contains 600 or more knowledge chunks with correct metadata and embeddings
- **SC-007**: Zero hallucination occurs in responses when tested with 3 edge-case questions designed to provoke out-of-context answers
- **SC-008**: All generated files include proper traceability headers linking back to this specification
- **SC-009**: System successfully deploys to Render.com free tier with auto-deployment configured
- **SC-010**: Selected text functionality works consistently across all page types in the Docusaurus documentation site
