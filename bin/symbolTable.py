class symbolTable:
	def __init__(self):
		self.name = "main"
		self.child = []
		self.parent = None
		self.symbol = {}
		self.level = 0

	def lookup(self,identifier):
		for key,value in self.symbol.iteritems():
			if key == identifier:
				return (value,self.name,self.level)
		if self.parent:
			return self.parent.lookup(identifier)
		return None

	def insert(self,identifier,identifierType):
		for key,value in self.symbol.iteritems():
			if key == identifier:
				value["identifierType"] = identifierType
				self.symbol[key] = value
				return
		newSymbolTableEntry = {}
		newSymbolTableEntry["identifierType"] = identifierType
		self.symbol[identifier] = newSymbolTableEntry

	def newTable(self,scopeName,scopeType="function"):
		childSymbolTable = symbolTable()
		childSymbolTable.name = scopeName
		childSymbolTable.level = self.level + 1
		childSymbolTable.parent = self
		self.child.append(childSymbolTable)
		return childSymbolTable


