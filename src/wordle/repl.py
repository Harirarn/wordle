from __future__ import absolute_import

import random
from pathlib import Path
from typing import Literal, Type

from wordle import core, loaders, solvers
from wordle.wordle import compare

signal_emoji = "⬛🟨🟩"
DEFAULT_LIST_SIZE = 20
solversdict: dict[str, Type[core.WordleSolver]] = {
    "default": core.DEFAULT_SOLVER,
    "statistical": solvers.StatisticalSolver,
}


help_text = """
This program helps in solving Wordle puzzles.
It stores a list of possible solutions and prunes it down as you enter guesses.
Available commands:
  quit
  length <n>
  wordfile <filename>
  compare <guess> <answer>
  new
  list
  difficulty <easy|hard>

In play mode:
  guess <word>
  answer
  solve

In solve mode:
  guess <word> <signal>
  best [n]
  besth [n]
  score <word>
  play
"""


def signaltext(signal: list[int]) -> str:
    signaltext = "".join([signal_emoji[i] for i in signal])
    return signaltext


class REPLoop:
    def __init__(
        self,
        mode: Literal["solve", "play"] = "solve",
        difficulty: Literal["easy", "hard"] = "easy",
        length: int = None,
        wordfile: str | Path | None = None,
        solver: str = "default",
        autorun: bool = True,
    ):
        if mode not in ("solve", "play"):
            raise ValueError("Invalid mode")
        self.mode = mode
        if difficulty not in ("easy", "hard"):
            raise ValueError("Invalid difficulty")
        self.difficulty = difficulty
        self.length = length
        self.wordfile = wordfile
        self.solver = solversdict[solver]

        self.load_wordlist()

        if autorun:
            self.run()

    def load_wordlist(self):
        self.wordlist = loaders.load_wordlelist(self.length, self.wordfile)
        self.solve_session = self.solver(self.wordlist)
        self.play_session = core.PlaySession(self.wordlist, mode=self.difficulty)

    def new(self):
        if self.mode == "play":
            self.play_session.new()
        self.solve_session.reset()

    def eval(self):
        if len(self.tokens) == 0:
            self.msg = None
            return
        cmd = self.tokens[0]

        if cmd == "quit":
            self.quit = True
            self.msg = None
            return

        if cmd == "length":
            if len(self.tokens) < 2:
                self.msg = "Missing length"
                return
            try:
                self.length = int(self.tokens[1])
            except ValueError:
                self.msg = "Length should be an integer"
                return
            if self.length == 0:
                self.length = None

            self.msg = f"Length set to {self.length}. There are {len(self.wordlist)}\
words. Game reset."
            return

        if cmd == "wordfile":
            if len(self.tokens) < 2:
                self.msg = "Missing filename"
                return
            wordfile = self.tokens[1]
            if not Path(wordfile).is_file():
                self.msg = "File not found"
                return
            self.wordfile = wordfile
            try:
                self.load_wordlist()
            except ValueError as e:
                self.msg = str(e)
                return

            self.msg = f"Read words from {self.wordfile}. There are {len(self.wordlist)}\
words. Game reset."
            return

        if cmd == "new":
            self.new()
            self.msg = "Game reset"
            return

        if cmd == "guess":
            if len(self.tokens) < 2:
                self.msg = "Missing guess"
                return
            guess = self.tokens[1]
            if self.length is not None and len(guess) != self.length:
                self.msg = f"Guess should be {self.length} characters long"
                return
            if self.mode == "play":
                try:
                    signal = self.play_session.guess(guess)
                except ValueError:
                    self.msg = "Invalid guess"
                    return
                self.solve_session.add_clue(core.Clue(guess, signal))
                self.msg = f"{guess}: {signaltext(signal)}"
                return
            if self.mode == "solve":
                guess = self.tokens[1]
                try:
                    signal = [{"0": 0, "1": 1, "2": 2}[s] for s in self.tokens[2:]]
                except (ValueError, KeyError):
                    self.msg = "Invalid signal"
                    return
                if len(signal) != len(guess):
                    self.msg = "Signal has wrong length"
                    return
                self.solve_session.add_clue(core.Clue(guess, signal))
                self.msg = None
                return

        if cmd == "answer":
            if self.mode != "play":
                self.msg = f"Can use {cmd} only in play mode"
                return
            self.msg = self.play_session.answer()
            return

        if cmd == "best" or cmd == "besth":
            if self.mode == "play":
                self.msg = f"Cannot use {cmd} in play mode"
                return
            if len(self.tokens) >= 2:
                try:
                    n = int(self.tokens[1])
                except ValueError:
                    self.msg = "Invalid number"
                    return
            else:
                n = DEFAULT_LIST_SIZE
            if cmd == "best":
                best = self.solve_session.best(n)
            else:
                best = self.solve_session.besth(n)
            self.msg = "\n".join([f"{w} ({p:.2f})" for w, p in best])
            return

        if cmd == "compare":
            if len(self.tokens) != 3:
                self.msg = "Needs two words"
                return
            w1 = self.tokens[1].lower()
            w2 = self.tokens[2].lower()
            if not (w1.isalpha() and w2.isalpha()):
                self.msg = "Words must be alphabetic"
                return
            if len(w1) != len(w2):
                self.msg = "Words must be the same length"
                return
            self.msg = signaltext(compare(w1, w2))
            return

        if cmd == "list":
            wl = self.solve_session.list()
            if len(wl) == 0:
                self.msg = "No words in list"
                return
            if len(wl) > DEFAULT_LIST_SIZE:
                self.msg = f"Showing {DEFAULT_LIST_SIZE}/{len(wl)} random options.\n"
                wl = random.sample(wl, DEFAULT_LIST_SIZE)
                self.msg += "\n".join(wl)
                return
            self.msg = "\n".join(wl)
            return

        if cmd == "score":
            if self.mode == "play":
                self.msg = f"Cannot use {cmd} in play mode"
                return
            if len(self.tokens) < 2:
                self.msg = "score needs a word"
                return
            guess = self.tokens[1].lower()
            if not guess.isalpha():
                self.msg = "Word must be alphabetic"
                return
            if len(guess) != self.length:
                self.msg = f"Word must be the same length as the game {self.length}"
                return
            score = self.solve_session.score(guess)
            self.msg = f"{guess}: {score}"
            return

        if cmd == "solve":
            if self.mode == "solve":
                self.msg = "Already in solve mode"
                return
            self.mode = "solve"
            self.new()
            self.msg = "Switched to solve mode and game reset"
            return

        if cmd == "play":
            if self.mode == "play":
                self.msg = "Already in play mode"
                return
            self.mode = "play"
            self.new()
            self.msg = "Switched to play mode and game reset"
            return

        if cmd == "difficulty":
            if len(self.tokens) < 2:
                self.msg = "Missing difficulty"
                return
            difficulty = self.tokens[1]
            if difficulty not in ("easy", "hard"):
                self.msg = "Difficulty must be easy or hard"
                return
            self.difficulty = difficulty
            if self.mode == "play":
                self.play_session.difficulty = difficulty
            self.msg = f"Difficulty set to {self.difficulty}."
            return

        if cmd == "help":
            self.msg = help_text
            return
        self.msg = f"Unknown command {cmd}"

    def read(self):
        try:
            line = input("> ").strip()
        except EOFError:
            print()
            line = "quit"
        self.tokens = line.split(" ")

    def print(self):
        if self.msg is None:
            return
        print(self.msg)
        self.msg = None

    def run(self):
        self.quit = False
        try:
            while not self.quit:
                self.read()
                self.eval()
                self.print()
        except KeyboardInterrupt:
            print("\nDetected KeyboardInterrupt. Quitting.")
