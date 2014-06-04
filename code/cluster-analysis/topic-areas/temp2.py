#temp count the percentage of shared authors for top 11 clusters
ids = "/Users/shiyansiadmin/Dropbox/Files/Field3Data1/DirectCitationNetworkGiantComponent.net" #giant component
Labels = "/Users/shiyansiadmin/Dropbox/Files/Field3Data1/DirectCitationNetworkGiantComponent_Synthe2.clu" #partition files
inputfile = "/Users/shiyansiadmin/Dropbox/Files/Field3Data1/in.txt" #input file
top = 11
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

papers = []
authorlist = {}
for i in range(1,top+1):
    authorlist[i] = []

def readPaperFromFile(File):
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
            if (p.label!=0) and (p.label<=top):
                for au in p.AU:
                    if au in authorlist[p.label]:
                       continue
                    authorlist[p.label].append(au)

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
readIDmatchLabel(ids,Labels)
readPaperFromFile(inputfile)
for i in range(1,top+1):
    suma = []
    for j in range (1,top+1):
        if i==j:
            continue
        suma = list(set(suma) | set(authorlist[j]))
    de = len(authorlist[i])
    no = len(list(set(authorlist[i]) & set(suma) ))
    perce = float(no) / float(de)
    print str(i) + "  " + str(perce)
