from typing import List


def sort_words(words: 'List'):
    # save "type" at each position into a list
    # split ints and texts into separate lists, sort independently
    # reconstruct output list using the types at each position to pull from the sorted lists
    pass


def clean_word(word: 'str'):
    #go char-by-char and remove text that isn't either alpha or numeric
    #make allowance for a single minus sign on left side of ints
    #rule for identifying an int: after all dirty content is removed, only digits remain
    pass


def clean_words(words: 'List'):
    cleaned = []
    for word in words:
        cleaned.append(clean_word(word))
    return cleaned


def clean_and_sort(words: 'List'):
    cleaned = clean_words(words)
    return sort_words(cleaned)
