
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

## Getting Started

To run this project:

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```
   This will start the Vite development server with hot module replacement (HMR).


   This creates an optimized production build in the `dist/` directory.

4. **Preview production build**:
   ```bash
   npm run preview
   ```
   This serves the production build locally for testing.

## Creating Files

To add new files to your project:

- **Components**: Create React components in the `src/` directory (e.g., `src/components/MyComponent.jsx`)
- **Styles**: Add CSS files alongside your components or in a `src/styles/` directory
- **Assets**: Place images, fonts, and other static assets in the `public/` directory or import them from `src/assets/`
- **Pages**: Create page components in `src/pages/` or organize them in a routing structure
- **Utilities**: Add helper functions and utilities in `src/utils/` or `src/lib/`

Files created in `src/` will be processed by Vite's build pipeline, while files in `public/` are served directly.

## Backend (RAG Pipeline)

This project includes a Python FastAPI backend with RAG (Retrieval Augmented Generation) capabilities using LangChain and Google Generative AI.

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd ../rag-pipeline
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install backend dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   Create a `.env` file in the `rag-pipeline` directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

6. **Start the backend server**:
   ```bash
   uvicorn main:app --reload
   ```

The backend server runs on http://localhost:8000 and provides:
- `GET /` - Health check endpoint
- `POST /chat` - Chat endpoint for RAG queries

### Using Ollama (Alternative LLM)

If you prefer to use Ollama instead of Google Generative AI:

1. **Install Ollama**:
   - Download from https://ollama.com
   - Install and start Ollama

2. **Pull the desired model**:
   ```bash
   ollama pull llama3
   ```

3. **Install LangChain Ollama**:
   ```bash
   pip install langchain-ollama
   ```

4. **Modify `src/query.py`**:
   - Comment out the Google Generative AI import and initialization
   - Uncomment the Ollama import and initialization:
   ```python
   from langchain_ollama import ChatOllama
   # from langchain_google_genai import ChatGoogleGenerativeAI

   llm = ChatOllama(
       model="llama3",
       temperature=0.2,
   )
   ```

5. **Update `src/config.py`** (optional):
   - Modify `OLLAMA_MODEL` to your preferred model
   - Update `EMBEDDING_MODEL` if using Ollama embeddings

6. **Restart the backend server**:
   ```bash
   uvicorn main:app --reload
   ```

### Tech Stack

**Frontend**:
- React 19.2.7
- Vite 8.1.1
- React Icons 5.7.0
- Oxlint for linting

**Backend**:
- FastAPI
- LangChain
- Google Generative AI
- ChromaDB (vector database)
- Uvicorn (ASGI server)
