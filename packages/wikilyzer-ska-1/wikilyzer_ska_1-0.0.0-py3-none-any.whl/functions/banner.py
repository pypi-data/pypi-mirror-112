from os import get_terminal_size
from classes.bip import BIP

def banner(*defx1):
    varx1 = get_terminal_size().columns

    if not varx1 % 2 == 0:
        varx1 = get_terminal_size().columns - 1

    for forx1 in range(0, len(open(defx1[0], "r").read().split("\n"))):
        BIP("black", "{0}{1}{0}".format("█" * (int(varx1 / 2) - int(len(open(defx1[0], "r").read().split("\n")[forx1]) / 2)), open(defx1[0], "r").read().split("\n")[forx1]))
