#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Code Coverage" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/Coverage.html
# Last change: 2022-02-09 08:18:28+01:00
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
The Fuzzing Book - Code Coverage
'''

from typing import Any, Optional, Callable, List, Type, Set, Tuple

def simplifyFname(fname):
    ind = fname.index("\\scss\\")
    return fname[ind+9:]

def foo():
    print(1)
    print(2)
    print(3)
    print(4)
    print(5)

## A CGI Decoder, target program
def cgi_decode(s: str) -> str:
    """Decode the CGI-encoded string `s`:
       * replace '+' by ' '
       * replace "%xx" by the character with hex number xx.
       Return the decoded string.  Raise `ValueError` for invalid inputs."""

    # Mapping of hex digits to their integer values
    hex_values = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    }

    foo()

    t = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c == '+':
            t += ' '
        elif c == '%':
            digit_high, digit_low = s[i + 1], s[i + 2]
            i += 2
            if digit_high in hex_values and digit_low in hex_values:
                v = hex_values[digit_high] * 16 + hex_values[digit_low]
                t += chr(v)
            else:
                raise ValueError("Invalid encoding")
        else:
            t += c
        i += 1
    return t


from types import FrameType, TracebackType

import sys
import inspect

## A Coverage Class
## ----------------

Location = Tuple[str, int]

class Coverage:
    """Track coverage within a `with` block. Use as
    ```
    with Coverage() as cov:
        function_to_be_traced()
    c = cov.coverage()
    ```
    """

    def __init__(self, fileList = None) -> None:
        """Constructor"""
        self._trace: List[Location] = []   # [(funcName, lineNo)]
        self.fileList = fileList

    # filename: frame.f_code.co_filename
    # lineno:frame.f_lineno
    # function name: frame.f_code.co_name
    # Trace function
    def traceit(self, frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
        """Tracing function. To be overloaded in subclasses."""
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        if event == "line":
            # print(frame, frame.f_code.co_filename)
            if frame.f_code.co_filename in self.fileList:
                function_name = frame.f_code.co_name
                lineno = frame.f_lineno
                file_name = frame.f_code.co_filename
                if function_name != '__exit__':  # avoid tracing ourselves:
                    self._trace.append((function_name, lineno, file_name))

        return self.traceit

    def __enter__(self) -> Any:
        """
        Start of `with` block. Turn on tracing. 在with块开头调用，开始trace
        """
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    def __exit__(self, exc_type: Type, exc_value: BaseException, 
                 tb: TracebackType) -> Optional[bool]:
        """End of `with` block. Turn off tracing. 在with块结尾调用，结束trace"""
        sys.settrace(self.original_trace_function)
        return None  # default: pass all exceptions

    def trace(self) -> List[Location]:
        """The list of executed lines, as (function_name, line_number) pairs"""
        return self._trace

    def coverage(self) -> Set[Location]:
        """The set of executed lines, as (function_name, line_number) pairs"""
        return set(self.trace())

    def function_names(self) -> Set[str]:
        """The set of function names seen"""
        return set(function_name for (function_name, line_number, file_name) in self.coverage())

    def __repr__(self) -> str:
        """Return a string representation of this object.
           Show covered (and uncovered) program code"""
        t = ""
        for function_name in self.function_names():
            # Similar code as in the example above
            try:
                fun = eval(function_name)
            except Exception as exc:
                t += f"Skipping {function_name}: {exc}"
                continue
            
            source_lines, start_line_number = inspect.getsourcelines(fun)
            for lineno in range(start_line_number, start_line_number + len(source_lines)):
                if (function_name, lineno) in self.trace():
                    t += "# "  # mark executed lines
                else:
                    t += "  "
                t += "%2d  " % lineno
                t += source_lines[lineno - start_line_number]

        return t



if __name__ == "__main__":
    with Coverage() as cov:
        cgi_decode("a+b")

    print(cov.coverage())
    print(cov)
    #trials = 100

##  Coverage of Basic Fuzzing
## --------------------------
from Fuzzer import fuzzer

def population_coverage(population: List[str], function: Callable) \
        -> Tuple[Set[Location], List[int]]:
    cumulative_coverage: List[int] = []
    all_coverage: Set[Location] = set()

    for s in population:
        with Coverage() as cov:
            try:
                function(s)
            except:
                pass
        all_coverage |= cov.coverage()
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage

def hundred_inputs() -> List[str]:
    population = []
    for i in range(trials):
        population.append(fuzzer())
    return population

# if __name__ == '__main__':
#     all_coverage, cumulative_coverage = \
#         population_coverage(hundred_inputs(), cgi_decode)

# %matplotlib inline

# if __name__ == '__main__':
#     import matplotlib.pyplot as plt  # type: ignore

# if __name__ == '__main__':
#     plt.plot(cumulative_coverage)
#     plt.title('Coverage of cgi_decode() with random inputs')
#     plt.xlabel('# of inputs')
#     plt.ylabel('lines covered')

# if __name__ == '__main__':
#     runs = 100

#     # Create an array with TRIALS elements, all zero
#     sum_coverage = [0] * trials

#     for run in range(runs):
#         all_coverage, coverage = population_coverage(hundred_inputs(), cgi_decode)
#         assert len(coverage) == trials
#         for i in range(trials):
#             sum_coverage[i] += coverage[i]

#     average_coverage = []
#     for i in range(trials):
#         average_coverage.append(sum_coverage[i] / runs)

# if __name__ == '__main__':
#     plt.plot(average_coverage)
#     plt.title('Average coverage of cgi_decode() with random inputs')
#     plt.xlabel('# of inputs')
#     plt.ylabel('lines covered')

## Finding Errors with Basic Fuzzing
## ---------------------------------
from ExpectError import ExpectError
from ClassDiagram import display_class_hierarchy
import os
import glob

def fixed_cgi_decode(s):
    """Decode the CGI-encoded string `s`:
       * replace "+" by " "
       * replace "%xx" by the character with hex number xx.
       Return the decoded string.  Raise `ValueError` for invalid inputs."""

    # Mapping of hex digits to their integer values
    hex_values = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    }

    t = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c == '+':
            t += ' '
        elif c == '%' and i + 2 < len(s):  # <--- *** FIX ***
            digit_high, digit_low = s[i + 1], s[i + 2]
            i += 2
            if digit_high in hex_values and digit_low in hex_values:
                v = hex_values[digit_high] * 16 + hex_values[digit_low]
                t += chr(v)
            else:
                raise ValueError("Invalid encoding")
        else:
            t += c
        i += 1
    return t

def branch_coverage(trace):
    coverage = set()
    past_line = None
    for line in trace:
        if past_line is not None:
            coverage.add((past_line, line))
        past_line = line

    return coverage


class BranchCoverage(Coverage):
    def coverage(self):
        """The set of executed line pairs"""
        coverage = set()
        past_line = None
        for line in self.trace():
            if past_line is not None:
                coverage.add((past_line, line))
            past_line = line

        return coverage

def population_branch_coverage(population, function):
    cumulative_coverage = []
    all_coverage = set()

    for s in population:
        with BranchCoverage() as cov:
            try:
                function(s)
            except Exception:
                pass
        all_coverage |= cov.coverage()
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage
