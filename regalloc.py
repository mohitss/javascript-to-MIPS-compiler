import sys
import codegen
import operator
dictionary={}
current_basic_block=1
filename=""

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

	def next_use(self,LINE_NO):
		f=open(filename)
		lines=f.readlines()
		local_dict={}
		start=LINE_NO-1
		end=codegen.dictionary[codegen.current_basic_block]['end']-1
		while(start=<end):
			line = line[end].strip()
			tac = line.split(",")
			if( tac[0] == "+"or tac[0] == "-" or tac[0] == "*" or tac[0] == "/" or tac[0] == "%" or tac[0] == "<<" or tac[0] == ">>"  or tac[0] == "^" or tac[0] == "|" or tac[0] == "&"):
				local_dict.update({tac[1]:-1})
				local_dict.update({tac[2]:end})
				local_dict.update({tac[3]:end})

			elif(tac[0]=="=" ):
				local_dict.update({tac[1]:-1})
				local_dict.update({tac[2]:end})
			elif(tac[0] == "ifgoto"  ):
				local_dict.update({tac[2]:end})
				local_dict.update({tac[3]:end})
			elif(tac[0]=="array"):

			end=end-1
		line = line[start].strip()
		tac = line.split(",")
		if( tac[0] == "+"or tac[0] == "-" or tac[0] == "*" or tac[0] == "/" or tac[0] == "%" or tac[0] == "<<" or tac[0] == ">>"  or tac[0] == "^" or tac[0] == "|" or tac[0] == "&"):
			local_dict.update({tac[1]:start})
			local_dict.update({tac[2]:start})
			local_dict.update({tac[3]:start})
		elif(tac[0]=="=" ):
			local_dict.update({tac[1]:start})
			local_dict.update({tac[2]:start})
		elif(tac[0] == "ifgoto"  ):
			local_dict.update({tac[2]:start})
			local_dict.update({tac[3]:start})
		elif(tac[0]=="array"):
		sorted_x=sorted(data.items(), key=lambda x:x[1],reverse=True)

		for s in sorted_x:
				return s[0]

		

	def getreg(self,variable,LINE_NO):
		if variable == " " and len(self.freeRegisters) > 0:
			reg = self.freeRegisters[0]
			self.freeRegisters.remove(reg)
			self.registerInUse.append(reg)
			return (reg,)
		elif variable in self.Registers.values():
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
			next_register=next_use(LINE_NO)
			for key,value in self.Registers.iteritems():
				if value == next_register:

			pass




