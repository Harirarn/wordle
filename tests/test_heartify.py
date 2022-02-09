import pytest

from wordle.heartify import heartify


@pytest.mark.parametrize(
    "text, theme, mode, black, yellow, green, expected",
    [
        (
            """Wordle 235 2/6

🟩⬛⬛🟨⬛
🟩🟩🟩🟩🟩
""",
            "heart",
            "dark",
            None,
            None,
            None,
            """Wordle 235 2/6

💚🖤🖤💛🖤
💚💚💚💚💚
""",
        ),
    ],
)
def test_heartify(text, theme, mode, black, yellow, green, expected):
    assert heartify(text, theme, mode, black, yellow, green) == expected
