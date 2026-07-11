from pathlib import Path

# ============================================================
# Project Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Root folders
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
CHROMA_DIR = BASE_DIR / "chroma_db"
OUTPUT_DIR = BASE_DIR / "outputs"

# Upload folders
PDF_UPLOAD_DIR = UPLOAD_DIR / "pdfs"
IMAGE_UPLOAD_DIR = UPLOAD_DIR / "images"

# Medical Dataset Folders
PDF_DIR = DATA_DIR / "pdfs"
XRAY_DIR = DATA_DIR / "xrays"
PRESCRIPTION_DIR = DATA_DIR / "prescriptions"
REPORT_DIR = DATA_DIR / "reports"

# Tracker
TRACKER_FILE = OUTPUT_DIR / "tracker.json"

# Chunk JSON
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"

# ============================================================
# Create Required Directories
# ============================================================

for folder in [
    DATA_DIR,
    UPLOAD_DIR,
    PDF_UPLOAD_DIR,
    IMAGE_UPLOAD_DIR,
    PDF_DIR,
    XRAY_DIR,
    PRESCRIPTION_DIR,
    REPORT_DIR,
    CHROMA_DIR,
    OUTPUT_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

# ============================================================
# File Extensions
# ============================================================

PDF_EXTENSIONS = {
    ".pdf",
}

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
}

SUPPORTED_EXTENSIONS = PDF_EXTENSIONS | IMAGE_EXTENSIONS

# ============================================================
# MIME Types
# ============================================================

ALLOWED_PDF_TYPES = {
    "application/pdf",
}

ALLOWED_IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
}

# ============================================================
# Upload Limits
# ============================================================

MAX_UPLOAD_SIZE_MB = 25

MAX_IMAGE_WIDTH = 2048
MAX_IMAGE_HEIGHT = 2048

# ============================================================
# Chunking
# ============================================================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ============================================================
# Retrieval
# ============================================================

TOP_K = 8
FETCH_K = 40

MAX_CONTEXT_DOCUMENTS = 8
MAX_CONTEXT_CHARS = 12000

VECTOR_WEIGHT = 0.7
BM25_WEIGHT = 0.3

VECTOR_DB = "chroma"

# ============================================================
# Embeddings
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ============================================================
# LLM Provider
# ============================================================

# Options:
# "gemini"
# "ollama"

LLM_PROVIDER = "gemini"

# ============================================================
# Gemini
# ============================================================

LLM_MODEL = "gemini-2.5-flash"

# -------------------------------------------------
# Ollama Text Model
# -------------------------------------------------

OLLAMA_MODEL = "llama3"

# -------------------------------------------------
# Ollama Vision Model
# -------------------------------------------------

OLLAMA_VISION_MODEL = "llava"
# or
# OLLAMA_VISION_MODEL = "llava:13b"
# ============================================================
# Vision
# ============================================================

VISION_PROVIDER = "gemini"

VISION_MODEL = "gemini-2.5-flash"

VISION_SYSTEM_PROMPT = """
You are an expert medical imaging assistant.

Analyze the uploaded medical image carefully.

Describe only what is visibly present.

Mention:
- anatomical structures
- fractures
- implants
- lesions
- swelling
- missing teeth
- restorations
- dental findings
- radiographic observations
- any visible abnormalities

Do NOT invent findings.

Do NOT diagnose diseases unless they are explicitly visible.

If the image quality is poor, clearly state that.
"""

# ============================================================
# OCR
# ============================================================

OCR_PROVIDER = "easyocr"

OCR_LANGUAGES = [
    "en",
]

# ============================================================
# Generation
# ============================================================

TEMPERATURE = 0.2

# ============================================================
# Chat
# ============================================================

MAX_CHAT_HISTORY = 10

# ============================================================
# Logging
# ============================================================

LOG_PERFORMANCE = True

LOG_RETRIEVAL = True

LOG_LLM = True

# ============================================================
# Debug
# ============================================================

DEBUG = True