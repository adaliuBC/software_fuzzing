import pickle as pickle

grammar = "HTML" #"HTML"
mode = "bs4"  #"bs4"
fuzzers = ["Random Fuzzer", "Mutation Fuzzer", "Grammar Fuzzer"]
lines = []
for fuzzer in fuzzers:
    with open(f"./output/{grammar}_{mode}_{fuzzer}.pickle", "rb") as f:
        trial = pickle.load(f)
        coverage = pickle.load(f)
        time = pickle.load(f)
        line = pickle.load(f)
        lines.append(line)

mutation_grammar = list(set(lines[1]) - set(lines[2]))
mutation_grammar.sort(key=lambda x: (x[2], x[0], x[1]))


grammar_mutation = list(set(lines[2]) - set(lines[1]))
grammar_mutation.sort(key=lambda x: x[2])

for line in mutation_grammar:
    print(line)
print("============================")
for line in grammar_mutation:
    print(line)
