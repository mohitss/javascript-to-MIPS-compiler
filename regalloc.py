import sys
class regalloc:
	def __init__(self):
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
				'$s5' : None, #Removed to be used in the functions
				'$s6' : None,
				'$s7' : None,
				}
		self.freeRegisters = [ reg for reg in self.Registers.keys() ] #Set all the registers to free
		self.variables = {}

	def getreg(self,variable):
		if variable in self.Registers.values():
			for key,value in self.Registers.iteritems():
				if value == variable:
					return (key,)
		elif len(self.freeRegisters) > 0:
			reg = self.freeRegisters[0]
			self.freeRegisters.remove(reg)
			self.registerInUse.append(reg)
			self.Registers[reg] = variable
			self.variables[variable] = reg
			code = "\tlw "+reg+","+variable
			return (reg,code)
		else:
			pass




