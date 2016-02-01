f = open('1.txt','r')
w=open('2.txt','w')
for fr in f.readlines():
	s = fr
	s=s.strip()
	if s:
		m = "t_"+s+"\t\t=\tr''\n"
		w.write(m)
f.close()
w.close()