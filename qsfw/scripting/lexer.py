from qsfw.scripting.common import BidirectionalIterator
from qsfw.scripting.token import *

class QSLexer():
	def __init__(self):
		pass

	def tokenize(self, content: str) -> list[Token]:
		tokens = []

		try:
			it = BidirectionalIterator(content)
			c = it.next()
			while 1: # Go char by char
				keep_char = False

				if c == '(':													# Left round bracket / parentheses
					tokens.append(LeftParent())
				elif c == ')':													# Right round bracket / parentheses
					tokens.append(RightParent())
				elif c == ';':													# Semicolon
					tokens.append(Semicolon())
				elif c == ',':													# Comma
					tokens.append(Comma())
				elif c == '\'':													# String literal with single quotes
					lit = ''
					c = it.next()
					while c != '\'':
						lit += c
						c = it.next()
					
					tokens.append(StringLiteral(lit))
				elif c == '"':													# String literal with double quotes
					lit = ''
					c = it.next()
					while c != '"':
						lit += c
						c = it.next()
					
					tokens.append(StringLiteral(lit))
				elif c == 'π' or (c == 'p' and it.peek() == 'i'):				# π or pi as float literal
					tokens.append(FloatLiteral('pi'))
					if c != 'π':
						it.next()
				elif c.isnumeric() or c == 'e':									# Float (including e) or Integer literal
					num_lit = c
					c = it.next()
					while c.isnumeric() or c == '.':
						num_lit += c
						c = it.next()

					keep_char = True
					if num_lit.isnumeric():
						tokens.append(IntegerLiteral(num_lit))
					else:
						tokens.append(FloatLiteral(num_lit))
				elif c == '/':
					next = it.next()
					if next == '/': # comment until end of line
						c = it.next()
						while c != '\n':
							c = it.next()
					elif next == '*': # comment until */ is encountered
						c = it.next()
						next = it.next()
						while not (c == '*' and next == '/'):
							c = next
							next = it.next()
					else:													# Divison operator
						tokens.append(DivOperator())
				elif c == "+":													# Addition operator
					tokens.append(PlusOperator())
				elif c == "-":													# Subtraction operator
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

				if not keep_char:
					c = it.next()
		except StopIteration:
			pass

		return tokens