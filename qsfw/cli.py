import argparse
import os
import warnings

from qsfw.scripting.interpreter import QSInterpreter

QSFW_VERSION = (1, 2, 0)

# OB - on black background | OW - on white background
ANSI_COLOR_YELLOW_OB = "\033[38;5;221;48;5;0m"
ANSI_COLOR_BLUE_OB = "\033[38;5;33;48;5;0m"
ANSI_COLOR_RED_OB = "\033[38;5;160;48;5;0m"
ANSI_COLOR_GREEN_OB = "\033[38;5;2;48;5;0m"
ANSI_COLOR_WHITE_OB = "\033[38;5;15;48;5;0m"
ANSI_COLOR_BLACK_OW = "\033[38;5;0;48;5;15m"

def print_version():
	print(f"qsfw (Quantum Simulation Framework)")
	print(f"Version {QSFW_VERSION[0]}.{QSFW_VERSION[1]}.{QSFW_VERSION[2]}")
	print("\nAuthor: Jonas Jelonek <jonas.jelonek@hs-nordhausen.de>")
	print("Copyright © 2023 Jonas Jelonek")

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

	print(
		ANSI_COLOR_GREEN_OB,
		"OUTPUT FORMAT:\nStep X/Final result:\n\t<partial state> :  <proportion of partial state to overall state>\n",
		ANSI_COLOR_WHITE_OB,
		sep = ""
	)
	qc.process_gates(args.stepping)
	
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
	parser.add_argument("-V", "--verbose",
		help="Print more messages/info, especially from parser, interpreter and other internals.",
		action="store_true"
	)
	parser.add_argument("-w", "--warning",
		help="Show warnings emitted by Python, possibly regarding calculations etc.",
		action="store_true"
	)
	parser.add_argument("-v", "--version",
		help="Print version information.",
		action=VersionAction,
		nargs = 0
	)
	parser.add_argument("filepath")

	args = parser.parse_args()
	run(args)
	return

class VersionAction(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		print_version()
		parser.exit()