class BIP():
    varx1 = [
        ["black", "\033[1;37;40m"],
        ["red", "\033[1;37;41m"],
        ["green", "\033[1;37;42m"],
        ["yellow", "\033[1;37;43m"],
        ["blue", "\033[1;37;44m"],
        ["purple", "\033[1;37;45m"],
        ["cyan", "\033[1;37;46m"],
        ["white", "\033[1;37;47m"]
    ]
    
    def __init__(self, *defx1):
        for forx1 in self.varx1:
            if forx1[0] == defx1[0]:
                print("{}{}\033[0m".format(forx1[1], " ".join(defx1[1:])))