import pickle
import matplotlib.pyplot as plt
import numpy as np 
grammar = "HTML"
mode = "bs4"
fuzzers = ["Random Fuzzer", "Mutation Fuzzer", "Grammar Fuzzer"]
with open(f"./output/file2lines.pickle", "rb") as f:
    file2lines = pickle.load(f)  # total lines of file

fuzzer2fileCoverage = {}
for fuzzer in fuzzers:
    with open(f"./output/{grammar}_{mode}_{fuzzer}.pickle", "rb") as f:
        trials = pickle.load(f)
        coverages = pickle.load(f)
        times = pickle.load(f)
        lines = pickle.load(f)

    # plt.plot(trials, coverages, label=fuzzer)  # add label
    # plt.xlabel("Trial")
    # plt.ylabel("Covered proportion")
    # plt.title(fuzzer)
    # plt.show()

    
    filename2cnt = {}
    for line in lines:
        _, _, filename = line
        if filename not in filename2cnt.keys():
            filename2cnt[filename] = 1
        else:
            filename2cnt[filename] += 1
    for file, cnt in filename2cnt.items():
        print(f"{file}: {cnt}/{file2lines[file]}, {cnt/file2lines[file]}")
    
    file2coveredLinesList = []
    for file, cnt in filename2cnt.items():
        file2coveredLinesList.append([file, cnt])
    print("~~~~", file2coveredLinesList)
    file2coveredLinesList.sort(key = lambda x: x[0])  # sort by name
    print("====", file2coveredLinesList)
    fuzzer2fileCoverage[fuzzer] = file2coveredLinesList


# # 画图
print("----", fuzzer2fileCoverage)
files = []
for fuzzer, filecov in fuzzer2fileCoverage.items():
    for i in range(len(filecov)):
        filename = filecov[i][0].split("\\")[-1]
        if filename not in files:
            files.append(filename)
xlabels = files
size = len(xlabels)
x = np.arange(size)
ys = []
for fuzzer in ["Random Fuzzer", "Mutation Fuzzer", "Grammar Fuzzer"]:
    y = []
    filecov = fuzzer2fileCoverage[fuzzer]
    for targetFileName in files:
        isFound = False
        for i in range(len(filecov)):
            fileName = filecov[i][0].split("\\")[-1]
            fileLineCnt = filecov[i][1]
            if fileName == targetFileName:
                y.append(fileLineCnt)
                isFound = True
        if not isFound:
            y.append(0)
    ys.append(y)

rFuzzerY = ys[0]
mFuzzerY = ys[1]
gFuzzerY = ys[2]

print(xlabels)
print(x)
print(ys)

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / 2

plt.bar(x, rFuzzerY,  width=width, label='Random Fuzzer')
plt.bar(x + width, mFuzzerY, width=width, label='Mutation Fuzzer')
plt.bar(x + 2 * width, gFuzzerY, width=width, label='Grammar Fuzzer')
plt.legend()
plt.show()

