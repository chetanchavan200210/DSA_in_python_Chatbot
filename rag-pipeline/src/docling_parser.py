from pathlib import Path
import time

from docling.document_converter import DocumentConverter


# --------------------------------------------------
# Singleton Converter
# --------------------------------------------------

_converter = None


def get_converter() -> DocumentConverter:
    """
    Load Docling converter only once.
    """

    global _converter


    if _converter is None:

        print("Loading Docling...")

        _converter = DocumentConverter()


    return _converter



# --------------------------------------------------
# Extract Text from PDF
# --------------------------------------------------

def extract_text(file_path: str) -> str:
    """
    Extract PDF content using Docling.

    Returns markdown text.
    """


    path = Path(file_path)


    if not path.exists():

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )


    converter = get_converter()


    try:

        print("\n" + "="*50)

        print(
            f"Parsing PDF: {path.name}"
        )

        print(
            f"File size: {round(path.stat().st_size / (1024*1024),2)} MB"
        )


        start = time.time()


        result = converter.convert(
            str(path)
        )


        text = (
            result.document
            .export_to_markdown()
        )


        elapsed = time.time() - start


        print(
            f"Characters extracted: {len(text)}"
        )


        print(
            f"Parsing time: {round(elapsed,2)} seconds"
        )


        if len(text.strip()) == 0:

            print(
                "Warning: No text extracted. OCR may be required."
            )


        print("="*50)


        return text.strip()



    except Exception as e:


        raise RuntimeError(
            f"Docling failed for '{path.name}': {e}"
        )