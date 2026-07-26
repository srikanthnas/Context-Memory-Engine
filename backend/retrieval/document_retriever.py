from document_processing.text_extractor import TextExtractor
from document_processing.chunker import DocumentChunker


class DocumentRetriever:
    """
    Retrieves relevant chunks from documents.

    Current implementation:
    - Extract text
    - Chunk text
    - Return every chunk

    Future implementation:
    - Embedding search
    - Return only relevant chunks
    """

    @staticmethod
    def retrieve(
        filepath: str,
        chunk_size: int = 500,
    ) -> list[str]:

        text = TextExtractor.extract(filepath)

        chunks = DocumentChunker.chunk_text(
            text=text,
            chunk_size=chunk_size,
        )

        return chunks