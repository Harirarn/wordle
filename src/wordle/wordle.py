from __future__ import annotations

import string
from typing import NamedTuple


class Wordle(str):
    def __new__(cls, word: str) -> Wordle:
        if isinstance(word, Wordle):
            return word
        return super().__new__(cls, word.lower())

    def compare(self, key: Wordle) -> Clue:
        return compare(self, key)

    def guess(self, guess: Wordle) -> Clue:
        return compare(guess, self)


class Clue(list):
    def __init__(self, word: Wordle, signal: list[int] = None):
        self.word = word
        if signal is None:
            signal = [0] * len(word)
        else:
            if len(signal) != len(word):
                raise ValueError("Signal length must match word length")
        super().__init__(signal)


def compare(guess: str, key: str) -> Clue:
    n = len(guess)
    signal = Clue(guess)

    # Compare greens
    for i in range(n):
        if guess[i] == key[i]:
            signal[i] = 2

    # Compare yellows
    for letter in string.ascii_lowercase:
        if letter not in guess or letter not in key:
            continue
        w = [(letter == L) - (letter == k) for L, k in zip(guess, key)]
        s = w.count(-1)
        for i in range(n):
            if s == 0:
                break
            if w[i] > 0:
                signal[i] = 1
                s -= 1

    return signal


class WeightedWordle(NamedTuple):
    word: Wordle
    weight: int


class WordleList(list):
    def __init__(self, wordlelist: list[tuple[str, int] | str]):
        if isinstance(wordlelist[0], str):
            list_ = [WeightedWordle(Wordle(word), 1) for word in wordlelist]
        else:
            list_ = [WeightedWordle(Wordle(word[0]), word[1]) for word in wordlelist]
        list_.sort(reverse=True)
        super.__init__(list_)
