import sys
sys.path.append('../')
sys.path.append('../qsfw')

from qsfw.circuitry.quantum_state import QuantumState
import qsfw.circuitry.quantum_gate as qgt

print("================ TEST 1 ================")
z = QuantumState((0, 0, 0, 1))
hgate = qgt.HGate()

print("Startzustand:")
z.print()

print("Erstes Mal Hadamard auf Qubit 1!")
z.apply_gate(hgate, ('1',))

print("Aktueller Zustand:")
z.print()

print("Zweites Mal Hadamard auf Qubit 1!")
z.apply_gate(hgate, ('1',))

print("Endzustand:")
z.print()

print("\n================ TEST 2 ================")
z = QuantumState((0, 1, 0, 1))
hgate = qgt.HGate()

print("Startzustand:")
z.print()

print("Erstes Mal Hadamard auf Qubit 1!")
z.apply_gate(hgate, ('1',))

print("Aktueller Zustand:")
z.print()

print("Zweites Mal Hadamard auf Qubit 1!")
z.apply_gate(hgate, ('1',))

print("Endzustand:")
z.print()

print("\n================ TEST 3 ================")

print("Aktuell nicht umsetzbar da keine überlagerten Anfangszustände angegeben werden können")

print("\n================ TEST 4 ================")
z = QuantumState((0, 1, 0, 1))
cnot = qgt.CNOTGate()

print("Startzustand:")
z.print()

print("CNOT auf Qubits 1 und 2, mit '1' als C-Qubit!")
z.apply_gate(cnot, ('1', '2'))

print("Aktueller Zustand:")
z.print()

print("Zweites Mal CNOT auf Qubit 1 und 2!")
z.apply_gate(cnot, ('1', '2'))

print("Endzustand:")
z.print()

print("\n================ TEST 5 ================")
z = QuantumState((0, 1, 0, 1))
cnot = qgt.CNOTGate()

print("Startzustand:")
z.print()

print("CNOT auf Qubits 1 und 2, mit '2' als C-Qubit!")
z.apply_gate(cnot, ('2', '1'))

print("Aktueller Zustand:")
z.print()

print("Zweites Mal CNOT auf Qubit 1 und 2!")
z.apply_gate(cnot, ('2', '1'))

print("Endzustand:")
z.print()

print("\n================ TEST 6 ================")
z = QuantumState((0, 1, 0, 1))
ccnot = qgt.ToffoliGate()

print("Startzustand:")
z.print()

print("CCNOT auf Qubits 0, 1, 3, mit 1 und 3 als C-Qubits!")
z.apply_gate(ccnot, ('1', '3', '0'))

print("Aktueller Zustand:")
z.print()

print("Zweites Mal CCNOT auf Qubit 0, 1 und 3!")
z.apply_gate(ccnot, ('1', '3', '0'))

print("Endzustand:")
z.print()