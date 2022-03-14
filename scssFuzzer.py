
from GrammarFuzzer import display_tree, all_terminals
from scssGrammar import SCSS_GRAMMAR
from splitGrammar import useGrammar
from scss import Compiler
from Coverage import Coverage
import matplotlib.pyplot as plt
from GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from MutationFuzzer import MutationFuzzer
import random, sys
# from func_timeout import func_set_timeout
# import func_timeout
import time, pickle
import pdb

prefixPath = "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\scss\\"

fileList_scss = [
    "Coverage.py", 
    prefixPath + "__main__.py", prefixPath + "__init__.py", 
    prefixPath + "ast.py", prefixPath + "calculator.py", prefixPath + "compiler.py", 
    prefixPath + "config.py", prefixPath + "cssdefs.py", prefixPath + "errors.py", 
    prefixPath + "legacy.py", prefixPath + "less2scss.py", prefixPath + "namespace.py",
    prefixPath + "rule.py", prefixPath + "scss_meta.py", prefixPath + "selector.py", 
    prefixPath + "setup.py", prefixPath + "source.py", prefixPath + "tool.py", 
    prefixPath + "types.py", prefixPath + "util.py", 
    prefixPath + "grammar\\expression.py", prefixPath + "grammar\\scanner.py", 
    prefixPath + "grammar\\__init__.py",
    prefixPath + "extension\\__init__.py", prefixPath + "extension\\api.py",
    prefixPath + "extension\\bootstrap.py", prefixPath + "extension\\core.py", 
    prefixPath + "extension\\extra.py", prefixPath + "extension\\fonts.py"]

def simplifyFname(fname):
    ind = fname.index("\\scss\\")
    return fname[ind+6:]


def countLines(fileList):
    global totalLines
    totalLines = 0
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
                    if line.isspace():
                        pass
                    elif "\""*3 in line:
                        line.replace((3*multiCommentwith), "aaa", 1)
                        if (3*multiCommentwith) in line:
                            pass
                        else:
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
        totalLines += cntLine
        #print(file, cntLine)
        file2lines[file] = cntLine        
    with open(f"./output/file2lines.pickle", "wb") as f:
        pickle.dump(file2lines, f)
    print("totalLines:", totalLines)
    
def operation_scss(data):
    cssText = Compiler().compile_string(data)

def fuzzingTrial(fuzzerStruct):  # fuzzername: fuzzer, operation, fileList, trial
    fuzzerName, fuzzerInfo = fuzzerStruct
    fuzzer = fuzzerInfo[0]
    operation = fuzzerInfo[1]
    fileList = fuzzerInfo[2]
    trial = fuzzerInfo[3]
    print("Generating data ... ")
    sTime = time.time()
    if fuzzerName == "Mutation Fuzzer" or "Random Fuzzer":
        data = fuzzer.fuzz()
    elif fuzzerName == "Grammar Fuzzer":
        fuzzer.fuzz()
        data = all_terminals(fuzzer.derivation_tree)
    eTime = time.time()
    with Coverage(fileList) as cov:
        try:
            operation(data)
        except Exception as e:
            print(e)
    return cov, eTime - sTime

file2lines = {}

if __name__ == '__main__':
    
    trial = 10

    # build fuzzer list, prepare for test
    random.seed(0)
    fuzzerMode = sys.argv[1]
    mode = "pyscss"
    countLines(fileList_scss)
    fuzzerList = {}
    operation = operation_scss
    fileList = fileList_scss
    # random fuzzer
    from Fuzzer import RandomFuzzer
    randomFuzzer = RandomFuzzer(min_length=300, max_length=500)
    fuzzerList["Random Fuzzer"] = [randomFuzzer, operation, fileList, trial]

    # mutation fuzzer
    # readin seeds
    import os
    rootdir="D:\\ada\\Master\\2022Winter\\Software Fuzzing\\software_fuzzing\\examples\\"
    filenameList = []
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        filenameList = filenames

    seedList = []
    for filename in filenameList:
        with open(".\\examples\\"+filename, "rb") as f:
            seed = f.read()
        seed = seed.decode(encoding='utf-8')
        seedList.append(seed)
    mutationFuzzer = MutationFuzzer(seedList)

    with open("example.txt", "rb") as f:
        seed = f.read()
    seed = seed.decode(encoding='utf-8')
    mutationFuzzer = MutationFuzzer([seed])
    cssText = Compiler().compile_string(seed)
    fuzzerList["Mutation Fuzzer"] = [mutationFuzzer, operation, fileList, trial]

    # grammar fuzzer
    grammarFuzzer = GeneratorGrammarFuzzer(useGrammar, min_nonterminals=10, max_nonterminals=30, log = False)
    grammarFuzzer.check_grammar()
    grammarFuzzer.compute_cost()
    fuzzerList["Grammar Fuzzer"] = [grammarFuzzer, operation, fileList, trial]

    coveredLineLists = []
    timeList = []

    if fuzzerMode == "RandomFuzzer":
        fuzzerName = "Random Fuzzer"
        fuzzerInfo = [randomFuzzer, operation, fileList, trial]
    elif fuzzerMode == "MutationFuzzer":
        fuzzerName = "Mutation Fuzzer"
        fuzzerInfo = [mutationFuzzer, operation, fileList, trial]
    elif fuzzerMode == "GrammarFuzzer":
        fuzzerName = "Grammar Fuzzer"
        fuzzerInfo = [grammarFuzzer, operation, fileList, trial]

    # init value
    coveragePercentageAll = 0.
    coveredLines = set()
    xList = []
    yList = []
    timeList = []
    startTime = time.time()
    for i in range(trial):
        #import bs4
        cov, posTime = fuzzingTrial((fuzzerName, fuzzerInfo))
        coveredLines = coveredLines | cov.coverage()
        coverPercent = len(coveredLines)/totalLines
        print(f"\r{fuzzerName} {i}th trial:{coverPercent} of code lines covered in total")
        xList.append(i)
        yList.append(coverPercent)
        timeList.append(timeList[-1]+posTime if len(timeList)>0 else posTime)

    endTime = time.time()
    posTime = endTime-startTime
    print(f"\r{fuzzerName} finished {trial} trials in {posTime}s")
    
    # get coveredLines, 计算每个文件hit了多少次
    lineList = list(coveredLines)
    lineList.sort(key = lambda x: (x[2], x[1]))

        
    with open(f"./output/SCSS_{mode}_{fuzzerName}.pickle", "wb") as f:
        pickle.dump(xList, f)
        pickle.dump(yList, f)
        pickle.dump(timeList, f)
        pickle.dump(lineList, f)
    #print(timeList)
