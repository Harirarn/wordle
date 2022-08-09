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
        if len(clue) != len(word):
            raise ValueError("Signal length invalid")
        self.wordlelist = [
            key for key in self.wordlelist if compare(word, key.word) == clue
        ]
        self.hmf.add_clue(clue)

    def list(self) -> list[Wordle]:
        return [word.word for word in self.wordlelist]


class StatisticalSolver(PruningWordleList):
    def score(self, word: Wordle, hard: bool = False) -> float:
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
            s += self.score_formula(n, numwords, signal.count(0), hard=hard)
        s = self.post_process_score(s)
        if word in [w.word for w in self.wordlelist]:
            s *= (numwords - 1) / numwords
        return s

    @classmethod
    def post_process_score(cls, s: float) -> float:
        return s

    @classmethod
    def score_formula(
        cls, n: float, numwords: float, blacks: int, hard: bool = False
    ) -> float:
        return n * n

    def compute(
        self, wordles: list[Wordle], hard: bool = False
    ) -> list[tuple[float, Wordle]]:
        scores = {word: self.score(word, hard=hard) for word in wordles}
        ss = [(s, w) for w, s in scores.items()]
        ss.sort()
        return ss

    def _best(
        self, n: int, wordles: list[WeightedWordle], hardmode: bool = False
    ) -> list[tuple[Wordle, float]]:
        testwords = [word.word for word in wordles]
        if hardmode:
            testwords = list(self.hmf.filter(testwords))
        bestlist = self.compute(testwords, hard=hardmode)
        if n > 0 and n < len(bestlist):
            bestlist = bestlist[:n]
        return [(w, s) for s, w in bestlist]

    def besth(self, n: int) -> list[tuple[Wordle, float]]:
        return self._best(n, self.masterlist, True)

    def best(self, n: int) -> list[tuple[Wordle, float]]:
        return self._best(n, self.masterlist, False)

    def guess(self) -> Wordle:
        return self.besth(1)[0][0]


class BlackSolver(StatisticalSolver):
    @classmethod
    def score_formula(
        cls, n: float, numwords: float, blacks: int, hard: bool = False
    ) -> float:
        return n * n / (blacks + 1)


class EntropySolver(StatisticalSolver):
    tpe = {
        True: [0.29074625, 0.57828474, 0.40057718, 0.31091934, 0.26057674, 0.2367127],
        False: [0.27205125, 0.46766151, 0.34938985, 0.29067934, 0.25604451, 0.23561666],
    }

    @classmethod
    def turn_per_entropy(cls, entropy: float, blacks: int, hard: bool = False) -> float:
        return entropy * cls.tpe[hard][blacks]

    @classmethod
    def score_formula(
        cls, n: float, numwords: float, blacks: int, hard: bool = False
    ) -> float:
        entropy = n / numwords * math.log(n, 2)
        return cls.turn_per_entropy(entropy, blacks, hard=hard)

    @classmethod
    def post_process_score(cls, s: float) -> float:
        return s + 1


class BlackEntropySolver(EntropySolver):
    @classmethod
    def score_formula(
        cls, n: float, numwords: float, blacks: int, hard: bool = False
    ) -> float:
        return n / numwords * math.log(n, 2) / (blacks + 1)


solversdict: dict[str, Type[core.WordleSolver]] = {
    "default": StatisticalSolver,
    "statistical": StatisticalSolver,
    "black": BlackSolver,
    "entropy": EntropySolver,
    "blackentropy": BlackEntropySolver,
}
