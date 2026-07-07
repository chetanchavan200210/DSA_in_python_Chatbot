from rank_bm25 import BM25Okapi
from langchain_core.documents import Document

from retriever import vector_store

# Load every document stored in Chroma
all_docs = vector_store.get()

documents = [
    Document(page_content=text, metadata=meta)
    for text, meta in zip(all_docs["documents"], all_docs["metadatas"])
]

tokenized_docs = [
    doc.page_content.lower().split()
    for doc in documents
]

bm25 = BM25Okapi(tokenized_docs)


def bm25_search(query, k=5):
    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    return [doc for doc, score in ranked[:k]]