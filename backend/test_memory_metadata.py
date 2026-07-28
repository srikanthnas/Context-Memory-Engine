from memory.memory_metadata import MemoryMetadata


def main():

    metadata = MemoryMetadata.create()

    print("New Memory")
    print(metadata)

    metadata = MemoryMetadata.touch(metadata)

    print("\nAfter Access")
    print(metadata)


if __name__ == "__main__":
    main()