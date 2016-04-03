from symbolTable import *
class TAC:
	def __init__(self,filename):
		self.filename = filename
		self.tempCounter = 0
		self.labelCounter = 0

	def newTemp():
		name = "t_"+str(self.tempCounter)
		self.labelCounter += 1
		return name

	def newLabel():
		name = "Label_"+str(self.labelCounter)
		self.labelCounter += 1
		return name

	