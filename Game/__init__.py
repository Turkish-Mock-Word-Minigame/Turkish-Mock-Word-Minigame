from . import word_generator
import re
from random import shuffle


class _game:
    def __init__(self):
        self.sentence = ""
        self.real_word = ""

    def generate_question(self) -> dict[str, str]:
        mock_word = word_generator.generate_word()
        real_word = word_generator.get_real_word(mock_word)
        sentence = word_generator.get_sentence(real_word)

        options = [real_word, mock_word]
        shuffle(options)

        question = {
            "sentence": re.sub(fr'\b{real_word}\b', '_' * 8, sentence),
            "options": options
        }

        self.sentence = sentence
        self.real_word = real_word

        return question

    def check_answer(self, answer: str) -> tuple[bool, str]:
        return answer == self.real_word, self.real_word, self.sentence


game = _game()

generate_question = game.generate_question
check_answer = game.check_answer
