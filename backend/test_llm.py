from llm.llm_manager import LLMManager

llm = LLMManager()

response = llm.generate(
    "What is Artificial Intelligence?"
)

print(response)