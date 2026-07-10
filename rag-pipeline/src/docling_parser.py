from docling.document_converter import DocumentConverter

# ----------------------------
# Initialize Docling Converter
# ----------------------------
converter = DocumentConverter()


# ----------------------------
# Extract text from PDF
# ----------------------------
def extract_text(file_path: str) -> str:
    """
    Extracts structured text from a PDF using Docling
    and returns it as Markdown.
    """

    result = converter.convert(file_path)

    text = result.document.export_to_markdown()

    return text