from __future__ import annotations

import string
from typing import NamedTuple


class Wordle(str):
    def __new__(cls, word: str) -> Wordle:
        if isinstance(word, Wordle):
            return word
        return super().__new__(cls, word.lower())


class Clue(list):
    def __init__(self, word: Wordle, signal: list[int] = None):
        self.word = word
        if signal is None:
            signal = [0] * len(word)
        else:
            if len(signal) != len(word):
                raise ValueError("Signal length must match word length")
        super().__init__(signal)

    def same(self, other: Clue) -> bool:
        return self.word == other.word and self == other

    @classmethod
    def from_compare(cls, guess: Wordle | str, key: Wordle | str) -> Clue:
        guess, key = Wordle(guess), Wordle(key)
        return cls(guess, compare(guess, key))


def compare(guess: str, key: str) -> list[int]:
    n = len(guess)
    signal = [0] * n

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
        ziplist = tuple(zip(*list_))
        self.words: tuple[Wordle] = ziplist[0]
        self.weights: tuple[int] = ziplist[1]
        super().__init__(list_)
