import hashlib
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config import (
    CHROMA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from embeddings import get_embedding_model
from docling_parser import extract_text
from vision import describe_medical_image
from ocr import extract_text_from_image

from ingest import save_chunks_to_json


# --------------------------------------------------
# Generate SHA256 Hash
# --------------------------------------------------
def get_file_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


# --------------------------------------------------
# Ingest Uploaded File
# --------------------------------------------------
def ingest_uploaded_file(file_path: Path, file_type: str):

    try:

        print("=" * 60)
        print("Processing Uploaded File")
        print("=" * 60)
        print(f"Filename : {file_path.name}")
        print(f"Type     : {file_type}")

        # ------------------------------------------
        # Extract Content
        # ------------------------------------------
        if file_type == "pdf":

            print("Extracting text using Docling...")

            text = extract_text(str(file_path))

            if not text.strip():
                text = "No readable text found in PDF."

        elif file_type == "image":

            print("Running OCR...")

            ocr_text = extract_text_from_image(str(file_path)).strip()

            if not ocr_text:
                ocr_text = "No readable text detected."

            print("Running Vision AI...")

            vision_text = describe_medical_image(str(file_path)).strip()

            if not vision_text:
                vision_text = "No visual findings returned."

            text = f"""
OCR TEXT
========
{ocr_text}

VISION ANALYSIS
===============
{vision_text}
"""

        else:
            raise ValueError("Unsupported file type.")

        # ------------------------------------------
        # Create LangChain Document
        # ------------------------------------------
        document = Document(
            page_content=text,
            metadata={
                "source": file_path.name,
                "filename": file_path.name,
                "page": 1,
                "file_type": file_type,
                "file_hash": get_file_hash(file_path),
            },
        )

        # ------------------------------------------
        # Split into Chunks
        # ------------------------------------------
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

        chunks = splitter.split_documents([document])

        print(f"Chunks Created : {len(chunks)}")

        # ------------------------------------------
        # Add Chunk IDs
        # ------------------------------------------
        for i, chunk in enumerate(chunks, start=1):

            chunk.metadata["chunk_id"] = (
                f"{file_path.stem}_p1_c{i}"
            )

        # ------------------------------------------
        # Save chunks to JSON
        # ------------------------------------------
        save_chunks_to_json(chunks)

        # ------------------------------------------
        # Load Embedding Model
        # ------------------------------------------
        print("Loading Embedding Model...")

        embedding_model = get_embedding_model()

        # ------------------------------------------
        # Open ChromaDB
        # ------------------------------------------
        print("Opening Chroma Database...")

        vector_db = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embedding_model,
        )

        # ------------------------------------------
        # Store Chunks
        # ------------------------------------------
        print("Adding chunks to ChromaDB...")

        vector_db.add_documents(chunks)

        print("Upload successfully indexed.")

        return {
            "filename": file_path.name,
            "file_type": file_type,
            "chunks": len(chunks),
            "status": "success",
        }

    except Exception as e:

        print(f"[ERROR] {e}")

        return {
            "filename": file_path.name,
            "file_type": file_type,
            "chunks": 0,
            "status": "failed",
            "error": str(e),
        }