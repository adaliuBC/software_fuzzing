#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This is the course project code for CS293C W22 @ UCSB. The original code 
is from fuzzingbook.org, and is revised by @adaliuBC.
'''
# "Efficient Grammar Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GrammarFuzzer.html
# Last change: 2022-02-09 08:23:49+01:00
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
The Fuzzing Book - Efficient Grammar Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python GrammarFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.GrammarFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/GrammarFuzzer.html

### Efficient Grammar Fuzzing

This chapter introduces `GrammarFuzzer`, an efficient grammar fuzzer that takes a grammar to produce syntactically valid input strings.  Here's a typical usage:

>>> from Grammars import US_PHONE_GRAMMAR
>>> phone_fuzzer = GrammarFuzzer(US_PHONE_GRAMMAR)
>>> phone_fuzzer.fuzz()
'(613)417-7523'

The `GrammarFuzzer` constructor takes a number of keyword arguments to control its behavior.  `start_symbol`, for instance, allows to set the symbol that expansion starts with (instead of ``):

>>> area_fuzzer = GrammarFuzzer(US_PHONE_GRAMMAR, start_symbol='')
>>> area_fuzzer.fuzz()
'367'

Here's how to parameterize the `GrammarFuzzer` constructor:

Produce strings from `grammar`, starting with `start_symbol`.
If `min_nonterminals` or `max_nonterminals` is given, use them as limits 
for the number of nonterminals produced.  
If `disp` is set, display the intermediate derivation trees.
If `log` is set, show intermediate steps as text on standard output.
### Derivation Trees

Internally, `GrammarFuzzer` makes use of [derivation trees](#Derivation-Trees), which it expands step by step.  After producing a string, the tree produced can be accessed in the `derivation_tree` attribute.

>>> display_tree(phone_fuzzer.derivation_tree)
In the internal representation of a derivation tree, a _node_ is a pair (`symbol`, `children`).  For nonterminals, `symbol` is the symbol that is being expanded, and `children` is a list of further nodes.  For terminals, `symbol` is the terminal string, and `children` is empty.

>>> phone_fuzzer.derivation_tree
('',
 [('',
   [('(', []),
    ('',
     [('', [('6', [])]),
      ('', [('1', [])]),
      ('', [('3', [])])]),
    (')', []),
    ('',
     [('', [('4', [])]),
      ('', [('1', [])]),
      ('', [('7', [])])]),
    ('-', []),
    ('',
     [('', [('7', [])]),
      ('', [('5', [])]),
      ('', [('2', [])]),
      ('', [('3', [])])])])])

The chapter contains various helpers to work with derivation trees, including visualization tools – notably, `display_tree()`, above.


For more details, source, and documentation, see
"The Fuzzing Book - Efficient Grammar Fuzzing"
at https://www.fuzzingbook.org/html/GrammarFuzzer.html
'''

from typing import Tuple, List, Optional, Any, Union, Set, Callable, Dict

from bookutils import unicode_escape

from Fuzzer import Fuzzer

from Grammars import EXPR_EBNF_GRAMMAR, convert_ebnf_grammar, Grammar, Expansion
from Grammars import simple_grammar_fuzzer, is_valid_grammar, exp_string

from ExpectError import ExpectTimeout
 
import matplotlib.pyplot as plt
import random


from Grammars import simple_grammar_fuzzer
from Grammars import START_SYMBOL, EXPR_GRAMMAR, URL_GRAMMAR, CGI_GRAMMAR
from Grammars import RE_NONTERMINAL, nonterminals, is_nonterminal
from Timer import Timer
from scss import Compiler
from Coverage import Coverage

from graphviz import Digraph

from IPython.display import display
import re
import pdb

from Coverage import Coverage

DerivationTree = Tuple[str, Optional[List[Any]]]


def dot_escape(s: str) -> str:
    """Return s in a form suitable for dot"""
    s = re.sub(r'([^a-zA-Z0-9" ])', r"\\\1", s)
    return s


def extract_node(node, id):
    symbol, children, *annotation = node
    return symbol, children, ''.join(str(a) for a in annotation)

def default_node_attr(dot, nid, symbol, ann):
    dot.node(repr(nid), dot_escape(unicode_escape(symbol)))

