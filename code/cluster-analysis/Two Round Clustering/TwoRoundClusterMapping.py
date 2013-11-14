#it's a two round clustering mapping algorithms
import os
import sys
import operator
import numpy
if __name__ == "__main__":
	fs1 = str(sys.argv[1])
	fs2 = str(sys.argv[2])
	inFile1 = open(fs1,'r')
	inFile2 = open(fs2,'r')
	map1 = {}
	map2 = {}
	i = 0
	flag = 0
	for lines in inFile1:
		if (flag == 0):
			flag = 1
			line1 = str(lines)
			continue
		i = i + 1
		string = str(lines)
		# if (i==1):
		# 	print string
		# 	print len(string)
		map1[i] = string[0:len(string)-2] # different .clu files need different length
	tot = i
	i = 0
	flag = 0
	for lines in inFile2:
		if (flag == 0):
			flag = 1
			continue
		i = i + 1
		string = str(lines)
		map2[str(i)] = string[0:len(string)-2]
	inFile1.close()
	inFile2.close()

	size = {}

	fs3 = str(sys.argv[3])
	outFile = open(fs3,'w')
	outFile.write( line1 )
	for k in range(1,tot+1):
		outFile.write( map2[map1[k]] + '\n')
		# print str(k) + str(map1[k])
		if map2[map1[k]] in size:
			size[map2[map1[k]]] = size[map2[map1[k]]] + 1
		else:
			size[map2[map1[k]]] = 1
	outFile.close()

	#count the size of clusters of the second round
	for t in sorted(size, key = size.get, reverse=True ):
		if (size[t] >= 1):
			print str(t) + '	' + str(size[t])



