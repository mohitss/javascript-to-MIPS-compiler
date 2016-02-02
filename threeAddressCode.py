import sys

# We store the 3 Address Code as list of lists:
# a[0] - Line Number
# a[1] - InstrType typ; // assign, goto...
# a[2] - SymtabEntry *in1;
# a[3] - SymtabEntry *in2
# a[4] - SymtabEntry *out;
# a[5] - int target; // jump target
# a[6] - Operator op 
def codeGenerator(inFile, outFile):
	i=0
	TAC = {}
	with openfile(filename,'r') as infile:
		for line in infile:
			if(line.rsplit(',')[0]=='goto'||line.rsplit(',')[0]=='call'||line.rsplit(',')[0]=='label'):
				TAC.append(i,line.rsplit(',')[0],'','','','',line.rsplit(',')[1])
			elif(line.rsplit(',')[0] == 'ret'):
				TAC.append(i,line.rsplit(',')[0],'','','','','')
			elif(line.rsplit(',')[0]=='='):
				TAC.append(i,'assign',line.rsplit(',')[2],'',line.rsplit(',')[1],'','')
			elif(line.rsplit(,)[0]=='+'||line.rsplit(',')[0]=='-'||line.rsplit(',')[0]=='*'||line.rsplit(',')[0]=='/'):
				TAC.append(i,'assign',line.rsplit(',')[2],line.rsplit(',')[3],line.rsplit(',')[1],'',line.rsplit(',')[0])
			elif(line.rsplit(',')[0]=='ifgoto'):
				TAC.append(i,line.rsplit(',')[0],line.rsplit(',')[2],line.rsplit(',')[3],'',line.rsplit(',')[4],line.rsplit(',')[1])

			i = i+1
	printTAC(TAC, outFile)

def printTAC(TAC, filename):
	with openfile(filename,'w') as outfile:
		for li in TAC:
			print(li[0]+' '+li[1]+' '+li[2]+' '+li[3]+' '+li[4]+' '+li[5]+' '+li[6]+'\n')



if __name__ == '__main__':
	filename = sys.argv[1]
	codeGenerator(filename, out)


