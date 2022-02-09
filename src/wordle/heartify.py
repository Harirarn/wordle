from typing import Literal

INPUTS = {"⬛": 3, "🟨": 1, "🟩": 2, "⬜": 3}
OUTPUTS = {
    "square": {"dark": ["⬛", "🟨", "🟩"], "light": ["⬜", "🟨", "🟩"]},
    "heart": {"dark": ["🖤", "💛", "💚"], "light": ["🤍", "💛", "💚"]},
    "circle": {"dark": ["⚫", "🟡", "🟢"], "light": ["⚪", "🟡", "🟢"]},
    "queerdle": {"dark": ["🥥", "🍌", "🐍"], "light": ["🥥", "🍌", "🐍"]},
}
# 💚🖤💛🟢⚫🟡🤍⚪🥥🍌🐍


def heartify(
    text: str,
    theme: Literal["square", "heart", "circle", "queerdle"] = "heart",
    mode: Literal["dark", "light"] = "dark",
    black: str = None,
    yellow: str = None,
    green: str = None,
) -> str:
    """Changes the theme of wordle shares."""
    if black is None:
        black = OUTPUTS[theme][mode][0]
    if yellow is None:
        yellow = OUTPUTS[theme][mode][1]
    if green is None:
        green = OUTPUTS[theme][mode][2]
    OUT = {3: black, 1: yellow, 2: green}
    collect = [INPUTS.get(s, False) or s for s in text]
    return "".join(OUT.get(i, False) or i for i in collect)


# print(
#     heartify(
#         """
# Wordle 235 2/6

# 🟩⬛⬛🟨⬛
# 🟩🟩🟩🟩🟩
# """
#     )
# )
