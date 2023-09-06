from qsfw.scripting.lexer import *
from qsfw.scripting.parser import QSParser

l = QSLexer()
#code = "circuit(('a', 4 * π), ('b', 3 * e), ('c', 2));"
f = open("examples/code.qs")
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