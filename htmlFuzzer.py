
from lib2to3.pytree import convert
from GrammarFuzzer import display_tree, all_terminals
from htmlGrammar import htmlGrammar
#from splitGrammar import *

from html.parser import HTMLParser

from Coverage import Coverage
import matplotlib.pyplot as plt
from GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from MutationFuzzer import MutationFuzzer
import random
from func_timeout import func_set_timeout
import func_timeout
import time, threading, signal, pdb, pickle

# seed_input = "http://www.google.com/search?q=fuzzing"
# mutation_fuzzer = MutationFuzzer(seed=[seed_input])
# print([mutation_fuzzer.fuzz() for i in range(10)])


fileList_parser = [
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\parser.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\__init__.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\entities.py"
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
        print(file, cntLine)
        file2lines[file] = cntLine        
    with open(f"./output/file2lines.pickle", "wb") as f:
        pickle.dump(file2lines, f)
    print("totalLines:", totalLines)


def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


def operation_parser(data):
    parser = HTMLParser()
    parser.feed(data)
    parser = HTMLParser(convert_charrefs = True)
    parser.feed(data)


def operationWithSoup(data, parser):
    import bs4
    from bs4 import BeautifulSoup, CData, UnicodeDammit
    soup = BeautifulSoup(data, parser)
    soup.prettify()
    title = soup.title
    a = soup.a
    a = soup.find_all('a')
    link3 = soup.find(id = "link3")
    text = soup.get_text()

    tag = soup.a
    if tag != None:
        tag.name
        tag.name = "helloworld"
        for k, v in tag.attrs.items():
            del tag[k]
            tag[k] = ['180', 'conts']

    if tag.string:
        tag.string.replace_with("The roads goes ever on and on...")
    comment = soup.b.string
    cdata = CData("A CDATA block")
    if comment:  comment.replace_with(cdata)
    posstr = soup.string
    tag.find_next_siblings()
    tag.find_next_sibling()
    tag.find_previous_siblings()
    tag.find_previous_sibling()
    tag.find_previous()
    tag.find_all_previous()
    cont = soup.contents
    child = soup.children
    str = soup.string
    for str in soup.stripped_strings:
        pass
    soup.find_all(has_class_but_no_id)
    soup.find_all(a = "annatar")
    soup.find_all(string = "hello", limit = 3)
    soup.select("a")

def operation_bs4(data):
    import bs4
    from bs4 import BeautifulSoup, CData, UnicodeDammit
    pos = UnicodeDammit(data)
    operationWithSoup(data, "html.parser")
    operationWithSoup(data, "lxml")
    operationWithSoup(data, "html5lib")


def fuzzingTrial(fuzzerStruct):  # fuzzername: fuzzer, operation, fileList, trial
    fuzzerName, fuzzerInfo = fuzzerStruct
    fuzzer = fuzzerInfo[0]
    operation = fuzzerInfo[1]
    fileList = fuzzerInfo[2]
    trial = fuzzerInfo[3]
    print("Generating data ... ")
    if fuzzerName == "Mutation Fuzzer" or "Random Fuzzer":
        data = fuzzer.fuzz()
    elif fuzzerName == "Grammar Fuzzer":
        fuzzer.fuzz()
        data = all_terminals(fuzzer.derivation_tree)

    with Coverage(fileList) as cov:
        try:
            operation(data)
        except Exception as e:
            print(e)
    return cov

file2lines = {}

if __name__ == '__main__':
    
    trial = 50
    mode = "bs4"

    # build fuzzer list, prepare for test
    random.seed(0)
    countLines(fileList_bs4)
    fuzzerList = {}
    operation = operation_bs4
    fileList = fileList_bs4
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
    #fuzzerList["Mutation Fuzzer"] = [mutationFuzzer, operation, fileList, trial]

    # grammar fuzzer
    grammarFuzzer = GeneratorGrammarFuzzer(htmlGrammar, min_nonterminals=10, max_nonterminals=100, log = False)
    grammarFuzzer.check_grammar()
    grammarFuzzer.compute_cost()
    #fuzzerList["Grammar Fuzzer"] = [grammarFuzzer, operation, fileList, trial]

    coveredLineLists = []
    timeList = []

    for (fuzzerName, fuzzerInfo) in fuzzerList.items():
        # init value
        coveragePercentageAll = 0.
        coveredLines = set()
        xList = []
        yList = []
        timeList = []
        startTime = time.time()
        for i in range(trial):
            cov = fuzzingTrial((fuzzerName, fuzzerInfo))
            coveredLines = coveredLines | cov.coverage()
            coverPercent = len(coveredLines)/totalLines
            print(f"\r{fuzzerName} {i}th trial:{coverPercent} of code lines covered in total")
            xList.append(i)
            yList.append(coverPercent)
            timeList.append(time.time()-startTime)

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
        # with open(f"./output/HTML_{mode}_{fuzzerName}.pickle", "rb") as f:
        #     xList = pickle.load(f)
        #     yList = pickle.load(f)
        #     timeList = pickle.load(f)
        #     lineList = pickle.load(f)
        #     print(xList)
        #     print(yList)
        #     print(timeList)
        #     print(lineList)


    