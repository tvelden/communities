# Compare two result files
import sys
import pickle

source1 = "/Users/shiyansiadmin/Dropbox/Files/OldField2Data2/DirectCitationNetworkGiantComponent_Synthe2.clu"
source2 = "/Users/shiyansiadmin/Dropbox/Files/article-cluster-area-Synthe.clu"
target =  "/Users/shiyansiadmin/Dropbox/Files/percentDifference.txt"

dict1 = {}
dict2 = {}

infile1 = open(source1,"r")
infile2 = open(source2,"r")

i = -1
for line in infile1:
    i += 1
    if (i==0):
        continue
    clus = int(line[0:len(line)-1])
    if clus in dict1:
        dict1[clus].append(i)
    else:
        dict1[clus] = []
        dict1[clus].append(i)
i = -1
for line in infile2:
    i += 1
    if (i==0):
        continue
    clus = int(line[0:len(line)-1])
    if clus in dict2:
        dict2[clus].append(i)
    else:
        dict2[clus] = []
        dict2[clus].append(i)

outfile = open(target,"w")

for i in sorted(dict1):
    sumt = 0
    for j in sorted(dict2):
        merge = list(set(dict1[i]) & set(dict2[j]))
        per = float(len(merge)) / float(len(dict1[i]))
        sumt += per
        if (j<=11):
            outfile.write(str(per) + "	")
        else:
        	outfile.write(str(1-sumt) + "\n")
        	break



