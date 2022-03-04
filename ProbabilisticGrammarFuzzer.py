#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Probabilistic Grammar Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/ProbabilisticGrammarFuzzer.html
# Last change: 2022-02-09 08:26:36+01:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''
The Fuzzing Book - Probabilistic Grammar Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python ProbabilisticGrammarFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.ProbabilisticGrammarFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/ProbabilisticGrammarFuzzer.html

A _probabilistic_ grammar allows to attach individual _probabilities_ to production rules.  To set the probability of an individual expansion `S` to the value `X` (between 0 and 1), replace it with a pair

(S, opts(prob=X))


If we want to ensure that 90% of phone numbers generated have an area code starting with `9`, we can write:

>>> from Grammars import US_PHONE_GRAMMAR, extend_grammar, opts
>>> PROBABILISTIC_US_PHONE_GRAMMAR: Grammar = extend_grammar(US_PHONE_GRAMMAR,
>>> {
>>>       "": [
>>>                           "2", "3", "4", "5", "6", "7", "8",
>>>                           ("9", opts(prob=0.9))
>>>                       ],
>>> })

A `ProbabilisticGrammarFuzzer` will extract and interpret these options.  Here is an example:

>>> probabilistic_us_phone_fuzzer = ProbabilisticGrammarFuzzer(PROBABILISTIC_US_PHONE_GRAMMAR)
>>> [probabilistic_us_phone_fuzzer.fuzz() for i in range(5)]
['(918)925-2501',
 '(981)925-0792',
 '(934)995-5029',
 '(955)999-7801',
 '(964)927-0877']

As you can see, the large majority of area codes now starts with `9`.

