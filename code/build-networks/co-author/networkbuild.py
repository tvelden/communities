#This file generates network files of different time-sliced windows
#Author: Syed Ishtiaque Ahmed
#Last Modified: June 27, 2012
#Takes input from parameter file in communities/parameters


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
                    
    fs = path + '/' + str(field) + '-' + str(run) + 'CoAuthorshipNetwork_'+ str(y1) + '-' + str(y2) + '.net' 
    outFile = open(fs,'w')
    #outFile.write('%START\n')
    #outFile.write('%' + str(y1) + '\n')
    #outFile.write('%END\n')
    #outFile.write('%' + str(y2) + '\n')
    outFile.write('*Vertices ' + str(index) + '\n')
    al = sorted(Authors.items(),key=itemgetter(1))
    for author in al:
        outFile.write(str(author[1]) + ' "'  + str(author[0]) + '"' + '\n')
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

def processPath(y1,y2,type,s, field, run, path):
    path1 = path + '/' + str(field) + '/' + str(run) + '/output/Network/' + str(type) + str(y1)+'-'+str(y2)+'_'+str(s)+'years'
    if not os.path.exists(path1):
        os.makedirs(path1)
        print('New directory made: ' + str(path1))

    return path1

def getParameters():
    path = str(os.getcwd())
    print('present directory of networkbuild.py: ' + str(path))
    l = len(path) - 1
    #now at pwd
    while(path[l]!='/'):
        l = l -1
    l = l -1
    # now at build-networks directory
    while(path[l]!='/'):
        l = l -1
    l = l -1
    # now at code directory
    while(path[l]!='/'):
        l = l -1
    # now at communities directory
    print('communties directory: ' + str(path[0:l]))
    origin = path[0:l]
    path = path[0:l] + '/parameters/parameters-global.txt'
    print('parameter file: ' + str(path))
    while(path[l]!='/'):
        l = l -1
    l = l-1
    while(path[l]!='/'):
        l = l -1
    origin = origin[0:l]
    print('origin: ' + str(origin))
    field = ''
    run = ''
    start_year = ''
    end_year = ''
    type = ''
    size = ''
    input_path = ''
    output_path = ''
    
    parameterfile = open(path, "r")
    for line in parameterfile:
        l = len(line)
        if(line[0:6] == 'FIELD='):
            field = line[6:(l-1)]
            #print field
        elif(line[0:4] == 'RUN='):
            run = line[4:(l-1)]
            #print run
        elif(line[0:11] == 'START_YEAR='):
            start_year = line[11:(l-1)]
            #print start_year
        elif(line[0:9] == 'END_YEAR='):
            end_year = line[9:(l-1)]
            #print end_year
        elif(line[0:5] == 'TYPE='):
            type = line[5:(l-1)]
            #print type
        elif(line[0:5] == 'SIZE='):
            size = line[5:(l-1)]
            #print size
        elif(line[0:11] == 'INPUT_PATH='):
            ip = line[11:(l-1)]
            input_path = origin + ip[2:(len(ip))]
            print('input file path: ' + str(input_path))
        elif(line[0:12] == 'OUTPUT_PATH='):
            op = line[12:(l-1)]
            output_path = origin + op[2:(len(op))]
            output_path = origin + '/Test/ProjectRoot/runs/'
            print('output directory runs path: ' + str(output_path))
    print field, run, start_year, end_year, type, size, input_path, output_path        
    return field, run, start_year, end_year, type, size, input_path, output_path 
            
if __name__ == "__main__":
    #input_path, outputpath, start_year, end_year, type, size
    field, run, start_year, end_year, type, size, input_path, output_path  = getParameters()
    readAllPapers(input_path)
    output_path = processPath(start_year, end_year, type, size, field, run, output_path)
    partitionNetwork(start_year, end_year, type, size, output_path, field, run)