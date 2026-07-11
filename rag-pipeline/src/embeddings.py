from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL

# --------------------------------------------------
# Singleton Embedding Model
# --------------------------------------------------

_embedding_model = None


def get_embedding_model():
    """
    Load the embedding model only once.
    """

    global _embedding_model

    if _embedding_model is None:

        print("Loading Embedding Model...")

        _embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    return _embedding_model