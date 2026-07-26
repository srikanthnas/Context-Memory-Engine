from document_processing.text_extractor import TextExtractor

text = TextExtractor.extract("uploads/Srikanth resume.pdf")

print("\n===== PDF TEXT =====\n")
print(text)