For more details, source, and documentation, see
"The Fuzzing Book - Probabilistic Grammar Fuzzing"
at https://www.fuzzingbook.org/html/ProbabilisticGrammarFuzzer.html
'''

# Probabilistic Grammar Fuzzing
# =============================

## The Law of Leading Digits
## -------------------------

from Fuzzer import Fuzzer
from ExpectError import ExpectError

from GrammarFuzzer import GrammarFuzzer, all_terminals, display_tree, DerivationTree

from Grammars import is_valid_grammar, EXPR_GRAMMAR, START_SYMBOL, crange
from Grammars import opts, exp_string, exp_opt, set_opts
from Grammars import Grammar, Expansion

from typing import List, Dict, Set, Optional, cast, Any, Tuple

import math

import matplotlib.pyplot as plt  # type: ignore

import random
random.seed(2001)

def first_digit_via_string(x: int) -> int:
    return ord(repr(x)[0]) - ord('0')

def first_digit_via_log(x: int) -> int:
    """
    本福特定律：
    log_{10}{d} < log_{10}{x} < log_{10}{d+1}
    """
    frac, whole = math.modf(math.log10(x))
    return int(10 ** frac)

def prob_leading_digit(d: int) -> float:
    return math.log10(d + 1) - math.log10(d)


PROBABILISTIC_EXPR_GRAMMAR: Grammar = {
    "<start>":
        ["<expr>"],

    "<expr>":
        [("<term> + <expr>", opts(prob=0.1)),
         ("<term> - <expr>", opts(prob=0.2)),
         "<term>"],

    "<term>":
        [("<factor> * <term>", opts(prob=0.1)),
         ("<factor> / <term>", opts(prob=0.1)),
         "<factor>"
         ],

    "<factor>":
        ["+<factor>", "-<factor>", "(<expr>)",
            "<leadinteger>", "<leadinteger>.<integer>"],

    "<leadinteger>":
        ["<leaddigit><integer>", "<leaddigit>"],

    # Benford's law: frequency distribution of leading digits
    "<leaddigit>":
        [("1", opts(prob=0.301)),
         ("2", opts(prob=0.176)),
         ("3", opts(prob=0.125)),
         ("4", opts(prob=0.097)),
         ("5", opts(prob=0.079)),
         ("6", opts(prob=0.067)),
         ("7", opts(prob=0.058)),
         ("8", opts(prob=0.051)),
         ("9", opts(prob=0.046)),
         ],

    # Remaining digits are equally distributed
    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

def exp_prob(expansion: Expansion) -> float:
    """Return the options of an expansion - 取出expansion中的prob"""
    return exp_opt(expansion, 'prob')

from GrammarCoverageFuzzer import GrammarCoverageFuzzer  # minor dependency
## Computing Probabilities
## -----------------------

### Distributing Probabilities

def prob_distribution(probabilities: List[Optional[float]],
                      nonterminal: str = "<symbol>"):
    """
    检查：如果所有prob都给定，那么它们必须和为1，返回
    or
    计算：如果不是所有的都给定，那么把剩下的prob平均分配在不同的unspecified non-terminal上
    """
    epsilon = 0.00001
    
    number_of_unspecified_probabilities = probabilities.count(None)
    if number_of_unspecified_probabilities == 0:
        sum_probabilities = cast(float, sum(probabilities))
        assert abs(sum_probabilities - 1.0) < epsilon, \
            nonterminal + ": sum of probabilities must be 1.0"
        return probabilities

    sum_of_specified_probabilities = 0.0
    for p in probabilities:
        if p is not None:
            sum_of_specified_probabilities += p
    assert 0 <= sum_of_specified_probabilities <= 1.0, \
        nonterminal + ": sum of specified probabilities must be between 0.0 and 1.0"

    default_probability = ((1.0 - sum_of_specified_probabilities)
                           / number_of_unspecified_probabilities)
    all_probabilities = []
    for p in probabilities:
        if p is None:
            p = default_probability
        all_probabilities.append(p)

    assert abs(sum(all_probabilities) - 1.0) < epsilon
    return all_probabilities

def exp_probabilities(expansions: List[Expansion],
                      nonterminal: str ="<symbol>") \
        -> Dict[Expansion, float]:
    # map digit到prob
    probabilities = [exp_prob(expansion) for expansion in expansions]
    prob_dist = prob_distribution(probabilities, nonterminal)  # type: ignore

    prob_mapping: Dict[Expansion, float] = {}
    for i in range(len(expansions)):
        expansion = exp_string(expansions[i])
        prob_mapping[expansion] = prob_dist[i]

    return prob_mapping

### Checking Probabilities
def is_valid_probabilistic_grammar(grammar: Grammar,
                                   start_symbol: str = START_SYMBOL) -> bool:
    """
    检查是不是有效的grammar
    """
    if not is_valid_grammar(grammar, start_symbol):
        return False

    for nonterminal in grammar:
        expansions = grammar[nonterminal]
        _ = exp_probabilities(expansions, nonterminal)

    return True



## Expanding by Probability
## ------------------------
class ProbabilisticGrammarFuzzer(GrammarFuzzer):
    """A grammar-based fuzzer respecting probabilities in grammars."""

    def check_grammar(self) -> None:
        """
        检查语法valid
        """
        super().check_grammar()
        assert is_valid_probabilistic_grammar(self.grammar)

    def supported_opts(self) -> Set[str]:
        """
        把opt加入support
        """
        return super().supported_opts() | {'prob'}

    def choose_node_expansion(self, node: DerivationTree,
                              children_alternatives: List[Any]) -> int:
        """
        重载expand node的函数
        """
        (symbol, tree) = node
        expansions = self.grammar[symbol]
        probabilities = exp_probabilities(expansions)

        weights: List[float] = []
        for children in children_alternatives:
            expansion = all_terminals((symbol, children))
            children_weight = probabilities[expansion]
            if self.log:
                print(repr(expansion), "p =", children_weight)
            weights.append(children_weight)

        if sum(weights) == 0:
            # No alternative (probably expanding at minimum cost)
            return random.choices(
                range(len(children_alternatives)))[0]
        else:
            return random.choices(
                range(len(children_alternatives)), weights=weights)[0]

## Directed Fuzzing
## ----------------
from Grammars import URL_GRAMMAR, extend_grammar
from Grammars import EXPR_GRAMMAR

## 为fuzzing过程中修改prob提供API
def set_prob(grammar: Grammar, symbol: str, 
             expansion: Expansion, prob: Optional[float]) -> None:
    """Set the probability of the given expansion of grammar[symbol]"""
    set_opts(grammar, symbol, expansion, opts(prob=prob))

## Probabilities in Context
## ------------------------
## 在概率的基础上考虑上下文（比如IPV4地址四段中某一段赋固定值，其他段仍然随机）
def decrange(start: int, end: int) -> List[Expansion]:
    """Return a list with string representations of numbers in the range [start, end)"""
    return [repr(n) for n in range(start, end)]

# 原始语法
IP_ADDRESS_GRAMMAR: Grammar = {
    "<start>": ["<address>"],
    "<address>": ["<octet>.<octet>.<octet>.<octet>"],
    # ["0", "1", "2", ..., "255"]
    "<octet>": decrange(0, 256)
}

# 修改之后，我们把<octet> * 4改成duplicate的<octet-1>, -2, -3, -4四个，并赋不同概率
from GrammarCoverageFuzzer import duplicate_context  # minor dependency

## Learning Probabilities from Samples
## -----------------------------------

### Counting Expansions

from Parser import Parser, EarleyParser

IP_ADDRESS_TOKENS = {"<octet>"}  # EarleyParser needs explicit tokens

from GrammarCoverageFuzzer import expansion_key  # minor dependency

from Grammars import is_nonterminal

class ExpansionCountMiner:
    def __init__(self, parser: Parser, log: bool = False) -> None:
        assert isinstance(parser, Parser)
        self.grammar = extend_grammar(parser.grammar())
        self.parser = parser
        self.log = log
        self.reset()

class ExpansionCountMiner(ExpansionCountMiner):
    def reset(self) -> None:
        self.expansion_counts: Dict[str, int] = {}

    def add_coverage(self, symbol: str, children: List[DerivationTree]) -> None:
        key = expansion_key(symbol, children)

        if self.log:
            print("Found", key)

        if key not in self.expansion_counts:
            self.expansion_counts[key] = 0
        self.expansion_counts[key] += 1

    def add_tree(self, tree: DerivationTree) -> None:
        (symbol, children) = tree
        if not is_nonterminal(symbol):
            return
        assert children is not None

        direct_children: List[DerivationTree] = [
            (symbol, None) if is_nonterminal(symbol) 
            else (symbol, []) for symbol, c in children]
        self.add_coverage(symbol, direct_children)

        for c in children:
            self.add_tree(c)

class ExpansionCountMiner(ExpansionCountMiner):
    def count_expansions(self, inputs: List[str]) -> None:
        for inp in inputs:
            tree, *_ = self.parser.parse(inp)
            self.add_tree(tree)

    def counts(self) -> Dict[str, int]:
        return self.expansion_counts

### Assigning Probabilities

class ProbabilisticGrammarMiner(ExpansionCountMiner):
    def set_probabilities(self, counts: Dict[str, int]):
        for symbol in self.grammar:
            self.set_expansion_probabilities(symbol, counts)

    def set_expansion_probabilities(self, symbol: str, counts: Dict[str, int]):
        expansions = self.grammar[symbol]
        if len(expansions) == 1:
            set_prob(self.grammar, symbol, expansions[0], None)
            return

        expansion_counts = [
            counts.get(
                expansion_key(
                    symbol,
                    expansion),
                0) for expansion in expansions]
        total = sum(expansion_counts)
        for i, expansion in enumerate(expansions):
            p = expansion_counts[i] / total if total > 0 else None
            # if self.log:
            #     print("Setting", expansion_key(symbol, expansion), p)
            set_prob(self.grammar, symbol, expansion, p)

class ProbabilisticGrammarMiner(ProbabilisticGrammarMiner):
    def mine_probabilistic_grammar(self, inputs: List[str]) -> Grammar:
        self.count_expansions(inputs)
        self.set_probabilities(self.counts())
        return self.grammar

URL_SAMPLE: List[str] = [
    "https://user:password@cispa.saarland:80/",
    "https://fuzzingbook.com?def=56&x89=3&x46=48&def=def",
    "https://cispa.saarland:80/def?def=7&x23=abc",
    "https://fuzzingbook.com:80/",
    "https://fuzzingbook.com:80/abc?def=abc&abc=x14&def=abc&abc=2&def=38",
    "ftps://fuzzingbook.com/x87",
    "https://user:password@fuzzingbook.com:6?def=54&x44=abc",
    "http://fuzzingbook.com:80?x33=25&def=8",
    "http://fuzzingbook.com:8080/def",
]

URL_TOKENS: Set[str] = {"<scheme>", "<userinfo>", "<host>", "<port>", "<id>"}

### Testing Uncommon Features

import copy

def invert_expansion(expansion: List[Expansion]) -> List[Expansion]:
    def sort_by_prob(x: Tuple[int, float]) -> float:
        index, prob = x
        return prob if prob is not None else 0.0

    inverted_expansion: List[Expansion] = copy.deepcopy(expansion)
    indexes_and_probs = [(index, exp_prob(alternative))
                         for index, alternative in enumerate(expansion)]
    indexes_and_probs.sort(key=sort_by_prob)
    indexes = [i for (i, _) in indexes_and_probs]

    for j in range(len(indexes)):
        k = len(indexes) - 1 - j
        # print(indexes[j], "gets", indexes[k])
        inverted_expansion[indexes[j]][1]['prob'] = expansion[indexes[k]][1]['prob']  # type: ignore

    return inverted_expansion

def invert_probs(grammar: Grammar) -> Grammar:
    inverted_grammar = extend_grammar(grammar)
    for symbol in grammar:
        inverted_grammar[symbol] = invert_expansion(grammar[symbol])
    return inverted_grammar

### Learning Probabilities from Input Slices

from Coverage import Coverage, cgi_decode
from Grammars import CGI_GRAMMAR

from Grammars import US_PHONE_GRAMMAR, extend_grammar, opts

PROBABILISTIC_US_PHONE_GRAMMAR: Grammar = extend_grammar(US_PHONE_GRAMMAR,
{
      "<lead-digit>": [
                          "2", "3", "4", "5", "6", "7", "8",
                          ("9", opts(prob=0.9))
                      ],
})


from ClassDiagram import display_class_hierarchy
from bookutils import inheritance_conflicts

class ProbabilisticGrammarCoverageFuzzer(
        GrammarCoverageFuzzer, ProbabilisticGrammarFuzzer):
    # Choose uncovered expansions first
    def choose_node_expansion(self, node, children_alternatives):
        return GrammarCoverageFuzzer.choose_node_expansion(
            self, node, children_alternatives)

    # Among uncovered expansions, pick by (relative) probability
    def choose_uncovered_node_expansion(self, node, children_alternatives):
        return ProbabilisticGrammarFuzzer.choose_node_expansion(
            self, node, children_alternatives)

    # For covered nodes, pick by probability, too
    def choose_covered_node_expansion(self, node, children_alternatives):
        return ProbabilisticGrammarFuzzer.choose_node_expansion(
            self, node, children_alternatives)


from scssGrammar import SCSS_GRAMMAR
from scss import Compiler
#from GeneratorGrammarFuzzer import PGGCFuzzer
# 试试不同的fuzzer
if __name__ == '__main__':

    f = GrammarFuzzer(SCSS_GRAMMAR, min_nonterminals=3, max_nonterminals=50, log=True)
    f.check_grammar()
    f.compute_cost()
    f.fuzz()
    treeFig = display_tree(f.derivation_tree)
    treeFig.render(directory="./output/", filename="scss_grammar_tree", view=True)
    scssText = all_terminals(f.derivation_tree)
    # with open("try.txt", "w") as f:
    #     f.write(scssText)
    print("generated scss code:\n", scssText)
    
    cssText = Compiler().compile_string(scssText)
    print("generated css code:\n", cssText)
    '''
    with Coverage() as cov:
        css = Compiler().compile_string(scss)
    #pdb.set_trace()
    trace = cov.trace()
    coverage = cov.coverage()
    print(coverage)
    '''
'''
if __name__ == '__main__':
    cov_leaddigit_fuzzer = ProbabilisticGrammarCoverageFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leaddigit>")
    print([cov_leaddigit_fuzzer.fuzz() for i in range(9)])

if __name__ == '__main__':
    trials = 10000

    count = {}
    for c in crange('0', '9'):
        count[c] = 0

    for i in range(trials):
        count[cov_leaddigit_fuzzer.fuzz()] += 1

    print([(digit, count[digit] / trials) for digit in count])

'''