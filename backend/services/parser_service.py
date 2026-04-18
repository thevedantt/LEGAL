import fitz  # PyMuPDF
from docx import Document

class ParserService:
    @staticmethod
    def parse_pdf(file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    @staticmethod
    def parse_docx(file_path):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
