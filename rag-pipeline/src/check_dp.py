from pathlib import Path
from langchain_chroma import Chroma
from embeddings import get_embedding_model

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

embedding_model = get_embedding_model()

db = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embedding_model,
)

data = db.get()

print("Total Chunks:", len(data["documents"]))

for i in range(min(5, len(data["documents"]))):
    print("\nChunk", i + 1)
    print("Metadata:", data["metadatas"][i])
    print("Text:", data["documents"][i][:200])