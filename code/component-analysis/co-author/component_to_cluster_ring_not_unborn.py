import sys

def ConvertToMap(infile):
	max = 10
	f = open(infile, 'r')
	last = len(infile) - 1
	while(infile[last] != '_'):
		last = last - 1
	x = 0

	
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
	of = infile[0:pos] + '_fake_cluster_no_unborn.map'
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


if __name__ == "__main__":
	#convert(sys.argv[1])
	ConvertToMap(sys.argv[1])