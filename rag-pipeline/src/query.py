import time
from pathlib import Path

from dotenv import load_dotenv

from config import (
    LLM_PROVIDER,
    LLM_MODEL,
    OLLAMA_MODEL,
    TEMPERATURE,
)

from chat_history import (
    get_history,
    save_message,
)

from hybrid_retriever import retrieve_documents

from guardrails import (
    detect_prompt_injection,
    validate_question_length,
    validate_empty_question,
    validate_repeated_characters,
)

from prompts import SYSTEM_PROMPT



# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)



# --------------------------------------------------
# Initialize LLM
# --------------------------------------------------

if LLM_PROVIDER == "gemini":

    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
    )


elif LLM_PROVIDER == "ollama":

    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=TEMPERATURE,
    )


else:

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}"
    )



# --------------------------------------------------
# Context Builder
# --------------------------------------------------

def build_context(
        docs,
        max_length=12000
):

    context_parts = []


    for doc in docs:


        source = doc.metadata.get(
            "source",
            "unknown"
        )

        page = doc.metadata.get(
            "page",
            "unknown"
        )

        file_type = doc.metadata.get(
            "file_type",
            "unknown"
        )


        context_parts.append(
f"""
==============================
Document : {source}
Page     : {page}
Type     : {file_type}

Content:
{doc.page_content}
"""
        )


    context = "\n\n".join(
        context_parts
    )


    return context[:max_length]



# --------------------------------------------------
# Extract Sources
# --------------------------------------------------

def extract_sources(docs):

    sources = []

    seen = set()


    for doc in docs:


        key = (

            doc.metadata.get("source"),

            doc.metadata.get("page"),

            doc.metadata.get("chunk_id")

        )


        if key not in seen:


            seen.add(key)


            sources.append(
                {
                    "document": key[0],
                    "page": key[1],
                    "chunk_id": key[2],
                    "file_type":
                        doc.metadata.get(
                            "file_type"
                        )
                }
            )


    return sources



# --------------------------------------------------
# Ask Question
# --------------------------------------------------

def ask_question(
        question,
        session_id=None
):


    # ------------------------------------------
    # Input Validation
    # ------------------------------------------

    if not validate_repeated_characters(question):

        return {
            "answer":
                "Please enter a meaningful question.",
            "sources": [],
            "related_questions": [],
        }



    if not validate_empty_question(question):

        return {
            "answer":
                "Please enter a valid question.",
            "sources": [],
            "related_questions": [],
        }



    if not validate_question_length(question):

        return {
            "answer":
                "Your question is too long. Please keep it under 500 characters.",
            "sources": [],
            "related_questions": [],
        }



    # ------------------------------------------
    # Prompt Injection Protection
    # ------------------------------------------

    if detect_prompt_injection(question):

        return {

            "answer":
                "Please ask questions related to the uploaded medical documents.",

            "sources": [],

            "related_questions": [],
        }



    # ------------------------------------------
    # Load Chat History
    # ------------------------------------------

    history = []


    if session_id:

        history = get_history(
            session_id
        )



    conversation = "\n".join(

        [

            f"{msg['role']}: {msg['content']}"

            for msg in history

        ]

    )



    # ------------------------------------------
    # Retrieval
    # ------------------------------------------

    retrieval_start = time.time()


    try:

        docs = retrieve_documents(
            question
        )


    except Exception as e:


        print(
            "[Retrieval Error]",
            e
        )


        return {

            "answer":
                "Retrieval failed internally.",

            "sources": [],

            "related_questions": [],

        }



    retrieval_time = (
        time.time()
        -
        retrieval_start
    )


    print(
        f"Retrieval Time: {retrieval_time:.2f}s"
    )



    if not docs:


        return {

            "answer":
                "I couldn't find relevant information in the uploaded documents.",

            "sources": [],

            "related_questions": [],

        }



    # ------------------------------------------
    # Build Context
    # ------------------------------------------

    context = build_context(
        docs
    )



    # ------------------------------------------
    # Prompt Construction
    # ------------------------------------------

    prompt = f"""

{SYSTEM_PROMPT}


==============================
PREVIOUS CONVERSATION
==============================

{conversation}


==============================
MEDICAL DOCUMENT CONTEXT
==============================

{context}


==============================
CURRENT USER QUESTION
==============================

{question}


==============================
ANSWER
==============================

"""



    # ------------------------------------------
    # LLM Generation
    # ------------------------------------------

    llm_start = time.time()


    try:

        response = llm.invoke(
            prompt
        )


    except Exception as e:


        print(
            "[LLM Error]",
            e
        )


        return {

            "answer":
                "LLM generation failed internally.",

            "sources": [],

            "related_questions": [],

        }



    llm_time = (
        time.time()
        -
        llm_start
    )



    print("\n========== Performance ==========")

    print(
        f"Retrieval : {retrieval_time:.2f}s"
    )

    print(
        f"LLM       : {llm_time:.2f}s"
    )

    print(
        f"Total     : {retrieval_time + llm_time:.2f}s"
    )

    print(
        "=================================\n"
    )



    # ------------------------------------------
    # Prepare Response
    # ------------------------------------------

    answer = str(
        response.content
    ).strip()



    sources = extract_sources(
        docs
    )



    # ------------------------------------------
    # Save Chat History
    # ------------------------------------------

    if session_id:


        save_message(

            session_id,

            "user",

            question

        )


        save_message(

            session_id,

            "assistant",

            answer

        )



    return {

        "answer":
            answer,

        "sources":
            sources,

        "related_questions":
            [],

    }



# --------------------------------------------------
# Terminal Testing
# --------------------------------------------------

if __name__ == "__main__":


    session = "test-session"


    while True:


        question = input(
            "\nAsk Question (exit): "
        )


        if question.lower() == "exit":

            break



        result = ask_question(

            question,

            session_id=session

        )


        print("\n====================")

        print(
            result["answer"]
        )


        print("\nSources:")


        for src in result["sources"]:


            print(
                f"- {src['document']} "
                f"(Page {src['page']})"
            )