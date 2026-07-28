from llm.gemini_client import GeminiClient

client = GeminiClient()

response = client.generate_response(
    "Say hello in one sentence."
)

print(response)