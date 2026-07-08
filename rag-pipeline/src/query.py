import time
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from hybrid_retriever import retrieve_documents

from guardrails import (
    detect_prompt_injection,
    validate_question_length,
    validate_empty_question,
)

from prompts import SYSTEM_PROMPT

# ----------------------------
# Load Environment
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

print("GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))

# ----------------------------
# Load LLM
# ----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

# ----------------------------
# Ask Question
# ----------------------------
def ask_question(question):

    # ----------------------------
    # Guardrail 1 : Empty Question
    # ----------------------------
    if not validate_empty_question(question):
        return {
            "answer": "Please enter a valid question.",
            "sources": [],
            "related_questions": [],
        }

    # ----------------------------
    # Guardrail 2 : Length Check
    # ----------------------------
    if not validate_question_length(question):
        return {
            "answer": "Your question is too long. Please keep it under 500 characters.",
            "sources": [],
            "related_questions": [],
        }

    # ----------------------------
    # Guardrail 3 : Prompt Injection
    # ----------------------------
    if detect_prompt_injection(question):
        return {
            "answer": "Your request couldn't be processed. Please ask a question related to the uploaded documents.",
            "sources": [],
            "related_questions": [],
        }

    # ----------------------------
    # Retrieve Documents
    # ----------------------------
    retrieval_start = time.time()

    try:
        docs = retrieve_documents(question)
    except Exception as e:
        print(f"[Retrieval Error] {e}")
        return {
            "answer": "An internal retrieval error occurred.",
            "sources": [],
            "related_questions": [],
        }

    retrieval_time = time.time() - retrieval_start
    print(f"\nRetrieval Time: {retrieval_time:.2f} sec")

    # ----------------------------
    # Guardrail 4 : No Documents
    # ----------------------------
    if not docs:
        return {
            "answer": "I couldn't find any relevant information in the uploaded documents.",
            "sources": [],
            "related_questions": [],
        }

    # ----------------------------
    # Build Context
    # ----------------------------
    context = "\n\n".join(
        [
            f"Document: {doc.metadata['source']}\n"
            f"Page: {doc.metadata['page']}\n\n"
            f"{doc.page_content}"
            for doc in docs
        ]
    )

    # ----------------------------
    # Prompt
    # ----------------------------
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer ONLY the user's question.

Rules:
- Do NOT generate follow-up questions.
- Do NOT suggest additional questions.
- Do NOT write:
    Here are related questions
    Related Questions
    Follow-up Questions
- Return only the answer text.
"""

    # ----------------------------
    # LLM
    # ----------------------------
    llm_start = time.time()

    try:
        response = llm.invoke(prompt)
    except Exception as e:
        print(f"[LLM Error] {e}")
        return {
            "answer": "An internal LLM error occurred.",
            "sources": [],
            "related_questions": [],
        }

    llm_time = time.time() - llm_start

    print(f"LLM Time: {llm_time:.2f} sec")
    print(f"Total Time: {retrieval_time + llm_time:.2f} sec")

    # ----------------------------
    # Clean Answer
    # ----------------------------
    answer = response.content.strip()

    markers = [
        "Here are",
        "Related Questions",
        "related questions",
        "Follow-up Questions",
        "follow-up questions",
    ]

    for marker in markers:
        if marker.lower() in answer.lower():
            answer = answer[: answer.lower().find(marker.lower())].strip()
            break

    # ----------------------------
    # Sources
    # ----------------------------
    seen = set()
    sources = []

    for doc in docs:
        key = (
            doc.metadata["source"],
            doc.metadata["page"],
        )

        if key not in seen:
            seen.add(key)
            sources.append(
                {
                    "document": key[0],
                    "page": key[1],
                }
            )

    # ----------------------------
    # Return
    # ----------------------------
    return {
        "answer": answer,
        "sources": sources,
        "related_questions": [],
    }


# ----------------------------
# Run from Terminal
# ----------------------------
if __name__ == "__main__":

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        result = ask_question(question)

        print("\n==============================")
        print("Answer")
        print("==============================")
        print(result["answer"])

        print("\nSources")

        for src in result["sources"]:
            print(f"- {src['document']} (Page {src['page']})")