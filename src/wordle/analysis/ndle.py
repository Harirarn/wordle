from typing import Iterable

import numpy as np

from wordle import core, loaders, solvers
from wordle.wordle import Wordle, compare

wl = loaders.load_wordlelist()
pruner = solvers.PruningWordleList(wl)
player = core.PlaySession(wl)
cl = pruner.list()

freql = [
    "e",
    "a",
    "r",
    "o",
    "t",
    "l",
    "i",
    "s",
    "n",
    "c",
    "u",
    "y",
    "d",
    "h",
    "p",
    "m",
    "g",
    "b",
    "f",
    "k",
    "w",
    "v",
    "z",
    "x",
    "q",
    "j",
]
freqs = set(freql[:18])

cli = []
for word in cl:
    if len(set(word)) == 5 and set(word).issubset(freqs):
        cli.append(word)


def score(words: Iterable[core.Wordle]) -> tuple[float, list[int]]:
    tries: dict[tuple[int, ...], int] = {}
    for ans in cl:
        s: list[int] = []
        for word in words:
            s.extend(compare(word, ans))
        st: tuple[int, ...] = tuple(s)
        tries[st] = tries.get(st, 0) + 1
    tries_list = list(tries.values())
    data = np.array(tries_list, dtype=np.float64)
    n = sum(data)
    return np.sum(data * np.log2(data)) / n, tries_list


data: list[tuple[Wordle, Wordle, float]] = []
for i, w1 in enumerate(cli):
    for w2 in cli[i + 1 :]:  # noqa: E203
        if len(set(w1) | set(w2)) < 10:
            continue
        print(f"{i}/{len(cli)} {w1} {w2}", end="\r")
        data.append((w1, w2, score([w1, w2])[0]))

scores = [d[2] for d in data]

ranks = np.argsort(scores)
data = [data[i] for i in ranks]

for i in range(10):
    print(data[i])

with open("2word.csv", "w") as f:
    for d in data:
        f.write(f"{d[0]},{d[1]},{d[2]}\n")
