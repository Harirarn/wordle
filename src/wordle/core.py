from __future__ import annotations

import random
from typing import Literal, Protocol

from wordle.wordle import Clue, HardModeFilter, Wordle, WordleList


class WordleSolver(Protocol):
    def __init__(self, masterlist: WordleList):
        ...

    def reset(self) -> None:
        ...

    def add_clue(self, clue: Clue) -> None:
        ...

    def best(self, n: int) -> list[tuple[Wordle, float]]:
        ...

    def besth(self, n: int) -> list[tuple[Wordle, float]]:
        ...

    def list(self) -> list[Wordle]:
        ...


class HardModeInvalid(Exception):
    pass


class PlaySession:
    def __init__(
        self,
        wordlist: WordleList,
        mode: Literal["easy", "hard"] = "easy",
        ans: Wordle | str | None = None,
    ):
        self.masterlist = wordlist
        self.hard_filter = HardModeFilter()
        self.mode = mode
        self.new(ans)

    def new(self, ans: Wordle | str | None = None) -> None:
        if ans is not None:
            if ans not in self.masterlist.words:
                raise ValueError("Invalid answer")
            self.choice = Wordle(ans)
        else:
            self.choice = random.choices(
                self.masterlist.words, weights=self.masterlist.weights
            )[0]
        self.tries = 0
        self.hard_filter.reset()

    def guess(self, guess: str | Wordle) -> Clue:
        guess = Wordle(guess)
        if guess not in self.masterlist.words:
            raise ValueError("Invalid guess")
        if self.mode == "hard" and (missing := self.hard_filter.test(guess)):
            raise HardModeInvalid(
                f"Invalid guess for hard mode. Must contain {missing}", missing
            )
        self.tries += 1
        clue = Clue.from_compare(guess, self.choice)
        self.hard_filter.add_clue(clue)
        return clue

    def answer(self) -> Wordle:
        return self.choice
