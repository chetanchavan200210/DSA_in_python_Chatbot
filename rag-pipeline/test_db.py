import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from retriever import get_vector_store

vs = get_vector_store()
docs = vs.get()
print(f'Total documents in ChromaDB: {len(docs["documents"])}')
print(f'Unique sources: {set(m["source"] for m in docs["metadatas"])}')
