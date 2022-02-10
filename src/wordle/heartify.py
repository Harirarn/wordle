from typing import Final, Literal, TypeAlias
import pyperclip

ColorMode: TypeAlias = Literal["dark", "light", "darkcb", "lightcb"]
ShapeTheme: TypeAlias = Literal["square", "heart", "circle", "queerdle", "flower"]

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
        "darkcb": ("🎱", "🍑", "💦"),
        "lightcb": ("🥥", "🍑", "💦"),
    },
    "flower": {
        "dark": ("💮", "🌸", "🏵️"),
        "light": ("🌼", "🌻", "🌹"),
        "darkcb": ("🥀", "🌷", "💐"),
        "lightcb": ("🌼", "💠", "🌺"),
    },
}
# 💚🖤💛🟢⚫🟡🤍⚪🥥🍌🐍🎱💧💦🍑

DEFAULT_THEME: Final = "heart"
DEFAULT_MODE: Final = "dark"


def heartify(
    text: str,
    theme: ShapeTheme = DEFAULT_THEME,
    mode: ColorMode = DEFAULT_MODE,
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


if __name__ == "__main__":
    from argparse import ArgumentParser

    def main() -> None:
        parser = ArgumentParser(
            description="Changes the theme of wordle shares."
            "Paste the share into the clipboard and run the script."
        )
        parser.add_argument(
            "-t",
            "--theme",
            choices=OUTPUTS.keys(),
            default=DEFAULT_THEME,
            help=" Theme to use. Default:  %(default)s",
        )
        parser.add_argument(
            "-m",
            "--mode",
            choices=OUTPUTS[DEFAULT_THEME].keys(),
            default=DEFAULT_MODE,
            help=" Dark / Light + ? Colour-blind. Default:  %(default)s",
        )
        parser.add_argument("-b", "--black", type=str, default=None)
        parser.add_argument("-y", "--yellow", type=str, default=None)
        parser.add_argument("-g", "--green", type=str, default=None)
        args = parser.parse_args()

        text = pyperclip.paste()

        out = heartify(text, args.theme, args.mode, args.black, args.yellow, args.green)

        print(out)
        pyperclip.copy(out)

    main()
