import pickle as pickle

fuzzerNameList = ["Random Fuzzer", "Mutation Fuzzer", "Grammar Fuzzer"]
with open("save.pickle", "rb") as f:
    coveredLineLists = pickle.load(f)
    timeList = pickle.load(f)
    #print(coveredLineLists)
    #print(timeList)
for i in range(len(fuzzerNameList)):
    fuzzerName = fuzzerNameList[i]
    coveredLines = coveredLineLists[i]
    time = timeList[i]
for line in (set(coveredLineLists[1]) - set(coveredLineLists[2])):
    print(line)
