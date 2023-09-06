import argparse

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
	parser.add_argument("filename")

	args = parser.parse_args()