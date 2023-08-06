

def divide_chunks(array: list, size: int):
    # looping till length l
    for i in range(0, len(array), size):
        yield array[i:i + size]
