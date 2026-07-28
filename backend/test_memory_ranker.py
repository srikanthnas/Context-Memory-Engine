from memory.memory_ranker import MemoryRanker


def main():

    print("Document:",
          MemoryRanker.rank("document"))

    print("Conversation:",
          MemoryRanker.rank("conversation"))

    print("Message:",
          MemoryRanker.rank("message"))

    print("Preference:",
          MemoryRanker.rank("preference"))


if __name__ == "__main__":
    main()