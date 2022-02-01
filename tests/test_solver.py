from typing import Type

import pytest
from wordle import core, loaders, solvers


@pytest.mark.parametrize(
    "solver",
    [
        solvers.StatisticalSolver,
    ],
)
def test_solver(solver: Type[core.WordleSolver]):
    wl = loaders.load_wordlelist(filename="tests/testwl.txt")
    ans = "antic"

    ps = core.PlaySession(wl, ans=ans)
    s = solver(wl)

    signal = [0, 0, 0, 0, 0]

    print(f"\nSolving for {ans} in easy mode.")
    while signal != [2, 2, 2, 2, 2]:
        guess = s.best(1)[0][0]
        signal = ps.guess(guess)
        print(f"{guess} {signal}")
        s.add_clue(signal)

    ans = "onion"

    ps.mode = "hard"
    ps.new(ans)
    s.reset()

    signal = [0, 0, 0, 0, 0]

    print(f"\nSolving for {ans} in hard mode.")
    while signal != [2, 2, 2, 2, 2]:
        guess = s.besth(1)[0][0]
        signal = ps.guess(guess)
        print(f"{guess} {signal}")
        s.add_clue(signal)


@pytest.mark.parametrize(
    "solver",
    [
        solvers.StatisticalSolver,
    ],
)
def test_solver_list(solver: Type[core.WordleSolver]):
    wl = loaders.load_wordlelist()
    s = solver(wl)

    s.add_clue(core.Clue("raise", [0, 1, 0, 0, 2]))

    assert set(s.list()) == {
        "plate",
        "elate",
        "blade",
        "glade",
        "alone",
        "angle",
        "amble",
        "plane",
        "algae",
        "ankle",
        "blame",
        "ample",
        "glaze",
        "blaze",
        "flake",
        "place",
        "leave",
        "flame",
        "apple",
        "above",
        "whale",
        "abate",
        "abode",
        "adobe",
        "anode",
        "atone",
        "agape",
        "knave",
        "agate",
        "evade",
        "ovate",
        "awoke",
        "adage",
        "peace",
        "awake",
        "weave",
        "amaze",
        "heave",
        "acute",
        "chafe",
        "quake",
    }

    s.add_clue(core.Clue("plate", [0, 0, 2, 0, 2]))

    assert set(s.list()) == {
        "weave",
        "quake",
        "knave",
        "heave",
        "evade",
        "chafe",
        "awake",
        "amaze",
        "adage",
    }
