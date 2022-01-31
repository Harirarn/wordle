from __future__ import annotations

import random
from typing import Protocol

from wordle.wordle import Clue, Wordle, WordleList


class WordleSolver(Protocol):
    def __init__(self, masterlist: WordleList):
        ...

    def reset(self):
        ...

    def add_clue(self, clue: Clue):
        ...

    def best(self, n: int) -> list[tuple[Wordle, float]]:
        ...

    def besth(self, n: int) -> list[tuple[Wordle, float]]:
        ...

    def list(self) -> list[Wordle]:
        ...


class PlaySession:
    def __init__(self, wordlist: WordleList):
        self.masterlist = wordlist
        self.new()

    def new(self):
        self.choice = random.choices(
            self.masterlist.words, weights=self.masterlist.weights
        )[0]
        self.tries = 0

    def guess(self, guess: str | Wordle) -> Clue:
        if guess not in self.masterlist.words:
            raise ValueError("Invalid guess")
        self.tries += 1
        return Clue.from_compare(guess, self.choice)

    def answer(self) -> Wordle:
        return self.choice
