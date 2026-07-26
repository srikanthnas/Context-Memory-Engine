from document_processing.parsers.base_parser import BaseParser


class TXTParser(BaseParser):

    def extract_text(self, filepath: str) -> str:

        with open(
            filepath,
            "r",
            encoding="utf-8",
        ) as file:

            return file.read()