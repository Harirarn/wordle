import json
import math
from argparse import ArgumentParser, Namespace

import numpy as np
from numpy.linalg import lstsq

from wordle.loaders import load_wordlelist
from wordle.solvers import PruningWordleList
from wordle.wordle import Clue


def parse() -> Namespace:
    parser = ArgumentParser(description="Wordle Entropy-Turn relation analyzer")
    parser.add_argument("file", type=str, help="Benchmark file to analyze")
    parser.add_argument("--output", type=str, help="Output file")
    parser.add_argument("-p", "--plot", action="store_true", help="Plot the data")

    return parser.parse_args()


def main() -> None:
    args = parse()
    with open(args.file) as f:
        data = json.load(f)

    wl = PruningWordleList(load_wordlelist())

    table = calc_datatable(data, wl)

    if args.output is None:
        if args.file[:9] == "benchmark":
            outfile = f"entval_{args.file[9:]}"
        else:
            outfile = f"entval_{args.file}"
    else:
        outfile = args.output
    with open(outfile, "w") as f:
        json.dump(table, f)

    if args.plot:
        import matplotlib.pyplot as plt

    for black, data in enumerate(table):
        x, y = zip(*data)
        tpe = calc_slope(x, y, intercept=1.0)
        if args.plot:
            plt.clf()
            plt.plot(
                x,
                y,
                label=f"{black} blacks" if black > 0 else "All",
                alpha=0.03,
                color="blue",
                marker="o",
                markeredgewidth=0.0,
                linestyle="None",
            )
            x_ = np.linspace(min(x), max(x), 2)
            plt.plot(x_, tpe * x_ + 1, color="blue")
            plt.xlabel("Entropy")
            plt.ylabel("Tries")
            plt.title(f"Entropy-Tries relation for {black} slope {tpe:.2f}")
            plt.savefig(f"entval_{black}_{args.file[9:-5]}.png")
        else:
            if black > 0:
                print(f"{black} black: {tpe:.4f}")
            else:
                print(f"Average: {tpe:.4f}")


def calc_datatable(data: dict, wl: PruningWordleList) -> list[list[tuple[float, int]]]:
    table: list[list[tuple[float, int]]] = [[] for _ in range(len(list(data)[0]) + 1)]

    for keydata in data.values():
        wl.reset()
        for tries, guess in zip(
            range(keydata["tries"] - 1, -1, -1), keydata["guesses"]
        ):
            if tries == 0:
                break
            wl.add_clue(Clue(guess[0], guess[2]))
            blacks = guess[2].count(0)
            entropy = math.log2(len(wl.list()))
            table[0].append((entropy, tries))
            table[blacks].append((entropy, tries))
    return table


def calc_slope(x: list[float], y: list[float], intercept: float = 0.0) -> float:
    m, _, _, _ = lstsq(np.array(x)[:, np.newaxis], np.array(y) - intercept, rcond=None)
    return m[0]


def calc_turns_per_entropy(table: list[list[tuple[float, int]]]) -> list[float]:
    result = []
    for xy in table:
        x, y = [i[0] for i in xy], [i[1] for i in xy]
        result.append(calc_slope(x, y, intercept=1.0))  # type: ignore
    return result


if __name__ == "__main__":
    main()
