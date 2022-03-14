# Software Fuzzing

Please note that the Fuzzer code and Coverage code are derived from the Fuzzing Book. My work is mainly included in `htmlFuzzer_bs4.py`, `htmlFuzzer_parser.py`, `scssFuzzer.py`, `htmlGrammar.py`, `scssGrammar.py`, `splitGrammar.py`(unfinished, trying to split up the SCSS grammar and test each part of it, explained in the report), `operation.py`, `dataProcessing.py` and `computeDiff.py`. I also modify the following files from the original repository of the Fuzzing Book: `Coverage.py`, `MutationFuzzer.py` `GrammarFuzzer.py`, `GeneratorGrammarFuzzer.py`. 



### Usage

```
> python <fuzzertest>.py <fuzzerMode>
```

fuzzertest = [htmlFuzzer_bs4, htmlFuzzer_parser, scssFuzzer]

fuzzerMode = [RandomFuzzer, MutationFuzzer, GrammarFuzzer]
