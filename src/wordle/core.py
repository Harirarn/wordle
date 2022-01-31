from __future__ import annotations

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
