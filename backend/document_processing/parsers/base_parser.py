from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
    Abstract base class for all document parsers.
    """

    @abstractmethod
    def extract_text(self, filepath: str) -> str:
        """
        Extract text from a document.
        """
        pass