import sys

def convert(infile):
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
	fo.write('*Vertices ' + str(index-1) + '\n')
	for e in Nodes:
		fo.write(str(Nodes[e]) + ' "' + str(e) + '"\n')
	fo.write('*Edges\n')
	for e in CL:
		l = len(CL[e])
		for i in range(0,l-1):
			x = CL[e][i]
			y = CL[e][i+1]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1\n')
		if(len(CL[e])>2):
			x = CL[e][0]
			y = CL[e][l-1]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1\n')
	fo.close()
if __name__ == "__main__":
	convert(sys.argv[1])