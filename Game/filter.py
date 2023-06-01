import re
from . import resources

ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz "

C = ['z', 'y', 'v', 't', 'ş', 's', 'r', 'p', 'n', 'r',
     'm', 'l', 'k', 'h', 'j', 'ğ', 'g', 'd', 'ç', 'c', 'b']
V = ['a', 'e', 'ı', 'i', 'o', 'ö', 'u', 'ü']
SONORANTS = ['m', 'n', 'r', 'l', 'y']
NOT_SONORANTS = ['t', 'p', 'k', 'd', 'b', 'g',
                 'ç', 'c', 'f', 'j', 'v', 's', 'z', 'ş', 'h']

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

    if word[0] in ["ğ"] or word[-1] in ["b", "d", "g", "c", "ğ"] or not all(char in ALPHABET for char in word):
        return False

    pattern = get_word_pattern(word)
    if re.search('|'.join(NOT_POSSIBLE_PATTERNS), pattern):
        return False

    if len(word) >= 2 and word[-2] in C and word[-1] in C:
        if not ((word[-2] in SONORANTS and word[-1] in NOT_SONORANTS) or (word[-2] in NOT_SONORANTS and word[-1] in NOT_SONORANTS)):
            return False

    return True
