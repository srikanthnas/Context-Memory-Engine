"""
Gemini Client

Handles communication with Google's Gemini model.
"""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:
    """
    Generic wrapper around the Google Gemini API.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate text from Gemini using any prompt.
        """

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )

        return response.text

    def generate_response(
        self,
        context: str,
    ) -> str:
        """
        Generate an assistant response using the Context Memory Engine.
        """

        prompt = f"""
You are an intelligent AI assistant with long-term memory.

You are provided with:
- User preferences
- Previous conversations
- Recent messages
- Relevant document excerpts
- The user's current question

INSTRUCTIONS:

1. Read the entire context carefully.
2. Answer the user's question using the retrieved context whenever possible.
3. If the answer exists in the document excerpts, use that information.
4. Do NOT ignore the provided context.
5. If the answer is not available in the context, clearly state that and answer using your general knowledge if appropriate.
6. Be concise, accurate, and helpful.

==================== CONTEXT ====================

{context}

=================================================
"""

        return self.generate(prompt)