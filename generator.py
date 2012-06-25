#This file generates network files of different time-sliced windows
#Author: Syed Ishtiaque Ahmed
#Last Modified: June 22, 2012
# Number of Arguments: 6
# Argument 1: The path of the input file
# Argument 2: The path of the output DIRECTORY

# Argument 3: The starting year of the first partition
# Argument 4: The ending year of the last partition . 
# Argument 5: type: any of the following three strings: 'discrete', 'sliding', 'accumulative' 
# Argument 6: size of each of the windows
# Argument 7: Filed Name
# Argument 8: Run name

# For example: If you want to generate all the discrete timesliced networks between 1992 to 2002 with a window size of 3
# You should pass arguments: <input file path> <output directory path> 1992 2002 discrete 3


import os
import sys
import operator
from operator import itemgetter

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
        self.YR = ''

#Global variables
AllPapers = {} #{paper_id:<paper_object>}
Productivity = {} #{author_name:[number_of_papers,[paperlist]]}
PublicationByYear = {} #{year:[list of paper_ids published in that year]}

def generateNetwork(y1,y2,Partition,path,field, run):
    Authors = {}
    CoAuthorShip = {} #{author:{coauthor:publication with that coauthor}}
    index = 0
    for paper in Partition:
        for author in Partition[paper].AU:
            if(author not in Authors):
                index = index + 1
                Authors[author] = index
            if author not in CoAuthorShip:
                CoAuthorShip[Authors[author]] = {}
            
        for author1 in Partition[paper].AU:
            for author2 in Partition[paper].AU:
                #print Authors[author1],Authors[author2]
                if(Authors[author1] < Authors[author2]):
                    if(Authors[author2] not in CoAuthorShip[Authors[author1]]):
                        CoAuthorShip[Authors[author1]][Authors[author2]] = 1
                    else:
                        CoAuthorShip[Authors[author1]][Authors[author2]] = CoAuthorShip[Authors[author1]][Authors[author2]] + 1
                        
                    if(Authors[author1] not in CoAuthorShip[Authors[author2]]):
                        CoAuthorShip[Authors[author2]][Authors[author1]] = 1
                    else:
                        CoAuthorShip[Authors[author2]][Authors[author1]] = CoAuthorShip[Authors[author2]][Authors[author1]] + 1
                    
    fs = path + '/' str(field) + '-' + str(run) + 'CoAuthorshipNetwork_'+ str(y1) + '-' + str(y2) + '.net' 
    outFile = open(fs,'w')
    #outFile.write('%START\n')
    #outFile.write('%' + str(y1) + '\n')
    #outFile.write('%END\n')
    #outFile.write('%' + str(y2) + '\n')
    outFile.write('*Vertices ' + str(index) + '\n')
    al = sorted(Authors.items(),key=itemgetter(1))
    for author in al:
        outFile.write('"' + str(author[1]) + ' ' + str(author[0]) + '"' + '\n')
    outFile.write('*Edges\n')
    for author in CoAuthorShip:
        for coauthor in CoAuthorShip[author]:
            if(author < coauthor):
                outFile.write(str(author) + ' ' + str(coauthor) + str(CoAuthorShip[author][coauthor]) + '\n')
    outFile.close()


def partitionNetwork(y1, y2, type, s, path, field, run):
    year1 = int(y1)
    year2 = int(y2)
    size = int(s)
    if(type == 'discrete'):
        start = year1
        end = year1 + size -1
        while(end<=year2):
            Partition = {}
            i = start
            while(i<=end):
                for paper in PublicationByYear[i]:
                    Partition[paper] = AllPapers[paper]
                i = i +1
            generateNetwork(start,end,Partition,path, field, run)
            start = end + 1
            end = end + size
    elif(type == 'accumulative'):
        start = year1
        end = year1 + size -1
        while(end<=year2):
            Partition = {}
            i = start
            while(i<=end):
                for paper in PublicationByYear[i]:
                    Partition[paper] = AllPapers[paper]
                i = i +1
            generateNetwork(start,end,Partition,path, field, run)
            end = end + size
    elif(type == 'sliding'):
        start = year1
        end = year1 + size -1
        while(end<=year2):
            Partition = {}
            i = start
            while(i<=end):
                for paper in PublicationByYear[i]:
                    Partition[paper] = AllPapers[paper]
                i = i +1
            generateNetwork(start,end,Partition,path, field, run)
            start = start + 1
            end = end + 1

def readAllPapers(inputFile):
    global AllPapers
    AllPapers = {}
    global PublicationByYear
    PublicationByYear = {}
    path = str(inputFile)
    inFile = open(path, "r")
    InitialNumberOfPapers = 0
    PaperFlag = 0 # 1 = inside processing a paper, 0 = otherwise
    p = Paper()
    
    for lines in inFile:
        string = str(lines)
        #print string
        if(len(string) == 1):
            PaperFlag = 0
            AllPapers[p.ID] = p
            InitialNumberOfPapers = InitialNumberOfPapers +1
            p = Paper()
            continue
        if(string[0] == 'I' and string[1]=='D'):
            PaperFlag = 1
            #processing ID
            l = len(string)
            p.ID = string[3:l-1]
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
            p.YR = string[l-5:l-1]
            Y = int(p.YR)
            if(Y not in PublicationByYear):
                paperArray = []
                paperArray.append(p.ID)
                PublicationByYear[Y] = paperArray
            else:
                PublicationByYear[Y].append(p.ID)
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
    
    #print AllPapers
    #print Productivity
    inFile.close()

if __name__ == "__main__":
    #input_path, outputpath, start_year, end_year, type, size
    readAllPapers(sys.argv[1])
    partitionNetwork(sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[2],sys.argv[7], sys.argv[8])
