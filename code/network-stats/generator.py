#This file generates network files of different time-sliced windows
#Author: Syed Ishtiaque Ahmed
#Last Modified: June 27, 2012
# Number of Arguments: 7
# Argument 1: The path of the input file
# Argument 2: The starting year of the first partition
# Argument 3: The ending year of the last partition . 
# Argument 4: type: any of the following three strings: 'discrete', 'sliding', 'accumulative' 
# Argument 5: size of each of the windows
# Argument 6: Filed Name
# Argument 7: Run name

# For example: If you want to generate all the discrete timesliced networks between 1992 to 2002 with a window size of 3 in field1 and run1
# You should pass arguments: <input file path> 1992 2002 discrete 3 field1 run1


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
CumulativeAuthorList = []

def generateNetwork(y1,y2,Partition, path2,field, run,type,s):
    Authors = {}
    NewAuthors = []
    CoAuthorShip = {} #{author:{coauthor:publication with that coauthor}}
    index = 0
    newAuthor = 0
    NewAuthorsNumbers = []
    oldAuthors = []
    oldAuthorsNumbers = []
    activeOldAuthors = []
    activeOldAuthorsNumbers = []
    oldAuthor = 0
    numberOfCumulativeAuthors = 0
    for paper in Partition:
        for author in Partition[paper].AU:
            if(author not in Authors):
                index = index + 1
                Authors[author] = index
            if( Authors[author] not in CoAuthorShip):
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

    activeoldauthornumber = 0
    for e in Authors:
        if e in CumulativeAuthorList:
            activeoldauthornumber = activeoldauthornumber + 1
            activeOldAuthors.append(e)
            activeOldAuthorsNumbers.append(Authors[e])
    
    for e in CumulativeAuthorList:
        oldAuthors.append(e)
        if (e in Authors):
            oldAuthorsNumbers.append(Authors[e])
    
    #number of new authors
    newAuthor = 0
    for author in Authors:
        if author not in CumulativeAuthorList:
            newAuthor = newAuthor + 1
            NewAuthors.append(author)
            CumulativeAuthorList.append(author)
    for e in CumulativeAuthorList:
        numberOfCumulativeAuthors = numberOfCumulativeAuthors +1
        
        
    #new authors making collaboration with at least one new author
    nncount = 0
    for a1 in NewAuthors:
        for a2 in NewAuthors:
            if Authors[a1] in CoAuthorShip[Authors[a2]]:
                nncount = nncount + 1
                flag = 0
                break
    pnn = int((float(nncount)/float(newAuthor)) * 100)
    
    #number of old authors
    oldAuthor = numberOfCumulativeAuthors - newAuthor
    
    #new authors collaborating with at least one old author
    for element in NewAuthors:
        NewAuthorsNumbers.append(Authors[element])
    oldcount = 0    
    for author in NewAuthors:
        for coauthor in CoAuthorShip[Authors[author]]:
            if( coauthor not in NewAuthorsNumbers):
                oldcount = oldcount + 1
                break
    pold = int((float(oldcount)/float(newAuthor)) * 100)
    
    #old author attached to at least one new author
    oldnewcount = 0
    for old in oldAuthors:
        if old in Authors:
            for coauthor in CoAuthorShip[Authors[old]]:
                if( coauthor in NewAuthorsNumbers):
                    oldnewcount = oldnewcount + 1
                    break
    if(oldAuthor != 0):
        poldnew = int((float(oldnewcount)/float(oldAuthor)) * 100)
    else:
        poldnew = 0
    
    #old author attached to at least one old author
    oldoldcount = 0
    for old in oldAuthors:
        if old in Authors:
            for coauthor in CoAuthorShip[Authors[old]]:
                if( coauthor in oldAuthorsNumbers):
                    oldoldcount = oldoldcount + 1
                    break
    if(oldAuthor!=0):
        poldold = int((float(oldoldcount)/float(oldAuthor)) * 100)
        poldany = int((float(activeoldauthornumber)/float(oldAuthor)) * 100)
        if (poldany > 1000):
            print numberOfCumulativeAuthors, activeoldauthornumber, oldAuthor, newAuthor
    else:
        poldold = 0
        poldany = 0
    
    
    #printing statistics
    statfs = path2 
    statfile = open(statfs,'a')
    statfile.write(str(y1) + ';' + str(y2) + ';' + str(numberOfCumulativeAuthors) + ';' + str(newAuthor) + ';' +str(nncount) + ';' + str(pnn) + ';' +str(oldcount) + ';' + str(pold) + ';' + str(oldnewcount) + ';' + str(poldnew) + ';' +str(oldoldcount) + ';' + str(poldold) + ';' +str(activeoldauthornumber) + ';' + str(poldany))
    statfile.write('\n')
    statfile.close()
    
    
