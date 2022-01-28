import string
import math
N=5
wordlist = "Wordlelist.txt"

class wordl():
    def __init__(self, txt):
        #print(txt)
        self.type, self.word = txt.split()
        self.type = int(self.type)
        self.word = self.word.lower()
        self.weight = {3:10,2:1,1:3}[self.type]

    def __gt__(self, other):
        return self.word > other.word


with open(wordlist) as f:
    words = [wordl(i) for i in f.read().split('\n')]

pruned = words [:]


def compare(word, key, n=N):
    signal = [0]*n
    for i in range(n):
        if word[i] == key[i]: signal[i] = 2
    for letter in string.ascii_lowercase:
        if letter not in word or letter not in key: continue
        w = [(letter == l)-(letter == k) for l, k in zip(word, key)]
        s = w.count(-1)
        for i in range(n):
            if s == 0: break
            if w[i] > 0:
                signal[i] = 1
                s -= 1
    return signal

def prune(word, signal, wordlist):
    return [key for key in wordlist if compare(word, key.word) == signal]
            

def score(word, pruned):
    boxes = {}
    for key in pruned:
        signal = tuple(compare(word, key.word))
        boxes[signal] = boxes.setdefault(signal,0) + key.weight
    s1 = s2 = 0
    for n in boxes.values():
        s1 += n*n
        s2 += n*math.log(n)
    return (s1, s2)

help_text = """
This program helps in solving Wordle puzzles.
It stores a list of possible solutions and prunes it down as you enter guesses.
Available commands:
prune wordl 00120
    Prunes the word list if 'wordl' was entered as a guess and the signal was
    ⬛⬛🟨🟩⬛
    where 0 is grey signal, 1 is yellow signal and 2 is green signal.
new
    Repopulates the wordlist with all words.
list [c|f]
    Shows the current wordlist, or their count if it is too long.
    optional parameter c forces count and f forces list of all words.
best [n=20]
    lists the next best n words to guess.
besth
    same as best but only considers words which can succeed.
score wordl+
    Gives the scoring for the 'wordl's provided.
compare wordl answer
    Gives the signal if wordl is guessed and the answer is answer.
exit|quit|end
    exits.
"""

while True:
    com = input().split()
    if com[0] in ["exit","quit","end"]: break
    elif com[0] == "new": pruned = words[:]
    elif com[0] == "prune":
        word = com[1]
        signal = [int(n) for n in com[2]]
        pruned = prune(word, signal, pruned)
    elif com[0] == "list":
        if (len(pruned) > 40 or com[-1] == 'c') and com[-1] != 'f': print(f"There are {len(pruned)} words")
        else: print("\n".join(word.word for word in pruned))
    elif com[0] in ["best", "besth"]:
        scores = {word:score(word.word, pruned) for word in {"best":words,"besth":pruned}[com[0]]}
        ss = [(s[0], s[1], w.word) for w, s in scores.items()]
        ss.sort()
        if len(com) >= 2: upto = int(com[1])
        else: upto = 20
        for i in ss[:upto]: print(i)
    elif com[0] == "compare":
        print(''.join(str(n) for n in compare(com[1], com[2])))
    elif com[0] == "score":
        for word in com[1:]:
            print(f"{word}: {score(word, pruned)}")
    elif com[0] == "reverse":
        key = com[1]
        signal = [int(n) for n in com[2]]
        reverse_list = [word for word in pruned if compare(word, key)==signal]
        print("\n".join(reverse_list))
    elif com[0] == "help":
        print(help_text)



