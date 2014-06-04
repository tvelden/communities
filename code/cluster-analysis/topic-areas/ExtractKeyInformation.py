#extract key information
import sys
source_dir = sys.argv[1] 
ids = source_dir + "DirectCitationNetworkGiantComponent.net" #giant component
Labels = source_dir + "DirectCitationNetworkGiantComponent_Synthe2.clu" #partition files
AllPapers = source_dir + "DirectCitationNetwork.net"
articleMatch = source_dir + "ArticleID-ClusterID"
inputfile = source_dir + "in.txt" #input file
IDmatchLabel = {}
top = 11
startyear = int(sys.argv[2])
endyear = int(sys.argv[3])
tt = 0
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
            if (p.YR>endyear) or (p.YR<startyear):
                k = k
            else:
                papers.append(p)
            InitialNumberOfPapers = InitialNumberOfPapers +1
            p = Paper()
            continue
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
        elif((string[0] == ' ') and (PaperFlag==1)):
            l = len(string)
            s = string[1:l-1]
  
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
    #print tt 


outfile = []
def printKeyInformation(source):
    tt = 0
    sourcet = source + "keyinfo/"
    for i in range(0,top+1):
        ss = sourcet + "cluster" + str(i)
        outfile.append(open(ss,"w"))
    cc  = 0
    for p in papers:
        if p.label ==0:
            cc +=1
        if p.label>top:
            p.label = 0 # both the papers not in the giant component and papers in the clusters ranked lower than 'top' will be included in key information of cluster0
        if p.TI!="":
            strti = "TI " + p.TI + "\n"
            outfile[p.label].write(strti)
        if p.YR!=0:
            stryr = "YR " + str(p.YR) + "\n"
            outfile[p.label].write(stryr)
        if p.SO!="":
            strso = "SO " + str(p.SO) + "\n"
            outfile[p.label].write(strso)
        if len(p.AU)!=0:
            outfile[p.label].write("AU ")
            for au in p.AU:
                if (str(au) =="IMAHORI, H"):                  
                    tt += 1

                outfile[p.label].write(au + " | ")
            outfile[p.label].write("\n")
        if len(p.CA)!=0:
            outfile[p.label].write("CA ")
            for ca in p.CA:
                outfile[p.label].write(ca + " | ")
            outfile[p.label].write("\n")
        outfile[p.label].write("\n")
    #print cc
    for i in range(0,top+1):
        outfile[i].close()
    #print tt

readIDmatchLabel(ids,Labels)
readPaperFromFile(inputfile)
papers = sorted(papers,key= lambda Paper:Paper.YR, reverse=False)
print "Total Paper Number: ",len(papers)
printKeyInformation(source_dir)

##other
oo = open(articleMatch,"w")
for p in papers:
    oo.write(p.ID)
    oo.write("\t")
    oo.write(str(p.label))
    oo.write("\n")