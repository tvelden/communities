#The codes aim to generate the proportion of papers in three big slices belong to the clusters in the accumulative network.
import sys
ids = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/DirectCitationNetworkGiantComponent.net" #giant component
Labels = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/DirectCitationNetworkGiantComponent_Synthe2.clu" #partition files
IDmatchLabel = {}
top = 11

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
print len(IDmatchLabel)

cluporp = {}
Tot =[]
for j in range(1,top+1):
    Tot.append(0)

for ii in range(1,4):
    for j in range(1,top+1):
        cluporp[j] = {}
    sourceid = "/Users/shiyansiadmin/Dropbox/Files/Field2DataSS" + str(ii) + "/DirectCitationNetworkGiantComponent.net"
    sourcelabel =  "/Users/shiyansiadmin/Dropbox/Files/Field2DataSS" + str(ii) + "/DirectCitationNetworkGiantComponent_Synthe2.clu"
    LabelInput = open(str(sourcelabel) , 'r')
    i = -1
    LabelMap = {}
    for lines in LabelInput:
        i = i + 1
        if (i == 0): continue
        LabelMap[i] = int(lines)
    LabelInput.close()            
    idInput = open(str(sourceid), 'r')
    i = 0
    for lines in idInput:
        k = lines.split('"')
        if (len(k) <= 1):
            continue
        else:
            i = i + 1
            accumuLabel = IDmatchLabel[k[1]]
            slicelabel = LabelMap[i]
            if (accumuLabel>top) or (slicelabel>top):
                continue
            if accumuLabel in cluporp[slicelabel]:
                cluporp[slicelabel][accumuLabel] += 1
            else:
                cluporp[slicelabel][accumuLabel] = 1

    outfile = open("/Users/shiyansiadmin/Dropbox/Files/8slicesPortion"+str(ii),"w")
    outfile.write("Clu	")
    for j in range(1,top+1):
        outfile.write("AC" + str(j) + "	")
    outfile.write("\n")
    for j in range(1, top+1):
        outfile.write("SC" +str(j) + "	")
        for k in range(1,top+1):
            # outfile.write("Sclu"+str(j)+"	"+"Aclu"+str(k)+"	")
            if k in cluporp[j]:
                outfile.write(str(cluporp[j][k]) + "	")
            else:
                outfile.write("0	")
        outfile.write("\n")
