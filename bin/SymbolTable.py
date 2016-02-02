class SymbolTable:
	def __init__(self):
		self.symbolTable = { 'main' : {
									'scope': 'main',
									'level': '0',
									'offset': '0',
									'parent': 'main'
									'type' : 'function'
								}
							}
		self.Address = {}
		#Stacks for the offset and scope for the current function
		self.offset = 0
		self.scope = ['main']
		self.temp = 0

	def createTemp(self, variable = '', memlocation = '', loadFromMemory = False):
		tempReg = $t+str(self.temp)
		self.temp += 1
		self.Address[tempReg] = {'memory' : memlocation, 'register': '', 'store': loadFromMemory, 'dirty': False, 'variable' = variable}
		return tempReg
