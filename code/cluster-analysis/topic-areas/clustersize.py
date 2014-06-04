#clustersize
import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import math
import networkx as nx
source = sys.argv[1]
ids = source + "DirectCitationNetworkGiantComponent.net" # Giantcomponent 
labels = source + "DirectCitationNetworkGiantComponent_Synthe2.clu" # partition file
inputfile = source + "in.txt" #input file
outfile = source + "clustersize.txt"
top = 11 # top X area
IDmatchLabel = {}
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

readIDmatchLabel(ids,labels)
class Paper:
    #ID
    #CI
    #SO
    #TI
    #BI
    #AU []
    #AF []
    #CT []
    #CO []
    #RF []
    #CA []
    #YR
    def __init__(self):
        self.ID = ''
        self.CI = ''
        self.SO = ''
        self.TI = ''
        self.BI = ''
        self.AU = []
        self.AF = []
        self.CT = []
        self.CO = []
        self.RF = []
        self.CA = []
        self.YR = 0 #integer
        self.label= 0 #label of clusters (after two rounds of clustering)

#sort

papers = []
clusteryearcount = {}
styr = int(sys.argv[2])
edyr = int(sys.argv[3])
for i in range(1,top+1):
    clusteryearcount[i] = {}
    for j in range(styr,edyr+1):
        clusteryearcount[i][j] = 0

def readPaperFromFile(File):
    inFile = open(str(File), "r")
    tt = 0
    InitialNumberOfPapers = 0
    PaperFlag = 0 # 1 = inside processing a paper, 0 = otherwise
    k = 0
    p = Paper()
    for lines in inFile:
        string = str(lines)
        if(string =='\n' or string ==' \n'):
            PaperFlag = 0
            papers.append(p)
            InitialNumberOfPapers = InitialNumberOfPapers +1
            

            if (p.label>0) and (p.label<=top):

                clusteryearcount[p.label][p.YR] += 1
            p = Paper()
        if(string[0] == 'I' and string[1]=='D'):
            PaperFlag = 1
            #processing ID
            l = len(string)
            p.ID = string[3:l-1]
            if p.ID in IDmatchLabel:
                p.label = IDmatchLabel[p.ID]
            else:
                p.label = 0
        elif(string[0] == 'C' and string[1]=='I'):
            #processing CI
            l = len(string)
            p.CI = string[3:l-1]
        elif(string[0] == 'S' and string[1]=='O'):
            #processing SO
            l = len(string)
            p.SO = string[3:l-1]
        elif(string[0] == 'T' and string[1]=='I'):
            #processing TI
            l = len(string)
            p.TI = string[3:l-1]
        elif(string[0] == 'B' and string[1]=='I'):
            #processing BI and Year
            l = len(string)
            p.BI = string[3:l-1]
            temp = string[l-5:l-1]
            p.YR  = int(temp)
        elif(string[0] == 'A' and string[1]=='U'):
            #processing AU
            l = len(string)
            s = string[3:l-1]    
            p.AU.append(s)
            # if (s == "IMAHORI, H"):
            #     tt += 1
            #     print p.YR
        elif((string[0] == ' ') and (PaperFlag==1)):
            l = len(string)
            s = string[1:l-1]
            # if (s == "IMAHORI, H"):
            #     tt += 1
            #     print p.YR    
            p.AU.append(s)
        elif(string[0] == 'A' and string[1]=='F'):
            #processing AF
            l = len(string)
            s = string[3:l-1]
            p.AF.append(s)
        elif(string[0] == 'C' and string[1]=='T'):
            #processing CT
            l = len(string)
            s = string[3:l-1]
            p.CT.append(s)
        elif(string[0] == 'C' and string[1]=='O'):
            #processing CO
            l = len(string)
            s = string[3:l-1]
            p.CO.append(s)
        elif(string[0] == 'R' and string[1]=='F'):
            #processing RF
            l = len(string)
            s = string[3:l-1]
            p.RF.append(s)
        elif(string[0] == 'C' and string[1]=='A'):
            #processing CA
            l = len(string)
            s = string[3:l-1]
            p.CA.append(s)
            
    inFile.close()

    print 'Read Complete'

readPaperFromFile(inputfile)
out = open(outfile,"w")
out.write("year\tpubl\n")
for i in range(1,top+1):
    for j in range(styr,edyr+1):
        out.write(str(j)+"\t"+str(clusteryearcount[i][j])+"\n")
out.close()
