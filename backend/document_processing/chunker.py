class DocumentChunker:
    """
    Splits extracted document text into smaller chunks.
    """

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 500,
    ) -> list[str]:

        chunks = []

        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])

        return chunks