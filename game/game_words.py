import random

ATTEMPTS = 6
users = {}


def get_all_words() -> list[str]:
    """Get all words from file and return list of strings"""
    with open("game/words.txt", 'r', encoding='utf-8') as f:
        words = f.read()
    return list(words.split())


def get_random_word() -> str:
    list_words = get_all_words()
    return list_words[random.randint(0, len(list_words))]


# users[1] = get_random_word()
# print(get_random_word())
# print(users[1]['secret_word'])
