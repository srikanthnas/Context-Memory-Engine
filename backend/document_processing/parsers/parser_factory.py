from pathlib import Path

from document_processing.parsers.txt_parser import TXTParser
from document_processing.parsers.pdf_parser import PDFParser


class ParserFactory:

    @staticmethod
    def get_parser(filepath: str):

        extension = Path(filepath).suffix.lower()

        parsers = {
            ".txt": TXTParser(),
            ".pdf": PDFParser(),
        }

        parser = parsers.get(extension)

        if parser is None:
            raise ValueError(
                f"No parser available for {extension}"
            )

        return parser