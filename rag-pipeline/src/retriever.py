from pathlib import Path

from langchain_chroma import Chroma

from config import CHROMA_DIR, TOP_K
from embeddings import get_embedding_model


# --------------------------------------------------
# Singleton Vector Store
# --------------------------------------------------

_vector_store = None



# --------------------------------------------------
# Load Chroma Database
# --------------------------------------------------

def get_vector_store():

    global _vector_store


    if _vector_store is None:

        print("Loading Chroma Database...")


        if not Path(CHROMA_DIR).exists():
            raise FileNotFoundError(
                f"Chroma database not found: {CHROMA_DIR}"
            )


        embedding_model = get_embedding_model()


        _vector_store = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embedding_model,
        )


        print("Chroma Database Loaded")


    return _vector_store



# --------------------------------------------------
# Vector Search
# --------------------------------------------------

def vector_search(query, k=TOP_K):

    vector_store = get_vector_store()


    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )


    formatted_results = []


    for doc, distance in results:


        similarity = max(
            0,
            1 - float(distance)
        )


        formatted_results.append(
            {
                "document": doc,
                "score": similarity
            }
        )


    return formatted_results



# --------------------------------------------------
# Build Context
# --------------------------------------------------

def get_context(query, k=TOP_K):


    results = vector_search(
        query,
        k
    )


    context = []

    sources = []


    for item in results:


        doc = item["document"]

        score = item["score"]


        context.append(
            doc.page_content
        )


        sources.append(
            {
                "document":
                    doc.metadata.get("source"),

                "page":
                    doc.metadata.get("page"),

                "type":
                    doc.metadata.get("type","pdf"),

                "score":
                    round(score,3)
            }
        )


    return {

        "context":
            "\n\n".join(context),

        "sources":
            sources
    }



# --------------------------------------------------
# Testing
# --------------------------------------------------

if __name__ == "__main__":


    store = get_vector_store()


    print(
        "Total Chunks:",
        store._collection.count()
    )


    question = input(
        "\nAsk Question: "
    )


    results = vector_search(question)


    for item in results:


        doc = item["document"]


        print("\n------------------")

        print(
            "Score:",
            item["score"]
        )


        print(
            "Source:",
            doc.metadata.get("source")
        )


        print(
            "Page:",
            doc.metadata.get("page")
        )


        print(
            "\n",
            doc.page_content[:500]
        )