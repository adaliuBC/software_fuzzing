from scss import Compiler
from Coverage import Coverage
import pdb

with open("try.txt", 'r') as f:
    scss = f.read()
'''
css = Compiler().compile_string(scss)
print(css)
'''
with Coverage() as cov:
    css = Compiler().compile_string(scss)
#pdb.set_trace()
trace = cov.trace()
coverage = cov.coverage()
print(coverage)
