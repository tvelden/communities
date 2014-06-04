#ObjectTransfer
import sys
import pickle
from sets import Set

presource = "/Users/shiyansiadmin/Dropbox/Files/OldField2Data2/DirectCitationNetworkGiantComponent.net"
preinfile = open(presource,"r")
idMap = {}
i = -1
for line in preinfile:
    i += 1
    if (i == 0):
        continue
    if (line == "*Arcs\n"):
        break
    kk = line.split('"')
    ids = kk[1]
    idMap[ids] = i


source="/Users/shiyansiadmin/Dropbox/Files/article-cluster-area2.pck"
target="/Users/shiyansiadmin/Dropbox/Files/article-cluster-area.clu"
infile = open(source,"r")
ob = pickle.load(infile)

cluMap = {}
tot = 0
for article,cluster in ob.items():
    if not article in idMap:
    	continue
    idnum = idMap[article]
    cluMap[idnum] = cluster[1]
    tot +=1

outfile = open(target,"w")
outfile.write("Vertices " + str(tot) +'\n')
for i in sorted(cluMap):
    outfile.write(str(cluMap[i]) + "\n")
