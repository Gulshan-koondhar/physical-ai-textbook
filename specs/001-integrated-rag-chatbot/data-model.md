# Data Model: Integrated RAG Chatbot

## Entities

### Chat Session
- **Description**: Represents a user's ongoing conversation with the chatbot
- **Fields**:
  - `session_id` (string): Unique identifier for the session
  - `user_id` (string, optional): Identifier for the user (if available)
  - `created_at` (timestamp): When the session was created
  - `updated_at` (timestamp): When the session was last updated
  - `messages` (array of Message objects): History of messages in the session
  - `metadata` (object): Additional session information (source page, etc.)

### Message
- **Description**: Represents a single message in the conversation
- **Fields**:
  - `message_id` (string): Unique identifier for the message
  - `session_id` (string): Reference to the parent session
  - `role` (string): 'user' or 'assistant'
  - `content` (string): The text content of the message
  - `timestamp` (timestamp): When the message was created
  - `sources` (array of Source objects, optional): Sources cited in the response

### Source
- **Description**: Represents a source document referenced in a response
- **Fields**:
  - `source_id` (string): Unique identifier for the source
  - `file_path` (string): Relative path to the source file in /docs/
  - `content_snippet` (string): Excerpt from the source that was referenced
  - `relevance_score` (number): How relevant this source was to the response (0-1)

### Knowledge Chunk
- **Description**: Represents a segment of textbook content stored in the vector database
- **Fields**:
  - `chunk_id` (string): Unique identifier for the chunk
  - `content` (string): The text content of the chunk
  - `file_path` (string): Relative path to the original document in /docs/
  - `embedding` (array of numbers): Vector embedding of the content
  - `metadata` (object): Additional information about the chunk (section, chapter, etc.)
  - `created_at` (timestamp): When the chunk was created

### User Query
- **Description**: Represents a query from the user, which may be general or about selected text
- **Fields**:
  - `query_id` (string): Unique identifier for the query
  - `session_id` (string): Reference to the parent session
  - `query_text` (string): The user's question or query
  - `query_type` (string): 'general' (RAG from textbook) or 'selected_text' (based only on selected text)
  - `selected_text` (string, optional): The text selected by the user (if applicable)
  - `timestamp` (timestamp): When the query was made

### Response
- **Description**: Represents the AI-generated answer to a user query
- **Fields**:
  - `response_id` (string): Unique identifier for the response
  - `query_id` (string): Reference to the associated query
  - `session_id` (string): Reference to the parent session
  - `content` (string): The AI-generated response text
  - `sources` (array of Source objects): Sources used to generate the response
  - `timestamp` (timestamp): When the response was generated
  - `model_used` (string): Which AI model was used to generate the response (e.g., gemini-2.5-flash)

## Relationships

- Chat Session 1 --- * Message: A session contains multiple messages
- Message 1 --- * Source: A message may reference multiple sources
- User Query 1 --- 1 Response: Each query generates one response
- Response 1 --- * Source: A response may cite multiple sources

## Validation Rules

1. **Session Validation**:
   - Session ID must be unique
   - Session must have a creation timestamp
   - Session messages must have chronological timestamps

2. **Message Validation**:
   - Message role must be either 'user' or 'assistant'
   - Message content must not be empty
   - Message must belong to a valid session

3. **Source Validation**:
   - File paths must be relative to the /docs/ directory
   - File paths must follow the pattern of actual documents in the textbook
   - Relevance scores must be between 0 and 1

4. **Query Validation**:
   - Query type must be either 'general' or 'selected_text'
   - If query type is 'selected_text', selected_text field must not be empty
   - Query text must not be empty

5. **Knowledge Chunk Validation**:
   - Chunk content must not be empty
   - File path must exist in the textbook
   - Embedding must be a valid vector array

## State Transitions

- **Session States**: active → inactive (when session expires or is closed)
- **Message States**: created → processed → stored