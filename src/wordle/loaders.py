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
    wordlist = filter_length(wordlist, length)
    wordlist = dedup(wordlist)
    return WordleList(wordlist)


def load_file(filename: str | Path) -> list[tuple[str, int]]:
    data = open(filename).read().split("\n")
    if re.match(r"^\w+$", data[0]):
        wordlist = [(word, 1) for word in data if word.isalpha()]
    elif re.match(r"^\w+ \d+$", data[0]):
        wordlist = [
            (word.split(" ")[0], int(word.split(" ")[1]))
            for word in data
            if word != "" and word.split(" ")[0].isalpha()
        ]
    elif re.match(r"^\d+ \w+$", data[0]):
        wordlist = [
            (word.split(" ")[1], int(word.split(" ")[0]))
            for word in data
            if word != "" and word.split(" ")[1].isalpha()
        ]
        pass
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
    return [(word, 0) for word in alls] + [(word, 1) for word in commons]


def filter_length(
    wordlist: list[tuple[str, int]], length: int | None
) -> list[tuple[str, int]]:
    if length is None:
        return wordlist
    return [word for word in wordlist if len(word[0]) == length]


def dedup(wl: list[tuple[str, int]]) -> list[tuple[str, int]]:
    wldict: dict[str, int] = {}
    for word, weight in wl:
        if word in wldict:
            wldict[word] += weight
        else:
            wldict[word] = weight
    return [(word, weight) for word, weight in wldict.items()]
