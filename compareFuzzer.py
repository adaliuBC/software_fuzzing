
from GrammarFuzzer import display_tree, all_terminals
from scssGrammar import SCSS_GRAMMAR
from splitGrammar import RULESET_GRAMMAR
from scss import Compiler
from Coverage import Coverage
from fileList import fileList
import matplotlib.pyplot as plt
from GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from MutationFuzzer import MutationFuzzer
# 试试不同的fuzzer

if __name__ == '__main__':
    # cnt the total line num that is provided by Pyscss
    cntLines = 0
    for file in fileList:
        cntLine = len(open(file,'rb').readlines())
        cntLines += cntLine
    print("cntLines:", cntLines)

    fuzzerList = []  # list of fuzzer

    with open("example.txt", "rb") as f:
        seed = f.read()
    mutationFuzzer = MutationFuzzer([seed])
    with Coverage() as cov:
        cssText = Compiler().compile_string(seed)
    # print("Covered percentage single:\n", len(cov.coverage())/cntLines)
    # print("generated css code:\n", cssText)
    print(len(cov.coverage())/cntLines)
    fuzzerList.append(mutationFuzzer)

    grammarFuzzer = GeneratorGrammarFuzzer(RULESET_GRAMMAR, min_nonterminals=3, max_nonterminals=50, log = False)
    grammarFuzzer.check_grammar()
    grammarFuzzer.compute_cost()
    fuzzerList.append(grammarFuzzer)
    trial = 50
    coveragePercentageAll = 0.
    coveredLines = set()
    xList = []
    yList = []
    for i in range(trial):
        grammarFuzzer.fuzz()
        #treeFig = display_tree(f.derivation_tree)
        #treeFig.render(directory="./output/", filename="scss_grammar_tree", view=True)
        scssText = all_terminals(grammarFuzzer.derivation_tree)
        # print("\ngenerated scss code:\n", scssText)
        
        with Coverage() as cov:
            cssText = Compiler().compile_string(scssText)
        # print("Covered percentage single:\n", len(cov.coverage())/cntLines)
        # print("generated css code:\n", cssText)
        coveredLines = coveredLines | cov.coverage()
        xList.append(i)
        yList.append(len(coveredLines)/cntLines)
    plt.plot(xList, yList)
    plt.show()

    print(coveredLines)
    
    #plt.plot(fileList, file2coveredLineNumOrdered)
    #plt.show()