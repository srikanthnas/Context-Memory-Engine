from document_processing.text_extractor import TextExtractor
from document_processing.chunker import DocumentChunker

text = TextExtractor.extract("uploads/hello.txt")

chunks = DocumentChunker.chunk_text(
    text,
    chunk_size=10,
)

print("\n===== CHUNKS =====\n")

for index, chunk in enumerate(chunks, start=1):
    print(f"Chunk {index}: {chunk}")