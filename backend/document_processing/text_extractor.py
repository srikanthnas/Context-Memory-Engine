from pathlib import Path


class TextExtractor:
    """
    Extracts text from supported document types.
    """

    @staticmethod
    def extract(file_path: str) -> str:

        extension = Path(file_path).suffix.lower()

        if extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        raise ValueError(f"Unsupported file type: {extension}")