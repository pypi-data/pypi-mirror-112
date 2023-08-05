from prompt_toolkit import prompt
from functions.clear import clear
from functions.csf import csf
from classes.uc import UC
from posix import listdir

def main():
    csf()
    clear("assets/W")
    while True:
        try:
            UC(prompt("wikilyzer ⇛> "))
            
        except KeyboardInterrupt:
            pass
            
if __name__ == "__main__":
    main()
    