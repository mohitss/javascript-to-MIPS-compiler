import sys
import regalloc

register_handler = None
labels=[]


def findlabels(filename):
	f = open(filename,'r')
	LINE_NO = 0
	labels.append('1')
	for line in f.readlines():
		LINE_NO += 1
		line = line.strip()
		tac = line.split(",")
		if tac[0] == "goto":
			labels.append(tac[1])
			labels.append(str(LINE_NO+1))
		elif tac[0] == "ifgoto":
			labels.append(tac[5])
			labels.append(str(LINE_NO+1))
	f.close()


def codegen(filename):
	f = open(filename,'r')
	assemblycode = []
	data = []
	LINE_NO = 0
	for line in f.readlines():
		LINE_NO += 1
		if (str(LINE_NO) in labels):
			assemblycode.append("LABEL_"+str(LINE_NO)+":")
		line = line.strip()
		tac = line.split(",")

		#equal assigment
		if len(tac) == 1 and tac[0] == "exit":
			assemblycode.append("\tli $v0, 10")
			assemblycode.append("\tsyscall")
		
		#assignment
		elif tac[0] == "=":
			reg1 = None
			reg2 = None
			ret_val = register_handler.getreg(tac[1])
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2])
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			assemblycode.append("\tmove "+reg1+","+reg2)
		
		# printing an integer
		elif tac[0] == "print_int":
			assemblycode.append("\tli $v0,1")
			assemblycode.append("\tli $a0,"+tac[1])
			assemblycode.append("\tsyscall")
		
		#adding two 
		elif tac[0] == "+":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1])
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2])
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3])
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]
			assemblycode.append("\tadd "+reg1+","+reg2+","+reg3)

		#subtracting two 
		elif tac[0] == "-":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1])
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2])
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3])
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]
			assemblycode.append("\tsub "+reg1+","+reg2+","+reg3)

		#multiplying two
		elif tac[0] == "*":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1])
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2])
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3])
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tmult "+reg2+","+reg3)
			assemblycode.append("\tmflo "+reg1)
		
		#dividing two
		elif tac[0] == "/":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1])
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2])
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3])
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tdiv "+reg2+","+reg3)
			assemblycode.append("\tmflo "+reg1)	

		#modulating two
		elif tac[0] == "%":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1])
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2])
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3])
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tdiv "+reg2+","+reg3)
			assemblycode.append("\tmfhi "+reg1)	

		#left shift
		elif tac[0] == "<<":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1])
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2])
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3])
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tsllv "+reg1+","+reg2+","+reg3)

		#right shift
		elif tac[0] == ">>":
			reg1 = None
			reg2 = None
			reg3 = None
			ret_val = register_handler.getreg(tac[1])
			if len(ret_val)==1:
				reg1 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg1 = ret_val[0]
			ret_val = register_handler.getreg(tac[2])
			if len(ret_val)==1:
				reg2 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg2 = ret_val[0]
			ret_val = register_handler.getreg(tac[3])
			if len(ret_val)==1:
				reg3 = ret_val[0]
			else:
				assemblycode.append(ret_val[1])
				reg3 = ret_val[0]

			assemblycode.append("\tsrlv "+reg1+","+reg2+","+reg3)

		#print char ~
		elif tac[0] == "print_char":
			assemblycode.append("\tli $v0,11")
			assemblycode.append("\tli $a0,"+tac[1])
			assemblycode.append("\tsyscall")

		#read int ~
		elif tac[0] == "read_int":
			assemblycode.append("\tli $v0,5")
			assemblycode.append("\tsyscall")
			assemblycode.append("\tsw $v0,"+tac[1])
	
	f.close()
	return assemblycode

if __name__ == '__main__':
	filename = sys.argv[1]
	findlabels(filename)
	register_handler = regalloc.regalloc()
	assemblycode = codegen(filename)

	for line in assemblycode:
		print line