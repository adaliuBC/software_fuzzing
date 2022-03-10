
from lib2to3.pytree import convert
from GrammarFuzzer import display_tree, all_terminals
from htmlGrammar import htmlGrammar
#from splitGrammar import *

from html.parser import HTMLParser
from bs4 import BeautifulSoup, CData

from Coverage import Coverage
import matplotlib.pyplot as plt
from GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from MutationFuzzer import MutationFuzzer
import random
from func_timeout import func_set_timeout
import func_timeout
import time, threading, signal, pdb


def myFunc():
    array = [
        1, 2, 3, 
        4, 5, 6,
        7, 8, 9
    ]
    for i in range(2):
        print(i, end = " ")

fileList = [
    "D:\\ada\\Master\\2022Winter\\Software Fuzzing\\software_fuzzing\\try.py", #"try.py"
    "D:\\ada\\Master\\2022Winter\\Software Fuzzing\\software_fuzzing\\try2.py"
]

if __name__ == '__main__':
    #myFunc()
    with Coverage(fileList) as cov:
        try:
            import try2
            myFunc()
            #myFunc2()

        except Exception as e:
            print(e)
            
    for line in cov.coverage():
        print(line)

    