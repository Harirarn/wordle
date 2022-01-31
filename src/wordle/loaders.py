import importlib.resources as pkg_resources
import re
from pathlib import Path

from wordle.wordle import WordleList

PACKAGE = "wordle"
RESOURSES = f"{PACKAGE}.resources"
WORDLISTS = {
    "official": {
        "alls": "official_wordle_all.txt",
        "commons": "official_wordle_common.txt",
    },
    "custom": {
        "alls": "sowpods.txt",
        "commons": "bnccoca10000-grouped.txt",
    },
}


def load_wordlelist(length: int | None = 5, filename: str = None) -> WordleList:
    if length == 5 and filename is None:
        wordlist = load_resource("official")
    elif filename is None:
        wordlist = load_resource("custom")
    else:
        wordlist = load_file(filename)
    return WordleList(filter_length(wordlist, length))


def load_file(filename: str | Path) -> list[tuple[str, int]]:
    data = open(filename).read().split("\n")
    if re.match(r"^\w+$", data[0]):
        wordlist = [(word, 1) for word in data if word.isalpha()]
    elif re.match(r"^\w+ \d+$", data[0]):
        wordlist = [
            (word.split(" ")[0], int(word.split(" ")[1]))
            for word in data
            if word[0].isalpha()
        ]
    elif re.match(r"^\d+ \w+$", data[0]):
        wordlist = [
            (word.split(" ")[1], int(word.split(" ")[0]))
            for word in data
            if word[0].isalpha()
        ]
    else:
        raise ValueError("Invalid file format")
    return wordlist


def load_resource(source: str) -> list[tuple[str, int]]:
    if source not in ("official", "custom"):
        raise ValueError("Invalid source")
    alls = pkg_resources.read_text(RESOURSES, WORDLISTS[source]["alls"]).split("\n")
    commons = pkg_resources.read_text(RESOURSES, WORDLISTS[source]["commons"]).split(
        "\n"
    )
    commonset = set(commons)
    commonset.remove("")
    allset = set(alls) - commonset
    allset.remove("")
    return [(word, 0) for word in allset] + [(word, 1) for word in commonset]


def filter_length(
    wordlist: list[tuple[str, int]] | list[str], length: int | None
) -> list[tuple[str, int]] | list[str]:
    if length is None:
        return wordlist
    if isinstance(wordlist[0], str):
        return [word for word in wordlist if len(word) == length]  # type: ignore
    return [word for word in wordlist if len(word[0]) == length]  # type: ignore


def prune_non_alphabetic(wordlist: list[str]) -> list[str]:
    return [word for word in wordlist if word.isalpha()]