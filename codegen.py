import sys
import regalloc
import json

register_handler = None
labels=[]
labelsss=[]
dictionary={}
current_basic_block=1
filename=""


def findlabels():
	f = open(filename,'r')
	LINE_NO = 0
	labels.append('1')
	labelsss.append(('1',1))
	for line in f.readlines():
		LINE_NO += 1
		line = line.strip()
		tac = line.split(",")
		if tac[0] == "goto":
			if tac[1].isdigit():
				labels.append(tac[1])
				labelsss.append((tac[1],int(tac[1])))
			labels.append(str(LINE_NO+1))
			labelsss.append((str(LINE_NO+1),LINE_NO+1))

		elif tac[0] == "call":
			if tac[1].isdigit():
				labels.append(tac[1])
				labelsss.append((tac[1],int(tac[1])))
			labels.append(str(LINE_NO+1))
			labelsss.append((str(LINE_NO+1),LINE_NO+1))

		elif tac[0] == "ifgoto":
			if tac[4].isdigit():
				labels.append(tac[4])
				labelsss.append((tac[4],int(tac[4])))
			# labels.append(tac[4])
			labels.append(str(LINE_NO+1))
			labelsss.append((str(LINE_NO+1),LINE_NO+1))
		elif tac[0]=="fun_label":
			labels.append(str(LINE_NO))
			labelsss.append((tac[1],LINE_NO))
		elif tac[0]=="main" :
			labels.append(str(LINE_NO))
			labelsss.append(("main",LINE_NO))
		elif tac[0]=="label":
			labels.append(str(LINE_NO))
			labelsss.append((tac[1],LINE_NO))
	sorted(labelsss,key=lambda x: x[1])
	convert_list_to_dict(LINE_NO)
	f.close()

def convert_list_to_dict(LINE_NO):
	length= len(labelsss)
	for x in labelsss:
		index = labelsss.index(x)
		if index<length-1:
			next=labelsss[index+1][1]-1
		else:
			next=LINE_NO
		dictionary[x[1]]={'start':x[1] ,'end':next,'name':x[0]}
		# print x[0], x[1]

