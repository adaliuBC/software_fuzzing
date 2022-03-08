
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
import time, threading, signal, pdb
# 试试不同的fuzzer

# seed_input = "http://www.google.com/search?q=fuzzing"
# mutation_fuzzer = MutationFuzzer(seed=[seed_input])
# print([mutation_fuzzer.fuzz() for i in range(10)])

def simplifyFname(fname):
    ind = fname.index("\\scss\\")
    return fname[ind+6:]

file2lines = {}
if __name__ == '__main__':
    # cnt the total line num that is provided by Pyscss
    # 计算总行数，benchmark（删除注释）
    random.seed(42)
    global cntLines
    cntLines = 0
    for file in fileList:
        cntLine = 0
        with open(file, "rb") as f:
            isComment = False
            multiCommentwith = ""
            lines = f.readlines()
            for line in lines:
                line = line.decode(encoding="utf-8")
                if isComment:
                    if (3*multiCommentwith) in line:
                        isComment = False
                        multiCommentwith = ""
                else:  # not in multi comment
                    if "\""*3 in line:
                        isComment = True
                        multiCommentwith = "\""
                    elif "\'"*3 in line:
                        isComment = True
                        multiCommentwith = "\'"
                    else:
                        if line.lstrip().startswith("#"):
                            continue
                        else:
                            cntLine += 1
                
        #cntLine = len(open(file,'rb').readlines())
        cntLines += cntLine
        print(file, cntLine)
        file2lines[file] = cntLine
    print("cntLines:", cntLines)
    
    # build fuzzer list, prepare for test
    fuzzerList = []  # list of fuzzer

    from Fuzzer import RandomFuzzer
    randomFuzzer = RandomFuzzer(min_length=20, max_length=40)
    #fuzzerList.append(randomFuzzer)  # open & close this fuzzer

    with open("example.txt", "rb") as f:
        seed = f.read()
    seed = seed.decode(encoding='utf-8')
    mutationFuzzer = MutationFuzzer([seed])
    cssText = Compiler().compile_string(seed)
    print(cssText)
    # with Coverage() as cov:
    #     cssText = Compiler().compile_string(seed)
    # # print("Covered percentage single:\n", len(cov.coverage())/cntLines)
    # # print("generated css code:\n", cssText)
    # print(le  n(cov.coverage())/cntLines)
    #fuzzerList.append(mutationFuzzer)  # open & close this fuzzer

    grammarFuzzer = GeneratorGrammarFuzzer(useGrammar, min_nonterminals=10, max_nonterminals=30, log = False)
    grammarFuzzer.check_grammar()
    grammarFuzzer.compute_cost()
    fuzzerList.append(grammarFuzzer)
    
    fuzzerNameList = ["Grammar Fuzzer"]#["Random Fuzzer", "Mutation Fuzzer", "Grammar Fuzzer"]
    trial = 200

    deadInput = []

    def fuzzing(scssText):
        cssText = Compiler().compile_string(scssText)
        #print("Generated css code:\n", cssText)

    for i in range(len(fuzzerList)):
        fuzzer = fuzzerList[i]
        fuzzerName = fuzzerNameList[i]
        coveragePercentageAll = 0.
        coveredLines = set()
        xList = []
        yList = []
        for i in range(trial):
            if fuzzerName == "Mutation Fuzzer" or "Random Fuzzer":
                scssText = fuzzer.fuzz()
            elif fuzzerName == "Grammar Fuzzer":
                fuzzer.fuzz()
                scssText = all_terminals(fuzzer.derivation_tree)

            #print("\ngenerated scss code:\n", scssText)
            print("GeneratedscssText, start compiling ... ")
            with Coverage() as cov:
                try:
                    thread = threading.Thread(
                        target = fuzzing, args = (scssText, )
                    )
                    thread.daemon = True
                    thread.start()
                    thread.join(5)
                    #cssText = Compiler().compile_string(scssText)
                except Exception as e:
                    print(e)
                    # pass
            # print("Covered percentage single:\n", len(cov.coverage())/cntLines)
            print("Compile finiashed, start computing ... ")
            
            coveredLines = coveredLines | cov.coverage()
            xList.append(i)
            coverPercent = len(coveredLines)/cntLines
            yList.append(coverPercent)
            #print(len(coveredLines), cntLines)
            print(f"{fuzzerName} {i}th trial cover percent:", coverPercent)
        plt.plot(xList, yList)  # add label
        plt.xlabel("Trial")
        plt.ylabel("Covered proportion")
        plt.title(fuzzerName)
        plt.show()

        # get coveredLines, 计算每个文件hit了多少次
        filename2cnt = {}
        linelist = list(coveredLines)
        linelist.sort(key = lambda x: (x[2], x[1]))
        # for line in linelist:
        #     print(line)
        for line in coveredLines:
            #pdb.set_trace()
            funcname, _, filename = line
            #filename = simplifyFname(filename)
            if filename not in filename2cnt.keys():
                filename2cnt[filename] = 1
            else:
                filename2cnt[filename] += 1
        for file, cnt in filename2cnt.items():
            print(f"{file}: {cnt}/{file2lines[file]}, {cnt/file2lines[file]}")

        # print(filename2cnt)
        # 画图
        fnameList = []
        cntList = []
        for fname, cnt in filename2cnt.items():
            fnameList.append(fname)
            cntList.append(cnt)
        # 柱状图
        #plt.
        #plt.show()
    
    #plt.plot(fileList, file2coveredLineNumOrdered)
    #plt.show()
    