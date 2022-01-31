from wordle.loaders import load_wordlelist as load


def test_default():
    wl = load()
    assert len(wl) == 12972
    assert len([word for word in wl if word.weight == 1]) == 2315


def test_custom():
    wl = load(4)
    assert len(wl) == 5461
    assert len([word for word in wl if word.weight == 1]) == 1318


def test_file_1():
    wl = load(length=None, filename="tests/ef3000.txt")
    assert len(wl) == 2994
    assert all([word.weight == 1 for word in wl])


def test_filt_2():
    wl = load(length=5, filename="tests/testwl.txt")
    assert len(wl) == 1099
