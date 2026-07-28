from llm.gemini_client import GeminiClient


class LLMManager:
    """
    Central manager for all LLM interactions.
    """

    def __init__(self):
        self.client = GeminiClient()

    def generate(self, prompt: str) -> str:
        """
        Generate an AI response.
        """

        return self.client.generate_response(prompt)