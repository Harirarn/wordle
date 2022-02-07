# wordle
This program helps in solving Wordle puzzles.
It stores a list of possible solutions and prunes it down as you enter guesses.

To install

`python -m pip install -e .`

To run, either execute

`python -m wordle`

or from inside a python interpreter

```
>>> from wordle import cli
>>> cli.main()
```


Available commands:

`guess wordl 00120`

    Prunes the word list if 'wordl' was entered as a guess and the signal was
    ⬛⬛🟨🟩⬛
    where 0 is grey signal, 1 is yellow signal and 2 is green signal.

`new`

    Repopulates the wordlist with all words.

`list`

    Shows the current wordlist, or their count if it is too long.

`best [n=20]`

    lists the next best n words to guess.

`besth [n=20]`

    same as best but only considers words which can succeed.

`score wordl+`

    Gives the scoring for the 'wordl's provided. Lower is better.

`compare wordl answer`

    Gives the signal if wordl is guessed and the answer is answer.

`quit`

    Exits.
