from pathlib import Path
import shutil

from config import (
    PDF_UPLOAD_DIR,
    IMAGE_UPLOAD_DIR,
    PDF_EXTENSIONS,
    IMAGE_EXTENSIONS,
    MAX_UPLOAD_SIZE_MB,
)


def save_uploaded_file(file):
    """
    Saves an uploaded PDF or image.

    Returns:
        destination (Path)
        file_type ("pdf" or "image")
    """

    if not file.filename:
        raise ValueError("No filename provided.")

    suffix = Path(file.filename).suffix.lower()

    # ----------------------------
    # Validate extension
    # ----------------------------
    if suffix in PDF_EXTENSIONS:
        destination = PDF_UPLOAD_DIR / file.filename
        file_type = "pdf"

    elif suffix in IMAGE_EXTENSIONS:
        destination = IMAGE_UPLOAD_DIR / file.filename
        file_type = "image"

    else:
        raise ValueError(
            "Unsupported file type. Only PDF, PNG, JPG and JPEG are allowed."
        )

    # ----------------------------
    # Validate file size
    # ----------------------------
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    max_size = MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if size > max_size:
        raise ValueError(
            f"File exceeds {MAX_UPLOAD_SIZE_MB} MB limit."
        )

    # ----------------------------
    # Save file
    # ----------------------------
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return destination, file_type