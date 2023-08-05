from functions.clear import clear
from functions.sto import folders
from datetime import datetime
from functions.req import req
from tabulate import tabulate
from classes.bip import BIP
from os import path, remove
from posix import listdir
from sys import stdout
import shlex

class UC():
    def __init__(self, *defx1):
        self.medx1 = defx1[0]
        self.medx2 = shlex.split(self.medx1)
        self.medx3 = "https://{}.wikipedia.com/w/api.php"
        self.defx1()
        
    def defx1(self):
        stdout.write("\033[F")
        stdout.write("\033[K")
        if not len(self.medx1.replace(" ", "")) == 0:                
            if self.medx2[0] == "rapor":
                self.rapor(0, self.medx2[1:])
            elif self.medx2[0] == "sistem":
                self.sistem(0, self.medx2[1:])
    
    def rapor(self, *defx1):
        if defx1[0] == 0:
            if len(defx1[1]) >= 3:
                if defx1[1][0] == "iste":
                    varx1 = {"action": "query", "prop": "revisions", "rvlimit": "500", "titles": "{}".format(defx1[1][len(defx1[1]) - 1]), "format": "json"}
                    varx2 = req(self.medx3.format(defx1[1][len(defx1[1]) - 2]), varx1)
                    varx3 = []
                    
                    if not varx1 == None:
                        for forx1 in varx2["query"]["pages"]:
                            if not forx1 == -1:
                                for forx2 in varx2["query"]["pages"][forx1]["revisions"]:
                                    varx4 = forx2["timestamp"].split("T")[0]
                                    varx5 = forx2["timestamp"].split("T")[1].split("Z")[0]
                                    
                                    if len(forx2["comment"]) >= 100:
                                        varx3.append(["\033[1;37;44m{}\033[0m".format(varx2["query"]["pages"][forx1]["title"]), "\033[1;37;45m{}\033[0m".format(varx4), "\033[1;37;45m{}\033[0m".format(varx5), "\033[1;37;41m{}\033[0m".format(forx2["user"]), forx2["comment"][:100] + "......"])
                                    else:
                                        varx3.append(["\033[1;37;44m{}\033[0m".format(varx2["query"]["pages"][forx1]["title"]), "\033[1;37;45m{}\033[0m".format(varx4), "\033[1;37;45m{}\033[0m".format(varx5), "\033[1;37;41m{}\033[0m".format(forx2["user"]), forx2["comment"]])
                                    
                        print(tabulate(varx3, headers=["Ad", "Tarih", "Zaman", "Kullanıcı", "Yorum"], tablefmt="fancy_grid", stralign="center"))
                        
                        for forx1 in defx1[1][1:len(defx1[1]) - 2]:
                            if forx1[0] == "-":
                                if forx1[1:] == "yazdır":
                                    if path.exists(path.join(folders[2], datetime.now().strftime("%A_%d-%m-%Y_%X"))):
                                        remove(path.join(folders[2], datetime.now().strftime("%A_%d-%m-%Y_%X")))
                                    createx1 = open(path.join(folders[2], datetime.now().strftime("%A_%d-%m-%Y_%X")), "x")
                                    with open(path.join(folders[2], datetime.now().strftime("%A_%d-%m-%Y_%X")), "w") as withx1:
                                        withx1.write(tabulate(varx3, headers=["Ad", "Tarih", "Zaman", "Kullanıcı", "Yorum"], tablefmt="fancy_grid"))
            
            elif len(defx1[1]) >= 2:
                if defx1[1][0] == "oku":
                    for forx1 in defx1[1][1:]:
                        if path.exists(path.join(folders[2], forx1)):
                            print(open(path.join(folders[2], forx1), "r").read())
                    
            elif len(defx1[1]) == 1:
                if defx1[1][0] == "listele":
                    if path.exists(folders[2]):
                        varx1 = []
                        for forx1 in listdir(folders[2]):
                            varx1.append(["\033[1;37;44m{}\033[0m".format(forx1)])
                        
                        print(tabulate(varx1, headers=["Ad"], tablefmt="fancy_grid"))  
    def sistem(self, *defx1):
        if defx1[0] == 0:
            if len(defx1[1]) == 1:
                if defx1[1][0] == "temizle":
                    clear("assets/W")
                    
                elif defx1[1][0] == "çık":
                    clear("assets/W")
                    exit(0)