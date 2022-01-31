import pytest

import wordle.wordle as wordle


@pytest.mark.parametrize(
    "word, key, expected",
    [
        ("mopey", "favor", [0, 1, 0, 0, 0]),
        ("sagol", "tiger", [0, 0, 2, 0, 0]),
        ("fleet", "tiger", [0, 0, 0, 2, 1]),
        ("abear", "abbey", [2, 2, 1, 0, 0]),
        ("abdeb", "abbey", [2, 2, 0, 2, 1]),
        ("wordle", "word", ValueError),
        ("word", "wordle", ValueError),
    ],
)
def test_compare(word, key, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            wordle.compare(word, key)
    else:
        assert wordle.compare(word, key) == expected
