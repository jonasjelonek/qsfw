from qsfw.circuitry.quantum_state import QuantumState
import qsfw.circuitry.quantum_gate as qgt

z = QuantumState((0, 1))
hgate = qgt.HGate()
#cnot = qgt.CNOTGate()

print("Startzustand:")
z.print()

print("Erstes Mal Hadamard auf Qubit 0!")
z.apply_gate(hgate, ('0',))
#print("CNOT auf qubits '0' und '1', mit '1' als C-Qubit!")
#z.apply_gate(cnot, ('1', '0'))

print("Aktueller Zustand:")
z.print()

print("Zweites Mal Hadamard auf Qubit 0!")
z.apply_gate(hgate, ('0',))

print("Endzustand:")
z.print()