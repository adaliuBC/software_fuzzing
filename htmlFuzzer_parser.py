
from GrammarFuzzer import display_tree, all_terminals
from htmlGrammar import htmlGrammar
from Coverage import Coverage
import matplotlib.pyplot as plt
from GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from MutationFuzzer import MutationFuzzer
import random, sys
from func_timeout import func_set_timeout
import func_timeout
import time, threading, signal, pdb, pickle
from operation import *

fileList_parser = [
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\parser.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\__init__.py",
    #"C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\entities.py"
]

fileList_bs4 = [
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\dammit.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\diagnose.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\element.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\formatter.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\testing.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\builder\\_html5lib.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\builder\\_htmlparser.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\builder\\_lxml.py",
]


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


def operation_parser(data):
    from html.parser import HTMLParser
    parser = HTMLParser()
    parser.feed(data)
    parser = HTMLParser(convert_charrefs = True)
    parser.feed(data)


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
    
    trial = 10000

    mode = "parser"
    fuzzerMode = sys.argv[1]
    # build fuzzer list, prepare for test
    random.seed(0)
    countLines(fileList_parser)
    fuzzerList = {}
    operation = operation_parser
    fileList = fileList_parser
    # random fuzzer
    from Fuzzer import RandomFuzzer
    randomFuzzer = RandomFuzzer(min_length=300, max_length=500)
    #fuzzerList["Random Fuzzer"] = [randomFuzzer, operation, fileList, trial]

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
    #fuzzerList["Mutation Fuzzer"] = [mutationFuzzer, operation, fileList, trial]

    # grammar fuzzer
    grammarFuzzer = GeneratorGrammarFuzzer(htmlGrammar, min_nonterminals=10, max_nonterminals=100, log = False)
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

        
    with open(f"./output/HTML_{mode}_{fuzzerName}.pickle", "wb") as f:
        pickle.dump(xList, f)
        pickle.dump(yList, f)
        pickle.dump(timeList, f)
        pickle.dump(lineList, f)
    #print(timeList)
