import numpy as np
import math
import cmath

W2INV = 1/np.sqrt(2)
IMAG = 0.+1j
IMAG_NEG = 0.-1j

"""
Abstrakte Klassen für Qubit-Gates
"""

class QGate:
	def do_something(self):
		pass

	def targeted_qubits(self) -> int:
		return 0

class Q1Gate(QGate):
	def __init__(self):
		self.matrix = np.ndarray(shape = (2,2), dtype = complex)

	def targeted_qubits(self) -> int:
		return 1

	def do_something(self):
		pass

class Q2Gate(QGate):
	def __init__(self):
		self.matrix = np.ndarray(shape = (4,4), dtype = complex)

	def targeted_qubits(self) -> int:
		return 2

	def do_something(self):
		pass

class Q3Gate(QGate):
	def __init__(self):
		self.matrix = np.ndarray(shape = (8,8), dtype = complex)

	def targeted_qubits(self) -> int:
		return 3

	def do_something(self):
		pass

"""
Klassen/Implementierungen spezifischer Gates
"""

# #############################################################################
# #### 1-Qubit-Gates ##########################################################
# #############################################################################

class IdentityGate(Q1Gate):
	def __init__(self):
		Q1Gate.__init__(self)
		self.matrix[0,0] = 1
		self.matrix[0,1] = self.matrix[1,0] = 0
		self.matrix[1,1] = 1

class HGate(Q1Gate):
	def __init__(self):
		Q1Gate.__init__(self)
		self.matrix[0,0] = self.matrix[0,1] = self.matrix[1,0] = W2INV
		self.matrix[1,1] = -W2INV

class PauliXGate(Q1Gate):
	def __init__(self):
		Q1Gate.__init__(self)
		self.matrix[0,0] = self.matrix[1,1] = 0
		self.matrix[0,1] = self.matrix[1,0] = 1

class PauliYGate(Q1Gate):
	def __init__(self):
		Q1Gate.__init__(self)
		self.matrix[0,0] = self.matrix[1,1] = 0
		self.matrix[0,1] = IMAG_NEG
		self.matrix[1,0] = IMAG

class PauliZGate(Q1Gate):
	def __init__(self):
		Q1Gate.__init__(self)
		self.matrix[0,0] = 1
		self.matrix[1,1] = -1
		self.matrix[0,1] = self.matrix[1,0] = 0

class PhaseGate(Q1Gate):
	def __init__(self, angle: float):
		Q1Gate.__init__(self)
		self.matrix[0,0] = 1
		self.matrix[0,1] = self.matrix[1,0] = 0
		self.matrix[1,1] = cmath.exp(IMAG * angle)

class SPhaseGate(Q1Gate):
	def __init__(self):
		Q1Gate.__init__(self)
		self.matrix[0,0] = 1
		self.matrix[0,1] = self.matrix[1,0] = 0
		self.matrix[1,1] = IMAG

class TPhaseGate(Q1Gate):
	def __init__(self):
		Q1Gate.__init__(self)
		self.matrix[0,0] = 1
		self.matrix[0,1] = self.matrix[1,0] = 0
		self.matrix[1,1] = cmath.exp(IMAG * math.pi / 4)

class Measurement(Q1Gate): # Spezielles 1-Qubit Gate
	def do_something(self):
		# Zustand, der bei der Messung rauskommt, 'würfeln'
		# Entsprechend des 'Würfelns' eine Matrix festlegen, die dann
		# den resultierenden Zustand 'produziert'
		pass

# #############################################################################
# #### 2-Qubit-Gates ##########################################################
# #############################################################################

class CNOTGate(Q2Gate):
	def __init__(self):
		Q2Gate.__init__(self)
		self.matrix[0,0] = self.matrix[1,1] = self.matrix[2,3] = self.matrix[3,2] = 1

class SwapGate(Q2Gate):
	def __init__(self):
		Q2Gate.__init__(self)
		self.matrix[0,0] = self.matrix[1,2] = self.matrix[2,1] = self.matrix[3,3] = 1

class CZGate(Q2Gate):
	def __init__(self):
		Q2Gate.__init__(self)
		self.matrix[0,0] = self.matrix[1,1] = self.matrix[2,2] = 1
		self.matrix[3,3] = -1
		# Rest ist 0

class CPhaseGate(Q2Gate):
	def __init__(self, angle: float):
		Q2Gate.__init__(self)
		self.matrix[0,0] = self.matrix[1,1] = self.matrix[2,2] = 1
		self.matrix[3,3] = cmath.exp(IMAG * angle)
		# Rest ist 0

# #############################################################################
# #### 3-Qubit-Gates ##########################################################
# #############################################################################

class ToffoliGate(Q3Gate):
	def __init__(self):
		Q3Gate.__init__(self)
		self.matrix[0,0] = self.matrix[1,1] = self.matrix[2,2] = \
			self.matrix[3,3] = self.matrix[4,4] = self.matrix[5,5] = \
			self.matrix[6,7] = self.matrix[7,6] = 1
		
class CSwapGate(Q3Gate): # Controlled Swap
	def __init__(self):
		Q3Gate.__init__(self)
		self.matrix[0,0] = self.matrix[1,1] = self.matrix[2,2] = \
			self.matrix[3,3] = self.matrix[4,4] = self.matrix[5,6] = \
			self.matrix[6,5] = self.matrix[7,7] = 1
