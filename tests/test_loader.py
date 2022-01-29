from wordle.loaders import load_wordlelist as load


def test_default():
    wl = load()
    assert len(wl) == 12972
    assert len([word for word in wl if word.weight == 1]) == 2315


def test_custom():
    wl = load(4)
    assert len(wl) == 5461
    assert len([word for word in wl if word.weight == 1]) == 1318


def test_file():
    wl = load(length=None, filename="tests/ef3000.txt")
    assert len(wl) == 3000
    assert all([word.weight == 1 for word in wl])
