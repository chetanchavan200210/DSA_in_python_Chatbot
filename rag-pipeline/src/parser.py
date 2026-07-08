# import fitz  # PyMuPDF
# from pathlib import Path


# # def extract_text_from_pdf(pdf_path):
# #     """
# #     Reads a PDF page by page and returns a list of dictionaries.

# #     Each dictionary contains:
# #     - document name
# #     - page number
# #     - page text
# #     """
    
# #     document = fitz.open(pdf_path)
    
# #     print("Reading:", pdf_path.name)
# #     print("Total Pages:", len(doc))
    
# #     pages = []

# #     for page_num in range(len(document)):
# #         page = document.load_page(page_num)
# #         text = page.get_text("text")

# #         if text.strip():
# #             pages.append(
# #                 {
# #                     "document": Path(pdf_path).name,
# #                     "page": page_num + 1,
# #                     "text": text,
# #                 }
# #             )

# #     document.close()
# #     return pages

# def extract_text_from_pdf(pdf_path):

#     document = fitz.open(pdf_path)

#     print(f"\nReading: {pdf_path.name}")
#     print(f"Total Pages: {len(document)}")

#     pages = []

#     for page_num in range(len(document)):

#         page = document.load_page(page_num)

#         text = page.get_text("text")

#         print(
#             f"Page {page_num+1}: {len(text.strip())} characters"
#         )

#         if text.strip():

#             pages.append(
#                 {
#                     "document": Path(pdf_path).name,
#                     "page": page_num + 1,
#                     "text": text,
#                 }
#             )

#     document.close()

#     print(f"Extracted Pages: {len(pages)}")

#     return pages
 
# if __name__ == "__main__":

#     # Get the project root folder automatically
#     BASE_DIR = Path(__file__).resolve().parent.parent

#     # Path to your PDF
#     pdf_path = BASE_DIR / "data" / "Data Structures and Algorithms with Python.pdf"

#     # Check whether the PDF exists
#     if not pdf_path.exists():
#         print(f"❌ PDF not found at:\n{pdf_path}")
#         exit()

#     # Extract text
#     pages = extract_text_from_pdf(pdf_path)

#     print("=" * 60)
#     print("✅ PDF Successfully Loaded")
#     print("=" * 60)
#     print(f"Document : {pdf_path.name}")
#     print(f"Pages Extracted : {len(pages)}")

#     print("\nFirst Page Preview\n")
#     print("-" * 60)
#     print(pages[0]["text"][:1000])
#     print("-" * 60)
    


# import fitz  # PyMuPDF
# import easyocr
# import numpy as np
# from pathlib import Path

# # ----------------------------
# # Load OCR Model (only once)
# # ----------------------------
# reader = easyocr.Reader(
#     ["en"],
#     gpu=False,  # Change to True if using CUDA
# )


# # ----------------------------
# # Extract Text from PDF
# # ----------------------------
# def extract_text_from_pdf(pdf_path):

#     document = fitz.open(pdf_path)

#     pages = []

#     print(f"\nReading: {Path(pdf_path).name}")
#     print(f"Total Pages: {len(document)}")

#     for page_num in range(len(document)):

#         page = document.load_page(page_num)

#         # ----------------------------
#         # Try Embedded Text First
#         # ----------------------------
#         text = page.get_text("text").strip()

#         # ----------------------------
#         # OCR Fallback
#         # ----------------------------
#         if len(text) < 50:

#             pix = page.get_pixmap(dpi=300)

#             image = np.frombuffer(
#                 pix.samples,
#                 dtype=np.uint8,
#             )

#             image = image.reshape(
#                 pix.height,
#                 pix.width,
#                 pix.n,
#             )

#             # Remove alpha channel if present
#             if pix.n == 4:
#                 image = image[:, :, :3]

#             result = reader.readtext(image)

#             text = "\n".join(
#                 item[1]
#                 for item in result
#             )

#         # ----------------------------
#         # Save Page
#         # ----------------------------
#         if text.strip():

#             pages.append(
#                 {
#                     "document": Path(pdf_path).name,
#                     "page": page_num + 1,
#                     "text": text,
#                 }
#             )

#         print(
#             f"Page {page_num + 1}/{len(document)} "
#             f"Characters: {len(text)}"
#         )

#     document.close()

#     print(f"\nExtracted Pages: {len(pages)}")

#     return pages


# # ----------------------------
# # Testing
# # ----------------------------
# if __name__ == "__main__":

#     BASE_DIR = Path(__file__).resolve().parent.parent

#     pdf_path = (
#         BASE_DIR
#         / "data"
#         / "1_Color-Atlas-of-Dental-Medicine-Radiology (1).pdf"
#     )

#     if not pdf_path.exists():
#         print(f"PDF not found:\n{pdf_path}")
#         exit()

#     pages = extract_text_from_pdf(pdf_path)

#     print("\n" + "=" * 60)
#     print("PDF Successfully Loaded")
#     print("=" * 60)
#     print(f"Document : {pdf_path.name}")
#     print(f"Pages Extracted : {len(pages)}")

#     if pages:
#         print("\nFirst Page Preview\n")
#         print("-" * 60)
#         print(pages[0]["text"][:1000])
#         print("-" * 60)

import fitz  # PyMuPDF
import easyocr
import cv2
import numpy as np
from pathlib import Path

# ----------------------------
# Load OCR Model (only once)
# ----------------------------
reader = easyocr.Reader(
    ["en"],
    gpu=False
)


# ----------------------------
# Image Preprocessing
# ----------------------------
def preprocess_image(image):

    # RGBA -> RGB
    if image.shape[2] == 4:
        image = cv2.cvtColor(
            image,
            cv2.COLOR_RGBA2RGB
        )

    # RGB -> Gray
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )

    # Enlarge image
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Remove noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Adaptive Threshold
    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    return gray


# ----------------------------
# Extract Text
# ----------------------------
def extract_text_from_pdf(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    print("\nReading:", Path(pdf_path).name)
    print("Total Pages:", len(document))

    for page_num in range(len(document)):

        page = document.load_page(page_num)

        # --------------------------------
        # Try normal text extraction first
        # --------------------------------
        text = page.get_text("text").strip()

        # --------------------------------
        # OCR if page has no embedded text
        # --------------------------------
        if len(text) < 20:

            pix = page.get_pixmap(
                dpi=300
            )

            image = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            )

            image = image.reshape( 
                pix.height,
                pix.width,
                pix.n
            )

            processed = preprocess_image(
                image
            )

            result = reader.readtext(
                processed,
                detail=0,
                paragraph=True
            )

            text = "\n".join(result)

        pages.append(
            {
                "document": Path(pdf_path).name,
                "page": page_num + 1,
                "text": text,
            }
        )

        print(
            f"Page {page_num+1}/{len(document)} "
            f"Characters: {len(text)}"
        )

    document.close()

    print("\nExtracted Pages:", len(pages))

    return pages


# ----------------------------
# Testing
# ----------------------------
if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    pdf_path = (
        BASE_DIR /
        "data" /
        "1_Color-Atlas-of-Dental-Medicine-Radiology (1).pdf"
    )

    pages = extract_text_from_pdf(
        pdf_path
    )

    print("\n" + "=" * 60)
    print("PDF Successfully Loaded")
    print("=" * 60)

    print("Document :", pdf_path.name)
    print("Pages Extracted :", len(pages))

    if pages:

        print("\nFirst Page Preview\n")

        print("-" * 60)

        print(
            pages[0]["text"][:1000]
        )

        print("-" * 60)