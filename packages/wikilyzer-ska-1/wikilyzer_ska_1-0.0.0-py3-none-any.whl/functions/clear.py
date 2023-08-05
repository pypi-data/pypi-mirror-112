from functions.banner import banner
from sys import platform
from os import system

def clear(*defx1):
    if platform == "win32":
        system("cls")
    
    else:
        system("clear")
        
    banner(defx1[0])