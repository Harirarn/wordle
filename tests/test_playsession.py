import pytest
from wordle import loaders
from wordle.core import HardModeInvalid, PlaySession
from wordle.wordle import Clue, Wordle


def test_playsession():
    wl = loaders.load_wordlelist(filename="tests/ef3000.txt")
    ps = PlaySession(wl)
    ans = ps.answer()
    assert ans in wl.words
    guess = wl[42].word
    assert ps.guess(guess) == Clue.from_compare(guess, ans)
    assert ps.tries == 1
    ps.new()
    assert ps.tries == 0
    assert ps.answer() in wl.words


def test_playsession_hard():
    wl = loaders.load_wordlelist(filename="tests/ef3000.txt")
    ans = "white"
    ps = PlaySession(wl, mode="hard", ans=ans)

    assert ans in wl.words
    assert ps.answer() == ans

    guess = Wordle("ahead")
    assert ps.guess(guess) == Clue(guess, [0, 2, 1, 0, 0])

    with pytest.raises(HardModeInvalid) as e:
        ps.guess("bread")
    assert e.value.args[1] == {"h"}

    with pytest.raises(ValueError):
        ps.new("fails")
