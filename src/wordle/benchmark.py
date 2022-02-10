import json
from pathlib import Path
from typing import Type

from wordle import loaders, solvers
from wordle.core import PlaySession, WordleSolver
from wordle.wordle import Wordle, WordleList

history_depth = 2


def calc_average_score(
    wordlist: WordleList,
    solvertype: Type[WordleSolver],
    firstguess: str = None,
    logfile: str | Path | None = None,
) -> float:
    player = PlaySession(wordlist)
    solver = solvertype(wordlist)
    solver.reset()
    scores: list[int] = []
    data = {}
    history: dict[tuple[tuple[Wordle, tuple[int, ...]], ...], tuple[Wordle, float]] = {}
    if firstguess is not None:
        history[()] = Wordle(firstguess), 0.0
    solvewords = tuple(word.word for word in wordlist if word.weight > 0)
    totalwords = len(solvewords)
    for iword, word in enumerate(solvewords):
        data[str(word)] = {
            "tries": 0,
            "guesses": [],
        }
        player.new(word)
        solver.reset()
        solved = False
        curhist: list[tuple[Wordle, tuple[int, ...]]] = []
        print(f"{iword + 1:4d}/{totalwords}: {word}", end="\r", flush=True)
        while not solved:
            if tuple(curhist) in history:
                guess, points = history[tuple(curhist)]
            else:
                guess, points = solver.besth(1)[0]
                if len(curhist) < history_depth:
                    history[tuple(curhist)] = guess, points
            clue = player.guess(guess)
            data[str(word)]["guesses"].append(  # type: ignore
                (guess, points, tuple(clue))
            )
            if all(i == 2 for i in clue):
                solved = True
                scores.append(player.tries)
                data[str(word)]["tries"] = player.tries
                continue
            solver.add_clue(clue)
            curhist.append((guess, tuple(clue)))
    if logfile is not None:
        with open(logfile, "w") as f:
            json.dump(data, f)
    return sum(scores) / len(scores)


if __name__ == "__main__":
    from argparse import ArgumentParser, Namespace

    def parse() -> Namespace:
        parser = ArgumentParser()
        parser.add_argument(
            "-s",
            "--solver",
            choices=solvers.solversdict.keys(),
            default="default",
            metavar="NAME",
            help="Algorithm to use for solving. Available: "
            f"{', '.join(solvers.solversdict.keys())}",
        )
        parser.add_argument("-l", "--logfile", type=Path, default=None)
        parser.add_argument("-g", "--firstguess", type=str, default=None)
        return parser.parse_args()

    def main() -> None:
        args = parse()
        solver = solvers.solversdict[args.solver]
        wordlist = loaders.load_wordlelist()
        if args.firstguess is not None and Wordle(args.firstguess) not in (
            word.word for word in wordlist if word.weight > 0
        ):
            print(f"{args.firstguess} is not in the wordlist.")
            exit(1)
        if args.logfile is not None:
            logfile = args.logfile
        else:
            if args.firstguess is not None:
                logfile = Path(f"benchmark_{args.solver}_{args.firstguess}.json")
            else:
                logfile = Path(f"benchmark_{args.solver}.json")
        score = calc_average_score(
            wordlist, solver, firstguess=args.firstguess, logfile=logfile
        )
        print(f"For solver: {args.solver} average score: {score:.2f}")

    main()
