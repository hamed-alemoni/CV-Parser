from typing import Iterator
def search_word(text: str, words: Iterator[str]) -> int:
    for word in words:
        index = text.find(word)
        if index != -1:
            return index
        
    return -1


def find_text(text: str, words: Iterator[str]) -> str:
    text = text.lower()
    index = search_word(text, words)
    if index != -1:
        text = text[index:]
    return text


def get_unique_list(X: list[str]) -> list[str]:
    return list(set(X))