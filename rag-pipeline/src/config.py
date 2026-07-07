# config.py
from pathlib import Path

# ----------------------------
# Project Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"
OUTPUT_DIR = BASE_DIR / "outputs"

# ----------------------------
# Chunking Config
# ----------------------------
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ----------------------------
# Retrieval Config
# ----------------------------
TOP_K = 5
FETCH_K = 20

# ----------------------------
# Embedding Config
# ----------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # or your Ollama / HF model

# ----------------------------
# LLM Config (if using Ollama)
# ----------------------------
OLLAMA_MODEL = "llama3"
TEMPERATURE = 0.2