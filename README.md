# wordle
This program helps in solving Wordle puzzles.
It stores a list of possible solutions and prunes it down as you enter guesses.
Available commands:

`prune wordl 00120`

    Prunes the word list if 'wordl' was entered as a guess and the signal was
    ⬛⬛🟨🟩⬛
    where 0 is grey signal, 1 is yellow signal and 2 is green signal.

`new`

    Repopulates the wordlist with all words.

`list [c|f]`

    Shows the current wordlist, or their count if it is too long.
    optional parameter c forces count and f forces list of all words.

`best [n=20]`

    lists the next best n words to guess.

`besth`

    same as best but only considers words which can succeed.

`score wordl+`

    Gives the scoring for the 'wordl's provided.

`compare wordl answer`

    Gives the signal if wordl is guessed and the answer is answer.

`exit|quit|end`

    Exits.
