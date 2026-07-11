from pathlib import Path
import sys
import traceback


from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
)

from fastapi.middleware.cors import CORSMiddleware



# --------------------------------------------------
# Add src folder
# --------------------------------------------------

sys.path.append(
    str(Path(__file__).parent / "src")
)



# --------------------------------------------------
# Imports
# --------------------------------------------------

from query import ask_question

from upload import save_uploaded_file

from ingest_uploaded_file import ingest_uploaded_file

from models import (
    ChatRequest,
    ChatResponse,
    UploadResponse,
)



# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(

    title="Medical AI Assistant (RAG + Vision)",

    description="""
Medical AI Assistant powered by:

- Retrieval Augmented Generation
- ChromaDB
- OCR
- Vision AI
- Gemini/Ollama
- FastAPI
- Chat Memory
""",

    version="3.0.0"

)



# --------------------------------------------------
# CORS
# --------------------------------------------------

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



# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
async def home():

    return {

        "message":
            "Medical AI Assistant Backend Running",

        "status":
            "success"

    }



# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/health")
async def health():

    return {

        "status":
            "healthy"

    }



# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(
        request: ChatRequest
):

    try:

        result = ask_question(

            question=request.query,

            session_id=request.session_id

        )


        print("\n========== CHAT RESPONSE ==========")

        print(result)

        print("===================================\n")


        return result



    except Exception as e:


        print("\n========== CHAT ERROR ==========")

        traceback.print_exc()

        print("================================\n")


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )



# --------------------------------------------------
# Upload Endpoint
# --------------------------------------------------

@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_file(
        file: UploadFile = File(...)
):

    try:

        print("=" * 60)

        print("New Upload")

        print("=" * 60)


        # Save file

        path, file_type = save_uploaded_file(
            file
        )


        print(
            "Saved:",
            path.name
        )


        print(
            "Type:",
            file_type
        )



        # Ingest file

        result = ingest_uploaded_file(

            path,

            file_type

        )



        print(
            "Upload Indexed Successfully"
        )



        return UploadResponse(

            filename=result["filename"],

            file_type=file_type,

            message=(

                f"Upload successful. "

                f"Indexed {result['chunks']} chunks."

            )

        )



    except Exception as e:


        print("\n========== UPLOAD ERROR ==========")

        traceback.print_exc()

        print("==================================\n")


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )



# --------------------------------------------------
# Run Server
# --------------------------------------------------

if __name__ == "__main__":

    import uvicorn


    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )