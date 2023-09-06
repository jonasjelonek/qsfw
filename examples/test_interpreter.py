from qsfw.scripting.interpreter import QSInterpreter

intptr = QSInterpreter(True)
intptr.parse_file("examples/code.qs")
qc = intptr.to_quantum_circuit()

qc.list_gates()