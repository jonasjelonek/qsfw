import sys
import os
sys.path.append('../')
sys.path.append('../qsfw')

from qsfw.scripting.lexer import *
from qsfw.scripting.parser import QSParser

script_path = os.path.dirname(__file__)

l = QSLexer()
f = open(f"{script_path}/code.qs")
code = f.read()

toks = l.tokenize(code)
print(toks)

for t in toks:
    print(type(t))
exit()

p = QSParser()
instructions = p.parse(toks)
#print(instructions)
for i, instr in enumerate(instructions):
    arg = ", ".join([str(x) for x in instr.args])
    print("(", i, ")\t", str(instr.action), "(", arg, ")", sep=None)