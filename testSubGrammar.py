
from GrammarFuzzer import display_tree, all_terminals
from scssGrammar import SCSS_GRAMMAR
from splitGrammar import *
from scss import Compiler
from Coverage import Coverage
from fileList import fileList
import matplotlib.pyplot as plt
from GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from MutationFuzzer import MutationFuzzer
import random
from func_timeout import func_set_timeout
import func_timeout
import time, threading, signal
# 试试不同的fuzzer

# seed_input = "http://www.google.com/search?q=fuzzing"
# mutation_fuzzer = MutationFuzzer(seed=[seed_input])
# print([mutation_fuzzer.fuzz() for i in range(10)])

if __name__ == '__main__':
    # cnt the total line num that is provided by Pyscss
    random.seed(42)
    print(useGrammar)
    grammarFuzzer = GeneratorGrammarFuzzer(useGrammar, min_nonterminals=10, max_nonterminals=30, log = False)
    grammarFuzzer.check_grammar()
    grammarFuzzer.compute_cost()
    trial = 20


    def fuzzing(scssText):
        cssText = Compiler().compile_string(scssText)
        print("Generated css code:\n", cssText)


    coveredLines = set()
    xList = []
    yList = []
    for i in range(trial):
        grammarFuzzer.fuzz()
        scssText = all_terminals(grammarFuzzer.derivation_tree)

        print("----", scssText)
        with Coverage() as cov:
            try:
                thread = threading.Thread(
                    target = fuzzing, args = (scssText, )
                )
                thread.daemon = True
                thread.start()
                thread.join(5)
                #cssText = Compiler().compile_string(scssText)
                pass
            except Exception as e:
                print(e)
                #pass
        # print("Covered percentage single:\n", len(cov.coverage())/cntLines)
        
        coveredLines = cov.coverage()
        xList.append(i)
        yList.append(len(coveredLines))
        #print(len(coveredLines), cntLines)
        print(f"----{i}th trial cover {len(coveredLines)}lines.")
    plt.plot(xList, yList)  # add label
    plt.xlabel("Trial")
    plt.ylabel("Covered Lines")
    plt.show()

    #print(len(coveredLines))
    
    #plt.plot(fileList, file2coveredLineNumOrdered)
    #plt.show()
    