def default_edge_attr(dot, start_node, stop_node):
    dot.edge(repr(start_node), repr(stop_node))

def default_graph_attr(dot):
    dot.attr('node', shape='plain')

def display_tree(derivation_tree: DerivationTree,
                 log: bool = False,
                 extract_node: Callable = extract_node,
                 node_attr: Callable = default_node_attr,
                 edge_attr: Callable = default_edge_attr,
                 graph_attr: Callable = default_graph_attr) -> Any:
    # If we import display_tree, we also have to import its functions
    from graphviz import Digraph

    counter = 0

    def traverse_tree(dot, tree, id=0):
        (symbol, children, annotation) = extract_node(tree, id)
        node_attr(dot, id, symbol, annotation)

        if children:
            for child in children:
                nonlocal counter
                counter += 1
                child_id = counter
                edge_attr(dot, id, child_id)
                traverse_tree(dot, child, child_id)

    dot = Digraph(comment="Derivation Tree")
    graph_attr(dot)
    traverse_tree(dot, derivation_tree)
    if log:
        print(dot)
    return dot


def display_annotated_tree(tree: DerivationTree,
                           a_nodes: Dict[int, str],
                           a_edges: Dict[Tuple[int, int], str],
                           log: bool = False):
    def graph_attr(dot):
        dot.attr('node', shape='plain')
        dot.graph_attr['rankdir'] = 'LR'

    def annotate_node(dot, nid, symbol, ann):
        if nid in a_nodes:
            dot.node(repr(nid), 
                     "%s (%s)" % (dot_escape(unicode_escape(symbol)),
                                  a_nodes[nid]))
        else:
            dot.node(repr(nid), dot_escape(unicode_escape(symbol)))

    def annotate_edge(dot, start_node, stop_node):
        if (start_node, stop_node) in a_edges:
            dot.edge(repr(start_node), repr(stop_node),
                     a_edges[(start_node, stop_node)])
        else:
            dot.edge(repr(start_node), repr(stop_node))

    return display_tree(tree, log=log,
                        node_attr=annotate_node,
                        edge_attr=annotate_edge,
                        graph_attr=graph_attr)


#### display all leaves in the tree as a string
def all_terminals(tree: DerivationTree) -> str:
    (symbol, children) = tree
    if children is None:
        # This is a nonterminal symbol not expanded yet
        return symbol

    if len(children) == 0:
        # This is a terminal symbol
        return symbol

    # This is an expanded symbol:
    # Concatenate all terminal symbols from all children
    return ''.join([all_terminals(c) for c in children])


#### Display tree as a string
def tree_to_string(tree: DerivationTree) -> str:
    symbol, children, *_ = tree
    if children:
        return ''.join(tree_to_string(c) for c in children)
    else:
        return '' if is_nonterminal(symbol) else symbol


### Getting a List of Possible Expansions
### input一个expansion string，把string分解成derivation trees的列表，
### 每个string中的symbol都对应一个tree。
def expansion_to_children(expansion: Expansion) -> List[DerivationTree]:
    # print("Converting " + repr(expansion))
    # strings contains all substrings -- both terminals and nonterminals such
    # that ''.join(strings) == expansion

    expansion = exp_string(expansion)
    assert isinstance(expansion, str)

    if expansion == "":  # Special case: epsilon expansion
        return [("", [])]

    strings = re.split(RE_NONTERMINAL, expansion)
    return [(s, None) if is_nonterminal(s) else (s, [])
            for s in strings if len(s) > 0]


