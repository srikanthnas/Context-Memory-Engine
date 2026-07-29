from llm.gemini_client import GeminiClient


class ConversationSummarizer:
    """
    Generates concise summaries for conversations.
    """

    def __init__(self):
        self.llm = GeminiClient()

    def summarize(
        self,
        title: str,
        messages: list,
    ) -> str:
        """
        Generate a concise summary of a conversation.
        """

        conversation = ""

        for message in messages:
            role = message["role"].capitalize()
            conversation += f"{role}: {message['content']}\n"

        prompt = f"""
You are creating long-term memory for an AI assistant.

Summarize the following conversation.

Requirements:
- Maximum 120 words.
- Preserve important facts.
- Preserve user preferences.
- Preserve discussed projects.
- Preserve important decisions.
- Ignore greetings and small talk.

Conversation Title:
{title}

Conversation:
{conversation}

Summary:
"""

        response = self.llm.generate(prompt)

        return response.strip() if response else ""