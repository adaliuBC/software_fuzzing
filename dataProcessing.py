import pickle
import matplotlib.pyplot as plt
import numpy as np 
grammar = "SCSS" #"HTML"
mode = "pyscss"  #"bs4"
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

    for i in range(len(coverages)):  # decimal -> %
        coverages[i] = coverages[i] * 100
    print(coverages[-1])
    #plt.plot(trials, times, label=fuzzer)  # add label
    plt.plot(trials, coverages, label=fuzzer)  # add label
    plt.xlabel("Trial")
    plt.ylabel("Coverage(%)")
    #plt.ylabel("Time(s)")

    
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
    file2coveredLinesList.sort(key = lambda x: x[0])  # sort by name
    fuzzer2fileCoverage[fuzzer] = file2coveredLinesList

plt.legend()
plt.title("Coverage-Trial")
#plt.title("Time-Trial")
plt.show()
# # 画图
print("----", fuzzer2fileCoverage)
files = []
for fuzzer, filecov in fuzzer2fileCoverage.items():
    for i in range(len(filecov)):
        filename = filecov[i][0].split("\\")[-1][:-3]
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
            fileName = filecov[i][0].split("\\")[-1][:-3]
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
plt.xticks(x, xlabels)

plt.bar(x - width, rFuzzerY,  width=width, label='Random Fuzzer')
plt.bar(x, mFuzzerY, width=width, label='Mutation Fuzzer')
plt.bar(x + width, gFuzzerY, width=width, label='Grammar Fuzzer')
plt.xlabel("File Name")
plt.ylabel("Number of covered lines")
plt.legend()
plt.show()

