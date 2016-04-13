class symbolTable:
	def __init__(self):
		self.name = "main"
		self.child = []
		self.parent = None
		self.symbol = {}
		self.level = 0
		self.offset = 0
		self.size = 4
		self.functionCallList=[]

	def lookup(self,identifier):
		for key,value in self.symbol.iteritems():
			if key == identifier:
				return (value,self.name,self.level)
		if self.parent:
			return self.parent.lookup(identifier)
		return None

	def insert(self,identifier,identifierType,param=[]):
		for key,value in self.symbol.iteritems():
			if key == identifier:
				value["identifierType"] = identifierType
				self.symbol[key] = value
				return
		newSymbolTableEntry = {}
		newSymbolTableEntry["identifierType"] = identifierType
		self.symbol[identifier] = newSymbolTableEntry
		if("identifierType"!= "undefined"):
			self.offset+=4
		if("identifierType"!= "function"):
			newSymbolTableEntry["param"] = param

	def insert_array(self,array,arrayType,size,list):
		for key,value in self.symbol.iteritems():
			if key == array:
				del self.symbol[key]
		newSymbolTableEntry = {}
		newSymbolTableEntry["identifierType"] = "array"
		self.symbol[array] = newSymbolTableEntry
		self.symbol[array]["offset"] = offset
		for i in range(0,size):
			self.symbol[array][i] = list[i]
		self.symobl[array]["size"] = size
		if("arrayType"!= "undefined"):
			self.offset+=4*size

	def newTable(self,scopeName,scopeType="function"):
		childSymbolTable = symbolTable()
		childSymbolTable.name = scopeName
		childSymbolTable.level = self.level + 1
		childSymbolTable.parent = self
		self.child.append(childSymbolTable)
		return childSymbolTable


