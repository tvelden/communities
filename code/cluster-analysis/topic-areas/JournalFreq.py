#Calculate the journal frequency
import sys
import math
top = 12
filein = sys.argv[1]
netin = sys.argv[2]
statsout = sys.argv[3]
#source = "/Users/shiyansiadmin/Dropbox/Files/Field2DataSS1"
ids = netin + "DirectCitationNetworkGiantComponent.net" #giant component
Labels = netin + "DirectCitationNetworkGiantComponent_Synthe2.clu" #partition files
inputfile = filein #input file
target = statsout + "JournalFrequency.txt" #output file

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

journalFreqAll = {}

journalFreqEvery = {}
for i in range(1,50):
    journalFreqEvery[i] = {}

IDmatchLabel = {}
papers = []
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

def readPapersFromFile(File):
    inFile = open(str(File), "r")
    InitialNumberOfPapers = 0
    PaperFlag = 0 # 1 = inside processing a paper, 0 = otherwise
        
    p = Paper()
    for lines in inFile:
        string = str(lines)
        if(string =='\n' or string ==' \n'):
            PaperFlag = 0
            papers.append(p)
            InitialNumberOfPapers = InitialNumberOfPapers +1
            if (p.label<=top) and (p.label>0):
                if p.SO in journalFreqEvery[p.label]:
                    journalFreqEvery[p.label][p.SO] +=1
                else:
                    journalFreqEvery[p.label][p.SO] = 1
            else:
                if p.SO in journalFreqEvery[top+1]:
                    journalFreqEvery[top+1][p.SO] +=1
                else:
                    journalFreqEvery[top+1][p.SO] = 1
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
        elif(string[0] == 'S' and string[1]=='O'):
                #processing SO

                l = len(string)
                p.SO = string[3:l-1]
                if p.SO in journalFreqAll:
                    journalFreqAll[p.SO] += 1
                else: 
                    journalFreqAll[p.SO] = 1      
    inFile.close()
    print 'Read Complete'

readIDmatchLabel(ids,Labels)
readPapersFromFile(inputfile)


outfile = open(target,"w")

for i in range(1,top+2):
    maxfreq = 0
    cc = 0
    if (i!=top+1):
        outfile.write("Area" + str(i) + "\n")
    else:
        outfile.write("Residual Area\n")
    tfs = {}
    idfs = {}
    tfidfs = {}
    jfreqs = {}
    for j in sorted(journalFreqEvery[i], key=journalFreqEvery[i].get, reverse=True):
        cc += 1
        if cc>15:
            break
        if journalFreqEvery[i][j]>maxfreq:
            maxfreq = journalFreqEvery[i][j]
        tf = float(journalFreqEvery[i][j])/float(maxfreq)
        cct = 0
        for t in range(1,top+2):
            c2 = 0
            for l in sorted(journalFreqEvery[t],key=journalFreqEvery[t].get, reverse=True):
                c2 +=1
                if j==l:
                    cct +=1
                    break
                if c2>15:
                    break
        #print cct
        idf = math.log(float(top+1) / float(cct),2)
        idfs[str(j)] = idf
        tfs[str(j)] = tf
        tfidfs[str(j)] = tf*idf
        jfreqs[str(j)] = journalFreqEvery[i][j]
        #outfile.write(str(j) + "	" + str(journalFreqEvery[i][j]) + "	" + str(tf) + "	" +str(idf) +"	" +str(tf*idf) + "\n")
    for j in sorted(tfidfs, key=tfidfs.get, reverse=True):
        outfile.write(str(j) + "	" + str(jfreqs[str(j)]) + "	" + str(tfs[str(j)]) + "	" + str(idfs[str(j)]) + "	" + str(tfidfs[str(j)]) + "\n")


outfile.close()