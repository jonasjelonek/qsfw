from .token import *

class QSLexer():
	def __init__(self):
		pass

	def tokenize(self, content: str) -> list[Token]:
		tokens = []

		try:
			it = iter(content)
			c = it.__next__()
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
					c = it.__next__()
					while c != '\'':
						lit += c
						c = it.__next__()
					
					tokens.append(StringLiteral(lit))
				elif c == '"':													# String literal with double quotes
					lit = ''
					c = it.__next__()
					while c != '"':
						lit += c
						c = it.__next__()
					
					tokens.append(StringLiteral(lit))
				elif c.isnumeric() or c == 'π' or c == 'e':						# Float (including π and e) or Integer literal
					num_lit = c
					c = it.__next__()
					while c.isnumeric() or c == '.':
						num_lit += c
						c = it.__next__()

					keep_char = True
					if num_lit.isnumeric():
						tokens.append(IntegerLiteral(num_lit))
					else:
						tokens.append(FloatLiteral(num_lit))
				elif c == '/':													# Comments
					next = it.__next__()
					if next == '/': # comment until end of line
						c = it.__next__()
						while c != '\n':
							c = it.__next__()
					elif next == '*': # comment until */ is encountered
						c = it.__next__()
						next = it.__next__()
						while not (c == '*' and next == '/'):
							c = next
							next = it.__next__()
				elif c == "+":													# Addition operator
					tokens.append(PlusOperator())
				elif c == "-":													# Subtraction operator
					tokens.append(MinusOperator())
				elif c == "*":													# Multiplication operator
					tokens.append(MulOperator())
				elif c == "/":													# Divison operator
					tokens.append(DivOperator())
				elif c.isalpha():												# Identifiers
					ident = c
					c = it.__next__()
					while c.isalpha() or c == "_":
						ident += c
						c = it.__next__()

					keep_char = True
					tokens.append(Identifier(ident))
				# Whitespace will be skipped

				if not keep_char:
					c = it.__next__()
		except StopIteration:
			pass

		return tokens