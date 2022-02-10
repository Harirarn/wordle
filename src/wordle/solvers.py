import math
from typing import Type

from wordle import core
from wordle.wordle import Clue, WeightedWordle, Wordle, WordleList, compare


class PruningWordleList:
    def __init__(self, masterlist: list[tuple[str, int]] | list[str] | WordleList):
        if not isinstance(masterlist, WordleList):
            masterlist = WordleList(masterlist)
        self.masterlist = masterlist
        self.reset()

    def reset(self) -> None:
        self.wordlelist = [word for word in self.masterlist if word.weight > 0]

    def add_clue(self, clue: Clue) -> None:
        word = clue.word
        if word not in self.masterlist.words:
            raise ValueError("Clue not in wordlist")
        if len(clue) != len(word):
            raise ValueError("Signal length invalid")
        self.wordlelist = [
            key for key in self.wordlelist if compare(word, key.word) == clue
        ]

    def list(self) -> list[Wordle]:
        return [word.word for word in self.wordlelist]


class StatisticalSolver(PruningWordleList):
    def score(self, word: Wordle) -> float:
        if not isinstance(word, Wordle):
            word = Wordle(word)
        boxes: dict[tuple[int, ...], int] = {}
        for key in self.wordlelist:
            if key.weight == 0 or key.word == word:
                continue
            signal = tuple(compare(word, key.word))
            boxes[signal] = boxes.setdefault(signal, 0) + key.weight
        s = 0.0
        numwords = len(self.wordlelist)
        for signal, n in boxes.items():
            if n == 0:
                continue
            s += self.score_formula(n, numwords, signal.count(0))
        return s

    @staticmethod
    def score_formula(n, numwords, blacks):
        return n * n

    def compute(self, wordles: list[Wordle]) -> list[tuple[float, Wordle]]:
        scores = {word: self.score(word) for word in wordles}
        ss = [(s, w) for w, s in scores.items()]
        ss.sort()
        return ss

    def _best(
        self, n: int, wordles: list[WeightedWordle]
    ) -> list[tuple[Wordle, float]]:
        bestlist = self.compute([word.word for word in wordles])
        if n > 0 and n < len(bestlist):
            bestlist = bestlist[:n]
        return [(w, s) for s, w in bestlist]

    def besth(self, n: int) -> list[tuple[Wordle, float]]:
        return self._best(n, self.wordlelist)

    def best(self, n: int) -> list[tuple[Wordle, float]]:
        if len(self.wordlelist) == 1:
            return [(self.wordlelist[0].word, 1.0)]
        return self._best(n, self.masterlist)

    def guess(self) -> Wordle:
        return self.besth(1)[0][0]


class BlackSolver(StatisticalSolver):
    @staticmethod
    def score_formula(n, numwords, blacks):
        return n * n / (blacks + 1)


class EntropySolver(StatisticalSolver):
    @staticmethod
    def score_formula(n, numwords, blacks):
        return n / numwords * math.log(n, 2)


class BlackEntropySolver(EntropySolver):
    @staticmethod
    def score_formula(n, numwords, blacks):
        return n / numwords * math.log(n, 2) / (blacks + 1)


solversdict: dict[str, Type[core.WordleSolver]] = {
    "default": StatisticalSolver,
    "statistical": StatisticalSolver,
    "black": BlackSolver,
    "entropy": EntropySolver,
    "blackentropy": BlackEntropySolver,
}
