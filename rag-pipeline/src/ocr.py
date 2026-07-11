from pathlib import Path

import easyocr

from config import OCR_LANGUAGES


# --------------------------------------------------
# Global OCR Reader (Singleton)
# --------------------------------------------------

_reader = None


def get_ocr_reader():
    """
    Load EasyOCR only once.
    """

    global _reader

    if _reader is None:

        print("Loading EasyOCR...")

        _reader = easyocr.Reader(
            OCR_LANGUAGES,
            gpu=False,      # Change to True if CUDA is available
        )

    return _reader


# --------------------------------------------------
# Extract Text from Image
# --------------------------------------------------

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image.

    Parameters
    ----------
    image_path : str
        Path to image.

    Returns
    -------
    str
        Extracted text.
    """

    image = Path(image_path)

    if not image.exists():
        return "Image not found."

    reader = get_ocr_reader()

    try:

        results = reader.readtext(
            str(image),
            detail=0,
            paragraph=True,
        )

        text = "\n".join(results).strip()

        if not text:
            return "No readable text detected."

        return text

    except Exception as e:

        print(f"OCR Error: {e}")

        return "OCR failed."