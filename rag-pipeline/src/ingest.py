import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from parser import extract_text_from_pdf
from embeddings import get_embedding_model

# ----------------------------
# Project Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"


# ----------------------------
# Load PDFs and convert to Documents
# ----------------------------
def load_documents():
    """
    Load all PDFs from the data folder.
    """

    documents = []

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data folder.")
        return []

    for pdf in pdf_files:

        print(f"Reading {pdf.name}")

        pages = extract_text_from_pdf(pdf)

        for page in pages:

            documents.append(
                Document(
                    page_content=page["text"],
                    metadata={
                        "source": page["document"],
                        "page": page["page"],
                    },
                )
            )

    return documents


# ----------------------------
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


# ----------------------------
# Save chunks into JSON file
# ----------------------------
def save_chunks_to_json(chunks):

    OUTPUT_DIR = BASE_DIR / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)

    data = []

    for i, chunk in enumerate(chunks, start=1):

        data.append({
            "id": i,
            "chunk_id": f"{chunk.metadata['source']}_p{chunk.metadata['page']}_c{i}",
            "document": chunk.metadata["source"],
            "page": chunk.metadata["page"],
            "chunk_index": i,
            "char_count": len(chunk.page_content),
            "text_preview": chunk.page_content[:200],
            "text": chunk.page_content
        })

    output_file = OUTPUT_DIR / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\nSaved chunks → {output_file}")


# ----------------------------
# Main pipeline
# ----------------------------
def main():

    print("=" * 50)
    print("Loading PDFs")
    print("=" * 50)

    documents = load_documents()

    print(f"Pages Loaded : {len(documents)}")

    print("\nSplitting into chunks...")

    chunks = split_documents(documents)

    print(f"Chunks Created : {len(chunks)}")

    # ✅ SAVE CHUNKS TO JSON
    save_chunks_to_json(chunks)

    print("\nLoading Embedding Model...")

    embedding_model = get_embedding_model()

    print("Creating Chroma Database...")

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DIR),
    )

    print("\nIngestion Complete!")
    print(f"Vector DB saved at:\n{CHROMA_DIR}")


if __name__ == "__main__":
    main()