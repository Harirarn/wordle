from typing import Literal, TypeAlias

ColorMode: TypeAlias = Literal["dark", "light", "darkcb", "lightcb"]
ShapeTheme: TypeAlias = Literal["square", "heart", "circle", "queerdle"]

INPUTS: dict[str, Literal[1, 2, 3]] = {"⬛": 3, "⬜": 3, "🟨": 1, "🟦": 1, "🟩": 2, "🟧": 2}
OUTPUTS: dict[ShapeTheme, dict[ColorMode, tuple[str, str, str]]] = {
    "square": {
        "dark": ("⬛", "🟨", "🟩"),
        "light": ("⬜", "🟨", "🟩"),
        "darkcb": ("⬛", "🟦", "🟧"),
        "lightcb": ("⬜", "🟦", "🟧"),
    },
    "heart": {
        "dark": ("🖤", "💛", "💚"),
        "light": ("🤍", "💛", "💚"),
        "darkcb": ("🖤", "💙", "🧡"),
        "lightcb": ("🤍", "💙", "🧡"),
    },
    "circle": {
        "dark": ("⚫", "🟡", "🟢"),
        "light": ("⚪", "🟡", "🟢"),
        "darkcb": ("⚫", "🔵", "🟠"),
        "lightcb": ("⚪", "🔵", "🟠"),
    },
    "queerdle": {
        "dark": ("🎱", "🍌", "🐍"),
        "light": ("🥥", "🍌", "🐍"),
        "darkcb": ("🎱", "💧", "🍊"),
        "lightcb": ("🥥", "💧", "🍊"),
    },
}
# 💚🖤💛🟢⚫🟡🤍⚪🥥🍌🐍


def heartify(
    text: str,
    theme: ShapeTheme = "heart",
    mode: ColorMode = "dark",
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
    collect = (INPUTS.get(s, False) or s for s in text)  # type: ignore
    return "".join(OUT.get(i, False) or i for i in collect)  # type: ignore


# print(
#     heartify(
#         """
# Wordle 235 2/6

# 🟩⬛⬛🟨⬛
# 🟩🟩🟩🟩🟩
# """
#     )
# )
