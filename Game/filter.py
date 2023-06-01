import re
from . import resources

ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz "

C = ['z', 'y', 'v', 't', 'ş', 's', 'r', 'p', 'n', 'r',
     'm', 'l', 'k', 'h', 'j', 'ğ', 'g', 'd', 'ç', 'c', 'b']
V = ['a', 'e', 'ı', 'i', 'o', 'ö', 'u', 'ü']
NOT_POSSIBLE_PATTERNS = [
    r"\bCC",
    r"\bVV",
    r"CCC\b",
    r"VV\b",
    r"VV"
]


def get_word_pattern(word: str):
    """Returns a vowel-consonant pattern (e.g. VVCC, CVCC) of a given string"""

    pattern = ""
    for char in word:
        if char in C:
            pattern += "C"
        if char in V:
            pattern += "V"
    return pattern


def is_valid_word(word: str) -> bool:
    """Checks to see whether a given string is possible as a word in Turkish, returns True if it is."""

    if word in resources.unwanted_words:
        return False

    if word.startswith("ğ") or word.endswith("ğ") or not all(char in ALPHABET for char in word):
        return False

    pattern = get_word_pattern(word)
    if re.search('|'.join(NOT_POSSIBLE_PATTERNS), pattern):
        return False

    return True
