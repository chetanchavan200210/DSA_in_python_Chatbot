from config import TOP_K

from retriever import vector_search
from bm25_retriever import bm25_search



# --------------------------------------------------
# Hybrid Retrieval
# --------------------------------------------------

def retrieve_documents(
        query,
        k=TOP_K
):


    vector_results = vector_search(
        query,
        k=k
    )


    bm25_results = bm25_search(
        query,
        k=k
    )


    combined = {}


    # ----------------------------
    # Vector Results
    # ----------------------------

    for item in vector_results:


        doc = item["document"]

        score = item["score"]


        key = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            hash(doc.page_content)
        )


        combined[key] = {

            "document":doc,

            "score":score

        }



    # ----------------------------
    # BM25 Results
    # ----------------------------

    for item in bm25_results:


        doc = item["document"]

        score = item["score"]


        key = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            hash(doc.page_content)
        )


        if key in combined:


            combined[key]["score"] += (
                normalize_bm25(score)
            )


        else:


            combined[key] = {

                "document":doc,

                "score":
                    normalize_bm25(score)

            }



    # ----------------------------
    # Rank
    # ----------------------------

    ranked = sorted(

        combined.values(),

        key=lambda x:x["score"],

        reverse=True

    )


    return [

        item["document"]

        for item in ranked[:k]

    ]



# --------------------------------------------------
# BM25 Score Normalization
# --------------------------------------------------

def normalize_bm25(score):

    return min(
        score / 20,
        1
    )



# --------------------------------------------------
# Testing
# --------------------------------------------------

if __name__ == "__main__":


    while True:


        query=input(
            "\nAsk Question: "
        )


        if query.lower()=="exit":
            break



        docs = retrieve_documents(query)



        print(
            f"\nRetrieved {len(docs)} documents"
        )


        for i,doc in enumerate(
            docs,
            start=1
        ):


            print("\n"+"="*50)

            print(
                "Result:",
                i
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
                doc.page_content[:500]
            )