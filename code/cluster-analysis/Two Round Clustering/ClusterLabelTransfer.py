import sys
#cluster label transfer
source = "/Users/shiyansiadmin/Dropbox/Files/OldField2Data2/DirectCitationNetwork"
infile = open(sys.argv[1],'r')
outfile = open(sys.argv[2],'w')

cluDic = {}
cluList = []
cluMap = {}

flag = 1 
for line in infile:
    cluList.append(line)
    if (flag ==1 ):
        flag = 0
        continue
    if line in cluDic:
        cluDic[line] += 1
    else:
        cluDic[line] = 1

tot = 1
print "Mapping Table"
for ke in sorted(cluDic, key = cluDic.get, reverse = True):
    cluMap[ke] = str(tot) + "\n"
    print str(tot) + " <-- " + str(ke)
    tot +=1

flag = 1
for line in cluList:
    if (flag == 1):
        flag = 0
        outfile.write(line)
        continue
    outfile.write(cluMap[line])
infile.close()
outfile.close()
