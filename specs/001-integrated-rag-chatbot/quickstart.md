# Quickstart Guide: Integrated RAG Chatbot

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Access to Google Gemini API
- Access to Qdrant Cloud
- Access to Neon Postgres

### Backend Setup
1. Navigate to the backend directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   export GEMINI_API_KEY=your_gemini_api_key
   export QDRANT_URL=your_qdrant_url
   export QDRANT_API_KEY=your_qdrant_api_key
   export DATABASE_URL=your_neon_postgres_connection_string
   ```
4. Run the backend:
   ```bash
   python src/main.py
   ```

### Frontend Setup
1. Navigate to the frontend directory
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables:
   ```bash
   export REACT_APP_BACKEND_URL=your_backend_url
   ```
4. Run the frontend:
   ```bash
   npm start
   ```

## Key Components

### Backend Services
- **RAG Service**: Handles retrieval and generation logic
- **Embedding Service**: Manages text embedding operations
- **Qdrant Service**: Interfaces with vector database
- **Postgres Service**: Manages session storage
- **Gemini Service**: Interfaces with Google Gemini API

### Frontend Components
- **ChatWidget**: Main chat interface component
- **TextSelection Handler**: Captures selected text from any page
- **SourceCitation Display**: Shows source citations with responses

## API Endpoints

### Chat
- `POST /api/chat` - Send a message and get a response
- `POST /api/chat/new-session` - Create a new chat session
- `GET /api/chat/session/{session_id}` - Get session history

### Health
- `GET /health` - Check service health

### Sessions
- `GET /api/session/{session_id}` - Get session info
- `DELETE /api/session/{session_id}` - Delete session

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `QDRANT_URL`: URL to your Qdrant instance
- `QDRANT_API_KEY`: Your Qdrant API key
- `DATABASE_URL`: Connection string for Neon Postgres
- `BACKEND_URL`: URL of the backend service

## Testing

### Backend Tests
Run backend tests with:
```bash
cd backend
pip install pytest pytest-asyncio
pytest
```

### Frontend Tests
Run frontend tests with:
```bash
cd frontend
npm test
```

## Deployment

### Backend (Render.com)
1. Create a Render account at https://render.com
2. Connect your GitHub repository
3. Create a new Web Service
4. Set the root directory to `backend`
5. Use the `Render.yaml` file in the backend directory for configuration
6. Add required environment variables:
   - GEMINI_API_KEY
   - QDRANT_URL
   - QDRANT_API_KEY
   - DATABASE_URL
   - OPENAI_API_KEY
7. Deploy the service

### Frontend (GitHub Pages)
GitHub Actions workflow is configured to automatically deploy the frontend to GitHub Pages on pushes to the main branch.
1. Enable GitHub Pages in your repository settings
2. The workflow in `.github/workflows/deploy-frontend.yml` will build and deploy the frontend
3. Access the frontend at `https://<username>.github.io/<repository>`

### Docusaurus Integration
The chat widget is integrated into all Docusaurus pages via the plugin in `plugins/docusaurus-plugin-physical-ai-chat`