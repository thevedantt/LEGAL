import fitz  # PyMuPDF

def parse_pdf(file_path):
    """
    Parses a PDF, returns text or raises informative exception.
    """
    try:
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        raise RuntimeError(f"PDF parsing failed: {e}")
