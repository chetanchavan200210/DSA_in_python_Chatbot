import re
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from config import TOP_K
from retriever import get_vector_store


# ----------------------------
# Load Documents from Chroma
# ----------------------------

def load_documents():

    vector_store = get_vector_store()

    all_docs = vector_store.get()


    documents = [
        Document(
            page_content=text,
            metadata=meta
        )
        for text, meta in zip(
            all_docs["documents"],
            all_docs["metadatas"]
        )
    ]


    return documents



# ----------------------------
# Initialize BM25
# ----------------------------

documents = load_documents()


tokenized_docs = [
    re.findall(r"\w+", doc.page_content.lower())
    for doc in documents
]


bm25 = BM25Okapi(tokenized_docs)



# ----------------------------
# BM25 Search
# ----------------------------

def bm25_search(query, k=TOP_K):

    tokenized_query = re.findall(r"\w+", query.lower())


    scores = bm25.get_scores(
        tokenized_query
    )


    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )


    return [
        doc
        for doc, score in ranked[:k]
    ]