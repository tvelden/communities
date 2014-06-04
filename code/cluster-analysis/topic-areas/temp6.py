#temp6
import sys
ids = "/Users/shiyansiadmin/Dropbox/Files/Field2DataS1/DirectCitationNetworkGiantComponent.net" #giant component
Labels = "/Users/shiyansiadmin/Dropbox/Files/Field2DataS1/DirectCitationNetworkGiantComponent_Synthe2.clu" #partition files
st = 1991
ed = 2001
out = "/Users/shiyansiadmin/Dropbox/Files/Field2DataS1/" + "ArticleID-ClusterID" +str(st) + "-" + str(ed)
IDmatchLabel = {}
top = 11

idsAll = "/Users/shiyansiadmin/Dropbox/Files/Field2DataS1/DirectCitationNetwork.net"

def readIDmatchLabel(IDs,Labels): #map between IDs and Labels
    # change the label from here
    LabelInput = open(str(Labels) , 'r')
    i = -1
    LabelMap = {}
    for lines in LabelInput:
        i = i + 1
        if (i == 0): continue
        LabelMap[i] = int(lines)
    LabelInput.close()            
        
    idInput = open(str(IDs), 'r')
    i = 0
    for lines in idInput:
        k = lines.split('"')
        if (len(k) <= 1):
            continue
        else:
            i = i + 1
            IDmatchLabel[k[1]] = LabelMap[i]
    print 'Match Complete'

readIDmatchLabel(ids,Labels)
infile = open(str(idsAll),"r")
outfile = open(str(out),"w")
i = 0
for lines in infile:
    k = lines.split('"')
    if (len(k)<=1):
    	continue
    else:
        outfile.write(k[1] + "	")
        if k[1] in IDmatchLabel:
            outfile.write(str(IDmatchLabel[k[1]]) + "\n")
        else:
            outfile.write(str(0) + "\n")