import math
from typing import Type

from wordle import core
from wordle.wordle import (
    Clue,
    HardModeFilter,
    WeightedWordle,
    Wordle,
    WordleList,
    compare,
)


class PruningWordleList:
    def __init__(self, masterlist: list[tuple[str, int]] | list[str] | WordleList):
        if not isinstance(masterlist, WordleList):
            masterlist = WordleList(masterlist)
        self.masterlist = masterlist
        self.hmf = HardModeFilter()
        self.reset()

    def reset(self) -> None:
        self.wordlelist = [word for word in self.masterlist if word.weight > 0]
        self.hmf.reset()

    def add_clue(self, clue: Clue) -> None:
        word = clue.word
        if word not in self.masterlist.words:
            raise ValueError("Clue not in wordlist")
        if len(clue) != len(word):
            raise ValueError("Signal length invalid")
        self.wordlelist = [
            key for key in self.wordlelist if compare(word, key.word) == clue
        ]
        self.hmf.add_clue(clue)

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
        self, n: int, wordles: list[WeightedWordle], hardmode: bool = False
    ) -> list[tuple[Wordle, float]]:
        testwords = [word.word for word in wordles]
        if hardmode:
            testwords = list(self.hmf.filter(testwords))
        bestlist = self.compute(testwords)
        if n > 0 and n < len(bestlist):
            bestlist = bestlist[:n]
        return [(w, s) for s, w in bestlist]

    def besth(self, n: int) -> list[tuple[Wordle, float]]:
        return self._best(n, self.masterlist, True)

    def best(self, n: int, hardmode: bool = False) -> list[tuple[Wordle, float]]:
        if len(self.wordlelist) == 1:
            return [(self.wordlelist[0].word, 1.0)]
        return self._best(n, self.masterlist, False)

    def guess(self) -> Wordle:
        return self.besth(1)[0][0]


class BlackSolver(StatisticalSolver):
    @staticmethod
    def score_formula(n, numwords, blacks):
        return n * n / (blacks + 1)


class EntropySolver(StatisticalSolver):
    def score(self, word: Wordle) -> float:
        if not isinstance(word, Wordle):
            word = Wordle(word)
        boxes: dict[tuple[int, ...], int] = {}
        for key in self.wordlelist:
            if key.weight == 0:
                continue
            signal = tuple(compare(word, key.word))
            boxes[signal] = boxes.setdefault(signal, 0) + key.weight
        s = 0.0
        numwords = len(self.wordlelist)
        for signal, n in boxes.items():
            if n == 0:
                continue
            s += self.score_formula(n, numwords, signal.count(0))
        s = self.turn_per_entropy(s) + 1
        if word in [w.word for w in self.wordlelist]:
            s *= (numwords - 1) / numwords
        return s

    @staticmethod
    def turn_per_entropy(x: float) -> float:
        return x * 0.31

    @staticmethod
    def score_formula(n, numwords, blacks):
        return n / numwords * math.log(n, 2)

    def besth(self, n: int) -> list[tuple[Wordle, float]]:
        return self._best(n, self.masterlist, True)


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
