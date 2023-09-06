from enum import Enum
from typing import Self
import shunting_yard as sy

from .token import *

class Function(Enum):
	Circuit = 0
	Ident = 1
	Hadamard = 2
	Phase = 3
	PauliX = 4
	PauliY = 5
	PauliZ = 6
	SPhase = 7
	TPhase = 8
	Measure = 9
	CNot = 10
	Swap = 11
	CZ = 12
	CPhase = 13
	Toffoli = 14
	CSwap = 15

	def __functions() -> list:
		return [ 
			"circuit", 
			"ident", "hadamard", "phase", "pauliX", "pauliY", "pauliZ", "sphase", "tphase", "measure",
			"cnot", "swap", "cz", "cphase",
			"toffoli", "cswap"
		]

	def from_token(token: Token) -> Self|None:
		if not isinstance(token, Identifier):
			return None

		try:
			func = Function(Function.__functions().index(token.content))
		except ValueError:
			return None
		else:
			return func
		
	def __str__(self) -> str:
		return Function.__functions()[self.value]

class Argument():
	def __init__(self, val):
		self.content = val

	def __str__(self) -> str:
		return str(self.content)

class NumericExpression():
	def __init__(self, parts: list):
		self.parts = parts

	def eval(self) -> float:
		parts = [ x.get() for x in self.parts ]
		expr = " ".join(parts)
		expr = expr.replace("π", "pi")
		return sy.compute(expr)

	def __repr__(self) -> str:
		return " ".join(self.parts)

class Instruction():
	def __init__(self, func: Function, args: list[Argument]):
		self.function = func
		self.args = args

class InstructionSpec():
	def __init__(self, args: tuple):
		self.args = args

class OneOf():
	def __init__(self, *args: type):
		self.variants = args

"""
This specifies the format (how many arguments, types of arguments) each function allows.
It is used by the parser to check whether the instructions that were parsed from the token
stream are semantically valid.
"""
instructions_specs: dict[Function, InstructionSpec|tuple[InstructionSpec]] = {
	Function.Circuit: (InstructionSpec(( ("n", IntegerLiteral) )), InstructionSpec(( ("*", (StringLiteral, IntegerLiteral)), ))),
	Function.Ident: InstructionSpec(( ("qubit", StringLiteral), )),
	Function.Hadamard: InstructionSpec(( ("qubit", StringLiteral), )),
	Function.PauliX: InstructionSpec(( ("qubit", StringLiteral), )),
	Function.PauliY: InstructionSpec(( ("qubit", StringLiteral), )),
	Function.PauliZ: InstructionSpec(( ("qubit", StringLiteral), )),
	Function.SPhase: InstructionSpec(( ("qubit", StringLiteral), )),
	Function.TPhase: InstructionSpec(( ("qubit", StringLiteral), )),
	Function.Measure: InstructionSpec(( ("qubit", StringLiteral), )),
	Function.Phase: InstructionSpec(( ("qubit", StringLiteral), ("angle", OneOf(NumericExpression, IntegerLiteral, FloatLiteral)) )),

	Function.CNot: InstructionSpec(( ("qubit0", StringLiteral), ("qubit1", StringLiteral) )),
	Function.Swap: InstructionSpec(( ("qubit0", StringLiteral), ("qubit1", StringLiteral) )),
	Function.CZ: InstructionSpec(( ("qubit0", StringLiteral), ("qubit1", StringLiteral) )),
	Function.CPhase: InstructionSpec(( ("qubit0", StringLiteral), ("qubit1", StringLiteral), ("angle", OneOf(NumericExpression, IntegerLiteral, FloatLiteral)) )),

	Function.Toffoli: InstructionSpec(( ("qubit0", StringLiteral), ("qubit1", StringLiteral), ("qubit2", StringLiteral) )),
	Function.CSwap: InstructionSpec(( ("qubit0", StringLiteral), ("qubit1", StringLiteral), ("qubit2", StringLiteral) )),
}