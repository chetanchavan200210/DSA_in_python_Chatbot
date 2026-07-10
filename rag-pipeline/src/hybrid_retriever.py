from config import TOP_K
from retriever import vector_search
from bm25_retriever import bm25_search


# ----------------------------
# Hybrid Retrieval
# ----------------------------
def retrieve_documents(query, k=TOP_K):

    # Vector Search
    vector_results = vector_search(
        query,
        k=k
    )

    # Extract Documents from (Document, score)
    vector_docs = [
        doc
        for doc, score in vector_results
    ]

    # BM25 Search
    bm25_docs = bm25_search(
        query,
        k=k
    )

    # Merge Results
    combined_docs = []

    seen = set()

    for doc in vector_docs + bm25_docs:

        doc_id = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            hash(doc.page_content),
        )

        if doc_id not in seen:
            combined_docs.append(doc)
            seen.add(doc_id)

    return combined_docs[:k]


# ----------------------------
# Testing
# ----------------------------
if __name__ == "__main__":

    while True:

        query = input("\nAsk Question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        docs = retrieve_documents(query)

        print(f"\nRetrieved {len(docs)} document(s)\n")

        for i, doc in enumerate(docs, start=1):

            print("=" * 60)
            print(f"Result {i}")
            print("=" * 60)
            print("Source :", doc.metadata.get("source"))
            print("Page   :", doc.metadata.get("page"))
            print("\nContent:\n")
            print(doc.page_content[:500])
            print()