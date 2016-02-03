import sys
import RegisterState

# We store the 3 Address Code as list of lists:
# a[1] - Line Number
# a[1] - InstrType typ; // assign, goto...
# a[2] - SymtabEntry *in1;
# a[3] - SymtabEntry *in2
# a[4] - SymtabEntry *out;
# a[5] - int target; // jump target
# a[6] - Operator op 
def codeGenerator(inFile):
	i=1
	TAC = {}
	with open(filename,'r') as infile:
		for line in infile:
			print line.rsplit(',')[1].strip()
			if(line.rsplit(',')[1].strip()=='goto' or line.rsplit(',')[1].strip()=='call' or line.rsplit(',')[1].strip()=='label'):
				TAC[i] = [line.rsplit(',')[1].strip(),'','','','',line.rsplit(',')[2].strip()]
			elif(line.rsplit(',')[1].strip() == 'ret'):
				TAC[i] = [line.rsplit(',')[1].strip(),'','','','','']
			elif(line.rsplit(',')[1].strip()=='='):
				TAC[i] = ['assign',line.rsplit(',')[2].strip(),'',line.rsplit(',')[3].strip(),'','']
			elif(line.rsplit(',')[1].strip()=='+' or line.rsplit(',')[1].strip()=='-' or line.rsplit(',')[1].strip()=='*' or line.rsplit(',')[1].strip()=='/'):
				TAC[i] = ['assign',line.rsplit(',')[3].strip(),line.rsplit(',')[4].strip(),line.rsplit(',')[2].strip(),'',line.rsplit(',')[1].strip()]
			elif(line.rsplit(',')[1].strip()=='ifgoto'):
				TAC[i] = [line.rsplit(',')[1].strip(),line.rsplit(',')[2].strip(),line.rsplit(',')[3].strip(),'',line.rsplit(',')[4].strip(),line.rsplit(',')[5].strip()]
			elif(line.rsplit(',')[1].strip()=='print'):
				TAC[i] = [line.rsplit(',')[1].strip(),line.rsplit(',')[2].strip(),'','','','']


			i = i+1
	printTAC(TAC)

def printTAC(TAC):
	with open('out','w') as outfile:
		print TAC
		print '\n'


if __name__ == '__main__':
	filename = sys.argv[1]
	codeGenerator(filename)


