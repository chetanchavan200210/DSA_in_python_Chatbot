from retriever import vector_search
from bm25_retriever import bm25_search


def retrieve_documents(query):

    vector_docs = vector_search(query, k=5)

    bm25_docs = bm25_search(query, k=5)

    combined = []

    seen = set()

    for doc in vector_docs + bm25_docs:

        key = (
            doc.metadata["source"],
            doc.metadata["page"],
            doc.page_content,
        )

        if key not in seen:
            seen.add(key)
            combined.append(doc)

    return combined[:5]