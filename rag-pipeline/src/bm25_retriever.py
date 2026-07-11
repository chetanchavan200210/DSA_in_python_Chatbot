import re

from rank_bm25 import BM25Okapi
from langchain_core.documents import Document

from config import TOP_K
from retriever import get_vector_store



# --------------------------------------------------
# Singleton BM25
# --------------------------------------------------

_bm25 = None
_documents = None



# --------------------------------------------------
# Load Documents
# --------------------------------------------------

def load_documents():

    global _documents


    if _documents is None:

        print("Loading documents for BM25...")


        vector_store = get_vector_store()


        data = vector_store.get()


        _documents = [

            Document(
                page_content=text,
                metadata=meta
            )

            for text, meta in zip(
                data["documents"],
                data["metadatas"]
            )

        ]


        print(
            f"BM25 Documents Loaded: {len(_documents)}"
        )


    return _documents



# --------------------------------------------------
# Build BM25 Index
# --------------------------------------------------

def get_bm25():

    global _bm25


    if _bm25 is None:


        documents = load_documents()


        if not documents:
            raise ValueError(
                "No documents available for BM25"
            )


        tokenized_docs = [

            re.findall(
                r"\w+",
                doc.page_content.lower()
            )

            for doc in documents

        ]


        _bm25 = BM25Okapi(
            tokenized_docs
        )


        print(
            "BM25 Index Created"
        )


    return _bm25



# --------------------------------------------------
# Search
# --------------------------------------------------

def bm25_search(
        query,
        k=TOP_K
):


    documents = load_documents()


    bm25 = get_bm25()


    tokens = re.findall(
        r"\w+",
        query.lower()
    )


    scores = bm25.get_scores(
        tokens
    )


    ranked = sorted(

        zip(
            documents,
            scores
        ),

        key=lambda x:x[1],

        reverse=True

    )


    return [

        {
            "document":doc,
            "score":float(score)
        }

        for doc,score in ranked[:k]

    ]