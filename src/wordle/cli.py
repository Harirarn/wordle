from argparse import ArgumentParser, Namespace
from pathlib import Path

from wordle import repl


def parse() -> Namespace:
    parser = ArgumentParser(description="Wordle")
    parser.add_argument(
        "-m",
        "--mode",
        choices=["play", "solve"],
        default="solve",
        help="Solve or Play, [default: %(default)s]",
    )
    parser.add_argument(
        "-d",
        "--difficulty",
        choices=["easy", "hard"],
        default="easy",
        help="Difficulty of the game. Any revealed hints must be used in subsequent\
 guesses in hard mode.",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=5,
        metavar="N",
        help="Word length. [default: %(default)s]",
    )
    parser.add_argument(
        "-w",
        "--wordfile",
        type=Path,
        default=None,
        metavar="FILE",
        help="Custom word list. Default uses the list of alls words from the official\
 wordle. For non-five length game, the default is a BNC COCA word list.",
    )
    parser.add_argument(
        "-s",
        "--solver",
        choices=repl.solversdict.keys(),
        default="default",
        metavar="NAME",
        help="Algorithm to use for solving. Available: "
        f"{', '.join(repl.solversdict.keys())}",
    )
    args = parser.parse_args()
    return args


def main() -> None:
    args = parse()
    repl.REPLoop(
        mode=args.mode,
        difficulty=args.difficulty,
        length=args.length,
        wordfile=args.wordfile,
        solver=args.solver,
    )
