import hashlib
import json
from pathlib import Path

from config import (
    DATA_DIR,
    CHROMA_DIR,
    OUTPUT_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from docling_parser import extract_text
from embeddings import get_embedding_model
from tracker import load_tracker, save_tracker


# ----------------------------
# Generate SHA256 Hash
# ----------------------------
def get_file_hash(file_path: Path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


# ----------------------------
# Load only new PDFs
# ----------------------------
def load_documents(existing_hashes):

    documents = []

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    print(f"\nDATA_DIR: {DATA_DIR}")

    print("\nPDFs Found:")
    for pdf in pdf_files:
        print(f" - {pdf.name}")

    if not pdf_files:
        print("No PDF files found.")
        return []

    for pdf in pdf_files:

        pdf_hash = get_file_hash(pdf)

        if pdf_hash in existing_hashes.values():
            print(f"[OK] Skipping {pdf.name} (already indexed)")
            continue

        print(f"[DOC] Reading {pdf.name}")

        text = extract_text(str(pdf))

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": pdf.name,
                    "page": 1,
                    "file_hash": pdf_hash,
                },
            )
        )

    return documents


# ----------------------------
# Split Documents into Chunks
# ----------------------------
def split_documents(documents):

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

    return splitter.split_documents(documents)


# ----------------------------
# Save Chunks to JSON
# ----------------------------
def save_chunks_to_json(chunks):

    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "chunks.json"

    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    start_id = len(data) + 1

    for i, chunk in enumerate(chunks, start=start_id):

        data.append(
            {
                "id": i,
                "chunk_id": chunk.metadata["chunk_id"],
                "document": chunk.metadata["source"],
                "page": chunk.metadata["page"],
                "chunk_index": i,
                "char_count": len(chunk.page_content),
                "file_hash": chunk.metadata["file_hash"],
                "text_preview": chunk.page_content[:200],
                "text": chunk.page_content,
            }
        )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\nSaved chunks → {output_file}")


# ----------------------------
# Main Pipeline
# ----------------------------
def main():

    print("=" * 50)
    print("Loading PDFs")
    print("=" * 50)

    tracker = load_tracker()

    documents = load_documents(tracker)

    if not documents:
        print("\nNo new PDFs found.")
        return

    print(f"\nDocuments Loaded : {len(documents)}")

    print("\nSplitting into chunks...")

    chunks = split_documents(documents)

    # ----------------------------
    # Add Chunk IDs
    # ----------------------------
    for i, chunk in enumerate(chunks, start=1):

        chunk.metadata["chunk_id"] = (
            f"{chunk.metadata['source']}_p{chunk.metadata['page']}_c{i}"
        )

    print(f"Chunks Created : {len(chunks)}")

    # ----------------------------
    # Save chunks to JSON
    # ----------------------------
    save_chunks_to_json(chunks)

    print("\nLoading Embedding Model...")

    embedding_model = get_embedding_model()

    print("Opening Chroma Database...")

    vector_db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_model,
    )

    print("\nAdding new documents to Chroma...")

    vector_db.add_documents(chunks)

    # ----------------------------
    # Update Tracker
    # ----------------------------
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    for pdf in pdf_files:

        pdf_hash = get_file_hash(pdf)

        tracker[pdf.name] = pdf_hash

    save_tracker(tracker)

    print("\n[SUCCESS] Ingestion Complete!")
    print(f"Vector DB saved at:\n{CHROMA_DIR}")


# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    main()