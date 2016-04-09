import sys
# import codegen
import re
import operator
# dictionary={}
# current_basic_block=1
# filename=""

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

	def next_use(self,LINE_NO,dictionary,filename,current_basic_block):
		f=open(filename)
		lines=f.readlines()
		local_dict={}
		start=LINE_NO-1
		end=dictionary[current_basic_block]['end']-1
		while(start<=end):
			line = lines[end].strip()
			tac = line.split(",")
			if( tac[0] == "+"or tac[0] == "-" or tac[0] == "*" or tac[0] == "/" or tac[0] == "%" or tac[0] == "<<" or tac[0] == ">>"  or tac[0] == "^" or tac[0] == "|" or tac[0] == "&"):
				local_dict.update({tac[1]:100000})
				local_dict.update({tac[2]:end})
				local_dict.update({tac[3]:end})

			elif(tac[0]=="=" ):
				local_dict.update({tac[1]:100000})
				local_dict.update({tac[2]:end})
			elif(tac[0] == "ifgoto"  ):
				local_dict.update({tac[2]:end})
				local_dict.update({tac[3]:end})
			elif(tac[0]=="array"):
				pass
			end=end-1
		line = lines[start].strip()
		tac = line.split(",")
		temp_list=[]
		if( tac[0] == "+"or tac[0] == "-" or tac[0] == "*" or tac[0] == "/" or tac[0] == "%" or tac[0] == "<<" or tac[0] == ">>"  or tac[0] == "^" or tac[0] == "|" or tac[0] == "&"):
			local_dict.update({tac[1]:start})
			local_dict.update({tac[2]:start})
			local_dict.update({tac[3]:start})
			temp_list.append(tac[1])
			temp_list.append(tac[2])
			temp_list.append(tac[3])
		elif(tac[0]=="=" ):
			local_dict.update({tac[1]:start})
			local_dict.update({tac[2]:start})
			temp_list.append(tac[1])
			temp_list.append(tac[2])
		elif(tac[0] == "ifgoto"  ):
			local_dict.update({tac[2]:start})
			local_dict.update({tac[3]:start})
			temp_list.append(tac[2])
			temp_list.append(tac[3])
		elif(tac[0]=="array"):
			pass
		sorted_x=sorted(local_dict.items(), key=lambda x:x[1],reverse=True)
		f.close()
		return(sorted_x,temp_list)


	def flush_temp(self):
		regex = re.compile('temp_[0-9_]*')
		code  = ""
		for key,value in self.Registers.iteritems():
			if value!= None  and regex.match(value):
				code += "\tsw "+key+","+value+"\n"
				self.freeRegisters.append(key)
				self.registerInUse.remove(key)
				self.Registers[key] = None
		return code

	def getreg(self,variable,LINE_NO,dictionary,filename,current_basic_block,arr=False):
		# print self.freeRegisters
		# print self.Registers
		if arr==True and variable in self.Registers.values():
			for key,value in self.Registers.iteritems():
				if value == variable:
					return (key,'')

		elif arr==True and len(self.freeRegisters) > 0:
			reg = self.freeRegisters[0]
			self.freeRegisters.remove(reg)
			self.registerInUse.append(reg)
			self.Registers[reg] = variable
			self.variables[variable] = reg
			return (reg,'')
		elif arr==True and len(self.freeRegisters) == 0:
			list1,list2=next_use(LINE_NO,dictionary,filename,current_basic_block)
			next_register='None'
			for s in list1:
				if s[0] in list2:
					break
				else:
					next_register= s[0]
			if next_register != 'None':
				for key,value in self.Registers.iteritems():
					if value == next_register:
						code = "\tsw "+ key +","+ value+"\n"
						return (key,code)

			for key,value in self.Registers.iteritems():
				if value in list2:
					pass
				else:
					code = "\tsw "+ key +","+ value+"\n"
					return (key,code)

		elif variable in self.Registers.values():
			for key,value in self.Registers.iteritems():
				if value == variable:
					return (key,'')
		elif len(self.freeRegisters) > 0:
			reg = self.freeRegisters[0]
			self.freeRegisters.remove(reg)
			self.registerInUse.append(reg)
			self.Registers[reg] = variable
			self.variables[variable] = reg
			code = "\tlw "+reg+","+variable
			return (reg,code)
		elif len(self.freeRegisters) == 0:
			list1,list2=self.next_use(LINE_NO,dictionary,filename,current_basic_block)
			# print self.freeRegisters
			next_register='None'
			for s in list1:
				if s[0] in list2:
					pass
				else:
					next_register= s[0]
			# print next_register
			if next_register != 'None':
				for key,value in self.Registers.iteritems():
					if value == next_register:
						self.Registers[key] = variable
						self.variables[variable] = key
						code = "\tsw "+ key +","+ value+"\n"
						code += "\tlw " + key + "," + variable

						return (key,code)

			for key,value in self.Registers.iteritems():
				if value in list2:
					pass
				else:
					self.Registers[key] = variable
					self.variables[variable] = key
					code = "\tsw "+ key +","+ value+"\n"
					code += "\tlw " + key + "," + variable
					return (key,code)
