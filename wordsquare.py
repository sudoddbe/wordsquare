import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import io
import os

from random import shuffle

from collections import OrderedDict


def read_wordlist():
    f = io.open("ss100.txt", encoding="iso-8859-1")
    wordlist = [l.rstrip() for l in f]

    rules = [lambda s: not any(x.isupper() for x in s),
             lambda s: not "aa" in s,
             lambda s: not "-" in s,
             ]

    wordlist = [word for word in wordlist if all(rule(word) for rule in rules)]
    f.close()

    wordlist = list(OrderedDict.fromkeys(wordlist))

    return wordlist

def get_sublist(wordlist, length=6):
    sublist = [word for word in wordlist if len(word) == length]
    return sublist

def test_condition(puzzle, sublist, nbr_rows):
    tmp_puzzle = puzzle[0:nbr_rows]
    for row in tmp_puzzle.T:
        cond = [np.all(row == np.array(list(word[0:nbr_rows]), dtype="<U1")) for word in sublist]
        if not np.any(cond):
            return False
    return True

def build_puzzle(puzzle, sublist, puzzle_size, index_list, current_row = 0):

    if current_row >= puzzle_size:
        print "Success"
        print_puzzle(puzzle)
        return True

    for i in range(index_list[current_row], len(sublist)):
        if current_row == 0:
            print i
            print sublist[i]
        puzzle[current_row] = np.array(list(sublist[i]))
        print_puzzle(puzzle)
        index_list[current_row] = i
        index_list[current_row::] = 0
        if test_condition(puzzle, sublist, current_row +1):
            retval = build_puzzle(puzzle, sublist, puzzle_size, index_list, current_row + 1)
            if retval:
                print "Success"
                print_puzzle(puzzle)
                return True
    return False

def print_puzzle(puzzle):
    os.system("clear")
    h =""
    h = h.join(["--" for row in puzzle])
    for row in puzzle:
        print h
        tmp =""
        tmp = tmp.join([c+"|" for c in row])
        print tmp
    print h

if __name__=="__main__":
    wordlist = read_wordlist()
    print len(wordlist)
    puzzle_size = 4
    sublist= get_sublist(wordlist, puzzle_size)
    shuffle(sublist)
    print len(sublist)
    puzzle = np.zeros((puzzle_size, puzzle_size), dtype="<U1")
    index_list = np.zeros(puzzle_size, dtype="int")

    #sublist = ["dab", "abc", "aaa", "bbb", "ccc"]
    build_puzzle(puzzle, sublist, puzzle_size, index_list)
