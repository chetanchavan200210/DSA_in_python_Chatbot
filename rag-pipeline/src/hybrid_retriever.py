from retriever import vector_search
from bm25_retriever import bm25_search


def retrieve_documents(query, k=5):

    # Vector search
    vector_results = vector_search(
        query,
        k=k
    )


    # Extract Documents from (Document, score)
    vector_docs = [
        doc
        for doc, score in vector_results
    ]


    # BM25 search
    bm25_docs = bm25_search(
        query,
        k=k
    )


    # Merge results
    combined_docs = []


    seen = set()


    for doc in vector_docs + bm25_docs:

        doc_id = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            doc.page_content[:50]
        )


        if doc_id not in seen:

            combined_docs.append(doc)
            seen.add(doc_id)


    return combined_docs[:k]