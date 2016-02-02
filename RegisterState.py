class RegisterState:
	def __init__(self, SymbolTable, ThreeAddressCode):
        self.assemblyCode = {}
        self.TAC = ThreeAddressCode
        self.ST = SymbolTable
        self.RegisterReset()

    def appendCode(self, line):
        self.assemblyCode.append(line)

    def RegisterReset(self):
        self.registerInUse = []                                       #Reg in use is empty
    	self.Registers = {
                '$t0' : None,   #Caller-Saved Registers
                '$t1' : None,
                '$t2' : None,
                '$t3' : None,
                '$t4' : None,
                '$t5' : None,
                '$t6' : None,
                '$t7' : None,
                '$s0' : None,   #Callee Saved Registers
                '$s1' : None,
                '$s2' : None,
                '$s3' : None,
                '$s4' : None, 
                # '$s5' : None, #Removed to be used in the functions
                # '$s6' : None,
                # '$s7' : None,
                }
        self.freeRegisters = [ reg for reg in self.Registers.keys() ] #Set all the registers to free
        
    def LoadAddress(self, variable):
        (level, offset) = self.ST.Address[variable]['memory']
        self.appendCode(['li', '$s6', 4*level, ''])
        self.appendCode(['la', '$s5', 'arrayReg', ''])          
        self.appendCode(['add', '$s7', '$s5', '$s6'])    

        self.appendCode(['li', '$s6', 4*offset, ''])       
        self.appendCode(['lw', '$s5', '0($s7)', ''])      
        self.appendCode(['add', '$s7', '$s5', '$s6'])     

    def getReg(self, variable):
        # If the variable is already there in one of the registers then we return the register
        if variable in self.Registers.values():
            reg = self.ST.Address[variable]['register']
            return reg
        elif len(self.freeReg) != 0:
            reg = self.freeReg.pop(-1)
            #Check out if the value is present in memory
            if self.ST.Address[variable]['memory'] != None and self.ST.Address[variable]['store']:
                # Get the value of level and offset
                LoadAddress(level, offset, variable)
                self.appendCode(['lw', reg,'0($s7)', ''])
            self.ST.Address[variable]['register'] = reg
            self.regInUse.append(reg)       
        else:
            reg = self.regInUse.pop(0)
            tempVar = self.Register[reg]
            self.Register[reg] = variable
            if self.ST.Address[tempVar]['memory'] != None:
                LoadAddress(level, offset, tempVar)
                self.appendCode(['sw', reg, '0($s7)', ''])    
                self.ST.Address[tempVar]['store'] = True
            if self.ST.Address[variable]['memory'] != None:
                LoadAddress(level, offset, variable)
                self.appendCode(['lw', reg, '0($s7)', ''])
            self.ST.Address[tempVar]['register'] = None
            self.ST.Address[variable]['register'] = reg  
            self.regInUse.append(reg)      

        self.Register[reg] = variable
        return reg