from qsfw.scripting.common import BidirectionalIterator
from qsfw.scripting.lexer import *
from qsfw.scripting.instruction import *

class QSParser():

	def __init__(self) -> None:
		pass

	def __function_identifier(self, token: Token) -> Function:
		"""__function_identifier
		
		"""
		
		if not isinstance(token, Identifier):
			return False
		
		action = Function.from_token(token)
		if action == None:
			print(f"[parser] Unknown function '{token.content}")
			raise TypeError()
		
		return action

	def __expect_left_parent(self, token: Token):
		"""__expect_left_parent
		
		"""

		if not isinstance(token, LeftParent):
			print(f"[parser] Expected '(', got '{type(token)}'", sep=None)
			raise SyntaxError()
	
	def __left_parent(self, token: Token) -> bool:
		"""__left_parent
		
		"""

		return isinstance(token, LeftParent)
		
	def __expect_right_parent(self, token: Token):
		"""__expect_right_parent
		
		"""

		if not isinstance(token, RightParent):
			print(f"[parser] Expected ')', got '{type(token)}'", sep=None)
			raise SyntaxError()
		
	def __right_parent(self, token: Token) -> bool:
		"""__right_parent
		
		"""

		return isinstance(token, RightParent)
	
	def __expect_comma(self, token: Token):
		"""__expect_comma
		
		"""

		if not isinstance(token, Comma):
			print(f"[parser] Expected ',', got '{type(token)}'")
			raise SyntaxError()
		
	def __comma(self, token: Token) -> bool:
		"""__comma
		
		"""

		return isinstance(token, Comma)

	def __expect_instruction_separator(self, token: Token):
		"""__expect_instruction_separator
		
		Expects the given token to be an instruction separator/semicolon.
		If not, this function will raise a SyntaxError.
		"""
		
		if not isinstance(token, Semicolon):
			print(f"[parser] Expected ';', got '{type(token)}'")
			raise SyntaxError()
		
	def __string_literal(self, token: Token) -> bool:
		"""__string_literal
		
		"""

		return isinstance(token, StringLiteral)
	
	def __operator_as_literal(self, token: Token) -> bool:
		"""__operator_as_literal
		
		Checks whether the token is a '+' or '-' which are allowed to be
		used as value literals instead of '0' and '1'.
		"""

		return isinstance(token, (PlusOperator, MinusOperator))
	
	def __numeric_literal(self, token: Token) -> bool:
		"""__numeric_literal
		
		"""

		return isinstance(token, (FloatLiteral, IntegerLiteral))
		
	def __numeric_expr(self, token_it: BidirectionalIterator) -> list|None:
		"""__numeric_expr
		
		Although a FloatLiteral/IntegerLiteral is also a numeric expression,
		this function returns None in case there is only one valid token
		which is a literal. This way the caller can check for literals after
		this.
		"""

		token = token_it.current()
		parts = []

		if isinstance(token, (FloatLiteral, IntegerLiteral)):
			parts.append(token)
			token = token_it.next()
			while isinstance(token, (FloatLiteral, IntegerLiteral, MathOperator)):
				parts.append(token)
				token = token_it.next()
		else:
			return None

		if len(parts) == 1 and isinstance(parts[0], (FloatLiteral, IntegerLiteral)):
			# Here we have a literal detected as NumericExpression
			token_it.prev()
			return None
		else:
			token_it.prev()
			return NumericExpression(parts)

	# Only supports 2-tuple
	def __tuple(self, token_it: BidirectionalIterator) -> tuple|None:
		"""__tuple
		
		"""
		
		content = []

		if not self.__left_parent(token_it.current()):
			print(f"[parser] Expected left bracket for tuple but got '{type(token_it.current())}'")
			return None
		
		if self.__string_literal(token_it.next()) or self.__operator_as_literal(token_it.current()):
			part = token_it.current()
		else:
			part = self.__numeric_expr(token_it)
			if part == None:
				if self.__numeric_literal(token_it.current()):
					part = token_it.current()
				else:
					print(f"[parser] Expected string literal or numeric expression in tuple, got '{type(token_it.current())}'")
					raise SyntaxError()
		content.append(part)

		self.__expect_comma(token_it.next())

		if self.__string_literal(token_it.next()) or self.__operator_as_literal(token_it.current()):
			part = token_it.current()
		else:
			part = self.__numeric_expr(token_it)
			if part == None:
				if self.__numeric_literal(token_it.current()):
					part = token_it.current()
				else:
					print(f"[parser] Expected string literal or numeric expression in tuple, got '{type(token_it.current())}'")
					raise SyntaxError()
		content.append(part)

		self.__expect_right_parent(token_it.next())
		return tuple(content)

	def __function_argument(self, token_it: BidirectionalIterator) -> Argument|None:
		"""__function_argument
		
		"""

		token = token_it.next()
		
		if self.__string_literal(token) or self.__operator_as_literal(token_it.current()):
			return Argument(token)
		
		arg = self.__numeric_expr(token_it)
		if arg != None:
			return Argument(arg)
		
		if self.__numeric_literal(token):
			return Argument(token)

		arg = self.__tuple(token_it)
		if arg != None:
			return Argument(arg)
		
		print(f"[parser] Expected string literal, numeric expression or tuple, got '{type(token)}'")
		raise SyntaxError()

	def __instruction(self, token_it: BidirectionalIterator) -> Instruction|None:
		"""__instruction
		
		Tries to parse a valid instruction starting from the current position
		of the token stream.
		"""

		func = self.__function_identifier(token_it.next())
		self.__expect_left_parent(token_it.next())

		args = []
		while 1:
			arg = self.__function_argument(token_it)
			if arg == None:
				print(f"[parser] Expected argument, got '{type(token_it.current())}'")

			args.append(arg)

			if not isinstance(token_it.next(), Comma):
				break

		self.__expect_right_parent(token_it.current())
		self.__expect_instruction_separator(token_it.next())

		instr = Instruction(func, args)
		return instr

	def __check_instance_for_type(self, instance: any, ty: any) -> bool:
		if isinstance(ty, OneOf):
			target_types = list(ty.variants)
			for x in target_types.copy():
				target_types.append(type(x))
				
			target_types = tuple(target_types)
		elif isinstance(ty, tuple):
			target_types = tuple
		else:
			target_types = ty

		# In case of tuple, deeper check won't be performed!
		return isinstance(instance, target_types)

	def __check_instr_for_spec(self, instr: Instruction, spec: InstructionSpec):
		"""__check_instr_for_spec
		
		Checks if the given instruction corresponds to the given instruction
		specification.
		"""

		num_of_args = len(instr.args)
		func = instr.function

		if spec.args[0][0] == "*": # That's a special case which marks this as variadic
			if num_of_args < 1:
				return (
					SyntaxError(),
					f"'{str(func)}' requires at least {len(spec.args)} arguments but only {num_of_args} were given."
				)
			variadic = True
		else:
			if num_of_args != len(spec.args):
				return (
					SyntaxError(),
					f"'{str(func)}' accepts {len(spec.args)} arguments but {num_of_args} were given"
				)
			variadic = False
		
		j = 0
		for i in range(num_of_args):
			if not self.__check_instance_for_type(instr.args[i].content, spec.args[j][1]):
				return (
					TypeError(),
					f"'{str(func)}' expects {spec.args[j][1]} but got {type(instr.args[i].content)}."
				)
				
			if isinstance(spec.args[j][1], tuple):
				if len(spec.args[j][1]) != len(instr.args[i].content):
					return (
						TypeError(),
						f"'{str(func)}' expected tuple of length {len(spec.args[j][1])} but got {len(instr.args[i].content)} elements"
					)

				for k in range(len(spec.args[j][1])):
					if not self.__check_instance_for_type(instr.args[i].content[k], spec.args[j][1][k]):
						return (
							TypeError(),
							f"'{str(func)}' expected {spec.args[j][1][k]} as tuple element but got {type(instr.args[i].content[k])}."
						)
			
			if not variadic: # if variadic we have just one argument which can be specified multiple times
				j += 1
			
		return None

	def __check_instructions(self, instructions: list[Instruction]):
		"""__check_instructions
		
		Checks the parsed instructions whether the correct amount of arguments
		were supplied and the arguments have the expected types.
		"""
		
		for instr in instructions:
			func = instr.function
			spec: InstructionSpec|tuple[InstructionSpec] = instructions_specs[func]

			if isinstance(spec, tuple): # allows two InstructionSpec variants
				if self.__check_instr_for_spec(instr, spec[0]) != None:
					res = self.__check_instr_for_spec(instr, spec[1])
					if res != None:
						print(f"[parser] {res[1]}")
						raise res[0]
			else:
				res = self.__check_instr_for_spec(instr, spec)
				if res != None:
					print(f"[parser] {res[1]}")
					raise res[0]

	def parse(self, tokens: list[Token]):
		"""parse
		
		Parses a given list of tokens (that were generated by QSLexer before)
		into a valid sequence of instructions.
		"""
		
		token_it = BidirectionalIterator(tokens)
		instructions: list[Instruction] = []

		while token_it.peek() != None:
			instr = self.__instruction(token_it)
			if instr == None:
				print(f"[parser] Expected an instruction")
				raise SyntaxError()
			else:
				instructions.append(instr)

		self.__check_instructions(instructions)
		return instructions