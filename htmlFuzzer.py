
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

# seed_input = "http://www.google.com/search?q=fuzzing"
# mutation_fuzzer = MutationFuzzer(seed=[seed_input])
# print([mutation_fuzzer.fuzz() for i in range(10)])

def countLines():
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
                    if line.isspace():
                        pass
                    elif "\""*3 in line:
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

def fuzzing(data):
    parser.feed(data)
    #print("Generated css code:\n", cssText)

def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

def operationWithSoup(data, parser):
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

file2lines = {}
# fileList = ["C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\parser.py",
#             "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\__init__.py",
#             "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\html\\entities.py"
#             ]
fileList = [
    #"C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\dammit.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\diagnose.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\element.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\formatter.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\testing.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\builder\\_html5lib.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\builder\\_htmlparser.py",
    "C:\\Users\\adali\\anaconda3\\envs\\python3\\lib\\site-packages\\bs4\\builder\\_lxml.py",
]
if __name__ == '__main__':
    # cnt the total line num that is provided by Pyscss
    # 计算总行数，benchmark（删除注释）
    random.seed(0)
    countLines()

    # build fuzzer list, prepare for test
    fuzzerList = []  # list of fuzzer

    # random fuzzer
    from Fuzzer import RandomFuzzer
    randomFuzzer = RandomFuzzer(min_length=500, max_length=1000)
    fuzzerList.append(randomFuzzer)  # open & close this fuzzer

    # mutation fuzzer
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
    #parser = HTMLParser()
    # with Coverage(fileList) as cov:
    #     parser.feed(seed)
    # print("Covered percentage single:\n", len(cov.coverage())/cntLines)
    # print("generated css code:\n", cssText)
    # print(len(cov.coverage()))
    fuzzerList.append(mutationFuzzer)  # open & close this fuzzer
    
    grammarFuzzer = GeneratorGrammarFuzzer(htmlGrammar, min_nonterminals=10, max_nonterminals=100, log = False)
    grammarFuzzer.check_grammar()
    grammarFuzzer.compute_cost()
    fuzzerList.append(grammarFuzzer)
    
    fuzzerNameList = ["Random Fuzzer", "Mutation Fuzzer", "Grammar Fuzzer"]
    trial = 200

    coveredLineLists = []
    timeList = []

    for i in range(len(fuzzerList)):
        fuzzer = fuzzerList[i]
        fuzzerName = fuzzerNameList[i]
        coveragePercentageAll = 0.
        coveredLines = set()
        xList = []
        yList = []
        starttime = time.time()
        for i in range(trial):
            #print("Generating data ... ")
            if fuzzerName == "Mutation Fuzzer" or "Random Fuzzer":
                data = fuzzer.fuzz()
            elif fuzzerName == "Grammar Fuzzer":
                fuzzer.fuzz()
                data = all_terminals(fuzzer.derivation_tree)

            #print(data)
            #print("Generated data, start compiling ... ")
            with Coverage(fileList) as cov:
                try:
                    # parser = HTMLParser()
                    # parser.feed(data)
                    # parser = HTMLParser(convert_charrefs = True)
                    # parser.feed(data)
                    operationWithSoup(data, "html.parser")
                    operationWithSoup(data, "lxml")
                    opeationWithSoup(data, "html5lib")

                except Exception as e:
                    print(e)
            # print("Covered percentage single:\n", len(cov.coverage())/cntLines)
            #print("Compile finiashed, start computing ... ")
            
            coveredLines = coveredLines | cov.coverage()
            xList.append(i)
            coverPercent = len(coveredLines)/cntLines
            yList.append(coverPercent)
            #print(len(coveredLines), cntLines)
            print(f"\r{fuzzerName} {i}th trial cover percent:", coverPercent)
            #print(cov)

        endtime = time.time()
        timeList.append(endtime-starttime)
        plt.plot(xList, yList, label=fuzzerName)  # add label
        plt.xlabel("Trial")
        plt.ylabel("Covered proportion")
        # plt.title(fuzzerName)
        # plt.show()

        # get coveredLines, 计算每个文件hit了多少次
        filename2cnt = {}
        linelist = list(coveredLines)
        linelist.sort(key = lambda x: (x[2], x[1]))

        for line in linelist:
            print(line)
        coveredLineLists.append(linelist)

        for line in coveredLines:
            funcname, _, filename = line
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
    plt.legend()
    plt.show()

    import pickle
    with open("save.pickle", "wb") as f:
        pickle.dump(coveredLineLists, f)
        pickle.dump(timeList, f)
    with open("save.pickle", "rb") as f:
        coveredLineLists = pickle.load(f)
        timeList = pickle.load(f)
        # print(coveredLineLists)
        # print(timeList)
    