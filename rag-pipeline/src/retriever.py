# from pathlib import Path

# from langchain_chroma import Chroma

from langchain_chroma import Chroma

from config import CHROMA_DIR, TOP_K
from embeddings import get_embedding_model
# Project Paths
# ----------------------------

# BASE_DIR = Path(__file__).resolve().parent.parent

# CHROMA_DIR = BASE_DIR / "chroma_db"


# ----------------------------
# Global Vector Store
# ----------------------------

_vector_store = None



# ----------------------------
# Load Chroma Database
# ----------------------------

def get_vector_store():

    global _vector_store


    if _vector_store is None:

        print("Loading Chroma Database...")


        embedding_model = get_embedding_model()
    

        _vector_store = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embedding_model,
        )


        print("Chroma Database Loaded")


    return _vector_store



# ----------------------------
# Similarity Search
# ----------------------------
def vector_search(query, k=TOP_K):

    vector_store = get_vector_store()


    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
    )


    return results



# ----------------------------
# Format Retrieved Context
# ----------------------------

def get_context(query, k=TOP_K):

    results = vector_search(query, k)


    context = []

    sources = []


    for doc, score in results:


        context.append(
            doc.page_content
        )


        sources.append(
            {
                "document": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "score": float(score)
            }
        )


    return {
        "context": "\n\n".join(context),
        "sources": sources
    }



# ----------------------------
# Testing
# ----------------------------

# ----------------------------
# Testing
# ----------------------------
if __name__ == "__main__":

    vector_store = get_vector_store()

    print("\nTotal Chunks in Chroma:")
    print(vector_store._collection.count())

    all_docs = vector_store.get()

    print("\nDocuments found in Chroma:\n")

    docs = set()

    for meta in all_docs["metadatas"]:
        docs.add(meta["source"])

    for doc in sorted(docs):
        print("-", doc)

    print("\n---------------------------------\n")

    question = input("Ask Question: ")

    results = vector_search(question)

    for doc, score in results:

        print("\n-----------------------")
        print("Similarity Score:", score)
        print("Source:", doc.metadata.get("source"))
        print("Page:", doc.metadata.get("page"))

        print("\nContent:\n")
        print(doc.page_content[:500])