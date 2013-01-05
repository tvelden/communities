import sys

def ConvertToMap(infile):
	max = 10
	f = open(infile, 'r')
	last = len(infile) - 1
	while(infile[last] != '_'):
		last = last - 1
	x = 0
	u = ''
	while(x<=last):
		u = u + str(infile[x])
		x = x + 1
	u = u + 'unborn.net'
	#print u
	ufile = open(u,'r')
	
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
	total = 0
	NC = {}
	CL = {}
	CL[0] = []
	for line in ufile:
		if line[0] =='*':
			#print line
			continue
		if line	 =='\n':
			continue
		Nodes[line[0:len(line)-1]] = index
		index = index +1
		NC[line[0:len(line)-1]] = 1
		CL[0].append(line[0:len(line)-1])
		total = total + 1
	ufile.close()
	
	print index
	count = 0
	if(total==0):
		count = -1
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
		if(count<max):
			total = total + 1
	f.close()
	
	if(count<max):
		max = count
	#print max
	pos = infile.find('.')
	of = infile[0:pos] + '_fake_cluster.map'
	print of
	fo = open(of, 'w')
	fo.write('# modules: ' + str(max) + '\n')
	fo.write('# modulelinks: 0\n')
	fo.write('# nodes: ' + str(total) + '\n')
	fo.write('# links: '+ str(total)+'\n')
	fo.write('# codelength: 2.51912\n')
	fo.write('*Directed\n')
	fo.write('*Modules '+str(max)+'\n')
	for i in range(0,max):
		fo.write(str(i+1)+ ' "' + str(CL[i][0]) +'" ' + str(float(len(CL[i]))/float(total)) + ' 0.0\n')
	fo.write('*Nodes '+ str(total) + '\n')
	for i in range(0,max):
		for j in range(0,len(CL[i])):
			fo.write(str(i+1) + ':' + str(j+1) + ' "' + str(CL[i][j]) + '" ' + str((float(len(CL[i]))/float(total))/float(len(CL[i]))) + '\n')
	fo.write('*Links 0\n')
	fo.close()


def convert(infile):
	max = 10
	f = open(infile, 'r')
	last = len(infile) - 1
	while(infile[last] != '_'):
		last = last - 1
	x = 0
	u = ''
	while(x<=last):
		u = u + str(infile[x])
		x = x + 1
	u = u + 'unborn.net'
	#print u
	ufile = open(u,'r')
	
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
	CL[1] = []
	for line in ufile:
		if line[0] =='*':
			#print line
			continue
		if line	 =='\n':
			continue
		Nodes[line[0:len(line)-1]] = index
		index = index +1
		NC[line[0:len(line)-1]] = 1
		CL[1].append(line[0:len(line)-1])
	ufile.close()
	print index
	count = 1
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
		print e, len(CL[e])
		if(e>max):
			break
		ct = ct + len(CL[e])
	fo.write('*Vertices ' + str(ct) + '\n')
	print ct
	cp = 0
	for e in Nodes:
		if(NC[e]<=max):
			#print NC[e]
			fo.write(str(Nodes[e]) + ' "' + str(e) + '"\n')
			cp = cp + 1
	print cp
	PP = {}
	#print NC
	for i in range(0,10):
		PP[i] = 0
	for e in NC:
		if NC[e] in range(0,10):
			PP[NC[e]] = PP[NC[e]] + 1
	print PP
	fo.write('*Edges\n')
	for e in CL:
		if(e>max):
			break
		l = len(CL[e])
		for i in range(2,l):
			x = CL[e][0]
			y = CL[e][i]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 15000\n')
		if(l>1):
			x = CL[e][0]
			y = CL[e][1]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 15000\n')
			for i in range(2,l):
				x = CL[e][1]
				y = CL[e][i]
				fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 15000\n')
		for i in range(0,l-4):
			x = CL[e][i]
			y = CL[e][i+1]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			y = CL[e][l-i-1]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			x = CL[e][i]
			y = CL[e][i+2]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			y = CL[e][l-i-2]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			x = CL[e][i]
			y = CL[e][i+3]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			y = CL[e][l-i-3]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			x = CL[e][i]
			y = CL[e][i+4]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			y = CL[e][l-i-4]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
		for i in range(1,l):
			x = CL[e][i]
			y = CL[e][l-i]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
		if(len(CL[e])>5):
			x = CL[e][3]
			y = CL[e][l-1]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			x = CL[e][2]
			y = CL[e][l-2]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			x = CL[e][1]
			y = CL[e][l-3]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
			x = CL[e][0]
			y = CL[e][l-4]
			fo.write(str(Nodes[x]) + ' ' + str(Nodes[y]) + ' 1000\n')
	fo.close()
if __name__ == "__main__":
	#convert(sys.argv[1])
	ConvertToMap(sys.argv[1])