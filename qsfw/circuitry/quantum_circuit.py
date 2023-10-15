from __future__ import annotations

import numpy as np
from collections import deque

from .quantum_gate import *
from .quantum_state import *

class QuantumCircuit():
	
	def __init__(self, qubits: int | dict[str,int]):
		"""__init__
		
		qubits:
		- either an integer denoting the number of qubits that the
			QuantumCircuit should have. Each qubit will receive an ascending
			string ID starting from '0' and will have the initial state '0'.
		- or a dictionary with a self-chosen ID as key and the initial state
			as value. The key must be string, the value can be either integer
			for states 0 and 1, or string for states '+' and '-'.
		"""

		self.gates = deque()
		"""
		List of gates that will be applied to the qubits of this QuantumCircuit.

		Every element in this list is a 2-tuple (gate, qubits).
		The tuple element 'gate' contains an instance of a gate object. The gate
		object defines the effect of an operation on one or more qubits.
		The tuple element 'qubits' an n-Tupel with (n0: str, n1: str, ...). This
		tuple specifies on which qubits the gate should be applied.
		"""

		# Initialise quantum state
		if isinstance(qubits, int):
			values = [0 for _ in range(qubits)]
			self.quantum_state = QuantumState(values)
		elif isinstance(qubits, dict):
			for q in qubits.values():
				assert q == '+' or q == '-' or 0 <= int(q) <= 1
			
			self.quantum_state = QuantumState(qubits)
		else:
			print(f"Expected int or dict, got {type(qubits)}")
			raise TypeError

	def add_gate(self, gate: QGate, qubits: tuple[str]):
		if isinstance(gate, Q2Gate):
			assert len(qubits) == 2
		elif isinstance(gate, Q3Gate):
			assert len(qubits) == 3
		else:
			assert len(qubits) == 1

		self.gates.append((gate, qubits))

	# 1-Qubit-Gate shortcuts

	def add_identity_gate(self, qubit: str):
		self.add_gate(IdentityGate(), (qubit))
	def add_hadamard_gate(self, qubit: str):
		self.add_gate(HGate(), (qubit))
	def add_pauliX_gate(self, qubit: str):
		self.add_gate(PauliXGate(), (qubit))
	def add_pauliY_gate(self, qubit: str):
		self.add_gate(PauliYGate(), (qubit))
	def add_pauliZ_gate(self, qubit: str):
		self.add_gate(PauliZGate(), (qubit))
	def add_phase_gate(self, qubit: str, angle: float):
		self.add_gate(PhaseGate(angle), (qubit))
	def add_sphase_gate(self, qubit: str):
		self.add_gate(SPhaseGate(), (qubit))
	def add_tphase_gate(self, qubit: str):
		self.add_gate(TPhaseGate(), (qubit))
	def add_measurement_gate(self, qubit):
		self.add_gate(Measurement(), (qubit))

	# 2-Qubit-Gate shortcuts

	def add_cnot_gate(self, qubit0: str, qubit1: str):
		self.add_gate(CNOTGate(), (qubit0, qubit1))
	def add_swap_gate(self, qubit0: str, qubit1: str):
		self.add_gate(SwapGate(), (qubit0, qubit1))
	def add_cz_gate(self, qubit0: str, qubit1: str):
		self.add_gate(CZGate(), (qubit0, qubit1))
	def add_cphase_gate(self, qubit0: str, qubit1: str, angle: float):
		self.add_gate(CPhaseGate(angle), (qubit0, qubit1))

	# 3-Qubit-Gate shortcuts

	def add_toffoli_gate(self, qubit0: str, qubit1: str, qubit2: str):
		self.add_gate(ToffoliGate(), (qubit0, qubit1, qubit2))
	def add_cswap_gate(self, qubit0: str, qubit1: str, qubit2: str):
		self.add_gate(CSwapGate(), (qubit0, qubit1, qubit2))

	# other methods

	def list_gates(self):
		for gate in self.gates:
			print(f"{type(gate[0])} on '{gate[1]}'")

	def calculate_all(self) -> bool:
		try:
			while 1:
				# This raises an exception when there is no element left
				(gate, qubits) = self.gates.popleft()
				self.quantum_state.apply_gate(gate, qubits)
		except IndexError:
			pass

		return True

	def next_step(self) -> bool:
		try:
			(gate, qubits) = self.gates.popleft()
			self.quantum_state.apply_gate(gate, qubits)
		except IndexError:
			return False
		else:
			return True

	def print_current_state(self):
		self.quantum_state.print()