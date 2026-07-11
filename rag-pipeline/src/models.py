from pydantic import BaseModel, Field
from typing import List, Optional


# --------------------------------------------------
# Chat Request
# --------------------------------------------------

class ChatRequest(BaseModel):

    query: str

    # Used for conversation memory
    session_id: Optional[str] = None



# --------------------------------------------------
# Source Model
# --------------------------------------------------

class Source(BaseModel):

    document: Optional[str] = None

    page: Optional[int | str] = None

    chunk_id: Optional[str] = None

    file_type: Optional[str] = None



# --------------------------------------------------
# Chat Response
# --------------------------------------------------

class ChatResponse(BaseModel):

    answer: str

    sources: List[Source] = Field(
        default_factory=list
    )

    related_questions: List[str] = Field(
        default_factory=list
    )



# --------------------------------------------------
# Upload Response
# --------------------------------------------------

class UploadResponse(BaseModel):

    filename: str

    file_type: str

    message: str