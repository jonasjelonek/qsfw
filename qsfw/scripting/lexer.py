from qsfw.scripting.common import BidirectionalIterator
from qsfw.scripting.token import *

class QSLexer():
	def __init__(self):
		pass

	def __tokenize_numeric_literal(self, it):
		num_lit = it.current()
		c = it.next()
		while c.isnumeric() or c == '.':
			num_lit += c
			c = it.next()

		if num_lit.isnumeric():
			return IntegerLiteral(num_lit)
		else:
			return FloatLiteral(num_lit)

	def tokenize(self, content: str) -> list[Token]:
		tokens = []

		try:
			it = BidirectionalIterator(content)
			c = it.next()
			while 1:
				keep_char = False

				if c == '(':													# Left round bracket / parentheses
					tokens.append(LeftParent())
				elif c == ')':													# Right round bracket / parentheses
					tokens.append(RightParent())
				elif c == ';':													# Semicolon
					tokens.append(Semicolon())
				elif c == ',':													# Comma
					tokens.append(Comma())
				elif c == '\'' or c == '"':										# String literal with single or double quotes
					terminator = c
					lit = ''
					c = it.next()
					while c != terminator:
						lit += c
						c = it.next()
					
					tokens.append(StringLiteral(lit))
				elif c == 'π' or (c == 'p' and it.peek() == 'i'):				# π or pi as float literal
					tokens.append(FloatLiteral('pi'))
					if c != 'π':
						it.next()
				elif c.isnumeric() or c == 'e':									# Float (including e) or Integer literal
					tokens.append(self.__tokenize_numeric_literal(it))
					keep_char = True
				elif c == '/':													# everything that may start with /
					next = it.next()
					if next == '/': 											# comment until end of line
						c = it.next()
						while c != '\n':
							c = it.next()
					elif next == '*': 											# comment until */ is encountered
						c = it.next()
						next = it.next()
						while not (c == '*' and next == '/'):
							c = next
							next = it.next()
					else:														# Divison operator
						tokens.append(DivOperator())
				elif c == "+":													# Addition operator
					tokens.append(PlusOperator())
				elif c == "-":													# Subtraction operator or negative value
					next_char = it.peek()
					if next_char.isnumeric():
						tokens.append(self.__tokenize_numeric_literal(it))
						keep_char = True
					elif next_char == 'π' or (next_char == 'p' and it.peek(2) == 'i'):
						tokens.append(FloatLiteral('-pi'))
						if next_char == 'π':
							it.advance_by(1)
						else:
							it.advance_by(2)
					else:
						tokens.append(MinusOperator())
				elif c == "*":													# Multiplication operator
					tokens.append(MulOperator())
				elif c.isalpha():												# Identifiers
					ident = c
					c = it.next()
					while c.isalpha() or c == "_":
						ident += c
						c = it.next()

					keep_char = True
					tokens.append(Identifier(ident))
				# Whitespace will be skipped

				if keep_char:
					# need to do this because __tokenize_numeric_literal modifies the iterator 
					c = it.current()
				else:
					c = it.next()
		except StopIteration:
			pass

		return tokens