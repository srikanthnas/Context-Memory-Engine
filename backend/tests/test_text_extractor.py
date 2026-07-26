from document_processing.text_extractor import TextExtractor

text = TextExtractor.extract("uploads/hello.txt")

print("\n===== EXTRACTED TEXT =====\n")
print(text)