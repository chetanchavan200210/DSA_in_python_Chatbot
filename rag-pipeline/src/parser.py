import fitz  # PyMuPDF
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """
    Reads a PDF page by page and returns a list of dictionaries.

    Each dictionary contains:
    - document name
    - page number
    - page text
    """

    document = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")

        if text.strip():
            pages.append(
                {
                    "document": Path(pdf_path).name,
                    "page": page_num + 1,
                    "text": text,
                }
            )

    document.close()
    return pages

 
if __name__ == "__main__":

    # Get the project root folder automatically
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Path to your PDF
    pdf_path = BASE_DIR / "data" / "Data Structures and Algorithms with Python.pdf"

    # Check whether the PDF exists
    if not pdf_path.exists():
        print(f"❌ PDF not found at:\n{pdf_path}")
        exit()

    # Extract text
    pages = extract_text_from_pdf(pdf_path)

    print("=" * 60)
    print("✅ PDF Successfully Loaded")
    print("=" * 60)
    print(f"Document : {pdf_path.name}")
    print(f"Pages Extracted : {len(pages)}")

    print("\nFirst Page Preview\n")
    print("-" * 60)
    print(pages[0]["text"][:1000])
    print("-" * 60)
    