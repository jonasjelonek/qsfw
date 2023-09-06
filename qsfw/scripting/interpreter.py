from .lexer import *
from .parser import *
import qsfw.circuitry.quantum_circuit as qcct

class QSInterpreter():
	def __init__(self, verbose: bool = False):
		self.instructions = []
		self.__parsed = False
		self.__verbose = verbose

	def parse_file(self, path: str):
		# Read source code from file
		src_file = open(path)
		src_content = src_file.read()
		if self.__verbose:
			print(f"[interpreter] Read source code from file '{path}'")

		# Init lexer and let it tokenize the source code
		if self.__verbose:
			print(f"[interpreter] Performing lexical analysis on source code")
		lexer = QSLexer()
		self.token_stream = lexer.tokenize(src_content)
		if self.__verbose:
			print(f"[interpreter] Converted source code into token stream")

		# Now pass the token stream to the parser to produce
		# valid instructions from the tokens
		if self.__verbose:
			print(f"[interpreter] Parsing token stream")
		parser = QSParser()

		self.instructions = parser.parse(self.token_stream)
		self.__parsed = True
		if self.__verbose:
			print(f"[interpreter] Successfully parsed instructions from token stream")

	def to_python_code(self) -> list[str]:
		pass

	def to_quantum_circuit(self) -> qcct.QuantumCircuit:
		# first instruction must be 'circuit'
		if self.instructions[0].function != Function.Circuit:
			print("[interpreter] First instruction must be a 'circuit' instruction!")
			raise RuntimeError()
		
		circuit_args = self.instructions[0].args
		if isinstance(circuit_args[0].content, IntegerLiteral):
			num = int(circuit_args[0].content.get())
			qc = qcct.QuantumCircuit(num)
		else:
			arg_dict = dict()
			for arg in circuit_args:
				key = arg.content[0]
				val = int(arg.content[1].get())
				arg_dict[key] = val
			
			qc = qcct.QuantumCircuit(arg_dict)

		# Now process the remaining instructions
		for i in range(1, len(self.instructions)):
			instr = self.instructions[i]
			args = instr.args
			match instr.function:
				case Function.Circuit:
					print("[interpreter] Only one 'circuit' instruction is allowed")
					raise RuntimeError
				case Function.Ident:
					qc.add_identity_gate(args[0].content.get())
				case Function.Hadamard:
					qc.add_hadamard_gate(args[0].content.get())
				case Function.PauliX:
					qc.add_pauliX_gate(args[0].content.get())
				case Function.PauliY:
					qc.add_pauliY_gate(args[0].content.get())
				case Function.PauliZ:
					qc.add_pauliZ_gate(args[0].content.get())
				case Function.SPhase:
					qc.add_sphase_gate(args[0].content.get())
				case Function.TPhase:
					qc.add_tphase_gate(args[0].content.get())
				case Function.Measure:
					qc.add_measurement_gate(args[0].content.get())
				case Function.Phase:
					qc.add_phase_gate(
						args[0].content.get(),
						args[1].content.eval()		# This must be a NumericExpression which has an eval method
					)
				case Function.CNot:
					qc.add_cnot_gate(
						args[0].content.get(),
						args[1].content.get()
					)
				case Function.Swap:
					qc.add_swap_gate(
						args[0].content.get(),
						args[1].content.get()
					)
				case Function.CZ:
					qc.add_cz_gate(
						args[0].content.get(),
						args[1].content.get()
					)
				case Function.CPhase:
					qc.add_cphase_gate(
						args[0].content.get(),
						args[1].content.get(),
						args[2].content.eval()		# This must be a NumericExpression which has an eval method
					)
				case Function.Toffoli:
					qc.add_toffoli_gate(
						args[0].content.get(),
						args[1].content.get(),
						args[2].content.get()
					)
				case Function.CSwap:
					qc.add_cswap_gate(
						args[0].content.get(),
						args[1].content.get(),
						args[2].content.get()
					)

		return qc
