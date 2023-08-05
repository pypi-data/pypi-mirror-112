from os import mkdir, path
from functions import sto 

def csf():
    for forx1 in sto.folders:
        if not path.exists(forx1):
            mkdir(forx1)