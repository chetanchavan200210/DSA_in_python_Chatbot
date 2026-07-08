import hashlib
import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from parser import extract_text_from_pdf
from embeddings import get_embedding_model
from tracker import load_tracker, save_tracker
# ----------------------------
# Project Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

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
# Load PDFs and convert to Documents
# ----------------------------
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

        pages = extract_text_from_pdf(pdf)

        for page in pages:
            documents.append(
                Document(
                    page_content=page["text"],
                    metadata={
                        "source": page["document"],
                        "page": page["page"],
                        "file_hash": pdf_hash,
                    },
                )
            )

    return documents
# Split documents into chunks
# ----------------------------
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    return splitter.split_documents(documents)


## ----------------------------
# Save chunks into JSON file
# ----------------------------
def save_chunks_to_json(chunks):

    OUTPUT_DIR = BASE_DIR / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "chunks.json"

    # Load existing chunks if file exists
    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    start_id = len(data) + 1

    for i, chunk in enumerate(chunks, start=start_id):

        data.append({
            "id": i,
            "chunk_id": f"{chunk.metadata['source']}_p{chunk.metadata['page']}_c{i}",
            "document": chunk.metadata["source"],
            "page": chunk.metadata["page"],
            "chunk_index": i,
            "char_count": len(chunk.page_content),
            "file_hash": chunk.metadata["file_hash"],
            "text_preview": chunk.page_content[:200],
            "text": chunk.page_content
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\nSaved chunks → {output_file}")
# ----------------------------
# ----------------------------
# Main pipeline
# ----------------------------
# ----------------------------
# Main pipeline
# ----------------------------
# ----------------------------
# Main pipeline
# ----------------------------
def main():

    print("=" * 50)
    print("Loading PDFs")
    print("=" * 50)

    # Load tracker
    tracker = load_tracker()

    # Load only new PDFs
    documents = load_documents(tracker)

    if not documents:
        print("\nNo new PDFs found.")
        return

    print(f"Pages Loaded : {len(documents)}")

    print("\nSplitting into chunks...")

    chunks = split_documents(documents)

    print(f"Chunks Created : {len(chunks)}")

    # Save chunks to JSON
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
 

    # Update tracker with newly indexed PDFs
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    for pdf in pdf_files:
        pdf_hash = get_file_hash(pdf)
        tracker[pdf.name] = pdf_hash

    save_tracker(tracker)

    print("\n[SUCCESS] Ingestion Complete!")
    print(f"Vector DB saved at:\n{CHROMA_DIR}")


if __name__ == "__main__":
    main()