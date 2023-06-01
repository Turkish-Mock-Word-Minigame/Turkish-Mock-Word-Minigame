import random
from scipy.stats import multinomial
from . import filter
from . import db_wrapper
from . import resources

last_word = ""


def __calculateNextGram(current_gram: tuple[str, str]) -> tuple[str, str]:
    """
    Returns the next gram based on the current gram and the
    probabilities of the current gram.
    """

    probable_characters = list(resources.ngram_pbs[current_gram].samples())
    ngram_probabilities = [resources.ngram_pbs[(current_gram)].prob(
        word) for word in probable_characters]

    result = multinomial.rvs(1, ngram_probabilities)
    index_of_probable_word = list(result).index(1)
    gram = (current_gram[1], probable_characters[index_of_probable_word])

    return gram


def generate_mock_word(min_len: int = 5, max_len: int = 8):
    """
    Returns a mock word between given lengths
    """

    global last_word

    generated_ngram_word = ""
    while generated_ngram_word == last_word \
            or len(generated_ngram_word) < min_len \
            or len(generated_ngram_word) > max_len \
            or db_wrapper.word_exists(generated_ngram_word) \
            or not filter.is_valid_word(generated_ngram_word) \
            or len(db_wrapper.get_closest_words(generated_ngram_word)) == 0:

        generated_ngram_word = ""
        current_gram = ("'", "^")

        # create word
        while current_gram[1] != "#":
            new_gram = __calculateNextGram(current_gram)

            if new_gram[1] == "#":
                if len(generated_ngram_word) < min_len:
                    continue
                else:
                    break

            current_gram = new_gram

            # else append the current gram to the generated word
            generated_ngram_word += current_gram[1]

            # if longer than max len then break
            if len(generated_ngram_word) > max_len:
                break

    last_word = generated_ngram_word
    return generated_ngram_word


def get_real_word(word: str):
    """
    Returns the closest real word from the database
    """
    return db_wrapper.get_closest_words(word)[0]


def get_sentence(word: str):
    """
    Returns a sentence with the given word
    """

    return random.choice(db_wrapper.get_sentences(word))
