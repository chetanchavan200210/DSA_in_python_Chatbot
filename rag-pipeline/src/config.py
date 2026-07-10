# config.py
from pathlib import Path

# ----------------------------
# Project Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

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
TOP_K = 8
FETCH_K = 40

# ----------------------------
# Embedding Config
# ----------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # or your Ollama / HF model

# ----------------------------
# LLM Config (if using Ollama)
# ----------------------------
OLLAMA_MODEL = "llama3"
TEMPERATURE = 0.2

LLM_MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.2