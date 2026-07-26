from document_processing.parsers.parser_factory import ParserFactory


class TextExtractor:
    """
    Delegates extraction to the appropriate parser.
    """

    @staticmethod
    def extract(file_path: str) -> str:

        parser = ParserFactory.get_parser(file_path)

        return parser.extract_text(file_path)