from pathlib import Path
from langchain_chroma import Chroma
from embeddings import get_embedding_model

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

embedding_model = get_embedding_model()

vector_store = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embedding_model,
)

def vector_search(query, k=5):
    return vector_store.similarity_search(
        query=query,
        k=k,
    )