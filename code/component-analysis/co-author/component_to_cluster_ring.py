import sys

def convert(infile):
	max = 10
	f = open(infile, 'r')
	
	num = 0
	for line in f:
		if (len(line)> 20):
			#print line[0:21]
			if((line[0:len('Number of Components:')] == 'Number of Components:')):
				n = line[len('Number of Components:'):len(line)-1]
				#print n
				num = int(n)
				break
	print('Number of Components (clusters): ' + str(num))
	f.close()
	f = open(infile, 'r')
	Nodes = {}
	index = 1
	NC = {}
	CL = {}
	count = 0
	start = 0
	for line in f:
		if(line[0]!='*' and start ==0):
			continue
		else:
			start = 1
		if(len(line) <=1):
			continue
		if(line[0] == '*' and line[1] == 'C'):
			continue
		if(line[0] =='*' and line[1] =='*'):
			 count = count + 1
			 CL[count] = []
			 continue
		#print line[0:len(line)-1]
		Nodes[line[0:len(line)-1]] = index
		index = index +1
		NC[line[0:len(line)-1]] = count
		CL[count].append(line[0:len(line)-1])
	f.close()
	
	pos = infile.find('.')
	of = infile[0:pos] + '_ring_cluster.net'
	print of
	fo = open(of, 'w')
	ct = 0
	for e in CL:
		if(e>max):
			break
		ct = ct + len(CL[e])
	fo.write('*Vertices ' + str(ct) + '\n')
	for e in Nodes:
		if(NC[e]<=max):
			fo.write(str(Nodes[e]) + ' "' + str(e) + '"\n')
	fo.write('*Edges\n')
	for e in CL:
		if(e>max):
			break
		l = len(CL[e])
		for i in range(1,l):
			x = CL[e][0]
			y = CL[e][i]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
		for i in range(0,l-3):
			x = CL[e][i]
			y = CL[e][i+1]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 100\n')
			x = CL[e][i]
			y = CL[e][i+2]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 100\n')
			x = CL[e][i]
			y = CL[e][i+3]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 100\n')
		if(len(CL[e])>4):
			x = CL[e][0]
			y = CL[e][l-1]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 100\n')
			x = CL[e][0]
			y = CL[e][l-2]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 100\n')
			x = CL[e][0]
			y = CL[e][l-3]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 100\n')
	fo.close()
if __name__ == "__main__":
	convert(sys.argv[1])