import sys
import os
sys.path.append('../')
sys.path.append('../qsfw')

from qsfw.scripting.interpreter import QSInterpreter

script_path = os.path.dirname(__file__)

intptr = QSInterpreter(True)
intptr.parse_file(f"{script_path}/code.qs")
qc = intptr.to_quantum_circuit()

qc.list_gates()