def partitionNetwork(y1, y2, type, s, field, run, path2):
    year1 = int(y1)
    year2 = int(y2)
    size = int(s)
    Partition = {}
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
            generateNetwork(start,end,Partition,path2, field, run, type,s)
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
            generateNetwork(start,end,Partition, path2, field, run, type,s)
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
            generateNetwork(start,end,Partition, path2, field, run, type,s)
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
    path2 = path + '/' + str(field) + '/' + str(run) + '/output/Statistics'
    if not os.path.exists(path2):
        os.makedirs(path2)
        print('New directory made: ' + str(path2))
    path2 = path2 + '/' + str(field) + '-' + str(run) + '_new-author-linking_' +str(type) + str(y1)+'-'+str(y2)+'_'+str(s)+'years' + '.csv'
    file = open(path2,'w')
    file.write('Start_Year, End_Year; Cumulative_No_of_Authors; No_of_New_Authors; No_Of_New_Authors_Connected_to_atleast_one_new_author; percent; No_Of_New_Authors_Connected_to_atleast_one_old_author; percent; No_Of_Old_Authors_Connected_to_atleast_one_new_author; percent, No_Of_Old_Authors_Connected_to_atleast_one_old_author; No_Of_Old_Authors_Connected_to_atleast_one_any_author; percent\n' )
    file.close()
    return path2

def getParameters():
    path = str(os.getcwd())
    l = len(path) - 1
    #now at pwd
    while(path[l]!='/'):
        l = l -1
    l = l -1
    # now at code directory
    while(path[l]!='/'):
        l = l -1
    # now at communities directory
    origin = path[0:l]
    path = path[0:l] + '/parameters/parameters-global.txt'
    print path
    while(path[l]!='/'):
        l = l -1
    l = l-1
    while(path[l]!='/'):
        l = l -1
    origin = origin[0:l]
    print origin
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
            print field
        elif(line[0:4] == 'RUN='):
            run = line[4:(l-1)]
            print run
        elif(line[0:11] == 'START_YEAR='):
            start_year = line[11:(l-1)]
            print start_year
        elif(line[0:9] == 'END_YEAR='):
            end_year = line[9:(l-1)]
            print end_year
        elif(line[0:5] == 'TYPE='):
            type = line[5:(l-1)]
            print type
        elif(line[0:5] == 'SIZE='):
            size = line[5:(l-1)]
            print size
        elif(line[0:11] == 'INPUT_PATH='):
            ip = line[11:(l-1)]
            input_path = origin + ip[2:(len(ip))]
            print input_path
        elif(line[0:12] == 'OUTPUT_PATH='):
            op = line[12:(l-1)]
            output_path = origin + op[2:(len(op))]
            #output_path = origin + '/Test/ProjectRoot/runs/'
            print output_path
    print field, run, start_year, end_year, type, size, input_path, output_path        
    return field, run, start_year, end_year, type, size, input_path, output_path 
    
if __name__ == "__main__":
    #input_path, start_year, end_year, type, size , field , run
    field, run, start_year, end_year, type, size, input_path, output_path  = getParameters()
    readAllPapers(input_path)
    output_path = processPath(start_year, end_year, type, size, field, run, output_path)
    partitionNetwork(start_year, end_year, type, size, field, run, output_path)
