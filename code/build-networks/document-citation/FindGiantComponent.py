#find the giant component
import sys
source = sys.argv[1]
target = sys.argv[2]

# source = '../../../../../Dropbox/Files/Field3Data1/DirectCitationNetwork.net'
# target = '../../../../../Dropbox/Files/Field3Data1/DirectCitationNetworkGiantComponent.net'

infile = open(source,'r')
outfile = open(target,'w')
father = []
idMap={}
i = -1

def findfather(i):
	if (father[i]!=i):
	    father[i] = findfather(father[i])
	    return father[i]
	else:
		return i

for line in infile:
    i+=1
    if (i==0):
        kk=line.split(" ")
        numOfNodes = int(kk[1][0:len(kk[1])-1])
        for j in range(0,numOfNodes+1):
            father.append(j)
    elif (i<=numOfNodes):
        kk=line.split('"')
        ids = kk[1][0:len(kk[1])]
        idMap[i] = ids
    elif (i!=numOfNodes+1):
    	kk=line.split(" ")
    	f1 = findfather(int(kk[0]))
    	f2 = findfather(int(kk[1]))
    	if (f1!=f2):
    		father[f2] = father[f1]

count = {}
maxcount = 0
maxindex = 0
for j in range(1,numOfNodes+1):
    ff = findfather(j)
    if (ff in count):
    	count[ff] += 1
    else:
    	count[ff] = 1
    if (count[ff]>maxcount):
    	maxcount = count[ff]
    	maxindex = ff
i = 0
for cc in sorted(count, key=count.get, reverse=True):
    i +=1
    print count[cc]
    if (i>10):
        break
#output
outfile.write("*Vertices " + str(maxcount) + "\n")
print "There are " + str(maxcount) + " nodes in the giant component"
i = 0

numMap = {}
for j in range(1,numOfNodes+1):
	if father[j]==maxindex:
	    i += 1
	    outfile.write(str(i)+' "' + str(idMap[j]) + '"\n')
	    numMap[j] = i

i = -1
outfile.write("*Arcs\n")
infile = open(source,'r')
for line in infile:
    i += 1
    if (i>numOfNodes+1):
        kk=line.split(" ")
        num1 = int(kk[0])
        num2 = int(kk[1])
        if (num1 in numMap):
        	outfile.write(str(numMap[num1]) + " " + str(numMap[num2]) + " " + "1\n")

outfile.close()



