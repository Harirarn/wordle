import numpy as np

from wordle import loaders, solvers
from wordle.analysis.benchmark import calc_average_score
from wordle.analysis.entval import calc_datatable, calc_turns_per_entropy

testwords = [
    "soare",
    "roate",
    "raise",
    "raile",
    "reast",
    "slate",
    "crate",
    "irate",
    "salet",
    "trace",
    "arise",
    "orate",
    "stare",
    "carte",
    "raine",
    "caret",
    "ariel",
    "snare",
    "arose",
    "taler",
    "carle",
    "slane",
    "artel",
    "strae",
    "carse",
    "saine",
    "earst",
    "least",
    "taser",
    "alert",
    "crane",
    "tares",
    "stale",
    "seral",
    "saner",
    "ratel",
    "torse",
    "tears",
    "alter",
    "resat",
    "later",
    "prate",
    "react",
    "trine",
    "saice",
    "toile",
    "earnt",
    "leant",
    "trade",
    "trone",
    "liane",
    "antre",
    "reist",
    "coate",
    "sorel",
    "urate",
    "slier",
    "teras",
    "learn",
    "stane",
    "trape",
    "peart",
    "rates",
    "paire",
    "cater",
    "roast",
    "stear",
    "setal",
    "stire",
    "aisle",
    "teals",
    "trice",
    "aline",
    "scare",
    "parse",
    "reals",
    "arles",
    "toise",
    "lares",
    "oater",
    "realo",
    "slart",
    "laser",
    "arets",
    "saute",
    "roset",
    "aesir",
    "tries",
    "parle",
    "heart",
    "rance",
    "alone",
    "litre",
    "tales",
    "store",
    "prase",
    "alien",
    "share",
    "grate",
    "ronte",
]


def main():
    solver = solvers.solversdict["entropy"]
    wordlist = loaders.load_wordlelist()
    pruner = solvers.PruningWordleList(wordlist)
    table = []
    for i, firstguess in enumerate(testwords):
        print(
            f"                    {firstguess}: {i+1} / {len(testwords)}",
            end="\r",
            flush=True,
        )
        data, _, _ = calc_average_score(
            wordlist,
            solver,
            False,
            firstguess=firstguess,
        )
        table.append(calc_turns_per_entropy(calc_datatable(data, pruner)))
    table = np.array(table)
    print(table.mean(axis=0))
    with open("tpe_easy.csv", "w") as f:
        for i, row in enumerate(table):
            f.write(f"{testwords[i]}")
            for j, col in enumerate(row):
                f.write(f",{col}")
            f.write("\n")


if __name__ == "__main__":
    main()
