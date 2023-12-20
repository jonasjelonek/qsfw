class BidirectionalIterator(object):
	def __init__(self, collection):
		self.collection = collection
		self.index = -1

	def next(self):
		try:
			self.index += 1
			result = self.collection[self.index]
		except IndexError:
			raise StopIteration
		return result

	def prev(self):
		self.index -= 1
		if self.index < 0:
			raise StopIteration
		return self.collection[self.index]
	
	def current(self):
		if self.index < 0:
			return None

		return self.collection[self.index]
	
	def peek(self, n=1):
		if (self.index + n) >= len(self.collection):
			return None
		
		return self.collection[self.index + n]
	
	def advance_by(self, n):
		if (self.index + n) >= len(self.collection):
			return None
		
		self.index += n

	def __iter__(self):
		return self