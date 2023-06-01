import os.path
import sqlite3

absolute_path = os.path.dirname(__file__)

_conn = sqlite3.connect(
    os.path.join(absolute_path, "./data/sentences.db"))
_conn.enable_load_extension(True)
_conn.load_extension(
    os.path.join(absolute_path, "spellfix"))
_conn.enable_load_extension(False)

cursor = _conn.cursor()


def word_exists(word: str) -> bool:
    """
    Returns true if word exists in database.
    """

    result = cursor.execute(
        """
        SELECT
            word
        FROM
            word_counts
        WHERE
            word = :word
        """,
        {"word": word}
    ).fetchone()

    return result is not None


def get_closest_words(word: str, n: int = 3, min_dist: int = 2, max_dist: int = 4, min_len: int = 5) -> list:
    """
    Returns n closest words to word, by edit distance.
    """

    result = cursor.execute(
        """
        SELECT
            tokens.word as w,
            distance,
            count,
            score
        FROM
            tokens
        INNER JOIN
            word_counts ON word_counts.word = w
        WHERE
                w
            MATCH
                :param
            AND
                w NOT LIKE :like
            AND
                distance >= :min_dist
            AND
                distance <= :max_dist
            AND
                LENGTH(w) >= :min_len
        ORDER BY
            score ASC,
            count DESC
        LIMIT
            :limit
        """,
        {"param": word, "like": "%" + word + "%", "limit": n,
            "min_dist": min_dist, "max_dist": max_dist, "min_len": min_len}
    ).fetchall()

    return [word[0] for word in result] if result else []


def get_sentences(word: str, n: int = 3) -> list[str]:
    """Returns n sentences that include the given word"""

    result = cursor.execute(
        """
        SELECT
            sentence
        FROM
            sentences
        WHERE
            sentence MATCH :param
        LIMIT
            :limit
        """,
        {"param": word, "limit": n}
    ).fetchall()

    return [sentence[0] for sentence in result] if result else []
