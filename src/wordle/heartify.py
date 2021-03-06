from typing import Final, Literal, TypeAlias

import pyperclip

ColorMode: TypeAlias = Literal["dark", "light", "darkcb", "lightcb"]
ShapeTheme: TypeAlias = Literal["square", "heart", "circle", "queerdle", "flower"]

INPUTS: dict[str, Literal[1, 2, 3]] = {"โฌ": 3, "โฌ": 3, "๐จ": 1, "๐ฆ": 1, "๐ฉ": 2, "๐ง": 2}
OUTPUTS: dict[ShapeTheme, dict[ColorMode, tuple[str, str, str]]] = {
    "square": {
        "dark": ("โฌ", "๐จ", "๐ฉ"),
        "light": ("โฌ", "๐จ", "๐ฉ"),
        "darkcb": ("โฌ", "๐ฆ", "๐ง"),
        "lightcb": ("โฌ", "๐ฆ", "๐ง"),
    },
    "heart": {
        "dark": ("๐ค", "๐", "๐"),
        "light": ("๐ค", "๐", "๐"),
        "darkcb": ("๐ค", "๐", "๐งก"),
        "lightcb": ("๐ค", "๐", "๐งก"),
    },
    "circle": {
        "dark": ("โซ", "๐ก", "๐ข"),
        "light": ("โช", "๐ก", "๐ข"),
        "darkcb": ("โซ", "๐ต", "๐ "),
        "lightcb": ("โช", "๐ต", "๐ "),
    },
    "queerdle": {
        "dark": ("๐ฑ", "๐", "๐"),
        "light": ("๐ฅฅ", "๐", "๐"),
        "darkcb": ("๐ฑ", "๐", "๐ฆ"),
        "lightcb": ("๐ฅฅ", "๐", "๐ฆ"),
    },
    "flower": {
        "dark": ("๐ฎ", "๐ธ", "๐ต๏ธ"),
        "light": ("๐ผ", "๐ป", "๐น"),
        "darkcb": ("๐ฅ", "๐ท", "๐"),
        "lightcb": ("๐ผ", "๐ ", "๐บ"),
    },
}
# ๐๐ค๐๐ขโซ๐ก๐คโช๐ฅฅ๐๐๐ฑ๐ง๐ฆ๐

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
