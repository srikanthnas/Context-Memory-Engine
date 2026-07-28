"""
Prompt Manager

Receives every prompt from the frontend and prepares it for
the Context Memory Engine.
"""

from datetime import datetime


class PromptManager:
    """
    Handles user prompts before memory retrieval.
    """

    def prepare_prompt(
        self,
        user_id: int,
        prompt: str,
        conversation_id: int | None = None,
        language: str = "English",
    ) -> dict:
        """
        Prepare a prompt with useful metadata.

        Args:
            user_id: User ID
            prompt: User's actual prompt
            conversation_id: Optional conversation ID
            language: Prompt language

        Returns:
            Dictionary containing prompt metadata.
        """

        return {
            "user_id": user_id,
            "prompt": prompt.strip(),          # <-- REAL PROMPT
            "timestamp": datetime.utcnow().isoformat(),
            "conversation_id": conversation_id,
            "language": language,
        }