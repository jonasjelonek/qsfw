import argparse
import os
import warnings

from qsfw.scripting.interpreter import QSInterpreter

def run(args: argparse.Namespace):
	if not args.warning:
		warnings.filterwarnings("ignore")

	file_path = args.filepath
	if not os.path.isabs(file_path):
		file_path = f"{os.getcwd()}/{file_path}"

	if not os.path.exists(file_path):
		print(f"Cannot find or access file '{file_path}'")
		raise FileNotFoundError

	intptr = QSInterpreter(args.verbose)
	intptr.parse_file(file_path)
	qc = intptr.to_quantum_circuit()


	if args.stepping:
		i = 1
		while qc.next_step():
			print(f"Step {i}: ")
			qc.print_current_state()
			i += 1
	else:
		qc.calculate_all()
		qc.print_current_state()
	
	print("done.")

def main():
	parser = argparse.ArgumentParser(
		prog="qsfw",
		description="Quantum Simulation Framework"
	)

	parser.add_argument("-s", "--stepping", 
		help="Process step by step and print current quantum state after every step.",
		action="store_true"
	)
	parser.add_argument("-v", "--verbose",
		help="Print more messages/info, especially from parser, interpreter and other internals.",
		action="store_true"
	)
	parser.add_argument("-w", "--warning",
		help="Show warnings emitted by Python, possibly regarding calculations etc.",
		action="store_true"
	)
	parser.add_argument("filepath")

	args = parser.parse_args()
	run(args)
	return