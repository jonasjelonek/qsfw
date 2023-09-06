class Token():
	def get(self):
		return self.content

class LeftParent(Token):
	def get(self):
		return '('
	
	def __repr__(self) -> str:
		return '\'(\''
class RightParent(Token):
	def get(self):
		return ')'

	def __repr__(self) -> str:
		return '\')\''
class StringLiteral(Token):
	def __init__(self, s: str):
		self.content = s

	def get(self):
		return self.content
	
	def __repr__(self) -> str:
		return '\'' + self.content + '\''
class FloatLiteral(Token):
	def __init__(self, s: str):
		self.content = s

	def get(self):
		return self.content
	
	def __repr__(self) -> str:
		return self.content
class IntegerLiteral(Token):
	def __init__(self, s: str):
		self.content = s

	def get(self):
		return self.content
	
	def __repr__(self) -> str:
		return self.content
class MathOperator(Token):
	def __init__(self, op: str):
		self.content = op

	def get(self):
		return self.content

	def __repr__(self) -> str:
		return '\'' + self.content + '\''
class Identifier(Token):
	def __init__(self, id: str):
		self.content = id

	def get(self):
		return self.content

	def __repr__(self) -> str:
		return '<' + self.content + '>'
class Semicolon(Token):
	def get(self):
		return ';'

	def __repr__(self) -> str:
		return '\';\''
class Comma(Token):
	def get(self):
		return ','
	
	def __repr__(self) -> str:
		return '\',\''