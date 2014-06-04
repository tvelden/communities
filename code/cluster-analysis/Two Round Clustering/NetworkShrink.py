#Network Shrunk
import sys
netsource = "/Users/shiyansiadmin/Dropbox/Files/OldField2Data3/DirectCitationNetworkGiantComponent"
netInfile = open(sys.argv[1],'r')
cluInfile = open(sys.argv[2],'r')
netOutfile = open(sys.argv[3],'w')

IdClusterMap = {}
i = -1
# Build ClusterLabel of every paper
for line in cluInfile:
    i += 1
    if (i == 0):
        continue
    num = int(line[0:len(line)-1])
    IdClusterMap[i] = num


i = -1

ClusterRepreId = {}
EdgeList = {}

totlabel = 0
ind = 0
for line in netInfile:
    i += 1
    if (i==0):
        kk = line.split(" ")
        numOfNodes = int(kk[1][0:len(kk[1])-1])
    elif (i<=numOfNodes):
        kk = line.split('"')
        idt = kk[1] #string
        label = IdClusterMap[i]
        if (label>totlabel): totlabel = label
        if (not (label in ClusterRepreId)):
            ind +=1
            ClusterRepreId[label] = idt
    elif (i>numOfNodes+1):
        kk = line.split(" ")
        c1 = IdClusterMap[int(kk[0])]
        c2 = IdClusterMap[int(kk[1])]
        if not (c1 in EdgeList):
            EdgeList[c1] = {}
            EdgeList[c1][c2] = 1
        else:
            if not (c2 in EdgeList[c1]):
                EdgeList[c1][c2] = 1
            else:
                EdgeList[c1][c2] += 1


netOutfile.write("*Vertices " + str(totlabel) + "\n")
print "There are " + str(totlabel) + " nodes in the shrunk network"

for j in range(1,totlabel+1):
    netOutfile.write(str(j) + ' "' + ClusterRepreId[j] + '"\n')

netOutfile.write("*Arcs\n")


for i in sorted(EdgeList):
    for j in sorted(EdgeList[i]):
        netOutfile.write(str(i) + " " + str(j) + " " +str(EdgeList[i][j]) +"\n")