class GrammarFuzzer(Fuzzer):
    """Produce strings from grammars efficiently, using derivation trees."""

    def __init__(self,
                 grammar: Grammar,
                 start_symbol: str = START_SYMBOL,
                 min_nonterminals: int = 0,
                 max_nonterminals: int = 10,
                 disp: bool = False,
                 log: Union[bool, int] = False) -> None:
        """Produce strings from `grammar`, starting with `start_symbol`.
        If `min_nonterminals` or `max_nonterminals` is given, use them as limits 
        for the number of nonterminals produced.  
        If `disp` is set, display the intermediate derivation trees.
        If `log` is set, show intermediate steps as text on standard output."""

        self.grammar = grammar
        self.start_symbol = start_symbol
        self.min_nonterminals = min_nonterminals
        self.max_nonterminals = max_nonterminals
        self.disp = disp
        self.log = log
        self.check_grammar()  # Invokes is_valid_grammar()
        self.symbol2cost = {}
        self.seen = set()

    def check_grammar(self) -> None:
        """Check the grammar passed is valid"""
        assert self.start_symbol in self.grammar
        assert is_valid_grammar(
            self.grammar,
            start_symbol=self.start_symbol,
            supported_opts=self.supported_opts())

    def supported_opts(self) -> Set[str]:
        """
        Set of supported options. To be overloaded in subclasses. 
        支持的options列表，用来在可能存在的subclasses里面重载运算符。
        """
        return set()  # We don't support specific options

    def init_tree(self) -> DerivationTree:
        """
        helper function，用来建立只有start symbol的tree
        """
        return (self.start_symbol, None)

    # node：当前要expand的node
    # children_alternatives：该node对应的可能的expansions列表
    # return：在所有children expansions里面，随机抽一个index
    ### Picking a Children Alternative to be Expanded
    def choose_node_expansion(self, node: DerivationTree,
                              children_alternatives: List[List[DerivationTree]]) -> int:
        """Return index of expansion in `children_alternatives` to be selected.
           'children_alternatives`: a list of possible children for `node`.
           Defaults to random. To be overloaded in subclasses."""
        return random.randrange(0, len(children_alternatives))

    def expansion_to_children(self, expansion: Expansion) -> List[DerivationTree]:
        return expansion_to_children(expansion)

    def expand_node_randomly(self, node: DerivationTree) -> DerivationTree:
        """
        Choose a random expansion for `node` and return it
        1. 给定tree里面的一个可以expand的node
        2. 选node的一个random expansion
        3. 返回new tree
        """
        (symbol, children) = node
        assert children is None  # 确定node还可以再expand

        # 记log
        if self.log:
            print("Expanding", all_terminals(node), "randomly")

        # Fetch the possible expansions from grammar...
        expansions = self.grammar[symbol]
        children_alternatives: List[List[DerivationTree]] = [
            self.expansion_to_children(expansion) for expansion in expansions
        ]

        # ... and select a random expansion
        index = self.choose_node_expansion(node, children_alternatives)
        chosen_children = children_alternatives[index]

        # Process children (for subclasses)
        chosen_children = self.process_chosen_children(chosen_children,
                                                       expansions[index])

        # Return with new children
        return (symbol, chosen_children)

    def expand_node(self, node: DerivationTree) -> DerivationTree:
        """
        用来选择不同的expansion strategy（现在就只是random一个罢了）
        """
        return self.expand_node_randomly(node)

    def process_chosen_children(self,
                                chosen_children: List[DerivationTree],
                                expansion: Expansion) -> List[DerivationTree]:
        """Process children after selection.  By default, does nothing."""
        return chosen_children

    def possible_expansions(self, node: DerivationTree) -> int:
        """
        计数这个node为根的整棵子树中的所有children的可能expansion数
        （对于input = 整棵树的DerivationTree的情况，就等于计算整个树里面有多少可能expansions）
        """
        (symbol, children) = node
        if children is None:
            return 1
        return sum(self.possible_expansions(c) for c in children)

    def any_possible_expansions(self, node: DerivationTree) -> bool:
        """
        Return true if the tree has any unexpanded nodes
        """
        (symbol, children) = node
        if children is None:
            return True  # ??? children == None是什么意思？

        return any(self.any_possible_expansions(c) for c in children)

    def choose_tree_expansion(self,
                              tree: DerivationTree,
                              children: List[DerivationTree]) -> int:
        """Return index of subtree in `children` to be selected for expansion.
           Defaults to random."""
        return random.randrange(0, len(children))

    def expand_tree_once(self, tree: DerivationTree) -> DerivationTree:
        """
        Choose an unexpanded symbol in tree; expand it inplace.
        Can be overloaded in subclasses.
        在tree里面选一个没有expand完的symbol，inplace地拓展它。
        """
        (symbol, children) = tree
        if children is None:  # ??? 这个symbol再expand一下就是None了？
            # Expand this node
            return self.expand_node(tree)

        # Find all children with possible expansions 
        # 找到所有可以expand的children
        expandable_children = [
            c for c in children if self.any_possible_expansions(c)]

        # `index_map` translates an index in `expandable_children`
        # back into the original index in `children`
        index_map = [i for (i, c) in enumerate(children)
                     if c in expandable_children]

        # Select a random child
        child_to_be_expanded = \
            self.choose_tree_expansion(tree, expandable_children)

        # Expand in place
        children[index_map[child_to_be_expanded]] = \
            self.expand_tree_once(expandable_children[child_to_be_expanded])

        return tree

    def symbol_cost(self, symbol: str, seen: Set[str] = set()) \
            -> Union[int, float]:
        """
        返回symbol的所有拓展里面的min cost
        """
        expansions = self.grammar[symbol]
        return min(self.expansion_cost(e, seen | {symbol}) for e in expansions)

    def expansion_cost(self, expansion: Expansion,
                       seen: Set[str] = set()) -> Union[int, float]:
        """
        返回所有expansions里面的expansion的cost之和
        """
        symbols = nonterminals(expansion)
        if len(symbols) == 0:
            return 1  # no symbol

        if any(s in seen for s in symbols):
            return float('inf')
        # if seen again -> inf，因为loop了

        # the value of a expansion is the sum of all expandable variables
        # inside + 1
        return sum(self.symbol_cost(s, seen) for s in symbols) + 1


    def expand_node_by_cost(self, node: DerivationTree, 
                            choose: Callable = min) -> DerivationTree:
        #print("Computing cost 1...")
        (symbol, children) = node
        assert children is None

        # Fetch the possible expansions from grammar...
        expansions = self.grammar[symbol]
        
        # children和cost的列表
        # （expansion_to_children是把expansion的string转换成children list）
        children_alternatives_with_cost = []
        self.seen = {symbol}
        for expansion in expansions:
            exp2child = self.expansion_to_children(expansion)
            
            ##
            symbols = nonterminals(expansion)
            if len(symbols) == 0:
                exp_cost = 1  # no symbol
            elif any(s in self.seen for s in symbols):
                exp_cost = float('inf')
            # if seen again -> inf，因为loop了
            else:
                exp_cost = 1
                for symbol in symbols:
                    exp_cost += self.symbol2cost[symbol]
            ##
            
            #exp_cost = self.expansion_cost(expansion, {symbol})
            children_alternatives_with_cost.append(
                (exp2child, exp_cost, expansion)
            )
        #print("Computing cost 2...")

        # 用choose函数选一个cost，并且取该cost对应的children和expansions
        # （此处考虑的是多个children的cost相同，把这些cost相同的children做成一个list）
        # 此处choose对应的函数就是min
        costs = [cost for (child, cost, expansion)
                 in children_alternatives_with_cost]
        chosen_cost = choose(costs)
        children_with_chosen_cost = [child for (child, child_cost, _) 
                                     in children_alternatives_with_cost
                                     if child_cost == chosen_cost]
        expansion_with_chosen_cost = [expansion for (_, child_cost, expansion)
                                      in children_alternatives_with_cost
                                      if child_cost == chosen_cost]

        # 在node的所有cost相同（== min cost）的children里面选一个
        index = self.choose_node_expansion(node, children_with_chosen_cost)
        #print("Computing cost 3...")

        chosen_children = children_with_chosen_cost[index]
        chosen_expansion = expansion_with_chosen_cost[index]
        chosen_children = self.process_chosen_children(
            chosen_children, chosen_expansion)
        #print("Computing cost 4...")

        # Return with a new list
        return (symbol, chosen_children)


    def expand_node_min_cost(self, node: DerivationTree) -> DerivationTree:
        if self.log:
            print("Expanding", all_terminals(node), "at minimum cost")
        #pdb.set_trace()
        return self.expand_node_by_cost(node, min)


    def expand_node_max_cost(self, node: DerivationTree) -> DerivationTree:
        if self.log:
            print("Expanding", all_terminals(node), "at maximum cost")

        return self.expand_node_by_cost(node, max)

    #'''
    def recursion_compute_cost(self, symbol: DerivationTree) ->Union[int, float]:
        if symbol in self.symbol2cost.keys():
            return self.symbol2cost[symbol]
        expansions = self.grammar[symbol]
        #self.seen = self.seen | {symbol}
        symbol_cost = float('inf')
        self.symbol2cost[symbol] = -1
        for expansion in expansions:
            symbols = nonterminals(expansion)
            if len(symbols) == 0:
                #self.symbol2cost[symbol] = 1
                expansion_cost = 1  # no nonterminal left
            elif any((s in self.seen) for s in symbols) and symbol not in symbols:
                #self.seen.discard(symbol)
                #self.symbol2cost[symbol] = float('inf')
                expansion_cost = float('inf')
                for s in symbols:
                    if s == symbol:
                        pass
                    elif s in self.seen:
                        pass
                    else:
                        self.seen = self.seen | {s}
                        expansion_cost += self.recursion_compute_cost(s)
                        self.seen.discard(s)
            else:
                expansion_cost = 0
                for s in symbols:
                    if s == symbol:
                        expansion_cost += self.symbol2cost[symbol]
                    else:
                        self.seen = self.seen | {s}
                        expansion_cost += self.recursion_compute_cost(s)
                        self.seen.discard(s)
                expansion_cost += 1
            symbol_cost = min(symbol_cost, expansion_cost)
        self.symbol2cost[symbol] = symbol_cost
        return symbol_cost

    def compute_cost(self) -> None:
        root = self.init_tree()
        print(root)
        (symbol, children) = root
        assert children is None
        #pdb.set_trace()
        self.seen = {symbol}  # start_symbol
        self.recursion_compute_cost(symbol)
        print("symbol2cost:", self.symbol2cost)
        self.seen.remove(symbol)
        return
    #'''
    def log_tree(self, tree: DerivationTree) -> None:
        """Output a tree if self.log is set; if self.display is also set, show the tree structure"""
        if self.log:
            print("Tree:", all_terminals(tree))
            if self.disp:
                display(display_tree(tree))
            # print(self.possible_expansions(tree), "possible expansion(s) left")

    ## 所以我们最终设计为3个phases：
    ## 先max cost expansion, 再random expansion，最后min cost expansion
    def expand_tree_with_strategy(self, tree: DerivationTree,
                                  expand_node_method: Callable,
                                  limit: Optional[int] = None):
        """Expand tree using `expand_node_method` as node expansion function
        until the number of possible expansions reaches `limit`."""
        self.expand_node = expand_node_method  # type: ignore
        while ((limit is None
                or self.possible_expansions(tree) < limit)
               and self.any_possible_expansions(tree)):
            tree = self.expand_tree_once(tree)
            self.log_tree(tree)
        return tree

    def expand_tree(self, tree: DerivationTree) -> DerivationTree:
        """
        Expand `tree` in a three-phase strategy until all expansions are complete.
        采用不同的stategy来在三个phase中expand tree，不断循环直到达到limit
        """
        self.log_tree(tree)
        tree = self.expand_tree_with_strategy(tree, self.expand_node_max_cost, self.min_nonterminals)
        tree = self.expand_tree_with_strategy(tree, self.expand_node_randomly, self.max_nonterminals)
        tree = self.expand_tree_with_strategy(tree, self.expand_node_min_cost)

        assert self.possible_expansions(tree) == 0

        return tree

    def fuzz_tree(self) -> DerivationTree:
        """Produce a derivation tree from the grammar."""
        tree = self.init_tree()
        # Expand all nonterminals
        tree = self.expand_tree(tree)  # 三个phase顺序拓展
        if self.log:
            print(repr(all_terminals(tree)))
        if self.disp:
            display(display_tree(tree))
        return tree

    def fuzz(self) -> str:
        """Produce a string from the grammar."""
        self.derivation_tree = self.fuzz_tree()
        return all_terminals(self.derivation_tree)

from scssGrammar import SCSS_GRAMMAR
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
# 试试50次trial
if __name__ == '__main__':
    trials = 50
    xs = []
    ys = []
    f = GrammarFuzzer(EXPR_GRAMMAR, max_nonterminals=20)
    for i in range(trials):
        with Timer() as t:
            s = f.fuzz()
        xs.append(len(s))
        ys.append(t.elapsed_time())
        print(i, end=" ")
    print()

    average_time = sum(ys) / trials
    print("Average time:", average_time)

    import matplotlib.pyplot as plt
    plt.scatter(xs, ys)
    plt.title('Time required for generating an output')
    # plt.show() # 显示一下图片
'''