def codegen(filename):
	f = open(filename,'r')
	assemblycode = []
	global current_basic_block
	assemblycode.append(".data")
	data = []
	LINE_NO = 0
	for line in f.readlines():
		LINE_NO += 1
		if LINE_NO in dictionary:
			current_basic_block=LINE_NO
			register_handler.flush_temp()
			if dictionary[LINE_NO]['name'].isdigit():
				assemblycode.append("LABEL_"+str(LINE_NO)+":")
			# print current_basic_block
		# if (str(LINE_NO) in labels):
			
		line = line.strip()
		tac = line.split(",")

		#equal assigment ~
		if len(tac) == 1 and tac[0] == "exit":
			assemblycode.append("\tli $v0, 10")
			assemblycode.append("\tsyscall")
		
		#assignment
		elif tac[0] == "=":
			reg1 = None
			reg2 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			# print "fdsafdsfs"
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			assemblycode.append("\tmove "+reg1+","+reg2)
		
		#adding two ~
		elif tac[0] == "+":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]
			assemblycode.append("\tadd "+reg1+","+reg2+","+reg3)

		#subtracting two ~
		elif tac[0] == "-":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]
			assemblycode.append("\tsub "+reg1+","+reg2+","+reg3)

		#multiplying two ~
		elif tac[0] == "*":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tmult "+reg2+","+reg3)
			assemblycode.append("\tmflo "+reg1)
		
		#dividing two ~
		elif tac[0] == "/":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tdiv "+reg2+","+reg3)
			assemblycode.append("\tmflo "+reg1)	

		#modulating two ~
		elif tac[0] == "%":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tdiv "+reg2+","+reg3)
			assemblycode.append("\tmfhi "+reg1)	

		#left shift ~
		elif tac[0] == "<<":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tsllv "+reg1+","+reg2+","+reg3)

		#right shift ~
		elif tac[0] == ">>":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tsrlv "+reg1+","+reg2+","+reg3)

		# print int ~ constant
		elif tac[0] == "print_int":
			assemblycode.append("\tli $v0,1")
			assemblycode.append("\tli $a0,"+tac[1])
			assemblycode.append("\tsyscall")

		#print char ~ constant
		elif tac[0] == "print_char":
			assemblycode.append("\tli $v0,11")
			assemblycode.append("\tli $a0,"+tac[1])
			assemblycode.append("\tsyscall")

		#read int ~
		elif tac[0] == "read_int":
			assemblycode.append("\tli $v0,5")
			assemblycode.append("\tsyscall")
			assemblycode.append("\tsw $v0,"+tac[1])
		
		#print int ~ variable
		elif tac[0] == "print_intv":
			assemblycode.append("\tli $v0,1")
			assemblycode.append("\tlw $a0,"+tac[1])
			assemblycode.append("\tsyscall")

		#print string ~ variable
		elif tac[0] == "print_stringv":
			assemblycode.append("\tli $v0,4")
			assemblycode.append("\tla $a0,"+tac[1])
			assemblycode.append("\tsyscall")
		
		#xor ~
		elif tac[0] == "^":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]
			assemblycode.append("\txor "+reg1+","+reg2+","+reg3)
		
		#or ~
		elif tac[0] == "|":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]
			assemblycode.append("\tor "+reg1+","+reg2+","+reg3)

		#and ~
		elif tac[0] == "&":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]
			assemblycode.append("\tand "+reg1+","+reg2+","+reg3)

		#goto ~
		elif tac[0] == "goto":
			label_to_jump = tac[1]
			assemblycode.append("\tj "+label_to_jump)

		#function ~
		elif tac[0] == "fun_label":
			function_label = tac[1]
			assemblycode.append(function_label+":")

		#return ~
		elif tac[0] == "ret":

			assemblycode.append("\tjr $ra")

		#call function ~
		elif tac[0] == "call":
			#save all the registers
			for key,value in register_handler.Registers.iteritems():
				assemblycode.append("\taddi $sp,$sp,-4")
				assemblycode.append("\tsw "+key+",($sp)")
			assemblycode.append("\taddi $sp,$sp,-4")
			assemblycode.append("\tsw $ra,($sp)")

			#call the function
			assemblycode.append("\tjal "+tac[1])

			#restore all the registers
			assemblycode.append("\tlw $ra,($sp)")
			assemblycode.append("\taddi $sp,$sp,4")
			keys = []
			for key,value in register_handler.Registers.iteritems():
				keys.append(key)
			for k in range(len(keys)-1,-1,-1):
				assemblycode.append("\tlw "+keys[k]+",($sp)")
				assemblycode.append("\taddi $sp,$sp,4")

		#data allocation ~
		elif tac[0] == "data":
			if tac[2] == "int":
				assemblycode.append("\t"+tac[1]+":\t.word\t"+tac[3])
			elif tac[2] == "array":
				assemblycode.append("\t"+tac[1]+":\t.space\t"+str(4*int(tac[4])))

		#main label ~
		elif tac[0] == "main":

			assemblycode.append(".text\nmain:")

		#label label ~
		elif tac[0] == "label":

			assemblycode.append(tac[1]+":")

		#condition if goto ~
		elif tac[0] == "ifgoto":
			label_to_jump = tac[4]
			reg1 = None
			reg2 = None
			ret_val = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[3],LINE_NO,dictionary,filename,current_basic_block)
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			#if equal !
			if tac[1] == "beq":
				assemblycode.append("\tbeq "+reg1+","+reg2+","+label_to_jump)
			elif tac[1] == "bge":
				assemblycode.append("\tbge "+reg1+","+reg2+","+label_to_jump)
			elif tac[1] == "bgt":
				assemblycode.append("\tbgt "+reg1+","+reg2+","+label_to_jump)
			elif tac[1] == "ble":
				assemblycode.append("\tble "+reg1+","+reg2+","+label_to_jump)
			elif tac[1] == "blt":
				assemblycode.append("\tblt "+reg1+","+reg2+","+label_to_jump)
			elif tac[1] == "bne":
				assemblycode.append("\tbne "+reg1+","+reg2+","+label_to_jump)

		#array access and modification
		elif tac[0]=="array":
			if tac[3] == "set":
				reg1,code = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block,True)
				assemblycode.append(code)
				assemblycode.append("\tla "+reg1+","+tac[1])
				ret_val = register_handler.getreg(tac[4],LINE_NO,dictionary,filename,current_basic_block)
				if len(ret_val) == 1:
					reg2 = ret_val[0]
				else:
					assemblycode.append(ret_val[1])
					reg2 = ret_val[0]
				assemblycode.append("\tsw "+reg2+","+str(4*int(tac[2]))+"("+reg1+")")
			elif tac[3] == "get":
				reg1,code1 = register_handler.getreg(tac[1],LINE_NO,dictionary,filename,current_basic_block)
				reg2,code2 = register_handler.getreg(tac[2],LINE_NO,dictionary,filename,current_basic_block,True)
				assemblycode.append(code1)
				assemblycode.append(code2)
				assemblycode.append("\tla "+reg1+","+tac[1])
				assemblycode.append("\tlw "+reg2+","+str(4*int(tac[2]))+"("+reg1+")")
				assemblycode.append("\tsw "+reg2+","+tac[4])
	f.close()
	return assemblycode

if __name__ == '__main__':
	filename = sys.argv[1]
	# print filename
	findlabels()
	# print(json.dumps(dictionary, indent = 4))
	# for car in dictionary.items():
	# 	print car
		# print "fdsafasfasd"
	register_handler = regalloc.regalloc()
	assemblycode = codegen(filename)
	# print dictionary
	# if 33 in dictionary:
	# 	print "dfasfdsaf"
	for line in assemblycode:
		print line


	# for x in labelsss:
	# 	print x[0], x[1]
	# for x in labels:
	# 	print x