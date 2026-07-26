from memory.memory_engine import MemoryEngine

engine = MemoryEngine()

result = engine.process_prompt(
    user_id=1,
    prompt="   What is Machine Learning?   "
)

print(result)