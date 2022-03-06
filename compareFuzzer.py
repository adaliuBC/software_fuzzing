
from GrammarFuzzer import display_tree, all_terminals
from scssGrammar import SCSS_GRAMMAR
from splitGrammar import USE_GRAMMAR
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

# https://blog.csdn.net/weixin_42368421/article/details/101354628
class TimeoutError(Exception):
    def __init__(self, msg):
        super(TimeoutError, self).__init__()
        self.msg = msg

def time_out(interval, callback):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError("run func timeout")
 
        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)       # interval秒后向进程发送SIGALRM信号
                result = func(*args, **kwargs)
                signal.alarm(0)              # 函数在规定时间执行完后关闭alarm闹钟
                return result
            except TimeoutError, e:
                callback(e)
        return wrapper
    return decorator

def timeout_callback(e):
    print(e.msg)

if __name__ == '__main__':
    # cnt the total line num that is provided by Pyscss
    random.seed(1)
    global cntLines
    cntLines = 0
    for file in fileList:
        cntLine = len(open(file,'rb').readlines())
        cntLines += cntLine
    print("cntLines:", cntLines)

    fuzzerList = []  # list of fuzzer

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

    grammarFuzzer = GeneratorGrammarFuzzer(SCSS_GRAMMAR, min_nonterminals=20, max_nonterminals=50, log = False)
    grammarFuzzer.check_grammar()
    grammarFuzzer.compute_cost()
    fuzzerList.append(grammarFuzzer)
    
    fuzzerNameList = ["Grammar Fuzzer"]
    trial = 200

    deadInput = []



    for i in range(len(fuzzerList)):
        fuzzer = fuzzerList[i]
        fuzzerName = fuzzerNameList[i]
        coveragePercentageAll = 0.
        coveredLines = set()
        xList = []
        yList = []
        for i in range(trial):
            if fuzzerName == "Mutation Fuzzer":
                scssText = fuzzer.fuzz()
            elif fuzzerName == "Grammar Fuzzer":
                fuzzer.fuzz()
                scssText = all_terminals(fuzzer.derivation_tree)

            #print("\ngenerated scss code:\n", scssText)
            # thread = threading.Thread(target=fuzzing, args = (scssText, coveredLines,))
            # thread.setDaemon(True)
            # thread.start()
            with Coverage() as cov:
                try:
                    cssText = Compiler().compile_string(scssText)
                except func_timeout.exceptions.FunctionTimedOut:
                    print("Timeout, looks like deadloop, save the input")
                    deadInput.append(scssText)
                    coveredLines = coveredLines | cov.coverage()
                except Exception as e:
                    print(e)
            # print("Covered percentage single:\n", len(cov.coverage())/cntLines)
            print("generated css code:\n", cssText)
            coveredLines = coveredLines | cov.coverage()
            xList.append(i)
            coverPercent = len(coveredLines)/cntLines
            yList.append(coverPercent)
            print(len(coveredLines), cntLines)
            print(f"----{i}th trial cover percent:", coverPercent)
        plt.plot(xList, yList)  # add label
        plt.xlabel("Trial")
        plt.ylabel("Covered proportion")
        plt.title(fuzzerName)
        plt.show()

    print(len(coveredLines))
    
    #plt.plot(fileList, file2coveredLineNumOrdered)
    #plt.show()
    