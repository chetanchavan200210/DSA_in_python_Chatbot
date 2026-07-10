from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---------------------------------------
# Add src folder to Python path
# ---------------------------------------
sys.path.append(str(Path(__file__).parent / "src"))

from query import ask_question

# ---------------------------------------
# FastAPI App
# ---------------------------------------
app = FastAPI(
    title="RAG Chatbot API",
    description="Hybrid Retrieval-Augmented Generation API using ChromaDB + BM25 + Gemini",
    version="1.0.0",
)

# ---------------------------------------
# CORS
# ---------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# Request / Response Models
# ---------------------------------------
class ChatRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=500,
        description="User question",
    )


class Source(BaseModel):
    document: str
    page: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    related_questions: list[str]


# ---------------------------------------
# Home Endpoint
# ---------------------------------------
@app.get("/")
async def home():
    return {
        "message": "RAG Backend Running",
        "status": "success",
    }


# ---------------------------------------
# Health Check
# ---------------------------------------
@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


# ---------------------------------------
# Chat Endpoint
# ---------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:
        result = ask_question(request.query)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )


# ---------------------------------------
# Run Server
# ---------------------------------------
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )