from retriever import retrieve_documents

docs = retrieve_documents("What is recursion?")

print(f"Retrieved {len(docs)} documents\n")

for doc in docs:
    print("=" * 60)
    print("Source :", doc.metadata["source"])
    print("Page   :", doc.metadata["page"])
    print(doc.page_content[:300])