from memory.prompt_manager import PromptManager

manager = PromptManager()

result = manager.prepare_prompt(
    user_id=1,
    prompt="   Explain transformers.   "
)

print(result)