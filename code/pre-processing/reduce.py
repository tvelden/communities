#Decrition: This file removes the single-paper-authors from the dataset
#Author: Syed Ishtiaque Ahmed
#Last Modified: June 27, 2012
#No. of Arguments: 2 (more than 2 is fine, the rests will be ignored)
#Argument 1: The path of the original input file. Example: '/Academic/CoAuthor/Test/in.txt'
#Argument 2: The path of the expected output file that has to be written. Example: '/Academic/CoAuthor/Test/reducedData.txt'


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
SinglePaperAuthors = []
PapersToDelete = []


def removeSignlePaperAuthors(p):
    global AllPapers
    global PublicationByYear
    global Productivity
    global SinglePaperAuthors 
    global PapersToDelete
    
    DeletedAuthors = 0
    
    NumberOfDeletedPapers = 0
    ReducedNumberOfPapers = 0
    
    for author in Productivity:
        if(Productivity[author][0] == 1):
            SinglePaperAuthors.append(author)
            DeletedAuthors = DeletedAuthors + 1
    print('Number of Deleted Authors: ' + str(DeletedAuthors) + '\n')
    
    for paper in AllPapers:
        for author in AllPapers[paper].AU:
            if(author in SinglePaperAuthors):
                AllPapers[paper].AU.remove(author)
                #print('Removing author: ' + str(author))
        if(len(AllPapers[paper].AU)<=1):
            PapersToDelete.append(paper)
    
    
    for paper in PapersToDelete:
        del AllPapers[paper]
        #print('Deleting paper: ' + str(paper))
        NumberOfDeletedPapers = NumberOfDeletedPapers + 1
    print('Number of Deleted papers: ' + str(NumberOfDeletedPapers) + '\n')
    
    #writing the reduced file
    path = str(p)
    outFile = open(path, "w")
    for paper in AllPapers:
        outFile.write('ID ' + str(AllPapers[paper].ID) + '\n')
        outFile.write('CI ' + str(AllPapers[paper].CI) + '\n')
        outFile.write('SO ' + str(AllPapers[paper].SO) + '\n')
        outFile.write('TI ' + str(AllPapers[paper].TI) + '\n')
        outFile.write('BI ' + str(AllPapers[paper].BI) + '\n')
        if(len(AllPapers[paper].AU)>0 ):
            outFile.write('AU')
            for author in AllPapers[paper].AU:
                outFile.write(' ' + str(author) + '\n')
        for element in AllPapers[paper].AF:
            outFile.write('AF ' + str(element) + '\n')
        for element in AllPapers[paper].CT:
            outFile.write('CT ' + str(element) + '\n')
        for element in AllPapers[paper].CO:
            outFile.write('CO ' + str(element) + '\n')
        for element in AllPapers[paper].RF:
            outFile.write('RF ' + str(element) + '\n')
        for element in AllPapers[paper].CA:
            outFile.write('CA ' + str(element) + '\n')
        outFile.write('\n')
        ReducedNumberOfPapers = ReducedNumberOfPapers + 1
    outFile.close()
    print('Remaining Number of Papers: ' + str(ReducedNumberOfPapers) + '\n')
    
    
def readAllPapers(p):
    global AllPapers
    AllPapers = {}
    global PublicationByYear
    PublicationByYear = {}
    global Productivity
    Productivity = {}
    
    TotalAuthors = 0
    
    path = str(p)
    inFile = open(path, "r")
    InitialNumberOfPapers = 0
    PaperFlag = 0 # 1 = inside processing a paper, 0 = otherwise
    p = Paper()
    
    for lines in inFile:
        string = str(lines)
        #print string
        if(string == '\n' or string == ' \n'):
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
        elif(string[0] == 'A' and string[1]=='U'):
            #processing AU
            l = len(string)
            s = string[3:l-1]    
            p.AU.append(s)
            if s in Productivity:
                Productivity[s][0] = Productivity[s][0] + 1
                Productivity[s][1].append(p.ID)
            else:
                TotalAuthors = TotalAuthors + 1
                paperlist = []
                paperlist.append(p.ID)
                production = []
                production.append(1)
                production.append(paperlist)
                Productivity[s] = production
        elif((string[0] == ' ') and (PaperFlag==1)):
            l = len(string)
            s = string[1:l-1]    
            p.AU.append(s)
            if s in Productivity:
                Productivity[s][0] = Productivity[s][0] + 1
                Productivity[s][1].append(p.ID)
            else:
                paperlist = []
                paperlist.append(p.ID)
                production = []
                production.append(1)
                production.append(paperlist)
                Productivity[s] = production
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
    print('Initially Total Number of Papers was: ' + str(InitialNumberOfPapers) + '\n')
    print('Initially Total Number of Authors was: ' + str(TotalAuthors) + '\n')
    inFile.close()


if __name__ == "__main__":
    readAllPapers(sys.argv[1])
    removeSignlePaperAuthors(sys.argv[2])