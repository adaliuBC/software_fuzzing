# software_fuzzing

use a DFS to get costs: 提升了效率

修改了不靠谱的grammar（content必须在@mixin里面）

grammar并没有用，因为不是生成式的，根据那个去生成会发现奇怪的东西，比如生成出两端类型不一样的加法表达式



TODO：给for语句设计一个for block直接替换掉里面的$i



we use statement coverage as measurement





### Introduction & background:

对pyscss进行了测试



### Method：

translate grammar to fuzzer n text book

target program：PyScss

Fuzzer：Mutation Fuzzer, Grammar Fuzzer, Prob Grammar Fuzzer

对比coverage

对比



Future work:

拓展到coverage based的fuzzing

完善Grammar的@import 和@include

