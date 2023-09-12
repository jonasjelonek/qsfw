import itertools
import numpy as np

import qsfw.circuitry.quantum_gate as gt

class QuantumState():
	"""
	A class to present a quantum state.

	Attributes
	----------
	components : dict
		Keep the base states/partial states with their shares.
	qubits_id : dict
		Keeps a mapping from qubit IDs to indices within a state tuple. Users
		of this class need to use string-based IDs but those are mapped
		internally to another representation.
	"""

	# Convention: Index 0 corresponds to the first qubit in the ket,
	# 				i.e. |0000...0>
	#					  ^ (index 0)

	#def __init__(self, values: tuple[int]|dict[str, int|str]):
	def __init__(self, values):
		self.qubits_id = dict()
		"""
		Keeps a mapping from qubit IDs to indices within a state tuple. Users
		of this class need to use string-based IDs but those are mapped
		internally to another representation.
		"""

		self.init_state = []
		"""
		
		"""

		if isinstance(values, tuple):
			for (i, q) in enumerate(values):		# we assigned generated IDs
				if q == '+' or q == '-':
					print("TODO")
					raise NotImplementedError
				
				self.qubits_id[str(i)] = i
				self.init_state.append(q)
		else:
			# Here we get a dict with string IDs as keys and the initial states as values
			for (i, q) in enumerate(values.keys()):
				if values[q] == '+' or values[q] == '-':
					print("TODO")
					raise NotImplementedError

				self.qubits_id[q] = i
				self.init_state.append(values[q])

		self.components = dict()
		"""
		Keep the base states/partial states with their shares.
		"""

		# The following code would fill the dictionary with all partial states
		# and a default share of 0.0. This is not required for us but could be
		# beneficial to understand that all better.
		#if len(values) == 1:
		#	self.components[(1,0)] = 0.0
		#	self.components[(0,1)] = 0.0
		#else:
		#	base_states = [*itertools.product([0, 1], repeat=len(values))]
		#	for b in base_states:
		#		self.components[tuple(b)] = 0.0

		# The share of the initial state is set to 1.0.
		self.components[tuple(self.init_state)] = 1.0+0j

	def print(self):
		for state in self.components.keys():
			s = '\t|'
			for i in range(len(state)):
				s += str(state[i])
			s += '>'

			print(s, ': ', str(self.components[state]), sep=None)

	def is_valid_id(self, id: str) -> bool:
		return (id in self.qubits_id.keys())

	def apply_gate(self, gate: gt.QGate, target_qubits: tuple):
		# Gate and number of affected qubits must match!
		assert len(target_qubits) == gate.targeted_qubits()

		qubits_idx = []
		for q in target_qubits:
			qubits_idx.append(self.qubits_id[q])

		qubits_idx = tuple(qubits_idx)

		# Step to apply gate to quantum state:
		# 	- find out which partial states are affected by the operation
		# 	- construct a vector from the shares of the affected states
		# 	- do matrix multiplication of that vector with gate matrix
		# 	- write back the adjusted shares to our state dictionary
		components_copy = self.components.copy()
		already_processed = []
		for c_key in components_copy.keys():
			if c_key in already_processed or components_copy[c_key] == 0.0+0j:
				continue
			
			# The 'affected' list can now also contain partial states that
			# do not exist in our 'components' dict yet. For those we just
			# create new entries with a share of 0+0j
			affected = self.__affected_states(c_key, qubits_idx)
			for e in affected:
				if e not in components_copy.keys():
					self.components[e] = 0.0+0j

			# The order of the target qubits should not matter here. For example,
			# one can say to use qubit '1' as control qubit and qubit '0' as
			# controlled qubit for a CNOT operation. For such an operation the
			# first qubit is always the controlling qubit and this qubit will
			# be the 'most significant' in the order of the list/vector.
			comp_vec = []
			for e in affected:
				comp_vec.append(self.components[e])
				already_processed.append(e)

			comp_vec = np.array(comp_vec)
			# Matrix of the gate adjusts the shares by simply matrix multiplication
			result = gate.matrix @ comp_vec		# operator for matrix multiplication (Python 3.5+)

			# Write back the adjusted shares to our partial states
			for i in range(len(result)):
				self.components[affected[i]] = result[i]

		# Cleanup, i.e. order the dict by keys and remove entries with a share of 0+0j
		self.__cleanup_components()

	def __affected_states(self, state: tuple, qubits: tuple):
		affected = []
		state_l = list(state)

		if len(qubits) == 1:
			for i in range(2):
				state_l[qubits[0]] = i
				affected.append(tuple(state_l))
		else:
			mod_state = list(state)
			mod_qubits = list(qubits)
			mod_qubits.pop(0)

			for i in range(2):
				mod_state[qubits[0]] = i
				affected.extend(self.__affected_states(tuple(mod_state), tuple(mod_qubits)))

		return affected
	
	def __cleanup_components(self):
		for c_key in self.components.copy().keys():
			if abs(self.components[c_key]) < 1e-10+0j:
				self.components[c_key] = 0.0+0j
			elif 1.0+0j - self.components[c_key] < 1e-10+0j:
				self.components[c_key] = 1.0+0j

			# Remove all entries that have a share of ~0.0
			if self.components[c_key] == 0.0+0j:
				del self.components[c_key]

		self.components = dict(sorted(self.components.items()))