from wordle import loaders
from wordle.core import PlaySession
from wordle.wordle import Clue


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
