import docx

def parse_docx(file_path):
    """
    Parses a DOCX, returns text or raises informative exception.
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        raise RuntimeError(f"DOCX parsing failed: {e}")
