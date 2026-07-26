"""
Memory Engine

Coordinates all memory components and builds
the complete context for an incoming prompt.
"""

from memory.prompt_manager import PromptManager


class MemoryEngine:
    """Main orchestrator for the Context Memory Engine."""

    def __init__(self):
        self.prompt_manager = PromptManager()

    def process_prompt(self, user_id: int, prompt: str):
        """
        Process an incoming user prompt.

        Returns:
            Structured prompt ready for memory retrieval.
        """

        prepared_prompt = self.prompt_manager.prepare_prompt(
            user_id=user_id,
            prompt=prompt
        )

        return prepared_prompt