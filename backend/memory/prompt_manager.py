"""
Prompt Manager

This module receives every prompt from the frontend
and prepares it for the Context Memory Engine.
"""


class PromptManager:
    """Handles user prompts before memory retrieval."""

    def __init__(self):
        pass

    def prepare_prompt(self, user_id: int, prompt: str) -> dict:
        """
        Prepare a user prompt for processing.

        Args:
            user_id: Unique user identifier
            prompt: User's input prompt

        Returns:
            Dictionary containing prompt metadata.
        """

        return {
            "user_id": user_id,
            "prompt": prompt.strip()
        }