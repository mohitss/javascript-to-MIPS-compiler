class A:
	def __init__(self):
		self.t = 1

	def create(self,child):
		b = A()
		b.t = 100
		return b