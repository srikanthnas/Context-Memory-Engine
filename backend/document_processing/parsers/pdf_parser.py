from pypdf import PdfReader

from document_processing.parsers.base_parser import BaseParser


class PDFParser(BaseParser):
    """
    Extract text from PDF documents.
    """

    def extract_text(self, filepath: str) -> str:

        reader = PdfReader(filepath)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)