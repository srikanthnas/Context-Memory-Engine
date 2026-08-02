"""
Memory Engine Configuration
"""

# Minimum score required for a memory to be considered.
MIN_MEMORY_SCORE = 0.60

# Maximum memories passed to the LLM.
MAX_MEMORY_ITEMS = 8

# Maximum memories of each type.
MAX_DOCUMENTS = 3
MAX_CONVERSATIONS = 2
MAX_MESSAGES = 2

# Phase 32:
# Allow multiple persistent user-profile facts
# to participate in final context.
MAX_PREFERENCES = 3